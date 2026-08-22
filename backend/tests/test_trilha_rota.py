from nucleo.personas.modelo import Papel
from nucleo.poderes.modelo import NaturezaDoPoder
from nucleo.trilhas.modelo import EtapaDoCiclo


def test_mestre_cria_trilha_pela_rota(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste, criar_poder
):
    chave, _ = criar_chave()
    mestre = criar_persona(Papel.mestre)
    poder = criar_poder(mestre, natureza=NaturezaDoPoder.de_guerreiro)
    token, _ = criar_sessao_de_teste(mestre)

    resposta = cliente.post(
        "/v1/trilhas",
        json={
            "nome": "Robô Educa",
            "objetivo": "Construir o próprio robô.",
            "area_do_conhecimento": "Programação e Robótica",
            "poder_id": str(poder.id),
        },
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
    )

    assert resposta.status_code == 201
    corpo = resposta.json()
    assert corpo["nome"] == "Robô Educa"
    assert corpo["situacao"] == "rascunho"


def test_trilha_com_poder_fora_da_natureza_e_recusada_pela_rota(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste, criar_poder
):
    chave, _ = criar_chave()
    mestre = criar_persona(Papel.mestre)
    poder_sustentador = criar_poder(mestre, natureza=NaturezaDoPoder.derivado_do_aporte)
    token, _ = criar_sessao_de_teste(mestre)

    resposta = cliente.post(
        "/v1/trilhas",
        json={
            "nome": "Trilha inválida",
            "objetivo": "Objetivo.",
            "area_do_conhecimento": "Tecnologia",
            "poder_id": str(poder_sustentador.id),
        },
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
    )

    assert resposta.status_code == 422


def test_criar_trilha_sem_persona_em_sessao_e_recusada(cliente, criar_chave):
    chave, _ = criar_chave()

    resposta = cliente.post(
        "/v1/trilhas",
        json={
            "nome": "Trilha",
            "objetivo": "Objetivo.",
            "area_do_conhecimento": "Tecnologia",
            "poder_id": None,
        },
        headers={"X-Chave-Aplicacao": chave},
    )

    assert resposta.status_code == 401


def test_mestre_le_o_proprio_rascunho_pela_rota(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste, criar_trilha
):
    chave, _ = criar_chave()
    mestre = criar_persona(Papel.mestre)
    trilha = criar_trilha(mestre)
    token, _ = criar_sessao_de_teste(mestre)

    resposta = cliente.get(
        "/v1/trilhas/minhas",
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
    )

    assert resposta.status_code == 200
    ids = [item["id"] for item in resposta.json()]
    assert str(trilha.id) in ids


def test_rascunho_alheio_nao_aparece_pela_rota(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste, criar_trilha
):
    chave, _ = criar_chave()
    mestre_autor = criar_persona(Papel.mestre)
    outro_mestre = criar_persona(Papel.mestre)
    criar_trilha(mestre_autor)
    token, _ = criar_sessao_de_teste(outro_mestre)

    resposta = cliente.get(
        "/v1/trilhas/minhas",
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
    )

    assert resposta.status_code == 200
    assert resposta.json() == []


def test_consulta_de_minhas_trilhas_nao_exige_comunidade(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste, criar_trilha
):
    chave, _ = criar_chave()
    mestre = criar_persona(Papel.mestre)
    criar_trilha(mestre)
    token, _ = criar_sessao_de_teste(mestre)

    resposta = cliente.get(
        "/v1/trilhas/minhas",
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
    )

    assert resposta.status_code == 200
    assert len(resposta.json()) == 1


def test_mestre_autor_acrescenta_missao_pela_rota(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste, criar_trilha
):
    chave, _ = criar_chave()
    mestre = criar_persona(Papel.mestre)
    trilha = criar_trilha(mestre)
    token, _ = criar_sessao_de_teste(mestre)

    resposta = cliente.post(
        f"/v1/trilhas/{trilha.id}/missoes",
        json={
            "titulo": "Primeira missão",
            "posicao": 1,
            "nivel_de_dificuldade": 1,
            "obrigatoria": True,
            "etapa_do_ciclo": EtapaDoCiclo.abertura.value,
        },
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
    )

    assert resposta.status_code == 201
    corpo = resposta.json()
    assert corpo["titulo"] == "Primeira missão"
    assert corpo["trilha_id"] == str(trilha.id)


def test_missao_sem_obrigatoriedade_e_recusada_pela_rota(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste, criar_trilha
):
    chave, _ = criar_chave()
    mestre = criar_persona(Papel.mestre)
    trilha = criar_trilha(mestre)
    token, _ = criar_sessao_de_teste(mestre)

    resposta = cliente.post(
        f"/v1/trilhas/{trilha.id}/missoes",
        json={
            "titulo": "Missão",
            "posicao": 1,
            "nivel_de_dificuldade": 1,
            "etapa_do_ciclo": EtapaDoCiclo.abertura.value,
        },
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
    )

    assert resposta.status_code == 422
    assert resposta.json()["campo"] == "obrigatoria"


