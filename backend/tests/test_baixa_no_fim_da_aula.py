"""A aula não tem fechamento: passado o horário de fim, a varredura baixa a
reserva da confirmada pelo sistema e a passa a realizada, e passa a pendente
de lastro a realizada sem lastro (`RF-07-09`, `RF-07-55`, `RF-01-91`,
`RN-07-43`, change `baixa-no-fim-da-aula`)."""

from datetime import UTC, date, datetime, timedelta
from decimal import Decimal

from nucleo.aulas.modelo import SituacaoDaAula
from nucleo.livro_razao.modelo import Lancamento, NaturezaDoLancamento
from nucleo.livro_razao.regra import saldo_de
from nucleo.personas.modelo import Papel
from nucleo.reservas.modelo import EstadoDaReserva, Reserva
from nucleo.reservas.regra import encerrar_aulas_vencidas

AGORA = datetime.now(UTC)
ONTEM = AGORA - timedelta(days=1)


def _cenario(
    criar_persona,
    criar_comunidade,
    criar_ponto_de_apoio,
    criar_tipo_de_recurso,
    criar_lancamento,
    criar_valor_de_referencia,
):
    admin = criar_persona(Papel.admin)
    comunidade = criar_comunidade()
    ponto = criar_ponto_de_apoio(admin, comunidade)
    lanche = criar_tipo_de_recurso(admin)
    criar_lancamento(admin, lanche, ponto, quantidade=Decimal("10.00"))
    criar_valor_de_referencia(admin, lanche, valor_em_moedas=Decimal("2.00"))
    return admin, comunidade, ponto, lanche


def _debitos(sessao):
    return sessao.query(Lancamento).filter_by(natureza=NaturezaDoLancamento.debito).all()


def test_aula_confirmada_vencida_tem_a_reserva_baixada_pelo_sistema(
    sessao,
    criar_persona,
    criar_comunidade,
    criar_ponto_de_apoio,
    criar_tipo_de_recurso,
    criar_lancamento,
    criar_valor_de_referencia,
    criar_aula,
    criar_reserva,
):
    admin, comunidade, ponto, lanche = _cenario(
        criar_persona,
        criar_comunidade,
        criar_ponto_de_apoio,
        criar_tipo_de_recurso,
        criar_lancamento,
        criar_valor_de_referencia,
    )
    aula = criar_aula(
        admin, comunidade, ponto_de_apoio=ponto, inicio_em=ONTEM - timedelta(hours=2), fim_em=ONTEM
    )
    reserva = criar_reserva(admin, aula, lanche, ponto, quantidade=Decimal("3.00"))

    assert encerrar_aulas_vencidas(sessao) == 1
    sessao.commit()

    sessao.refresh(aula)
    sessao.refresh(reserva)
    assert aula.situacao == SituacaoDaAula.realizada
    assert reserva.estado == EstadoDaReserva.consumida
    [debito] = _debitos(sessao)
    assert debito.quantidade == Decimal("3.00")
    assert debito.valor_em_moedas == Decimal("6.00")
    assert debito.aula_id == aula.id
    assert (debito.autor_id, debito.papel_do_autor) == (aula.autor_id, "sistema")
    assert saldo_de(sessao, tipo_de_recurso_id=lanche.id, ponto_de_apoio_id=ponto.id) == Decimal(
        "7.00"
    )


def test_aula_pendente_vencida_vira_realizada_sem_lastro_sem_baixa(
    sessao, criar_persona, criar_comunidade, criar_aula
):
    admin = criar_persona(Papel.admin)
    aula = criar_aula(admin, criar_comunidade(), inicio_em=ONTEM - timedelta(hours=2), fim_em=ONTEM)
    aula.situacao = SituacaoDaAula.pendente_de_lastro
    sessao.commit()

    encerrar_aulas_vencidas(sessao)
    sessao.commit()

    sessao.refresh(aula)
    assert aula.situacao == SituacaoDaAula.realizada_sem_lastro
    assert _debitos(sessao) == []


def test_aula_em_andamento_nao_e_encerrada(sessao, criar_persona, criar_comunidade, criar_aula):
    admin = criar_persona(Papel.admin)
    aula = criar_aula(admin, criar_comunidade())

    assert encerrar_aulas_vencidas(sessao) == 0
    sessao.refresh(aula)
    assert aula.situacao == SituacaoDaAula.confirmada


