from nucleo.personas.modelo import Papel
from nucleo.poderes.modelo import NaturezaDoPoder
from nucleo.trilhas.modelo import EtapaDoCiclo, SituacaoDaTrilha


def _criar_trilha_completa_pela_rota(cliente, cabecalhos, poder, criar_tipo_de_coleta, mestre):
    """Trilha em rascunho que atende às três travas de publicação, montada
    só por HTTP: sondagem, desafio de coleta e culminância."""
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
            "titulo": "Sondagem",
            "posicao": 1,
            "nivel_de_dificuldade": 1,
            "obrigatoria": True,
            "etapa_do_ciclo": EtapaDoCiclo.abertura.value,
            "e_sondagem": True,
        },
        headers=cabecalhos,
    )
    assert resposta_missao.status_code == 201
    missao_id = resposta_missao.json()["id"]

    tipo_de_coleta = criar_tipo_de_coleta(mestre)
    resposta_desafio = cliente.post(
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
    assert resposta_desafio.status_code == 201

    resposta_culminancia = cliente.post(
        f"/v1/trilhas/{trilha_id}/culminancia",
        json={
            "descricao": "Um robô que resolve um problema da comunidade.",
            "modalidade": "individual",
            "criterio_de_validacao": "O robô precisa funcionar.",
        },
        headers=cabecalhos,
    )
    assert resposta_culminancia.status_code == 200

    return trilha_id


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


def test_mestre_autor_publica_a_propria_trilha_pela_rota(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste, criar_poder, criar_tipo_de_coleta
):
    chave, _ = criar_chave()
    mestre = criar_persona(Papel.mestre)
    poder = criar_poder(mestre, natureza=NaturezaDoPoder.de_guerreiro)
    token, _ = criar_sessao_de_teste(mestre)
    cabecalhos = {"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"}
    trilha_id = _criar_trilha_completa_pela_rota(
        cliente, cabecalhos, poder, criar_tipo_de_coleta, mestre
    )

    resposta = cliente.post(f"/v1/trilhas/{trilha_id}/publicacao", headers=cabecalhos)

    assert resposta.status_code == 200
    assert resposta.json()["situacao"] == "publicada"


def test_trilha_sem_etiqueta_ods_publica_no_ciclo_01(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste, criar_poder, criar_tipo_de_coleta
):
    """`RF-09-93`: a falta de etiqueta ODS não é trava de publicação no
    Ciclo 01 — a trava do `RF-09-96` é do Ciclo 02."""
    chave, _ = criar_chave()
    mestre = criar_persona(Papel.mestre)
    poder = criar_poder(mestre, natureza=NaturezaDoPoder.de_guerreiro)
    token, _ = criar_sessao_de_teste(mestre)
    cabecalhos = {"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"}
    trilha_id = _criar_trilha_completa_pela_rota(
        cliente, cabecalhos, poder, criar_tipo_de_coleta, mestre
    )

    resposta = cliente.post(f"/v1/trilhas/{trilha_id}/publicacao", headers=cabecalhos)

    assert resposta.status_code == 200
    corpo = resposta.json()
    assert corpo["situacao"] == "publicada"
    assert corpo["etiquetas_ods"] == []
    assert corpo["cobertura_ods"]["objetivos"] == []


def test_publicacao_por_outro_mestre_e_recusada_pela_rota(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste, criar_trilha
):
    chave, _ = criar_chave()
    mestre_autor = criar_persona(Papel.mestre)
    outro_mestre = criar_persona(Papel.mestre)
    trilha = criar_trilha(mestre_autor)
    token, _ = criar_sessao_de_teste(outro_mestre)

    resposta = cliente.post(
        f"/v1/trilhas/{trilha.id}/publicacao",
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
    )

    assert resposta.status_code == 403


def test_admin_despublica_trilha_publicada_com_motivo_pela_rota(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste, criar_trilha
):
    chave, _ = criar_chave()
    mestre = criar_persona(Papel.mestre)
    admin = criar_persona(Papel.admin)
    trilha = criar_trilha(mestre, situacao=SituacaoDaTrilha.publicada)
    token, _ = criar_sessao_de_teste(admin)

    resposta = cliente.post(
        f"/v1/trilhas/{trilha.id}/despublicacao",
        json={"motivo": "Conteúdo desatualizado."},
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
    )

    assert resposta.status_code == 200
    corpo = resposta.json()
    assert corpo["situacao"] == "despublicada"
    assert corpo["motivo_da_situacao"] == "Conteúdo desatualizado."


def test_despublicacao_sem_motivo_e_recusada_pela_rota(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste, criar_trilha
):
    chave, _ = criar_chave()
    mestre = criar_persona(Papel.mestre)
    admin = criar_persona(Papel.admin)
    trilha = criar_trilha(mestre, situacao=SituacaoDaTrilha.publicada)
    token, _ = criar_sessao_de_teste(admin)

    resposta = cliente.post(
        f"/v1/trilhas/{trilha.id}/despublicacao",
        json={"motivo": ""},
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
    )

    assert resposta.status_code == 422


def test_mestre_nao_despublica_pela_rota(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste, criar_trilha
):
    chave, _ = criar_chave()
    mestre = criar_persona(Papel.mestre)
    trilha = criar_trilha(mestre, situacao=SituacaoDaTrilha.publicada)
    token, _ = criar_sessao_de_teste(mestre)

    resposta = cliente.post(
        f"/v1/trilhas/{trilha.id}/despublicacao",
        json={"motivo": "Motivo qualquer."},
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
    )

    assert resposta.status_code == 403


def test_despublicacao_de_rascunho_e_recusada_pela_rota(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste, criar_trilha
):
    chave, _ = criar_chave()
    mestre = criar_persona(Papel.mestre)
    admin = criar_persona(Papel.admin)
    trilha = criar_trilha(mestre)
    token, _ = criar_sessao_de_teste(admin)

    resposta = cliente.post(
        f"/v1/trilhas/{trilha.id}/despublicacao",
        json={"motivo": "Motivo qualquer."},
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
    )

    assert resposta.status_code == 422


def test_mestre_autor_republica_trilha_corrigida_pela_rota(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste, criar_poder, criar_tipo_de_coleta
):
    chave, _ = criar_chave()
    mestre = criar_persona(Papel.mestre)
    admin = criar_persona(Papel.admin)
    poder = criar_poder(mestre, natureza=NaturezaDoPoder.de_guerreiro)
    token_mestre, _ = criar_sessao_de_teste(mestre)
    token_admin, _ = criar_sessao_de_teste(admin)
    cabecalhos_mestre = {"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token_mestre}"}
    cabecalhos_admin = {"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token_admin}"}

    trilha_id = _criar_trilha_completa_pela_rota(
        cliente, cabecalhos_mestre, poder, criar_tipo_de_coleta, mestre
    )
    cliente.post(f"/v1/trilhas/{trilha_id}/publicacao", headers=cabecalhos_mestre)
    resposta_despublicacao = cliente.post(
        f"/v1/trilhas/{trilha_id}/despublicacao",
        json={"motivo": "Corrigir a descrição."},
        headers=cabecalhos_admin,
    )
    assert resposta_despublicacao.status_code == 200

    resposta_republicacao = cliente.post(
        f"/v1/trilhas/{trilha_id}/publicacao", headers=cabecalhos_mestre
    )

    assert resposta_republicacao.status_code == 200
    corpo = resposta_republicacao.json()
    assert corpo["situacao"] == "publicada"
    assert corpo["motivo_da_situacao"] is None


def test_republicacao_reconfere_as_travas_pela_rota(
    cliente,
    criar_chave,
    criar_persona,
    criar_sessao_de_teste,
    criar_trilha,
    criar_missao,
    criar_desafio_de_coleta,
):
    chave, _ = criar_chave()
    mestre = criar_persona(Papel.mestre)
    trilha = criar_trilha(mestre, situacao=SituacaoDaTrilha.despublicada)
    missao = criar_missao(trilha, mestre, posicao=1, e_sondagem=True)
    criar_desafio_de_coleta(missao, mestre)
    token, _ = criar_sessao_de_teste(mestre)

    resposta = cliente.post(
        f"/v1/trilhas/{trilha.id}/publicacao",
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
    )

    assert resposta.status_code == 422
    assert "culminância" in resposta.json()["mensagem"]


def test_get_trilha_publica_serve_so_publicada(cliente, criar_chave, criar_persona, criar_trilha):
    chave, _ = criar_chave()
    mestre = criar_persona(Papel.mestre)
    trilha_publicada = criar_trilha(mestre, situacao=SituacaoDaTrilha.publicada)
    trilha_rascunho = criar_trilha(mestre, situacao=SituacaoDaTrilha.rascunho)
    trilha_despublicada = criar_trilha(mestre, situacao=SituacaoDaTrilha.despublicada)

    resposta_publicada = cliente.get(
        f"/v1/trilhas/{trilha_publicada.id}", headers={"X-Chave-Aplicacao": chave}
    )
    resposta_rascunho = cliente.get(
        f"/v1/trilhas/{trilha_rascunho.id}", headers={"X-Chave-Aplicacao": chave}
    )
    resposta_despublicada = cliente.get(
        f"/v1/trilhas/{trilha_despublicada.id}", headers={"X-Chave-Aplicacao": chave}
    )

    assert resposta_publicada.status_code == 200
    corpo = resposta_publicada.json()
    assert corpo["licenca"] == "CC BY-SA"
    assert corpo["situacao"] == "publicada"
    assert resposta_rascunho.status_code == 404
    assert resposta_despublicada.status_code == 404


def test_motivo_da_despublicacao_aparece_em_minhas_pela_rota(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste, criar_trilha
):
    chave, _ = criar_chave()
    mestre = criar_persona(Papel.mestre)
    admin = criar_persona(Papel.admin)
    trilha = criar_trilha(mestre, situacao=SituacaoDaTrilha.publicada)
    token_admin, _ = criar_sessao_de_teste(admin)
    token_mestre, _ = criar_sessao_de_teste(mestre)

    cliente.post(
        f"/v1/trilhas/{trilha.id}/despublicacao",
        json={"motivo": "Conteúdo desatualizado."},
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token_admin}"},
    )

    resposta = cliente.get(
        "/v1/trilhas/minhas",
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token_mestre}"},
    )

    assert resposta.status_code == 200
    trilha_na_lista = next(item for item in resposta.json() if item["id"] == str(trilha.id))
    assert trilha_na_lista["situacao"] == "despublicada"
    assert trilha_na_lista["motivo_da_situacao"] == "Conteúdo desatualizado."


