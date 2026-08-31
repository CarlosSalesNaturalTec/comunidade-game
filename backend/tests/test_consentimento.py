from datetime import UTC, datetime

import pytest
from sqlalchemy import text
from sqlalchemy.exc import DBAPIError

from nucleo.consentimentos.modelo import (
    Consentimento,
    DecisaoDeConsentimento,
    OrigemDoConsentimento,
    TipoDeConsentimento,
)
from nucleo.consentimentos.regra import (
    EstadoDaAutorizacao,
    autorizacao_de_divulgacao_vigente,
    consultar_consentimento_vigente_em,
    decidir_autorizacao,
    ler_autorizacao,
    registrar_consentimento,
)
from nucleo.erros import (
    AutorizacaoSuspensaPorOutroResponsavel,
    ConsentimentoImutavel,
    ErroDeValidacao,
    PermissaoNegada,
    RevogacaoSemAutorizacaoVigente,
)
from nucleo.personas.modelo import Papel, Persona
from nucleo.responsaveis.regra import cadastrar_responsavel, criar_vinculo
from nucleo.solicitacoes_do_responsavel.modelo import SolicitacaoDoResponsavel

TIPO = TipoDeConsentimento.autorizacao_de_divulgacao


def _vincular(sessao, responsavel, guerreiro, cadastrado_por):
    return criar_vinculo(
        sessao,
        responsavel=responsavel,
        guerreiro_id=guerreiro.id,
        grau_de_parentesco="mãe",
        cadastrado_por=cadastrado_por,
    )


def _responsavel_vinculado(sessao, admin, guerreiro, nome="mãe"):
    responsavel = cadastrar_responsavel(sessao, criado_por=admin, nome=nome)
    _vincular(sessao, responsavel, guerreiro, admin)
    return responsavel


def test_registro_guarda_o_que_valia(sessao, criar_persona):
    admin = criar_persona(Papel.admin)
    responsavel = cadastrar_responsavel(sessao, criado_por=admin, nome="mãe")
    guerreiro = criar_persona(Papel.guerreiro)
    _vincular(sessao, responsavel, guerreiro, admin)

    consentimento = registrar_consentimento(
        sessao,
        responsavel=responsavel,
        guerreiro_id=guerreiro.id,
        tipo=TIPO,
        versao_do_termo="1.0",
        decisao=DecisaoDeConsentimento.concede,
        origem=OrigemDoConsentimento.propria,
        operado_por=responsavel,
    )
    sessao.commit()

    assert consentimento.versao_do_termo == "1.0"
    assert consentimento.decisao == DecisaoDeConsentimento.concede
    assert consentimento.autor_id == responsavel.id
    assert consentimento.papel_do_autor == Papel.responsavel.value
    assert consentimento.registrado_em is not None


def test_consentimento_sem_versao_do_termo_e_recusado(sessao, criar_persona):
    admin = criar_persona(Papel.admin)
    responsavel = cadastrar_responsavel(sessao, criado_por=admin, nome="mãe")
    guerreiro = criar_persona(Papel.guerreiro)
    _vincular(sessao, responsavel, guerreiro, admin)

    with pytest.raises(ErroDeValidacao) as excinfo:
        registrar_consentimento(
            sessao,
            responsavel=responsavel,
            guerreiro_id=guerreiro.id,
            tipo=TIPO,
            versao_do_termo="",
            decisao=DecisaoDeConsentimento.concede,
            origem=OrigemDoConsentimento.propria,
            operado_por=responsavel,
        )
    assert excinfo.value.campo == "versao_do_termo"
    assert sessao.query(Consentimento).count() == 0


def test_responsavel_nao_consente_por_crianca_que_nao_e_sua(sessao, criar_persona):
    admin = criar_persona(Papel.admin)
    responsavel = cadastrar_responsavel(sessao, criado_por=admin, nome="mãe")
    guerreiro_sem_vinculo = criar_persona(Papel.guerreiro)

    with pytest.raises(PermissaoNegada):
        registrar_consentimento(
            sessao,
            responsavel=responsavel,
            guerreiro_id=guerreiro_sem_vinculo.id,
            tipo=TIPO,
            versao_do_termo="1.0",
            decisao=DecisaoDeConsentimento.concede,
            origem=OrigemDoConsentimento.propria,
            operado_por=responsavel,
        )
    assert sessao.query(Consentimento).count() == 0


