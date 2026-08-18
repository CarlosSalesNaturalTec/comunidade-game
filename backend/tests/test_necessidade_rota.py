from decimal import Decimal

from nucleo.aulas.modelo import SituacaoDaAula
from nucleo.personas.modelo import Papel


def _tornar_pendente(sessao, aula):
    aula.situacao = SituacaoDaAula.pendente_de_lastro
    sessao.commit()


def test_rota_publica_responde_sem_credencial_de_persona(
    cliente,
    sessao,
    criar_chave,
    criar_persona,
    criar_comunidade,
    criar_ponto_de_apoio,
    criar_tipo_de_recurso,
    criar_aula,
    criar_recurso_declarado_da_aula,
):
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    comunidade = criar_comunidade()
    ponto_de_apoio = criar_ponto_de_apoio(admin, comunidade)
    tipo = criar_tipo_de_recurso(admin)
    aula = criar_aula(admin, comunidade, ponto_de_apoio=ponto_de_apoio)
    criar_recurso_declarado_da_aula(aula, tipo, quantidade=Decimal("2.00"))
    _tornar_pendente(sessao, aula)

    resposta = cliente.get("/v1/vitrine/necessidades", headers={"X-Chave-Aplicacao": chave})

    assert resposta.status_code == 200
    corpo = resposta.json()
    assert len(corpo) == 1
    assert corpo[0]["aula_id"] == str(aula.id)


def test_rota_publica_recusa_sem_chave_de_aplicacao(cliente):
    resposta = cliente.get("/v1/vitrine/necessidades")

    assert resposta.status_code == 401


def test_nenhuma_rota_devolve_reais_nem_pessoa(
    cliente,
    sessao,
    criar_chave,
    criar_persona,
    criar_comunidade,
    criar_ponto_de_apoio,
    criar_tipo_de_recurso,
    criar_valor_de_referencia,
    criar_aula,
    criar_recurso_declarado_da_aula,
    criar_sessao_de_teste,
    criar_vinculo_jogador,
):
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    comunidade = criar_comunidade()
    ponto_de_apoio = criar_ponto_de_apoio(admin, comunidade)
    tipo = criar_tipo_de_recurso(admin)
    criar_valor_de_referencia(admin, tipo, valor_em_moedas=Decimal("0.50"))
    aula = criar_aula(admin, comunidade, ponto_de_apoio=ponto_de_apoio)
    criar_recurso_declarado_da_aula(aula, tipo, quantidade=Decimal("2.00"))
    _tornar_pendente(sessao, aula)

    mestre = criar_persona(Papel.mestre)
    criar_vinculo_jogador(mestre, comunidade)
    token, _ = criar_sessao_de_teste(mestre)

    campos_esperados = {
        "aula_id",
        "tipo_de_recurso_id",
        "quantidade_faltante",
        "valor_em_moedas",
        "comunidade_virtual_id",
        "ponto_de_apoio_id",
        "inicio_em",
        "fim_em",
    }

    resposta_publica = cliente.get("/v1/vitrine/necessidades", headers={"X-Chave-Aplicacao": chave})
    resposta_do_mestre = cliente.get(
        "/v1/necessidades/minhas",
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
    )

    for resposta in (resposta_publica, resposta_do_mestre):
        assert resposta.status_code == 200
        corpo = resposta.json()
        assert len(corpo) == 1
        assert set(corpo[0].keys()) == campos_esperados


def test_lista_do_mestre_filtra_pela_comunidade_vinculada(
    cliente,
    sessao,
    criar_chave,
    criar_persona,
    criar_comunidade,
    criar_ponto_de_apoio,
    criar_tipo_de_recurso,
    criar_aula,
    criar_recurso_declarado_da_aula,
    criar_sessao_de_teste,
    criar_vinculo_jogador,
):
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    comunidade = criar_comunidade()
    outra_comunidade = criar_comunidade()
    ponto_de_apoio = criar_ponto_de_apoio(admin, comunidade)
    ponto_de_apoio_alheio = criar_ponto_de_apoio(admin, outra_comunidade)
    tipo = criar_tipo_de_recurso(admin)

    aula = criar_aula(admin, comunidade, ponto_de_apoio=ponto_de_apoio)
    criar_recurso_declarado_da_aula(aula, tipo, quantidade=Decimal("2.00"))
    _tornar_pendente(sessao, aula)

    aula_alheia = criar_aula(admin, outra_comunidade, ponto_de_apoio=ponto_de_apoio_alheio)
    criar_recurso_declarado_da_aula(aula_alheia, tipo, quantidade=Decimal("2.00"))
    _tornar_pendente(sessao, aula_alheia)

    mestre = criar_persona(Papel.mestre)
    criar_vinculo_jogador(mestre, comunidade)
    token, _ = criar_sessao_de_teste(mestre)

    resposta = cliente.get(
        "/v1/necessidades/minhas",
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
    )

    assert resposta.status_code == 200
    corpo = resposta.json()
    assert [item["aula_id"] for item in corpo] == [str(aula.id)]


def test_necessidades_minhas_recusa_papel_que_nao_e_mestre(
    cliente,
    criar_chave,
    criar_persona,
    criar_sessao_de_teste,
):
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    token, _ = criar_sessao_de_teste(admin)

    resposta = cliente.get(
        "/v1/necessidades/minhas",
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
    )

    assert resposta.status_code == 403
