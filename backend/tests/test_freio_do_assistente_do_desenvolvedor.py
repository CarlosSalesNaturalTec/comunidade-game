"""Freio por origem sobre a consulta ao assistente do Desenvolvedor
(`RN-03-08`, `RN-03-35`, decisão do fundador de 2026-09-29, change
`2026-09-29-area-do-apoiador-desenvolvedor`)."""

import pytest

from nucleo.assistente.desenvolvedor.fabrica import (
    dependencia_do_assistente_do_desenvolvedor,
)
from nucleo.assistente.desenvolvedor.porta import (
    PortaDoAssistenteDoDesenvolvedor,
    RespostaDoDesenvolvedor,
)

CAMINHO = "/v1/assistente-do-desenvolvedor"
PERGUNTA = {"texto": "Como funciona a chave de aplicação?"}


class PortaQueConta(PortaDoAssistenteDoDesenvolvedor):
    def __init__(self) -> None:
        self.chamadas = 0

    def responder(self, *, texto, corpus, historico):
        self.chamadas += 1
        return RespostaDoDesenvolvedor(desfecho="respondida", resposta="Resposta.", opcoes=("Uma",))


@pytest.fixture
def porta_que_conta(app):
    porta = PortaQueConta()
    app.dependency_overrides[dependencia_do_assistente_do_desenvolvedor] = lambda: porta
    return porta


def test_repeticao_encontra_429_com_o_tempo_de_espera_e_nada_vai_ao_modelo(
    cliente_com_origem, criar_chave, sobrescrever_configuracao, porta_que_conta
):
    sobrescrever_configuracao(protecao_freio_assistente_do_desenvolvedor_limite=1)
    chave, _ = criar_chave()
    cliente = cliente_com_origem()
    cabecalhos = {"X-Chave-Aplicacao": chave}

    primeira = cliente.post(CAMINHO, json=PERGUNTA, headers=cabecalhos)
    segunda = cliente.post(CAMINHO, json=PERGUNTA, headers=cabecalhos)

    assert primeira.status_code == 200
    assert segunda.status_code == 429
    corpo = segunda.json()
    assert corpo["codigo"] == "freio_por_origem_acionado"
    assert "Tente novamente em" in corpo["mensagem"]
    assert porta_que_conta.chamadas == 1


def test_origens_distintas_nao_dividem_o_freio_do_assistente(
    cliente_com_origem, criar_chave, sobrescrever_configuracao, porta_que_conta
):
    sobrescrever_configuracao(protecao_freio_assistente_do_desenvolvedor_limite=1)
    chave, _ = criar_chave()
    cabecalhos = {"X-Chave-Aplicacao": chave}
    primeira_origem = cliente_com_origem("203.0.113.10")
    segunda_origem = cliente_com_origem("203.0.113.11")

    primeira_origem.post(CAMINHO, json=PERGUNTA, headers=cabecalhos)
    primeira_origem.post(CAMINHO, json=PERGUNTA, headers=cabecalhos)
    resposta = segunda_origem.post(CAMINHO, json=PERGUNTA, headers=cabecalhos)

    assert resposta.status_code == 200


def test_freio_do_assistente_nao_alcanca_a_solicitacao_de_chave(
    cliente_com_origem, criar_chave, sobrescrever_configuracao, porta_que_conta
):
    """`RN-03-35`: nova solicitação de chave é sempre possível, mesmo depois de
    a origem ser freada no assistente."""
    sobrescrever_configuracao(protecao_freio_assistente_do_desenvolvedor_limite=1)
    chave, _ = criar_chave()
    cliente = cliente_com_origem()
    cabecalhos = {"X-Chave-Aplicacao": chave}

    cliente.post(CAMINHO, json=PERGUNTA, headers=cabecalhos)
    assert cliente.post(CAMINHO, json=PERGUNTA, headers=cabecalhos).status_code == 429

    solicitacoes = [
        cliente.post(
            "/v1/solicitacoes-de-chave",
            json={
                "solicitante": "Desenvolvedora de Tal",
                "contato": "dev@example.org",
                "o_que_pretende_construir": "Um painel comunitário.",
            },
            headers=cabecalhos,
        )
        for _ in range(5)
    ]

    assert all(resposta.status_code == 201 for resposta in solicitacoes)
