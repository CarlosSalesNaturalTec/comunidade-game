"""A porta do assistente de trilhas — `RF-04-36`, `RF-04-40`, design —
decisões 1, 3 e 4."""

import json

import httpx

from nucleo.assistente.local import AssistenteDeTrilhasLocal
from nucleo.assistente.nuvem import AssistenteDeTrilhasNaNuvem

_CORPUS = "Missão: Programação\nVariável é um espaço na memória para guardar um valor."


def test_local_responde_pergunta_sobre_o_corpus():
    porta = AssistenteDeTrilhasLocal()

    resposta = porta.responder(texto="O que é uma variável?", arquivo=None, corpus=_CORPUS)

    assert resposta is not None
    assert resposta.desfecho == "respondida"
    assert resposta.transcricao_da_pergunta == "O que é uma variável?"
    assert resposta.resposta


def test_local_recusa_pergunta_fora_do_corpus():
    porta = AssistenteDeTrilhasLocal()

    resposta = porta.responder(texto="Qual é a capital da Mongólia?", arquivo=None, corpus=_CORPUS)

    assert resposta is not None
    assert resposta.desfecho == "fora_do_corpus"


def test_local_encaminha_tarefa_escolar():
    porta = AssistenteDeTrilhasLocal()

    resposta = porta.responder(
        texto="Preciso fazer o dever de casa de matemática", arquivo=None, corpus=_CORPUS
    )

    assert resposta is not None
    assert resposta.desfecho == "tarefa_escolar"


def test_local_transcreve_audio_sem_expor_os_bytes():
    porta = AssistenteDeTrilhasLocal()

    resposta = porta.responder(texto=None, arquivo=b"segredo-do-audio", corpus=_CORPUS)

    assert resposta is not None
    assert "segredo-do-audio" not in resposta.transcricao_da_pergunta


class _RespostaFake:
    def __init__(self, corpo: dict):
        self._corpo = corpo

    def raise_for_status(self):
        pass

    def json(self):
        return self._corpo


def _corpo_gemini(texto: str) -> dict:
    return {"candidates": [{"content": {"parts": [{"text": texto}]}}]}


def test_nuvem_sem_chave_devolve_none():
    porta = AssistenteDeTrilhasNaNuvem(chave_de_api="", modelo="gemini-2.5-flash")

    assert porta.responder(texto="Uma pergunta", arquivo=None, corpus=_CORPUS) is None


def test_nuvem_devolve_none_em_erro_de_transporte(monkeypatch):
    def _levanta(*args, **kwargs):
        raise httpx.ConnectError("rede indisponível")

    monkeypatch.setattr(httpx, "post", _levanta)
    porta = AssistenteDeTrilhasNaNuvem(chave_de_api="chave-de-teste", modelo="gemini-2.5-flash")

    assert porta.responder(texto="Uma pergunta", arquivo=None, corpus=_CORPUS) is None


def test_nuvem_devolve_none_em_demora(monkeypatch):
    def _levanta(*args, **kwargs):
        raise httpx.TimeoutException("sem resposta a tempo")

    monkeypatch.setattr(httpx, "post", _levanta)
    porta = AssistenteDeTrilhasNaNuvem(chave_de_api="chave-de-teste", modelo="gemini-2.5-flash")

    assert porta.responder(texto="Uma pergunta", arquivo=None, corpus=_CORPUS) is None


def test_nuvem_devolve_none_em_json_fora_do_formato(monkeypatch):
    corpo = _corpo_gemini(json.dumps({"desfecho": "respondida"}))
    monkeypatch.setattr(httpx, "post", lambda *a, **k: _RespostaFake(corpo))
    porta = AssistenteDeTrilhasNaNuvem(chave_de_api="chave-de-teste", modelo="gemini-2.5-flash")

    assert porta.responder(texto="Uma pergunta", arquivo=None, corpus=_CORPUS) is None


def test_nuvem_responde_com_json_valido(monkeypatch):
    corpo = _corpo_gemini(
        json.dumps(
            {
                "transcricao_da_pergunta": "O que é uma variável?",
                "desfecho": "respondida",
                "resposta": "É um espaço na memória.",
            }
        )
    )
    monkeypatch.setattr(httpx, "post", lambda *a, **k: _RespostaFake(corpo))
    porta = AssistenteDeTrilhasNaNuvem(chave_de_api="chave-de-teste", modelo="gemini-2.5-flash")

    resposta = porta.responder(texto="O que é uma variável?", arquivo=None, corpus=_CORPUS)

    assert resposta is not None
    assert resposta.desfecho == "respondida"
    assert resposta.resposta == "É um espaço na memória."


def test_nuvem_nao_registra_o_byte_do_audio_em_log(monkeypatch, caplog):
    def _levanta(*args, **kwargs):
        raise httpx.ConnectError("rede indisponível")

    monkeypatch.setattr(httpx, "post", _levanta)
    porta = AssistenteDeTrilhasNaNuvem(chave_de_api="chave-de-teste", modelo="gemini-2.5-flash")

    with caplog.at_level("WARNING", logger="nucleo.assistente"):
        porta.responder(texto=None, arquivo=b"segredo-do-audio", corpus=_CORPUS)

    texto_do_log = " ".join(registro.getMessage() for registro in caplog.records)
    assert "segredo-do-audio" not in texto_do_log
