import pytest
from sqlalchemy import text
from sqlalchemy.exc import DBAPIError

from nucleo.consentimentos.modelo import (
    Consentimento,
    DecisaoDeConsentimento,
    OrigemDoConsentimento,
)
from nucleo.consentimentos.regra import consultar_consentimento_vigente_em, registrar_consentimento
from nucleo.erros import ConsentimentoImutavel, ErroDeValidacao, PermissaoNegada
from nucleo.personas.modelo import Papel
from nucleo.responsaveis.regra import cadastrar_responsavel, criar_vinculo


def _vincular(sessao, responsavel, guerreiro, cadastrado_por):
    return criar_vinculo(
        sessao,
        responsavel=responsavel,
        guerreiro_id=guerreiro.id,
        grau_de_parentesco="mãe",
        cadastrado_por=cadastrado_por,
    )


def test_registro_guarda_o_que_valia(sessao, criar_persona):
    admin = criar_persona(Papel.admin)
    responsavel = cadastrar_responsavel(sessao, criado_por=admin)
    guerreiro = criar_persona(Papel.guerreiro)
    _vincular(sessao, responsavel, guerreiro, admin)

    consentimento = registrar_consentimento(
        sessao,
        responsavel=responsavel,
        guerreiro_id=guerreiro.id,
        tipo="autorizacao",
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
    responsavel = cadastrar_responsavel(sessao, criado_por=admin)
    guerreiro = criar_persona(Papel.guerreiro)
    _vincular(sessao, responsavel, guerreiro, admin)

    with pytest.raises(ErroDeValidacao) as excinfo:
        registrar_consentimento(
            sessao,
            responsavel=responsavel,
            guerreiro_id=guerreiro.id,
            tipo="autorizacao",
            versao_do_termo="",
            decisao=DecisaoDeConsentimento.concede,
            origem=OrigemDoConsentimento.propria,
            operado_por=responsavel,
        )
    assert excinfo.value.campo == "versao_do_termo"
    assert sessao.query(Consentimento).count() == 0


def test_responsavel_nao_consente_por_crianca_que_nao_e_sua(sessao, criar_persona):
    admin = criar_persona(Papel.admin)
    responsavel = cadastrar_responsavel(sessao, criado_por=admin)
    guerreiro_sem_vinculo = criar_persona(Papel.guerreiro)

    with pytest.raises(PermissaoNegada):
        registrar_consentimento(
            sessao,
            responsavel=responsavel,
            guerreiro_id=guerreiro_sem_vinculo.id,
            tipo="autorizacao",
            versao_do_termo="1.0",
            decisao=DecisaoDeConsentimento.concede,
            origem=OrigemDoConsentimento.propria,
            operado_por=responsavel,
        )
    assert sessao.query(Consentimento).count() == 0


def test_revogar_cria_registro_novo_e_anterior_continua_consultavel(sessao, criar_persona):
    admin = criar_persona(Papel.admin)
    responsavel = cadastrar_responsavel(sessao, criado_por=admin)
    guerreiro = criar_persona(Papel.guerreiro)
    _vincular(sessao, responsavel, guerreiro, admin)

    concedido = registrar_consentimento(
        sessao,
        responsavel=responsavel,
        guerreiro_id=guerreiro.id,
        tipo="autorizacao",
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
        tipo="autorizacao",
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
    responsavel = cadastrar_responsavel(sessao, criado_por=admin)
    guerreiro = criar_persona(Papel.guerreiro)
    _vincular(sessao, responsavel, guerreiro, admin)

    consentimento = registrar_consentimento(
        sessao,
        responsavel=responsavel,
        guerreiro_id=guerreiro.id,
        tipo="autorizacao",
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
    engine, sessao, criar_persona
):
    """Fora do ORM — direto no banco — o gatilho da migração recusa também
    (`RN-01-12`, design — decisões)."""
    admin = criar_persona(Papel.admin)
    responsavel = cadastrar_responsavel(sessao, criado_por=admin)
    guerreiro = criar_persona(Papel.guerreiro)
    _vincular(sessao, responsavel, guerreiro, admin)

    consentimento = registrar_consentimento(
        sessao,
        responsavel=responsavel,
        guerreiro_id=guerreiro.id,
        tipo="autorizacao",
        versao_do_termo="1.0",
        decisao=DecisaoDeConsentimento.concede,
        origem=OrigemDoConsentimento.propria,
        operado_por=responsavel,
    )
    sessao.commit()

    with engine.connect() as conexao, pytest.raises(DBAPIError):
        conexao.execute(
            text("UPDATE consentimento SET versao_do_termo = '2.0' WHERE id = :id"),
            {"id": str(consentimento.id)},
        )
        conexao.commit()

    with engine.connect() as conexao, pytest.raises(DBAPIError):
        conexao.execute(
            text("DELETE FROM consentimento WHERE id = :id"), {"id": str(consentimento.id)}
        )
        conexao.commit()

    ainda_existe = sessao.get(Consentimento, consentimento.id)
    assert ainda_existe is not None
    assert ainda_existe.versao_do_termo == "1.0"


def test_historico_responde_pelo_registro_vigente_na_data(sessao, criar_persona):
    admin = criar_persona(Papel.admin)
    responsavel = cadastrar_responsavel(sessao, criado_por=admin)
    guerreiro = criar_persona(Papel.guerreiro)
    _vincular(sessao, responsavel, guerreiro, admin)

    concedido = registrar_consentimento(
        sessao,
        responsavel=responsavel,
        guerreiro_id=guerreiro.id,
        tipo="autorizacao",
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
        tipo="autorizacao",
        versao_do_termo="1.0",
        decisao=DecisaoDeConsentimento.nega,
        origem=OrigemDoConsentimento.propria,
        operado_por=responsavel,
    )
    sessao.commit()

    vigente_no_intermediario = consultar_consentimento_vigente_em(
        sessao, guerreiro_id=guerreiro.id, tipo="autorizacao", em=momento_intermediario
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
    responsavel = cadastrar_responsavel(sessao, criado_por=admin)
    guerreiro = criar_persona(Papel.guerreiro)
    vinculo = _vincular(sessao, responsavel, guerreiro, admin)
    sessao.commit()

    registrar_consentimento(
        sessao,
        responsavel=responsavel,
        guerreiro_id=guerreiro.id,
        tipo="autorizacao",
        versao_do_termo="1.0",
        decisao=DecisaoDeConsentimento.nega,
        origem=OrigemDoConsentimento.propria,
        operado_por=responsavel,
    )
    sessao.commit()

    assert vinculo.fim is None
    persona_do_guerreiro = sessao.get(type(guerreiro), guerreiro.id)
    assert persona_do_guerreiro is not None
