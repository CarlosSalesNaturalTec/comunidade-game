from datetime import timedelta

import pytest
from sqlalchemy.orm import sessionmaker

from nucleo.fila.modelo import SolicitacaoDeDados, SugestaoOuProposta
from nucleo.personas.modelo import Papel, Persona
from nucleo.ponto_extra.modelo import PontoExtra
from nucleo.pontuacao.modelo import Badge, TipoDeBadge
from nucleo.tempo import agora


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


def _headers(chave, token):
    return {"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"}


def _registrar_participacao(cliente, chave, **campos):
    corpo = {
        "nome_ou_razao_social": "Fulana de Tal",
        "email": "fulana@example.org",
        "whatsapp": "+55 11 90000-0000",
        "pretensao": "mestre",
        "apresentacao": "Quero ser Mestre na comunidade.",
        **campos,
    }
    resposta = cliente.post(
        "/v1/solicitacoes-de-participacao", data=corpo, headers={"X-Chave-Aplicacao": chave}
    )
    return resposta.json()["id"]


def test_admin_le_a_fila_de_participacao(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste
):
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    token, _ = criar_sessao_de_teste(admin)
    _registrar_participacao(cliente, chave)

    resposta = cliente.get("/v1/solicitacoes-de-participacao", headers=_headers(chave, token))

    assert resposta.status_code == 200
    corpo = resposta.json()
    assert len(corpo["itens"]) == 1
    item = corpo["itens"][0]
    assert item["nome_ou_razao_social"] == "Fulana de Tal"
    assert item["pretensao"] == "mestre"
    assert item["situacao"] == "recebida"
    assert item["prazo"] is not None


def test_solicitacao_de_apoiador_traz_pre_cadastro_na_fila(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste
):
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    token, _ = criar_sessao_de_teste(admin)
    cliente.post(
        "/v1/solicitacoes-de-participacao",
        data={
            "nome_ou_razao_social": "Apoiadora de Tal",
            "email": "apoiadora@example.org",
            "whatsapp": "+55 11 90000-0000",
            "pretensao": "apoiador",
            "apresentacao": "Quero apoiar a comunidade.",
            "aporte_declarado": "R$ 500,00 em material escolar",
            "nick": "ApoiadoraPretendida",
        },
        files={"comprovante": ("comprovante.pdf", b"conteudo", "application/pdf")},
        headers={"X-Chave-Aplicacao": chave},
    )

    resposta = cliente.get("/v1/solicitacoes-de-participacao", headers=_headers(chave, token))

    item = resposta.json()["itens"][0]
    assert item["aporte_declarado"] == "R$ 500,00 em material escolar"
    assert item["nick"] == "ApoiadoraPretendida"
    assert item["comprovante_anexado"] is True
    assert "conteudo" not in str(item)


def test_solicitacao_com_prazo_vencido_vem_marcada_em_atraso(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste, sessao
):
    from nucleo.fila.modelo import SolicitacaoDeParticipacao

    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    token, _ = criar_sessao_de_teste(admin)
    id_solicitacao = _registrar_participacao(cliente, chave)
    solicitacao = sessao.get(SolicitacaoDeParticipacao, id_solicitacao)
    solicitacao.prazo = agora() - timedelta(seconds=1)
    sessao.commit()

    resposta = cliente.get("/v1/solicitacoes-de-participacao", headers=_headers(chave, token))

    item = resposta.json()["itens"][0]
    assert item["em_atraso"] is True
    assert item["situacao"] == "recebida"


def test_solicitacao_ja_avaliada_traz_desfecho_e_nao_vem_em_atraso(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste
):
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    token, _ = criar_sessao_de_teste(admin)
    id_solicitacao = _registrar_participacao(cliente, chave)
    cliente.post(
        f"/v1/solicitacoes-de-participacao/{id_solicitacao}/avaliacao",
        json={"situacao": "aceita", "parecer": "Perfil compatível."},
        headers=_headers(chave, token),
    )

    resposta = cliente.get("/v1/solicitacoes-de-participacao", headers=_headers(chave, token))

    item = resposta.json()["itens"][0]
    assert item["situacao"] == "aceita"
    assert item["parecer"] == "Perfil compatível."
    assert item["avaliado_por_id"] == str(admin.id)
    assert item["decidido_em"] is not None
    assert item["em_atraso"] is False