def test_revogar_cria_registro_novo_e_anterior_continua_consultavel(sessao, criar_persona):
    admin = criar_persona(Papel.admin)
    responsavel = cadastrar_responsavel(sessao, criado_por=admin, nome="mãe")
    guerreiro = criar_persona(Papel.guerreiro)
    _vincular(sessao, responsavel, guerreiro, admin)

    concedido = registrar_consentimento(
        sessao,
        responsavel=responsavel,
        guerreiro_id=guerreiro.id,
        tipo=TIPO,
        versao_do_termo="1.0",
        decisao=DecisaoDeConsentimento.concede,
        origem=OrigemDoConsentimento.propria,
        operado_por=responsavel,
    )
    sessao.commit()

    revogado = registrar_consentimento(
        sessao,
        responsavel=responsavel,
        guerreiro_id=guerreiro.id,
        tipo=TIPO,
        versao_do_termo="1.0",
        decisao=DecisaoDeConsentimento.nega,
        origem=OrigemDoConsentimento.propria,
        operado_por=responsavel,
    )
    sessao.commit()

    assert revogado.id != concedido.id
    assert sessao.query(Consentimento).count() == 2

    ainda_consultavel = sessao.get(Consentimento, concedido.id)
    assert ainda_consultavel is not None
    assert ainda_consultavel.decisao == DecisaoDeConsentimento.concede


def test_consentimento_gravado_nao_e_editado_nem_apagado_no_orm(sessao, criar_persona):
    admin = criar_persona(Papel.admin)
    responsavel = cadastrar_responsavel(sessao, criado_por=admin, nome="mãe")
    guerreiro = criar_persona(Papel.guerreiro)
    _vincular(sessao, responsavel, guerreiro, admin)

    consentimento = registrar_consentimento(
        sessao,
        responsavel=responsavel,
        guerreiro_id=guerreiro.id,
        tipo=TIPO,
        versao_do_termo="1.0",
        decisao=DecisaoDeConsentimento.concede,
        origem=OrigemDoConsentimento.propria,
        operado_por=responsavel,
    )
    sessao.commit()

    consentimento.versao_do_termo = "2.0"
    with pytest.raises(ConsentimentoImutavel):
        sessao.commit()
    sessao.rollback()

    consentimento_intacto = sessao.get(Consentimento, consentimento.id)
    assert consentimento_intacto.versao_do_termo == "1.0"

    sessao.delete(consentimento_intacto)
    with pytest.raises(ConsentimentoImutavel):
        sessao.commit()
    sessao.rollback()

    assert sessao.get(Consentimento, consentimento.id) is not None


def test_update_e_delete_em_consentimento_sao_recusados_direto_no_banco(
    conexao, sessao, criar_persona
):
    """Fora do ORM — direto no banco — o gatilho da migração recusa também
    (`RN-01-12`, design — decisões)."""
    admin = criar_persona(Papel.admin)
    responsavel = cadastrar_responsavel(sessao, criado_por=admin, nome="mãe")
    guerreiro = criar_persona(Papel.guerreiro)
    _vincular(sessao, responsavel, guerreiro, admin)

    consentimento = registrar_consentimento(
        sessao,
        responsavel=responsavel,
        guerreiro_id=guerreiro.id,
        tipo=TIPO,
        versao_do_termo="1.0",
        decisao=DecisaoDeConsentimento.concede,
        origem=OrigemDoConsentimento.propria,
        operado_por=responsavel,
    )
    sessao.commit()

    with pytest.raises(DBAPIError), conexao.begin_nested():
        conexao.execute(
            text("UPDATE consentimento SET versao_do_termo = '2.0' WHERE id = :id"),
            {"id": str(consentimento.id)},
        )

    with pytest.raises(DBAPIError), conexao.begin_nested():
        conexao.execute(
            text("DELETE FROM consentimento WHERE id = :id"), {"id": str(consentimento.id)}
        )

    ainda_existe = sessao.get(Consentimento, consentimento.id)
    assert ainda_existe is not None
    assert ainda_existe.versao_do_termo == "1.0"