def test_a_varredura_repetida_nao_baixa_de_novo(
    sessao,
    criar_persona,
    criar_comunidade,
    criar_ponto_de_apoio,
    criar_tipo_de_recurso,
    criar_lancamento,
    criar_valor_de_referencia,
    criar_aula,
    criar_reserva,
):
    admin, comunidade, ponto, lanche = _cenario(
        criar_persona,
        criar_comunidade,
        criar_ponto_de_apoio,
        criar_tipo_de_recurso,
        criar_lancamento,
        criar_valor_de_referencia,
    )
    aula = criar_aula(
        admin, comunidade, ponto_de_apoio=ponto, inicio_em=ONTEM - timedelta(hours=2), fim_em=ONTEM
    )
    criar_reserva(admin, aula, lanche, ponto, quantidade=Decimal("3.00"))

    encerrar_aulas_vencidas(sessao)
    sessao.commit()
    assert encerrar_aulas_vencidas(sessao) == 0
    sessao.commit()

    assert len(_debitos(sessao)) == 1


def test_aula_sem_vigencia_no_dia_do_fim_fica_para_a_proxima(
    sessao,
    criar_persona,
    criar_comunidade,
    criar_ponto_de_apoio,
    criar_tipo_de_recurso,
    criar_lancamento,
    criar_valor_de_referencia,
    criar_aula,
    criar_reserva,
):
    admin = criar_persona(Papel.admin)
    comunidade = criar_comunidade()
    ponto = criar_ponto_de_apoio(admin, comunidade)
    lanche = criar_tipo_de_recurso(admin)
    criar_lancamento(admin, lanche, ponto, quantidade=Decimal("10.00"))
    # A vigência só começa amanhã: no dia do fim da aula não há valor.
    criar_valor_de_referencia(admin, lanche, vigencia_inicio=date.today() + timedelta(days=1))
    aula = criar_aula(
        admin, comunidade, ponto_de_apoio=ponto, inicio_em=ONTEM - timedelta(hours=2), fim_em=ONTEM
    )
    reserva = criar_reserva(admin, aula, lanche, ponto, quantidade=Decimal("3.00"))

    assert encerrar_aulas_vencidas(sessao) == 0
    sessao.commit()

    sessao.refresh(aula)
    sessao.refresh(reserva)
    assert aula.situacao == SituacaoDaAula.confirmada
    assert reserva.estado == EstadoDaReserva.reservada
    assert _debitos(sessao) == []


def test_a_leitura_da_agenda_encerra_a_aula_vencida(
    cliente,
    sessao,
    criar_chave,
    criar_persona,
    criar_sessao_de_teste,
    criar_comunidade,
    criar_ponto_de_apoio,
    criar_tipo_de_recurso,
    criar_lancamento,
    criar_valor_de_referencia,
    criar_aula,
    criar_reserva,
):
    admin, comunidade, ponto, lanche = _cenario(
        criar_persona,
        criar_comunidade,
        criar_ponto_de_apoio,
        criar_tipo_de_recurso,
        criar_lancamento,
        criar_valor_de_referencia,
    )
    aula = criar_aula(
        admin, comunidade, ponto_de_apoio=ponto, inicio_em=ONTEM - timedelta(hours=2), fim_em=ONTEM
    )
    criar_reserva(admin, aula, lanche, ponto, quantidade=Decimal("3.00"))
    chave, _ = criar_chave()
    token, _ = criar_sessao_de_teste(admin)

    resposta = cliente.get(
        "/v1/aulas",
        params={"comunidade": str(comunidade.id)},
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
    )

    assert resposta.status_code == 200
    [item] = resposta.json()["itens"]
    assert item["situacao"] == SituacaoDaAula.realizada.value
    assert (
        sessao.query(Reserva).filter_by(aula_id=aula.id).one().estado == EstadoDaReserva.consumida
    )


def test_a_leitura_das_necessidades_tira_a_aula_pendente_que_terminou(
    cliente, sessao, criar_chave, criar_persona, criar_comunidade, criar_aula
):
    admin = criar_persona(Papel.admin)
    aula = criar_aula(admin, criar_comunidade(), inicio_em=ONTEM - timedelta(hours=2), fim_em=ONTEM)
    aula.situacao = SituacaoDaAula.pendente_de_lastro
    sessao.commit()
    chave, _ = criar_chave()

    resposta = cliente.get("/v1/vitrine/necessidades", headers={"X-Chave-Aplicacao": chave})

    assert resposta.status_code == 200
    assert all(item["aula_id"] != str(aula.id) for item in resposta.json())
    sessao.refresh(aula)
    assert aula.situacao == SituacaoDaAula.realizada_sem_lastro


def test_aula_que_ja_terminou_nao_se_cancela(sessao, criar_persona, criar_comunidade, criar_aula):
    import pytest

    from nucleo.aulas.regra import cancelar_aula
    from nucleo.erros import ErroDeValidacao

    admin = criar_persona(Papel.admin)
    aula = criar_aula(admin, criar_comunidade(), inicio_em=ONTEM - timedelta(hours=2), fim_em=ONTEM)

    with pytest.raises(ErroDeValidacao) as erro:
        cancelar_aula(sessao, operador=admin, aula=aula, motivo="Chuva")
    assert erro.value.campo == "situacao"
