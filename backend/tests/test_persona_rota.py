import uuid
from datetime import UTC, date, datetime

from nucleo.comunidades.modelo import VinculoJogador
from nucleo.personas.modelo import Papel, Persona


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


def test_listagem_de_guerreiros_traz_comunidade_e_data_do_vinculo_vigente(
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
            "nome": "Zeferina",
            "nascimento": "2015-03-20",
            "nick": "ZeferinaComVinculo",
            "avatar": "avatar-opaco",
            "aula_id": str(aula.id),
        },
        headers=cabecalhos,
    ).json()

    resposta = cliente.get("/v1/guerreiros", headers=cabecalhos)
    assert resposta.status_code == 200
    item = next(i for i in resposta.json()["itens"] if i["id"] == criado["id"])
    assert item["comunidade_virtual_id"] == str(comunidade.id)
    assert item["vinculo_iniciado_em"] is not None


def test_listagem_de_guerreiro_sem_vinculo_vigente_sai_com_campos_vazios(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste, sessao
):
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    token, _ = criar_sessao_de_teste(admin)

    # Persona gravada direto, sem o vínculo que a fixture `criar_persona`
    # abre automaticamente para o papel Guerreiro(a) — é o cenário de
    # ausência que a listagem precisa tolerar sem virar erro.
    guerreiro_sem_vinculo = Persona(
        papel=Papel.guerreiro,
        nome="Sem Vínculo",
        nascimento=date(2015, 3, 20),
        avatar="avatar-opaco",
    )
    sessao.add(guerreiro_sem_vinculo)
    sessao.commit()

    resposta = cliente.get(
        "/v1/guerreiros",
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
    )
    assert resposta.status_code == 200
    item = next(i for i in resposta.json()["itens"] if i["id"] == str(guerreiro_sem_vinculo.id))
    assert item["comunidade_virtual_id"] is None
    assert item["vinculo_iniciado_em"] is None


def test_listagem_de_guerreiros_nao_devolve_vinculo_encerrado(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste, criar_comunidade, sessao
):
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    comunidade_antiga = criar_comunidade("Comunidade Antiga")
    comunidade_nova = criar_comunidade("Comunidade Nova")

    # Persona gravada direto, com um vínculo já encerrado e outro vigente —
    # só o vigente pode sair na listagem (`RN-02-06`).
    guerreiro = Persona(
        papel=Papel.guerreiro,
        nome="Com Histórico",
        nascimento=date(2015, 3, 20),
        avatar="avatar-opaco",
    )
    sessao.add(guerreiro)
    sessao.flush()
    sessao.add(
        VinculoJogador(
            guerreiro_id=guerreiro.id,
            comunidade_virtual_id=comunidade_antiga.id,
            data_fim=datetime(2020, 1, 1, tzinfo=UTC),
        )
    )
    sessao.add(VinculoJogador(guerreiro_id=guerreiro.id, comunidade_virtual_id=comunidade_nova.id))
    sessao.commit()
    token, _ = criar_sessao_de_teste(admin)

    resposta = cliente.get(
        "/v1/guerreiros",
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
    )
    assert resposta.status_code == 200
    item = next(i for i in resposta.json()["itens"] if i["id"] == str(guerreiro.id))
    assert item["comunidade_virtual_id"] == str(comunidade_nova.id)


def test_mestre_recebe_403_ao_listar_guerreiros_pela_rota(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste
):
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    mestre = criar_persona(Papel.mestre, criada_por=admin)
    token, _ = criar_sessao_de_teste(mestre)

    resposta = cliente.get(
        "/v1/guerreiros",
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
    )
    assert resposta.status_code == 403


def test_guerreiro_do_onboarding_nasce_vinculado_a_comunidade_da_aula_sem_caminho_de_transferencia(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste, criar_comunidade, criar_aula
):
    """Critério de aceite do PRD-02 §12: o vínculo nasce da aula agendada, e
    não existe rota que o troque (`RF-08-03`, `RN-02-06`)."""
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    comunidade = criar_comunidade()
    aula = criar_aula(admin, comunidade)
    token, _ = criar_sessao_de_teste(admin)
    cabecalhos = {"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"}

    criado = cliente.post(
        "/v1/guerreiros",
        json={
            "nome": "Zeferina",
            "nascimento": "2015-03-20",
            "nick": "ZeferinaOnboarding",
            "avatar": "avatar-opaco",
            "aula_id": str(aula.id),
        },
        headers=cabecalhos,
    ).json()
    assert criado["comunidade_virtual_id"] == str(comunidade.id)

    outra_comunidade = criar_comunidade("Outra Comunidade")
    resposta = cliente.post(
        f"/v1/guerreiros/{criado['id']}/vinculo",
        json={"comunidade_id": str(outra_comunidade.id)},
        headers=cabecalhos,
    )
    assert resposta.status_code == 404
