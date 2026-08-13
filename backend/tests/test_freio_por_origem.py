from datetime import timedelta

from sqlalchemy import func, select

from nucleo.banco import Base


def _contar_linhas(sessao) -> dict[str, int]:
    return {
        tabela.name: sessao.execute(select(func.count()).select_from(tabela)).scalar_one()
        for tabela in Base.metadata.sorted_tables
    }


def test_origem_dentro_do_limite_e_processada(
    cliente_com_origem, criar_chave, sobrescrever_configuracao
):
    sobrescrever_configuracao(protecao_freio_nick_limite=2)
    chave, _ = criar_chave()
    cliente = cliente_com_origem()
    headers = {"X-Chave-Aplicacao": chave}

    primeira = cliente.get("/v1/consulta-por-nick", headers=headers)
    segunda = cliente.get("/v1/consulta-por-nick", headers=headers)

    assert primeira.status_code == 200
    assert segunda.status_code == 200


def test_origem_acima_do_limite_e_recusada_com_tempo_de_espera(
    cliente_com_origem, criar_chave, sobrescrever_configuracao
):
    sobrescrever_configuracao(protecao_freio_nick_limite=1)
    chave, _ = criar_chave()
    cliente = cliente_com_origem()
    headers = {"X-Chave-Aplicacao": chave}

    cliente.get("/v1/consulta-por-nick", headers=headers)
    resposta = cliente.get("/v1/consulta-por-nick", headers=headers)

    assert resposta.status_code == 429
    assert resposta.json()["codigo"] == "freio_por_origem_acionado"
    assert "Retry-After" in resposta.headers
    assert int(resposta.headers["Retry-After"]) >= 1


def test_atraso_cresce_a_cada_repeticao_e_para_no_teto(
    cliente_com_origem, criar_chave, sobrescrever_configuracao
):
    sobrescrever_configuracao(
        protecao_freio_nick_limite=1,
        protecao_freio_atraso_inicial=timedelta(seconds=2),
        protecao_freio_atraso_fator_de_crescimento=2.0,
        protecao_freio_atraso_teto=timedelta(seconds=8),
    )
    chave, _ = criar_chave()
    cliente = cliente_com_origem()
    headers = {"X-Chave-Aplicacao": chave}

    cliente.get("/v1/consulta-por-nick", headers=headers)  # dentro do limite, não conta atraso

    tempos_de_espera = []
    for _ in range(5):
        resposta = cliente.get("/v1/consulta-por-nick", headers=headers)
        assert resposta.status_code == 429
        tempos_de_espera.append(int(resposta.headers["Retry-After"]))

    assert tempos_de_espera == sorted(tempos_de_espera)
    assert tempos_de_espera[0] < tempos_de_espera[-1]
    assert tempos_de_espera[-1] == 8
    assert tempos_de_espera.count(8) >= 2


def test_origens_distintas_nao_dividem_o_mesmo_freio(
    cliente_com_origem, criar_chave, sobrescrever_configuracao
):
    sobrescrever_configuracao(protecao_freio_nick_limite=1)
    chave, _ = criar_chave()
    headers = {"X-Chave-Aplicacao": chave}
    origem_a = cliente_com_origem("203.0.113.10")
    origem_b = cliente_com_origem("203.0.113.20")

    origem_a.get("/v1/consulta-por-nick", headers=headers)
    freada = origem_a.get("/v1/consulta-por-nick", headers=headers)
    processada = origem_b.get("/v1/consulta-por-nick", headers=headers)

    assert freada.status_code == 429
    assert processada.status_code == 200


def test_superficies_contam_separadamente(
    cliente_com_origem, criar_chave, sobrescrever_configuracao
):
    sobrescrever_configuracao(protecao_freio_nick_limite=1, protecao_freio_formulario_limite=1)
    chave, _ = criar_chave()
    headers = {"X-Chave-Aplicacao": chave}
    cliente = cliente_com_origem()

    cliente.get("/v1/consulta-por-nick", headers=headers)
    freada_no_nick = cliente.get("/v1/consulta-por-nick", headers=headers)
    processado_no_formulario = cliente.post("/v1/formulario-participacao", headers=headers)

    assert freada_no_nick.status_code == 429
    assert processado_no_formulario.status_code == 200


def test_freio_nao_exige_captcha_nem_cadastro(
    cliente_com_origem, criar_chave, sobrescrever_configuracao
):
    sobrescrever_configuracao(protecao_freio_nick_limite=1)
    chave, _ = criar_chave()
    cliente = cliente_com_origem()
    headers = {"X-Chave-Aplicacao": chave}

    cliente.get("/v1/consulta-por-nick", headers=headers)
    resposta = cliente.get("/v1/consulta-por-nick", headers=headers)

    assert resposta.status_code == 429
    corpo = resposta.json()
    assert set(corpo.keys()) <= {"codigo", "mensagem", "campo"}
    assert "captcha" not in str(corpo).lower()
    assert "set-cookie" not in {nome.lower() for nome in resposta.headers.keys()}


def test_freio_nao_grava_nada_no_banco(
    cliente_com_origem, criar_chave, sobrescrever_configuracao, sessao
):
    sobrescrever_configuracao(protecao_freio_nick_limite=1)
    chave, _ = criar_chave()
    cliente = cliente_com_origem()
    headers = {"X-Chave-Aplicacao": chave}

    antes = _contar_linhas(sessao)
    for _ in range(5):
        cliente.get("/v1/consulta-por-nick", headers=headers)
    depois = _contar_linhas(sessao)

    assert antes == depois


def test_rota_sem_freio_declarado_nunca_e_freada_por_origem(cliente_com_origem, criar_chave):
    """A solicitação de chave é o exemplo do PRD (`RN-01-46`): esta fatia
    ainda não tem essa rota, mas qualquer rota que não declare o freio já
    exibe a mesma ausência de limite por origem."""
    chave, _ = criar_chave()
    cliente = cliente_com_origem()
    headers = {"X-Chave-Aplicacao": chave}

    respostas = [cliente.get("/v1/publica", headers=headers) for _ in range(50)]

    assert all(resposta.status_code == 200 for resposta in respostas)


def test_mensagem_do_429_esta_em_portugues_e_e_legivel(
    cliente_com_origem, criar_chave, sobrescrever_configuracao
):
    sobrescrever_configuracao(protecao_freio_nick_limite=1)
    chave, _ = criar_chave()
    cliente = cliente_com_origem()
    headers = {"X-Chave-Aplicacao": chave}

    cliente.get("/v1/consulta-por-nick", headers=headers)
    resposta = cliente.get("/v1/consulta-por-nick", headers=headers)

    mensagem = resposta.json()["mensagem"].lower()
    assert "tente novamente" in mensagem
    assert any(termo in mensagem for termo in ("segundo", "minuto"))
