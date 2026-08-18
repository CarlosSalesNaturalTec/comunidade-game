from decimal import Decimal

from nucleo.livro_razao.regra import saldo_de
from nucleo.personas.modelo import Papel
from nucleo.reservas.modelo import EstadoDaReserva, Reserva
from nucleo.reservas.regra import (
    confirmar_aulas_pendentes,
    consumir_reservas_da_aula,
    disponivel_de,
    liberar_reservas_da_aula,
    quantidade_reservada,
    tentar_reservar_recursos,
)


def test_reserva_nao_altera_o_saldo_derivado(
    sessao,
    criar_persona,
    criar_comunidade,
    criar_ponto_de_apoio,
    criar_tipo_de_recurso,
    criar_lancamento,
    criar_aula,
    criar_recurso_declarado_da_aula,
):
    admin = criar_persona(Papel.admin)
    comunidade = criar_comunidade()
    ponto_de_apoio = criar_ponto_de_apoio(admin, comunidade)
    tipo = criar_tipo_de_recurso(admin)
    criar_lancamento(admin, tipo, ponto_de_apoio, quantidade=Decimal("10.00"))
    aula = criar_aula(admin, comunidade, ponto_de_apoio=ponto_de_apoio)
    criar_recurso_declarado_da_aula(aula, tipo, quantidade=Decimal("3.00"))

    saldo_antes = saldo_de(sessao, tipo_de_recurso_id=tipo.id, ponto_de_apoio_id=ponto_de_apoio.id)
    reservou = tentar_reservar_recursos(sessao, aula=aula, operador=admin)
    sessao.commit()

    assert reservou is True
    saldo_depois = saldo_de(sessao, tipo_de_recurso_id=tipo.id, ponto_de_apoio_id=ponto_de_apoio.id)
    assert saldo_depois == saldo_antes == Decimal("10.00")


def test_reserva_reduz_a_disponivel_sem_reduzir_o_saldo(
    sessao,
    criar_persona,
    criar_comunidade,
    criar_ponto_de_apoio,
    criar_tipo_de_recurso,
    criar_lancamento,
    criar_aula,
    criar_recurso_declarado_da_aula,
):
    admin = criar_persona(Papel.admin)
    comunidade = criar_comunidade()
    ponto_de_apoio = criar_ponto_de_apoio(admin, comunidade)
    tipo = criar_tipo_de_recurso(admin)
    criar_lancamento(admin, tipo, ponto_de_apoio, quantidade=Decimal("10.00"))
    aula = criar_aula(admin, comunidade, ponto_de_apoio=ponto_de_apoio)
    criar_recurso_declarado_da_aula(aula, tipo, quantidade=Decimal("4.00"))

    tentar_reservar_recursos(sessao, aula=aula, operador=admin)
    sessao.commit()

    saldo = saldo_de(sessao, tipo_de_recurso_id=tipo.id, ponto_de_apoio_id=ponto_de_apoio.id)
    disponivel = disponivel_de(
        sessao, tipo_de_recurso_id=tipo.id, ponto_de_apoio_id=ponto_de_apoio.id
    )
    assert saldo == Decimal("10.00")
    assert disponivel == Decimal("6.00")


def test_segunda_aula_nao_reserva_o_que_a_primeira_ja_comprometeu(
    sessao,
    criar_persona,
    criar_comunidade,
    criar_ponto_de_apoio,
    criar_tipo_de_recurso,
    criar_lancamento,
    criar_aula,
    criar_recurso_declarado_da_aula,
):
    admin = criar_persona(Papel.admin)
    comunidade = criar_comunidade()
    ponto_de_apoio = criar_ponto_de_apoio(admin, comunidade)
    tipo = criar_tipo_de_recurso(admin)
    criar_lancamento(admin, tipo, ponto_de_apoio, quantidade=Decimal("10.00"))

    primeira_aula = criar_aula(admin, comunidade, ponto_de_apoio=ponto_de_apoio)
    criar_recurso_declarado_da_aula(primeira_aula, tipo, quantidade=Decimal("8.00"))
    assert tentar_reservar_recursos(sessao, aula=primeira_aula, operador=admin) is True
    sessao.commit()

    segunda_aula = criar_aula(admin, comunidade, ponto_de_apoio=ponto_de_apoio)
    criar_recurso_declarado_da_aula(segunda_aula, tipo, quantidade=Decimal("5.00"))
    reservou = tentar_reservar_recursos(sessao, aula=segunda_aula, operador=admin)
    sessao.commit()

    assert reservou is False
    assert sessao.query(Reserva).filter_by(aula_id=segunda_aula.id).count() == 0
    disponivel = disponivel_de(
        sessao, tipo_de_recurso_id=tipo.id, ponto_de_apoio_id=ponto_de_apoio.id
    )
    assert disponivel == Decimal("2.00")


