from datetime import UTC, datetime, timedelta

from nucleo.personas.modelo import Papel


def test_admin_consulta_a_trilha(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste, criar_registro_de_auditoria
):
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    token, _ = criar_sessao_de_teste(admin)
    criar_registro_de_auditoria(admin, acao="POST cadastrar_responsavel_rota")

    resposta = cliente.get(
        "/v1/auditoria", headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"}
    )
    assert resposta.status_code == 200
    corpo = resposta.json()
    assert len(corpo["itens"]) == 1
    assert corpo["itens"][0]["acao"] == "POST cadastrar_responsavel_rota"
    assert corpo["itens"][0]["autor_id"] == str(admin.id)


def test_persona_sem_papel_admin_recebe_recusa_por_permissao(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste
):
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    mestre = criar_persona(Papel.mestre, criada_por=admin)
    token, _ = criar_sessao_de_teste(mestre)

    resposta = cliente.get(
        "/v1/auditoria", headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"}
    )
    assert resposta.status_code == 403
    assert resposta.json()["codigo"] == "permissao_negada"


def test_consulta_sem_chave_e_401(cliente, criar_persona, criar_sessao_de_teste):
    admin = criar_persona(Papel.admin)
    token, _ = criar_sessao_de_teste(admin)

    resposta = cliente.get("/v1/auditoria", headers={"Authorization": f"Bearer {token}"})
    assert resposta.status_code == 401
    assert resposta.json()["codigo"] == "chave_invalida"


def test_parametro_desconhecido_e_recusado_nomeando_o_parametro(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste
):
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    token, _ = criar_sessao_de_teste(admin)

    resposta = cliente.get(
        "/v1/auditoria",
        params={"tema": "qualquer"},
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
    )
    assert resposta.status_code == 422
    corpo = resposta.json()
    assert corpo["codigo"] == "parametro_desconhecido"
    assert corpo["campo"] == "tema"


def test_consulta_filtra_por_periodo_e_persona(
    cliente,
    criar_chave,
    criar_persona,
    criar_sessao_de_teste,
    criar_registro_de_auditoria,
):
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    mestre = criar_persona(Papel.mestre, criada_por=admin)
    token, _ = criar_sessao_de_teste(admin)

    agora = datetime.now(UTC)
    dentro_do_periodo = criar_registro_de_auditoria(
        admin, acao="POST a", entidade_afetada="a", momento=agora
    )
    criar_registro_de_auditoria(
        mestre, acao="POST b", entidade_afetada="b", momento=agora - timedelta(days=10)
    )
    criar_registro_de_auditoria(mestre, acao="POST c", entidade_afetada="c", momento=agora)

    resposta = cliente.get(
        "/v1/auditoria",
        params={
            "periodo_inicio": (agora - timedelta(hours=1)).isoformat(),
            "periodo_fim": (agora + timedelta(hours=1)).isoformat(),
            "persona": str(admin.id),
        },
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
    )
    assert resposta.status_code == 200
    corpo = resposta.json()
    assert len(corpo["itens"]) == 1
    assert corpo["itens"][0]["id"] == str(dentro_do_periodo.id)


def test_consulta_filtra_por_acao_e_entidade_afetada(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste, criar_registro_de_auditoria
):
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    token, _ = criar_sessao_de_teste(admin)
    criar_registro_de_auditoria(admin, acao="POST cadastrar_responsavel_rota", entidade_afetada="a")
    criar_registro_de_auditoria(admin, acao="POST criar_vinculo_rota", entidade_afetada="b")

    resposta = cliente.get(
        "/v1/auditoria",
        params={"entidade_afetada": "b"},
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
    )
    assert resposta.status_code == 200
    corpo = resposta.json()
    assert len(corpo["itens"]) == 1
    assert corpo["itens"][0]["acao"] == "POST criar_vinculo_rota"

    resposta_por_acao = cliente.get(
        "/v1/auditoria",
        params={"acao": "POST cadastrar_responsavel_rota"},
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
    )
    assert resposta_por_acao.status_code == 200
    corpo_por_acao = resposta_por_acao.json()
    assert len(corpo_por_acao["itens"]) == 1
    assert corpo_por_acao["itens"][0]["entidade_afetada"] == "a"


