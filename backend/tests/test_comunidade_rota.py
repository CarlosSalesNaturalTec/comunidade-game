from nucleo.personas.modelo import Papel


def test_admin_cria_comunidade_pela_rota(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste
):
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    token, _ = criar_sessao_de_teste(admin)

    resposta = cliente.post(
        "/v1/comunidades",
        json={
            "nome": "Comunidade Nova",
            "localizacao": "Bairro Novo",
            "granularidade_maxima": "bairro",
        },
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
    )

    assert resposta.status_code == 201
    corpo = resposta.json()
    assert corpo["nome"] == "Comunidade Nova"
    assert corpo["admin_criador_id"] == str(admin.id)


def test_quem_nao_e_admin_recebe_403_ao_criar_comunidade(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste
):
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    mestre = criar_persona(Papel.mestre, criada_por=admin)
    token, _ = criar_sessao_de_teste(mestre)

    resposta = cliente.post(
        "/v1/comunidades",
        json={"nome": "X", "localizacao": "Y", "granularidade_maxima": "bairro"},
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
    )

    assert resposta.status_code == 403
    assert resposta.json()["codigo"] == "permissao_negada"


def test_comunidade_sem_localizacao_devolve_422(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste
):
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    token, _ = criar_sessao_de_teste(admin)

    resposta = cliente.post(
        "/v1/comunidades",
        json={"nome": "X", "granularidade_maxima": "bairro"},
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
    )

    assert resposta.status_code == 422


def test_nenhuma_rota_transfere_guerreiro_entre_comunidades(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste, criar_comunidade
):
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    guerreiro = criar_persona(Papel.guerreiro)
    outra_comunidade = criar_comunidade("Outra Comunidade")
    token, _ = criar_sessao_de_teste(admin)

    resposta = cliente.post(
        f"/v1/guerreiros/{guerreiro.id}/comunidade",
        json={"comunidade_id": str(outra_comunidade.id)},
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
    )

    assert resposta.status_code == 404