def test_trilha_sem_conteudo_algum_continua_publicando_por_tres_travas(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste, criar_poder, criar_tipo_de_coleta
):
    """`RN-09-01` a `RN-09-03`: `conteudo-e-bibliografia-da-missao` não toca
    `trilhas.regra` — as três travas de publicação continuam sendo as
    únicas, sem conteúdo nem bibliografia declarados."""
    chave, _ = criar_chave()
    mestre = criar_persona(Papel.mestre)
    poder = criar_poder(mestre, natureza=NaturezaDoPoder.de_guerreiro)
    token, _ = criar_sessao_de_teste(mestre)
    cabecalhos = {"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"}
    trilha_id = _criar_trilha_completa_pela_rota(
        cliente, cabecalhos, poder, criar_tipo_de_coleta, mestre
    )

    resposta = cliente.post(f"/v1/trilhas/{trilha_id}/publicacao", headers=cabecalhos)

    assert resposta.status_code == 200
    assert resposta.json()["situacao"] == "publicada"


def test_leitura_publica_traz_conteudo_fonte_e_bibliografia_so_quando_publicada(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste, criar_poder, criar_tipo_de_coleta
):
    chave, _ = criar_chave()
    mestre = criar_persona(Papel.mestre)
    poder = criar_poder(mestre, natureza=NaturezaDoPoder.de_guerreiro)
    token, _ = criar_sessao_de_teste(mestre)
    cabecalhos = {"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"}
    trilha_id = _criar_trilha_completa_pela_rota(
        cliente, cabecalhos, poder, criar_tipo_de_coleta, mestre
    )
    missao_id = cliente.get("/v1/trilhas/minhas", headers=cabecalhos).json()[0]["missoes"][0]["id"]

    resposta_conteudo = cliente.post(
        f"/v1/missoes/{missao_id}/conteudos",
        json={
            "tipo": "texto",
            "ordem": 1,
            "corpo": "Trecho citado de outro autor.",
            "autoria": "terceiro",
            "fonte": "Autor Exemplo, 2020.",
        },
        headers=cabecalhos,
    )
    assert resposta_conteudo.status_code == 201

    resposta_bibliografia = cliente.post(
        f"/v1/missoes/{missao_id}/bibliografia",
        json={"titulo": "Robótica Educativa", "capitulo": "Capítulo 3"},
        headers=cabecalhos,
    )
    assert resposta_bibliografia.status_code == 201

    resposta_leitura_em_rascunho = cliente.get(
        f"/v1/trilhas/{trilha_id}", headers={"X-Chave-Aplicacao": chave}
    )
    assert resposta_leitura_em_rascunho.status_code == 404

    cliente.post(f"/v1/trilhas/{trilha_id}/publicacao", headers=cabecalhos)

    resposta_leitura = cliente.get(f"/v1/trilhas/{trilha_id}", headers={"X-Chave-Aplicacao": chave})

    assert resposta_leitura.status_code == 200
    corpo = resposta_leitura.json()
    assert corpo["licenca"] == "CC BY-SA"
    missao = next(m for m in corpo["missoes"] if m["id"] == missao_id)
    assert len(missao["conteudos"]) == 1
    assert missao["conteudos"][0]["fonte"] == "Autor Exemplo, 2020."
    assert len(missao["bibliografia"]) == 1
    assert missao["bibliografia"][0]["titulo"] == "Robótica Educativa"
