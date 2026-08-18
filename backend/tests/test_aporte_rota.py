from decimal import Decimal

from nucleo.personas.modelo import Papel


def test_admin_registra_aporte_pela_rota(
    cliente,
    criar_chave,
    criar_persona,
    criar_sessao_de_teste,
    criar_comunidade,
    criar_ponto_de_apoio,
    criar_tipo_de_recurso,
    criar_valor_de_referencia,
):
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    apoiador = criar_persona(Papel.apoiador)
    token, _ = criar_sessao_de_teste(admin)
    comunidade = criar_comunidade()
    ponto_de_apoio = criar_ponto_de_apoio(admin, comunidade)
    tipo = criar_tipo_de_recurso(admin)
    criar_valor_de_referencia(admin, tipo, valor_em_moedas=Decimal("0.50"))

    resposta = cliente.post(
        "/v1/aportes",
        data={
            "provedor_id": str(apoiador.id),
            "tipo_de_recurso_id": str(tipo.id),
            "quantidade": "3",
            "ponto_de_apoio_id": str(ponto_de_apoio.id),
            "data_do_aporte": "2026-06-01",
            "forma": "material",
        },
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
    )

    assert resposta.status_code == 201
    corpo = resposta.json()
    assert corpo["valor_em_moedas"] == "1.50"
    assert corpo["origem_do_registro"] == "gestao"
    assert corpo["ressarcivel"] is False


def test_registro_de_aporte_com_comprovante_em_pdf(
    cliente,
    criar_chave,
    criar_persona,
    criar_sessao_de_teste,
    criar_comunidade,
    criar_ponto_de_apoio,
    criar_tipo_de_recurso,
    criar_valor_de_referencia,
):
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    apoiador = criar_persona(Papel.apoiador)
    token, _ = criar_sessao_de_teste(admin)
    comunidade = criar_comunidade()
    ponto_de_apoio = criar_ponto_de_apoio(admin, comunidade)
    tipo = criar_tipo_de_recurso(admin, exige_comprovante=True)
    criar_valor_de_referencia(admin, tipo)

    resposta = cliente.post(
        "/v1/aportes",
        data={
            "provedor_id": str(apoiador.id),
            "tipo_de_recurso_id": str(tipo.id),
            "quantidade": "1",
            "ponto_de_apoio_id": str(ponto_de_apoio.id),
            "data_do_aporte": "2026-06-01",
            "forma": "material",
        },
        files={"comprovante": ("comprovante.pdf", b"conteudo", "application/pdf")},
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
    )

    assert resposta.status_code == 201


def test_aporte_sem_comprovante_quando_tipo_exige_e_recusado_com_422(
    cliente,
    criar_chave,
    criar_persona,
    criar_sessao_de_teste,
    criar_comunidade,
    criar_ponto_de_apoio,
    criar_tipo_de_recurso,
    criar_valor_de_referencia,
):
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    apoiador = criar_persona(Papel.apoiador)
    token, _ = criar_sessao_de_teste(admin)
    comunidade = criar_comunidade()
    ponto_de_apoio = criar_ponto_de_apoio(admin, comunidade)
    tipo = criar_tipo_de_recurso(admin, exige_comprovante=True)
    criar_valor_de_referencia(admin, tipo)

    resposta = cliente.post(
        "/v1/aportes",
        data={
            "provedor_id": str(apoiador.id),
            "tipo_de_recurso_id": str(tipo.id),
            "quantidade": "1",
            "ponto_de_apoio_id": str(ponto_de_apoio.id),
            "data_do_aporte": "2026-06-01",
            "forma": "material",
        },
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
    )

    assert resposta.status_code == 422
    assert resposta.json()["campo"] == "comprovante"


def test_aporte_em_nome_de_si_mesmo_e_recusado_com_403_pela_rota(
    cliente,
    criar_chave,
    criar_persona,
    criar_sessao_de_teste,
    criar_comunidade,
    criar_ponto_de_apoio,
    criar_tipo_de_recurso,
    criar_valor_de_referencia,
):
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    token, _ = criar_sessao_de_teste(admin)
    comunidade = criar_comunidade()
    ponto_de_apoio = criar_ponto_de_apoio(admin, comunidade)
    tipo = criar_tipo_de_recurso(admin)
    criar_valor_de_referencia(admin, tipo)

    resposta = cliente.post(
        "/v1/aportes",
        data={
            "provedor_id": str(admin.id),
            "tipo_de_recurso_id": str(tipo.id),
            "quantidade": "1",
            "ponto_de_apoio_id": str(ponto_de_apoio.id),
            "data_do_aporte": "2026-06-01",
            "forma": "material",
        },
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
    )

    assert resposta.status_code == 403


