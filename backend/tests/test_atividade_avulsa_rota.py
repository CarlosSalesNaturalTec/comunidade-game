from nucleo.personas.modelo import Papel

# `RF-02-29`, PRD-02 §9: `POST /v1/atividades` cadastra a atividade avulsa.


def test_admin_cadastra_pela_rota(
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
            "producao_esperada": "Registro fotográfico do mutirão.",
            "poder_id": str(poder.id),
        },
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
    )

    assert resposta.status_code == 201
    corpo = resposta.json()
    assert corpo["poder_id"] == str(poder.id)
    assert "missao_id" not in corpo


def test_mestre_recebe_403_pela_rota(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste, criar_poder
):
    chave, _ = criar_chave()
    mestre = criar_persona(Papel.mestre)
    token, _ = criar_sessao_de_teste(mestre)
    poder = criar_poder(mestre)

    resposta = cliente.post(
        "/v1/atividades",
        json={
            "titulo": "Mutirão de limpeza",
            "modalidade": "em_equipe",
            "formato": "presencial",
            "natureza": "meio ambiente",
            "producao_esperada": "Registro fotográfico do mutirão.",
            "poder_id": str(poder.id),
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
