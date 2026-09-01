import uuid

from nucleo.personas.modelo import ArtefatoComprobatorio, Papel


def test_apoiador_declara_curriculo_e_termo_de_doacao(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste
):
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    apoiador = criar_persona(Papel.apoiador, criada_por=admin)
    token, _ = criar_sessao_de_teste(apoiador)
    cabecalhos = {"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"}

    curriculo = cliente.post(
        "/v1/eu/apoiador/documentos",
        json={"endereco": "https://exemplo.org/curriculo", "rotulo": "Currículo"},
        headers=cabecalhos,
    )
    termo = cliente.post(
        "/v1/eu/apoiador/documentos",
        json={"endereco": "https://exemplo.org/termo", "rotulo": "Termo de doação"},
        headers=cabecalhos,
    )

    assert curriculo.status_code == 201
    assert termo.status_code == 201
    assert curriculo.json()["publicado"] is False
    assert termo.json()["publicado"] is False

    leitura = cliente.get("/v1/eu/apoiador/documentos", headers=cabecalhos)
    assert leitura.status_code == 200
    assert len(leitura.json()) == 2


def test_documento_sem_endereco_ou_sem_rotulo_e_422(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste
):
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    apoiador = criar_persona(Papel.apoiador, criada_por=admin)
    token, _ = criar_sessao_de_teste(apoiador)
    cabecalhos = {"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"}

    sem_rotulo = cliente.post(
        "/v1/eu/apoiador/documentos",
        json={"endereco": "https://exemplo.org/x", "rotulo": ""},
        headers=cabecalhos,
    )
    assert sem_rotulo.status_code == 422
    assert sem_rotulo.json()["campo"] == "rotulo"


def test_outro_papel_recebe_403_ao_declarar_documento(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste
):
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    mestre = criar_persona(Papel.mestre, criada_por=admin)
    token, _ = criar_sessao_de_teste(mestre)
    cabecalhos = {"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"}

    resposta = cliente.post(
        "/v1/eu/apoiador/documentos",
        json={"endereco": "https://exemplo.org/x", "rotulo": "Rótulo"},
        headers=cabecalhos,
    )
    assert resposta.status_code == 403
    assert resposta.json()["codigo"] == "permissao_negada"


def test_admin_anexa_e_publica_o_documento(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste
):
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    apoiador = criar_persona(Papel.apoiador, criada_por=admin)
    token_do_apoiador, _ = criar_sessao_de_teste(apoiador)
    cabecalhos_do_apoiador = {
        "X-Chave-Aplicacao": chave,
        "Authorization": f"Bearer {token_do_apoiador}",
    }

    declarado = cliente.post(
        "/v1/eu/apoiador/documentos",
        json={"endereco": "https://exemplo.org/curriculo", "rotulo": "Currículo"},
        headers=cabecalhos_do_apoiador,
    ).json()

    token_do_admin, _ = criar_sessao_de_teste(admin)
    cabecalhos_do_admin = {
        "X-Chave-Aplicacao": chave,
        "Authorization": f"Bearer {token_do_admin}",
    }
    anexado = cliente.post(
        f"/v1/apoiadores/{apoiador.id}/artefatos/{declarado['id']}/anexacao",
        headers=cabecalhos_do_admin,
    )
    assert anexado.status_code == 200
    assert anexado.json()["publicado"] is True

    leitura = cliente.get("/v1/eu/apoiador/documentos", headers=cabecalhos_do_apoiador)
    item = next(d for d in leitura.json() if d["id"] == declarado["id"])
    assert item["publicado"] is True


def test_quem_nao_e_admin_nao_anexa_e_documento_segue_pendente(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste
):
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    apoiador = criar_persona(Papel.apoiador, criada_por=admin)
    token_do_apoiador, _ = criar_sessao_de_teste(apoiador)
    cabecalhos_do_apoiador = {
        "X-Chave-Aplicacao": chave,
        "Authorization": f"Bearer {token_do_apoiador}",
    }

    declarado = cliente.post(
        "/v1/eu/apoiador/documentos",
        json={"endereco": "https://exemplo.org/curriculo", "rotulo": "Currículo"},
        headers=cabecalhos_do_apoiador,
    ).json()

    resposta = cliente.post(
        f"/v1/apoiadores/{apoiador.id}/artefatos/{declarado['id']}/anexacao",
        headers=cabecalhos_do_apoiador,
    )
    assert resposta.status_code == 403

    leitura = cliente.get("/v1/eu/apoiador/documentos", headers=cabecalhos_do_apoiador)
    item = next(d for d in leitura.json() if d["id"] == declarado["id"])
    assert item["publicado"] is False


