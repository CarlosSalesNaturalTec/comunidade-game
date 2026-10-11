from nucleo.personas.modelo import Papel

# `RF-02-29`, PRD-02 §9: `POST /v1/atividades` cadastra a atividade avulsa.


def test_admin_cadastra_pela_rota(
    cliente,
    criar_chave,
    criar_persona,
    criar_sessao_de_teste,
    criar_poder,
    criar_comunidade,
    criar_aula,
):
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    token, _ = criar_sessao_de_teste(admin)
    poder = criar_poder(admin)
    aula = criar_aula(admin, criar_comunidade())

    resposta = cliente.post(
        "/v1/atividades",
        json={
            "titulo": "Mutirão de limpeza",
            "modalidade": "em_equipe",
            "formato": "presencial",
            "natureza": "meio ambiente",
            "producao_esperada": "Registro fotográfico do mutirão.",
            "poder_id": str(poder.id),
            "aula_id": str(aula.id),
        },
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
    )

    assert resposta.status_code == 201
    corpo = resposta.json()
    assert corpo["poder_id"] == str(poder.id)
    assert corpo["aula_id"] == str(aula.id)
    assert "missao_id" not in corpo


def test_mestre_recebe_403_pela_rota(
    cliente,
    criar_chave,
    criar_persona,
    criar_sessao_de_teste,
    criar_poder,
    criar_comunidade,
    criar_aula,
):
    chave, _ = criar_chave()
    mestre = criar_persona(Papel.mestre)
    token, _ = criar_sessao_de_teste(mestre)
    poder = criar_poder(mestre)
    aula = criar_aula(mestre, criar_comunidade())

    resposta = cliente.post(
        "/v1/atividades",
        json={
            "titulo": "Mutirão de limpeza",
            "modalidade": "em_equipe",
            "formato": "presencial",
            "natureza": "meio ambiente",
            "producao_esperada": "Registro fotográfico do mutirão.",
            "poder_id": str(poder.id),
            "aula_id": str(aula.id),
        },
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
    )

    assert resposta.status_code == 403


def test_campo_em_falta_responde_422(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste, criar_poder
):
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    token, _ = criar_sessao_de_teste(admin)
    poder = criar_poder(admin)

    resposta = cliente.post(
        "/v1/atividades",
        json={
            "titulo": "Mutirão de limpeza",
            "modalidade": "em_equipe",
            "formato": "presencial",
            "natureza": "meio ambiente",
            "poder_id": str(poder.id),
        },
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
    )

    assert resposta.status_code == 422


def test_listagem_devolve_o_cadastrado(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste, criar_atividade_avulsa
):
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    token, _ = criar_sessao_de_teste(admin)
    atividade = criar_atividade_avulsa(admin)

    resposta = cliente.get(
        "/v1/atividades",
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
    )

    assert resposta.status_code == 200
    ids = {item["id"] for item in resposta.json()}
    assert str(atividade.id) in ids


def test_campo_de_comunidade_e_recusado(
    cliente,
    criar_chave,
    criar_persona,
    criar_sessao_de_teste,
    criar_poder,
    criar_comunidade,
    criar_aula,
):
    """A comunidade é passo do formulário da App 03, não dado do cadastro:
    o `extra="forbid"` da entrada a recusa (`RF-02-29`, documento 09 §1)."""
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    token, _ = criar_sessao_de_teste(admin)
    poder = criar_poder(admin)
    comunidade = criar_comunidade()
    aula = criar_aula(admin, comunidade)

    resposta = cliente.post(
        "/v1/atividades",
        json={
            "titulo": "Mutirão de limpeza",
            "modalidade": "em_equipe",
            "formato": "presencial",
            "natureza": "meio ambiente",
            "producao_esperada": "Registro fotográfico do mutirão.",
            "poder_id": str(poder.id),
            "aula_id": str(aula.id),
            "comunidade_virtual_id": str(comunidade.id),
        },
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
    )

    assert resposta.status_code == 422


# `RF-02-112`: o filtro por aula na leitura da lista.


def test_listagem_filtra_pela_aula(
    cliente,
    criar_chave,
    criar_persona,
    criar_sessao_de_teste,
    criar_comunidade,
    criar_aula,
    criar_atividade_avulsa,
):
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    token, _ = criar_sessao_de_teste(admin)
    comunidade = criar_comunidade()
    aula = criar_aula(admin, comunidade)
    da_aula = criar_atividade_avulsa(admin, aula=aula, titulo="Da aula")
    de_outra = criar_atividade_avulsa(admin, aula=criar_aula(admin, comunidade), titulo="De outra")

    resposta = cliente.get(
        f"/v1/atividades?aula={aula.id}",
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
    )

    assert resposta.status_code == 200
    ids = {item["id"] for item in resposta.json()}
    assert ids == {str(da_aula.id)}
    assert str(de_outra.id) not in ids


def test_listagem_de_aula_sem_avulsa_responde_200_vazio(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste, criar_comunidade, criar_aula
):
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    token, _ = criar_sessao_de_teste(admin)
    aula = criar_aula(admin, criar_comunidade())

    resposta = cliente.get(
        f"/v1/atividades?aula={aula.id}",
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
    )

    assert resposta.status_code == 200
    assert resposta.json() == []


def test_mestre_nao_le_a_lista_filtrada(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste, criar_comunidade, criar_aula
):
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    mestre = criar_persona(Papel.mestre)
    token, _ = criar_sessao_de_teste(mestre)
    aula = criar_aula(admin, criar_comunidade())

    resposta = cliente.get(
        f"/v1/atividades?aula={aula.id}",
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
    )

    assert resposta.status_code == 403
