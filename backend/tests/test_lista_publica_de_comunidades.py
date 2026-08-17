from datetime import UTC, datetime, timedelta

import pytest
from sqlalchemy import text

from nucleo.coletas.modelo import Cadencia
from nucleo.coletas.regra import (
    contar_periodos_vencidos,
    contar_periodos_vencidos_com_registro_valido,
    periodo_de_cadencia,
)
from nucleo.locais.modelo import NivelDoLocal
from nucleo.personas.modelo import Papel
from nucleo.tempo import agora

MOMENTO = datetime(2026, 6, 1, 12, 0, tzinfo=UTC)


def _ancora_ha_n_periodos_completos(referencia: datetime, cadencia: Cadencia, n: int) -> datetime:
    """Um instante dentro do período que está `n` períodos completos antes
    do período de `referencia`, andando pelas bordas de `periodo_de_cadencia`
    — a mesma régua de `test_serie_de_coleta.py` (design — a régua dos
    períodos)."""
    limite = referencia
    for _ in range(n):
        inicio_do_periodo, _ = periodo_de_cadencia(limite, cadencia)
        limite = inicio_do_periodo - timedelta(microseconds=1)
    return limite


def _preparar_desafio(
    criar_persona,
    criar_trilha,
    criar_missao,
    criar_tipo_de_coleta,
    criar_desafio_de_coleta,
    **kwargs,
):
    mestre = criar_persona(Papel.mestre)
    trilha = criar_trilha(mestre)
    missao = criar_missao(trilha, mestre)
    tipo = criar_tipo_de_coleta(mestre)
    return criar_desafio_de_coleta(missao, mestre, tipo=tipo, **kwargs)


def _criar_bairro(criar_local, comunidade):
    """Um local de nível bairro exige um pai — a raiz de nível comunidade
    (`ck_local_pai_so_vazio_no_nivel_comunidade`)."""
    raiz = criar_local(comunidade, nivel=NivelDoLocal.comunidade, rotulo="Comunidade")
    return criar_local(comunidade, nivel=NivelDoLocal.bairro, rotulo="Bairro", local_pai=raiz)


# --- 1. Períodos de cadência da série (unidade, sem passar pela rota) ---


def test_serie_sem_periodo_vencido_devolve_zero(
    sessao,
    criar_persona,
    criar_comunidade,
    criar_local,
    criar_trilha,
    criar_missao,
    criar_tipo_de_coleta,
    criar_desafio_de_coleta,
    criar_serie_de_coleta,
):
    """1.3: série recém-aberta ainda não tem período vencido."""
    comunidade = criar_comunidade()
    local = _criar_bairro(criar_local, comunidade)
    desafio = _preparar_desafio(
        criar_persona, criar_trilha, criar_missao, criar_tipo_de_coleta, criar_desafio_de_coleta
    )
    guerreiro = criar_persona(Papel.guerreiro, comunidade=comunidade)
    serie = criar_serie_de_coleta(guerreiro, desafio, local, cadencia=Cadencia.semanal)

    agora_do_teste = agora()
    assert contar_periodos_vencidos(serie, agora_do_teste) == 0
    assert contar_periodos_vencidos_com_registro_valido(sessao, serie, agora_do_teste) == 0


def test_serie_com_todos_os_periodos_cumpridos(
    sessao,
    criar_persona,
    criar_comunidade,
    criar_local,
    criar_trilha,
    criar_missao,
    criar_tipo_de_coleta,
    criar_desafio_de_coleta,
    criar_serie_de_coleta,
    criar_registro_de_coleta,
):
    """1.3: registro válido em cada um dos períodos vencidos."""
    comunidade = criar_comunidade()
    local = _criar_bairro(criar_local, comunidade)
    desafio = _preparar_desafio(
        criar_persona, criar_trilha, criar_missao, criar_tipo_de_coleta, criar_desafio_de_coleta
    )
    guerreiro = criar_persona(Papel.guerreiro, comunidade=comunidade)
    serie = criar_serie_de_coleta(guerreiro, desafio, local, cadencia=Cadencia.diaria)
    agora_do_teste = agora()
    serie.aberta_em = _ancora_ha_n_periodos_completos(agora_do_teste, Cadencia.diaria, 3)
    sessao.commit()

    momento = serie.aberta_em
    for _ in range(3):
        criar_registro_de_coleta(serie, guerreiro, comunidade.id, momento_do_fato=momento)
        _, momento = periodo_de_cadencia(momento, Cadencia.diaria)

    assert contar_periodos_vencidos(serie, agora_do_teste) == 3
    assert contar_periodos_vencidos_com_registro_valido(sessao, serie, agora_do_teste) == 3


