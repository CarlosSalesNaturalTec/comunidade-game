from datetime import date
from decimal import Decimal

from nucleo.aportes.modelo import FormaDeAporte
from nucleo.livro_razao.modelo import NaturezaDoLancamento
from nucleo.personas.modelo import Papel
from nucleo.prestacao_de_contas.regra import (
    consumo_por_aula_e_comunidade,
    movimentado_total_e_por_provedor,
)


def test_o_aporte_novo_aparece_na_leitura_seguinte(
    sessao,
    criar_persona,
    criar_comunidade,
    criar_ponto_de_apoio,
    criar_tipo_de_recurso,
    criar_lancamento,
    criar_aporte,
):
    admin = criar_persona(Papel.admin)
    apoiador = criar_persona(Papel.apoiador)
    comunidade = criar_comunidade()
    ponto_de_apoio = criar_ponto_de_apoio(admin, comunidade)
    tipo = criar_tipo_de_recurso(admin)

    total_antes, _ = movimentado_total_e_por_provedor(sessao)
    assert total_antes == Decimal("0")

    credito = criar_lancamento(
        admin,
        tipo,
        ponto_de_apoio,
        natureza=NaturezaDoLancamento.credito,
        quantidade=Decimal("2.00"),
        valor_em_moedas=Decimal("2.00"),
    )
    criar_aporte(
        admin,
        apoiador,
        tipo,
        ponto_de_apoio,
        credito,
        quantidade=Decimal("2.00"),
        valor_em_moedas=Decimal("2.00"),
        forma=FormaDeAporte.financeira,
    )

    total_depois, _ = movimentado_total_e_por_provedor(sessao)
    assert total_depois == Decimal("2.00")


def test_a_recontagem_devolve_o_mesmo_movimentado(
    sessao,
    criar_persona,
    criar_comunidade,
    criar_ponto_de_apoio,
    criar_tipo_de_recurso,
    criar_lancamento,
    criar_aporte,
):
    admin = criar_persona(Papel.admin)
    apoiador = criar_persona(Papel.apoiador)
    comunidade = criar_comunidade()
    ponto_de_apoio = criar_ponto_de_apoio(admin, comunidade)
    tipo = criar_tipo_de_recurso(admin)

    credito = criar_lancamento(
        admin,
        tipo,
        ponto_de_apoio,
        natureza=NaturezaDoLancamento.credito,
        valor_em_moedas=Decimal("3.00"),
    )
    criar_aporte(
        admin,
        apoiador,
        tipo,
        ponto_de_apoio,
        credito,
        valor_em_moedas=Decimal("3.00"),
        forma=FormaDeAporte.financeira,
    )

    primeira, _ = movimentado_total_e_por_provedor(sessao)
    segunda, _ = movimentado_total_e_por_provedor(sessao)

    assert primeira == segunda == Decimal("3.00")


def test_o_movimentado_total_soma_os_creditos_do_livro_razao(
    sessao,
    criar_persona,
    criar_comunidade,
    criar_ponto_de_apoio,
    criar_tipo_de_recurso,
    criar_lancamento,
    criar_aporte,
):
    admin = criar_persona(Papel.admin)
    apoiador_a = criar_persona(Papel.apoiador)
    apoiador_b = criar_persona(Papel.apoiador)
    comunidade = criar_comunidade()
    ponto_de_apoio = criar_ponto_de_apoio(admin, comunidade)
    tipo = criar_tipo_de_recurso(admin)

    credito_a = criar_lancamento(
        admin,
        tipo,
        ponto_de_apoio,
        natureza=NaturezaDoLancamento.credito,
        valor_em_moedas=Decimal("1.50"),
    )
    criar_aporte(
        admin,
        apoiador_a,
        tipo,
        ponto_de_apoio,
        credito_a,
        valor_em_moedas=Decimal("1.50"),
        forma=FormaDeAporte.financeira,
    )
    credito_b = criar_lancamento(
        admin,
        tipo,
        ponto_de_apoio,
        natureza=NaturezaDoLancamento.credito,
        valor_em_moedas=Decimal("2.50"),
    )
    criar_aporte(
        admin,
        apoiador_b,
        tipo,
        ponto_de_apoio,
        credito_b,
        valor_em_moedas=Decimal("2.50"),
        forma=FormaDeAporte.financeira,
    )

    total, por_provedor = movimentado_total_e_por_provedor(sessao)

    assert total == Decimal("4.00")
    valores = {linha.provedor_id: linha.movimentado_em_moedas for linha in por_provedor}
    assert valores[apoiador_a.id] == Decimal("1.50")
    assert valores[apoiador_b.id] == Decimal("2.50")


