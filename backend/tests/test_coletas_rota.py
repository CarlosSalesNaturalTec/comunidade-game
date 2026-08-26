import uuid
from datetime import UTC, datetime, timedelta

from nucleo.coletas.modelo import Cadencia, FormaDeRegistro, SerieDeColeta, TipoDeColeta
from nucleo.coletas.regra import abrir_serie_de_coleta
from nucleo.comunidades.modelo import ComunidadeVirtual, VinculoJogador
from nucleo.locais.modelo import NivelDoLocal
from nucleo.personas.modelo import Papel, Persona
from nucleo.trilhas.modelo import Missao, Trilha

INICIO = "2026-01-01T00:00:00-03:00"
FIM = "2026-12-31T00:00:00-03:00"
MOMENTO_DA_MEDICAO = "2026-07-08T14:00:00-03:00"


def test_admin_cadastra_tipo_de_coleta_pela_rota(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste
):
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    token, _ = criar_sessao_de_teste(admin)

    resposta = cliente.post(
        "/v1/tipos-de-coleta",
        json={
            "nome": "Temperatura",
            "forma_de_registro": FormaDeRegistro.numero.value,
            "unidade": "°C",
            "faixa_minima": -10,
            "faixa_maxima": 55,
        },
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
    )

    assert resposta.status_code == 201
    corpo = resposta.json()
    assert corpo["nome"] == "Temperatura"
    assert corpo["ativo"] is True


def test_mestre_recebe_403_ao_cadastrar_tipo_de_coleta_pela_rota(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste
):
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    mestre = criar_persona(Papel.mestre, criada_por=admin)
    token, _ = criar_sessao_de_teste(mestre)

    resposta = cliente.post(
        "/v1/tipos-de-coleta",
        json={"nome": "Temperatura", "forma_de_registro": FormaDeRegistro.numero.value},
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
    )

    assert resposta.status_code == 403


def test_mestre_autor_cria_desafio_de_coleta_pela_rota(
    cliente,
    criar_chave,
    criar_persona,
    criar_sessao_de_teste,
    criar_trilha,
    criar_missao,
    criar_tipo_de_coleta,
):
    chave, _ = criar_chave()
    mestre = criar_persona(Papel.mestre)
    trilha = criar_trilha(mestre)
    missao = criar_missao(trilha, mestre)
    tipo = criar_tipo_de_coleta(mestre)
    token, _ = criar_sessao_de_teste(mestre)

    resposta = cliente.post(
        "/v1/desafios-de-coleta",
        json={
            "missao_id": str(missao.id),
            "tipo_de_coleta_id": str(tipo.id),
            "cadencia": Cadencia.semanal.value,
            "vigencia_inicio": INICIO,
            "vigencia_fim": FIM,
            "granularidade_exigida": NivelDoLocal.rua.value,
            "registros_que_pontuam_por_periodo": 1,
        },
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
    )

    assert resposta.status_code == 201
    corpo = resposta.json()
    assert corpo["missao_id"] == str(missao.id)
    assert corpo["tipo_de_coleta_id"] == str(tipo.id)


def test_mestre_que_nao_e_autor_recebe_403_pela_rota(
    cliente,
    criar_chave,
    criar_persona,
    criar_sessao_de_teste,
    criar_trilha,
    criar_missao,
    criar_tipo_de_coleta,
):
    chave, _ = criar_chave()
    autor = criar_persona(Papel.mestre)
    outro_mestre = criar_persona(Papel.mestre)
    trilha = criar_trilha(autor)
    missao = criar_missao(trilha, autor)
    tipo = criar_tipo_de_coleta(autor)
    token, _ = criar_sessao_de_teste(outro_mestre)

    resposta = cliente.post(
        "/v1/desafios-de-coleta",
        json={
            "missao_id": str(missao.id),
            "tipo_de_coleta_id": str(tipo.id),
            "cadencia": Cadencia.semanal.value,
            "vigencia_inicio": INICIO,
            "vigencia_fim": FIM,
            "granularidade_exigida": NivelDoLocal.rua.value,
            "registros_que_pontuam_por_periodo": 1,
        },
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
    )

    assert resposta.status_code == 403