def test_serie_com_periodo_vencido_sem_registro(
    sessao,
    criar_persona,
    criar_comunidade,
    criar_local,
    criar_trilha,
    criar_missao,
    criar_tipo_de_coleta,
    criar_desafio_de_coleta,
    criar_serie_de_coleta,
):
    """1.3: período vencido sem nenhum registro válido."""
    comunidade = criar_comunidade()
    local = _criar_bairro(criar_local, comunidade)
    desafio = _preparar_desafio(
        criar_persona, criar_trilha, criar_missao, criar_tipo_de_coleta, criar_desafio_de_coleta
    )
    guerreiro = criar_persona(Papel.guerreiro, comunidade=comunidade)
    serie = criar_serie_de_coleta(guerreiro, desafio, local, cadencia=Cadencia.diaria)
    agora_do_teste = agora()
    serie.aberta_em = _ancora_ha_n_periodos_completos(agora_do_teste, Cadencia.diaria, 2)
    sessao.commit()

    assert contar_periodos_vencidos(serie, agora_do_teste) == 2
    assert contar_periodos_vencidos_com_registro_valido(sessao, serie, agora_do_teste) == 0


# --- 2, 3 e 4: a rota pública ---


def test_lista_de_comunidades_sem_chave_e_recusada_com_401(cliente):
    resposta = cliente.get("/v1/comunidades")
    assert resposta.status_code == 401


def test_lista_de_comunidades_responde_sem_token_de_sessao(cliente, criar_chave, criar_comunidade):
    criar_comunidade()
    chave, _ = criar_chave()
    resposta = cliente.get("/v1/comunidades", headers={"X-Chave-Aplicacao": chave})
    assert resposta.status_code == 200


def test_lista_de_comunidades_parametro_nao_declarado_e_recusado_com_422(cliente, criar_chave):
    chave, _ = criar_chave()
    resposta = cliente.get(
        "/v1/comunidades",
        params={"nao_declarado": "x"},
        headers={"X-Chave-Aplicacao": chave},
    )
    assert resposta.status_code == 422


def test_lista_de_comunidades_declara_o_rotulo_do_ciclo_corrente(
    cliente, criar_chave, criar_comunidade, configuracao
):
    criar_comunidade()
    chave, _ = criar_chave()
    resposta = cliente.get("/v1/comunidades", headers={"X-Chave-Aplicacao": chave})
    assert resposta.status_code == 200
    assert resposta.json()["ciclo_rotulo"] == configuracao.ciclo_rotulo


def test_lista_de_comunidades_comunidade_recem_criada_sai_zerada(
    cliente, criar_chave, criar_comunidade, sobrescrever_configuracao
):
    """2.5: sem piso na jogada, a comunidade vazia sai com as três contagens
    em zero e a continuidade nula (`RF-08-30`)."""
    comunidade = criar_comunidade()
    sobrescrever_configuracao(territorio_piso_de_coletores_distintos=0)
    chave, _ = criar_chave()

    resposta = cliente.get("/v1/comunidades", headers={"X-Chave-Aplicacao": chave})
    assert resposta.status_code == 200
    item = next(i for i in resposta.json()["itens"] if i["id"] == str(comunidade.id))
    assert item["series_abertas"] == 0
    assert item["series_ativas"] == 0
    assert item["registros_validos"] == 0
    assert item["continuidade"] is None


