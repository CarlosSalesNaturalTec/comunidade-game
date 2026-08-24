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
