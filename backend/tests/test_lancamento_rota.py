from decimal import Decimal

from nucleo.livro_razao.regra import lancar_ajuste, lancar_credito
from nucleo.personas.modelo import Papel


def test_admin_lanca_ajuste_pela_rota(
    cliente,
    criar_chave,
    criar_persona,
    criar_sessao_de_teste,
    criar_comunidade,
    criar_ponto_de_apoio,
    criar_tipo_de_recurso,
    sessao,
):
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    token, _ = criar_sessao_de_teste(admin)
    comunidade = criar_comunidade()
    ponto_de_apoio = criar_ponto_de_apoio(admin, comunidade)
    tipo = criar_tipo_de_recurso(admin)

    credito = lancar_credito(
        sessao,
        tipo_de_recurso_id=tipo.id,
        ponto_de_apoio_id=ponto_de_apoio.id,
        quantidade=Decimal("3.00"),
        valor_em_moedas=Decimal("3.00"),
        operador=admin,
    )
    sessao.commit()

    resposta = cliente.post(
        f"/v1/lancamentos/{credito.id}/ajuste",
        json={"quantidade": "-1.00", "valor_em_moedas": "-1.00", "motivo": "Corrige a maior."},
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
    )

    assert resposta.status_code == 201
    corpo = resposta.json()
    assert corpo["natureza"] == "ajuste"
    assert corpo["lancamento_original_id"] == str(credito.id)
    assert corpo["motivo_do_ajuste"] == "Corrige a maior."


def test_mestre_nao_lanca_ajuste_pela_rota(
    cliente,
    criar_chave,
    criar_persona,
    criar_sessao_de_teste,
    criar_comunidade,
    criar_ponto_de_apoio,
    criar_tipo_de_recurso,
    sessao,
):
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    mestre = criar_persona(Papel.mestre, criada_por=admin)
    token, _ = criar_sessao_de_teste(mestre)
    comunidade = criar_comunidade()
    ponto_de_apoio = criar_ponto_de_apoio(admin, comunidade)
    tipo = criar_tipo_de_recurso(admin)

    credito = lancar_credito(
        sessao,
        tipo_de_recurso_id=tipo.id,
        ponto_de_apoio_id=ponto_de_apoio.id,
        quantidade=Decimal("3.00"),
        valor_em_moedas=Decimal("3.00"),
        operador=admin,
    )
    sessao.commit()

    resposta = cliente.post(
        f"/v1/lancamentos/{credito.id}/ajuste",
        json={"quantidade": "-1.00", "valor_em_moedas": "-1.00", "motivo": "Corrige a maior."},
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
    )

    assert resposta.status_code == 403


def test_edicao_de_lancamento_responde_405(
    cliente,
    criar_chave,
    criar_persona,
    criar_comunidade,
    criar_ponto_de_apoio,
    criar_tipo_de_recurso,
    sessao,
):
    """Não há `PUT` nem `PATCH` declarados sobre `lancamento`: o FastAPI
    responde 405 sozinho ao método não previsto no caminho existente
    (`RF-07-19`, design — Decisions 4)."""
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    comunidade = criar_comunidade()
    ponto_de_apoio = criar_ponto_de_apoio(admin, comunidade)
    tipo = criar_tipo_de_recurso(admin)

    credito = lancar_credito(
        sessao,
        tipo_de_recurso_id=tipo.id,
        ponto_de_apoio_id=ponto_de_apoio.id,
        quantidade=Decimal("3.00"),
        valor_em_moedas=Decimal("3.00"),
        operador=admin,
    )
    sessao.commit()

    resposta = cliente.put(
        f"/v1/lancamentos/{credito.id}/ajuste", headers={"X-Chave-Aplicacao": chave}
    )

    assert resposta.status_code == 405


