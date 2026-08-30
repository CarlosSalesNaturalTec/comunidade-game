"""A porta HTTP da equipe da trilha — `RF-04-61`, `RF-04-62`, `RN-01-44`,
do PRD-04 §9."""

from nucleo.personas.modelo import Papel


def _cabecalhos(chave, token):
    return {"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"}


def test_guerreiro_cria_a_equipe_da_trilha_e_entra_como_primeiro_integrante(
    cliente,
    criar_chave,
    criar_persona,
    criar_comunidade,
    criar_trilha,
    criar_sessao_de_teste,
    criar_nick,
):
    chave, _ = criar_chave()
    mestre = criar_persona(Papel.mestre)
    comunidade = criar_comunidade()
    trilha = criar_trilha(mestre)
    guerreiro = criar_persona(Papel.guerreiro, comunidade=comunidade, avatar="avatar-1")
    criar_nick(guerreiro, "zeferina")
    token, _ = criar_sessao_de_teste(guerreiro)

    resposta = cliente.post(
        f"/v1/trilhas/{trilha.id}/equipes", json={}, headers=_cabecalhos(chave, token)
    )

    assert resposta.status_code == 201
    corpo = resposta.json()
    assert corpo["aula_id"] is None
    assert corpo["integrantes"] == [{"avatar": "avatar-1", "nick": "zeferina", "papel": None}]


def test_teto_de_integrantes_vale_na_equipe_da_trilha(
    cliente,
    criar_chave,
    criar_persona,
    criar_comunidade,
    criar_trilha,
    criar_equipe,
    adicionar_integrante,
    criar_sessao_de_teste,
    criar_nick,
):
    chave, _ = criar_chave()
    mestre = criar_persona(Papel.mestre)
    comunidade = criar_comunidade()
    trilha = criar_trilha(mestre)
    criador = criar_persona(Papel.guerreiro, comunidade=comunidade)
    criar_nick(criador, "criadora")
    equipe = criar_equipe(criador, trilha=trilha)
    for indice in range(4):
        outro = criar_persona(Papel.guerreiro, comunidade=comunidade)
        criar_nick(outro, f"integrante{indice}")
        adicionar_integrante(equipe, outro)

    sexto = criar_persona(Papel.guerreiro, comunidade=comunidade)
    criar_nick(sexto, "sexta")
    token, _ = criar_sessao_de_teste(sexto)

    resposta = cliente.post(
        f"/v1/equipes/{equipe.id}/integrantes", json={}, headers=_cabecalhos(chave, token)
    )

    assert resposta.status_code == 422


def test_segunda_equipe_da_mesma_trilha_e_recusada_pela_porta(
    cliente,
    criar_chave,
    criar_persona,
    criar_comunidade,
    criar_trilha,
    criar_equipe,
    criar_sessao_de_teste,
    criar_nick,
):
    chave, _ = criar_chave()
    mestre = criar_persona(Papel.mestre)
    comunidade = criar_comunidade()
    trilha = criar_trilha(mestre)
    guerreiro = criar_persona(Papel.guerreiro, comunidade=comunidade)
    criar_nick(guerreiro, "zeferina")
    criar_equipe(guerreiro, trilha=trilha)
    token, _ = criar_sessao_de_teste(guerreiro)

    resposta = cliente.post(
        f"/v1/trilhas/{trilha.id}/equipes", json={}, headers=_cabecalhos(chave, token)
    )

    assert resposta.status_code == 422


def test_admin_e_mestre_nao_criam_equipe_da_trilha_pela_porta(
    cliente, criar_chave, criar_persona, criar_trilha, criar_sessao_de_teste
):
    chave, _ = criar_chave()
    mestre = criar_persona(Papel.mestre)
    trilha = criar_trilha(mestre)

    for operador in (mestre, criar_persona(Papel.admin)):
        token, _ = criar_sessao_de_teste(operador)
        resposta = cliente.post(
            f"/v1/trilhas/{trilha.id}/equipes", json={}, headers=_cabecalhos(chave, token)
        )
        assert resposta.status_code == 403


