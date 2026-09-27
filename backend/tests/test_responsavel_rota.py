import json
import uuid

from nucleo.personas.modelo import Credencial, Papel


def test_admin_cadastra_responsavel_pela_rota(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste
):
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    token, _ = criar_sessao_de_teste(admin)

    resposta = cliente.post(
        "/v1/responsaveis",
        json={"nome": "mãe"},
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
    )
    assert resposta.status_code == 201
    corpo = resposta.json()
    assert "id" in corpo
    assert corpo["nome"] == "mãe"


def test_mestre_cadastra_responsavel_pela_rota(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste
):
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    mestre = criar_persona(Papel.mestre, criada_por=admin)
    token, _ = criar_sessao_de_teste(mestre)

    resposta = cliente.post(
        "/v1/responsaveis",
        json={"nome": "mãe"},
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
    )
    assert resposta.status_code == 201


def test_quem_nao_e_admin_nem_mestre_recebe_403_ao_cadastrar_responsavel(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste
):
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    apoiador = criar_persona(Papel.apoiador, criada_por=admin)
    token, _ = criar_sessao_de_teste(apoiador)

    resposta = cliente.post(
        "/v1/responsaveis",
        json={"nome": "mãe"},
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
    )
    assert resposta.status_code == 403
    assert resposta.json()["codigo"] == "permissao_negada"


def test_cadastro_de_responsavel_sem_nome_pela_rota_e_422(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste
):
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    token, _ = criar_sessao_de_teste(admin)

    resposta = cliente.post(
        "/v1/responsaveis",
        json={"nome": ""},
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
    )
    assert resposta.status_code == 422
    assert resposta.json()["codigo"] == "erro_de_validacao"


def test_cadastro_de_responsavel_nao_cria_credencial(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste, sessao
):
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    token, _ = criar_sessao_de_teste(admin)

    resposta = cliente.post(
        "/v1/responsaveis",
        json={"nome": "mãe"},
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
    )
    responsavel_id = resposta.json()["id"]
    assert sessao.query(Credencial).filter_by(persona_id=responsavel_id).count() == 0


def test_criar_vinculo_pela_rota(cliente, criar_chave, criar_persona, criar_sessao_de_teste):
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    responsavel = criar_persona(Papel.responsavel, criada_por=admin)
    guerreiro = criar_persona(Papel.guerreiro)
    token, _ = criar_sessao_de_teste(admin)

    resposta = cliente.post(
        f"/v1/responsaveis/{responsavel.id}/vinculos",
        json={"guerreiro_id": str(guerreiro.id), "grau_de_parentesco": "mãe"},
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
    )
    assert resposta.status_code == 201
    corpo = resposta.json()
    assert corpo["responsavel_id"] == str(responsavel.id)
    assert corpo["guerreiro_id"] == str(guerreiro.id)
    assert corpo["grau_de_parentesco"] == "mãe"
    assert corpo["inicio"] is not None


def test_quem_nao_e_admin_nem_mestre_recebe_403_ao_criar_vinculo(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste
):
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    apoiador = criar_persona(Papel.apoiador, criada_por=admin)
    responsavel = criar_persona(Papel.responsavel, criada_por=admin)
    guerreiro = criar_persona(Papel.guerreiro)
    token, _ = criar_sessao_de_teste(apoiador)

    resposta = cliente.post(
        f"/v1/responsaveis/{responsavel.id}/vinculos",
        json={"guerreiro_id": str(guerreiro.id), "grau_de_parentesco": "mãe"},
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
    )
    assert resposta.status_code == 403
    assert resposta.json()["codigo"] == "permissao_negada"


def test_vinculo_sem_grau_de_parentesco_pela_rota_e_422(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste
):
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    responsavel = criar_persona(Papel.responsavel, criada_por=admin)
    guerreiro = criar_persona(Papel.guerreiro)
    token, _ = criar_sessao_de_teste(admin)

    resposta = cliente.post(
        f"/v1/responsaveis/{responsavel.id}/vinculos",
        json={"guerreiro_id": str(guerreiro.id), "grau_de_parentesco": ""},
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
    )
    assert resposta.status_code == 422
    corpo = resposta.json()
    assert corpo["codigo"] == "erro_de_validacao"
    assert corpo["campo"] == "grau_de_parentesco"