def test_lista_de_comunidades_sem_coletor_algum_sai_sem_indicadores(
    cliente, criar_chave, criar_comunidade
):
    """3.4: comunidade sem coletor algum, abaixo do piso padrão."""
    comunidade = criar_comunidade()
    chave, _ = criar_chave()

    resposta = cliente.get("/v1/comunidades", headers={"X-Chave-Aplicacao": chave})
    assert resposta.status_code == 200
    item = next(i for i in resposta.json()["itens"] if i["id"] == str(comunidade.id))
    assert item["nome"] == comunidade.nome
    assert item["localizacao"] == comunidade.localizacao
    assert item["series_abertas"] is None
    assert item["series_ativas"] is None
    assert item["registros_validos"] is None
    assert item["continuidade"] is None


def test_lista_de_comunidades_abaixo_do_piso_sai_sem_indicadores(
    cliente,
    criar_chave,
    criar_comunidade,
    criar_local,
    criar_persona,
    criar_trilha,
    criar_missao,
    criar_tipo_de_coleta,
    criar_desafio_de_coleta,
    criar_serie_de_coleta,
    criar_registro_de_coleta,
):
    """3.4: comunidade com dois coletores e piso três — os quatro
    indicadores saem nulos, sem subconjunto que escape (`RF-08-31`,
    `RN-08-28`)."""
    comunidade = criar_comunidade()
    local = _criar_bairro(criar_local, comunidade)
    desafio = _preparar_desafio(
        criar_persona, criar_trilha, criar_missao, criar_tipo_de_coleta, criar_desafio_de_coleta
    )
    for _ in range(2):
        guerreiro = criar_persona(Papel.guerreiro, comunidade=comunidade)
        serie = criar_serie_de_coleta(guerreiro, desafio, local)
        criar_registro_de_coleta(serie, guerreiro, comunidade.id, momento_do_fato=MOMENTO)

    chave, _ = criar_chave()
    resposta = cliente.get("/v1/comunidades", headers={"X-Chave-Aplicacao": chave})
    assert resposta.status_code == 200
    item = next(i for i in resposta.json()["itens"] if i["id"] == str(comunidade.id))
    assert item["series_abertas"] is None
    assert item["series_ativas"] is None
    assert item["registros_validos"] is None
    assert item["continuidade"] is None


def test_lista_de_comunidades_no_piso_sai_com_indicadores(
    cliente,
    criar_chave,
    criar_comunidade,
    criar_local,
    criar_persona,
    criar_trilha,
    criar_missao,
    criar_tipo_de_coleta,
    criar_desafio_de_coleta,
    criar_serie_de_coleta,
    criar_registro_de_coleta,
):
    """3.4: comunidade com três coletores e piso três — os quatro
    indicadores saem apurados (`RF-08-31`, `RN-08-28`)."""
    comunidade = criar_comunidade()
    local = _criar_bairro(criar_local, comunidade)
    desafio = _preparar_desafio(
        criar_persona, criar_trilha, criar_missao, criar_tipo_de_coleta, criar_desafio_de_coleta
    )
    for _ in range(3):
        guerreiro = criar_persona(Papel.guerreiro, comunidade=comunidade)
        serie = criar_serie_de_coleta(guerreiro, desafio, local)
        criar_registro_de_coleta(serie, guerreiro, comunidade.id, momento_do_fato=MOMENTO)

    chave, _ = criar_chave()
    resposta = cliente.get("/v1/comunidades", headers={"X-Chave-Aplicacao": chave})
    assert resposta.status_code == 200
    item = next(i for i in resposta.json()["itens"] if i["id"] == str(comunidade.id))
    assert item["series_abertas"] == 3
    assert item["registros_validos"] == 3