def test_desafio_com_etiqueta_ods_declarada_e_recusado(
    cliente,
    criar_chave,
    criar_persona,
    criar_sessao_de_teste,
    criar_trilha,
    criar_missao,
    criar_tipo_de_coleta,
):
    """A etiqueta ODS é derivada da missão ou da trilha, nunca declarada
    pelo Mestre — o contrato de entrada nem sequer tem o campo, e o
    `extra="forbid"` recusa qualquer tentativa (`RF-08-25`)."""
    chave, _ = criar_chave()
    mestre = criar_persona(Papel.mestre)
    trilha = criar_trilha(mestre)
    missao = criar_missao(trilha, mestre)
    tipo = criar_tipo_de_coleta(mestre)
    token, _ = criar_sessao_de_teste(mestre)

    resposta = cliente.post(
        "/v1/desafios-de-coleta",
        json={
            "missao_id": str(missao.id),
            "tipo_de_coleta_id": str(tipo.id),
            "cadencia": Cadencia.semanal.value,
            "vigencia_inicio": INICIO,
            "vigencia_fim": FIM,
            "granularidade_exigida": NivelDoLocal.rua.value,
            "registros_que_pontuam_por_periodo": 1,
            "etiqueta_ods": 4,
        },
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
    )

    assert resposta.status_code == 422


def _preparar_serie_pela_rota(
    sessao,
    criar_chave,
    criar_persona,
    criar_comunidade,
    criar_sessao_de_teste,
    criar_trilha,
    criar_missao,
    criar_tipo_de_coleta,
    criar_desafio_de_coleta,
    criar_local,
    criar_poder_do_territorio,
):
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    criar_poder_do_territorio(admin)
    mestre = criar_persona(Papel.mestre)
    trilha = criar_trilha(mestre)
    missao = criar_missao(trilha, mestre)
    tipo = criar_tipo_de_coleta(admin)
    desafio = criar_desafio_de_coleta(
        missao,
        mestre,
        tipo=tipo,
        granularidade_exigida=NivelDoLocal.bairro,
        vigencia_inicio="2026-01-01T00:00:00+00:00",
        vigencia_fim="2026-12-31T00:00:00+00:00",
    )
    # `criar_comunidade` nasce com granularidade máxima "bairro" — o mesmo
    # teto exigido pelo desafio acima.
    comunidade = criar_comunidade()
    guerreiro = criar_persona(Papel.guerreiro, comunidade=comunidade)
    # A medição do teste é datada no passado simulado; recua o início do
    # vínculo, que nasce em `server_default=func.now()`, para que aquela
    # data caia dentro do intervalo vigente (`RN-08-03`).
    vinculo = sessao.query(VinculoJogador).filter_by(guerreiro_id=guerreiro.id).one()
    vinculo.data_inicio = datetime(2025, 1, 1, tzinfo=UTC)
    sessao.commit()
    local_da_comunidade = criar_local(
        comunidade, nivel=NivelDoLocal.comunidade, rotulo="Território"
    )
    local = criar_local(
        comunidade, nivel=NivelDoLocal.bairro, rotulo="Bairro", local_pai=local_da_comunidade
    )

    token, _ = criar_sessao_de_teste(guerreiro)
    return chave, token, guerreiro, desafio, local


def test_guerreiro_abre_serie_de_coleta_pela_rota(
    cliente,
    sessao,
    criar_chave,
    criar_persona,
    criar_comunidade,
    criar_sessao_de_teste,
    criar_trilha,
    criar_missao,
    criar_tipo_de_coleta,
    criar_desafio_de_coleta,
    criar_local,
    criar_poder_do_territorio,
):
    chave, token, _, desafio, local = _preparar_serie_pela_rota(
        sessao,
        criar_chave,
        criar_persona,
        criar_comunidade,
        criar_sessao_de_teste,
        criar_trilha,
        criar_missao,
        criar_tipo_de_coleta,
        criar_desafio_de_coleta,
        criar_local,
        criar_poder_do_territorio,
    )

    resposta = cliente.post(
        "/v1/series-de-coleta",
        json={"desafio_de_coleta_id": str(desafio.id), "local_id": str(local.id)},
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
    )

    assert resposta.status_code == 201
    corpo = resposta.json()
    assert corpo["desafio_de_coleta_id"] == str(desafio.id)
    assert corpo["local_id"] == str(local.id)
    assert corpo["estado"] == "ativa"