def test_falta_em_um_tipo_nao_reserva_nenhum_dos_dois(
    sessao,
    criar_persona,
    criar_comunidade,
    criar_ponto_de_apoio,
    criar_tipo_de_recurso,
    criar_lancamento,
    criar_aula,
    criar_recurso_declarado_da_aula,
):
    admin = criar_persona(Papel.admin)
    comunidade = criar_comunidade()
    ponto_de_apoio = criar_ponto_de_apoio(admin, comunidade)
    tipo_com_saldo = criar_tipo_de_recurso(admin, nome="Lanche")
    tipo_sem_saldo = criar_tipo_de_recurso(admin, nome="Kit")
    criar_lancamento(admin, tipo_com_saldo, ponto_de_apoio, quantidade=Decimal("10.00"))

    aula = criar_aula(admin, comunidade, ponto_de_apoio=ponto_de_apoio)
    criar_recurso_declarado_da_aula(aula, tipo_com_saldo, quantidade=Decimal("3.00"))
    criar_recurso_declarado_da_aula(aula, tipo_sem_saldo, quantidade=Decimal("1.00"))

    reservou = tentar_reservar_recursos(sessao, aula=aula, operador=admin)
    sessao.commit()

    assert reservou is False
    assert sessao.query(Reserva).filter_by(aula_id=aula.id).count() == 0
    disponivel_com_saldo = disponivel_de(
        sessao, tipo_de_recurso_id=tipo_com_saldo.id, ponto_de_apoio_id=ponto_de_apoio.id
    )
    assert disponivel_com_saldo == Decimal("10.00")


def test_aula_sem_recurso_declarado_reserva_trivialmente(
    sessao, criar_persona, criar_comunidade, criar_aula
):
    admin = criar_persona(Papel.admin)
    comunidade = criar_comunidade()
    aula = criar_aula(admin, comunidade)

    assert tentar_reservar_recursos(sessao, aula=aula, operador=admin) is True
    assert sessao.query(Reserva).filter_by(aula_id=aula.id).count() == 0


