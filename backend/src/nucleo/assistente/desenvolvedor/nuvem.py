import json
import logging

import httpx

from ..nuvem import _extrair_json, _registrar_falha
from .porta import (
    MensagemDaConversa,
    PortaDoAssistenteDoDesenvolvedor,
    RespostaDoDesenvolvedor,
)

logger = logging.getLogger("nucleo.assistente")

# Sem a chave na URL: a mensagem de uma `HTTPStatusError` carrega a URL
# inteira, e o log a registraria em texto claro (mesmo cuidado de
# `assistente.nuvem`).
_ENDPOINT = "https://generativelanguage.googleapis.com/v1beta/models/{modelo}:generateContent"

_DESFECHOS_VALIDOS = {"respondida", "fora_do_corpus"}

# Quantas opções do próximo passo se aceita do modelo: mais que isso deixa de
# ser pergunta de múltipla escolha e vira lista.
_TETO_DE_OPCOES = 4

_INSTRUCAO = (
    "Você é o assistente da Área do Apoiador Desenvolvedor do Comunidade Game, e conversa "
    "com quem quer construir uma aplicação ou um jogo sobre a API da plataforma. Responda "
    "SOMENTE com base no material abaixo — nunca de conhecimento próprio. Se a pergunta não "
    'estiver no material, classifique como "fora_do_corpus" e não a responda. Nunca peça nem '
    "registre dado pessoal de quem pergunta.\n\nMaterial:\n{corpus}\n\n"
    "Responda apenas com um JSON no formato "
    '{{"desfecho": "respondida"|"fora_do_corpus", "resposta": str|null, "opcoes": [str]}}, '
    "em que `opcoes` traz de duas a quatro escolhas curtas do próximo passo que a pessoa "
    "pode querer conhecer."
)


class AssistenteDoDesenvolvedorNaNuvem(PortaDoAssistenteDoDesenvolvedor):
    """Adaptador de produção (documento 03 §1.12, `RN-03-31`): o mesmo Gemini
    do assistente de trilhas, pela chave única do projeto. Qualquer falha,
    demora ou resposta fora do formato esperado devolve `None`."""

    def __init__(self, *, chave_de_api: str, modelo: str) -> None:
        self._chave_de_api = chave_de_api
        self._modelo = modelo

    def responder(
        self,
        *,
        texto: str,
        corpus: str,
        historico: tuple[MensagemDaConversa, ...],
    ) -> RespostaDoDesenvolvedor | None:
        if not self._chave_de_api:
            logger.warning(
                "Chave de API do Gemini ausente: a resposta do assistente do Desenvolvedor "
                "não foi pedida."
            )
            return None

        partes: list[dict] = [{"text": _INSTRUCAO.format(corpus=corpus)}]
        for mensagem in historico:
            partes.append({"text": f"{mensagem.de}: {mensagem.texto}"})
        partes.append({"text": f"Pergunta: {texto}"})

        try:
            resposta = httpx.post(
                _ENDPOINT.format(modelo=self._modelo),
                headers={"x-goog-api-key": self._chave_de_api},
                json={"contents": [{"parts": partes}]},
                timeout=20.0,
            )
            resposta.raise_for_status()
            texto_bruto = resposta.json()["candidates"][0]["content"]["parts"][0]["text"]
            validada = _validar_resposta(json.loads(_extrair_json(texto_bruto)))
            if validada is None:
                logger.warning(
                    "Resposta do Gemini fora do formato esperado para o assistente do "
                    "Desenvolvedor."
                )
            return validada
        except Exception as excecao:
            _registrar_falha("o assistente do Desenvolvedor no Gemini", excecao)
            return None


def _validar_resposta(dados: dict) -> RespostaDoDesenvolvedor | None:
    desfecho = dados.get("desfecho")
    if desfecho not in _DESFECHOS_VALIDOS:
        return None
    resposta = dados.get("resposta")
    if resposta is not None and not isinstance(resposta, str):
        return None
    if desfecho == "respondida" and not resposta:
        return None

    brutas = dados.get("opcoes")
    opcoes: tuple[str, ...] = ()
    if isinstance(brutas, list):
        opcoes = tuple(item.strip() for item in brutas if isinstance(item, str) and item.strip())[
            :_TETO_DE_OPCOES
        ]

    return RespostaDoDesenvolvedor(desfecho=desfecho, resposta=resposta, opcoes=opcoes)
