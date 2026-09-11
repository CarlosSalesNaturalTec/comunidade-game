"""A porta do assistente de trilhas — `RF-04-36`, `RF-04-40`, `RN-04-21`,
design — decisões 1 e 3. A pergunta chega sempre transcrita no aparelho: a
porta nunca recebe áudio."""

import json
import logging

import httpx

from nucleo.assistente.local import AssistenteDeTrilhasLocal
from nucleo.assistente.nuvem import AssistenteDeTrilhasNaNuvem

_CORPUS = "Missão: Programação\nVariável é um espaço na memória para guardar um valor."


def test_local_responde_pergunta_sobre_o_corpus():
    porta = AssistenteDeTrilhasLocal()

    resposta = porta.responder(texto="O que é uma variável?", corpus=_CORPUS)

    assert resposta is not None
    assert resposta.desfecho == "respondida"
    assert resposta.transcricao_da_pergunta == "O que é uma variável?"
    assert resposta.resposta


def test_local_recusa_pergunta_fora_do_corpus():
    porta = AssistenteDeTrilhasLocal()

    resposta = porta.responder(texto="Qual é a capital da Mongólia?", corpus=_CORPUS)

    assert resposta is not None
    assert resposta.desfecho == "fora_do_corpus"


def test_local_encaminha_tarefa_escolar():
    porta = AssistenteDeTrilhasLocal()

    resposta = porta.responder(texto="Preciso fazer o dever de casa de matemática", corpus=_CORPUS)

    assert resposta is not None
    assert resposta.desfecho == "tarefa_escolar"


class _RespostaFake:
    def __init__(self, corpo: dict):
        self._corpo = corpo

    def raise_for_status(self):
        pass

    def json(self):
        return self._corpo


def _corpo_gemini(texto: str) -> dict:
    return {"candidates": [{"content": {"parts": [{"text": texto}]}}]}


def test_nuvem_sem_chave_devolve_none_e_registra_a_causa(caplog):
    porta = AssistenteDeTrilhasNaNuvem(chave_de_api="", modelo="gemini-2.5-flash")

    with caplog.at_level(logging.WARNING, logger="nucleo.assistente"):
        assert porta.responder(texto="Uma pergunta", corpus=_CORPUS) is None

    assert "Chave de API do Gemini ausente" in caplog.text


def test_nuvem_devolve_none_em_erro_de_transporte(monkeypatch):
    def _levanta(*args, **kwargs):
        raise httpx.ConnectError("rede indisponível")

    monkeypatch.setattr(httpx, "post", _levanta)
    porta = AssistenteDeTrilhasNaNuvem(chave_de_api="chave-de-teste", modelo="gemini-2.5-flash")

    assert porta.responder(texto="Uma pergunta", corpus=_CORPUS) is None


def test_nuvem_devolve_none_em_demora(monkeypatch):
    def _levanta(*args, **kwargs):
        raise httpx.TimeoutException("sem resposta a tempo")

    monkeypatch.setattr(httpx, "post", _levanta)
    porta = AssistenteDeTrilhasNaNuvem(chave_de_api="chave-de-teste", modelo="gemini-2.5-flash")

    assert porta.responder(texto="Uma pergunta", corpus=_CORPUS) is None


def test_nuvem_devolve_none_e_registra_json_fora_do_formato(monkeypatch, caplog):
    """O validador devolve `None` de dentro do `try`, sem exceção: sem a linha
    própria a causa ficaria indistinguível da chave ausente."""
    corpo = _corpo_gemini(json.dumps({"desfecho": "respondida"}))
    monkeypatch.setattr(httpx, "post", lambda *a, **k: _RespostaFake(corpo))
    porta = AssistenteDeTrilhasNaNuvem(chave_de_api="chave-de-teste", modelo="gemini-2.5-flash")

    with caplog.at_level(logging.WARNING, logger="nucleo.assistente"):
        assert porta.responder(texto="Uma pergunta", corpus=_CORPUS) is None

    assert "fora do formato esperado" in caplog.text


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

    resposta = porta.responder(texto="O que é uma variável?", corpus=_CORPUS)

    assert resposta is not None
    assert resposta.desfecho == "respondida"
    assert resposta.resposta == "É um espaço na memória."


def test_nuvem_manda_so_texto_ao_gemini(monkeypatch):
    """`RF-04-40`, `RN-04-21`: a fala já chega transcrita no aparelho, e a
    passada ao Gemini não leva `inlineData` de áudio algum — só as duas
    partes de texto, instrução e pergunta."""
    capturado = {}

    def _capturar(url, **kwargs):
        capturado["partes"] = kwargs["json"]["contents"][0]["parts"]
        return _RespostaFake(
            _corpo_gemini(
                json.dumps(
                    {"desfecho": "respondida", "transcricao_da_pergunta": "P", "resposta": "R"}
                )
            )
        )

    monkeypatch.setattr(httpx, "post", _capturar)
    porta = AssistenteDeTrilhasNaNuvem(chave_de_api="chave-de-teste", modelo="gemini-2.5-flash")

    assert porta.responder(texto="Uma pergunta", corpus=_CORPUS) is not None

    assert len(capturado["partes"]) == 2
    assert all("inlineData" not in parte for parte in capturado["partes"])
    assert all("text" in parte for parte in capturado["partes"])


class _RespostaDeErro:
    def __init__(self, codigo: int, corpo: str):
        self.status_code = codigo
        self.text = corpo

    def raise_for_status(self):
        raise httpx.HTTPStatusError("erro", request=None, response=self)


def test_a_credencial_do_gemini_vai_no_cabecalho_e_nunca_na_url(monkeypatch):
    """A URL entra na mensagem da `HTTPStatusError`, que o log registra:
    chave na _query string_ vira segredo em texto claro (change
    `template-da-missao-no-deepseek`, design — decisão 4)."""
    capturado = {}

    def _capturar(url, **kwargs):
        capturado["url"] = url
        capturado["headers"] = kwargs.get("headers", {})
        return _RespostaFake(
            _corpo_gemini(
                json.dumps(
                    {"desfecho": "respondida", "transcricao_da_pergunta": "P", "resposta": "R"}
                )
            )
        )

    monkeypatch.setattr(httpx, "post", _capturar)
    porta = AssistenteDeTrilhasNaNuvem(chave_de_api="chave-secreta", modelo="gemini-2.5-flash")

    assert porta.responder(texto="Uma pergunta", corpus=_CORPUS) is not None
    assert "chave-secreta" not in capturado["url"]
    assert capturado["headers"]["x-goog-api-key"] == "chave-secreta"


def test_o_corpo_do_erro_de_http_entra_no_log(monkeypatch, caplog):
    corpo = '{"error": {"code": 429, "message": "prepayment credits are depleted"}}'
    monkeypatch.setattr(httpx, "post", lambda *a, **k: _RespostaDeErro(429, corpo))
    porta = AssistenteDeTrilhasNaNuvem(chave_de_api="chave-secreta", modelo="gemini-2.5-flash")

    with caplog.at_level(logging.WARNING, logger="nucleo.assistente"):
        assert porta.responder(texto="Uma pergunta", corpus=_CORPUS) is None

    assert "429" in caplog.text
    assert "prepayment credits are depleted" in caplog.text
    assert "chave-secreta" not in caplog.text