def test_mestre_recebe_403_ao_abrir_serie_de_coleta_pela_rota(
    cliente,
    sessao,
    criar_chave,
    criar_persona,
    criar_comunidade,
    criar_sessao_de_teste,
    criar_trilha,
    criar_missao,
    criar_tipo_de_coleta,
    criar_desafio_de_coleta,
    criar_local,
    criar_poder_do_territorio,
):
    chave, _, _, desafio, local = _preparar_serie_pela_rota(
        sessao,
        criar_chave,
        criar_persona,
        criar_comunidade,
        criar_sessao_de_teste,
        criar_trilha,
        criar_missao,
        criar_tipo_de_coleta,
        criar_desafio_de_coleta,
        criar_local,
        criar_poder_do_territorio,
    )
    mestre = criar_persona(Papel.mestre)
    token, _ = criar_sessao_de_teste(mestre)

    resposta = cliente.post(
        "/v1/series-de-coleta",
        json={"desafio_de_coleta_id": str(desafio.id), "local_id": str(local.id)},
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
    )

    assert resposta.status_code == 403


def test_coletor_grava_registro_de_coleta_pela_rota(
    cliente,
    sessao,
    criar_chave,
    criar_persona,
    criar_comunidade,
    criar_sessao_de_teste,
    criar_trilha,
    criar_missao,
    criar_tipo_de_coleta,
    criar_desafio_de_coleta,
    criar_local,
    criar_poder_do_territorio,
):
    chave, token, guerreiro, desafio, local = _preparar_serie_pela_rota(
        sessao,
        criar_chave,
        criar_persona,
        criar_comunidade,
        criar_sessao_de_teste,
        criar_trilha,
        criar_missao,
        criar_tipo_de_coleta,
        criar_desafio_de_coleta,
        criar_local,
        criar_poder_do_territorio,
    )
    headers = {"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"}
    resposta_serie = cliente.post(
        "/v1/series-de-coleta",
        json={"desafio_de_coleta_id": str(desafio.id), "local_id": str(local.id)},
        headers=headers,
    )
    serie_id = resposta_serie.json()["id"]

    resposta = cliente.post(
        "/v1/registros-de-coleta",
        data={
            "serie_de_coleta_id": serie_id,
            "momento_do_fato": MOMENTO_DA_MEDICAO,
            "origem": "manual",
            "valor": "25.0",
            "unidade": "°C",
        },
        headers=headers,
    )

    assert resposta.status_code == 201
    corpo = resposta.json()
    assert corpo["serie_de_coleta_id"] == serie_id
    assert corpo["pontos_creditados"] == 5
    assert corpo["pontuou"] is True


def test_mestre_recebe_403_ao_consultar_series_do_guerreiro_pela_rota(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste
):
    chave, _ = criar_chave()
    mestre = criar_persona(Papel.mestre)
    token, _ = criar_sessao_de_teste(mestre)

    resposta = cliente.get(
        "/v1/series-de-coleta/minhas",
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
    )

    assert resposta.status_code == 403


