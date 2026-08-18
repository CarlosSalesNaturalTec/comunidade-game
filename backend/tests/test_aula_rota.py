from decimal import Decimal

from nucleo.personas.modelo import Papel

INICIO = "2026-08-01T10:00:00-03:00"
FIM = "2026-08-01T12:00:00-03:00"


def test_admin_agenda_aula_pela_rota(
    cliente,
    criar_chave,
    criar_persona,
    criar_sessao_de_teste,
    criar_comunidade,
    criar_ponto_de_apoio,
):
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    token, _ = criar_sessao_de_teste(admin)
    comunidade = criar_comunidade()
    ponto_de_apoio = criar_ponto_de_apoio(admin, comunidade)

    resposta = cliente.post(
        "/v1/aulas",
        json={
            "comunidade_virtual_id": str(comunidade.id),
            "ponto_de_apoio_id": str(ponto_de_apoio.id),
            "inicio_em": INICIO,
            "fim_em": FIM,
        },
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
    )

    assert resposta.status_code == 201
    corpo = resposta.json()
    assert corpo["situacao"] == "confirmada"
    assert corpo["recursos_faltantes"] == []


def test_agendamento_sem_saldo_devolve_o_que_falta(
    cliente,
    criar_chave,
    criar_persona,
    criar_sessao_de_teste,
    criar_comunidade,
    criar_ponto_de_apoio,
    criar_tipo_de_recurso,
):
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    token, _ = criar_sessao_de_teste(admin)
    comunidade = criar_comunidade()
    ponto_de_apoio = criar_ponto_de_apoio(admin, comunidade)
    tipo = criar_tipo_de_recurso(admin)

    resposta = cliente.post(
        "/v1/aulas",
        json={
            "comunidade_virtual_id": str(comunidade.id),
            "ponto_de_apoio_id": str(ponto_de_apoio.id),
            "inicio_em": INICIO,
            "fim_em": FIM,
            "recursos_declarados": [{"tipo_de_recurso_id": str(tipo.id), "quantidade": "3.00"}],
        },
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
    )

    assert resposta.status_code == 201
    corpo = resposta.json()
    assert corpo["situacao"] == "pendente_de_lastro"
    assert corpo["recursos_faltantes"] == [
        {
            "tipo_de_recurso_id": str(tipo.id),
            "quantidade_declarada": "3.00",
            "quantidade_disponivel": "0",
        }
    ]


def test_mestre_nao_agenda_aula_pela_rota(
    cliente,
    criar_chave,
    criar_persona,
    criar_sessao_de_teste,
    criar_comunidade,
    criar_ponto_de_apoio,
):
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    mestre = criar_persona(Papel.mestre)
    token, _ = criar_sessao_de_teste(mestre)
    comunidade = criar_comunidade()
    ponto_de_apoio = criar_ponto_de_apoio(admin, comunidade)

    resposta = cliente.post(
        "/v1/aulas",
        json={
            "comunidade_virtual_id": str(comunidade.id),
            "ponto_de_apoio_id": str(ponto_de_apoio.id),
            "inicio_em": INICIO,
            "fim_em": FIM,
        },
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
    )

    assert resposta.status_code == 403
    corpo = resposta.json()
    assert corpo["codigo"] == "permissao_negada"


def test_reserva_pela_rota_confirma_aula_pendente(
    cliente,
    criar_chave,
    criar_persona,
    criar_sessao_de_teste,
    criar_comunidade,
    criar_ponto_de_apoio,
    criar_tipo_de_recurso,
    criar_lancamento,
    criar_aula,
    criar_recurso_declarado_da_aula,
    sessao,
):
    from nucleo.aulas.modelo import SituacaoDaAula

    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    token, _ = criar_sessao_de_teste(admin)
    comunidade = criar_comunidade()
    ponto_de_apoio = criar_ponto_de_apoio(admin, comunidade)
    tipo = criar_tipo_de_recurso(admin)
    aula = criar_aula(admin, comunidade, ponto_de_apoio=ponto_de_apoio)
    criar_recurso_declarado_da_aula(aula, tipo, quantidade=Decimal("2.00"))
    aula.situacao = SituacaoDaAula.pendente_de_lastro
    sessao.commit()
    criar_lancamento(admin, tipo, ponto_de_apoio, quantidade=Decimal("2.00"))

    resposta = cliente.post(
        f"/v1/aulas/{aula.id}/reservas",
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
    )

    assert resposta.status_code == 200
    assert resposta.json()["situacao"] == "confirmada"


