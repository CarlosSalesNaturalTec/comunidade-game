import uuid
from decimal import Decimal

from nucleo.aportes.modelo import FormaDeAporte
from nucleo.livro_razao.modelo import NaturezaDoLancamento
from nucleo.personas.modelo import Papel


def test_visitante_sem_persona_le_o_poder_sustentador(
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
        quantidade=Decimal("3.00"),
        valor_em_moedas=Decimal("1.50"),
    )
    criar_aporte(
        admin,
        apoiador,
        tipo,
        ponto_de_apoio,
        credito,
        quantidade=Decimal("3.00"),
        valor_em_moedas=Decimal("1.50"),
        forma=FormaDeAporte.absorcao,
    )

    resposta = cliente.get(
        f"/v1/provedores/{apoiador.id}/poder-sustentador", headers={"X-Chave-Aplicacao": chave}
    )

    assert resposta.status_code == 200
    corpo = resposta.json()
    assert corpo["provedor_id"] == str(apoiador.id)
    assert corpo["poder_sustentador_em_moedas"] == "1.50"
    assert corpo["absorcoes"] == 1


def test_sem_chave_a_rota_do_provedor_nao_responde(cliente, criar_persona):
    apoiador = criar_persona(Papel.apoiador)

    resposta = cliente.get(f"/v1/provedores/{apoiador.id}/poder-sustentador")

    assert resposta.status_code == 401


def test_a_rota_nao_serve_guerreiro(cliente, criar_chave, criar_persona, criar_comunidade):
    chave, _ = criar_chave()
    comunidade = criar_comunidade()
    guerreiro = criar_persona(Papel.guerreiro, comunidade=comunidade)

    resposta = cliente.get(
        f"/v1/provedores/{guerreiro.id}/poder-sustentador", headers={"X-Chave-Aplicacao": chave}
    )

    assert resposta.status_code == 404


def test_identificador_inexistente_devolve_o_mesmo_404(cliente, criar_chave):
    chave, _ = criar_chave()

    resposta = cliente.get(
        f"/v1/provedores/{uuid.uuid4()}/poder-sustentador", headers={"X-Chave-Aplicacao": chave}
    )

    assert resposta.status_code == 404


def test_nenhuma_saida_traz_reais(
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
    credito = criar_lancamento(admin, tipo, ponto_de_apoio, natureza=NaturezaDoLancamento.credito)
    criar_aporte(
        admin,
        apoiador,
        tipo,
        ponto_de_apoio,
        credito,
        valor_de_origem=Decimal("50.00"),
        forma=FormaDeAporte.financeira,
    )

    resposta = cliente.get(
        f"/v1/provedores/{apoiador.id}/poder-sustentador", headers={"X-Chave-Aplicacao": chave}
    )

    corpo_bruto = resposta.text
    assert "reais" not in corpo_bruto.lower()
    assert "valor_de_origem" not in corpo_bruto


def test_o_apoiador_ve_os_proprios_aportes(
    cliente,
    criar_chave,
    criar_persona,
    criar_sessao_de_teste,
    criar_comunidade,
    criar_ponto_de_apoio,
    criar_tipo_de_recurso,
    criar_lancamento,
    criar_aporte,
):
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    apoiador = criar_persona(Papel.apoiador)
    token, _ = criar_sessao_de_teste(apoiador)
    comunidade = criar_comunidade()
    ponto_de_apoio = criar_ponto_de_apoio(admin, comunidade)
    tipo = criar_tipo_de_recurso(admin)
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

    resposta = cliente.get(
        "/v1/meus-aportes", headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"}
    )

    assert resposta.status_code == 200
    corpo = resposta.json()
    assert corpo["poder_sustentador_em_moedas"] == "2.00"
    assert len(corpo["aportes"]) == 1


def test_o_aporte_alheio_fica_de_fora(
    cliente,
    criar_chave,
    criar_persona,
    criar_sessao_de_teste,
    criar_comunidade,
    criar_ponto_de_apoio,
    criar_tipo_de_recurso,
    criar_lancamento,
    criar_aporte,
):
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    apoiador_a = criar_persona(Papel.apoiador)
    apoiador_b = criar_persona(Papel.apoiador)
    token_a, _ = criar_sessao_de_teste(apoiador_a)
    comunidade = criar_comunidade()
    ponto_de_apoio = criar_ponto_de_apoio(admin, comunidade)
    tipo = criar_tipo_de_recurso(admin)

    credito_a = criar_lancamento(admin, tipo, ponto_de_apoio, natureza=NaturezaDoLancamento.credito)
    aporte_a = criar_aporte(
        admin, apoiador_a, tipo, ponto_de_apoio, credito_a, forma=FormaDeAporte.financeira
    )
    credito_b = criar_lancamento(admin, tipo, ponto_de_apoio, natureza=NaturezaDoLancamento.credito)
    criar_aporte(admin, apoiador_b, tipo, ponto_de_apoio, credito_b, forma=FormaDeAporte.financeira)

    resposta = cliente.get(
        "/v1/meus-aportes",
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token_a}"},
    )

    corpo = resposta.json()
    assert len(corpo["aportes"]) == 1
    assert corpo["aportes"][0]["id"] == str(aporte_a.id)


def test_meus_aportes_traz_o_nome_do_tipo_e_o_destino(
    cliente,
    criar_chave,
    criar_persona,
    criar_sessao_de_teste,
    criar_comunidade,
    criar_ponto_de_apoio,
    criar_tipo_de_recurso,
    criar_lancamento,
    criar_aporte,
):
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    apoiador = criar_persona(Papel.apoiador)
    token, _ = criar_sessao_de_teste(apoiador)
    comunidade = criar_comunidade()
    ponto_de_apoio = criar_ponto_de_apoio(admin, comunidade)
    tipo = criar_tipo_de_recurso(admin, nome="Lanche")
    credito = criar_lancamento(admin, tipo, ponto_de_apoio, natureza=NaturezaDoLancamento.credito)
    criar_aporte(admin, apoiador, tipo, ponto_de_apoio, credito, forma=FormaDeAporte.financeira)

    resposta = cliente.get(
        "/v1/meus-aportes", headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"}
    )

    assert resposta.status_code == 200
    aporte_na_saida = resposta.json()["aportes"][0]
    assert aporte_na_saida["tipo_de_recurso_nome"] == "Lanche"
    assert aporte_na_saida["ponto_de_apoio_nome"] == ponto_de_apoio.nome


def test_sem_sessao_a_rota_de_meus_aportes_nao_responde(cliente, criar_chave):
    chave, _ = criar_chave()

    resposta = cliente.get("/v1/meus-aportes", headers={"X-Chave-Aplicacao": chave})

    assert resposta.status_code == 401
