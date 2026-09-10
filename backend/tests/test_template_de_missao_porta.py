"""O adaptador de produção do template da missão — `RF-09-85`, `RF-09-91`.

Esta porta manda **só texto** e por isso é a que o documento 03 §1.12 destina
ao DeepSeek; `producoes` e `assistente` leem imagem e áudio e seguem no
Gemini. Nenhuma causa de indisponibilidade é muda, nenhuma vira exceção, e a
credencial nunca entra na URL — a mensagem de uma `HTTPStatusError` a levaria
ao log em texto claro (changes `chave-do-gemini-em-producao` e
`template-da-missao-no-deepseek`)."""

import json
import logging

import httpx

from nucleo.template_de_missao.nuvem import TemplateDeMissaoNaNuvem

_LOGGER = "nucleo.template_de_missao"

_ESTRUTURA_VALIDA = {
    "atividades": [
        {
            "titulo": "Mapa da horta",
            "modalidade": "em_equipe",
            "formato": "presencial",
            "natureza": "construcao",
            "producao_esperada": "Um mapa desenhado da horta.",
            "desplugada": True,
        }
    ],
    "objetivo_ods": 2,
    "meta_ods": "2.4",
}


class _RespostaFake:
    def __init__(self, corpo: dict):
        self._corpo = corpo

    def raise_for_status(self):
        pass

    def json(self):
        return self._corpo


def _corpo_do_modelo(texto: str) -> dict:
    """A forma de _chat completions_, que o DeepSeek fala."""
    return {"choices": [{"message": {"content": texto}}]}


def _pedir(porta):
    return porta.sugerir_estrutura(topico="horta comunitária", exigir_atividade_desplugada=True)


def test_nuvem_sem_chave_devolve_none_e_registra_a_causa(caplog):
    porta = TemplateDeMissaoNaNuvem(chave_de_api="", modelo="deepseek-v4-flash")

    with caplog.at_level(logging.WARNING, logger=_LOGGER):
        assert _pedir(porta) is None

    assert "Chave de API do DeepSeek ausente" in caplog.text


def test_nuvem_sem_chave_nao_chega_a_chamar_o_modelo(monkeypatch):
    def _nao_deve_ser_chamado(*args, **kwargs):
        raise AssertionError("sem chave, o adaptador não pode alcançar a rede")

    monkeypatch.setattr(httpx, "post", _nao_deve_ser_chamado)
    porta = TemplateDeMissaoNaNuvem(chave_de_api="", modelo="deepseek-v4-flash")

    assert _pedir(porta) is None


def test_nuvem_devolve_none_em_erro_de_transporte(monkeypatch, caplog):
    def _levanta(*args, **kwargs):
        raise httpx.ConnectError("rede indisponível")

    monkeypatch.setattr(httpx, "post", _levanta)
    porta = TemplateDeMissaoNaNuvem(chave_de_api="chave-de-teste", modelo="deepseek-v4-flash")

    with caplog.at_level(logging.WARNING, logger=_LOGGER):
        assert _pedir(porta) is None

    assert "Falha ao consultar a estrutura da missão no DeepSeek." in caplog.text


def test_nuvem_devolve_none_em_demora(monkeypatch):
    def _levanta(*args, **kwargs):
        raise httpx.TimeoutException("sem resposta a tempo")

    monkeypatch.setattr(httpx, "post", _levanta)
    porta = TemplateDeMissaoNaNuvem(chave_de_api="chave-de-teste", modelo="deepseek-v4-flash")

    assert _pedir(porta) is None


def test_nuvem_devolve_none_e_registra_json_fora_do_formato(monkeypatch, caplog):
    """Este caminho não levanta exceção: o validador devolve `None` de dentro
    do `try`, e sem a linha própria a causa ficaria indistinguível da chave
    ausente."""
    corpo = _corpo_do_modelo(json.dumps({"atividades": []}))
    monkeypatch.setattr(httpx, "post", lambda *a, **k: _RespostaFake(corpo))
    porta = TemplateDeMissaoNaNuvem(chave_de_api="chave-de-teste", modelo="deepseek-v4-flash")

    with caplog.at_level(logging.WARNING, logger=_LOGGER):
        assert _pedir(porta) is None

    assert "fora do formato esperado" in caplog.text


