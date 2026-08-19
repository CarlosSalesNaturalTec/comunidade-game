from nucleo.personas.modelo import Papel


def test_admin_tomba_item_pela_rota(
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
    token, _ = criar_sessao_de_teste(admin)

    resposta = cliente.post(
        "/v1/itens-patrimoniais",
        json={
            "titulo": "Descobrindo o Mundo",
            "numero_de_tombo": "0001",
            "ponto_de_apoio_id": str(ponto_de_apoio.id),
            "estado_de_conservacao": "novo",
        },
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
    )

    assert resposta.status_code == 201
    corpo = resposta.json()
    assert corpo["titulo"] == "Descobrindo o Mundo"
    assert corpo["numero_de_tombo"] == "0001"
    assert corpo["ficha_de_vida"] == []
    assert corpo["responsavel_id"] is None
    assert "valor_em_moedas" not in corpo
    assert "valor_de_origem" not in corpo


def test_admin_le_o_acervo_de_qualquer_comunidade(
    cliente,
    criar_chave,
    criar_persona,
    criar_sessao_de_teste,
    criar_comunidade,
    criar_ponto_de_apoio,
    criar_item_patrimonial,
):
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    comunidade = criar_comunidade()
    ponto_de_apoio = criar_ponto_de_apoio(admin, comunidade)
    criar_item_patrimonial(admin, ponto_de_apoio)
    token, _ = criar_sessao_de_teste(admin)

    resposta = cliente.get(
        "/v1/itens-patrimoniais",
        params={"comunidade_virtual_id": str(comunidade.id)},
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
    )

    assert resposta.status_code == 200
    assert len(resposta.json()) == 1


def test_mestre_le_apenas_o_acervo_da_sua_comunidade(
    cliente,
    criar_chave,
    criar_persona,
    criar_sessao_de_teste,
    criar_comunidade,
    criar_ponto_de_apoio,
    criar_item_patrimonial,
    criar_vinculo_jogador,
):
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    comunidade = criar_comunidade()
    outra_comunidade = criar_comunidade("Outra Comunidade")
    ponto_de_apoio = criar_ponto_de_apoio(admin, comunidade)
    outro_ponto = criar_ponto_de_apoio(admin, outra_comunidade)
    criar_item_patrimonial(admin, ponto_de_apoio, numero_de_tombo="0001")
    criar_item_patrimonial(admin, outro_ponto, numero_de_tombo="0001")
    mestre = criar_persona(Papel.mestre, criada_por=admin)
    criar_vinculo_jogador(mestre, comunidade)
    token, _ = criar_sessao_de_teste(mestre)

    resposta = cliente.get(
        "/v1/itens-patrimoniais",
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
    )

    assert resposta.status_code == 200
    corpo = resposta.json()
    assert len(corpo) == 1
    assert corpo[0]["ponto_de_apoio_id"] == str(ponto_de_apoio.id)


def test_apoiador_nao_le_o_acervo_da_gestao(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste
):
    chave, _ = criar_chave()
    apoiador = criar_persona(Papel.apoiador)
    token, _ = criar_sessao_de_teste(apoiador)

    resposta = cliente.get(
        "/v1/itens-patrimoniais",
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
    )

    assert resposta.status_code == 403


def test_leitura_traz_o_responsavel_derivado_do_ponto_de_apoio(
    cliente,
    criar_chave,
    criar_persona,
    criar_sessao_de_teste,
    criar_comunidade,
    criar_ponto_de_apoio,
    criar_item_patrimonial,
):
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    comunidade = criar_comunidade()
    responsavel = criar_persona(Papel.mestre, criada_por=admin)
    ponto_de_apoio = criar_ponto_de_apoio(admin, comunidade, responsavel=responsavel)
    criar_item_patrimonial(admin, ponto_de_apoio)
    token, _ = criar_sessao_de_teste(admin)

    resposta = cliente.get(
        "/v1/itens-patrimoniais",
        params={"comunidade_virtual_id": str(comunidade.id)},
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
    )

    assert resposta.status_code == 200
    assert resposta.json()[0]["responsavel_id"] == str(responsavel.id)


def test_troca_do_responsavel_alcanca_os_exemplares_sem_escrita_neles(
    sessao,
    cliente,
    criar_chave,
    criar_persona,
    criar_sessao_de_teste,
    criar_comunidade,
    criar_ponto_de_apoio,
    criar_item_patrimonial,
):
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    comunidade = criar_comunidade()
    primeiro_responsavel = criar_persona(Papel.mestre, criada_por=admin)
    novo_responsavel = criar_persona(Papel.mestre, criada_por=admin)
    ponto_de_apoio = criar_ponto_de_apoio(admin, comunidade, responsavel=primeiro_responsavel)
    criar_item_patrimonial(admin, ponto_de_apoio)
    ponto_de_apoio.responsavel_id = novo_responsavel.id
    sessao.commit()
    token, _ = criar_sessao_de_teste(admin)

    resposta = cliente.get(
        "/v1/itens-patrimoniais",
        params={"comunidade_virtual_id": str(comunidade.id)},
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
    )

    assert resposta.status_code == 200
    assert resposta.json()[0]["responsavel_id"] == str(novo_responsavel.id)


def test_mestre_anota_a_ficha_de_vida_pela_rota(
    cliente,
    criar_chave,
    criar_persona,
    criar_sessao_de_teste,
    criar_comunidade,
    criar_ponto_de_apoio,
    criar_item_patrimonial,
):
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    comunidade = criar_comunidade()
    ponto_de_apoio = criar_ponto_de_apoio(admin, comunidade)
    item = criar_item_patrimonial(admin, ponto_de_apoio)
    mestre = criar_persona(Papel.mestre, criada_por=admin)
    token, _ = criar_sessao_de_teste(mestre)

    resposta = cliente.post(
        f"/v1/itens-patrimoniais/{item.id}/ficha-de-vida",
        json={"teor": "cuidado", "estado_de_conservacao": "bom"},
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
    )

    assert resposta.status_code == 201
    corpo = resposta.json()
    assert corpo["estado_de_conservacao"] == "bom"
    assert len(corpo["ficha_de_vida"]) == 1
    assert corpo["ficha_de_vida"][0]["teor"] == "cuidado"


def test_guerreiro_nao_anota_a_ficha_de_vida_pela_rota(
    cliente,
    criar_chave,
    criar_persona,
    criar_sessao_de_teste,
    criar_comunidade,
    criar_ponto_de_apoio,
    criar_item_patrimonial,
):
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    comunidade = criar_comunidade()
    ponto_de_apoio = criar_ponto_de_apoio(admin, comunidade)
    item = criar_item_patrimonial(admin, ponto_de_apoio)
    guerreiro = criar_persona(Papel.guerreiro, comunidade=comunidade)
    token, _ = criar_sessao_de_teste(guerreiro)

    resposta = cliente.post(
        f"/v1/itens-patrimoniais/{item.id}/ficha-de-vida",
        json={"teor": "cuidado", "estado_de_conservacao": "bom"},
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
    )

    assert resposta.status_code == 403