def test_sondagem_fora_da_primeira_posicao_e_recusada_pela_rota(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste, criar_trilha
):
    chave, _ = criar_chave()
    mestre = criar_persona(Papel.mestre)
    trilha = criar_trilha(mestre)
    token, _ = criar_sessao_de_teste(mestre)

    resposta = cliente.post(
        f"/v1/trilhas/{trilha.id}/missoes",
        json={
            "titulo": "Sondagem",
            "posicao": 2,
            "nivel_de_dificuldade": 1,
            "obrigatoria": True,
            "etapa_do_ciclo": EtapaDoCiclo.abertura.value,
            "e_sondagem": True,
        },
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
    )

    assert resposta.status_code == 422
    assert resposta.json()["campo"] == "e_sondagem"


def test_segunda_sondagem_e_recusada_pela_rota(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste, criar_trilha, criar_missao
):
    chave, _ = criar_chave()
    mestre = criar_persona(Papel.mestre)
    trilha = criar_trilha(mestre)
    criar_missao(trilha, mestre, posicao=1, e_sondagem=True)
    token, _ = criar_sessao_de_teste(mestre)

    resposta = cliente.post(
        f"/v1/trilhas/{trilha.id}/missoes",
        json={
            "titulo": "Segunda sondagem",
            "posicao": 1,
            "nivel_de_dificuldade": 1,
            "obrigatoria": True,
            "etapa_do_ciclo": EtapaDoCiclo.abertura.value,
            "e_sondagem": True,
        },
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
    )

    assert resposta.status_code == 422
    assert resposta.json()["campo"] == "e_sondagem"


def test_mestre_nao_autor_e_recusado_ao_criar_missao_pela_rota(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste, criar_trilha
):
    chave, _ = criar_chave()
    mestre_autor = criar_persona(Papel.mestre)
    outro_mestre = criar_persona(Papel.mestre)
    trilha = criar_trilha(mestre_autor)
    token, _ = criar_sessao_de_teste(outro_mestre)

    resposta = cliente.post(
        f"/v1/trilhas/{trilha.id}/missoes",
        json={
            "titulo": "Missão",
            "posicao": 1,
            "nivel_de_dificuldade": 1,
            "obrigatoria": True,
            "etapa_do_ciclo": EtapaDoCiclo.abertura.value,
        },
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
    )

    assert resposta.status_code == 403


def test_mestre_autor_cria_atividade_pela_rota(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste, criar_trilha, criar_missao
):
    chave, _ = criar_chave()
    mestre = criar_persona(Papel.mestre)
    trilha = criar_trilha(mestre)
    missao = criar_missao(trilha, mestre)
    token, _ = criar_sessao_de_teste(mestre)

    resposta = cliente.post(
        f"/v1/missoes/{missao.id}/atividades",
        json={
            "titulo": "Montagem do robô",
            "descricao": "Montar o chassi.",
            "modalidade": "individual",
            "formato": "presencial",
            "natureza": "construcao",
            "producao_esperada": "Construir o próprio robô.",
        },
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
    )

    assert resposta.status_code == 201
    corpo = resposta.json()
    assert corpo["titulo"] == "Montagem do robô"
    assert corpo["missao_id"] == str(missao.id)


def test_atividade_sem_formato_e_recusada_pela_rota(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste, criar_trilha, criar_missao
):
    chave, _ = criar_chave()
    mestre = criar_persona(Papel.mestre)
    trilha = criar_trilha(mestre)
    missao = criar_missao(trilha, mestre)
    token, _ = criar_sessao_de_teste(mestre)

    resposta = cliente.post(
        f"/v1/missoes/{missao.id}/atividades",
        json={
            "titulo": "Atividade",
            "modalidade": "individual",
            "natureza": "construcao",
            "producao_esperada": "Construir algo.",
        },
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
    )

    assert resposta.status_code == 422
    assert resposta.json()["campo"] == "formato"


def test_natureza_nova_e_aceita_pela_rota(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste, criar_trilha, criar_missao
):
    chave, _ = criar_chave()
    mestre = criar_persona(Papel.mestre)
    trilha = criar_trilha(mestre)
    missao = criar_missao(trilha, mestre)
    token, _ = criar_sessao_de_teste(mestre)

    resposta = cliente.post(
        f"/v1/missoes/{missao.id}/atividades",
        json={
            "titulo": "Roda de capoeira",
            "modalidade": "em_equipe",
            "formato": "presencial",
            "natureza": "expressao_artistica",
            "producao_esperada": "Executar a sequência.",
        },
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
    )

    assert resposta.status_code == 201
    assert resposta.json()["natureza"] == "expressao_artistica"


def test_mestre_nao_autor_e_recusado_ao_criar_atividade_pela_rota(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste, criar_trilha, criar_missao
):
    chave, _ = criar_chave()
    mestre_autor = criar_persona(Papel.mestre)
    outro_mestre = criar_persona(Papel.mestre)
    trilha = criar_trilha(mestre_autor)
    missao = criar_missao(trilha, mestre_autor)
    token, _ = criar_sessao_de_teste(outro_mestre)

    resposta = cliente.post(
        f"/v1/missoes/{missao.id}/atividades",
        json={
            "titulo": "Atividade",
            "modalidade": "individual",
            "formato": "presencial",
            "natureza": "construcao",
            "producao_esperada": "Construir algo.",
        },
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
    )

    assert resposta.status_code == 403


