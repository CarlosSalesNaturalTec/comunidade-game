from nucleo.personas.modelo import Papel, Persona


def test_solicitacao_de_participacao_devolve_so_registro_e_prazo_e_nao_cria_persona(
    cliente, criar_chave, sessao
):
    chave, _ = criar_chave()

    resposta = cliente.post(
        "/v1/solicitacoes-de-participacao",
        data={
            "nome_ou_razao_social": "Fulana de Tal",
            "email": "fulana@example.org",
            "whatsapp": "+55 11 90000-0000",
            "pretensao": "mestre",
            "apresentacao": "Quero ser Mestre na comunidade.",
        },
        headers={"X-Chave-Aplicacao": chave},
    )

    assert resposta.status_code == 201
    corpo = resposta.json()
    assert set(corpo.keys()) == {"id", "prazo"}
    assert sessao.query(Persona).count() == 0


def test_autenticacao_com_os_dados_da_solicitacao_e_recusada(cliente, criar_chave):
    chave, _ = criar_chave()
    cliente.post(
        "/v1/solicitacoes-de-participacao",
        data={
            "nome_ou_razao_social": "Fulana de Tal",
            "email": "fulana@example.org",
            "whatsapp": "+55 11 90000-0000",
            "pretensao": "mestre",
            "apresentacao": "Quero ser Mestre na comunidade.",
        },
        headers={"X-Chave-Aplicacao": chave},
    )

    resposta = cliente.post(
        "/v1/sessoes/credencial",
        json={"usuario": "fulana@example.org", "senha": "qualquer-coisa"},
        headers={"X-Chave-Aplicacao": chave},
    )

    assert resposta.status_code == 403
    assert resposta.json()["codigo"] == "login_sem_cadastro"


def test_solicitacao_de_participacao_de_apoiador_com_comprovante(cliente, criar_chave, sessao):
    chave, _ = criar_chave()

    resposta = cliente.post(
        "/v1/solicitacoes-de-participacao",
        data={
            "nome_ou_razao_social": "Apoiadora de Tal",
            "email": "apoiadora@example.org",
            "whatsapp": "+55 11 90000-0000",
            "pretensao": "apoiador",
            "apresentacao": "Quero apoiar a comunidade.",
            "aporte_declarado": "R$ 500,00 em material escolar",
        },
        files={"comprovante": ("comprovante.pdf", b"conteudo do comprovante", "application/pdf")},
        headers={"X-Chave-Aplicacao": chave},
    )

    assert resposta.status_code == 201
    corpo = resposta.json()
    assert set(corpo.keys()) == {"id", "prazo"}
    assert sessao.query(Persona).count() == 0


def test_solicitacao_de_participacao_com_cpf_e_recusada(cliente, criar_chave):
    chave, _ = criar_chave()

    resposta = cliente.post(
        "/v1/solicitacoes-de-participacao",
        data={
            "nome_ou_razao_social": "Fulana de Tal",
            "email": "fulana@example.org",
            "whatsapp": "+55 11 90000-0000",
            "pretensao": "mestre",
            "apresentacao": "Meu CPF é 529.982.247-25.",
        },
        headers={"X-Chave-Aplicacao": chave},
    )

    assert resposta.status_code == 422
    assert resposta.json()["codigo"] == "documento_pessoal_recusado"


def test_solicitacao_de_dados_sem_finalidade_e_422(cliente, criar_chave):
    chave, _ = criar_chave()

    resposta = cliente.post(
        "/v1/solicitacoes-de-dados",
        json={
            "solicitante": "Pesquisadora de Tal",
            "instituicao": "Universidade de Teste",
            "email": "pesquisadora@example.org",
            "finalidade_declarada": "",
            "recorte_pedido": "Comunidade de Teste, 2026",
        },
        headers={"X-Chave-Aplicacao": chave},
    )

    assert resposta.status_code == 422


def test_solicitacao_de_dados_devolve_so_registro_e_prazo(cliente, criar_chave, sessao):
    chave, _ = criar_chave()

    resposta = cliente.post(
        "/v1/solicitacoes-de-dados",
        json={
            "solicitante": "Pesquisadora de Tal",
            "instituicao": "Universidade de Teste",
            "email": "pesquisadora@example.org",
            "finalidade_declarada": "Pesquisa acadêmica sobre evasão escolar.",
            "recorte_pedido": "Comunidade de Teste, 2026",
        },
        headers={"X-Chave-Aplicacao": chave},
    )

    assert resposta.status_code == 201
    corpo = resposta.json()
    assert set(corpo.keys()) == {"id", "prazo"}
    assert sessao.query(Persona).count() == 0


def test_solicitacao_de_chave_nunca_devolve_chave(cliente, criar_chave, sessao):
    chave, _ = criar_chave()

    resposta = cliente.post(
        "/v1/solicitacoes-de-chave",
        json={
            "solicitante": "Desenvolvedora de Tal",
            "contato": "dev@example.org",
            "o_que_pretende_construir": "Um painel comunitário.",
        },
        headers={"X-Chave-Aplicacao": chave},
    )

    assert resposta.status_code == 201
    corpo = resposta.json()
    assert set(corpo.keys()) == {"id", "prazo"}
    assert "chave" not in str(corpo).lower()
    assert sessao.query(Persona).count() == 0


