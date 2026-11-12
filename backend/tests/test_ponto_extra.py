from datetime import UTC, datetime

import pytest
from sqlalchemy import text
from sqlalchemy.exc import DBAPIError

from nucleo.erros import DebitoDePontoExtraRecusado, ErroDeValidacao
from nucleo.personas.modelo import Papel
from nucleo.ponto_extra.modelo import PontoExtra
from nucleo.ponto_extra.regra import creditar_ponto_extra, estornar_ponto_extra_da_presenca
from nucleo.resultados.modelo import DesfechoDoResultado
from nucleo.resultados.regra import registrar_resultado
from nucleo.trilhas.modelo import FormatoDeAtividade, ModalidadeDeAtividade
from nucleo.trilhas.regra import criar_atividade

MOMENTO_DO_FATO = datetime(2026, 8, 1, 10, 0, tzinfo=UTC)


def _lancar(sessao, *, mestre, guerreiro, missao, desfecho):
    from tests.conftest import criar_aula_para_resultado

    atividade = criar_atividade(
        sessao,
        operador=mestre,
        missao=missao,
        titulo="Atividade de Teste",
        modalidade=ModalidadeDeAtividade.individual,
        formato=FormatoDeAtividade.presencial,
        natureza="construcao",
        producao_esperada="Produção esperada.",
    )
    aula = criar_aula_para_resultado(sessao, mestre)
    sessao.commit()
    registrar_resultado(
        sessao,
        operador=mestre,
        aula=aula,
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
    conexao, sessao, criar_persona
):
    guerreiro = criar_persona(Papel.guerreiro)

    with pytest.raises(DBAPIError), conexao.begin_nested():
        conexao.execute(
            text(
                "INSERT INTO ponto_extra (id, guerreiro_id, acumulado, saldo_disponivel) "
                "VALUES (gen_random_uuid(), :guerreiro_id, 10, -1)"
            ),
            {"guerreiro_id": str(guerreiro.id)},
        )


def test_ponto_extra_recusa_debito_e_remocao_direto_no_banco(conexao, sessao, criar_persona):
    """Fora do ORM — direto no banco — o gatilho da migração recusa também
    (`RN-01-39`, mesmo padrão de `RN-01-12`)."""
    guerreiro = criar_persona(Papel.guerreiro)
    conta = creditar_ponto_extra(sessao, guerreiro_id=guerreiro.id, valor=10)
    sessao.commit()

    with pytest.raises(DBAPIError), conexao.begin_nested():
        conexao.execute(
            text("UPDATE ponto_extra SET acumulado = 5 WHERE id = :id"), {"id": str(conta.id)}
        )

    with pytest.raises(DBAPIError), conexao.begin_nested():
        conexao.execute(text("DELETE FROM ponto_extra WHERE id = :id"), {"id": str(conta.id)})

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


def test_estorno_da_presenca_tira_das_duas_contas(sessao, criar_persona):
    """`RF-01-83`, `RN-01-64`: cenário "Anulação estorna das duas contas"."""
    guerreiro = criar_persona(Papel.guerreiro)
    creditar_ponto_extra(sessao, guerreiro_id=guerreiro.id, valor=30)
    conta = sessao.query(PontoExtra).filter_by(guerreiro_id=guerreiro.id).one()
    conta.saldo_disponivel = 12
    sessao.commit()

    estornar_ponto_extra_da_presenca(sessao, guerreiro_id=guerreiro.id, valor=5)
    sessao.commit()

    conta = sessao.query(PontoExtra).filter_by(guerreiro_id=guerreiro.id).one()
    assert conta.acumulado == 25
    assert conta.saldo_disponivel == 7


def test_estorno_com_saldo_ja_trocado_para_em_zero(sessao, criar_persona):
    """`RN-01-64`: cenário "Estorno com o saldo já trocado para em zero"."""
    guerreiro = criar_persona(Papel.guerreiro)
    creditar_ponto_extra(sessao, guerreiro_id=guerreiro.id, valor=10)
    conta = sessao.query(PontoExtra).filter_by(guerreiro_id=guerreiro.id).one()
    conta.saldo_disponivel = 2
    sessao.commit()

    estornar_ponto_extra_da_presenca(sessao, guerreiro_id=guerreiro.id, valor=5)
    sessao.commit()

    conta = sessao.query(PontoExtra).filter_by(guerreiro_id=guerreiro.id).one()
    assert conta.acumulado == 5
    assert conta.saldo_disponivel == 0


