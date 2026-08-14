from nucleo.locais.modelo import NivelDoLocal
from nucleo.personas.modelo import Papel


def test_admin_cadastra_local_pela_rota(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste, criar_comunidade
):
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    comunidade = criar_comunidade()
    token, _ = criar_sessao_de_teste(admin)

    resposta = cliente.post(
        "/v1/locais",
        json={
            "comunidade_id": str(comunidade.id),
            "nivel": NivelDoLocal.comunidade.value,
            "rotulo": "Território",
        },
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
    )

    assert resposta.status_code == 201
    corpo = resposta.json()
    assert corpo["rotulo"] == "Território"
    assert corpo["local_pai_id"] is None


def test_quem_nao_e_admin_recebe_403_ao_cadastrar_local(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste, criar_comunidade
):
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    mestre = criar_persona(Papel.mestre, criada_por=admin)
    comunidade = criar_comunidade()
    token, _ = criar_sessao_de_teste(mestre)

    resposta = cliente.post(
        "/v1/locais",
        json={
            "comunidade_id": str(comunidade.id),
            "nivel": NivelDoLocal.comunidade.value,
            "rotulo": "Território",
        },
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
    )

    assert resposta.status_code == 403


def test_listagem_de_locais_exige_filtro_de_comunidade(cliente, criar_chave):
    chave, _ = criar_chave()

    resposta = cliente.get("/v1/locais", headers={"X-Chave-Aplicacao": chave})

    assert resposta.status_code == 422


def test_listagem_de_locais_pela_rota(cliente, criar_chave, criar_comunidade, criar_local):
    chave, _ = criar_chave()
    comunidade = criar_comunidade()
    criar_local(comunidade, nivel=NivelDoLocal.comunidade, rotulo="Raiz")

    resposta = cliente.get(
        f"/v1/locais?comunidade={comunidade.id}",
        headers={"X-Chave-Aplicacao": chave},
    )

    assert resposta.status_code == 200
    corpo = resposta.json()
    assert len(corpo["itens"]) == 1
    assert corpo["itens"][0]["rotulo"] == "Raiz"
