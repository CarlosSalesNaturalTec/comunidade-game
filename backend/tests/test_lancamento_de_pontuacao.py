"""Lançamento de pontuação por movimento (`RF-01-88`, `RN-01-67`)."""

from datetime import UTC, datetime

import pytest
from sqlalchemy import func, text
from sqlalchemy.exc import DBAPIError

from nucleo.erros import ErroDeValidacao, LancamentoDePontuacaoImutavel
from nucleo.historico_de_pontuacao.modelo import (
    ContaDoLancamento,
    LancamentoDePontuacao,
    OrigemDoLancamento,
)
from nucleo.ocorrencias_de_conduta.regra import lancar_ocorrencia_de_conduta
from nucleo.personas.modelo import Papel
from nucleo.ponto_extra.modelo import PontoExtra
from nucleo.ponto_extra.regra import (
    creditar_ponto_extra,
    debitar_ponto_extra,
    estornar_ponto_extra_da_presenca,
)
from nucleo.pontuacao.modelo import PontoRegular
from nucleo.pontuacao.regra import creditar_ponto_regular
from nucleo.resultados.modelo import DesfechoDoResultado
from nucleo.resultados.regra import registrar_resultado
from nucleo.trilhas.modelo import FormatoDeAtividade, ModalidadeDeAtividade
from nucleo.trilhas.regra import criar_atividade as criar_atividade_pela_regra

MOMENTO_DO_FATO = datetime(2026, 8, 1, 10, 0, tzinfo=UTC)


def _lancamentos(sessao, guerreiro, conta=None):
    consulta = sessao.query(LancamentoDePontuacao).filter_by(guerreiro_id=guerreiro.id)
    if conta is not None:
        consulta = consulta.filter_by(conta=conta)
    return consulta.order_by(LancamentoDePontuacao.registrado_em).all()


def test_resultado_com_merito_grava_um_lancamento_em_cada_conta(
    sessao, criar_persona, criar_trilha, criar_missao
):
    from tests.conftest import criar_aula_para_resultado

    mestre = criar_persona(Papel.mestre)
    guerreiro = criar_persona(Papel.guerreiro)
    trilha = criar_trilha(mestre)
    missao = criar_missao(trilha, mestre)
    atividade = criar_atividade_pela_regra(
        sessao,
        operador=mestre,
        missao=missao,
        titulo="Robô seguidor de linha",
        modalidade=ModalidadeDeAtividade.individual,
        formato=FormatoDeAtividade.presencial,
        natureza="construcao",
        producao_esperada="Produção esperada.",
    )
    aula = criar_aula_para_resultado(sessao, mestre)
    sessao.commit()

    resultado = registrar_resultado(
        sessao,
        operador=mestre,
        aula=aula,
        guerreiro_id=guerreiro.id,
        atividade=atividade,
        momento_do_fato=MOMENTO_DO_FATO,
        producao="Produção do Guerreiro(a).",
        desfecho=DesfechoDoResultado.realizada_com_merito,
    )
    sessao.commit()

    (regular,) = _lancamentos(sessao, guerreiro, ContaDoLancamento.regular)
    assert regular.origem == OrigemDoLancamento.resultado
    assert regular.trilha_id == trilha.id
    assert regular.referencia_id == resultado.id
    assert regular.detalhe == "Robô seguidor de linha"
    total = sessao.query(PontoRegular.total).filter_by(guerreiro_id=guerreiro.id).scalar()
    assert regular.valor == total

    (extra,) = _lancamentos(sessao, guerreiro, ContaDoLancamento.extra)
    assert extra.origem == OrigemDoLancamento.merito_do_resultado
    assert (extra.valor, extra.valor_no_acumulado) == (5, 5)


def test_conduta_grava_o_debito_que_parou_em_zero(
    sessao,
    criar_persona,
    criar_comunidade,
    criar_trilha,
    criar_missao,
    criar_atividade,
    criar_aula,
):
    mestre = criar_persona(Papel.mestre)
    comunidade = criar_comunidade()
    guerreiro = criar_persona(Papel.guerreiro, comunidade=comunidade)
    trilha = criar_trilha(mestre)
    atividade = criar_atividade(criar_missao(trilha, mestre), mestre)
    aula = criar_aula(mestre, comunidade)
    creditar_ponto_regular(
        sessao,
        guerreiro_id=guerreiro.id,
        trilha_id=trilha.id,
        valor=3,
        origem=OrigemDoLancamento.resultado,
        referencia_id=None,
    )
    sessao.commit()

    ocorrencia = lancar_ocorrencia_de_conduta(
        sessao,
        operador=mestre,
        aula=aula,
        atividade=atividade,
        guerreiro_id=guerreiro.id,
        motivo="Desrespeitou um colega.",
        momento_do_fato=MOMENTO_DO_FATO,
    )
    sessao.commit()

    debito = _lancamentos(sessao, guerreiro)[-1]
    assert debito.origem == OrigemDoLancamento.ocorrencia_de_conduta
    assert debito.referencia_id == ocorrencia.id
    assert debito.trilha_id == trilha.id
    assert debito.valor == -3
    assert sum(lanc.valor for lanc in _lancamentos(sessao, guerreiro)) == 0


