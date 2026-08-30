import base64
import json
import logging

import httpx

from .porta import LeituraDaProducao, PortaDaProducaoDaMissao

logger = logging.getLogger("nucleo.producoes")

_ENDPOINT = (
    "https://generativelanguage.googleapis.com/v1beta/models/{modelo}:generateContent?key={chave}"
)

_MIME_POR_FORMA = {"audio": "audio/webm", "foto": "image/jpeg"}

_INSTRUCAO = (
    "Você é um educador (Mestre) que lê a produção que uma equipe de crianças e "
    'adolescentes de 6 a 16 anos entregou para a missão: "{producao_esperada}". Primeiro, '
    "transcreva fielmente o que a equipe produziu. Depois, escreva uma devolutiva "
    "construtiva e curta, que aponta o próximo passo — nunca uma nota, aprovação ou "
    "reprovação; o resultado é lançado pelo Mestre, não por você. Responda apenas com um "
    'JSON no formato {{"transcricao": str, "devolutiva": str}}.'
)


class ProducaoDaMissaoNaNuvem(PortaDaProducaoDaMissao):
    """Adaptador de produção (documento 03 §1.12): fala com a API do Gemini
    por HTTP simples, multimodal — a mesma passada lê e comenta, com metade
    da latência num encontro presencial (design — decisão 4). Qualquer
    falha, demora ou resposta fora do formato esperado devolve `None`."""

    def __init__(self, *, chave_de_api: str, modelo: str) -> None:
        self._chave_de_api = chave_de_api
        self._modelo = modelo

    def ler(
        self, *, forma: str, texto: str | None, arquivo: bytes | None, producao_esperada: str
    ) -> LeituraDaProducao | None:
        if not self._chave_de_api:
            return None

        partes: list[dict] = [{"text": _INSTRUCAO.format(producao_esperada=producao_esperada)}]
        if forma == "texto":
            partes.append({"text": f"Produção entregue pela equipe: {texto}"})
        else:
            partes.append(
                {
                    "inlineData": {
                        "mimeType": _MIME_POR_FORMA[forma],
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
            return _validar_leitura(dados)
        except Exception:
            logger.warning("Falha ao consultar a leitura da produção no Gemini.", exc_info=True)
            return None


def _extrair_json(texto: str) -> str:
    """O modelo às vezes envolve a resposta em cerca de código; extrai só o
    trecho entre a primeira `{` e a última `}`."""
    inicio = texto.index("{")
    fim = texto.rindex("}")
    return texto[inicio : fim + 1]


def _validar_leitura(dados: dict) -> LeituraDaProducao | None:
    transcricao = dados.get("transcricao")
    if not isinstance(transcricao, str) or not transcricao.strip():
        return None
    devolutiva = dados.get("devolutiva")
    if devolutiva is not None and not isinstance(devolutiva, str):
        return None
    return LeituraDaProducao(transcricao=transcricao, devolutiva=devolutiva)