def test_historico_responde_pelo_registro_vigente_na_data(sessao, criar_persona):
    admin = criar_persona(Papel.admin)
    responsavel = cadastrar_responsavel(sessao, criado_por=admin, nome="mãe")
    guerreiro = criar_persona(Papel.guerreiro)
    _vincular(sessao, responsavel, guerreiro, admin)

    concedido = registrar_consentimento(
        sessao,
        responsavel=responsavel,
        guerreiro_id=guerreiro.id,
        tipo=TIPO,
        versao_do_termo="1.0",
        decisao=DecisaoDeConsentimento.concede,
        origem=OrigemDoConsentimento.propria,
        operado_por=responsavel,
    )
    sessao.commit()
    sessao.refresh(concedido)
    momento_intermediario = concedido.registrado_em

    registrar_consentimento(
        sessao,
        responsavel=responsavel,
        guerreiro_id=guerreiro.id,
        tipo=TIPO,
        versao_do_termo="1.0",
        decisao=DecisaoDeConsentimento.nega,
        origem=OrigemDoConsentimento.propria,
        operado_por=responsavel,
    )
    sessao.commit()

    vigente_no_intermediario = consultar_consentimento_vigente_em(
        sessao, guerreiro_id=guerreiro.id, tipo=TIPO, em=momento_intermediario
    )
    assert vigente_no_intermediario.id == concedido.id
    assert vigente_no_intermediario.decisao == DecisaoDeConsentimento.concede


def test_recusa_de_consentimento_nao_impede_participacao_e_revogacao_nao_desfaz(
    sessao, criar_persona
):
    """`RN-01-21`: a decisão do responsável nunca é usada para excluir o
    Guerreiro(a) da atividade — nada além do registro do consentimento é
    alterado, e o vínculo segue vigente."""
    admin = criar_persona(Papel.admin)
    responsavel = cadastrar_responsavel(sessao, criado_por=admin, nome="mãe")
    guerreiro = criar_persona(Papel.guerreiro)
    vinculo = _vincular(sessao, responsavel, guerreiro, admin)
    sessao.commit()

    registrar_consentimento(
        sessao,
        responsavel=responsavel,
        guerreiro_id=guerreiro.id,
        tipo=TIPO,
        versao_do_termo="1.0",
        decisao=DecisaoDeConsentimento.nega,
        origem=OrigemDoConsentimento.propria,
        operado_por=responsavel,
    )
    sessao.commit()

    assert vinculo.fim is None
    persona_do_guerreiro = sessao.get(type(guerreiro), guerreiro.id)
    assert persona_do_guerreiro is not None


def test_tipo_fora_do_conjunto_e_recusado(sessao, criar_persona):
    admin = criar_persona(Papel.admin)
    responsavel = cadastrar_responsavel(sessao, criado_por=admin, nome="mãe")
    guerreiro = criar_persona(Papel.guerreiro)
    _vincular(sessao, responsavel, guerreiro, admin)

    with pytest.raises(ErroDeValidacao) as excinfo:
        registrar_consentimento(
            sessao,
            responsavel=responsavel,
            guerreiro_id=guerreiro.id,
            tipo="tipo_inventado",
            versao_do_termo="1.0",
            decisao=DecisaoDeConsentimento.concede,
            origem=OrigemDoConsentimento.propria,
            operado_por=responsavel,
        )
    assert excinfo.value.campo == "tipo"
    assert sessao.query(Consentimento).count() == 0


def test_biometria_nao_entra_na_autorizacao_unica(sessao, criar_persona):
    admin = criar_persona(Papel.admin)
    responsavel = cadastrar_responsavel(sessao, criado_por=admin, nome="mãe")
    guerreiro = criar_persona(Papel.guerreiro)
    _vincular(sessao, responsavel, guerreiro, admin)

    registrar_consentimento(
        sessao,
        responsavel=responsavel,
        guerreiro_id=guerreiro.id,
        tipo=TipoDeConsentimento.autorizacao_de_divulgacao,
        versao_do_termo="1.0",
        decisao=DecisaoDeConsentimento.concede,
        origem=OrigemDoConsentimento.propria,
        operado_por=responsavel,
    )
    sessao.commit()

    vigente_biometria = consultar_consentimento_vigente_em(
        sessao,
        guerreiro_id=guerreiro.id,
        tipo=TipoDeConsentimento.biometria,
        em=datetime.now(UTC),
    )
    assert vigente_biometria is None


def test_estado_sem_decisao_nenhuma_e_nao_autorizada(sessao, criar_persona):
    guerreiro = criar_persona(Papel.guerreiro)

    leitura = ler_autorizacao(sessao, guerreiro_id=guerreiro.id)

    assert leitura.estado == EstadoDaAutorizacao.nao_autorizada
    assert leitura.suspensa_por is None
    assert leitura.historico == []