def test_aporte_sem_chave_e_recusado_com_401(
    cliente,
    criar_persona,
    criar_sessao_de_teste,
    criar_comunidade,
    criar_ponto_de_apoio,
    criar_tipo_de_recurso,
    criar_valor_de_referencia,
):
    admin = criar_persona(Papel.admin)
    apoiador = criar_persona(Papel.apoiador)
    token, _ = criar_sessao_de_teste(admin)
    comunidade = criar_comunidade()
    ponto_de_apoio = criar_ponto_de_apoio(admin, comunidade)
    tipo = criar_tipo_de_recurso(admin)
    criar_valor_de_referencia(admin, tipo)

    resposta = cliente.post(
        "/v1/aportes",
        data={
            "provedor_id": str(apoiador.id),
            "tipo_de_recurso_id": str(tipo.id),
            "quantidade": "1",
            "ponto_de_apoio_id": str(ponto_de_apoio.id),
            "data_do_aporte": "2026-06-01",
            "forma": "material",
        },
        headers={"Authorization": f"Bearer {token}"},
    )

    assert resposta.status_code == 401


def test_aporte_sem_credencial_de_persona_e_recusado_com_401(
    cliente,
    criar_chave,
    criar_persona,
    criar_comunidade,
    criar_ponto_de_apoio,
    criar_tipo_de_recurso,
    criar_valor_de_referencia,
):
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    apoiador = criar_persona(Papel.apoiador)
    comunidade = criar_comunidade()
    ponto_de_apoio = criar_ponto_de_apoio(admin, comunidade)
    tipo = criar_tipo_de_recurso(admin)
    criar_valor_de_referencia(admin, tipo)

    resposta = cliente.post(
        "/v1/aportes",
        data={
            "provedor_id": str(apoiador.id),
            "tipo_de_recurso_id": str(tipo.id),
            "quantidade": "1",
            "ponto_de_apoio_id": str(ponto_de_apoio.id),
            "data_do_aporte": "2026-06-01",
            "forma": "material",
        },
        headers={"X-Chave-Aplicacao": chave},
    )

    assert resposta.status_code == 401


def test_mestre_absorve_um_recurso_pela_rota(
    cliente,
    criar_chave,
    criar_persona,
    criar_sessao_de_teste,
    criar_comunidade,
    criar_ponto_de_apoio,
    criar_tipo_de_recurso,
    criar_valor_de_referencia,
):
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    mestre = criar_persona(Papel.mestre, criada_por=admin)
    token, _ = criar_sessao_de_teste(mestre)
    comunidade = criar_comunidade()
    ponto_de_apoio = criar_ponto_de_apoio(admin, comunidade)
    tipo = criar_tipo_de_recurso(admin)
    criar_valor_de_referencia(admin, tipo, valor_em_moedas=Decimal("1.00"))

    resposta = cliente.post(
        "/v1/aportes/absorcao",
        data={
            "tipo_de_recurso_id": str(tipo.id),
            "quantidade": "2",
            "ponto_de_apoio_id": str(ponto_de_apoio.id),
            "data_do_aporte": "2026-06-01",
        },
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
    )

    assert resposta.status_code == 201
    corpo = resposta.json()
    assert corpo["provedor_id"] == str(mestre.id)
    assert corpo["ressarcivel"] is True
    assert corpo["situacao_de_ressarcimento"] == "em_aberto"


def test_apoiador_nao_absorve_pela_rota(
    cliente,
    criar_chave,
    criar_persona,
    criar_sessao_de_teste,
    criar_comunidade,
    criar_ponto_de_apoio,
    criar_tipo_de_recurso,
    criar_valor_de_referencia,
):
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    apoiador = criar_persona(Papel.apoiador)
    token, _ = criar_sessao_de_teste(apoiador)
    comunidade = criar_comunidade()
    ponto_de_apoio = criar_ponto_de_apoio(admin, comunidade)
    tipo = criar_tipo_de_recurso(admin)
    criar_valor_de_referencia(admin, tipo)

    resposta = cliente.post(
        "/v1/aportes/absorcao",
        data={
            "tipo_de_recurso_id": str(tipo.id),
            "quantidade": "1",
            "ponto_de_apoio_id": str(ponto_de_apoio.id),
            "data_do_aporte": "2026-06-01",
        },
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
    )

    assert resposta.status_code == 403