def test_ajuste_sem_chave_e_recusado_com_401(
    cliente,
    criar_persona,
    criar_sessao_de_teste,
    criar_comunidade,
    criar_ponto_de_apoio,
    criar_tipo_de_recurso,
    sessao,
):
    admin = criar_persona(Papel.admin)
    token, _ = criar_sessao_de_teste(admin)
    comunidade = criar_comunidade()
    ponto_de_apoio = criar_ponto_de_apoio(admin, comunidade)
    tipo = criar_tipo_de_recurso(admin)

    credito = lancar_credito(
        sessao,
        tipo_de_recurso_id=tipo.id,
        ponto_de_apoio_id=ponto_de_apoio.id,
        quantidade=Decimal("3.00"),
        valor_em_moedas=Decimal("3.00"),
        operador=admin,
    )
    sessao.commit()

    resposta = cliente.post(
        f"/v1/lancamentos/{credito.id}/ajuste",
        json={"quantidade": "-1.00", "valor_em_moedas": "-1.00", "motivo": "Corrige."},
        headers={"Authorization": f"Bearer {token}"},
    )

    assert resposta.status_code == 401


def test_admin_lista_os_lancamentos_do_ponto_de_apoio(
    cliente,
    criar_chave,
    criar_persona,
    criar_sessao_de_teste,
    criar_comunidade,
    criar_ponto_de_apoio,
    criar_tipo_de_recurso,
    sessao,
):
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    token, _ = criar_sessao_de_teste(admin)
    comunidade = criar_comunidade()
    ponto_de_apoio = criar_ponto_de_apoio(admin, comunidade)
    outro_ponto_de_apoio = criar_ponto_de_apoio(admin, comunidade, nome="Outro ponto")
    tipo = criar_tipo_de_recurso(admin)

    lancar_credito(
        sessao,
        tipo_de_recurso_id=tipo.id,
        ponto_de_apoio_id=ponto_de_apoio.id,
        quantidade=Decimal("3.00"),
        valor_em_moedas=Decimal("3.00"),
        operador=admin,
    )
    lancar_credito(
        sessao,
        tipo_de_recurso_id=tipo.id,
        ponto_de_apoio_id=outro_ponto_de_apoio.id,
        quantidade=Decimal("5.00"),
        valor_em_moedas=Decimal("5.00"),
        operador=admin,
    )
    sessao.commit()

    resposta = cliente.get(
        f"/v1/lancamentos?ponto_de_apoio={ponto_de_apoio.id}",
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
    )

    assert resposta.status_code == 200
    corpo = resposta.json()
    assert len(corpo["itens"]) == 1
    assert corpo["itens"][0]["ponto_de_apoio_id"] == str(ponto_de_apoio.id)
    assert corpo["itens"][0]["quantidade"] == "3.00"


def test_listagem_traz_o_ajuste_com_original_e_motivo(
    cliente,
    criar_chave,
    criar_persona,
    criar_sessao_de_teste,
    criar_comunidade,
    criar_ponto_de_apoio,
    criar_tipo_de_recurso,
    sessao,
):
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    token, _ = criar_sessao_de_teste(admin)
    comunidade = criar_comunidade()
    ponto_de_apoio = criar_ponto_de_apoio(admin, comunidade)
    tipo = criar_tipo_de_recurso(admin)

    credito = lancar_credito(
        sessao,
        tipo_de_recurso_id=tipo.id,
        ponto_de_apoio_id=ponto_de_apoio.id,
        quantidade=Decimal("3.00"),
        valor_em_moedas=Decimal("3.00"),
        operador=admin,
    )
    ajuste = lancar_ajuste(
        sessao,
        operador=admin,
        lancamento_original=credito,
        quantidade=Decimal("-1.00"),
        valor_em_moedas=Decimal("-1.00"),
        motivo="Corrige a maior.",
    )
    sessao.commit()

    resposta = cliente.get(
        f"/v1/lancamentos?ponto_de_apoio={ponto_de_apoio.id}",
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
    )

    assert resposta.status_code == 200
    itens_por_id = {item["id"]: item for item in resposta.json()["itens"]}
    assert itens_por_id[str(ajuste.id)]["lancamento_original_id"] == str(credito.id)
    assert itens_por_id[str(ajuste.id)]["motivo_do_ajuste"] == "Corrige a maior."