def test_estado_com_todos_concedendo_e_vigente(sessao, criar_persona):
    admin = criar_persona(Papel.admin)
    guerreiro = criar_persona(Papel.guerreiro)
    a = _responsavel_vinculado(sessao, admin, guerreiro, nome="mãe")
    b = _responsavel_vinculado(sessao, admin, guerreiro, nome="pai")

    decidir_autorizacao(
        sessao,
        responsavel=a,
        guerreiro_id=guerreiro.id,
        decisao=DecisaoDeConsentimento.concede,
        versao_do_termo="1.0",
    )
    sessao.commit()
    decidir_autorizacao(
        sessao,
        responsavel=b,
        guerreiro_id=guerreiro.id,
        decisao=DecisaoDeConsentimento.concede,
        versao_do_termo="1.0",
    )
    sessao.commit()

    leitura = ler_autorizacao(sessao, guerreiro_id=guerreiro.id)
    assert leitura.estado == EstadoDaAutorizacao.vigente


def test_estado_com_recusa_isolada_e_nao_autorizada(sessao, criar_persona):
    admin = criar_persona(Papel.admin)
    guerreiro = criar_persona(Papel.guerreiro)
    responsavel = _responsavel_vinculado(sessao, admin, guerreiro)

    with pytest.raises(RevogacaoSemAutorizacaoVigente):
        decidir_autorizacao(
            sessao,
            responsavel=responsavel,
            guerreiro_id=guerreiro.id,
            decisao=DecisaoDeConsentimento.nega,
            versao_do_termo="1.0",
        )

    leitura = ler_autorizacao(sessao, guerreiro_id=guerreiro.id)
    assert leitura.estado == EstadoDaAutorizacao.nao_autorizada


def test_concessao_de_um_e_recusa_de_outro_da_suspensa(sessao, criar_persona):
    admin = criar_persona(Papel.admin)
    guerreiro = criar_persona(Papel.guerreiro)
    a = _responsavel_vinculado(sessao, admin, guerreiro, nome="mãe")
    b = _responsavel_vinculado(sessao, admin, guerreiro, nome="pai")

    decidir_autorizacao(
        sessao,
        responsavel=a,
        guerreiro_id=guerreiro.id,
        decisao=DecisaoDeConsentimento.concede,
        versao_do_termo="1.0",
    )
    sessao.commit()
    decidir_autorizacao(
        sessao,
        responsavel=b,
        guerreiro_id=guerreiro.id,
        decisao=DecisaoDeConsentimento.nega,
        versao_do_termo="1.0",
    )
    sessao.commit()

    leitura = ler_autorizacao(sessao, guerreiro_id=guerreiro.id)
    assert leitura.estado == EstadoDaAutorizacao.suspensa
    assert leitura.suspensa_por.responsavel_id == b.id


def test_suspensa_retira_do_publico_sem_apagar_registro(sessao, criar_persona):
    admin = criar_persona(Papel.admin)
    guerreiro = criar_persona(Papel.guerreiro)
    a = _responsavel_vinculado(sessao, admin, guerreiro, nome="mãe")
    b = _responsavel_vinculado(sessao, admin, guerreiro, nome="pai")

    decidir_autorizacao(
        sessao,
        responsavel=a,
        guerreiro_id=guerreiro.id,
        decisao=DecisaoDeConsentimento.concede,
        versao_do_termo="1.0",
    )
    sessao.commit()
    assert autorizacao_de_divulgacao_vigente(sessao, guerreiro.id) is True

    decidir_autorizacao(
        sessao,
        responsavel=b,
        guerreiro_id=guerreiro.id,
        decisao=DecisaoDeConsentimento.nega,
        versao_do_termo="1.0",
    )
    sessao.commit()

    assert autorizacao_de_divulgacao_vigente(sessao, guerreiro.id) is False
    assert sessao.query(Consentimento).filter_by(guerreiro_id=guerreiro.id).count() == 2
    assert sessao.get(Persona, guerreiro.id) is not None