def test_baixa_leva_a_reserva_a_consumida_e_deriuba_o_saldo(
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
    ponto_de_apoio = criar_ponto_de_apoio(admin, comunidade)
    tipo = criar_tipo_de_recurso(admin)
    criar_lancamento(admin, tipo, ponto_de_apoio, quantidade=Decimal("10.00"))
    criar_valor_de_referencia(admin, tipo, valor_em_moedas=Decimal("2.00"))
    aula = criar_aula(admin, comunidade, ponto_de_apoio=ponto_de_apoio)
    reserva = criar_reserva(admin, aula, tipo, ponto_de_apoio, quantidade=Decimal("3.00"))

    lancamentos = consumir_reservas_da_aula(sessao, aula=aula, operador=admin)
    sessao.commit()

    assert len(lancamentos) == 1
    assert lancamentos[0].quantidade == Decimal("3.00")
    sessao.refresh(reserva)
    assert reserva.estado == EstadoDaReserva.consumida

    saldo = saldo_de(sessao, tipo_de_recurso_id=tipo.id, ponto_de_apoio_id=ponto_de_apoio.id)
    disponivel = disponivel_de(
        sessao, tipo_de_recurso_id=tipo.id, ponto_de_apoio_id=ponto_de_apoio.id
    )
    assert saldo == Decimal("7.00")
    assert disponivel == Decimal("7.00")


def test_liberacao_devolve_a_quantidade_a_disponivel(
    sessao,
    criar_persona,
    criar_comunidade,
    criar_ponto_de_apoio,
    criar_tipo_de_recurso,
    criar_lancamento,
    criar_aula,
    criar_reserva,
):
    admin = criar_persona(Papel.admin)
    comunidade = criar_comunidade()
    ponto_de_apoio = criar_ponto_de_apoio(admin, comunidade)
    tipo = criar_tipo_de_recurso(admin)
    criar_lancamento(admin, tipo, ponto_de_apoio, quantidade=Decimal("10.00"))
    aula = criar_aula(admin, comunidade, ponto_de_apoio=ponto_de_apoio)
    reserva = criar_reserva(admin, aula, tipo, ponto_de_apoio, quantidade=Decimal("4.00"))

    liberar_reservas_da_aula(sessao, aula=aula)
    sessao.commit()

    sessao.refresh(reserva)
    assert reserva.estado == EstadoDaReserva.liberada
    disponivel = disponivel_de(
        sessao, tipo_de_recurso_id=tipo.id, ponto_de_apoio_id=ponto_de_apoio.id
    )
    assert disponivel == Decimal("10.00")


def test_aula_que_passou_da_data_mantem_a_reserva(
    sessao,
    criar_persona,
    criar_comunidade,
    criar_ponto_de_apoio,
    criar_tipo_de_recurso,
    criar_lancamento,
    criar_aula,
    criar_reserva,
):
    from datetime import UTC, datetime, timedelta

    admin = criar_persona(Papel.admin)
    comunidade = criar_comunidade()
    ponto_de_apoio = criar_ponto_de_apoio(admin, comunidade)
    tipo = criar_tipo_de_recurso(admin)
    criar_lancamento(admin, tipo, ponto_de_apoio, quantidade=Decimal("10.00"))
    agora = datetime.now(UTC)
    aula = criar_aula(
        admin,
        comunidade,
        ponto_de_apoio=ponto_de_apoio,
        inicio_em=agora - timedelta(days=2),
        fim_em=agora - timedelta(days=2, hours=-1),
    )
    reserva = criar_reserva(admin, aula, tipo, ponto_de_apoio, quantidade=Decimal("4.00"))

    # Nada no núcleo observa o relógio para desfazer reserva — a passagem
    # do tempo sozinha não move estado algum (`RF-07-09`, PRD-07 §5.3).
    sessao.refresh(reserva)
    assert reserva.estado == EstadoDaReserva.reservada
    disponivel = disponivel_de(
        sessao, tipo_de_recurso_id=tipo.id, ponto_de_apoio_id=ponto_de_apoio.id
    )
    assert disponivel == Decimal("6.00")


def test_confirmar_aulas_pendentes_atende_a_mais_proxima_primeiro(
    sessao,
    criar_persona,
    criar_comunidade,
    criar_ponto_de_apoio,
    criar_tipo_de_recurso,
    criar_lancamento,
    criar_aula,
    criar_recurso_declarado_da_aula,
):
    from datetime import UTC, datetime, timedelta

    from nucleo.aulas.modelo import SituacaoDaAula

    admin = criar_persona(Papel.admin)
    comunidade = criar_comunidade()
    ponto_de_apoio = criar_ponto_de_apoio(admin, comunidade)
    tipo = criar_tipo_de_recurso(admin)
    agora = datetime.now(UTC)

    aula_distante = criar_aula(
        admin,
        comunidade,
        ponto_de_apoio=ponto_de_apoio,
        inicio_em=agora + timedelta(days=5),
        fim_em=agora + timedelta(days=5, hours=1),
    )
    aula_proxima = criar_aula(
        admin,
        comunidade,
        ponto_de_apoio=ponto_de_apoio,
        inicio_em=agora + timedelta(days=1),
        fim_em=agora + timedelta(days=1, hours=1),
    )
    criar_recurso_declarado_da_aula(aula_distante, tipo, quantidade=Decimal("6.00"))
    criar_recurso_declarado_da_aula(aula_proxima, tipo, quantidade=Decimal("6.00"))
    aula_distante.situacao = SituacaoDaAula.pendente_de_lastro
    aula_proxima.situacao = SituacaoDaAula.pendente_de_lastro
    sessao.commit()

    # Só há disponível para uma das duas.
    criar_lancamento(admin, tipo, ponto_de_apoio, quantidade=Decimal("6.00"))

    confirmadas = confirmar_aulas_pendentes(
        sessao, tipo=tipo, ponto_de_apoio=ponto_de_apoio, operador=admin
    )
    sessao.commit()

    assert [a.id for a in confirmadas] == [aula_proxima.id]
    sessao.refresh(aula_proxima)
    sessao.refresh(aula_distante)
    assert aula_proxima.situacao == SituacaoDaAula.confirmada
    assert aula_distante.situacao == SituacaoDaAula.pendente_de_lastro
    assert quantidade_reservada(
        sessao, tipo_de_recurso_id=tipo.id, ponto_de_apoio_id=ponto_de_apoio.id
    ) == Decimal("6.00")