def test_listagem_sem_ponto_de_apoio_e_recusada(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste
):
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    token, _ = criar_sessao_de_teste(admin)

    resposta = cliente.get(
        "/v1/lancamentos",
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
    )

    assert resposta.status_code == 422


def test_listagem_filtra_por_tipo_de_recurso(
    cliente,
    criar_chave,
    criar_persona,
    criar_sessao_de_teste,
    criar_comunidade,
    criar_ponto_de_apoio,
    criar_tipo_de_recurso,
    sessao,
):
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    token, _ = criar_sessao_de_teste(admin)
    comunidade = criar_comunidade()
    ponto_de_apoio = criar_ponto_de_apoio(admin, comunidade)
    tipo_a = criar_tipo_de_recurso(admin, nome="Lanche")
    tipo_b = criar_tipo_de_recurso(admin, nome="Material")

    lancar_credito(
        sessao,
        tipo_de_recurso_id=tipo_a.id,
        ponto_de_apoio_id=ponto_de_apoio.id,
        quantidade=Decimal("3.00"),
        valor_em_moedas=Decimal("3.00"),
        operador=admin,
    )
    lancar_credito(
        sessao,
        tipo_de_recurso_id=tipo_b.id,
        ponto_de_apoio_id=ponto_de_apoio.id,
        quantidade=Decimal("2.00"),
        valor_em_moedas=Decimal("2.00"),
        operador=admin,
    )
    sessao.commit()

    resposta = cliente.get(
        f"/v1/lancamentos?ponto_de_apoio={ponto_de_apoio.id}&tipo_de_recurso={tipo_a.id}",
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
    )

    corpo = resposta.json()
    assert len(corpo["itens"]) == 1
    assert corpo["itens"][0]["tipo_de_recurso_id"] == str(tipo_a.id)


def test_listagem_pagina_por_cursor(
    cliente,
    criar_chave,
    criar_persona,
    criar_sessao_de_teste,
    criar_comunidade,
    criar_ponto_de_apoio,
    criar_tipo_de_recurso,
    sessao,
):
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    token, _ = criar_sessao_de_teste(admin)
    comunidade = criar_comunidade()
    ponto_de_apoio = criar_ponto_de_apoio(admin, comunidade)
    tipo = criar_tipo_de_recurso(admin)

    for _ in range(3):
        lancar_credito(
            sessao,
            tipo_de_recurso_id=tipo.id,
            ponto_de_apoio_id=ponto_de_apoio.id,
            quantidade=Decimal("1.00"),
            valor_em_moedas=Decimal("1.00"),
            operador=admin,
        )
    sessao.commit()
    headers = {"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"}

    primeira_pagina = cliente.get(
        f"/v1/lancamentos?ponto_de_apoio={ponto_de_apoio.id}&tamanho=2", headers=headers
    )
    assert len(primeira_pagina.json()["itens"]) == 2
    cursor = primeira_pagina.json()["proximo_cursor"]
    assert cursor is not None

    segunda_pagina = cliente.get(
        f"/v1/lancamentos?ponto_de_apoio={ponto_de_apoio.id}&tamanho=2&cursor={cursor}",
        headers=headers,
    )
    assert len(segunda_pagina.json()["itens"]) == 1
    assert segunda_pagina.json()["proximo_cursor"] is None

    ids_da_primeira = {item["id"] for item in primeira_pagina.json()["itens"]}
    ids_da_segunda = {item["id"] for item in segunda_pagina.json()["itens"]}
    assert ids_da_primeira.isdisjoint(ids_da_segunda)


def test_mestre_nao_lista_lancamentos(
    cliente,
    criar_chave,
    criar_persona,
    criar_sessao_de_teste,
    criar_comunidade,
    criar_ponto_de_apoio,
):
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    mestre = criar_persona(Papel.mestre, criada_por=admin)
    token, _ = criar_sessao_de_teste(mestre)
    comunidade = criar_comunidade()
    ponto_de_apoio = criar_ponto_de_apoio(admin, comunidade)

    resposta = cliente.get(
        f"/v1/lancamentos?ponto_de_apoio={ponto_de_apoio.id}",
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
    )

    assert resposta.status_code == 403