def test_quem_nao_e_admin_nao_le_a_fila_de_participacao(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste
):
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    for papel in (Papel.mestre, Papel.apoiador, Papel.guerreiro, Papel.responsavel):
        persona = criar_persona(papel, criada_por=admin)
        token, _ = criar_sessao_de_teste(persona)

        resposta = cliente.get("/v1/solicitacoes-de-participacao", headers=_headers(chave, token))

        assert resposta.status_code == 403


def test_fila_nunca_devolve_o_conteudo_do_comprovante(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste
):
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    token, _ = criar_sessao_de_teste(admin)
    cliente.post(
        "/v1/solicitacoes-de-participacao",
        data={
            "nome_ou_razao_social": "Apoiadora de Tal",
            "email": "apoiadora@example.org",
            "whatsapp": "+55 11 90000-0000",
            "pretensao": "apoiador",
            "apresentacao": "Quero apoiar a comunidade.",
        },
        files={"comprovante": ("comprovante.pdf", b"segredo-do-arquivo", "application/pdf")},
        headers={"X-Chave-Aplicacao": chave},
    )

    resposta = cliente.get("/v1/solicitacoes-de-participacao", headers=_headers(chave, token))

    assert "segredo-do-arquivo" not in resposta.text
    assert "comprovante_referencia" not in resposta.text


def test_admin_aceita_solicitacao_e_nenhuma_persona_e_criada(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste, sessao
):
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    token, _ = criar_sessao_de_teste(admin)
    id_solicitacao = _registrar_participacao(cliente, chave)
    total_de_personas_antes = sessao.query(Persona).count()

    resposta = cliente.post(
        f"/v1/solicitacoes-de-participacao/{id_solicitacao}/avaliacao",
        json={"situacao": "aceita", "parecer": "Perfil compatível com a proposta."},
        headers=_headers(chave, token),
    )

    assert resposta.status_code == 200
    corpo = resposta.json()
    assert corpo["situacao"] == "aceita"
    assert sessao.query(Persona).count() == total_de_personas_antes


def test_admin_recusa_solicitacao_com_o_motivo(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste
):
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    token, _ = criar_sessao_de_teste(admin)
    id_solicitacao = _registrar_participacao(cliente, chave)

    resposta = cliente.post(
        f"/v1/solicitacoes-de-participacao/{id_solicitacao}/avaliacao",
        json={"situacao": "recusada", "parecer": "Perfil incompatível com a proposta."},
        headers=_headers(chave, token),
    )

    assert resposta.status_code == 200
    corpo = resposta.json()
    assert corpo["situacao"] == "recusada"
    assert corpo["parecer"] == "Perfil incompatível com a proposta."


def test_desfecho_fora_do_vocabulario_e_422(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste
):
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    token, _ = criar_sessao_de_teste(admin)
    id_solicitacao = _registrar_participacao(cliente, chave)

    resposta = cliente.post(
        f"/v1/solicitacoes-de-participacao/{id_solicitacao}/avaliacao",
        json={"situacao": "aprovada"},
        headers=_headers(chave, token),
    )

    assert resposta.status_code == 422


def test_segundo_desfecho_sobre_solicitacao_avaliada_e_409_com_original_intacto(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste
):
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    token, _ = criar_sessao_de_teste(admin)
    id_solicitacao = _registrar_participacao(cliente, chave)
    cliente.post(
        f"/v1/solicitacoes-de-participacao/{id_solicitacao}/avaliacao",
        json={"situacao": "aceita", "parecer": "Perfil compatível."},
        headers=_headers(chave, token),
    )

    resposta = cliente.post(
        f"/v1/solicitacoes-de-participacao/{id_solicitacao}/avaliacao",
        json={"situacao": "recusada", "parecer": "Mudei de ideia."},
        headers=_headers(chave, token),
    )

    assert resposta.status_code == 409
    assert resposta.json()["codigo"] == "solicitacao_ja_avaliada"

    conferencia = cliente.get(
        "/v1/solicitacoes-de-participacao", headers=_headers(chave, token)
    ).json()["itens"][0]
    assert conferencia["situacao"] == "aceita"
    assert conferencia["parecer"] == "Perfil compatível."