def test_vinculo_a_guerreiro_inexistente_pela_rota_e_404(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste
):
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    responsavel = criar_persona(Papel.responsavel, criada_por=admin)
    token, _ = criar_sessao_de_teste(admin)

    resposta = cliente.post(
        f"/v1/responsaveis/{responsavel.id}/vinculos",
        json={"guerreiro_id": str(uuid.uuid4()), "grau_de_parentesco": "mãe"},
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
    )
    assert resposta.status_code == 404


def test_vinculo_para_responsavel_inexistente_e_404(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste
):
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    guerreiro = criar_persona(Papel.guerreiro)
    token, _ = criar_sessao_de_teste(admin)

    resposta = cliente.post(
        f"/v1/responsaveis/{uuid.uuid4()}/vinculos",
        json={"guerreiro_id": str(guerreiro.id), "grau_de_parentesco": "mãe"},
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
    )
    assert resposta.status_code == 404


def test_quarto_vinculo_pela_rota_e_422(cliente, criar_chave, criar_persona, criar_sessao_de_teste):
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    responsavel = criar_persona(Papel.responsavel, criada_por=admin)
    guerreiro = criar_persona(Papel.guerreiro)
    token, _ = criar_sessao_de_teste(admin)
    cabecalhos = {"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"}

    for grau in ("mãe", "pai", "avó"):
        outro_responsavel = criar_persona(Papel.responsavel, criada_por=admin)
        resposta = cliente.post(
            f"/v1/responsaveis/{outro_responsavel.id}/vinculos",
            json={"guerreiro_id": str(guerreiro.id), "grau_de_parentesco": grau},
            headers=cabecalhos,
        )
        assert resposta.status_code == 201

    resposta = cliente.post(
        f"/v1/responsaveis/{responsavel.id}/vinculos",
        json={"guerreiro_id": str(guerreiro.id), "grau_de_parentesco": "tio"},
        headers=cabecalhos,
    )
    assert resposta.status_code == 422
    assert resposta.json()["codigo"] == "erro_de_validacao"


def test_cadastrar_responsavel_sem_chave_e_401(cliente):
    resposta = cliente.post("/v1/responsaveis")
    assert resposta.status_code == 401
    assert resposta.json()["codigo"] == "chave_invalida"


def test_criar_vinculo_sem_chave_e_401(cliente, criar_persona):
    responsavel = criar_persona(Papel.responsavel)
    resposta = cliente.post(
        f"/v1/responsaveis/{responsavel.id}/vinculos",
        json={"guerreiro_id": str(uuid.uuid4()), "grau_de_parentesco": "mãe"},
    )
    assert resposta.status_code == 401
    assert resposta.json()["codigo"] == "chave_invalida"


# `RF-02-111`, `RF-09-122`: a lista dos responsáveis cadastrados. Restrita a
# Admin e Mestre pela mesma operação de vínculo que os dois já têm.
def _listar(cliente, chave, token, parametros=""):
    return cliente.get(
        f"/v1/responsaveis{parametros}",
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
    )


def test_admin_lista_os_responsaveis_com_os_vinculados(
    cliente, criar_chave, criar_persona, criar_nick, criar_sessao_de_teste
):
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    token, _ = criar_sessao_de_teste(admin)
    cabecalhos = {"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"}

    guerreiro = criar_persona(Papel.guerreiro)
    criar_nick(guerreiro, "ZeferinaGuerreira")
    criado = cliente.post("/v1/responsaveis", json={"nome": "Dona Maria"}, headers=cabecalhos)
    responsavel_id = criado.json()["id"]
    cliente.post(
        f"/v1/responsaveis/{responsavel_id}/vinculos",
        json={"guerreiro_id": str(guerreiro.id), "grau_de_parentesco": "mãe"},
        headers=cabecalhos,
    )

    resposta = _listar(cliente, chave, token)

    assert resposta.status_code == 200
    itens = resposta.json()["itens"]
    assert len(itens) == 1
    assert itens[0]["nome"] == "Dona Maria"
    assert itens[0]["vinculados"] == [
        {
            "guerreiro_id": str(guerreiro.id),
            "nick": "ZeferinaGuerreira",
            "grau_de_parentesco": "mãe",
        }
    ]


