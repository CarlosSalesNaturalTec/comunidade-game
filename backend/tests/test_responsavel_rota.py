import json
import uuid

from nucleo.personas.modelo import Credencial, Papel, Persona, TipoDeCredencial
from nucleo.sessoes.social import obter_verificador_social


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
    cliente, sessao, criar_chave, criar_persona, criar_nick, criar_sessao_de_teste
):
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    token, _ = criar_sessao_de_teste(admin)
    cabecalhos = {"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"}

    guerreiro = criar_persona(Papel.guerreiro)
    guerreiro.nome = "Zeferina da Silva"
    sessao.commit()
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
            "nome": "Zeferina da Silva",
            "grau_de_parentesco": "mãe",
        }
    ]


def test_mestre_lista_os_responsaveis_da_sua_comunidade(
    cliente,
    sessao,
    criar_chave,
    criar_persona,
    criar_comunidade,
    criar_vinculo_do_mestre,
    criar_nick,
    criar_sessao_de_teste,
):
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    comunidade = criar_comunidade()
    mestre = criar_persona(Papel.mestre, criada_por=admin)
    criar_vinculo_do_mestre(mestre, comunidade)
    guerreiro = criar_persona(Papel.guerreiro, comunidade=comunidade)
    guerreiro.nome = "Ana Teste"
    sessao.commit()
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
    vinculado = itens[0]["vinculados"][0]
    assert (vinculado["nick"], vinculado["nome"], vinculado["grau_de_parentesco"]) == (
        "guerreira-teste",
        "Ana Teste",
        "pai",
    )