def test_estado_suspenso_nao_tira_ninguem_da_atividade(sessao, criar_persona):
    """`RN-13-09`: a suspensão só restringe o que o consentimento cobre —
    aqui apenas a confirmação de que o Guerreiro(a) continua existindo e
    alcançável como qualquer outro, sem operação de participação recusada
    por causa do estado."""
    admin = criar_persona(Papel.admin)
    guerreiro = criar_persona(Papel.guerreiro)
    a = _responsavel_vinculado(sessao, admin, guerreiro, nome="mãe")
    b = _responsavel_vinculado(sessao, admin, guerreiro, nome="pai")

    decidir_autorizacao(
        sessao,
        responsavel=a,
        guerreiro_id=guerreiro.id,
        decisao=DecisaoDeConsentimento.concede,
        versao_do_termo="1.0",
    )
    sessao.commit()
    decidir_autorizacao(
        sessao,
        responsavel=b,
        guerreiro_id=guerreiro.id,
        decisao=DecisaoDeConsentimento.nega,
        versao_do_termo="1.0",
    )
    sessao.commit()

    guerreiro_apos = sessao.get(Persona, guerreiro.id)
    assert guerreiro_apos is not None
    assert guerreiro_apos.papel == Papel.guerreiro


def test_reenvio_da_mesma_decisao_nao_grava_segundo_registro(sessao, criar_persona):
    admin = criar_persona(Papel.admin)
    guerreiro = criar_persona(Papel.guerreiro)
    responsavel = _responsavel_vinculado(sessao, admin, guerreiro)

    primeiro, _ = decidir_autorizacao(
        sessao,
        responsavel=responsavel,
        guerreiro_id=guerreiro.id,
        decisao=DecisaoDeConsentimento.concede,
        versao_do_termo="1.0",
    )
    sessao.commit()

    segundo, estado = decidir_autorizacao(
        sessao,
        responsavel=responsavel,
        guerreiro_id=guerreiro.id,
        decisao=DecisaoDeConsentimento.concede,
        versao_do_termo="1.0",
    )
    sessao.commit()

    assert segundo.id == primeiro.id
    assert estado == EstadoDaAutorizacao.vigente
    assert (
        sessao.query(Consentimento)
        .filter_by(responsavel_id=responsavel.id, guerreiro_id=guerreiro.id)
        .count()
        == 1
    )


def test_decisao_contraria_sempre_grava(sessao, criar_persona):
    admin = criar_persona(Papel.admin)
    guerreiro = criar_persona(Papel.guerreiro)
    responsavel = _responsavel_vinculado(sessao, admin, guerreiro)

    decidir_autorizacao(
        sessao,
        responsavel=responsavel,
        guerreiro_id=guerreiro.id,
        decisao=DecisaoDeConsentimento.concede,
        versao_do_termo="1.0",
    )
    sessao.commit()

    novo, estado = decidir_autorizacao(
        sessao,
        responsavel=responsavel,
        guerreiro_id=guerreiro.id,
        decisao=DecisaoDeConsentimento.nega,
        versao_do_termo="1.0",
    )
    sessao.commit()

    assert estado == EstadoDaAutorizacao.nao_autorizada
    assert (
        sessao.query(Consentimento)
        .filter_by(responsavel_id=responsavel.id, guerreiro_id=guerreiro.id)
        .count()
        == 2
    )
    assert novo.decisao == DecisaoDeConsentimento.nega


def test_concessao_sobre_recusa_de_outro_e_recusada(sessao, criar_persona):
    """A guarda é sobre a recusa de **outro**: quem já concedeu pode
    reenviar a própria concessão (idempotência) sem tropeçar nela — por
    isso o terceiro responsável, que nunca decidiu, é quem prova o 409."""
    admin = criar_persona(Papel.admin)
    guerreiro = criar_persona(Papel.guerreiro)
    a = _responsavel_vinculado(sessao, admin, guerreiro, nome="mãe")
    b = _responsavel_vinculado(sessao, admin, guerreiro, nome="pai")
    c = _responsavel_vinculado(sessao, admin, guerreiro, nome="avó")

    decidir_autorizacao(
        sessao,
        responsavel=a,
        guerreiro_id=guerreiro.id,
        decisao=DecisaoDeConsentimento.concede,
        versao_do_termo="1.0",
    )
    sessao.commit()
    decidir_autorizacao(
        sessao,
        responsavel=b,
        guerreiro_id=guerreiro.id,
        decisao=DecisaoDeConsentimento.nega,
        versao_do_termo="1.0",
    )
    sessao.commit()

    with pytest.raises(AutorizacaoSuspensaPorOutroResponsavel):
        decidir_autorizacao(
            sessao,
            responsavel=c,
            guerreiro_id=guerreiro.id,
            decisao=DecisaoDeConsentimento.concede,
            versao_do_termo="1.0",
        )
    assert (
        sessao.query(Consentimento)
        .filter_by(responsavel_id=c.id, guerreiro_id=guerreiro.id)
        .count()
        == 0
    )


