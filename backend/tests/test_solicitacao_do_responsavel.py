from datetime import timedelta

import pytest

from nucleo.erros import (
    PermissaoNegada,
    SolicitacaoDoResponsavelDuplicada,
    SolicitacaoJaAvaliada,
)
from nucleo.fila.modelo import SituacaoDaSolicitacao
from nucleo.fila.regra import PRAZO_DE_AVALIACAO
from nucleo.personas.modelo import Papel, Persona
from nucleo.responsaveis.regra import criar_vinculo
from nucleo.solicitacoes_do_responsavel.modelo import (
    SolicitacaoDoResponsavel,
    TipoDeSolicitacaoDoResponsavel,
)
from nucleo.solicitacoes_do_responsavel.regra import (
    abrir_solicitacao,
    abrir_solicitacao_da_divergencia,
    esta_em_atraso,
    registrar_tratamento,
)
from nucleo.tempo import agora


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


@pytest.mark.parametrize(
    "tipo",
    [
        TipoDeSolicitacaoDoResponsavel.acesso,
        TipoDeSolicitacaoDoResponsavel.correcao,
        TipoDeSolicitacaoDoResponsavel.exclusao,
        TipoDeSolicitacaoDoResponsavel.esclarecimento,
    ],
)
def test_abertura_nos_quatro_tipos_nasce_recebida_com_prazo_de_sete_dias(sessao, cenario, tipo):
    c = cenario()

    solicitacao = abrir_solicitacao(
        sessao,
        responsavel=c["responsavel"],
        guerreiro_id=c["guerreiro"].id,
        tipo=tipo,
        texto="Pedido do responsável.",
    )
    sessao.commit()

    assert solicitacao.situacao == SituacaoDaSolicitacao.recebida
    diferenca = solicitacao.prazo - solicitacao.registrado_em
    assert abs(diferenca - PRAZO_DE_AVALIACAO) < timedelta(seconds=5)


def test_guerreiro_nao_vinculado_recusa_a_abertura(sessao, criar_persona):
    admin = criar_persona(Papel.admin)
    responsavel = criar_persona(Papel.responsavel, criada_por=admin)
    guerreiro = criar_persona(Papel.guerreiro)

    with pytest.raises(PermissaoNegada):
        abrir_solicitacao(
            sessao,
            responsavel=responsavel,
            guerreiro_id=guerreiro.id,
            tipo=TipoDeSolicitacaoDoResponsavel.acesso,
            texto="Pedido.",
        )
    assert sessao.query(SolicitacaoDoResponsavel).count() == 0


def test_duplicata_em_aberto_e_recusada_e_aceita_depois_do_desfecho(sessao, cenario):
    c = cenario()

    primeira = abrir_solicitacao(
        sessao,
        responsavel=c["responsavel"],
        guerreiro_id=c["guerreiro"].id,
        tipo=TipoDeSolicitacaoDoResponsavel.correcao,
        texto="Corrija o nome.",
    )
    sessao.commit()

    with pytest.raises(SolicitacaoDoResponsavelDuplicada):
        abrir_solicitacao(
            sessao,
            responsavel=c["responsavel"],
            guerreiro_id=c["guerreiro"].id,
            tipo=TipoDeSolicitacaoDoResponsavel.correcao,
            texto="De novo.",
        )
    assert sessao.query(SolicitacaoDoResponsavel).count() == 1

    registrar_tratamento(
        sessao,
        primeira,
        situacao=SituacaoDaSolicitacao.aceita,
        tratado_por=c["admin"],
        desfecho="Corrigido.",
    )
    sessao.commit()

    segunda = abrir_solicitacao(
        sessao,
        responsavel=c["responsavel"],
        guerreiro_id=c["guerreiro"].id,
        tipo=TipoDeSolicitacaoDoResponsavel.correcao,
        texto="Nova correção.",
    )
    sessao.commit()

    assert segunda.id != primeira.id
    assert sessao.query(SolicitacaoDoResponsavel).count() == 2


def test_atraso_derivado_nao_fecha_a_solicitacao(sessao, cenario):
    c = cenario()
    solicitacao = abrir_solicitacao(
        sessao,
        responsavel=c["responsavel"],
        guerreiro_id=c["guerreiro"].id,
        tipo=TipoDeSolicitacaoDoResponsavel.acesso,
        texto="Pedido.",
    )
    solicitacao.prazo = agora() - timedelta(seconds=1)
    sessao.commit()

    assert esta_em_atraso(solicitacao)
    assert solicitacao.situacao == SituacaoDaSolicitacao.recebida


