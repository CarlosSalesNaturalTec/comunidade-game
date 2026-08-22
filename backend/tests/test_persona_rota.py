import uuid

from nucleo.personas.modelo import Papel


def test_admin_cadastra_guerreiro_pela_rota(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste, criar_comunidade, criar_aula
):
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    comunidade = criar_comunidade()
    aula = criar_aula(admin, comunidade)
    token, _ = criar_sessao_de_teste(admin)

    resposta = cliente.post(
        "/v1/guerreiros",
        json={
            "nome": "Zeferina",
            "nascimento": "2015-03-20",
            "nick": "ZeferinaGuerreira",
            "avatar": "avatar-opaco",
            "aula_id": str(aula.id),
        },
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
    )
    assert resposta.status_code == 201
    corpo = resposta.json()
    assert corpo["nome"] == "Zeferina"
    assert corpo["nick"] == "ZeferinaGuerreira"

    listagem = cliente.get(
        "/v1/guerreiros",
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
    )
    assert listagem.status_code == 200
    assert any(item["id"] == corpo["id"] for item in listagem.json()["itens"])


def test_mestre_recebe_403_ao_cadastrar_guerreiro_pela_rota(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste, criar_comunidade, criar_aula
):
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    mestre = criar_persona(Papel.mestre, criada_por=admin)
    comunidade = criar_comunidade()
    aula = criar_aula(admin, comunidade)
    token, _ = criar_sessao_de_teste(mestre)

    resposta = cliente.post(
        "/v1/guerreiros",
        json={
            "nome": "Zeferina",
            "nascimento": "2015-03-20",
            "nick": "ZeferinaGuerreira",
            "avatar": "avatar-opaco",
            "aula_id": str(aula.id),
        },
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
    )
    assert resposta.status_code == 403
    assert resposta.json()["codigo"] == "permissao_negada"


def test_editar_guerreiro_pela_rota(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste, criar_comunidade, criar_aula
):
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    comunidade = criar_comunidade()
    aula = criar_aula(admin, comunidade)
    token, _ = criar_sessao_de_teste(admin)
    cabecalhos = {"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"}

    criado = cliente.post(
        "/v1/guerreiros",
        json={
            "nome": "Nome Antigo",
            "nascimento": "2015-03-20",
            "nick": "NickFixo",
            "avatar": "avatar-1",
            "aula_id": str(aula.id),
        },
        headers=cabecalhos,
    ).json()

    resposta = cliente.patch(
        f"/v1/guerreiros/{criado['id']}",
        json={
            "nome": "Nome Novo",
            "nascimento": "2015-03-20",
            "nick": "NickFixo",
            "avatar": "avatar-1",
        },
        headers=cabecalhos,
    )
    assert resposta.status_code == 200
    assert resposta.json()["nome"] == "Nome Novo"


def test_editar_guerreiro_inexistente_e_404(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste
):
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    token, _ = criar_sessao_de_teste(admin)

    resposta = cliente.patch(
        f"/v1/guerreiros/{uuid.uuid4()}",
        json={"nome": "X", "nascimento": "2015-03-20", "nick": "Nick", "avatar": "a"},
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
    )
    assert resposta.status_code == 404


def test_admin_cadastra_mestre_pela_rota(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste
):
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    token, _ = criar_sessao_de_teste(admin)

    resposta = cliente.post(
        "/v1/mestres",
        json={
            "nome": "Mestre de Tal",
            "email": "mestre@example.org",
            "artefatos": [{"endereco": "https://exemplo.org/curriculo", "rotulo": "Currículo"}],
        },
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
    )
    assert resposta.status_code == 201
    corpo = resposta.json()
    assert corpo["nome"] == "Mestre de Tal"
    assert corpo["nick"] is None
    assert len(corpo["artefatos"]) == 1


def test_cadastro_de_mestre_sem_artefato_e_422_pela_rota(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste
):
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    token, _ = criar_sessao_de_teste(admin)

    resposta = cliente.post(
        "/v1/mestres",
        json={"nome": "Mestre de Tal", "email": "mestre@example.org", "artefatos": []},
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
    )
    assert resposta.status_code == 422
    assert resposta.json()["campo"] == "artefatos"


def test_admin_cadastra_apoiador_pela_rota(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste
):
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    token, _ = criar_sessao_de_teste(admin)

    resposta = cliente.post(
        "/v1/apoiadores",
        json={
            "nome": "Apoiador de Tal",
            "email": "apoiador@example.org",
            "nick": "ApoiadorNick",
            "artefatos": [{"endereco": "https://exemplo.org/doacao", "rotulo": "Termos"}],
        },
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
    )
    assert resposta.status_code == 201
    corpo = resposta.json()
    assert corpo["nick"] == "ApoiadorNick"

    listagem = cliente.get(
        "/v1/apoiadores",
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
    )
    assert listagem.status_code == 200
    assert any(item["id"] == corpo["id"] for item in listagem.json()["itens"])


def test_admin_inclui_outro_admin_pela_rota(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste
):
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    token, _ = criar_sessao_de_teste(admin)

    resposta = cliente.post(
        "/v1/admins",
        json={"nome": "Admin Nova", "email": "nova@example.org"},
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
    )
    assert resposta.status_code == 201
    assert resposta.json()["nome"] == "Admin Nova"


def test_apoiador_recebe_403_ao_incluir_admin_pela_rota(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste
):
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    apoiador = criar_persona(Papel.apoiador, criada_por=admin)
    token, _ = criar_sessao_de_teste(apoiador)

    resposta = cliente.post(
        "/v1/admins",
        json={"nome": "Outro Admin", "email": "outro@example.org"},
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
    )
    assert resposta.status_code == 403
    assert resposta.json()["codigo"] == "permissao_negada"


def test_admin_grava_nick_do_adulto_pela_rota(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste
):
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    apoiador = criar_persona(Papel.apoiador, criada_por=admin)
    token, _ = criar_sessao_de_teste(admin)

    resposta = cliente.patch(
        f"/v1/personas/{apoiador.id}/nick",
        json={"nick": "NickRecebidoPorFora"},
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
    )
    assert resposta.status_code == 200
    assert resposta.json()["nick"] == "NickRecebidoPorFora"


def test_admin_recebe_404_ao_gravar_nick_de_guerreiro_pela_rota(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste
):
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    guerreiro = criar_persona(Papel.guerreiro)
    token, _ = criar_sessao_de_teste(admin)

    resposta = cliente.patch(
        f"/v1/personas/{guerreiro.id}/nick",
        json={"nick": "NickQualquer"},
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
    )
    assert resposta.status_code == 404