def test_anexacao_de_documento_de_outro_apoiador_e_404(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste
):
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    apoiador_1 = criar_persona(Papel.apoiador, criada_por=admin)
    apoiador_2 = criar_persona(Papel.apoiador, criada_por=admin)
    token_do_apoiador_1, _ = criar_sessao_de_teste(apoiador_1)
    cabecalhos_do_apoiador_1 = {
        "X-Chave-Aplicacao": chave,
        "Authorization": f"Bearer {token_do_apoiador_1}",
    }

    declarado = cliente.post(
        "/v1/eu/apoiador/documentos",
        json={"endereco": "https://exemplo.org/curriculo", "rotulo": "Currículo"},
        headers=cabecalhos_do_apoiador_1,
    ).json()

    token_do_admin, _ = criar_sessao_de_teste(admin)
    cabecalhos_do_admin = {
        "X-Chave-Aplicacao": chave,
        "Authorization": f"Bearer {token_do_admin}",
    }
    resposta = cliente.post(
        f"/v1/apoiadores/{apoiador_2.id}/artefatos/{declarado['id']}/anexacao",
        headers=cabecalhos_do_admin,
    )
    assert resposta.status_code == 404


def test_anexacao_de_documento_inexistente_e_404(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste
):
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    apoiador = criar_persona(Papel.apoiador, criada_por=admin)
    token_do_admin, _ = criar_sessao_de_teste(admin)
    cabecalhos_do_admin = {
        "X-Chave-Aplicacao": chave,
        "Authorization": f"Bearer {token_do_admin}",
    }

    resposta = cliente.post(
        f"/v1/apoiadores/{apoiador.id}/artefatos/{uuid.uuid4()}/anexacao",
        headers=cabecalhos_do_admin,
    )
    assert resposta.status_code == 404


def test_anexacao_repetida_nao_troca_a_autoria(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste, sessao
):
    chave, _ = criar_chave()
    admin_1 = criar_persona(Papel.admin)
    admin_2 = criar_persona(Papel.admin)
    apoiador = criar_persona(Papel.apoiador, criada_por=admin_1)
    token_do_apoiador, _ = criar_sessao_de_teste(apoiador)
    cabecalhos_do_apoiador = {
        "X-Chave-Aplicacao": chave,
        "Authorization": f"Bearer {token_do_apoiador}",
    }

    declarado = cliente.post(
        "/v1/eu/apoiador/documentos",
        json={"endereco": "https://exemplo.org/curriculo", "rotulo": "Currículo"},
        headers=cabecalhos_do_apoiador,
    ).json()

    token_do_admin_1, _ = criar_sessao_de_teste(admin_1)
    cliente.post(
        f"/v1/apoiadores/{apoiador.id}/artefatos/{declarado['id']}/anexacao",
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token_do_admin_1}"},
    )

    artefato_antes = sessao.get(ArtefatoComprobatorio, uuid.UUID(declarado["id"]))
    primeiro_anexador_id = artefato_antes.anexado_por_id
    primeiro_momento = artefato_antes.anexado_em

    token_do_admin_2, _ = criar_sessao_de_teste(admin_2)
    segunda = cliente.post(
        f"/v1/apoiadores/{apoiador.id}/artefatos/{declarado['id']}/anexacao",
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token_do_admin_2}"},
    )
    assert segunda.status_code == 200
    assert segunda.json()["publicado"] is True

    sessao.expire_all()
    artefato_depois = sessao.get(ArtefatoComprobatorio, uuid.UUID(declarado["id"]))
    assert artefato_depois.anexado_por_id == primeiro_anexador_id
    assert artefato_depois.anexado_em == primeiro_momento


def test_leitura_nao_alcanca_documento_alheio(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste
):
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    apoiador_1 = criar_persona(Papel.apoiador, criada_por=admin)
    apoiador_2 = criar_persona(Papel.apoiador, criada_por=admin)
    token_1, _ = criar_sessao_de_teste(apoiador_1)
    token_2, _ = criar_sessao_de_teste(apoiador_2)
    cabecalhos_1 = {"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token_1}"}
    cabecalhos_2 = {"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token_2}"}

    cliente.post(
        "/v1/eu/apoiador/documentos",
        json={"endereco": "https://exemplo.org/curriculo", "rotulo": "Currículo"},
        headers=cabecalhos_1,
    )

    leitura_de_1 = cliente.get("/v1/eu/apoiador/documentos", headers=cabecalhos_1)
    leitura_de_2 = cliente.get("/v1/eu/apoiador/documentos", headers=cabecalhos_2)
    assert len(leitura_de_1.json()) == 1
    assert len(leitura_de_2.json()) == 0
