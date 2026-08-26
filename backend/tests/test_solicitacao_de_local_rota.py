from nucleo.locais.modelo import NivelDoLocal
from nucleo.personas.modelo import Papel


def _headers(chave, token):
    return {"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"}


def test_guerreiro_solicita_local_pela_rota(
    cliente,
    criar_chave,
    criar_persona,
    criar_comunidade,
    criar_sessao_de_teste,
    criar_trilha,
    criar_missao,
    criar_desafio_de_coleta,
):
    chave, _ = criar_chave()
    comunidade = criar_comunidade()
    guerreiro = criar_persona(Papel.guerreiro, comunidade=comunidade)
    mestre = criar_persona(Papel.mestre)
    trilha = criar_trilha(mestre)
    missao = criar_missao(trilha, mestre)
    desafio = criar_desafio_de_coleta(missao, mestre)
    token, _ = criar_sessao_de_teste(guerreiro)

    resposta = cliente.post(
        "/v1/solicitacoes-de-local",
        json={
            "comunidade_id": str(comunidade.id),
            "desafio_de_coleta_id": str(desafio.id),
            "nivel": NivelDoLocal.bairro.value,
            "rotulo": "Bairro Novo",
            "justificativa": "Falta um local para registrar a coleta.",
        },
        headers=_headers(chave, token),
    )

    assert resposta.status_code == 201
    corpo = resposta.json()
    assert corpo["situacao"] == "recebida"
    assert corpo["solicitante_id"] == str(guerreiro.id)
    assert corpo["local_criado_id"] is None


def test_mestre_recebe_403_ao_solicitar_local_pela_rota(
    cliente,
    criar_chave,
    criar_persona,
    criar_comunidade,
    criar_sessao_de_teste,
    criar_trilha,
    criar_missao,
    criar_desafio_de_coleta,
):
    chave, _ = criar_chave()
    comunidade = criar_comunidade()
    mestre = criar_persona(Papel.mestre)
    trilha = criar_trilha(mestre)
    missao = criar_missao(trilha, mestre)
    desafio = criar_desafio_de_coleta(missao, mestre)
    token, _ = criar_sessao_de_teste(mestre)

    resposta = cliente.post(
        "/v1/solicitacoes-de-local",
        json={
            "comunidade_id": str(comunidade.id),
            "desafio_de_coleta_id": str(desafio.id),
            "nivel": NivelDoLocal.bairro.value,
            "rotulo": "Bairro Novo",
            "justificativa": "Falta um local para registrar a coleta.",
        },
        headers=_headers(chave, token),
    )

    assert resposta.status_code == 403


def _preparar_solicitacao_pela_rota(
    cliente,
    criar_chave,
    criar_persona,
    criar_comunidade,
    criar_sessao_de_teste,
    criar_trilha,
    criar_missao,
    criar_desafio_de_coleta,
    criar_local,
):
    chave, _ = criar_chave()
    comunidade = criar_comunidade()
    raiz = criar_local(comunidade, nivel=NivelDoLocal.comunidade, rotulo="Raiz")
    guerreiro = criar_persona(Papel.guerreiro, comunidade=comunidade)
    mestre = criar_persona(Papel.mestre)
    trilha = criar_trilha(mestre)
    missao = criar_missao(trilha, mestre)
    desafio = criar_desafio_de_coleta(missao, mestre, granularidade_exigida=NivelDoLocal.bairro)
    token_guerreiro, _ = criar_sessao_de_teste(guerreiro)

    resposta = cliente.post(
        "/v1/solicitacoes-de-local",
        json={
            "comunidade_id": str(comunidade.id),
            "desafio_de_coleta_id": str(desafio.id),
            "nivel": NivelDoLocal.bairro.value,
            "rotulo": "Bairro Novo",
            "justificativa": "Falta um local para registrar a coleta.",
        },
        headers=_headers(chave, token_guerreiro),
    )
    solicitacao_id = resposta.json()["id"]
    return chave, comunidade, raiz, guerreiro, mestre, desafio, solicitacao_id


def test_mestre_autor_aprova_solicitacao_pela_rota(
    cliente,
    criar_chave,
    criar_persona,
    criar_comunidade,
    criar_sessao_de_teste,
    criar_trilha,
    criar_missao,
    criar_desafio_de_coleta,
    criar_local,
):
    chave, _, raiz, _, mestre, _, solicitacao_id = _preparar_solicitacao_pela_rota(
        cliente,
        criar_chave,
        criar_persona,
        criar_comunidade,
        criar_sessao_de_teste,
        criar_trilha,
        criar_missao,
        criar_desafio_de_coleta,
        criar_local,
    )
    token_mestre, _ = criar_sessao_de_teste(mestre)

    resposta = cliente.post(
        f"/v1/solicitacoes-de-local/{solicitacao_id}/avaliacao",
        json={"situacao": "aprovada", "local_pai_id": str(raiz.id)},
        headers=_headers(chave, token_mestre),
    )

    assert resposta.status_code == 200
    corpo = resposta.json()
    assert corpo["situacao"] == "aprovada"
    assert corpo["local_criado_id"] is not None