def test_nuvem_devolve_a_estrutura_quando_o_modelo_responde(monkeypatch, caplog):
    corpo = _corpo_do_modelo(f"```json\n{json.dumps(_ESTRUTURA_VALIDA)}\n```")
    monkeypatch.setattr(httpx, "post", lambda *a, **k: _RespostaFake(corpo))
    porta = TemplateDeMissaoNaNuvem(chave_de_api="chave-de-teste", modelo="deepseek-v4-flash")

    with caplog.at_level(logging.WARNING, logger=_LOGGER):
        estrutura = _pedir(porta)

    assert estrutura is not None
    assert [atividade.titulo for atividade in estrutura.atividades] == ["Mapa da horta"]
    assert estrutura.atividades[0].desplugada is True
    assert estrutura.objetivo_ods == 2
    assert caplog.text == ""


class _RespostaDeErro:
    """Uma resposta de erro de verdade: `raise_for_status` levanta a
    `HTTPStatusError` que carrega `response`, e é dela que sai o corpo."""

    def __init__(self, codigo: int, corpo: str):
        self.status_code = codigo
        self.text = corpo

    def raise_for_status(self):
        raise httpx.HTTPStatusError("erro", request=None, response=self)


def test_a_credencial_vai_no_cabecalho_e_nunca_na_url(monkeypatch):
    """A mensagem de uma `HTTPStatusError` carrega a URL inteira: chave na
    _query string_ vira segredo em texto claro no Cloud Logging."""
    capturado = {}

    def _capturar(url, **kwargs):
        capturado["url"] = url
        capturado["headers"] = kwargs.get("headers", {})
        capturado["json"] = kwargs.get("json", {})
        return _RespostaFake(_corpo_do_modelo(json.dumps(_ESTRUTURA_VALIDA)))

    monkeypatch.setattr(httpx, "post", _capturar)
    porta = TemplateDeMissaoNaNuvem(chave_de_api="chave-secreta", modelo="deepseek-v4-flash")

    assert _pedir(porta) is not None
    assert "chave-secreta" not in capturado["url"]
    assert capturado["headers"]["Authorization"] == "Bearer chave-secreta"
    assert capturado["json"]["model"] == "deepseek-v4-flash"
    assert capturado["json"]["response_format"] == {"type": "json_object"}


def test_o_corpo_do_erro_de_http_entra_no_log(monkeypatch, caplog):
    """O provedor explica a causa no corpo — modelo indisponível, crédito
    esgotado —, e o `raise_for_status` a descartava. Sem isto, cada
    diagnóstico custa uma rodada."""
    corpo = '{"error": {"code": 402, "message": "Insufficient Balance"}}'
    monkeypatch.setattr(httpx, "post", lambda *a, **k: _RespostaDeErro(402, corpo))
    porta = TemplateDeMissaoNaNuvem(chave_de_api="chave-de-teste", modelo="deepseek-v4-flash")

    with caplog.at_level(logging.WARNING, logger=_LOGGER):
        assert _pedir(porta) is None

    assert "402" in caplog.text
    assert "Insufficient Balance" in caplog.text


def test_o_corpo_logado_e_truncado(monkeypatch, caplog):
    """Resposta de erro é curta, mas não tem teto declarado: log não é lugar
    de despejo."""
    monkeypatch.setattr(httpx, "post", lambda *a, **k: _RespostaDeErro(500, "x" * 5000))
    porta = TemplateDeMissaoNaNuvem(chave_de_api="chave-de-teste", modelo="deepseek-v4-flash")

    with caplog.at_level(logging.WARNING, logger=_LOGGER):
        assert _pedir(porta) is None

    assert len(caplog.text) < 2000


def test_a_credencial_nunca_aparece_no_log_do_erro(monkeypatch, caplog):
    monkeypatch.setattr(httpx, "post", lambda *a, **k: _RespostaDeErro(401, "Unauthorized"))
    porta = TemplateDeMissaoNaNuvem(chave_de_api="chave-secretissima", modelo="deepseek-v4-flash")

    with caplog.at_level(logging.WARNING, logger=_LOGGER):
        assert _pedir(porta) is None

    assert "chave-secretissima" not in caplog.text