def test_mestre_recebe_403_ao_avaliar_solicitacao_de_participacao(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste
):
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    mestre = criar_persona(Papel.mestre, criada_por=admin)
    token, _ = criar_sessao_de_teste(mestre)
    id_solicitacao = _registrar_participacao(cliente, chave)

    resposta = cliente.post(
        f"/v1/solicitacoes-de-participacao/{id_solicitacao}/avaliacao",
        json={"situacao": "aceita", "parecer": "Perfil compatível."},
        headers=_headers(chave, token),
    )

    assert resposta.status_code == 403


@pytest.mark.banco_compartilhado
def test_desfecho_da_participacao_entra_na_trilha_de_auditoria(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste, engine, monkeypatch
):
    """A auditoria grava por uma conexão própria (design.md — Decisions do
    middleware); o teste precisa de dado realmente comitado, por isso o
    marcador `banco_compartilhado` (design.md — Decisions 4). O middleware
    lê `Configuracao()` sem override — a mesma fábrica de sessão presa ao
    `engine` que o marcador já usa, para não depender de env var alguma
    fora de `CG_DSN_BANCO_TESTE` (molde de `fabrica_de_auditoria`, ligado
    ao `engine` em vez da `conexao` por não haver `conexao` sob o
    marcador)."""
    monkeypatch.setattr(
        "nucleo.auditoria.middleware.obter_fabrica_de_sessao",
        lambda: sessionmaker(bind=engine, expire_on_commit=False),
    )
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    token, _ = criar_sessao_de_teste(admin)
    id_solicitacao = _registrar_participacao(cliente, chave)

    cliente.post(
        f"/v1/solicitacoes-de-participacao/{id_solicitacao}/avaliacao",
        json={"situacao": "aceita", "parecer": "Perfil compatível."},
        headers=_headers(chave, token),
    )

    resposta = cliente.get("/v1/auditoria", headers=_headers(chave, token))
    corpo = resposta.json()
    registro = next(
        item
        for item in corpo["itens"]
        if item["acao"] == "POST avaliar_solicitacao_de_participacao_rota"
    )
    assert registro["autor_id"] == str(admin.id)
    assert registro["papel_do_autor"] == Papel.admin.value
    assert registro["momento"] is not None


# --- Solicitação de dados (`RF-02-77`, `RF-02-78`, `RF-02-93`, `RF-02-79`) --


def _registrar_dados(cliente, chave, **campos):
    corpo = {
        "solicitante": "Pesquisadora de Tal",
        "instituicao": "Universidade de Teste",
        "email": "pesquisadora@example.org",
        "finalidade_declarada": "Pesquisa acadêmica sobre evasão escolar.",
        "recorte_pedido": "Comunidade de Teste, 2026",
        **campos,
    }
    resposta = cliente.post(
        "/v1/solicitacoes-de-dados", json=corpo, headers={"X-Chave-Aplicacao": chave}
    )
    return resposta.json()["id"]


def test_admin_le_a_fila_de_dados_com_finalidade_e_recorte(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste
):
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    token, _ = criar_sessao_de_teste(admin)
    _registrar_dados(cliente, chave)

    resposta = cliente.get("/v1/solicitacoes-de-dados", headers=_headers(chave, token))

    assert resposta.status_code == 200
    item = resposta.json()["itens"][0]
    assert item["solicitante"] == "Pesquisadora de Tal"
    assert item["instituicao"] == "Universidade de Teste"
    assert item["finalidade_declarada"] == "Pesquisa acadêmica sobre evasão escolar."
    assert item["recorte_pedido"] == "Comunidade de Teste, 2026"
    assert item["situacao"] == "recebida"