def test_lista_de_comunidades_nao_identifica_coletor(
    cliente,
    criar_chave,
    criar_comunidade,
    criar_local,
    criar_persona,
    criar_trilha,
    criar_missao,
    criar_tipo_de_coleta,
    criar_desafio_de_coleta,
    criar_serie_de_coleta,
    criar_registro_de_coleta,
):
    """4.6 / 3.3: nenhum campo da resposta identifica coletor, e a contagem
    de coletores distintos que decide o piso não sai na resposta
    (`RN-08-12`)."""
    comunidade = criar_comunidade()
    local = _criar_bairro(criar_local, comunidade)
    desafio = _preparar_desafio(
        criar_persona, criar_trilha, criar_missao, criar_tipo_de_coleta, criar_desafio_de_coleta
    )
    guerreiros_ids = []
    for _ in range(3):
        guerreiro = criar_persona(Papel.guerreiro, comunidade=comunidade)
        serie = criar_serie_de_coleta(guerreiro, desafio, local)
        criar_registro_de_coleta(serie, guerreiro, comunidade.id, momento_do_fato=MOMENTO)
        guerreiros_ids.append(str(guerreiro.id))

    chave, _ = criar_chave()
    resposta = cliente.get("/v1/comunidades", headers={"X-Chave-Aplicacao": chave})
    assert resposta.status_code == 200
    corpo = resposta.text
    for guerreiro_id in guerreiros_ids:
        assert guerreiro_id not in corpo

    campos_esperados = {
        "id",
        "nome",
        "localizacao",
        "series_abertas",
        "series_ativas",
        "registros_validos",
        "continuidade",
    }
    for item in resposta.json()["itens"]:
        assert set(item.keys()) == campos_esperados


def test_lista_de_comunidades_series_ativas_no_instante_da_consulta(
    sessao,
    cliente,
    criar_chave,
    criar_comunidade,
    criar_local,
    criar_persona,
    criar_trilha,
    criar_missao,
    criar_tipo_de_coleta,
    criar_desafio_de_coleta,
    criar_serie_de_coleta,
    criar_registro_de_coleta,
):
    """2.1/2.2: séries abertas conta as três, qualquer que seja o estado;
    séries ativas só conta as apuradas como ativas no instante da consulta
    (`RF-08-30`, `RN-08-29`)."""
    comunidade = criar_comunidade()
    local = _criar_bairro(criar_local, comunidade)
    desafio = _preparar_desafio(
        criar_persona,
        criar_trilha,
        criar_missao,
        criar_tipo_de_coleta,
        criar_desafio_de_coleta,
        cadencia=Cadencia.diaria,
    )
    guerreiros = [criar_persona(Papel.guerreiro, comunidade=comunidade) for _ in range(3)]
    agora_do_teste = agora()

    serie_ativa = criar_serie_de_coleta(guerreiros[0], desafio, local, cadencia=Cadencia.diaria)
    criar_registro_de_coleta(
        serie_ativa, guerreiros[0], comunidade.id, momento_do_fato=agora_do_teste
    )

    serie_interrompida = criar_serie_de_coleta(
        guerreiros[1], desafio, local, cadencia=Cadencia.diaria
    )
    serie_interrompida.aberta_em = _ancora_ha_n_periodos_completos(
        agora_do_teste, Cadencia.diaria, 2
    )
    sessao.commit()
    criar_registro_de_coleta(
        serie_interrompida,
        guerreiros[1],
        comunidade.id,
        momento_do_fato=serie_interrompida.aberta_em,
    )

    serie_extra = criar_serie_de_coleta(guerreiros[2], desafio, local, cadencia=Cadencia.diaria)
    criar_registro_de_coleta(
        serie_extra, guerreiros[2], comunidade.id, momento_do_fato=agora_do_teste
    )

    chave, _ = criar_chave()
    resposta = cliente.get("/v1/comunidades", headers={"X-Chave-Aplicacao": chave})
    assert resposta.status_code == 200
    item = next(i for i in resposta.json()["itens"] if i["id"] == str(comunidade.id))
    assert item["series_abertas"] == 3
    assert item["series_ativas"] == 2


