"""Assistente da Área do Apoiador Desenvolvedor (`RF-03-69` a `RF-03-72`,
`RN-03-29`, `RN-03-30`, change `2026-09-29-area-do-apoiador-desenvolvedor`)."""

import json

import pytest

from nucleo.assistente.desenvolvedor.fabrica import (
    dependencia_do_assistente_do_desenvolvedor,
)
from nucleo.assistente.desenvolvedor.porta import (
    PortaDoAssistenteDoDesenvolvedor,
    RespostaDoDesenvolvedor,
)
from nucleo.assistente.desenvolvedor.regra import OPCOES_FIXAS
from nucleo.assistente.modelo import ConsultaAoAssistente
from nucleo.corpus_do_desenvolvedor.bloco import BlocoDoCorpus
from nucleo.corpus_do_desenvolvedor.montagem import escrever

CAMINHO = "/v1/assistente-do-desenvolvedor"


class PortaDeTeste(PortaDoAssistenteDoDesenvolvedor):
    def __init__(self, resposta: RespostaDoDesenvolvedor | None) -> None:
        self.resposta = resposta
        self.corpus_recebido: str | None = None
        self.historico_recebido: tuple = ()

    def responder(self, *, texto, corpus, historico):
        self.corpus_recebido = corpus
        self.historico_recebido = historico
        return self.resposta


@pytest.fixture
def corpus_semeado(tmp_path, sobrescrever_configuracao):
    """Artefato pequeno no lugar do que a esteira monta (design — decisão 1)."""
    saida = tmp_path / "corpus.json"
    escrever(
        [
            BlocoDoCorpus(
                origem="docs/03-plataforma-e-arquitetura.md",
                titulo="Arquitetura — Chave de aplicação",
                texto="Sem chave a API não responde, e a chave não amplia direito de escrita.",
            )
        ],
        saida,
    )
    sobrescrever_configuracao(corpus_do_desenvolvedor_caminho=saida)
    return saida


@pytest.fixture
def com_porta(app):
    def _com_porta(resposta: RespostaDoDesenvolvedor | None) -> PortaDeTeste:
        porta = PortaDeTeste(resposta)
        app.dependency_overrides[dependencia_do_assistente_do_desenvolvedor] = lambda: porta
        return porta

    return _com_porta


def _perguntar(cliente, chave, **extras):
    corpo = {"texto": "Como funciona a chave de aplicação?"} | extras
    return cliente.post(CAMINHO, json=corpo, headers={"X-Chave-Aplicacao": chave})


def test_pergunta_respondida_pelo_corpus_sai_com_a_escolha_do_proximo_passo(
    cliente, criar_chave, corpus_semeado, com_porta
):
    chave, _ = criar_chave()
    porta = com_porta(
        RespostaDoDesenvolvedor(
            desfecho="respondida",
            resposta="A chave vai no cabeçalho.",
            opcoes=("Como pedir a chave",),
        )
    )

    resposta = _perguntar(cliente, chave)

    assert resposta.status_code == 200
    corpo = resposta.json()
    assert corpo["desfecho"] == "respondida"
    assert corpo["resposta"] == "A chave vai no cabeçalho."
    assert corpo["opcoes"] == ["Como pedir a chave"]
    assert "Sem chave a API não responde" in porta.corpus_recebido


def test_pergunta_fora_do_corpus_recebe_nao_sei_com_o_caminho_da_documentacao(
    cliente, criar_chave, corpus_semeado, com_porta
):
    chave, _ = criar_chave()
    com_porta(RespostaDoDesenvolvedor(desfecho="fora_do_corpus", resposta=None, opcoes=()))

    corpo = _perguntar(cliente, chave).json()

    assert corpo["desfecho"] == "fora_do_corpus"
    assert "só respondo a partir deles" in corpo["resposta"]
    assert "documentação" in corpo["resposta"]
    assert corpo["opcoes"] == list(OPCOES_FIXAS)


