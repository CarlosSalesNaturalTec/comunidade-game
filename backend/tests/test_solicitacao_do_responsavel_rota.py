import uuid
from datetime import timedelta

from nucleo.personas.modelo import Papel
from nucleo.responsaveis.regra import criar_vinculo
from nucleo.solicitacoes_do_responsavel.modelo import SolicitacaoDoResponsavel
from nucleo.tempo import agora


def _montar_vinculo(sessao, criar_persona):
    admin = criar_persona(Papel.admin)
    responsavel = criar_persona(Papel.responsavel, criada_por=admin)
    guerreiro = criar_persona(Papel.guerreiro)
    criar_vinculo(
        sessao,
        responsavel=responsavel,
        guerreiro_id=guerreiro.id,
        grau_de_parentesco="mãe",
        cadastrado_por=admin,
    )
    sessao.commit()
    return admin, responsavel, guerreiro


def test_envio_devolve_so_protocolo_e_prazo(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste, sessao
):
    chave, _ = criar_chave()
    _, responsavel, guerreiro = _montar_vinculo(sessao, criar_persona)
    token, _ = criar_sessao_de_teste(responsavel)

    resposta = cliente.post(
        "/v1/solicitacoes",
        json={"guerreiro_id": str(guerreiro.id), "tipo": "acesso", "texto": "Quero ver os dados."},
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
    )

    assert resposta.status_code == 201
    corpo = resposta.json()
    assert set(corpo.keys()) == {"id", "prazo"}


def test_persona_de_outro_papel_nao_abre_solicitacao(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste, sessao
):
    chave, _ = criar_chave()
    admin, _, guerreiro = _montar_vinculo(sessao, criar_persona)
    mestre = criar_persona(Papel.mestre, criada_por=admin)
    token, _ = criar_sessao_de_teste(mestre)

    resposta = cliente.post(
        "/v1/solicitacoes",
        json={"guerreiro_id": str(guerreiro.id), "tipo": "acesso", "texto": "Pedido."},
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
    )

    assert resposta.status_code == 403
    assert resposta.json()["codigo"] == "permissao_negada"


def test_leitura_das_proprias_nao_alcanca_a_de_outro_responsavel(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste, sessao
):
    chave, _ = criar_chave()
    _, responsavel1, guerreiro1 = _montar_vinculo(sessao, criar_persona)
    _, responsavel2, guerreiro2 = _montar_vinculo(sessao, criar_persona)
    cabecalhos = {"X-Chave-Aplicacao": chave}

    token1, _ = criar_sessao_de_teste(responsavel1)
    cliente.post(
        "/v1/solicitacoes",
        json={"guerreiro_id": str(guerreiro1.id), "tipo": "acesso", "texto": "Pedido 1."},
        headers={**cabecalhos, "Authorization": f"Bearer {token1}"},
    )

    token2, _ = criar_sessao_de_teste(responsavel2)
    cliente.post(
        "/v1/solicitacoes",
        json={"guerreiro_id": str(guerreiro2.id), "tipo": "correcao", "texto": "Pedido 2."},
        headers={**cabecalhos, "Authorization": f"Bearer {token2}"},
    )

    resposta = cliente.get(
        "/v1/eu/solicitacoes",
        headers={**cabecalhos, "Authorization": f"Bearer {token1}"},
    )

    assert resposta.status_code == 200
    corpo = resposta.json()
    assert len(corpo) == 1
    assert corpo[0]["guerreiro_id"] == str(guerreiro1.id)
    assert corpo[0]["tipo"] == "acesso"


