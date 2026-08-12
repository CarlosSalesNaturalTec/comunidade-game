from datetime import UTC, datetime

import pytest
from sqlalchemy import text
from sqlalchemy.exc import DBAPIError

from nucleo.erros import DebitoDePontoExtraRecusado, ErroDeValidacao
from nucleo.personas.modelo import Papel
from nucleo.ponto_extra.modelo import PontoExtra
from nucleo.ponto_extra.regra import creditar_ponto_extra
from nucleo.resultados.modelo import DesfechoDoResultado
from nucleo.resultados.regra import registrar_resultado
from nucleo.trilhas.modelo import FormatoDeAtividade, ModalidadeDeAtividade
from nucleo.trilhas.regra import criar_atividade

MOMENTO_DO_FATO = datetime(2026, 8, 1, 10, 0, tzinfo=UTC)


def _lancar(sessao, *, mestre, guerreiro, missao, desfecho):
    atividade = criar_atividade(
        sessao,
        operador=mestre,
        missao=missao,
        modalidade=ModalidadeDeAtividade.individual,
        formato=FormatoDeAtividade.presencial,
        natureza="construcao",
        producao_esperada="Produção esperada.",
    )
    sessao.commit()
    registrar_resultado(
        sessao,
        operador=mestre,
        guerreiro_id=guerreiro.id,
        atividade=atividade,
        momento_do_fato=MOMENTO_DO_FATO,
        producao="Produção do Guerreiro(a).",
        desfecho=desfecho,
    )
    sessao.commit()


def test_credito_aumenta_o_acumulado_e_o_saldo_disponivel_juntos(sessao, criar_persona):
    guerreiro = criar_persona(Papel.guerreiro)

    conta = creditar_ponto_extra(sessao, guerreiro_id=guerreiro.id, valor=10)
    sessao.commit()

    assert conta.acumulado == 10
    assert conta.saldo_disponivel == 10

    conta = creditar_ponto_extra(sessao, guerreiro_id=guerreiro.id, valor=5)
    sessao.commit()

    assert conta.acumulado == 15
    assert conta.saldo_disponivel == 15


def test_credito_com_valor_nao_positivo_e_recusado(sessao, criar_persona):
    guerreiro = criar_persona(Papel.guerreiro)

    with pytest.raises(ErroDeValidacao) as excinfo:
        creditar_ponto_extra(sessao, guerreiro_id=guerreiro.id, valor=0)
    assert excinfo.value.campo == "valor"
    assert sessao.query(PontoExtra).count() == 0


def test_acumulado_nunca_decresce_pelo_orm(sessao, criar_persona):
    guerreiro = criar_persona(Papel.guerreiro)
    conta = creditar_ponto_extra(sessao, guerreiro_id=guerreiro.id, valor=10)
    sessao.commit()

    conta.acumulado = 5
    with pytest.raises(DebitoDePontoExtraRecusado):
        sessao.commit()
    sessao.rollback()

    conta_intacta = sessao.get(PontoExtra, conta.id)
    assert conta_intacta.acumulado == 10


def test_saldo_disponivel_nunca_aceita_valor_negativo_direto_no_banco(
    engine, sessao, criar_persona
):
    guerreiro = criar_persona(Papel.guerreiro)

    with engine.connect() as conexao, pytest.raises(DBAPIError):
        conexao.execute(
            text(
                "INSERT INTO ponto_extra (id, guerreiro_id, acumulado, saldo_disponivel) "
                "VALUES (gen_random_uuid(), :guerreiro_id, 10, -1)"
            ),
            {"guerreiro_id": str(guerreiro.id)},
        )
        conexao.commit()


def test_ponto_extra_recusa_debito_e_remocao_direto_no_banco(engine, sessao, criar_persona):
    """Fora do ORM — direto no banco — o gatilho da migração recusa também
    (`RN-01-39`, mesmo padrão de `RN-01-12`)."""
    guerreiro = criar_persona(Papel.guerreiro)
    conta = creditar_ponto_extra(sessao, guerreiro_id=guerreiro.id, valor=10)
    sessao.commit()

    with engine.connect() as conexao, pytest.raises(DBAPIError):
        conexao.execute(
            text("UPDATE ponto_extra SET acumulado = 5 WHERE id = :id"), {"id": str(conta.id)}
        )
        conexao.commit()

    with engine.connect() as conexao, pytest.raises(DBAPIError):
        conexao.execute(text("DELETE FROM ponto_extra WHERE id = :id"), {"id": str(conta.id)})
        conexao.commit()

    conta_intacta = sessao.get(PontoExtra, conta.id)
    assert conta_intacta is not None
    assert conta_intacta.acumulado == 10


def test_resultado_realizada_com_merito_credita_cinco_nas_duas_contas_de_extra(
    sessao, criar_persona, criar_trilha, criar_missao
):
    mestre = criar_persona(Papel.mestre)
    guerreiro = criar_persona(Papel.guerreiro)
    trilha = criar_trilha(mestre)
    missao = criar_missao(trilha, mestre)

    _lancar(
        sessao,
        mestre=mestre,
        guerreiro=guerreiro,
        missao=missao,
        desfecho=DesfechoDoResultado.realizada_com_merito,
    )

    conta = sessao.query(PontoExtra).filter_by(guerreiro_id=guerreiro.id).one()
    assert conta.acumulado == 5
    assert conta.saldo_disponivel == 5


def test_resultado_merito_extra_por_auxilio_credita_dez_nas_duas_contas_de_extra(
    sessao, criar_persona, criar_trilha, criar_missao
):
    mestre = criar_persona(Papel.mestre)
    guerreiro = criar_persona(Papel.guerreiro)
    trilha = criar_trilha(mestre)
    missao = criar_missao(trilha, mestre)

    _lancar(
        sessao,
        mestre=mestre,
        guerreiro=guerreiro,
        missao=missao,
        desfecho=DesfechoDoResultado.merito_extra_por_auxilio,
    )

    conta = sessao.query(PontoExtra).filter_by(guerreiro_id=guerreiro.id).one()
    assert conta.acumulado == 10
    assert conta.saldo_disponivel == 10


def test_resultado_realizada_sem_merito_nao_credita_ponto_extra(
    sessao, criar_persona, criar_trilha, criar_missao
):
    mestre = criar_persona(Papel.mestre)
    guerreiro = criar_persona(Papel.guerreiro)
    trilha = criar_trilha(mestre)
    missao = criar_missao(trilha, mestre)

    _lancar(
        sessao,
        mestre=mestre,
        guerreiro=guerreiro,
        missao=missao,
        desfecho=DesfechoDoResultado.realizada,
    )

    assert sessao.query(PontoExtra).filter_by(guerreiro_id=guerreiro.id).first() is None