def test_guerreiro_consulta_suas_series_pela_rota(
    cliente,
    sessao,
    criar_chave,
    criar_persona,
    criar_comunidade,
    criar_sessao_de_teste,
    criar_trilha,
    criar_missao,
    criar_tipo_de_coleta,
    criar_desafio_de_coleta,
    criar_local,
    criar_poder_do_territorio,
):
    """Ponta a ponta do critério de aceite do PRD-08 §12: série sem
    registro por dois períodos de cadência aparece `interrompida` e para
    de creditar; o registro seguinte a devolve para `ativa` (`RF-08-10`,
    `RF-08-11`, `RF-08-17`)."""
    chave, token, guerreiro, desafio, local = _preparar_serie_pela_rota(
        sessao,
        criar_chave,
        criar_persona,
        criar_comunidade,
        criar_sessao_de_teste,
        criar_trilha,
        criar_missao,
        criar_tipo_de_coleta,
        criar_desafio_de_coleta,
        criar_local,
        criar_poder_do_territorio,
    )
    headers = {"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"}
    resposta_serie = cliente.post(
        "/v1/series-de-coleta",
        json={"desafio_de_coleta_id": str(desafio.id), "local_id": str(local.id)},
        headers=headers,
    )
    serie_id = resposta_serie.json()["id"]

    serie = sessao.get(SerieDeColeta, uuid.UUID(serie_id))
    serie.aberta_em = datetime.now(UTC) - timedelta(weeks=3)
    sessao.commit()

    resposta_interrompida = cliente.get("/v1/series-de-coleta/minhas", headers=headers)
    assert resposta_interrompida.status_code == 200
    corpo_interrompido = resposta_interrompida.json()
    assert len(corpo_interrompido["itens"]) == 1
    assert corpo_interrompido["itens"][0]["id"] == serie_id
    assert corpo_interrompido["itens"][0]["estado"] == "interrompida"
    assert corpo_interrompido["itens"][0]["pontos"] == 0

    resposta_registro = cliente.post(
        "/v1/registros-de-coleta",
        data={
            "serie_de_coleta_id": serie_id,
            "momento_do_fato": datetime.now(UTC).isoformat(),
            "origem": "manual",
            "valor": "25.0",
            "unidade": "°C",
        },
        headers=headers,
    )
    assert resposta_registro.status_code == 201

    resposta_ativa = cliente.get("/v1/series-de-coleta/minhas", headers=headers)
    corpo_ativo = resposta_ativa.json()
    assert corpo_ativo["itens"][0]["estado"] == "ativa"
    assert corpo_ativo["itens"][0]["pontos"] > 0


def test_consulta_das_series_pagina_com_cursor(
    cliente,
    sessao,
    criar_chave,
    criar_persona,
    criar_comunidade,
    criar_sessao_de_teste,
    criar_trilha,
    criar_missao,
    criar_tipo_de_coleta,
    criar_desafio_de_coleta,
    criar_local,
    criar_poder_do_territorio,
    sobrescrever_configuracao,
):
    """A página devolve só o tamanho pedido e o cursor da página seguinte
    quando há mais séries do que cabem nela; percorrer as páginas até o
    cursor vir nulo devolve cada série do Guerreiro(a) uma única vez, sem
    repetição e sem falta (`RF-01-28`)."""
    chave, token, guerreiro, desafio, local = _preparar_serie_pela_rota(
        sessao,
        criar_chave,
        criar_persona,
        criar_comunidade,
        criar_sessao_de_teste,
        criar_trilha,
        criar_missao,
        criar_tipo_de_coleta,
        criar_desafio_de_coleta,
        criar_local,
        criar_poder_do_territorio,
    )
    headers = {"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"}
    missao = sessao.get(Missao, desafio.missao_id)
    trilha = sessao.get(Trilha, missao.trilha_id)
    mestre = sessao.get(Persona, trilha.autor_id)
    tipo = sessao.get(TipoDeColeta, desafio.tipo_de_coleta_id)
    outro_desafio = criar_desafio_de_coleta(
        missao,
        mestre,
        tipo=tipo,
        granularidade_exigida=NivelDoLocal.bairro,
        vigencia_inicio="2026-01-01T00:00:00+00:00",
        vigencia_fim="2026-12-31T00:00:00+00:00",
    )
    cliente.post(
        "/v1/series-de-coleta",
        json={"desafio_de_coleta_id": str(desafio.id), "local_id": str(local.id)},
        headers=headers,
    )
    cliente.post(
        "/v1/series-de-coleta",
        json={"desafio_de_coleta_id": str(outro_desafio.id), "local_id": str(local.id)},
        headers=headers,
    )

    sobrescrever_configuracao(paginacao_tamanho_padrao=1)

    primeira_pagina = cliente.get("/v1/series-de-coleta/minhas", headers=headers)
    assert primeira_pagina.status_code == 200
    corpo_primeira = primeira_pagina.json()
    assert len(corpo_primeira["itens"]) == 1
    assert corpo_primeira["proximo_cursor"] is not None

    segunda_pagina = cliente.get(
        "/v1/series-de-coleta/minhas",
        params={"cursor": corpo_primeira["proximo_cursor"]},
        headers=headers,
    )
    assert segunda_pagina.status_code == 200
    corpo_segunda = segunda_pagina.json()
    assert len(corpo_segunda["itens"]) == 1
    assert corpo_segunda["proximo_cursor"] is None

    ids_da_primeira = {item["id"] for item in corpo_primeira["itens"]}
    ids_da_segunda = {item["id"] for item in corpo_segunda["itens"]}
    assert ids_da_primeira.isdisjoint(ids_da_segunda)