def test_mestre_lista_os_responsaveis_da_sua_comunidade(
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
    guerreiro = criar_persona(Papel.guerreiro, comunidade=comunidade)
    criar_nick(guerreiro, "guerreira-teste")

    token_do_admin, _ = criar_sessao_de_teste(admin)
    cabecalhos_do_admin = {
        "X-Chave-Aplicacao": chave,
        "Authorization": f"Bearer {token_do_admin}",
    }
    criado = cliente.post("/v1/responsaveis", json={"nome": "Pai"}, headers=cabecalhos_do_admin)
    cliente.post(
        f"/v1/responsaveis/{criado.json()['id']}/vinculos",
        json={"guerreiro_id": str(guerreiro.id), "grau_de_parentesco": "pai"},
        headers=cabecalhos_do_admin,
    )

    token_do_mestre, _ = criar_sessao_de_teste(mestre)
    resposta = _listar(cliente, chave, token_do_mestre)

    assert resposta.status_code == 200
    itens = resposta.json()["itens"]
    assert [item["nome"] for item in itens] == ["Pai"]
    assert itens[0]["vinculados"][0]["nick"] == "guerreira-teste"


def test_a_resposta_nao_traz_credencial_nem_contato_nem_dado_civil_da_crianca(
    cliente, criar_chave, criar_persona, criar_nick, criar_sessao_de_teste
):
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    token, _ = criar_sessao_de_teste(admin)
    cabecalhos = {"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"}

    guerreiro = criar_persona(Papel.guerreiro)
    criar_nick(guerreiro, "ZeferinaGuerreira")
    criado = cliente.post("/v1/responsaveis", json={"nome": "Dona Maria"}, headers=cabecalhos)
    responsavel_id = criado.json()["id"]
    cliente.post(
        f"/v1/responsaveis/{responsavel_id}/vinculos",
        json={"guerreiro_id": str(guerreiro.id), "grau_de_parentesco": "mãe"},
        headers=cabecalhos,
    )
    cliente.post(
        "/v1/credenciais",
        json={"persona_id": responsavel_id, "usuario": "dona.maria"},
        headers=cabecalhos,
    )

    item = _listar(cliente, chave, token).json()["itens"][0]

    assert set(item) == {"id", "nome", "vinculados"}
    assert set(item["vinculados"][0]) == {"guerreiro_id", "nick", "grau_de_parentesco"}
    assert "dona.maria" not in json.dumps(item, ensure_ascii=False)


def test_responsavel_sem_vinculo_aparece_com_a_lista_vazia(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste
):
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    token, _ = criar_sessao_de_teste(admin)
    cabecalhos = {"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"}
    cliente.post("/v1/responsaveis", json={"nome": "Sozinho"}, headers=cabecalhos)

    itens = _listar(cliente, chave, token).json()["itens"]

    assert [item["nome"] for item in itens] == ["Sozinho"]
    assert itens[0]["vinculados"] == []


def test_a_listagem_devolve_cursor(cliente, criar_chave, criar_persona, criar_sessao_de_teste):
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    token, _ = criar_sessao_de_teste(admin)
    cabecalhos = {"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"}
    for indice in range(3):
        cliente.post("/v1/responsaveis", json={"nome": f"r{indice}"}, headers=cabecalhos)

    primeira = _listar(cliente, chave, token, "?tamanho=2").json()
    assert len(primeira["itens"]) == 2
    assert primeira["proximo_cursor"] is not None

    segunda = _listar(cliente, chave, token, f"?tamanho=2&cursor={primeira['proximo_cursor']}")
    assert segunda.status_code == 200
    assert len(segunda.json()["itens"]) == 1


def test_responsavel_apoiador_e_guerreiro_recebem_403_na_lista(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste
):
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    for papel in (Papel.responsavel, Papel.apoiador, Papel.guerreiro):
        persona = criar_persona(papel, criada_por=admin)
        token, _ = criar_sessao_de_teste(persona)
        assert _listar(cliente, chave, token).status_code == 403, papel