def test_lista_de_comunidades_continuidade_e_a_media_dos_periodos_vencidos(
    sessao,
    cliente,
    criar_chave,
    criar_comunidade,
    criar_local,
    criar_persona,
    criar_trilha,
    criar_missao,
    criar_tipo_de_coleta,
    criar_desafio_de_coleta,
    criar_serie_de_coleta,
    criar_registro_de_coleta,
):
    """2.4: a continuidade é a média entre as séries com ao menos um período
    vencido — a série sem período vencido fica fora da média (`RN-08-29`,
    design — Decisions 2)."""
    comunidade = criar_comunidade()
    local = _criar_bairro(criar_local, comunidade)
    desafio = _preparar_desafio(
        criar_persona, criar_trilha, criar_missao, criar_tipo_de_coleta, criar_desafio_de_coleta
    )
    agora_do_teste = agora()

    # série A: 4 períodos vencidos, 3 com registro válido -> 0,75
    guerreiro_a = criar_persona(Papel.guerreiro, comunidade=comunidade)
    serie_a = criar_serie_de_coleta(guerreiro_a, desafio, local, cadencia=Cadencia.diaria)
    serie_a.aberta_em = _ancora_ha_n_periodos_completos(agora_do_teste, Cadencia.diaria, 4)
    sessao.commit()
    momento = serie_a.aberta_em
    for _ in range(3):
        criar_registro_de_coleta(serie_a, guerreiro_a, comunidade.id, momento_do_fato=momento)
        _, momento = periodo_de_cadencia(momento, Cadencia.diaria)

    # série C: 2 períodos vencidos, os 2 com registro válido -> 1,0
    guerreiro_c = criar_persona(Papel.guerreiro, comunidade=comunidade)
    serie_c = criar_serie_de_coleta(guerreiro_c, desafio, local, cadencia=Cadencia.diaria)
    serie_c.aberta_em = _ancora_ha_n_periodos_completos(agora_do_teste, Cadencia.diaria, 2)
    sessao.commit()
    momento = serie_c.aberta_em
    for _ in range(2):
        criar_registro_de_coleta(serie_c, guerreiro_c, comunidade.id, momento_do_fato=momento)
        _, momento = periodo_de_cadencia(momento, Cadencia.diaria)

    # série D: recém-aberta, sem período vencido — fora da média, só para
    # alcançar o piso de coletores distintos
    guerreiro_d = criar_persona(Papel.guerreiro, comunidade=comunidade)
    serie_d = criar_serie_de_coleta(guerreiro_d, desafio, local)
    criar_registro_de_coleta(serie_d, guerreiro_d, comunidade.id, momento_do_fato=agora_do_teste)

    chave, _ = criar_chave()
    resposta = cliente.get("/v1/comunidades", headers={"X-Chave-Aplicacao": chave})
    assert resposta.status_code == 200
    item = next(i for i in resposta.json()["itens"] if i["id"] == str(comunidade.id))
    assert item["continuidade"] == pytest.approx(0.875)


