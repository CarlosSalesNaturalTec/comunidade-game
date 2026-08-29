from nucleo.personas.modelo import Papel


def test_mestre_ve_os_guerreiros_ativos_da_sua_comunidade(
    cliente,
    criar_chave,
    criar_persona,
    criar_comunidade,
    criar_vinculo_jogador,
    criar_nick,
    criar_sessao_de_teste,
):
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    comunidade = criar_comunidade()
    mestre = criar_persona(Papel.mestre, criada_por=admin)
    criar_vinculo_jogador(mestre, comunidade)
    guerreiro = criar_persona(Papel.guerreiro, comunidade=comunidade, avatar="avatar-1")
    criar_nick(guerreiro, "guerreira-teste")
    token, _ = criar_sessao_de_teste(mestre)

    resposta = cliente.get(
        "/v1/guerreiros/vinculaveis",
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
    )
    assert resposta.status_code == 200
    corpo = resposta.json()
    assert len(corpo["itens"]) == 1
    item = corpo["itens"][0]
    assert item["id"] == str(guerreiro.id)
    assert item["nick"] == "guerreira-teste"
    assert item["avatar"] == "avatar-1"
    assert "nome" not in item
    assert "nascimento" not in item


def test_guerreiro_de_outra_comunidade_nao_aparece(
    cliente,
    criar_chave,
    criar_persona,
    criar_comunidade,
    criar_vinculo_jogador,
    criar_sessao_de_teste,
):
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    comunidade_do_mestre = criar_comunidade("Comunidade do Mestre")
    outra_comunidade = criar_comunidade("Outra Comunidade")
    mestre = criar_persona(Papel.mestre, criada_por=admin)
    criar_vinculo_jogador(mestre, comunidade_do_mestre)
    criar_persona(Papel.guerreiro, comunidade=outra_comunidade)
    token, _ = criar_sessao_de_teste(mestre)

    resposta = cliente.get(
        "/v1/guerreiros/vinculaveis",
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
    )
    assert resposta.status_code == 200
    assert resposta.json()["itens"] == []


def test_papel_sem_permissao_recebe_403_na_leitura_dos_vinculaveis(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste
):
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    apoiador = criar_persona(Papel.apoiador, criada_por=admin)
    token, _ = criar_sessao_de_teste(apoiador)

    resposta = cliente.get(
        "/v1/guerreiros/vinculaveis",
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
    )
    assert resposta.status_code == 403


def test_mestre_sem_vinculo_ve_lista_vazia(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste
):
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    mestre = criar_persona(Papel.mestre, criada_por=admin)
    token, _ = criar_sessao_de_teste(mestre)

    resposta = cliente.get(
        "/v1/guerreiros/vinculaveis",
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
    )
    assert resposta.status_code == 200
    assert resposta.json()["itens"] == []