def test_solicitacao_de_dados_com_prazo_vencido_vem_em_atraso(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste, sessao
):
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    token, _ = criar_sessao_de_teste(admin)
    id_solicitacao = _registrar_dados(cliente, chave)
    solicitacao = sessao.get(SolicitacaoDeDados, id_solicitacao)
    solicitacao.prazo = agora() - timedelta(seconds=1)
    sessao.commit()

    resposta = cliente.get("/v1/solicitacoes-de-dados", headers=_headers(chave, token))

    item = resposta.json()["itens"][0]
    assert item["em_atraso"] is True


def test_mestre_recebe_403_na_fila_de_dados(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste
):
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    mestre = criar_persona(Papel.mestre, criada_por=admin)
    token, _ = criar_sessao_de_teste(mestre)

    resposta = cliente.get("/v1/solicitacoes-de-dados", headers=_headers(chave, token))

    assert resposta.status_code == 403


def test_admin_aprova_dados_com_compromisso_grava_o_desfecho(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste
):
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    token, _ = criar_sessao_de_teste(admin)
    id_solicitacao = _registrar_dados(cliente, chave)

    resposta = cliente.post(
        f"/v1/solicitacoes-de-dados/{id_solicitacao}/avaliacao",
        json={
            "situacao": "aceita",
            "parecer": "Finalidade compatível com política pública.",
            "compromisso_de_nao_reidentificar": True,
        },
        headers=_headers(chave, token),
    )

    assert resposta.status_code == 200
    corpo = resposta.json()
    assert corpo["situacao"] == "aceita"
    assert corpo["avaliado_por_id"] == str(admin.id)
    assert corpo["decidido_em"] is not None


def test_aprovacao_de_dados_sem_compromisso_e_422(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste
):
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    token, _ = criar_sessao_de_teste(admin)
    id_solicitacao = _registrar_dados(cliente, chave)

    resposta = cliente.post(
        f"/v1/solicitacoes-de-dados/{id_solicitacao}/avaliacao",
        json={"situacao": "aceita", "parecer": "Finalidade compatível."},
        headers=_headers(chave, token),
    )

    assert resposta.status_code == 422


def test_desfecho_de_dados_com_parecer_vazio_e_422(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste
):
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    token, _ = criar_sessao_de_teste(admin)
    id_solicitacao = _registrar_dados(cliente, chave)

    resposta = cliente.post(
        f"/v1/solicitacoes-de-dados/{id_solicitacao}/avaliacao",
        json={"situacao": "recusada", "parecer": ""},
        headers=_headers(chave, token),
    )

    assert resposta.status_code == 422


def test_reavaliacao_de_dados_e_409(cliente, criar_chave, criar_persona, criar_sessao_de_teste):
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    token, _ = criar_sessao_de_teste(admin)
    id_solicitacao = _registrar_dados(cliente, chave)
    cliente.post(
        f"/v1/solicitacoes-de-dados/{id_solicitacao}/avaliacao",
        json={
            "situacao": "aceita",
            "parecer": "Finalidade compatível.",
            "compromisso_de_nao_reidentificar": True,
        },
        headers=_headers(chave, token),
    )

    resposta = cliente.post(
        f"/v1/solicitacoes-de-dados/{id_solicitacao}/avaliacao",
        json={"situacao": "recusada", "parecer": "Mudei de ideia."},
        headers=_headers(chave, token),
    )

    assert resposta.status_code == 409
    assert resposta.json()["codigo"] == "solicitacao_ja_avaliada"


def test_nenhum_conjunto_sai_de_solicitacao_sem_desfecho_ou_recusada(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste
):
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    token, _ = criar_sessao_de_teste(admin)
    id_solicitacao = _registrar_dados(cliente, chave)

    resposta = cliente.post(
        f"/v1/solicitacoes-de-dados/{id_solicitacao}/avaliacao",
        json={
            "situacao": "recusada",
            "parecer": "Finalidade incompatível.",
            "entregue": "CSV anonimizado",
        },
        headers=_headers(chave, token),
    )

    assert resposta.status_code == 422