def test_o_consumo_da_aula_e_o_que_o_debito_gravou(
    sessao,
    criar_persona,
    criar_comunidade,
    criar_ponto_de_apoio,
    criar_tipo_de_recurso,
    criar_valor_de_referencia,
    criar_lancamento,
    criar_aula,
):
    admin = criar_persona(Papel.admin)
    comunidade = criar_comunidade()
    ponto_de_apoio = criar_ponto_de_apoio(admin, comunidade)
    tipo = criar_tipo_de_recurso(admin)
    criar_valor_de_referencia(admin, tipo, valor_em_moedas=Decimal("0.50"))
    aula = criar_aula(admin, comunidade, ponto_de_apoio=ponto_de_apoio)

    criar_lancamento(
        admin,
        tipo,
        ponto_de_apoio,
        natureza=NaturezaDoLancamento.debito,
        quantidade=Decimal("2.00"),
        valor_em_moedas=Decimal("1.00"),
        aula=aula,
    )

    # O valor de referência muda depois da baixa; o consumo já gravado não
    # se revalora por isso (`RN-07-33`, `RN-07-36`).
    criar_valor_de_referencia(
        admin, tipo, valor_em_moedas=Decimal("0.80"), vigencia_inicio=date(2026, 6, 1)
    )

    aulas, _ = consumo_por_aula_e_comunidade(sessao)

    assert len(aulas) == 1
    assert aulas[0].aula_id == aula.id
    assert aulas[0].consumo_em_moedas == Decimal("1.00")


def test_o_consumo_agrega_por_comunidade(
    sessao,
    criar_persona,
    criar_comunidade,
    criar_ponto_de_apoio,
    criar_tipo_de_recurso,
    criar_lancamento,
    criar_aula,
):
    admin = criar_persona(Papel.admin)
    comunidade_a = criar_comunidade("Comunidade A")
    comunidade_b = criar_comunidade("Comunidade B")
    ponto_a = criar_ponto_de_apoio(admin, comunidade_a)
    ponto_b = criar_ponto_de_apoio(admin, comunidade_b)
    tipo = criar_tipo_de_recurso(admin)
    aula_a = criar_aula(admin, comunidade_a, ponto_de_apoio=ponto_a)
    aula_b = criar_aula(admin, comunidade_b, ponto_de_apoio=ponto_b)

    criar_lancamento(
        admin,
        tipo,
        ponto_a,
        natureza=NaturezaDoLancamento.debito,
        valor_em_moedas=Decimal("1.00"),
        aula=aula_a,
    )
    criar_lancamento(
        admin,
        tipo,
        ponto_b,
        natureza=NaturezaDoLancamento.debito,
        valor_em_moedas=Decimal("2.00"),
        aula=aula_b,
    )

    _, comunidades = consumo_por_aula_e_comunidade(sessao)

    valores = {linha.comunidade_virtual_id: linha.consumo_em_moedas for linha in comunidades}
    assert valores[comunidade_a.id] == Decimal("1.00")
    assert valores[comunidade_b.id] == Decimal("2.00")


def test_aula_sem_baixa_nao_aparece_com_consumo(
    sessao, criar_persona, criar_comunidade, criar_ponto_de_apoio, criar_aula
):
    admin = criar_persona(Papel.admin)
    comunidade = criar_comunidade()
    ponto_de_apoio = criar_ponto_de_apoio(admin, comunidade)
    criar_aula(admin, comunidade, ponto_de_apoio=ponto_de_apoio)

    aulas, comunidades = consumo_por_aula_e_comunidade(sessao)

    assert aulas == []
    assert comunidades == []
