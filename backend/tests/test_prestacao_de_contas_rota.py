from decimal import Decimal

from nucleo.aportes.modelo import FormaDeAporte
from nucleo.livro_razao.modelo import NaturezaDoLancamento
from nucleo.personas.modelo import Papel


def test_visitante_sem_persona_le_a_prestacao_de_contas(
    cliente,
    criar_chave,
    criar_persona,
    criar_comunidade,
    criar_ponto_de_apoio,
    criar_tipo_de_recurso,
    criar_lancamento,
    criar_aporte,
):
    chave, _ = criar_chave()
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
        valor_em_moedas=Decimal("1.50"),
    )
    criar_aporte(
        admin,
        apoiador,
        tipo,
        ponto_de_apoio,
        credito,
        valor_em_moedas=Decimal("1.50"),
        forma=FormaDeAporte.financeira,
    )

    resposta = cliente.get("/v1/prestacao-de-contas", headers={"X-Chave-Aplicacao": chave})

    assert resposta.status_code == 200
    corpo = resposta.json()
    assert corpo["movimentado_total_em_moedas"] == "1.50"


def test_sem_chave_a_rota_nao_responde(cliente):
    resposta = cliente.get("/v1/prestacao-de-contas")

    assert resposta.status_code == 401

    resposta_aulas = cliente.get("/v1/prestacao-de-contas/aulas")

    assert resposta_aulas.status_code == 401


def test_nenhuma_resposta_traz_reais_comprovante_ou_guerreiro(
    cliente,
    sessao,
    criar_chave,
    criar_persona,
    criar_comunidade,
    criar_ponto_de_apoio,
    criar_tipo_de_recurso,
    criar_lancamento,
    criar_aporte,
    criar_aula,
):
    chave, _ = criar_chave()
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
        valor_em_moedas=Decimal("1.50"),
    )
    criar_aporte(
        admin,
        apoiador,
        tipo,
        ponto_de_apoio,
        credito,
        valor_em_moedas=Decimal("1.50"),
        valor_de_origem=Decimal("30.00"),
        forma=FormaDeAporte.financeira,
    )
    aula = criar_aula(admin, comunidade, ponto_de_apoio=ponto_de_apoio)
    criar_lancamento(
        admin,
        tipo,
        ponto_de_apoio,
        natureza=NaturezaDoLancamento.debito,
        valor_em_moedas=Decimal("0.50"),
        aula=aula,
    )

    resposta_contas = cliente.get("/v1/prestacao-de-contas", headers={"X-Chave-Aplicacao": chave})
    resposta_aulas = cliente.get(
        "/v1/prestacao-de-contas/aulas", headers={"X-Chave-Aplicacao": chave}
    )

    for texto in (resposta_contas.text.lower(), resposta_aulas.text.lower()):
        assert "reais" not in texto
        assert "comprovante" not in texto
        assert "guerreiro" not in texto
        assert "nick" not in texto
        assert "avatar" not in texto