def test_trilha_inexistente_nao_forma_equipe(
    cliente, criar_chave, criar_persona, criar_comunidade, criar_sessao_de_teste, criar_nick
):
    import uuid

    chave, _ = criar_chave()
    comunidade = criar_comunidade()
    guerreiro = criar_persona(Papel.guerreiro, comunidade=comunidade)
    criar_nick(guerreiro, "zeferina")
    token, _ = criar_sessao_de_teste(guerreiro)

    resposta = cliente.post(
        f"/v1/trilhas/{uuid.uuid4()}/equipes", json={}, headers=_cabecalhos(chave, token)
    )

    assert resposta.status_code == 404


def test_mestre_homologa_pela_porta(
    cliente,
    criar_chave,
    criar_persona,
    criar_comunidade,
    criar_trilha,
    criar_equipe,
    criar_sessao_de_teste,
):
    chave, _ = criar_chave()
    mestre = criar_persona(Papel.mestre)
    comunidade = criar_comunidade()
    trilha = criar_trilha(mestre)
    guerreiro = criar_persona(Papel.guerreiro, comunidade=comunidade)
    equipe = criar_equipe(guerreiro, trilha=trilha)
    token, _ = criar_sessao_de_teste(mestre)

    resposta = cliente.post(
        f"/v1/equipes/{equipe.id}/homologacao", headers=_cabecalhos(chave, token)
    )

    assert resposta.status_code == 200
    corpo = resposta.json()
    assert corpo["equipe_id"] == str(equipe.id)
    assert corpo["homologado_por_id"] == str(mestre.id)
    assert corpo["homologado_em"] is not None


def test_composicao_fixa_depois_da_homologacao_pela_porta(
    cliente,
    criar_chave,
    criar_persona,
    criar_comunidade,
    criar_trilha,
    criar_equipe,
    criar_sessao_de_teste,
    criar_nick,
):
    chave, _ = criar_chave()
    mestre = criar_persona(Papel.mestre)
    comunidade = criar_comunidade()
    trilha = criar_trilha(mestre)
    guerreiro = criar_persona(Papel.guerreiro, comunidade=comunidade)
    equipe = criar_equipe(guerreiro, trilha=trilha, homologada=True, homologado_por=mestre)

    outro = criar_persona(Papel.guerreiro, comunidade=comunidade)
    criar_nick(outro, "outra")
    token, _ = criar_sessao_de_teste(outro)

    resposta = cliente.post(
        f"/v1/equipes/{equipe.id}/integrantes", json={}, headers=_cabecalhos(chave, token)
    )

    assert resposta.status_code == 422


def test_guerreiro_nao_homologa_pela_porta(
    cliente,
    criar_chave,
    criar_persona,
    criar_comunidade,
    criar_trilha,
    criar_equipe,
    criar_sessao_de_teste,
):
    chave, _ = criar_chave()
    mestre = criar_persona(Papel.mestre)
    comunidade = criar_comunidade()
    trilha = criar_trilha(mestre)
    guerreiro = criar_persona(Papel.guerreiro, comunidade=comunidade)
    equipe = criar_equipe(guerreiro, trilha=trilha)
    token, _ = criar_sessao_de_teste(guerreiro)

    resposta = cliente.post(
        f"/v1/equipes/{equipe.id}/homologacao", headers=_cabecalhos(chave, token)
    )

    assert resposta.status_code == 403


def test_equipe_da_aula_nao_se_homologa_pela_porta(
    cliente,
    criar_chave,
    criar_persona,
    criar_comunidade,
    criar_aula,
    criar_equipe,
    criar_sessao_de_teste,
):
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    mestre = criar_persona(Papel.mestre)
    comunidade = criar_comunidade()
    aula = criar_aula(admin, comunidade)
    guerreiro = criar_persona(Papel.guerreiro, comunidade=comunidade)
    equipe = criar_equipe(guerreiro, aula=aula)
    token, _ = criar_sessao_de_teste(mestre)

    resposta = cliente.post(
        f"/v1/equipes/{equipe.id}/homologacao", headers=_cabecalhos(chave, token)
    )

    assert resposta.status_code == 422