def test_consulta_das_series_recusa_parametro_desconhecido(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste
):
    chave, _ = criar_chave()
    guerreiro = criar_persona(Papel.guerreiro)
    token, _ = criar_sessao_de_teste(guerreiro)

    resposta = cliente.get(
        "/v1/series-de-coleta/minhas",
        params={"tema": "qualquer"},
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
    )

    assert resposta.status_code == 422
    corpo = resposta.json()
    assert corpo["codigo"] == "parametro_desconhecido"
    assert corpo["campo"] == "tema"


def test_consulta_das_series_recusa_tamanho_acima_do_teto(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste
):
    chave, _ = criar_chave()
    guerreiro = criar_persona(Papel.guerreiro)
    token, _ = criar_sessao_de_teste(guerreiro)

    resposta = cliente.get(
        "/v1/series-de-coleta/minhas",
        params={"tamanho": "1000"},
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
    )

    assert resposta.status_code == 422
    corpo = resposta.json()
    assert corpo["codigo"] == "tamanho_de_pagina_acima_do_teto"
    assert corpo["campo"] == "tamanho"


def test_consulta_das_series_pela_rota_nunca_alcanca_serie_de_outro_guerreiro(
    cliente,
    sessao,
    criar_chave,
    criar_persona,
    criar_comunidade,
    criar_sessao_de_teste,
    criar_trilha,
    criar_missao,
    criar_tipo_de_coleta,
    criar_desafio_de_coleta,
    criar_local,
    criar_poder_do_territorio,
):
    """Sob o contrato de listagem, a consulta continua devolvendo só as
    séries do Guerreiro(a) da sessão, mesmo havendo série de outro sobre o
    mesmo desafio e local (`RN-08-04`, `RF-08-17`)."""
    chave, token, guerreiro, desafio, local = _preparar_serie_pela_rota(
        sessao,
        criar_chave,
        criar_persona,
        criar_comunidade,
        criar_sessao_de_teste,
        criar_trilha,
        criar_missao,
        criar_tipo_de_coleta,
        criar_desafio_de_coleta,
        criar_local,
        criar_poder_do_territorio,
    )
    headers = {"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"}
    resposta_serie = cliente.post(
        "/v1/series-de-coleta",
        json={"desafio_de_coleta_id": str(desafio.id), "local_id": str(local.id)},
        headers=headers,
    )
    serie_id = resposta_serie.json()["id"]

    comunidade = sessao.get(ComunidadeVirtual, local.comunidade_virtual_id)
    outro_guerreiro = criar_persona(Papel.guerreiro, comunidade=comunidade)
    abrir_serie_de_coleta(sessao, operador=outro_guerreiro, desafio=desafio, local_id=local.id)
    sessao.commit()

    resposta = cliente.get("/v1/series-de-coleta/minhas", headers=headers)

    assert resposta.status_code == 200
    corpo = resposta.json()
    assert [item["id"] for item in corpo["itens"]] == [serie_id]


