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