def test_mestre_autor_declara_cadencia_de_retomada_pela_rota(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste, criar_trilha, criar_missao
):
    chave, _ = criar_chave()
    mestre = criar_persona(Papel.mestre)
    trilha = criar_trilha(mestre)
    missao = criar_missao(trilha, mestre)
    token, _ = criar_sessao_de_teste(mestre)

    resposta = cliente.post(
        f"/v1/missoes/{missao.id}/retomada",
        json={"cadencia_de_retomada": [2, 7, 21]},
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
    )

    assert resposta.status_code == 200
    assert resposta.json()["cadencia_de_retomada"] == [2, 7, 21]

    resposta_substituta = cliente.post(
        f"/v1/missoes/{missao.id}/retomada",
        json={"cadencia_de_retomada": [3]},
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
    )

    assert resposta_substituta.status_code == 200
    assert resposta_substituta.json()["cadencia_de_retomada"] == [3]


def test_mestre_nao_autor_e_recusado_ao_declarar_cadencia_pela_rota(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste, criar_trilha, criar_missao
):
    chave, _ = criar_chave()
    mestre_autor = criar_persona(Papel.mestre)
    outro_mestre = criar_persona(Papel.mestre)
    trilha = criar_trilha(mestre_autor)
    missao = criar_missao(trilha, mestre_autor)
    token, _ = criar_sessao_de_teste(outro_mestre)

    resposta = cliente.post(
        f"/v1/missoes/{missao.id}/retomada",
        json={"cadencia_de_retomada": [2, 7, 21]},
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
    )

    assert resposta.status_code == 403


def test_fluxo_completo_de_autoria_destrava_rotas_orfas(
    cliente,
    criar_chave,
    criar_persona,
    criar_sessao_de_teste,
    criar_poder,
    criar_tipo_de_coleta,
    criar_tipo_de_recurso,
):
    """Cria trilha → missão → atividade só por HTTP e usa os identificadores
    devolvidos para destravar as três rotas órfãs da proposal (`POST
    /desafios-de-coleta` e `POST /trilhas/{id}/recompensas-de-marco`)."""
    chave, _ = criar_chave()
    mestre = criar_persona(Papel.mestre)
    poder = criar_poder(mestre, natureza=NaturezaDoPoder.de_guerreiro)
    token, _ = criar_sessao_de_teste(mestre)
    cabecalhos = {"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"}

    resposta_trilha = cliente.post(
        "/v1/trilhas",
        json={
            "nome": "Robô Educa",
            "objetivo": "Construir o próprio robô.",
            "area_do_conhecimento": "Programação e Robótica",
            "poder_id": str(poder.id),
        },
        headers=cabecalhos,
    )
    assert resposta_trilha.status_code == 201
    trilha_id = resposta_trilha.json()["id"]

    resposta_missao = cliente.post(
        f"/v1/trilhas/{trilha_id}/missoes",
        json={
            "titulo": "Primeira missão",
            "posicao": 1,
            "nivel_de_dificuldade": 1,
            "obrigatoria": True,
            "etapa_do_ciclo": EtapaDoCiclo.abertura.value,
        },
        headers=cabecalhos,
    )
    assert resposta_missao.status_code == 201
    missao_id = resposta_missao.json()["id"]

    resposta_atividade = cliente.post(
        f"/v1/missoes/{missao_id}/atividades",
        json={
            "titulo": "Montagem do robô",
            "modalidade": "individual",
            "formato": "presencial",
            "natureza": "construcao",
            "producao_esperada": "Construir o próprio robô.",
        },
        headers=cabecalhos,
    )
    assert resposta_atividade.status_code == 201

    tipo_de_coleta = criar_tipo_de_coleta(mestre)
    resposta_desafio_de_coleta = cliente.post(
        "/v1/desafios-de-coleta",
        json={
            "missao_id": missao_id,
            "tipo_de_coleta_id": str(tipo_de_coleta.id),
            "cadencia": "semanal",
            "vigencia_inicio": "2026-01-01T00:00:00-03:00",
            "vigencia_fim": "2026-12-31T00:00:00-03:00",
            "granularidade_exigida": "rua",
            "registros_que_pontuam_por_periodo": 1,
        },
        headers=cabecalhos,
    )
    assert resposta_desafio_de_coleta.status_code == 201

    tipo_de_recurso = criar_tipo_de_recurso(mestre)
    resposta_recompensa = cliente.post(
        f"/v1/trilhas/{trilha_id}/recompensas-de-marco",
        json={
            "missao_id": missao_id,
            "tipo_de_recurso_id": str(tipo_de_recurso.id),
            "quantidade": "30",
        },
        headers=cabecalhos,
    )
    assert resposta_recompensa.status_code == 201
