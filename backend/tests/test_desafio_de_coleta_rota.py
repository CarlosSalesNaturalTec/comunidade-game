from nucleo.coletas.modelo import EstadoDaSerie
from nucleo.personas.modelo import Papel
from nucleo.trilhas.modelo import SituacaoDaTrilha


def test_admin_le_desafio_publicado_com_cadencia_vigencia_e_series_ativas(
    cliente,
    criar_chave,
    criar_persona,
    criar_sessao_de_teste,
    criar_trilha,
    criar_missao,
    criar_desafio_de_coleta,
    criar_local,
    criar_comunidade,
    criar_serie_de_coleta,
):
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    mestre = criar_persona(Papel.mestre, criada_por=admin)
    trilha = criar_trilha(mestre, situacao=SituacaoDaTrilha.publicada)
    missao = criar_missao(trilha, mestre)
    desafio = criar_desafio_de_coleta(missao, mestre)
    comunidade = criar_comunidade()
    local = criar_local(comunidade)
    guerreiro = criar_persona(Papel.guerreiro, comunidade=comunidade)
    criar_serie_de_coleta(guerreiro, desafio, local)
    token, _ = criar_sessao_de_teste(admin)

    resposta = cliente.get(
        "/v1/desafios-de-coleta",
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
    )
    assert resposta.status_code == 200
    item = next(i for i in resposta.json()["itens"] if i["id"] == str(desafio.id))
    assert item["cadencia"] == desafio.cadencia.value
    assert item["granularidade_exigida"] == desafio.granularidade_exigida.value
    assert item["tipo_de_coleta"]["nome"]
    assert item["quantidade_de_series_ativas"] == 1


def test_desafio_de_trilha_em_rascunho_fica_de_fora(
    cliente,
    criar_chave,
    criar_persona,
    criar_sessao_de_teste,
    criar_trilha,
    criar_missao,
    criar_desafio_de_coleta,
):
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    mestre = criar_persona(Papel.mestre, criada_por=admin)

    trilha_publicada = criar_trilha(mestre, nome="Publicada", situacao=SituacaoDaTrilha.publicada)
    missao_publicada = criar_missao(trilha_publicada, mestre)
    desafio_publicado = criar_desafio_de_coleta(missao_publicada, mestre)

    trilha_rascunho = criar_trilha(mestre, nome="Rascunho", situacao=SituacaoDaTrilha.rascunho)
    missao_rascunho = criar_missao(trilha_rascunho, mestre, titulo="Missão do rascunho")
    desafio_rascunho = criar_desafio_de_coleta(missao_rascunho, mestre)

    token, _ = criar_sessao_de_teste(admin)

    resposta = cliente.get(
        "/v1/desafios-de-coleta",
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
    )
    assert resposta.status_code == 200
    ids = {item["id"] for item in resposta.json()["itens"]}
    assert str(desafio_publicado.id) in ids
    assert str(desafio_rascunho.id) not in ids


def test_so_a_serie_ativa_e_contada(
    cliente,
    criar_chave,
    criar_persona,
    criar_sessao_de_teste,
    criar_trilha,
    criar_missao,
    criar_desafio_de_coleta,
    criar_local,
    criar_comunidade,
    criar_serie_de_coleta,
):
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    mestre = criar_persona(Papel.mestre, criada_por=admin)
    trilha = criar_trilha(mestre, situacao=SituacaoDaTrilha.publicada)
    missao = criar_missao(trilha, mestre)
    desafio = criar_desafio_de_coleta(missao, mestre)
    comunidade = criar_comunidade()
    local = criar_local(comunidade)

    guerreiro_ativo = criar_persona(Papel.guerreiro, comunidade=comunidade)
    guerreiro_interrompido = criar_persona(Papel.guerreiro, comunidade=comunidade)
    guerreiro_encerrado = criar_persona(Papel.guerreiro, comunidade=comunidade)
    criar_serie_de_coleta(guerreiro_ativo, desafio, local, estado=EstadoDaSerie.ativa)
    criar_serie_de_coleta(guerreiro_interrompido, desafio, local, estado=EstadoDaSerie.interrompida)
    criar_serie_de_coleta(guerreiro_encerrado, desafio, local, estado=EstadoDaSerie.encerrada)

    token, _ = criar_sessao_de_teste(admin)

    resposta = cliente.get(
        "/v1/desafios-de-coleta",
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
    )
    assert resposta.status_code == 200
    item = next(i for i in resposta.json()["itens"] if i["id"] == str(desafio.id))
    assert item["quantidade_de_series_ativas"] == 1


def test_desafio_sem_serie_sai_com_zero(
    cliente,
    criar_chave,
    criar_persona,
    criar_sessao_de_teste,
    criar_trilha,
    criar_missao,
    criar_desafio_de_coleta,
):
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    mestre = criar_persona(Papel.mestre, criada_por=admin)
    trilha = criar_trilha(mestre, situacao=SituacaoDaTrilha.publicada)
    missao = criar_missao(trilha, mestre)
    desafio = criar_desafio_de_coleta(missao, mestre)
    token, _ = criar_sessao_de_teste(admin)

    resposta = cliente.get(
        "/v1/desafios-de-coleta",
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
    )
    assert resposta.status_code == 200
    item = next(i for i in resposta.json()["itens"] if i["id"] == str(desafio.id))
    assert item["quantidade_de_series_ativas"] == 0


def test_paginacao_dos_desafios_publicados(
    cliente,
    criar_chave,
    criar_persona,
    criar_sessao_de_teste,
    criar_trilha,
    criar_missao,
    criar_desafio_de_coleta,
):
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    mestre = criar_persona(Papel.mestre, criada_por=admin)
    trilha = criar_trilha(mestre, situacao=SituacaoDaTrilha.publicada)
    for indice in range(3):
        missao = criar_missao(trilha, mestre, titulo=f"Missão {indice}", posicao=indice + 1)
        criar_desafio_de_coleta(missao, mestre)
    token, _ = criar_sessao_de_teste(admin)
    cabecalhos = {"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"}

    primeira_pagina = cliente.get("/v1/desafios-de-coleta?tamanho=2", headers=cabecalhos).json()
    assert len(primeira_pagina["itens"]) == 2
    assert primeira_pagina["proximo_cursor"] is not None

    segunda_pagina = cliente.get(
        f"/v1/desafios-de-coleta?tamanho=2&cursor={primeira_pagina['proximo_cursor']}",
        headers=cabecalhos,
    ).json()
    assert len(segunda_pagina["itens"]) == 1
    assert segunda_pagina["proximo_cursor"] is None


def test_recusa_com_403_quem_nao_e_admin(
    cliente,
    criar_chave,
    criar_persona,
    criar_sessao_de_teste,
    criar_trilha,
    criar_missao,
    criar_desafio_de_coleta,
):
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    mestre = criar_persona(Papel.mestre, criada_por=admin)
    trilha = criar_trilha(mestre, situacao=SituacaoDaTrilha.publicada)
    missao = criar_missao(trilha, mestre)
    criar_desafio_de_coleta(missao, mestre)

    guerreiro = criar_persona(Papel.guerreiro)
    responsavel = criar_persona(Papel.responsavel, criada_por=admin)
    apoiador = criar_persona(Papel.apoiador, criada_por=admin)

    for persona in (mestre, guerreiro, responsavel, apoiador):
        token, _ = criar_sessao_de_teste(persona)
        resposta = cliente.get(
            "/v1/desafios-de-coleta",
            headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
        )
        assert resposta.status_code == 403
