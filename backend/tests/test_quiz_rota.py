from nucleo.personas.modelo import Papel

ALTERNATIVAS = ["Salvador", "Recife", "Cachoeira", "Ilhéus"]


def test_openapi_lista_as_duas_rotas_do_banco(cliente):
    esquema = cliente.get("/openapi.json").json()
    assert "/v1/perguntas" in esquema["paths"]
    assert "post" in esquema["paths"]["/v1/perguntas"]
    assert "/v1/perguntas/minhas" in esquema["paths"]
    assert "get" in esquema["paths"]["/v1/perguntas/minhas"]


def test_cadastro_e_leitura_do_banco_pela_rota(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste, criar_trilha, criar_missao
):
    chave, _ = criar_chave()
    mestre = criar_persona(Papel.mestre)
    trilha = criar_trilha(mestre)
    missao = criar_missao(trilha, mestre)
    token, _ = criar_sessao_de_teste(mestre)
    cabecalhos = {"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"}

    resposta_cadastro = cliente.post(
        "/v1/perguntas",
        json={
            "enunciado": "Qual é a primeira capital do Brasil?",
            "alternativas": ALTERNATIVAS,
            "alternativa_correta": 3,
            "missao_id": str(missao.id),
        },
        headers=cabecalhos,
    )

    assert resposta_cadastro.status_code == 201
    corpo = resposta_cadastro.json()
    assert corpo["missao_id"] == str(missao.id)
    assert corpo["trilha_id"] == str(trilha.id)

    resposta_leitura = cliente.get("/v1/perguntas/minhas", headers=cabecalhos)

    assert resposta_leitura.status_code == 200
    pagina = resposta_leitura.json()
    assert [item["id"] for item in pagina["itens"]] == [corpo["id"]]


def test_guerreiro_recebe_403_ao_ler_o_banco(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste, criar_comunidade
):
    chave, _ = criar_chave()
    guerreiro = criar_persona(Papel.guerreiro, comunidade=criar_comunidade())
    token, _ = criar_sessao_de_teste(guerreiro)
    cabecalhos = {"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"}

    resposta = cliente.get("/v1/perguntas/minhas", headers=cabecalhos)

    assert resposta.status_code == 403