def test_resposta_do_modelo_sem_opcoes_recebe_o_conjunto_fixo(
    cliente, criar_chave, corpus_semeado, com_porta
):
    """Nenhuma mensagem sai sem pergunta de múltipla escolha (`RF-03-69`)."""
    chave, _ = criar_chave()
    com_porta(RespostaDoDesenvolvedor(desfecho="respondida", resposta="Resposta.", opcoes=()))

    corpo = _perguntar(cliente, chave).json()

    assert corpo["opcoes"] == list(OPCOES_FIXAS)


def test_assistente_fora_do_ar_devolve_indisponibilidade_declarada(
    cliente, criar_chave, corpus_semeado, com_porta
):
    chave, _ = criar_chave()
    com_porta(None)

    resposta = _perguntar(cliente, chave)

    assert resposta.status_code == 503
    corpo = resposta.json()
    assert corpo["codigo"] == "assistente_do_desenvolvedor_indisponivel"
    assert "voltará" in corpo["mensagem"]


def test_campo_que_descreve_o_visitante_e_recusado(cliente, criar_chave, corpus_semeado, com_porta):
    """`RF-03-71`: o assistente não coleta nem pede dado pessoal do visitante."""
    chave, _ = criar_chave()
    porta = com_porta(
        RespostaDoDesenvolvedor(desfecho="respondida", resposta="Resposta.", opcoes=("Uma",))
    )

    resposta = _perguntar(cliente, chave, email="visitante@example.org")

    assert resposta.status_code == 422
    assert porta.corpus_recebido is None


def test_historico_viaja_com_a_pergunta_e_nao_e_gravado(
    cliente, criar_chave, corpus_semeado, com_porta, sessao
):
    chave, _ = criar_chave()
    porta = com_porta(
        RespostaDoDesenvolvedor(desfecho="respondida", resposta="Resposta.", opcoes=("Uma",))
    )

    resposta = _perguntar(
        cliente,
        chave,
        historico=[
            {"de": "assistente", "texto": "A plataforma tem oito aplicações."},
            {"de": "visitante", "texto": "Quais?"},
        ],
    )

    assert resposta.status_code == 200
    assert [mensagem.de for mensagem in porta.historico_recebido] == ["assistente", "visitante"]
    assert sessao.query(ConsultaAoAssistente).count() == 0


def test_nenhuma_consulta_e_gravada_em_nenhum_desfecho(
    cliente, criar_chave, corpus_semeado, com_porta, sessao
):
    """PRD-03 §8: a conversa some ao fechar a página, e nada dela é guardado —
    nem a consulta ao assistente da equipe e do Guerreiro(a) é tocada."""
    chave, _ = criar_chave()

    for resposta_da_porta in (
        RespostaDoDesenvolvedor(desfecho="respondida", resposta="Resposta.", opcoes=("Uma",)),
        RespostaDoDesenvolvedor(desfecho="fora_do_corpus", resposta=None, opcoes=()),
        None,
    ):
        com_porta(resposta_da_porta)
        _perguntar(cliente, chave)

    assert sessao.query(ConsultaAoAssistente).count() == 0


def test_pergunta_vazia_e_recusada(cliente, criar_chave, corpus_semeado, com_porta):
    chave, _ = criar_chave()
    com_porta(RespostaDoDesenvolvedor(desfecho="respondida", resposta="Resposta.", opcoes=()))

    resposta = cliente.post(CAMINHO, json={"texto": "  "}, headers={"X-Chave-Aplicacao": chave})

    assert resposta.status_code == 422


def test_adaptador_da_nuvem_valida_o_json_do_modelo():
    from nucleo.assistente.desenvolvedor.nuvem import _validar_resposta

    assert _validar_resposta({"desfecho": "tarefa_escolar", "resposta": "x"}) is None
    assert _validar_resposta({"desfecho": "respondida", "resposta": None}) is None
    validada = _validar_resposta(
        json.loads('{"desfecho": "respondida", "resposta": "R", "opcoes": ["a", "", "b"]}')
    )
    assert validada.opcoes == ("a", "b")