def test_entrega_sobre_solicitacao_aprovada_registra_o_que_foi_entregue_e_a_quem(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste
):
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    token, _ = criar_sessao_de_teste(admin)
    id_solicitacao = _registrar_dados(cliente, chave)

    resposta = cliente.post(
        f"/v1/solicitacoes-de-dados/{id_solicitacao}/avaliacao",
        json={
            "situacao": "aceita",
            "parecer": "Finalidade compatível.",
            "compromisso_de_nao_reidentificar": True,
            "entregue": "CSV anonimizado enviado a pesquisadora@example.org",
        },
        headers=_headers(chave, token),
    )

    assert resposta.status_code == 200
    assert resposta.json()["entregue"] == "CSV anonimizado enviado a pesquisadora@example.org"

    conferencia = cliente.get("/v1/solicitacoes-de-dados", headers=_headers(chave, token)).json()[
        "itens"
    ][0]
    assert conferencia["entregue"] == "CSV anonimizado enviado a pesquisadora@example.org"


# --- Solicitação de chave (`RF-02-87`, `RF-02-88`) -------------------------


def _registrar_chave(cliente, chave, **campos):
    corpo = {
        "solicitante": "Desenvolvedora de Tal",
        "contato": "dev@example.org",
        "o_que_pretende_construir": "Um painel comunitário.",
        **campos,
    }
    resposta = cliente.post(
        "/v1/solicitacoes-de-chave", json=corpo, headers={"X-Chave-Aplicacao": chave}
    )
    return resposta.json()["id"]


def test_admin_le_a_fila_de_solicitacoes_de_chave(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste
):
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    token, _ = criar_sessao_de_teste(admin)
    _registrar_chave(cliente, chave)

    resposta = cliente.get("/v1/solicitacoes-de-chave", headers=_headers(chave, token))

    assert resposta.status_code == 200
    item = resposta.json()["itens"][0]
    assert item["solicitante"] == "Desenvolvedora de Tal"
    assert item["o_que_pretende_construir"] == "Um painel comunitário."
    assert item["chave_emitida"] is False
    assert "segredo" not in str(item).lower()


def test_admin_aprova_pedido_de_chave_sem_emitir(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste
):
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    token, _ = criar_sessao_de_teste(admin)
    id_solicitacao = _registrar_chave(cliente, chave)

    resposta = cliente.post(
        f"/v1/solicitacoes-de-chave/{id_solicitacao}/avaliacao",
        json={"situacao": "aceita", "parecer": "Projeto compatível."},
        headers=_headers(chave, token),
    )

    assert resposta.status_code == 200
    corpo = resposta.json()
    assert corpo["situacao"] == "aceita"
    assert corpo["chave_emitida"] is False


def test_desfecho_de_chave_fora_do_vocabulario_e_422(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste
):
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    token, _ = criar_sessao_de_teste(admin)
    id_solicitacao = _registrar_chave(cliente, chave)

    resposta = cliente.post(
        f"/v1/solicitacoes-de-chave/{id_solicitacao}/avaliacao",
        json={"situacao": "aprovada"},
        headers=_headers(chave, token),
    )

    assert resposta.status_code == 422


def test_reavaliacao_de_chave_e_409(cliente, criar_chave, criar_persona, criar_sessao_de_teste):
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    token, _ = criar_sessao_de_teste(admin)
    id_solicitacao = _registrar_chave(cliente, chave)
    cliente.post(
        f"/v1/solicitacoes-de-chave/{id_solicitacao}/avaliacao",
        json={"situacao": "aceita", "parecer": "Projeto compatível."},
        headers=_headers(chave, token),
    )

    resposta = cliente.post(
        f"/v1/solicitacoes-de-chave/{id_solicitacao}/avaliacao",
        json={"situacao": "recusada", "parecer": "Mudei de ideia."},
        headers=_headers(chave, token),
    )

    assert resposta.status_code == 409


