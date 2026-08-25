from nucleo.personas.modelo import Papel


def test_guerreiro_le_as_proprias_contas(
    cliente, criar_chave, criar_persona, criar_ponto_extra, criar_sessao_de_teste
):
    guerreiro = criar_persona(Papel.guerreiro)
    criar_ponto_extra(guerreiro, acumulado=30, saldo_disponivel=18)

    chave, _ = criar_chave()
    token, _ = criar_sessao_de_teste(guerreiro)

    resposta = cliente.get(
        "/v1/eu/pontos-extras",
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
    )

    assert resposta.status_code == 200
    assert resposta.json() == {"acumulado": 30, "saldo_disponivel": 18}


def test_guerreiro_sem_ponto_extra_recebe_zero(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste
):
    guerreiro = criar_persona(Papel.guerreiro)

    chave, _ = criar_chave()
    token, _ = criar_sessao_de_teste(guerreiro)

    resposta = cliente.get(
        "/v1/eu/pontos-extras",
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
    )

    assert resposta.status_code == 200
    assert resposta.json() == {"acumulado": 0, "saldo_disponivel": 0}


def test_mestre_nao_le_pontos_extras_por_esta_rota(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste
):
    mestre = criar_persona(Papel.mestre)

    chave, _ = criar_chave()
    token, _ = criar_sessao_de_teste(mestre)

    resposta = cliente.get(
        "/v1/eu/pontos-extras",
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
    )

    assert resposta.status_code == 403


def test_admin_nao_le_pontos_extras_por_esta_rota(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste
):
    admin = criar_persona(Papel.admin)

    chave, _ = criar_chave()
    token, _ = criar_sessao_de_teste(admin)

    resposta = cliente.get(
        "/v1/eu/pontos-extras",
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
    )

    assert resposta.status_code == 403