def test_quem_recusou_pode_voltar_atras(sessao, criar_persona):
    admin = criar_persona(Papel.admin)
    guerreiro = criar_persona(Papel.guerreiro)
    a = _responsavel_vinculado(sessao, admin, guerreiro, nome="mãe")
    b = _responsavel_vinculado(sessao, admin, guerreiro, nome="pai")

    decidir_autorizacao(
        sessao,
        responsavel=a,
        guerreiro_id=guerreiro.id,
        decisao=DecisaoDeConsentimento.concede,
        versao_do_termo="1.0",
    )
    sessao.commit()
    decidir_autorizacao(
        sessao,
        responsavel=b,
        guerreiro_id=guerreiro.id,
        decisao=DecisaoDeConsentimento.nega,
        versao_do_termo="1.0",
    )
    sessao.commit()

    _, estado = decidir_autorizacao(
        sessao,
        responsavel=b,
        guerreiro_id=guerreiro.id,
        decisao=DecisaoDeConsentimento.concede,
        versao_do_termo="1.0",
    )
    sessao.commit()

    assert estado == EstadoDaAutorizacao.vigente


def test_quem_nunca_decidiu_revoga_sobre_a_concessao_de_outro(sessao, criar_persona):
    """`RF-13-17`, `RN-13-07`: a divergência não exige que quem recusa
    tenha concedido antes — é assim que o segundo responsável diverge."""
    admin = criar_persona(Papel.admin)
    guerreiro = criar_persona(Papel.guerreiro)
    a = _responsavel_vinculado(sessao, admin, guerreiro, nome="mãe")
    b = _responsavel_vinculado(sessao, admin, guerreiro, nome="pai")

    decidir_autorizacao(
        sessao,
        responsavel=a,
        guerreiro_id=guerreiro.id,
        decisao=DecisaoDeConsentimento.concede,
        versao_do_termo="1.0",
    )
    sessao.commit()

    registro, estado = decidir_autorizacao(
        sessao,
        responsavel=b,
        guerreiro_id=guerreiro.id,
        decisao=DecisaoDeConsentimento.nega,
        versao_do_termo="1.0",
    )
    sessao.commit()

    assert registro.decisao == DecisaoDeConsentimento.nega
    assert estado == EstadoDaAutorizacao.suspensa


def test_revogacao_sem_vinculo_e_recusada(sessao, criar_persona):
    admin = criar_persona(Papel.admin)
    responsavel = cadastrar_responsavel(sessao, criado_por=admin, nome="mãe")
    guerreiro_sem_vinculo = criar_persona(Papel.guerreiro)

    with pytest.raises(PermissaoNegada):
        decidir_autorizacao(
            sessao,
            responsavel=responsavel,
            guerreiro_id=guerreiro_sem_vinculo.id,
            decisao=DecisaoDeConsentimento.concede,
            versao_do_termo="1.0",
        )


def test_divergencia_abre_solicitacao_no_mesmo_commit(sessao, criar_persona):
    """A abertura da solicitação de divergência é encadeada ao ato de
    decidir, sem passo à parte (`RF-13-19`, design — decisão 4)."""
    admin = criar_persona(Papel.admin)
    guerreiro = criar_persona(Papel.guerreiro)
    a = _responsavel_vinculado(sessao, admin, guerreiro, nome="mãe")
    b = _responsavel_vinculado(sessao, admin, guerreiro, nome="pai")

    decidir_autorizacao(
        sessao,
        responsavel=a,
        guerreiro_id=guerreiro.id,
        decisao=DecisaoDeConsentimento.concede,
        versao_do_termo="1.0",
    )
    sessao.commit()
    decidir_autorizacao(
        sessao,
        responsavel=b,
        guerreiro_id=guerreiro.id,
        decisao=DecisaoDeConsentimento.nega,
        versao_do_termo="1.0",
    )
    sessao.commit()

    solicitacoes = (
        sessao.query(SolicitacaoDoResponsavel)
        .filter_by(guerreiro_id=guerreiro.id, aberta_pela_suspensao=True)
        .all()
    )
    assert len(solicitacoes) == 1
    assert solicitacoes[0].responsavel_id == b.id