def test_quem_nao_e_admin_nao_avalia_pedido_de_chave(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste
):
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    mestre = criar_persona(Papel.mestre, criada_por=admin)
    token, _ = criar_sessao_de_teste(mestre)
    id_solicitacao = _registrar_chave(cliente, chave)

    resposta = cliente.post(
        f"/v1/solicitacoes-de-chave/{id_solicitacao}/avaliacao",
        json={"situacao": "aceita", "parecer": "Projeto compatível."},
        headers=_headers(chave, token),
    )

    assert resposta.status_code == 403


# --- Sugestões e propostas (`RF-02-25`, `RF-02-26`) -------------------------


def test_admin_le_a_fila_de_sugestoes(cliente, criar_chave, criar_persona, criar_sessao_de_teste):
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    token, _ = criar_sessao_de_teste(admin)
    guerreiro = criar_persona(Papel.guerreiro)
    token_guerreiro, _ = criar_sessao_de_teste(guerreiro)
    cliente.post(
        "/v1/sugestoes",
        json={"alvo_tipo": "plataforma", "texto": "Podíamos ter um mural entre trilhas."},
        headers=_headers(chave, token_guerreiro),
    )

    resposta = cliente.get("/v1/sugestoes", headers=_headers(chave, token))

    assert resposta.status_code == 200
    item = resposta.json()["itens"][0]
    assert item["autor_id"] == str(guerreiro.id)
    assert item["papel_do_autor"] == Papel.guerreiro.value
    assert item["texto"] == "Podíamos ter um mural entre trilhas."
    assert item["situacao"] == "recebida"


def test_sugestao_com_prazo_vencido_vem_em_atraso(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste, sessao
):
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    token, _ = criar_sessao_de_teste(admin)
    guerreiro = criar_persona(Papel.guerreiro)
    token_guerreiro, _ = criar_sessao_de_teste(guerreiro)
    id_sugestao = cliente.post(
        "/v1/sugestoes",
        json={"alvo_tipo": "plataforma", "texto": "Sugestão qualquer."},
        headers=_headers(chave, token_guerreiro),
    ).json()["id"]
    sugestao = sessao.get(SugestaoOuProposta, id_sugestao)
    sugestao.prazo = agora() - timedelta(seconds=1)
    sessao.commit()

    resposta = cliente.get("/v1/sugestoes", headers=_headers(chave, token))

    item = resposta.json()["itens"][0]
    assert item["em_atraso"] is True


def test_sugestao_adotada_credita_extras_e_badge_na_mesma_operacao(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste, sessao
):
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    token, _ = criar_sessao_de_teste(admin)
    guerreiro = criar_persona(Papel.guerreiro)
    token_guerreiro, _ = criar_sessao_de_teste(guerreiro)
    id_sugestao = cliente.post(
        "/v1/sugestoes",
        json={"alvo_tipo": "plataforma", "texto": "Sugestão qualquer."},
        headers=_headers(chave, token_guerreiro),
    ).json()["id"]

    resposta = cliente.post(
        f"/v1/sugestoes/{id_sugestao}/avaliacao",
        json={"situacao": "adotada", "parecer": "Ótima ideia."},
        headers=_headers(chave, token),
    )

    assert resposta.status_code == 200
    conta = sessao.query(PontoExtra).filter_by(guerreiro_id=guerreiro.id).one()
    assert conta.acumulado == 20
    assert conta.saldo_disponivel == 20
    badge = (
        sessao.query(Badge)
        .filter_by(guerreiro_id=guerreiro.id, tipo=TipoDeBadge.de_protagonismo)
        .one()
    )
    assert badge is not None


def test_regravar_sugestao_adotada_nao_credita_de_novo(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste
):
    """A regra não reavalia (409); o teste confere que a idempotência de
    `avaliar_sugestao` — já coberta em `test_fila.py` — também vale pela
    rota, sem caminho de segundo crédito."""
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    token, _ = criar_sessao_de_teste(admin)
    guerreiro = criar_persona(Papel.guerreiro)
    token_guerreiro, _ = criar_sessao_de_teste(guerreiro)
    id_sugestao = cliente.post(
        "/v1/sugestoes",
        json={"alvo_tipo": "plataforma", "texto": "Sugestão qualquer."},
        headers=_headers(chave, token_guerreiro),
    ).json()["id"]
    cliente.post(
        f"/v1/sugestoes/{id_sugestao}/avaliacao",
        json={"situacao": "adotada", "parecer": "Ótima ideia."},
        headers=_headers(chave, token),
    )

    resposta = cliente.post(
        f"/v1/sugestoes/{id_sugestao}/avaliacao",
        json={"situacao": "adotada", "parecer": "De novo."},
        headers=_headers(chave, token),
    )

    assert resposta.status_code == 409