def test_fila_do_admin_traz_atraso_e_nicks(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste, criar_nick, sessao
):
    chave, _ = criar_chave()
    admin, responsavel, guerreiro = _montar_vinculo(sessao, criar_persona)
    criar_nick(responsavel, "mae-da-zeferina")
    criar_nick(guerreiro, "zeferina")
    cabecalhos = {"X-Chave-Aplicacao": chave}

    token_do_responsavel, _ = criar_sessao_de_teste(responsavel)
    resposta_de_envio = cliente.post(
        "/v1/solicitacoes",
        json={"guerreiro_id": str(guerreiro.id), "tipo": "acesso", "texto": "Quero ver os dados."},
        headers={**cabecalhos, "Authorization": f"Bearer {token_do_responsavel}"},
    )
    id_da_solicitacao = resposta_de_envio.json()["id"]

    solicitacao = sessao.get(SolicitacaoDoResponsavel, uuid.UUID(id_da_solicitacao))
    solicitacao.prazo = agora() - timedelta(seconds=1)
    sessao.commit()

    token_do_admin, _ = criar_sessao_de_teste(admin)
    resposta = cliente.get(
        "/v1/solicitacoes-do-responsavel",
        headers={**cabecalhos, "Authorization": f"Bearer {token_do_admin}"},
    )

    assert resposta.status_code == 200
    corpo = resposta.json()
    assert len(corpo) == 1
    item = corpo[0]
    assert item["nick_do_responsavel"] == "mae-da-zeferina"
    assert item["nick_do_guerreiro"] == "zeferina"
    assert item["em_atraso"] is True


def test_admin_registra_o_tratamento(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste, sessao
):
    chave, _ = criar_chave()
    admin, responsavel, guerreiro = _montar_vinculo(sessao, criar_persona)
    cabecalhos = {"X-Chave-Aplicacao": chave}

    token_do_responsavel, _ = criar_sessao_de_teste(responsavel)
    resposta_de_envio = cliente.post(
        "/v1/solicitacoes",
        json={"guerreiro_id": str(guerreiro.id), "tipo": "acesso", "texto": "Quero ver os dados."},
        headers={**cabecalhos, "Authorization": f"Bearer {token_do_responsavel}"},
    )
    id_da_solicitacao = resposta_de_envio.json()["id"]

    token_do_admin, _ = criar_sessao_de_teste(admin)
    resposta = cliente.post(
        f"/v1/solicitacoes-do-responsavel/{id_da_solicitacao}/tratamento",
        json={"situacao": "aceita", "desfecho": "Acesso concedido por escrito."},
        headers={**cabecalhos, "Authorization": f"Bearer {token_do_admin}"},
    )

    assert resposta.status_code == 200
    corpo = resposta.json()
    assert corpo["situacao"] == "aceita"
    assert corpo["desfecho"] == "Acesso concedido por escrito."
    assert corpo["tratado_por_id"] == str(admin.id)
    assert corpo["tratado_em"] is not None


def test_mestre_nao_alcanca_a_fila_nem_o_tratamento(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste, sessao
):
    chave, _ = criar_chave()
    admin, responsavel, guerreiro = _montar_vinculo(sessao, criar_persona)
    mestre = criar_persona(Papel.mestre, criada_por=admin)
    cabecalhos = {"X-Chave-Aplicacao": chave}

    token_do_responsavel, _ = criar_sessao_de_teste(responsavel)
    resposta_de_envio = cliente.post(
        "/v1/solicitacoes",
        json={"guerreiro_id": str(guerreiro.id), "tipo": "acesso", "texto": "Quero ver os dados."},
        headers={**cabecalhos, "Authorization": f"Bearer {token_do_responsavel}"},
    )
    id_da_solicitacao = resposta_de_envio.json()["id"]

    token_do_mestre, _ = criar_sessao_de_teste(mestre)

    resposta_da_fila = cliente.get(
        "/v1/solicitacoes-do-responsavel",
        headers={**cabecalhos, "Authorization": f"Bearer {token_do_mestre}"},
    )
    assert resposta_da_fila.status_code == 403

    resposta_do_tratamento = cliente.post(
        f"/v1/solicitacoes-do-responsavel/{id_da_solicitacao}/tratamento",
        json={"situacao": "aceita"},
        headers={**cabecalhos, "Authorization": f"Bearer {token_do_mestre}"},
    )
    assert resposta_do_tratamento.status_code == 403
