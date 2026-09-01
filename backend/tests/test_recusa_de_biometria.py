from datetime import timedelta

import pytest

from nucleo.consentimentos.modelo import (
    Consentimento,
    DecisaoDeConsentimento,
    OrigemDoConsentimento,
    TipoDeConsentimento,
)
from nucleo.consentimentos.regra import recusar_biometria
from nucleo.erros import PermissaoNegada
from nucleo.personas.modelo import Papel
from nucleo.responsaveis.regra import criar_vinculo

VERSAO_DO_TERMO = "2026-09"


@pytest.fixture
def cenario(sessao, criar_persona):
    def _montar():
        admin = criar_persona(Papel.admin)
        responsavel = criar_persona(Papel.responsavel, criada_por=admin)
        guerreiro = criar_persona(Papel.guerreiro)
        criar_vinculo(
            sessao,
            responsavel=responsavel,
            guerreiro_id=guerreiro.id,
            grau_de_parentesco="mãe",
            cadastrado_por=admin,
        )
        sessao.commit()
        return {"admin": admin, "responsavel": responsavel, "guerreiro": guerreiro}

    return _montar


def test_recusa_grava_consentimento_de_biometria_com_origem_propria(sessao, cenario):
    c = cenario()

    consentimento, _apagar_em = recusar_biometria(
        sessao,
        responsavel=c["responsavel"],
        guerreiro_id=c["guerreiro"].id,
        versao_do_termo=VERSAO_DO_TERMO,
    )
    sessao.commit()

    assert consentimento.tipo == TipoDeConsentimento.biometria
    assert consentimento.decisao == DecisaoDeConsentimento.nega
    assert consentimento.origem == OrigemDoConsentimento.propria
    assert consentimento.versao_do_termo == VERSAO_DO_TERMO
    assert consentimento.responsavel_id == c["responsavel"].id


def test_guerreiro_nao_vinculado_e_recusado_com_403(sessao, criar_persona):
    admin = criar_persona(Papel.admin)
    responsavel = criar_persona(Papel.responsavel, criada_por=admin)
    guerreiro = criar_persona(Papel.guerreiro)

    with pytest.raises(PermissaoNegada):
        recusar_biometria(
            sessao,
            responsavel=responsavel,
            guerreiro_id=guerreiro.id,
            versao_do_termo=VERSAO_DO_TERMO,
        )
    assert sessao.query(Consentimento).count() == 0


def test_recusa_nao_mexe_na_autorizacao_unica(sessao, cenario):
    from nucleo.consentimentos.regra import decidir_autorizacao, ler_autorizacao

    c = cenario()
    decidir_autorizacao(
        sessao,
        responsavel=c["responsavel"],
        guerreiro_id=c["guerreiro"].id,
        decisao=DecisaoDeConsentimento.concede,
        versao_do_termo="1.0",
    )
    sessao.commit()

    recusar_biometria(
        sessao,
        responsavel=c["responsavel"],
        guerreiro_id=c["guerreiro"].id,
        versao_do_termo=VERSAO_DO_TERMO,
    )
    sessao.commit()

    leitura = ler_autorizacao(sessao, guerreiro_id=c["guerreiro"].id)
    assert leitura.estado.value == "vigente"


def test_recusa_repetida_nao_gera_segundo_registro(sessao, cenario):
    c = cenario()

    primeira, _ = recusar_biometria(
        sessao,
        responsavel=c["responsavel"],
        guerreiro_id=c["guerreiro"].id,
        versao_do_termo=VERSAO_DO_TERMO,
    )
    sessao.commit()

    segunda, _ = recusar_biometria(
        sessao,
        responsavel=c["responsavel"],
        guerreiro_id=c["guerreiro"].id,
        versao_do_termo=VERSAO_DO_TERMO,
    )
    sessao.commit()

    assert segunda.id == primeira.id
    assert (
        sessao.query(Consentimento)
        .filter_by(guerreiro_id=c["guerreiro"].id, tipo=TipoDeConsentimento.biometria)
        .count()
        == 1
    )


def test_recusa_devolve_a_data_do_apagamento_cinco_dias_a_frente(
    sessao, cenario, criar_template_biometrico
):
    c = cenario()
    criar_template_biometrico(c["guerreiro"])

    _consentimento, apagar_em = recusar_biometria(
        sessao,
        responsavel=c["responsavel"],
        guerreiro_id=c["guerreiro"].id,
        versao_do_termo=VERSAO_DO_TERMO,
    )
    sessao.commit()

    assert apagar_em is not None
    diferenca = apagar_em - consentimento_registrado_em(sessao, c["guerreiro"].id)
    assert abs(diferenca - timedelta(days=5)) < timedelta(seconds=5)


def consentimento_registrado_em(sessao, guerreiro_id):
    return (
        sessao.query(Consentimento)
        .filter_by(guerreiro_id=guerreiro_id, tipo=TipoDeConsentimento.biometria)
        .one()
        .registrado_em
    )


def test_recusa_sobre_quem_nao_tem_template_nao_traz_data(sessao, cenario):
    c = cenario()

    _consentimento, apagar_em = recusar_biometria(
        sessao,
        responsavel=c["responsavel"],
        guerreiro_id=c["guerreiro"].id,
        versao_do_termo=VERSAO_DO_TERMO,
    )
    sessao.commit()

    assert apagar_em is None


def test_recusa_nao_exclui_o_guerreiro_de_nada(sessao, cenario, criar_template_biometrico):
    from nucleo.personas.modelo import Persona

    c = cenario()
    criar_template_biometrico(c["guerreiro"])

    recusar_biometria(
        sessao,
        responsavel=c["responsavel"],
        guerreiro_id=c["guerreiro"].id,
        versao_do_termo=VERSAO_DO_TERMO,
    )
    sessao.commit()

    assert sessao.get(Persona, c["guerreiro"].id) is not None