def test_tratamento_grava_quem_tratou_e_quando(sessao, cenario):
    c = cenario()
    solicitacao = abrir_solicitacao(
        sessao,
        responsavel=c["responsavel"],
        guerreiro_id=c["guerreiro"].id,
        tipo=TipoDeSolicitacaoDoResponsavel.acesso,
        texto="Pedido.",
    )
    solicitacao.prazo = agora() - timedelta(seconds=1)
    sessao.commit()

    tratada = registrar_tratamento(
        sessao,
        solicitacao,
        situacao=SituacaoDaSolicitacao.aceita,
        tratado_por=c["admin"],
        desfecho="Concedido.",
    )
    sessao.commit()

    assert tratada.situacao == SituacaoDaSolicitacao.aceita
    assert tratada.tratado_por_id == c["admin"].id
    assert tratada.desfecho == "Concedido."
    assert tratada.tratado_em is not None
    assert not esta_em_atraso(tratada)


def test_segundo_desfecho_e_recusado(sessao, cenario):
    c = cenario()
    solicitacao = abrir_solicitacao(
        sessao,
        responsavel=c["responsavel"],
        guerreiro_id=c["guerreiro"].id,
        tipo=TipoDeSolicitacaoDoResponsavel.acesso,
        texto="Pedido.",
    )
    sessao.commit()
    registrar_tratamento(
        sessao, solicitacao, situacao=SituacaoDaSolicitacao.aceita, tratado_por=c["admin"]
    )
    sessao.commit()

    with pytest.raises(SolicitacaoJaAvaliada):
        registrar_tratamento(
            sessao, solicitacao, situacao=SituacaoDaSolicitacao.recusada, tratado_por=c["admin"]
        )
    assert solicitacao.situacao == SituacaoDaSolicitacao.aceita


def test_desfecho_de_exclusao_nao_apaga_nem_despersonaliza_nada(sessao, cenario):
    c = cenario()
    solicitacao = abrir_solicitacao(
        sessao,
        responsavel=c["responsavel"],
        guerreiro_id=c["guerreiro"].id,
        tipo=TipoDeSolicitacaoDoResponsavel.exclusao,
        texto="Quero excluir os dados.",
    )
    sessao.commit()

    guerreiro_antes = sessao.get(Persona, c["guerreiro"].id)
    nome_antes, nascimento_antes = guerreiro_antes.nome, guerreiro_antes.nascimento

    registrar_tratamento(
        sessao,
        solicitacao,
        situacao=SituacaoDaSolicitacao.aceita,
        tratado_por=c["admin"],
        desfecho="Pedido aceito.",
    )
    sessao.commit()

    assert sessao.query(Persona).filter_by(papel=Papel.guerreiro).count() == 1
    guerreiro_depois = sessao.get(Persona, c["guerreiro"].id)
    assert guerreiro_depois.nome == nome_antes
    assert guerreiro_depois.nascimento == nascimento_antes


def test_abrir_solicitacao_da_divergencia_abre_em_nome_de_quem_recusou(sessao, cenario):
    c = cenario()

    solicitacao = abrir_solicitacao_da_divergencia(
        sessao, guerreiro_id=c["guerreiro"].id, responsavel_que_recusou=c["responsavel"]
    )
    sessao.commit()

    assert solicitacao is not None
    assert solicitacao.responsavel_id == c["responsavel"].id
    assert solicitacao.guerreiro_id == c["guerreiro"].id
    assert solicitacao.tipo == TipoDeSolicitacaoDoResponsavel.esclarecimento
    assert solicitacao.aberta_pela_suspensao is True
    assert solicitacao.situacao == SituacaoDaSolicitacao.recebida
    diferenca = solicitacao.prazo - solicitacao.registrado_em
    assert abs(diferenca - PRAZO_DE_AVALIACAO) < timedelta(seconds=5)


def test_segunda_chamada_com_a_primeira_em_aberto_nao_duplica(sessao, cenario):
    c = cenario()

    primeira = abrir_solicitacao_da_divergencia(
        sessao, guerreiro_id=c["guerreiro"].id, responsavel_que_recusou=c["responsavel"]
    )
    sessao.commit()

    segunda = abrir_solicitacao_da_divergencia(
        sessao, guerreiro_id=c["guerreiro"].id, responsavel_que_recusou=c["responsavel"]
    )
    sessao.commit()

    assert primeira is not None
    assert segunda is None
    assert (
        sessao.query(SolicitacaoDoResponsavel)
        .filter_by(guerreiro_id=c["guerreiro"].id, aberta_pela_suspensao=True)
        .count()
        == 1
    )


