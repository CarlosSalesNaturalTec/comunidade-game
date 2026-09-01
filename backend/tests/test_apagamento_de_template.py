from datetime import UTC, datetime, timedelta

import pytest

from nucleo.biometria.modelo import (
    AcessoAoTemplate,
    ApagamentoDeTemplate,
    DesfechoDoAcesso,
    GatilhoDeApagamento,
    NaturezaDoAcesso,
)
from nucleo.biometria.regra import (
    PRAZO_DE_APAGAMENTO_POR_GATILHO,
    apagar_templates_vencidos,
    autenticar_por_nick_e_descritor,
    marcar_apagamento,
)
from nucleo.personas.modelo import Credencial, Papel, Persona, TipoDeCredencial

DESCRITOR = [0.1, 0.2, 0.3, 0.4]


@pytest.mark.parametrize(
    "gatilho",
    [
        GatilhoDeApagamento.exclusao_deferida,
        GatilhoDeApagamento.recusa_biometria,
        GatilhoDeApagamento.fim_do_vinculo,
    ],
)
def test_cada_gatilho_marca_no_prazo_do_documento_03(
    sessao, criar_persona, criar_template_biometrico, gatilho
):
    guerreiro = criar_persona(Papel.guerreiro)
    criar_template_biometrico(guerreiro)

    apagamento = marcar_apagamento(sessao, guerreiro_id=guerreiro.id, gatilho=gatilho)
    sessao.commit()

    assert apagamento is not None
    assert apagamento.gatilho == gatilho
    diferenca = apagamento.apagar_em - apagamento.criado_em
    assert abs(diferenca - PRAZO_DE_APAGAMENTO_POR_GATILHO[gatilho]) < timedelta(seconds=5)


def test_guerreiro_sem_template_nao_marca_nem_falha(sessao, criar_persona):
    guerreiro = criar_persona(Papel.guerreiro)

    apagamento = marcar_apagamento(
        sessao, guerreiro_id=guerreiro.id, gatilho=GatilhoDeApagamento.recusa_biometria
    )
    sessao.commit()

    assert apagamento is None
    assert sessao.query(ApagamentoDeTemplate).count() == 0


def test_marca_nao_se_substitui_nem_se_adia_por_gatilho_posterior(
    sessao, criar_persona, criar_template_biometrico
):
    guerreiro = criar_persona(Papel.guerreiro)
    criar_template_biometrico(guerreiro)

    primeira = marcar_apagamento(
        sessao, guerreiro_id=guerreiro.id, gatilho=GatilhoDeApagamento.recusa_biometria
    )
    sessao.commit()

    segunda = marcar_apagamento(
        sessao, guerreiro_id=guerreiro.id, gatilho=GatilhoDeApagamento.fim_do_vinculo
    )
    sessao.commit()

    assert segunda.id == primeira.id
    assert segunda.gatilho == GatilhoDeApagamento.recusa_biometria
    assert segunda.apagar_em == primeira.apagar_em
    assert sessao.query(ApagamentoDeTemplate).filter_by(guerreiro_id=guerreiro.id).count() == 1


def test_apagar_templates_vencidos_destroi_o_cifrado_e_audita_sem_descritor(
    sessao, criar_persona, criar_template_biometrico
):
    guerreiro = criar_persona(Papel.guerreiro)
    criar_template_biometrico(guerreiro, descritor=DESCRITOR)
    marcar_apagamento(
        sessao, guerreiro_id=guerreiro.id, gatilho=GatilhoDeApagamento.recusa_biometria
    )
    vencido = sessao.query(ApagamentoDeTemplate).filter_by(guerreiro_id=guerreiro.id).one()
    vencido.apagar_em = datetime.now(UTC) - timedelta(seconds=1)
    sessao.commit()

    apagados = apagar_templates_vencidos(sessao)
    sessao.commit()

    assert apagados == 1
    assert (
        sessao.query(Credencial)
        .filter_by(persona_id=guerreiro.id, tipo=TipoDeCredencial.biometria, ativa=True)
        .count()
        == 0
    )

    acesso = (
        sessao.query(AcessoAoTemplate)
        .filter_by(guerreiro_id=guerreiro.id, natureza=NaturezaDoAcesso.apagamento)
        .one()
    )
    assert acesso.desfecho == DesfechoDoAcesso.sucesso
    assert acesso.acessado_por is None


