from nucleo.personas.modelo import Papel


def test_apoiador_declara_aporte_pela_rota(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste
):
    chave, _ = criar_chave()
    apoiador = criar_persona(Papel.apoiador)
    token, _ = criar_sessao_de_teste(apoiador)

    resposta = cliente.post(
        "/v1/aportes/declarados",
        data={
            "valor_declarado": "50.00",
            "forma": "financeira",
            "origem_da_escolha": "valor_livre",
        },
        files={"comprovante": ("comprovante.pdf", b"conteudo", "application/pdf")},
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
    )

    assert resposta.status_code == 201
    corpo = resposta.json()
    assert corpo["situacao"] == "pendente"
    assert corpo["valor_declarado"] == "50.00"


def test_declarar_aporte_sem_sessao_e_recusado_com_401(cliente, criar_chave):
    chave, _ = criar_chave()

    resposta = cliente.post(
        "/v1/aportes/declarados",
        data={
            "valor_declarado": "50.00",
            "forma": "financeira",
            "origem_da_escolha": "valor_livre",
        },
        files={"comprovante": ("comprovante.pdf", b"conteudo", "application/pdf")},
        headers={"X-Chave-Aplicacao": chave},
    )

    assert resposta.status_code == 401


def test_leitura_alcanca_so_as_proprias_declaracoes(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste
):
    chave, _ = criar_chave()
    apoiador_a = criar_persona(Papel.apoiador)
    apoiador_b = criar_persona(Papel.apoiador)
    token_a, _ = criar_sessao_de_teste(apoiador_a)
    token_b, _ = criar_sessao_de_teste(apoiador_b)

    for token in (token_a, token_b):
        cliente.post(
            "/v1/aportes/declarados",
            data={
                "valor_declarado": "10.00",
                "forma": "financeira",
                "origem_da_escolha": "valor_livre",
            },
            files={"comprovante": ("comprovante.pdf", b"conteudo", "application/pdf")},
            headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
        )

    resposta = cliente.get(
        "/v1/eu/aportes/declarados",
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token_a}"},
    )

    assert resposta.status_code == 200
    corpo = resposta.json()
    assert len(corpo) == 1


def test_admin_recusa_declaracao_com_motivo(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste
):
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    apoiador = criar_persona(Papel.apoiador)
    token_apoiador, _ = criar_sessao_de_teste(apoiador)
    token_admin, _ = criar_sessao_de_teste(admin)

    resposta_declaracao = cliente.post(
        "/v1/aportes/declarados",
        data={
            "valor_declarado": "10.00",
            "forma": "financeira",
            "origem_da_escolha": "valor_livre",
        },
        files={"comprovante": ("comprovante.pdf", b"conteudo", "application/pdf")},
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token_apoiador}"},
    )
    id_da_declaracao = resposta_declaracao.json()["id"]

    resposta = cliente.post(
        f"/v1/aportes/declarados/{id_da_declaracao}/recusa",
        json={"motivo": "Comprovante ilegível."},
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token_admin}"},
    )

    assert resposta.status_code == 200
    corpo = resposta.json()
    assert corpo["situacao"] == "recusada"
    assert corpo["motivo_da_recusa"] == "Comprovante ilegível."


def test_recusa_e_restrita_a_admin(cliente, criar_chave, criar_persona, criar_sessao_de_teste):
    chave, _ = criar_chave()
    apoiador = criar_persona(Papel.apoiador)
    outro_apoiador = criar_persona(Papel.apoiador)
    token_apoiador, _ = criar_sessao_de_teste(apoiador)
    token_outro, _ = criar_sessao_de_teste(outro_apoiador)

    resposta_declaracao = cliente.post(
        "/v1/aportes/declarados",
        data={
            "valor_declarado": "10.00",
            "forma": "financeira",
            "origem_da_escolha": "valor_livre",
        },
        files={"comprovante": ("comprovante.pdf", b"conteudo", "application/pdf")},
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token_apoiador}"},
    )
    id_da_declaracao = resposta_declaracao.json()["id"]

    resposta = cliente.post(
        f"/v1/aportes/declarados/{id_da_declaracao}/recusa",
        json={"motivo": "Motivo qualquer."},
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token_outro}"},
    )

    assert resposta.status_code == 403