def test_guerreiro_recebe_403_ao_avaliar_pela_rota(
    cliente,
    criar_chave,
    criar_persona,
    criar_comunidade,
    criar_sessao_de_teste,
    criar_trilha,
    criar_missao,
    criar_desafio_de_coleta,
    criar_local,
):
    chave, _, raiz, guerreiro, _, _, solicitacao_id = _preparar_solicitacao_pela_rota(
        cliente,
        criar_chave,
        criar_persona,
        criar_comunidade,
        criar_sessao_de_teste,
        criar_trilha,
        criar_missao,
        criar_desafio_de_coleta,
        criar_local,
    )
    token_guerreiro, _ = criar_sessao_de_teste(guerreiro)

    resposta = cliente.post(
        f"/v1/solicitacoes-de-local/{solicitacao_id}/avaliacao",
        json={"situacao": "aprovada", "local_pai_id": str(raiz.id)},
        headers=_headers(chave, token_guerreiro),
    )

    assert resposta.status_code == 403


def test_listagem_de_abertas_exige_filtro_de_comunidade(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste
):
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    token, _ = criar_sessao_de_teste(admin)

    resposta = cliente.get(
        "/v1/solicitacoes-de-local/abertas",
        headers=_headers(chave, token),
    )

    assert resposta.status_code == 422


def test_admin_lista_solicitacoes_em_aberto_pela_rota(
    cliente,
    criar_chave,
    criar_persona,
    criar_comunidade,
    criar_sessao_de_teste,
    criar_trilha,
    criar_missao,
    criar_desafio_de_coleta,
    criar_local,
):
    chave, comunidade, _, _, _, _, _ = _preparar_solicitacao_pela_rota(
        cliente,
        criar_chave,
        criar_persona,
        criar_comunidade,
        criar_sessao_de_teste,
        criar_trilha,
        criar_missao,
        criar_desafio_de_coleta,
        criar_local,
    )
    admin = criar_persona(Papel.admin)
    token_admin, _ = criar_sessao_de_teste(admin)

    resposta = cliente.get(
        f"/v1/solicitacoes-de-local/abertas?comunidade={comunidade.id}",
        headers=_headers(chave, token_admin),
    )

    assert resposta.status_code == 200
    corpo = resposta.json()
    assert len(corpo["itens"]) == 1


def test_guerreiro_recebe_403_ao_listar_abertas_pela_rota(
    cliente, criar_chave, criar_persona, criar_comunidade, criar_sessao_de_teste
):
    chave, _ = criar_chave()
    comunidade = criar_comunidade()
    guerreiro = criar_persona(Papel.guerreiro, comunidade=comunidade)
    token, _ = criar_sessao_de_teste(guerreiro)

    resposta = cliente.get(
        f"/v1/solicitacoes-de-local/abertas?comunidade={comunidade.id}",
        headers=_headers(chave, token),
    )

    assert resposta.status_code == 403


def test_guerreiro_consulta_as_proprias_solicitacoes_pela_rota(
    cliente,
    criar_chave,
    criar_persona,
    criar_comunidade,
    criar_sessao_de_teste,
    criar_trilha,
    criar_missao,
    criar_desafio_de_coleta,
    criar_local,
):
    chave, _, _, guerreiro, _, _, solicitacao_id = _preparar_solicitacao_pela_rota(
        cliente,
        criar_chave,
        criar_persona,
        criar_comunidade,
        criar_sessao_de_teste,
        criar_trilha,
        criar_missao,
        criar_desafio_de_coleta,
        criar_local,
    )
    token_guerreiro, _ = criar_sessao_de_teste(guerreiro)

    resposta = cliente.get(
        "/v1/solicitacoes-de-local/minhas", headers=_headers(chave, token_guerreiro)
    )

    assert resposta.status_code == 200
    corpo = resposta.json()
    assert [item["id"] for item in corpo["itens"]] == [solicitacao_id]
    assert corpo["itens"][0]["situacao"] == "recebida"


def test_mestre_recebe_403_ao_consultar_proprias_solicitacoes_pela_rota(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste
):
    chave, _ = criar_chave()
    mestre = criar_persona(Papel.mestre)
    token, _ = criar_sessao_de_teste(mestre)

    resposta = cliente.get("/v1/solicitacoes-de-local/minhas", headers=_headers(chave, token))

    assert resposta.status_code == 403
