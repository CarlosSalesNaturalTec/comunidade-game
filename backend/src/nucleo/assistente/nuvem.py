import base64
import json
import logging

import httpx

from .porta import PortaDoAssistente, RespostaDoAssistente

logger = logging.getLogger("nucleo.assistente")

_ENDPOINT = (
    "https://generativelanguage.googleapis.com/v1beta/models/{modelo}:generateContent?key={chave}"
)

_DESFECHOS_VALIDOS = {"respondida", "fora_do_corpus", "tarefa_escolar"}

_INSTRUCAO = (
    "Você é o assistente de trilhas que ajuda uma equipe de crianças e adolescentes de 6 a "
    "16 anos, num encontro presencial. Responda SOMENTE com base no material abaixo — nunca "
    "de conhecimento próprio. Se a pergunta não estiver no material, classifique como "
    '"fora_do_corpus". Se for pergunta de tarefa ou dever de casa da escola, classifique '
    'como "tarefa_escolar", sem respondê-la. Só responda o conteúdo quando classificar como '
    '"respondida".\n\nMaterial:\n{corpus}\n\n'
    "Primeiro, transcreva fielmente a pergunta da equipe. Depois, responda apenas com um "
    'JSON no formato {{"transcricao_da_pergunta": str, "desfecho": '
    '"respondida"|"fora_do_corpus"|"tarefa_escolar", "resposta": str|null}}.'
)


class AssistenteDeTrilhasNaNuvem(PortaDoAssistente):
    """Adaptador de produção (documento 03 §1.12): fala com a API do Gemini
    por HTTP simples, multimodal — a mesma passada transcreve e responde
    (design — decisão 4). Qualquer falha, demora ou resposta fora do
    formato esperado devolve `None`."""

    def __init__(self, *, chave_de_api: str, modelo: str) -> None:
        self._chave_de_api = chave_de_api
        self._modelo = modelo

    def responder(
        self, *, texto: str | None, arquivo: bytes | None, corpus: str
    ) -> RespostaDoAssistente | None:
        if not self._chave_de_api:
            return None

        partes: list[dict] = [{"text": _INSTRUCAO.format(corpus=corpus)}]
        if texto is not None:
            partes.append({"text": f"Pergunta da equipe: {texto}"})
        else:
            partes.append(
                {
                    "inlineData": {
                        "mimeType": "audio/webm",
                        "data": base64.b64encode(arquivo or b"").decode("ascii"),
                    }
                }
            )

        try:
            resposta = httpx.post(
                _ENDPOINT.format(modelo=self._modelo, chave=self._chave_de_api),
                json={"contents": [{"parts": partes}]},
                timeout=20.0,
            )
            resposta.raise_for_status()
            texto_bruto = resposta.json()["candidates"][0]["content"]["parts"][0]["text"]
            dados = json.loads(_extrair_json(texto_bruto))
            return _validar_resposta(dados)
        except Exception:
            logger.warning("Falha ao consultar o assistente de trilhas no Gemini.", exc_info=True)
            return None


def _extrair_json(texto: str) -> str:
    """O modelo às vezes envolve a resposta em cerca de código; extrai só o
    trecho entre a primeira `{` e a última `}`."""
    inicio = texto.index("{")
    fim = texto.rindex("}")
    return texto[inicio : fim + 1]


def _validar_resposta(dados: dict) -> RespostaDoAssistente | None:
    transcricao = dados.get("transcricao_da_pergunta")
    if not isinstance(transcricao, str) or not transcricao.strip():
        return None
    desfecho = dados.get("desfecho")
    if desfecho not in _DESFECHOS_VALIDOS:
        return None
    resposta = dados.get("resposta")
    if resposta is not None and not isinstance(resposta, str):
        return None
    if desfecho == "respondida" and not resposta:
        return None
    return RespostaDoAssistente(
        transcricao_da_pergunta=transcricao, desfecho=desfecho, resposta=resposta
    )
