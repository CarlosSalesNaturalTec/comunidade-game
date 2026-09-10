"""O adaptador de produção do template da missão — `RF-09-85`, `RF-09-91`,
design da change `chave-do-gemini-em-producao` — decisão 3: nenhuma causa de
indisponibilidade é muda, e nenhuma delas vira exceção."""

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


def _corpo_gemini(texto: str) -> dict:
    return {"candidates": [{"content": {"parts": [{"text": texto}]}}]}


def _pedir(porta):
    return porta.sugerir_estrutura(topico="horta comunitária", exigir_atividade_desplugada=True)


def test_nuvem_sem_chave_devolve_none_e_registra_a_causa(caplog):
    porta = TemplateDeMissaoNaNuvem(chave_de_api="", modelo="gemini-2.5-flash")

    with caplog.at_level(logging.WARNING, logger=_LOGGER):
        assert _pedir(porta) is None

    assert "Chave de API do Gemini ausente" in caplog.text


def test_nuvem_sem_chave_nao_chega_a_chamar_o_modelo(monkeypatch):
    def _nao_deve_ser_chamado(*args, **kwargs):
        raise AssertionError("sem chave, o adaptador não pode alcançar a rede")

    monkeypatch.setattr(httpx, "post", _nao_deve_ser_chamado)
    porta = TemplateDeMissaoNaNuvem(chave_de_api="", modelo="gemini-2.5-flash")

    assert _pedir(porta) is None


def test_nuvem_devolve_none_em_erro_de_transporte(monkeypatch, caplog):
    def _levanta(*args, **kwargs):
        raise httpx.ConnectError("rede indisponível")

    monkeypatch.setattr(httpx, "post", _levanta)
    porta = TemplateDeMissaoNaNuvem(chave_de_api="chave-de-teste", modelo="gemini-2.5-flash")

    with caplog.at_level(logging.WARNING, logger=_LOGGER):
        assert _pedir(porta) is None

    assert "Falha ao consultar o template da missão no Gemini." in caplog.text


def test_nuvem_devolve_none_em_demora(monkeypatch):
    def _levanta(*args, **kwargs):
        raise httpx.TimeoutException("sem resposta a tempo")

    monkeypatch.setattr(httpx, "post", _levanta)
    porta = TemplateDeMissaoNaNuvem(chave_de_api="chave-de-teste", modelo="gemini-2.5-flash")

    assert _pedir(porta) is None


def test_nuvem_devolve_none_e_registra_json_fora_do_formato(monkeypatch, caplog):
    """Este caminho não levanta exceção: o validador devolve `None` de dentro
    do `try`, e sem a linha própria a causa ficaria indistinguível da chave
    ausente."""
    corpo = _corpo_gemini(json.dumps({"atividades": []}))
    monkeypatch.setattr(httpx, "post", lambda *a, **k: _RespostaFake(corpo))
    porta = TemplateDeMissaoNaNuvem(chave_de_api="chave-de-teste", modelo="gemini-2.5-flash")

    with caplog.at_level(logging.WARNING, logger=_LOGGER):
        assert _pedir(porta) is None

    assert "fora do formato esperado" in caplog.text


def test_nuvem_devolve_a_estrutura_quando_o_modelo_responde(monkeypatch, caplog):
    corpo = _corpo_gemini(f"```json\n{json.dumps(_ESTRUTURA_VALIDA)}\n```")
    monkeypatch.setattr(httpx, "post", lambda *a, **k: _RespostaFake(corpo))
    porta = TemplateDeMissaoNaNuvem(chave_de_api="chave-de-teste", modelo="gemini-2.5-flash")

    with caplog.at_level(logging.WARNING, logger=_LOGGER):
        estrutura = _pedir(porta)

    assert estrutura is not None
    assert [atividade.titulo for atividade in estrutura.atividades] == ["Mapa da horta"]
    assert estrutura.atividades[0].desplugada is True
    assert estrutura.objetivo_ods == 2
    assert caplog.text == ""