def test_sugestao_nao_adotada_sem_motivo_e_422(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste
):
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    token, _ = criar_sessao_de_teste(admin)
    guerreiro = criar_persona(Papel.guerreiro)
    token_guerreiro, _ = criar_sessao_de_teste(guerreiro)
    id_sugestao = cliente.post(
        "/v1/sugestoes",
        json={"alvo_tipo": "plataforma", "texto": "Sugestão qualquer."},
        headers=_headers(chave, token_guerreiro),
    ).json()["id"]

    resposta = cliente.post(
        f"/v1/sugestoes/{id_sugestao}/avaliacao",
        json={"situacao": "nao_adotada", "parecer": "Já existe algo parecido."},
        headers=_headers(chave, token),
    )

    assert resposta.status_code == 422


def test_sugestao_nao_adotada_com_motivo_marca_descarte_em_90_dias(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste, sessao
):
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    token, _ = criar_sessao_de_teste(admin)
    guerreiro = criar_persona(Papel.guerreiro)
    token_guerreiro, _ = criar_sessao_de_teste(guerreiro)
    id_sugestao = cliente.post(
        "/v1/sugestoes",
        json={"alvo_tipo": "plataforma", "texto": "Sugestão qualquer."},
        headers=_headers(chave, token_guerreiro),
    ).json()["id"]

    resposta = cliente.post(
        f"/v1/sugestoes/{id_sugestao}/avaliacao",
        json={
            "situacao": "nao_adotada",
            "parecer": "Já existe algo parecido.",
            "motivo_do_retorno": "Já existe um mural na trilha atual.",
        },
        headers=_headers(chave, token),
    )

    assert resposta.status_code == 200
    corpo = resposta.json()
    assert corpo["motivo_do_retorno"] == "Já existe um mural na trilha atual."
    sugestao = sessao.get(SugestaoOuProposta, id_sugestao)
    assert sugestao.descartar_em == sugestao.decidido_em + timedelta(days=90)


def test_reavaliacao_de_sugestao_e_409(cliente, criar_chave, criar_persona, criar_sessao_de_teste):
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    token, _ = criar_sessao_de_teste(admin)
    guerreiro = criar_persona(Papel.guerreiro)
    token_guerreiro, _ = criar_sessao_de_teste(guerreiro)
    id_sugestao = cliente.post(
        "/v1/sugestoes",
        json={"alvo_tipo": "plataforma", "texto": "Sugestão qualquer."},
        headers=_headers(chave, token_guerreiro),
    ).json()["id"]
    cliente.post(
        f"/v1/sugestoes/{id_sugestao}/avaliacao",
        json={"situacao": "nao_adotada", "parecer": "Já existe.", "motivo_do_retorno": "Motivo."},
        headers=_headers(chave, token),
    )

    resposta = cliente.post(
        f"/v1/sugestoes/{id_sugestao}/avaliacao",
        json={"situacao": "nao_adotada", "parecer": "De novo.", "motivo_do_retorno": "Motivo."},
        headers=_headers(chave, token),
    )

    assert resposta.status_code == 409


def test_autor_ve_as_proprias_sugestoes_em_qualquer_situacao(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste
):
    chave, _ = criar_chave()
    guerreiro = criar_persona(Papel.guerreiro)
    token_guerreiro, _ = criar_sessao_de_teste(guerreiro)
    cliente.post(
        "/v1/sugestoes",
        json={"alvo_tipo": "plataforma", "texto": "Sugestão qualquer."},
        headers=_headers(chave, token_guerreiro),
    )

    resposta = cliente.get("/v1/sugestoes/minhas", headers=_headers(chave, token_guerreiro))

    assert resposta.status_code == 200
    item = resposta.json()["itens"][0]
    assert item["texto"] == "Sugestão qualquer."
    assert item["situacao"] == "recebida"
    assert item["alvo_tipo"] == "plataforma"
    assert item["prazo"] is not None