def test_divergencia_nova_depois_do_desfecho_da_primeira(sessao, cenario):
    c = cenario()

    primeira = abrir_solicitacao_da_divergencia(
        sessao, guerreiro_id=c["guerreiro"].id, responsavel_que_recusou=c["responsavel"]
    )
    sessao.commit()

    registrar_tratamento(
        sessao,
        primeira,
        situacao=SituacaoDaSolicitacao.aceita,
        tratado_por=c["admin"],
        desfecho="Conversamos com a família.",
    )
    sessao.commit()

    segunda = abrir_solicitacao_da_divergencia(
        sessao, guerreiro_id=c["guerreiro"].id, responsavel_que_recusou=c["responsavel"]
    )
    sessao.commit()

    assert segunda is not None
    assert segunda.id != primeira.id
    assert (
        sessao.query(SolicitacaoDoResponsavel)
        .filter_by(guerreiro_id=c["guerreiro"].id, aberta_pela_suspensao=True)
        .count()
        == 2
    )


def test_recusa_isolada_nao_abre_divergencia(sessao, cenario):
    """A decisão de abrir cabe a quem chama (`consentimentos.decidir_autorizacao`),
    não a esta função — mas a recusa isolada nunca leva o estado a
    `suspensa` (não há concessão alguma para revogar), então a chamadora
    nunca invoca esta abertura."""
    from nucleo.consentimentos.modelo import DecisaoDeConsentimento
    from nucleo.consentimentos.regra import decidir_autorizacao
    from nucleo.erros import RevogacaoSemAutorizacaoVigente

    c = cenario()

    with pytest.raises(RevogacaoSemAutorizacaoVigente):
        decidir_autorizacao(
            sessao,
            responsavel=c["responsavel"],
            guerreiro_id=c["guerreiro"].id,
            decisao=DecisaoDeConsentimento.nega,
            versao_do_termo="1.0",
        )

    assert (
        sessao.query(SolicitacaoDoResponsavel)
        .filter_by(guerreiro_id=c["guerreiro"].id, aberta_pela_suspensao=True)
        .count()
        == 0
    )


def test_concessao_nunca_abre_divergencia(sessao, cenario):
    from nucleo.consentimentos.modelo import DecisaoDeConsentimento
    from nucleo.consentimentos.regra import decidir_autorizacao

    c = cenario()

    decidir_autorizacao(
        sessao,
        responsavel=c["responsavel"],
        guerreiro_id=c["guerreiro"].id,
        decisao=DecisaoDeConsentimento.concede,
        versao_do_termo="1.0",
    )
    sessao.commit()

    assert (
        sessao.query(SolicitacaoDoResponsavel)
        .filter_by(guerreiro_id=c["guerreiro"].id, aberta_pela_suspensao=True)
        .count()
        == 0
    )


def test_esclarecimento_do_responsavel_nao_bloqueia_a_divergencia(sessao, cenario):
    c = cenario()

    abrir_solicitacao(
        sessao,
        responsavel=c["responsavel"],
        guerreiro_id=c["guerreiro"].id,
        tipo=TipoDeSolicitacaoDoResponsavel.esclarecimento,
        texto="Uma dúvida qualquer.",
    )
    sessao.commit()

    divergencia = abrir_solicitacao_da_divergencia(
        sessao, guerreiro_id=c["guerreiro"].id, responsavel_que_recusou=c["responsavel"]
    )
    sessao.commit()

    assert divergencia is not None
    assert (
        sessao.query(SolicitacaoDoResponsavel).filter_by(guerreiro_id=c["guerreiro"].id).count()
        == 2
    )


def test_divergencia_nao_bloqueia_o_pedido_do_responsavel(sessao, cenario):
    c = cenario()

    abrir_solicitacao_da_divergencia(
        sessao, guerreiro_id=c["guerreiro"].id, responsavel_que_recusou=c["responsavel"]
    )
    sessao.commit()

    pedido = abrir_solicitacao(
        sessao,
        responsavel=c["responsavel"],
        guerreiro_id=c["guerreiro"].id,
        tipo=TipoDeSolicitacaoDoResponsavel.esclarecimento,
        texto="Quero entender o que houve.",
    )
    sessao.commit()

    assert pedido is not None
    assert pedido.aberta_pela_suspensao is False
    assert (
        sessao.query(SolicitacaoDoResponsavel).filter_by(guerreiro_id=c["guerreiro"].id).count()
        == 2
    )


def test_solicitacao_da_divergencia_aparece_na_fila_do_admin(sessao, cenario):
    from nucleo.solicitacoes_do_responsavel.regra import listar_fila_do_admin

    c = cenario()

    solicitacao = abrir_solicitacao_da_divergencia(
        sessao, guerreiro_id=c["guerreiro"].id, responsavel_que_recusou=c["responsavel"]
    )
    sessao.commit()

    fila = listar_fila_do_admin(sessao)

    assert any(item.id == solicitacao.id for item in fila)