def test_consulta_pagina_pelo_tamanho_informado(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste, criar_registro_de_auditoria
):
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    token, _ = criar_sessao_de_teste(admin)
    for indice in range(3):
        criar_registro_de_auditoria(admin, acao=f"POST acao_{indice}", entidade_afetada="x")

    resposta = cliente.get(
        "/v1/auditoria",
        params={"tamanho": "2"},
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
    )
    assert resposta.status_code == 200
    primeira_pagina = resposta.json()
    assert len(primeira_pagina["itens"]) == 2
    assert primeira_pagina["proximo_cursor"] is not None

    resposta_seguinte = cliente.get(
        "/v1/auditoria",
        params={"tamanho": "2", "cursor": primeira_pagina["proximo_cursor"]},
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
    )
    assert resposta_seguinte.status_code == 200
    segunda_pagina = resposta_seguinte.json()
    assert len(segunda_pagina["itens"]) == 1
    assert segunda_pagina["proximo_cursor"] is None

    ids_da_primeira = {item["id"] for item in primeira_pagina["itens"]}
    ids_da_segunda = {item["id"] for item in segunda_pagina["itens"]}
    assert ids_da_primeira.isdisjoint(ids_da_segunda)


def test_filtro_de_periodo_sem_fuso_e_recusado(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste
):
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    token, _ = criar_sessao_de_teste(admin)

    resposta = cliente.get(
        "/v1/auditoria",
        params={"periodo_inicio": "2026-08-01T10:00:00"},
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
    )
    assert resposta.status_code == 422
    corpo = resposta.json()
    assert corpo["codigo"] == "erro_de_validacao"
    assert corpo["campo"] == "periodo_inicio"


def test_filtro_de_periodo_mal_formado_e_recusado(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste
):
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    token, _ = criar_sessao_de_teste(admin)

    resposta = cliente.get(
        "/v1/auditoria",
        params={"periodo_fim": "não é uma data"},
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
    )
    assert resposta.status_code == 422
    corpo = resposta.json()
    assert corpo["codigo"] == "erro_de_validacao"
    assert corpo["campo"] == "periodo_fim"


def test_filtro_de_persona_mal_formado_e_recusado(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste
):
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    token, _ = criar_sessao_de_teste(admin)

    resposta = cliente.get(
        "/v1/auditoria",
        params={"persona": "não é um uuid"},
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
    )
    assert resposta.status_code == 422
    corpo = resposta.json()
    assert corpo["codigo"] == "erro_de_validacao"
    assert corpo["campo"] == "persona"


def test_cursor_invalido_e_recusado(cliente, criar_chave, criar_persona, criar_sessao_de_teste):
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    token, _ = criar_sessao_de_teste(admin)

    resposta = cliente.get(
        "/v1/auditoria",
        params={"cursor": "cursor-invalido"},
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
    )
    assert resposta.status_code == 422
    assert resposta.json()["codigo"] == "erro_de_validacao"


def test_cursor_bem_formado_mas_com_forma_errada_e_recusado(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste
):
    from nucleo.paginacao import codificar_cursor

    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    token, _ = criar_sessao_de_teste(admin)
    cursor = codificar_cursor({"algo": "inesperado"})

    resposta = cliente.get(
        "/v1/auditoria",
        params={"cursor": cursor},
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
    )
    assert resposta.status_code == 422
    corpo = resposta.json()
    assert corpo["codigo"] == "erro_de_validacao"
    assert corpo["campo"] == "cursor"


def test_trilha_nao_traz_escrita_anterior_a_existencia_do_middleware(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste
):
    """A trilha só existe a partir de quando o middleware sobe (design.md —
    Non-Goals): uma persona criada fora dela (sem passar pela API) não gera
    registro — confirmado por ausência, não reconstruindo nada."""
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    criar_persona(Papel.responsavel, criada_por=admin)  # escrita "anterior", direto no banco
    token, _ = criar_sessao_de_teste(admin)

    resposta = cliente.get(
        "/v1/auditoria", headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"}
    )
    assert resposta.status_code == 200
    assert resposta.json()["itens"] == []