def test_proposta_nao_adotada_devolve_o_motivo_do_retorno(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste
):
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    token_admin, _ = criar_sessao_de_teste(admin)
    mestre = criar_persona(Papel.mestre)
    token_mestre, _ = criar_sessao_de_teste(mestre)
    id_sugestao = cliente.post(
        "/v1/sugestoes",
        json={"alvo_tipo": "plataforma", "texto": "Proposta de evolução."},
        headers=_headers(chave, token_mestre),
    ).json()["id"]
    cliente.post(
        f"/v1/sugestoes/{id_sugestao}/avaliacao",
        json={
            "situacao": "nao_adotada",
            "parecer": "Parecer interno.",
            "motivo_do_retorno": "Já está no roteiro de outra fatia.",
        },
        headers=_headers(chave, token_admin),
    )

    resposta = cliente.get("/v1/sugestoes/minhas", headers=_headers(chave, token_mestre))

    item = resposta.json()["itens"][0]
    assert item["situacao"] == "nao_adotada"
    assert item["motivo_do_retorno"] == "Já está no roteiro de outra fatia."
    assert item["decidido_em"] is not None


def test_proposta_com_prazo_vencido_sai_marcada_em_atraso_pela_minhas(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste, sessao
):
    chave, _ = criar_chave()
    mestre = criar_persona(Papel.mestre)
    token_mestre, _ = criar_sessao_de_teste(mestre)
    id_sugestao = cliente.post(
        "/v1/sugestoes",
        json={"alvo_tipo": "plataforma", "texto": "Proposta qualquer."},
        headers=_headers(chave, token_mestre),
    ).json()["id"]
    sugestao = sessao.get(SugestaoOuProposta, id_sugestao)
    sugestao.prazo = agora() - timedelta(seconds=1)
    sessao.commit()

    resposta = cliente.get("/v1/sugestoes/minhas", headers=_headers(chave, token_mestre))

    item = resposta.json()["itens"][0]
    assert item["em_atraso"] is True
    assert item["situacao"] == "recebida"


def test_minhas_sugestoes_nao_alcanca_proposta_de_outro_autor(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste
):
    chave, _ = criar_chave()
    mestre = criar_persona(Papel.mestre)
    token_mestre, _ = criar_sessao_de_teste(mestre)
    outro_mestre = criar_persona(Papel.mestre)
    token_outro, _ = criar_sessao_de_teste(outro_mestre)
    cliente.post(
        "/v1/sugestoes",
        json={"alvo_tipo": "plataforma", "texto": "Proposta do outro Mestre."},
        headers=_headers(chave, token_outro),
    )

    resposta = cliente.get("/v1/sugestoes/minhas", headers=_headers(chave, token_mestre))

    assert resposta.status_code == 200
    assert resposta.json()["itens"] == []


def test_minhas_sugestoes_nunca_traz_o_parecer_interno(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste
):
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    token_admin, _ = criar_sessao_de_teste(admin)
    mestre = criar_persona(Papel.mestre)
    token_mestre, _ = criar_sessao_de_teste(mestre)
    id_sugestao = cliente.post(
        "/v1/sugestoes",
        json={"alvo_tipo": "plataforma", "texto": "Proposta qualquer."},
        headers=_headers(chave, token_mestre),
    ).json()["id"]
    cliente.post(
        f"/v1/sugestoes/{id_sugestao}/avaliacao",
        json={"situacao": "adotada", "parecer": "Parecer que não pode vazar."},
        headers=_headers(chave, token_admin),
    )

    resposta = cliente.get("/v1/sugestoes/minhas", headers=_headers(chave, token_mestre))

    item = resposta.json()["itens"][0]
    assert "parecer" not in item