def test_solicitacao_de_chave_repetida_da_mesma_origem_nao_e_freada(
    cliente_com_origem, criar_chave
):
    chave, _ = criar_chave()
    cliente = cliente_com_origem()
    corpo = {
        "solicitante": "Desenvolvedora de Tal",
        "contato": "dev@example.org",
        "o_que_pretende_construir": "Um painel comunitário.",
    }

    respostas = [
        cliente.post("/v1/solicitacoes-de-chave", json=corpo, headers={"X-Chave-Aplicacao": chave})
        for _ in range(10)
    ]

    assert all(resposta.status_code == 201 for resposta in respostas)


def test_formulario_de_participacao_repetido_encontra_429(
    cliente_com_origem, criar_chave, sobrescrever_configuracao
):
    sobrescrever_configuracao(protecao_freio_formulario_limite=1)
    chave, _ = criar_chave()
    cliente = cliente_com_origem()
    corpo = {
        "nome_ou_razao_social": "Fulana de Tal",
        "email": "fulana@example.org",
        "whatsapp": "+55 11 90000-0000",
        "pretensao": "mestre",
        "apresentacao": "Quero ser Mestre na comunidade.",
    }

    cliente.post(
        "/v1/solicitacoes-de-participacao", data=corpo, headers={"X-Chave-Aplicacao": chave}
    )
    resposta = cliente.post(
        "/v1/solicitacoes-de-participacao", data=corpo, headers={"X-Chave-Aplicacao": chave}
    )

    assert resposta.status_code == 429
    assert resposta.json()["codigo"] == "freio_por_origem_acionado"


def test_cada_formulario_conta_em_separado(
    cliente_com_origem, criar_chave, sobrescrever_configuracao
):
    sobrescrever_configuracao(protecao_freio_formulario_limite=1)
    chave, _ = criar_chave()
    cliente = cliente_com_origem()
    headers = {"X-Chave-Aplicacao": chave}
    corpo_de_participacao = {
        "nome_ou_razao_social": "Fulana de Tal",
        "email": "fulana@example.org",
        "whatsapp": "+55 11 90000-0000",
        "pretensao": "mestre",
        "apresentacao": "Quero ser Mestre na comunidade.",
    }
    corpo_de_dados = {
        "solicitante": "Pesquisadora de Tal",
        "instituicao": "Universidade de Teste",
        "email": "pesquisadora@example.org",
        "finalidade_declarada": "Pesquisa acadêmica sobre evasão escolar.",
        "recorte_pedido": "Comunidade de Teste, 2026",
    }

    cliente.post("/v1/solicitacoes-de-participacao", data=corpo_de_participacao, headers=headers)
    freada = cliente.post(
        "/v1/solicitacoes-de-participacao", data=corpo_de_participacao, headers=headers
    )
    processada = cliente.post("/v1/solicitacoes-de-dados", json=corpo_de_dados, headers=headers)

    assert freada.status_code == 429
    assert processada.status_code == 201


def test_sugestao_sem_credencial_de_persona_e_401(cliente, criar_chave):
    chave, _ = criar_chave()

    resposta = cliente.post(
        "/v1/sugestoes",
        json={"alvo_tipo": "plataforma", "texto": "Sugestão qualquer."},
        headers={"X-Chave-Aplicacao": chave},
    )

    assert resposta.status_code == 401


def test_sugestao_autenticada_grava_autor_persona_e_alvo(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste
):
    chave, _ = criar_chave()
    guerreiro = criar_persona(Papel.guerreiro)
    token, _ = criar_sessao_de_teste(guerreiro)

    resposta = cliente.post(
        "/v1/sugestoes",
        json={"alvo_tipo": "plataforma", "texto": "Podíamos ter um mural entre trilhas."},
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
    )

    assert resposta.status_code == 201
    corpo = resposta.json()
    assert set(corpo.keys()) == {"id", "prazo"}


def test_sugestao_nao_aceita_campo_de_audio(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste
):
    chave, _ = criar_chave()
    guerreiro = criar_persona(Papel.guerreiro)
    token, _ = criar_sessao_de_teste(guerreiro)

    resposta = cliente.post(
        "/v1/sugestoes",
        json={
            "alvo_tipo": "plataforma",
            "texto": "Sugestão qualquer.",
            "audio": "dGVzdGU=",
        },
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
    )

    assert resposta.status_code == 422


def test_apoiador_tambem_pode_registrar_sugestao(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste
):
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    apoiador = criar_persona(Papel.apoiador, criada_por=admin)
    token, _ = criar_sessao_de_teste(apoiador)

    resposta = cliente.post(
        "/v1/sugestoes",
        json={"alvo_tipo": "plataforma", "texto": "Proposta de evolução do Apoiador."},
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
    )

    assert resposta.status_code == 201


def test_guerreiro_nao_ve_dado_de_outra_solicitacao_na_resposta_da_sugestao(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste
):
    chave, _ = criar_chave()
    guerreiro = criar_persona(Papel.guerreiro)
    token, _ = criar_sessao_de_teste(guerreiro)

    resposta = cliente.post(
        "/v1/sugestoes",
        json={"alvo_tipo": "plataforma", "texto": "Sugestão qualquer."},
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
    )

    corpo = resposta.json()
    assert "texto" not in corpo
    assert "autor" not in corpo