def test_lancamentos_pela_rota_lanca_a_atividade_realizada(
    cliente,
    criar_chave,
    criar_persona,
    criar_sessao_de_teste,
    criar_comunidade,
    criar_aula,
    criar_trilha,
    criar_missao,
    criar_atividade,
):
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    token, _ = criar_sessao_de_teste(admin)
    comunidade = criar_comunidade()
    aula = criar_aula(admin, comunidade)
    guerreiro = criar_persona(Papel.guerreiro, comunidade=comunidade)
    trilha = criar_trilha(admin)
    missao = criar_missao(trilha, admin)
    atividade = criar_atividade(missao, admin)

    resposta = cliente.post(
        f"/v1/aulas/{aula.id}/lancamentos",
        json={
            "resultados": [
                {
                    "guerreiro_id": str(guerreiro.id),
                    "atividade_id": str(atividade.id),
                    "momento_do_fato": INICIO,
                    "producao": "Produção do Guerreiro(a).",
                    "desfecho": "realizada",
                }
            ]
        },
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
    )

    assert resposta.status_code == 201
    assert resposta.json()["situacao"] == "realizada"


def test_mestre_nao_lanca_atividade_pela_rota(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste, criar_comunidade, criar_aula
):
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    mestre = criar_persona(Papel.mestre)
    token, _ = criar_sessao_de_teste(mestre)
    comunidade = criar_comunidade()
    aula = criar_aula(admin, comunidade)

    resposta = cliente.post(
        f"/v1/aulas/{aula.id}/lancamentos",
        json={"resultados": []},
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
    )

    assert resposta.status_code == 403


def test_admin_cancela_aula_pela_rota(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste, criar_comunidade, criar_aula
):
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    token, _ = criar_sessao_de_teste(admin)
    comunidade = criar_comunidade()
    aula = criar_aula(admin, comunidade)

    resposta = cliente.post(
        f"/v1/aulas/{aula.id}/cancelamento",
        json={"motivo": "Chuva forte."},
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
    )

    assert resposta.status_code == 200
    corpo = resposta.json()
    assert corpo["situacao"] == "cancelada"
    assert corpo["cancelamento_motivo"] == "Chuva forte."


def test_mestre_da_comunidade_cancela_aula_pela_rota(
    cliente,
    criar_chave,
    criar_persona,
    criar_sessao_de_teste,
    criar_comunidade,
    criar_aula,
    criar_vinculo_jogador,
):
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    mestre = criar_persona(Papel.mestre)
    token, _ = criar_sessao_de_teste(mestre)
    comunidade = criar_comunidade()
    criar_vinculo_jogador(mestre, comunidade)
    aula = criar_aula(admin, comunidade)

    resposta = cliente.post(
        f"/v1/aulas/{aula.id}/cancelamento",
        json={"motivo": "Chuva forte."},
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
    )

    assert resposta.status_code == 200


def test_apoiador_nao_cancela_aula_pela_rota(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste, criar_comunidade, criar_aula
):
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    apoiador = criar_persona(Papel.apoiador)
    token, _ = criar_sessao_de_teste(apoiador)
    comunidade = criar_comunidade()
    aula = criar_aula(admin, comunidade)

    resposta = cliente.post(
        f"/v1/aulas/{aula.id}/cancelamento",
        json={"motivo": "Não pode."},
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
    )

    assert resposta.status_code == 403


def test_cancelamento_sem_motivo_e_recusado_com_422_pela_rota(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste, criar_comunidade, criar_aula
):
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    token, _ = criar_sessao_de_teste(admin)
    comunidade = criar_comunidade()
    aula = criar_aula(admin, comunidade)

    resposta = cliente.post(
        f"/v1/aulas/{aula.id}/cancelamento",
        json={"motivo": ""},
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
    )

    assert resposta.status_code == 422
    assert resposta.json()["codigo"] == "erro_de_validacao"