def test_troca_move_so_o_saldo_e_troca_recusada_nao_deixa_lancamento(sessao, criar_persona):
    guerreiro = criar_persona(Papel.guerreiro)
    creditar_ponto_extra(
        sessao,
        guerreiro_id=guerreiro.id,
        valor=30,
        origem=OrigemDoLancamento.presenca,
        referencia_id=None,
    )
    debitar_ponto_extra(
        sessao,
        guerreiro_id=guerreiro.id,
        valor=25,
        origem=OrigemDoLancamento.troca,
        referencia_id=None,
        detalhe="Camiseta",
    )
    sessao.commit()

    troca = _lancamentos(sessao, guerreiro)[-1]
    assert troca.origem == OrigemDoLancamento.troca
    assert (troca.valor, troca.valor_no_acumulado, troca.detalhe) == (-25, 0, "Camiseta")

    with pytest.raises(ErroDeValidacao):
        debitar_ponto_extra(
            sessao,
            guerreiro_id=guerreiro.id,
            valor=25,
            origem=OrigemDoLancamento.troca,
            referencia_id=None,
        )
    sessao.rollback()
    assert len(_lancamentos(sessao, guerreiro)) == 2


def test_estorno_da_presenca_registra_o_que_moveu_em_cada_conta(sessao, criar_persona):
    guerreiro = criar_persona(Papel.guerreiro)
    creditar_ponto_extra(
        sessao,
        guerreiro_id=guerreiro.id,
        valor=5,
        origem=OrigemDoLancamento.presenca,
        referencia_id=None,
    )
    debitar_ponto_extra(
        sessao,
        guerreiro_id=guerreiro.id,
        valor=3,
        origem=OrigemDoLancamento.troca,
        referencia_id=None,
    )
    sessao.commit()

    estornar_ponto_extra_da_presenca(sessao, guerreiro_id=guerreiro.id, valor=5, referencia_id=None)
    sessao.commit()

    estorno = _lancamentos(sessao, guerreiro)[-1]
    assert estorno.origem == OrigemDoLancamento.estorno_de_presenca
    assert (estorno.valor, estorno.valor_no_acumulado) == (-2, -5)

    conta = sessao.query(PontoExtra).filter_by(guerreiro_id=guerreiro.id).one()
    lancamentos = _lancamentos(sessao, guerreiro, ContaDoLancamento.extra)
    assert sum(lanc.valor for lanc in lancamentos) == conta.saldo_disponivel
    assert sum(lanc.valor_no_acumulado for lanc in lancamentos) == conta.acumulado


def test_soma_dos_lancamentos_fecha_com_o_total_regular(sessao, criar_persona, criar_trilha):
    from nucleo.pontuacao.regra import debitar_ponto_regular

    mestre = criar_persona(Papel.mestre)
    guerreiro = criar_persona(Papel.guerreiro)
    trilha = criar_trilha(mestre)
    for valor in (10, 5):
        creditar_ponto_regular(
            sessao,
            guerreiro_id=guerreiro.id,
            trilha_id=trilha.id,
            valor=valor,
            origem=OrigemDoLancamento.resultado,
            referencia_id=None,
        )
    debitar_ponto_regular(
        sessao,
        guerreiro_id=guerreiro.id,
        trilha_id=trilha.id,
        valor=20,
        origem=OrigemDoLancamento.ocorrencia_de_conduta,
        referencia_id=None,
    )
    sessao.commit()

    soma = (
        sessao.query(func.sum(LancamentoDePontuacao.valor))
        .filter_by(guerreiro_id=guerreiro.id, trilha_id=trilha.id)
        .scalar()
    )
    total = sessao.query(PontoRegular.total).filter_by(guerreiro_id=guerreiro.id).scalar()
    assert soma == total == 0


def test_lancamento_nao_se_altera_nem_se_remove(conexao, sessao, criar_persona):
    guerreiro = criar_persona(Papel.guerreiro)
    creditar_ponto_extra(
        sessao,
        guerreiro_id=guerreiro.id,
        valor=5,
        origem=OrigemDoLancamento.presenca,
        referencia_id=None,
    )
    sessao.commit()
    (lancamento,) = _lancamentos(sessao, guerreiro)

    with pytest.raises(DBAPIError), conexao.begin_nested():
        conexao.execute(
            text("UPDATE lancamento_de_pontuacao SET valor = 50 WHERE id = :id"),
            {"id": str(lancamento.id)},
        )
    with pytest.raises(DBAPIError), conexao.begin_nested():
        conexao.execute(
            text("DELETE FROM lancamento_de_pontuacao WHERE id = :id"),
            {"id": str(lancamento.id)},
        )
    assert sessao.get(LancamentoDePontuacao, lancamento.id).valor == 5


def test_lancamento_nao_se_altera_pelo_orm(sessao, criar_persona):
    guerreiro = criar_persona(Papel.guerreiro)
    creditar_ponto_extra(
        sessao,
        guerreiro_id=guerreiro.id,
        valor=5,
        origem=OrigemDoLancamento.presenca,
        referencia_id=None,
    )
    sessao.commit()
    (lancamento,) = _lancamentos(sessao, guerreiro)

    lancamento.valor = 50
    with pytest.raises(LancamentoDePontuacaoImutavel):
        sessao.flush()
    sessao.rollback()

    sessao.delete(lancamento)
    with pytest.raises(LancamentoDePontuacaoImutavel):
        sessao.flush()