def test_lista_de_comunidades_registro_invalidado_sai_das_duas_apuracoes(
    sessao,
    cliente,
    criar_chave,
    criar_comunidade,
    criar_local,
    criar_persona,
    criar_trilha,
    criar_missao,
    criar_tipo_de_coleta,
    criar_desafio_de_coleta,
    criar_serie_de_coleta,
    criar_registro_de_coleta,
):
    """Registro invalidado sai da contagem de registros válidos e o período
    dele volta a contar como período sem registro na continuidade
    (`RN-08-09`). Quatro coletores distintos — um a mais que o piso — para
    que a invalidação de um deles não derrube a comunidade abaixo do piso
    e confunda este cenário com o de `RF-08-31`.
    """
    comunidade = criar_comunidade()
    local = _criar_bairro(criar_local, comunidade)
    desafio = _preparar_desafio(
        criar_persona, criar_trilha, criar_missao, criar_tipo_de_coleta, criar_desafio_de_coleta
    )
    guerreiros = [criar_persona(Papel.guerreiro, comunidade=comunidade) for _ in range(4)]
    series = [
        criar_serie_de_coleta(guerreiro, desafio, local, cadencia=Cadencia.diaria)
        for guerreiro in guerreiros
    ]
    agora_do_teste = agora()
    for serie in series:
        serie.aberta_em = _ancora_ha_n_periodos_completos(agora_do_teste, Cadencia.diaria, 1)
    sessao.commit()

    registros = [
        criar_registro_de_coleta(serie, guerreiro, comunidade.id, momento_do_fato=serie.aberta_em)
        for serie, guerreiro in zip(series, guerreiros, strict=True)
    ]

    sessao.execute(
        text("UPDATE registro_de_coleta SET situacao = 'invalidada' WHERE id = :id"),
        {"id": str(registros[0].id)},
    )
    sessao.commit()

    chave, _ = criar_chave()
    resposta = cliente.get("/v1/comunidades", headers={"X-Chave-Aplicacao": chave})
    assert resposta.status_code == 200
    item = next(i for i in resposta.json()["itens"] if i["id"] == str(comunidade.id))
    assert item["registros_validos"] == 3
    assert item["continuidade"] == pytest.approx(0.75)


def test_lista_de_comunidades_supressao_nao_depende_da_pagina(
    cliente,
    criar_chave,
    criar_comunidade,
    criar_local,
    criar_persona,
    criar_trilha,
    criar_missao,
    criar_tipo_de_coleta,
    criar_desafio_de_coleta,
    criar_serie_de_coleta,
    criar_registro_de_coleta,
):
    """4.3/4.5: o piso é aplicado antes do corte de página — a comunidade
    abaixo do piso sai sem indicadores na segunda página, exatamente como
    sairia na primeira (`RF-08-31`)."""
    comunidade_acima = criar_comunidade("AAA Comunidade")
    comunidade_abaixo = criar_comunidade("BBB Comunidade")
    local_acima = _criar_bairro(criar_local, comunidade_acima)
    local_abaixo = _criar_bairro(criar_local, comunidade_abaixo)
    desafio = _preparar_desafio(
        criar_persona, criar_trilha, criar_missao, criar_tipo_de_coleta, criar_desafio_de_coleta
    )
    for _ in range(3):
        guerreiro = criar_persona(Papel.guerreiro, comunidade=comunidade_acima)
        serie = criar_serie_de_coleta(guerreiro, desafio, local_acima)
        criar_registro_de_coleta(serie, guerreiro, comunidade_acima.id, momento_do_fato=MOMENTO)
    for _ in range(2):
        guerreiro = criar_persona(Papel.guerreiro, comunidade=comunidade_abaixo)
        serie = criar_serie_de_coleta(guerreiro, desafio, local_abaixo)
        criar_registro_de_coleta(serie, guerreiro, comunidade_abaixo.id, momento_do_fato=MOMENTO)

    chave, _ = criar_chave()
    headers = {"X-Chave-Aplicacao": chave}

    primeira_pagina = cliente.get("/v1/comunidades", params={"tamanho": "1"}, headers=headers)
    assert primeira_pagina.status_code == 200
    corpo_primeira = primeira_pagina.json()
    assert corpo_primeira["itens"][0]["nome"] == "AAA Comunidade"
    assert corpo_primeira["itens"][0]["series_abertas"] == 3
    assert corpo_primeira["proximo_cursor"] is not None

    segunda_pagina = cliente.get(
        "/v1/comunidades",
        params={"tamanho": "1", "cursor": corpo_primeira["proximo_cursor"]},
        headers=headers,
    )
    assert segunda_pagina.status_code == 200
    corpo_segunda = segunda_pagina.json()
    assert corpo_segunda["itens"][0]["nome"] == "BBB Comunidade"
    assert corpo_segunda["itens"][0]["series_abertas"] is None
    assert corpo_segunda["itens"][0]["continuidade"] is None