def test_a_resposta_nao_traz_credencial_nem_contato_nem_imagem_ou_nascimento_da_crianca(
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

    # E-mail e usuário de acesso saem desde 2026-11-27 (`RF-01-92`); senha,
    # hash e troca pendente nunca.
    assert set(item) == {"id", "nome", "email", "usuario", "vinculados"}
    assert item["usuario"] == "dona.maria"
    assert item["email"] == ""
    texto = json.dumps(item, ensure_ascii=False)
    assert "senha" not in texto and "troca" not in texto
    # O nome do vinculado sai desde 2026-11-26; imagem, nascimento e contato
    # nunca (`RN-09-18`).
    assert set(item["vinculados"][0]) == {"guerreiro_id", "nick", "nome", "grau_de_parentesco"}


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


def test_guerreiro_sem_nome_gravado_continua_na_lista_com_o_nome_vazio(
    cliente, criar_chave, criar_persona, criar_nick, criar_sessao_de_teste
):
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    token, _ = criar_sessao_de_teste(admin)
    cabecalhos = {"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"}
    guerreiro = criar_persona(Papel.guerreiro)
    criar_nick(guerreiro, "SemNome")
    criado = cliente.post("/v1/responsaveis", json={"nome": "Tia"}, headers=cabecalhos)
    cliente.post(
        f"/v1/responsaveis/{criado.json()['id']}/vinculos",
        json={"guerreiro_id": str(guerreiro.id), "grau_de_parentesco": "tia"},
        headers=cabecalhos,
    )

    vinculado = _listar(cliente, chave, token).json()["itens"][0]["vinculados"][0]

    assert (vinculado["nick"], vinculado["nome"]) == ("SemNome", "")


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


# --- E-mail, acesso e ficha do responsável (`RF-01-92`, `RF-02-121`) ---


def _verificador(app, email: str) -> None:
    app.dependency_overrides[obter_verificador_social] = lambda: lambda _token: email


def _login_social(cliente, chave) -> int:
    return cliente.post(
        "/v1/sessoes/social", json={"id_token": "x"}, headers={"X-Chave-Aplicacao": chave}
    ).status_code


def _admin(criar_chave, criar_persona, criar_sessao_de_teste):
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    token, _ = criar_sessao_de_teste(admin)
    return chave, token, {"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"}


def _credenciais_sociais(sessao, persona_id):
    sessao.expire_all()
    return (
        sessao.query(Credencial)
        .filter_by(persona_id=uuid.UUID(persona_id), tipo=TipoDeCredencial.login_social)
        .all()
    )


def test_cadastro_com_email_abre_o_login_social(
    app, cliente, sessao, criar_chave, criar_persona, criar_sessao_de_teste
):
    chave, _, cabecalhos = _admin(criar_chave, criar_persona, criar_sessao_de_teste)

    criado = cliente.post(
        "/v1/responsaveis",
        json={"nome": "Dona Maria", "email": "maria@example.org"},
        headers=cabecalhos,
    )

    assert criado.status_code == 201
    persona = sessao.get(Persona, uuid.UUID(criado.json()["id"]))
    assert persona.email == "maria@example.org"
    [credencial] = _credenciais_sociais(sessao, criado.json()["id"])
    assert credencial.identificador == "maria@example.org" and credencial.ativa
    _verificador(app, "maria@example.org")
    assert _login_social(cliente, chave) == 201


def test_mestre_cadastra_responsavel_com_email(
    cliente, sessao, criar_chave, criar_persona, criar_sessao_de_teste
):
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    mestre = criar_persona(Papel.mestre, criada_por=admin)
    token, _ = criar_sessao_de_teste(mestre)

    criado = cliente.post(
        "/v1/responsaveis",
        json={"nome": "Pai", "email": "pai@example.org"},
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
    )

    assert criado.status_code == 201
    assert len(_credenciais_sociais(sessao, criado.json()["id"])) == 1


def test_email_vazio_no_cadastro_nao_cria_credencial(
    cliente, sessao, criar_chave, criar_persona, criar_sessao_de_teste
):
    _, _, cabecalhos = _admin(criar_chave, criar_persona, criar_sessao_de_teste)

    criado = cliente.post(
        "/v1/responsaveis", json={"nome": "Mãe", "email": "  "}, headers=cabecalhos
    )

    assert criado.status_code == 201
    assert _credenciais_sociais(sessao, criado.json()["id"]) == []


def test_email_de_outra_pessoa_e_recusado_no_cadastro(
    cliente, sessao, criar_chave, criar_persona, criar_sessao_de_teste
):
    _, _, cabecalhos = _admin(criar_chave, criar_persona, criar_sessao_de_teste)
    cliente.post(
        "/v1/responsaveis", json={"nome": "Mãe", "email": "a@example.org"}, headers=cabecalhos
    )
    antes = sessao.query(Persona).filter_by(papel=Papel.responsavel).count()

    recusado = cliente.post(
        "/v1/responsaveis", json={"nome": "Tia", "email": "a@example.org"}, headers=cabecalhos
    )

    assert recusado.status_code == 422
    assert recusado.json()["campo"] == "email"
    sessao.expire_all()
    assert sessao.query(Persona).filter_by(papel=Papel.responsavel).count() == antes


def _alterar(cliente, cabecalhos, responsavel_id, corpo):
    return cliente.patch(f"/v1/responsaveis/{responsavel_id}", json=corpo, headers=cabecalhos)


def test_admin_corrige_o_nome_e_os_vinculos_seguem(
    cliente, criar_chave, criar_persona, criar_nick, criar_sessao_de_teste
):
    _, _, cabecalhos = _admin(criar_chave, criar_persona, criar_sessao_de_teste)
    guerreiro = criar_persona(Papel.guerreiro)
    criar_nick(guerreiro, "Zefa")
    rid = cliente.post("/v1/responsaveis", json={"nome": "Mria"}, headers=cabecalhos).json()["id"]
    cliente.post(
        f"/v1/responsaveis/{rid}/vinculos",
        json={"guerreiro_id": str(guerreiro.id), "grau_de_parentesco": "mãe"},
        headers=cabecalhos,
    )

    resposta = _alterar(cliente, cabecalhos, rid, {"nome": "Maria"})

    assert resposta.status_code == 200
    assert resposta.json()["nome"] == "Maria"
    assert [v["nick"] for v in resposta.json()["vinculados"]] == ["Zefa"]


def test_nome_em_branco_na_edicao_e_422(cliente, criar_chave, criar_persona, criar_sessao_de_teste):
    _, _, cabecalhos = _admin(criar_chave, criar_persona, criar_sessao_de_teste)
    rid = cliente.post("/v1/responsaveis", json={"nome": "Mãe"}, headers=cabecalhos).json()["id"]

    resposta = _alterar(cliente, cabecalhos, rid, {"nome": " "})

    assert resposta.status_code == 422
    assert resposta.json()["campo"] == "nome"


def test_admin_grava_troca_e_retira_o_email(
    app, cliente, sessao, criar_chave, criar_persona, criar_sessao_de_teste
):
    chave, _, cabecalhos = _admin(criar_chave, criar_persona, criar_sessao_de_teste)
    rid = cliente.post("/v1/responsaveis", json={"nome": "Mãe"}, headers=cabecalhos).json()["id"]
    cliente.post(
        "/v1/credenciais", json={"persona_id": rid, "usuario": "mae.da.zefa"}, headers=cabecalhos
    )

    gravado = _alterar(cliente, cabecalhos, rid, {"email": "mae@example.org"})
    assert gravado.status_code == 200
    assert (gravado.json()["email"], gravado.json()["usuario"]) == (
        "mae@example.org",
        "mae.da.zefa",
    )
    _verificador(app, "mae@example.org")
    assert _login_social(cliente, chave) == 201

    trocado = _alterar(cliente, cabecalhos, rid, {"email": "nova@example.org"})
    assert trocado.json()["email"] == "nova@example.org"
    assert _login_social(cliente, chave) == 403
    _verificador(app, "nova@example.org")
    assert _login_social(cliente, chave) == 201

    retirado = _alterar(cliente, cabecalhos, rid, {"email": None})
    assert retirado.status_code == 200
    assert (retirado.json()["email"], retirado.json()["usuario"]) == ("", "mae.da.zefa")
    assert _login_social(cliente, chave) == 403
    [credencial] = _credenciais_sociais(sessao, rid)
    assert credencial.ativa is False
    usuario_e_senha = (
        sessao.query(Credencial)
        .filter_by(persona_id=uuid.UUID(rid), tipo=TipoDeCredencial.usuario_e_senha)
        .one()
    )
    assert usuario_e_senha.ativa is True

    regravado = _alterar(cliente, cabecalhos, rid, {"email": "nova@example.org"})
    assert regravado.json()["email"] == "nova@example.org"
    assert _login_social(cliente, chave) == 201


def test_email_de_outra_pessoa_e_recusado_na_edicao(
    cliente, sessao, criar_chave, criar_persona, criar_sessao_de_teste
):
    _, _, cabecalhos = _admin(criar_chave, criar_persona, criar_sessao_de_teste)
    cliente.post(
        "/v1/responsaveis", json={"nome": "Mãe", "email": "a@example.org"}, headers=cabecalhos
    )
    rid = cliente.post(
        "/v1/responsaveis", json={"nome": "Tia", "email": "b@example.org"}, headers=cabecalhos
    ).json()["id"]

    resposta = _alterar(cliente, cabecalhos, rid, {"email": "a@example.org"})

    assert resposta.status_code == 422
    assert resposta.json()["campo"] == "email"
    sessao.expire_all()
    assert sessao.get(Persona, uuid.UUID(rid)).email == "b@example.org"


def test_mestre_e_os_demais_papeis_nao_alteram_a_ficha(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste
):
    chave, _, cabecalhos = _admin(criar_chave, criar_persona, criar_sessao_de_teste)
    admin = criar_persona(Papel.admin)
    rid = cliente.post("/v1/responsaveis", json={"nome": "Mãe"}, headers=cabecalhos).json()["id"]

    for papel in (Papel.mestre, Papel.apoiador, Papel.responsavel):
        persona = criar_persona(papel, criada_por=admin)
        token, _ = criar_sessao_de_teste(persona)
        resposta = _alterar(
            cliente,
            {"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
            rid,
            {"nome": "Outro"},
        )
        assert resposta.status_code == 403, papel


def test_alterar_persona_que_nao_e_responsavel_e_404(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste
):
    _, _, cabecalhos = _admin(criar_chave, criar_persona, criar_sessao_de_teste)
    mestre = criar_persona(Papel.mestre)

    assert _alterar(cliente, cabecalhos, mestre.id, {"nome": "X"}).status_code == 404
    assert _alterar(cliente, cabecalhos, uuid.uuid4(), {"nome": "X"}).status_code == 404


def test_responsavel_sem_credencial_vem_com_o_acesso_vazio(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste
):
    chave, token, cabecalhos = _admin(criar_chave, criar_persona, criar_sessao_de_teste)
    cliente.post("/v1/responsaveis", json={"nome": "Mãe"}, headers=cabecalhos)

    item = _listar(cliente, chave, token).json()["itens"][0]

    assert (item["email"], item["usuario"]) == ("", "")
