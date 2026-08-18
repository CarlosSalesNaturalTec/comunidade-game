from decimal import Decimal

from nucleo.personas.modelo import Papel


def test_fluxo_completo_de_ressarcimento_pela_rota(
    cliente,
    criar_chave,
    criar_persona,
    criar_sessao_de_teste,
    criar_comunidade,
    criar_ponto_de_apoio,
    criar_tipo_de_recurso,
    criar_valor_de_referencia,
):
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    mestre = criar_persona(Papel.mestre, criada_por=admin)
    apoiador = criar_persona(Papel.apoiador)
    token_admin, _ = criar_sessao_de_teste(admin)
    token_mestre, _ = criar_sessao_de_teste(mestre)
    comunidade = criar_comunidade()
    ponto_de_apoio = criar_ponto_de_apoio(admin, comunidade)
    tipo = criar_tipo_de_recurso(admin)
    criar_valor_de_referencia(admin, tipo, valor_em_moedas=Decimal("1.00"))

    resposta_absorcao = cliente.post(
        "/v1/aportes/absorcao",
        data={
            "tipo_de_recurso_id": str(tipo.id),
            "quantidade": "5",
            "ponto_de_apoio_id": str(ponto_de_apoio.id),
            "data_do_aporte": "2026-06-01",
            "valor_de_origem": "50.00",
        },
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token_mestre}"},
    )
    assert resposta_absorcao.status_code == 201
    aporte_id = resposta_absorcao.json()["id"]

    resposta_receita = cliente.post(
        "/v1/aportes",
        data={
            "provedor_id": str(apoiador.id),
            "tipo_de_recurso_id": str(tipo.id),
            "quantidade": "100",
            "ponto_de_apoio_id": str(ponto_de_apoio.id),
            "data_do_aporte": "2026-06-02",
            "forma": "financeira",
            "destinacao": "ressarcimento",
            "valor_de_origem": "100.00",
        },
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token_admin}"},
    )
    assert resposta_receita.status_code == 201
    receita_id = resposta_receita.json()["id"]

    resposta_fila = cliente.get(
        "/v1/aportes/ressarciveis",
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token_admin}"},
    )
    assert resposta_fila.status_code == 200
    corpo_fila = resposta_fila.json()
    assert aporte_id in [item["id"] for item in corpo_fila["aportes"]]

    resposta_ressarcimento = cliente.post(
        f"/v1/aportes/{aporte_id}/ressarcimento",
        data={"receita_destinada_id": receita_id, "data": "2026-07-01"},
        files={"comprovante": ("comprovante.pdf", b"conteudo", "application/pdf")},
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token_admin}"},
    )
    assert resposta_ressarcimento.status_code == 201
    assert resposta_ressarcimento.json()["valor_em_reais"] == "50.00"

    resposta_minhas = cliente.get(
        "/v1/meus-aportes/ressarciveis",
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token_mestre}"},
    )
    assert resposta_minhas.status_code == 200
    situacoes = {item["id"]: item["situacao_de_ressarcimento"] for item in resposta_minhas.json()}
    assert situacoes[aporte_id] == "ressarcido"


def test_ressarcimento_sem_comprovante_pela_rota_e_422(
    cliente,
    criar_chave,
    criar_persona,
    criar_sessao_de_teste,
    criar_comunidade,
    criar_ponto_de_apoio,
    criar_tipo_de_recurso,
    criar_valor_de_referencia,
):
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    mestre = criar_persona(Papel.mestre, criada_por=admin)
    apoiador = criar_persona(Papel.apoiador)
    token_admin, _ = criar_sessao_de_teste(admin)
    token_mestre, _ = criar_sessao_de_teste(mestre)
    comunidade = criar_comunidade()
    ponto_de_apoio = criar_ponto_de_apoio(admin, comunidade)
    tipo = criar_tipo_de_recurso(admin)
    criar_valor_de_referencia(admin, tipo, valor_em_moedas=Decimal("1.00"))

    resposta_absorcao = cliente.post(
        "/v1/aportes/absorcao",
        data={
            "tipo_de_recurso_id": str(tipo.id),
            "quantidade": "5",
            "ponto_de_apoio_id": str(ponto_de_apoio.id),
            "data_do_aporte": "2026-06-01",
            "valor_de_origem": "50.00",
        },
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token_mestre}"},
    )
    aporte_id = resposta_absorcao.json()["id"]

    resposta_receita = cliente.post(
        "/v1/aportes",
        data={
            "provedor_id": str(apoiador.id),
            "tipo_de_recurso_id": str(tipo.id),
            "quantidade": "100",
            "ponto_de_apoio_id": str(ponto_de_apoio.id),
            "data_do_aporte": "2026-06-02",
            "forma": "financeira",
            "destinacao": "ressarcimento",
            "valor_de_origem": "100.00",
        },
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token_admin}"},
    )
    receita_id = resposta_receita.json()["id"]

    resposta = cliente.post(
        f"/v1/aportes/{aporte_id}/ressarcimento",
        data={"receita_destinada_id": receita_id, "data": "2026-07-01"},
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token_admin}"},
    )
    assert resposta.status_code == 422