def test_a_porta_do_estorno_nao_fica_aberta_no_orm(sessao, criar_persona):
    """`RN-01-39`: depois do estorno, o ORM volta a recusar a redução do
    acumulado — o marcador não sobra na conexão (design — decisão 4)."""
    guerreiro = criar_persona(Papel.guerreiro)
    conta = creditar_ponto_extra(sessao, guerreiro_id=guerreiro.id, valor=20)
    sessao.commit()
    estornar_ponto_extra_da_presenca(sessao, guerreiro_id=guerreiro.id, valor=5)
    sessao.commit()

    conta.acumulado = 1
    with pytest.raises(DebitoDePontoExtraRecusado):
        sessao.commit()
    sessao.rollback()

    assert sessao.get(PontoExtra, conta.id).acumulado == 15


def test_a_porta_do_estorno_nao_fica_aberta_no_banco(conexao, sessao, criar_persona):
    """`RN-01-39`: depois do estorno, o gatilho volta a recusar a redução do
    acumulado por SQL direto, na mesma transação (design — decisão 4)."""
    guerreiro = criar_persona(Papel.guerreiro)
    conta = creditar_ponto_extra(sessao, guerreiro_id=guerreiro.id, valor=20)
    sessao.commit()
    estornar_ponto_extra_da_presenca(sessao, guerreiro_id=guerreiro.id, valor=5)
    sessao.commit()

    with pytest.raises(DBAPIError), conexao.begin_nested():
        conexao.execute(
            text("UPDATE ponto_extra SET acumulado = 1 WHERE id = :id"), {"id": str(conta.id)}
        )
    assert sessao.get(PontoExtra, conta.id).acumulado == 15


def test_estorno_de_valor_zero_nao_toca_a_conta(sessao, criar_persona):
    """`RN-01-65`: a presença anterior à regra creditou zero."""
    guerreiro = criar_persona(Papel.guerreiro)
    creditar_ponto_extra(sessao, guerreiro_id=guerreiro.id, valor=10)
    sessao.commit()

    assert estornar_ponto_extra_da_presenca(sessao, guerreiro_id=guerreiro.id, valor=0) is None
    conta = sessao.query(PontoExtra).filter_by(guerreiro_id=guerreiro.id).one()
    assert (conta.acumulado, conta.saldo_disponivel) == (10, 10)


# ---------------------------------------------------------------------------
# O cuidado com o bem recebido é fonte só extra (`RF-01-85`, `RF-01-87`,
# documento 11 §5).
# ---------------------------------------------------------------------------


def _regulares(sessao, guerreiro):
    from nucleo.pontuacao.modelo import PontoRegular

    return sessao.query(PontoRegular).filter_by(guerreiro_id=guerreiro.id).count()


def test_a_conservacao_credita_1_extra_e_nenhum_regular(sessao, cenario):
    from nucleo.cuidado_do_bem.regra import validar_conservacao

    validar_conservacao(
        sessao,
        operador=cenario.mestre,
        aula_id=cenario.aula.id,
        guerreiro_id=cenario.guerreiro.id,
        entrega_de_recompensa_id=cenario.entrega_do_livro.id,
    )
    sessao.commit()

    conta = sessao.query(PontoExtra).filter_by(guerreiro_id=cenario.guerreiro.id).one()
    assert (conta.acumulado, conta.saldo_disponivel) == (1, 1)
    assert _regulares(sessao, cenario.guerreiro) == 0


@pytest.mark.parametrize(("aprovado", "esperado"), [(True, 1), (False, 0)])
def test_a_customizacao_aprovada_credita_1_extra_e_a_reprovada_nada(
    sessao, cenario, aprovado, esperado
):
    from nucleo.cuidado_do_bem.regra import julgar_customizacao, registrar_customizacao

    registro = registrar_customizacao(
        sessao,
        operador=cenario.guerreiro,
        entrega_de_recompensa_id=cenario.entrega_do_kit.id,
        descricao="Pintei de azul.",
    )
    registro.midia_referencia = "customizacoes/teste/midia"
    registro.midia_tipo_do_arquivo = "image/png"
    sessao.commit()

    julgar_customizacao(
        sessao,
        registro,
        operador=cenario.mestre,
        aula_id=cenario.aula.id,
        aprovado=aprovado,
        motivo=None if aprovado else "Apareceu o rosto.",
    )
    sessao.commit()

    conta = sessao.query(PontoExtra).filter_by(guerreiro_id=cenario.guerreiro.id).first()
    assert (conta.acumulado if conta else 0) == esperado
    assert _regulares(sessao, cenario.guerreiro) == 0