def test_auditoria_anterior_permanece_depois_do_apagamento(
    sessao, criar_persona, criar_template_biometrico
):
    guerreiro = criar_persona(Papel.guerreiro)
    criar_template_biometrico(guerreiro, descritor=DESCRITOR)

    acesso_anterior = AcessoAoTemplate(
        guerreiro_id=guerreiro.id,
        acessado_por=None,
        natureza=NaturezaDoAcesso.comparacao_de_login,
        desfecho=DesfechoDoAcesso.sucesso,
    )
    sessao.add(acesso_anterior)
    sessao.commit()

    marcar_apagamento(
        sessao, guerreiro_id=guerreiro.id, gatilho=GatilhoDeApagamento.recusa_biometria
    )
    vencido = sessao.query(ApagamentoDeTemplate).filter_by(guerreiro_id=guerreiro.id).one()
    vencido.apagar_em = datetime.now(UTC) - timedelta(seconds=1)
    sessao.commit()

    apagar_templates_vencidos(sessao)
    sessao.commit()

    assert sessao.get(AcessoAoTemplate, acesso_anterior.id) is not None


def test_entrada_por_imagem_deixa_de_conferir_apos_apagamento(
    sessao, configuracao, criar_persona, criar_nick, criar_template_biometrico
):
    guerreiro = criar_persona(Papel.guerreiro)
    criar_nick(guerreiro, "guerreiro_apagado")
    criar_template_biometrico(guerreiro, descritor=DESCRITOR)
    marcar_apagamento(
        sessao, guerreiro_id=guerreiro.id, gatilho=GatilhoDeApagamento.recusa_biometria
    )
    vencido = sessao.query(ApagamentoDeTemplate).filter_by(guerreiro_id=guerreiro.id).one()
    vencido.apagar_em = datetime.now(UTC) - timedelta(seconds=1)
    sessao.commit()
    apagar_templates_vencidos(sessao)
    sessao.commit()

    resultado = autenticar_por_nick_e_descritor(
        sessao, configuracao, nick="guerreiro_apagado", descritor=DESCRITOR
    )

    assert resultado is None


def test_desfecho_recusado_nao_marca_nada(sessao, criar_persona, criar_template_biometrico):
    """RN-13-22: só o desfecho aceito, do tipo exclusão, é gatilho — este
    teste garante que `marcar_apagamento` nunca é chamada por si só sem um
    gatilho explícito, e que nenhuma marca nasce por acaso."""
    guerreiro = criar_persona(Papel.guerreiro)
    criar_template_biometrico(guerreiro)

    assert sessao.query(ApagamentoDeTemplate).filter_by(guerreiro_id=guerreiro.id).count() == 0


def test_participacao_do_guerreiro_segue_intacta_apos_apagamento(
    sessao, criar_persona, criar_template_biometrico
):
    guerreiro = criar_persona(Papel.guerreiro)
    criar_template_biometrico(guerreiro)
    marcar_apagamento(
        sessao, guerreiro_id=guerreiro.id, gatilho=GatilhoDeApagamento.recusa_biometria
    )
    vencido = sessao.query(ApagamentoDeTemplate).filter_by(guerreiro_id=guerreiro.id).one()
    vencido.apagar_em = datetime.now(UTC) - timedelta(seconds=1)
    sessao.commit()

    apagar_templates_vencidos(sessao)
    sessao.commit()

    ainda_existe = sessao.get(Persona, guerreiro.id)
    assert ainda_existe is not None
    assert ainda_existe.papel == Papel.guerreiro
