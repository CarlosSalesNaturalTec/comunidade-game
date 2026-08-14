from datetime import UTC, datetime

from nucleo.coletas.modelo import Cadencia
from nucleo.coletas.regra import periodo_de_cadencia


def test_virada_das_22h_de_sexta_permanece_na_semana_da_sexta():
    """`RN-08-06`: 22h de sexta em São Paulo (UTC-03) é 01h de sábado em
    UTC — apurar em UTC deslocaria a medição para a semana seguinte.
    2026-08-14 é sexta-feira; 22h em São Paulo é 2026-08-15T01:00Z."""
    momento_utc = datetime(2026, 8, 15, 1, 0, tzinfo=UTC)

    inicio, fim = periodo_de_cadencia(momento_utc, Cadencia.semanal)

    # A semana civil de segunda a domingo que contém sexta 2026-08-14 vai de
    # 2026-08-10 (segunda) a 2026-08-17 (fim exclusivo).
    inicio_esperado = datetime(2026, 8, 10, 3, 0, tzinfo=UTC)  # 00h de segunda em SP = 03h UTC
    fim_esperado = datetime(2026, 8, 17, 3, 0, tzinfo=UTC)
    assert inicio == inicio_esperado
    assert fim == fim_esperado
    assert inicio <= momento_utc < fim


def test_periodo_diario_e_o_dia_civil_em_sao_paulo():
    # 2026-08-15T01:00Z = 2026-08-14T22:00 em São Paulo.
    momento_utc = datetime(2026, 8, 15, 1, 0, tzinfo=UTC)

    inicio, fim = periodo_de_cadencia(momento_utc, Cadencia.diaria)

    assert inicio == datetime(2026, 8, 14, 3, 0, tzinfo=UTC)
    assert fim == datetime(2026, 8, 15, 3, 0, tzinfo=UTC)


def test_periodo_mensal_vira_o_ano_corretamente():
    # 2026-12-31T23:30 em São Paulo = 2027-01-01T02:30Z.
    momento_utc = datetime(2027, 1, 1, 2, 30, tzinfo=UTC)

    inicio, fim = periodo_de_cadencia(momento_utc, Cadencia.mensal)

    assert inicio == datetime(2026, 12, 1, 3, 0, tzinfo=UTC)
    assert fim == datetime(2027, 1, 1, 3, 0, tzinfo=UTC)
