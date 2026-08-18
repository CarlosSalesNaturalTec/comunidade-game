from nucleo.personas.modelo import Papel


def test_admin_cadastra_ponto_de_apoio_pela_rota(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste, criar_comunidade
):
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    comunidade = criar_comunidade()
    token, _ = criar_sessao_de_teste(admin)

    resposta = cliente.post(
        "/v1/pontos-de-apoio",
        json={"nome": "Sede", "comunidade_id": str(comunidade.id)},
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
    )

    assert resposta.status_code == 201
    corpo = resposta.json()
    assert corpo["nome"] == "Sede"
    assert corpo["comunidade_virtual_id"] == str(comunidade.id)
    assert corpo["responsavel_id"] is None
    assert corpo["ativo"] is True


def test_quem_nao_e_admin_recebe_403_ao_cadastrar_ponto_de_apoio(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste, criar_comunidade
):
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    mestre = criar_persona(Papel.mestre, criada_por=admin)
    comunidade = criar_comunidade()
    token, _ = criar_sessao_de_teste(mestre)

    resposta = cliente.post(
        "/v1/pontos-de-apoio",
        json={"nome": "Sede", "comunidade_id": str(comunidade.id)},
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
    )

    assert resposta.status_code == 403


def test_cadastro_de_ponto_de_apoio_sem_chave_e_recusado_com_401(
    cliente, criar_persona, criar_sessao_de_teste, criar_comunidade
):
    admin = criar_persona(Papel.admin)
    comunidade = criar_comunidade()
    token, _ = criar_sessao_de_teste(admin)

    resposta = cliente.post(
        "/v1/pontos-de-apoio",
        json={"nome": "Sede", "comunidade_id": str(comunidade.id)},
        headers={"Authorization": f"Bearer {token}"},
    )

    assert resposta.status_code == 401


def test_admin_designa_responsavel_pela_rota(
    cliente,
    criar_chave,
    criar_persona,
    criar_sessao_de_teste,
    criar_comunidade,
    criar_ponto_de_apoio,
):
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    comunidade = criar_comunidade()
    ponto_de_apoio = criar_ponto_de_apoio(admin, comunidade)
    mestre = criar_persona(Papel.mestre, criada_por=admin)
    token, _ = criar_sessao_de_teste(admin)

    resposta = cliente.put(
        f"/v1/pontos-de-apoio/{ponto_de_apoio.id}/responsavel",
        json={"responsavel_id": str(mestre.id)},
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
    )

    assert resposta.status_code == 200
    corpo = resposta.json()
    assert corpo["responsavel_id"] == str(mestre.id)


def test_guerreiro_designado_responsavel_e_recusado_com_422_pela_rota(
    cliente,
    criar_chave,
    criar_persona,
    criar_sessao_de_teste,
    criar_comunidade,
    criar_ponto_de_apoio,
):
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    comunidade = criar_comunidade()
    ponto_de_apoio = criar_ponto_de_apoio(admin, comunidade)
    guerreiro = criar_persona(Papel.guerreiro, comunidade=comunidade)
    token, _ = criar_sessao_de_teste(admin)

    resposta = cliente.put(
        f"/v1/pontos-de-apoio/{ponto_de_apoio.id}/responsavel",
        json={"responsavel_id": str(guerreiro.id)},
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
    )

    assert resposta.status_code == 422