def test_guerreiro_consulta_historico_da_serie_pela_rota(
    cliente,
    sessao,
    criar_chave,
    criar_persona,
    criar_comunidade,
    criar_sessao_de_teste,
    criar_trilha,
    criar_missao,
    criar_tipo_de_coleta,
    criar_desafio_de_coleta,
    criar_local,
    criar_poder_do_territorio,
):
    chave, token, guerreiro, desafio, local = _preparar_serie_pela_rota(
        sessao,
        criar_chave,
        criar_persona,
        criar_comunidade,
        criar_sessao_de_teste,
        criar_trilha,
        criar_missao,
        criar_tipo_de_coleta,
        criar_desafio_de_coleta,
        criar_local,
        criar_poder_do_territorio,
    )
    headers = {"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"}
    resposta_serie = cliente.post(
        "/v1/series-de-coleta",
        json={"desafio_de_coleta_id": str(desafio.id), "local_id": str(local.id)},
        headers=headers,
    )
    serie_id = resposta_serie.json()["id"]
    cliente.post(
        "/v1/registros-de-coleta",
        data={
            "serie_de_coleta_id": serie_id,
            "momento_do_fato": MOMENTO_DA_MEDICAO,
            "origem": "manual",
            "valor": "25.0",
            "unidade": "°C",
        },
        headers=headers,
    )

    resposta = cliente.get(f"/v1/series-de-coleta/{serie_id}/registros", headers=headers)

    assert resposta.status_code == 200
    corpo = resposta.json()
    assert len(corpo["itens"]) == 1
    assert corpo["itens"][0]["valor"] == 25.0
    assert corpo["itens"][0]["situacao"] == "valida"


def test_mestre_recebe_403_ao_consultar_historico_da_serie_pela_rota(
    cliente,
    sessao,
    criar_chave,
    criar_persona,
    criar_comunidade,
    criar_sessao_de_teste,
    criar_trilha,
    criar_missao,
    criar_tipo_de_coleta,
    criar_desafio_de_coleta,
    criar_local,
    criar_poder_do_territorio,
):
    chave, token, guerreiro, desafio, local = _preparar_serie_pela_rota(
        sessao,
        criar_chave,
        criar_persona,
        criar_comunidade,
        criar_sessao_de_teste,
        criar_trilha,
        criar_missao,
        criar_tipo_de_coleta,
        criar_desafio_de_coleta,
        criar_local,
        criar_poder_do_territorio,
    )
    headers = {"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"}
    resposta_serie = cliente.post(
        "/v1/series-de-coleta",
        json={"desafio_de_coleta_id": str(desafio.id), "local_id": str(local.id)},
        headers=headers,
    )
    serie_id = resposta_serie.json()["id"]
    mestre = criar_persona(Papel.mestre)
    token_mestre, _ = criar_sessao_de_teste(mestre)

    resposta = cliente.get(
        f"/v1/series-de-coleta/{serie_id}/registros",
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token_mestre}"},
    )

    assert resposta.status_code == 403


def test_guerreiro_consulta_desafios_disponiveis_pela_rota(
    cliente,
    sessao,
    criar_chave,
    criar_persona,
    criar_comunidade,
    criar_sessao_de_teste,
    criar_trilha,
    criar_missao,
    criar_tipo_de_coleta,
    criar_desafio_de_coleta,
    criar_local,
    criar_poder_do_territorio,
):
    chave, token, guerreiro, desafio, local = _preparar_serie_pela_rota(
        sessao,
        criar_chave,
        criar_persona,
        criar_comunidade,
        criar_sessao_de_teste,
        criar_trilha,
        criar_missao,
        criar_tipo_de_coleta,
        criar_desafio_de_coleta,
        criar_local,
        criar_poder_do_territorio,
    )
    headers = {"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"}

    resposta = cliente.get("/v1/desafios-de-coleta/disponiveis", headers=headers)

    assert resposta.status_code == 200
    corpo = resposta.json()
    assert [item["id"] for item in corpo["itens"]] == [str(desafio.id)]


def test_mestre_recebe_403_ao_consultar_desafios_disponiveis_pela_rota(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste
):
    chave, _ = criar_chave()
    mestre = criar_persona(Papel.mestre)
    token, _ = criar_sessao_de_teste(mestre)

    resposta = cliente.get(
        "/v1/desafios-de-coleta/disponiveis",
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
    )

    assert resposta.status_code == 403
