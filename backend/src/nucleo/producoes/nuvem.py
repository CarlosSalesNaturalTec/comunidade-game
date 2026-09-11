import base64
import json
import logging

import httpx

from .porta import LeituraDaProducao, PortaDaProducaoDaMissao

logger = logging.getLogger("nucleo.producoes")

_TETO_DO_CORPO_NO_LOG = 500


def _registrar_falha(assunto: str, excecao: Exception) -> None:
    """O corpo da resposta é onde o provedor explica a causa — modelo
    indisponível, crédito esgotado, chave restrita. O `raise_for_status`
    levanta com a linha de status e descarta o corpo, e sem ele cada
    diagnóstico custa uma rodada de investigação. Truncado: resposta de erro
    é curta, mas não tem teto declarado (change `template-da-missao-no-deepseek`,
    design — decisão 3)."""
    if isinstance(excecao, httpx.HTTPStatusError):
        logger.warning(
            "Falha ao consultar %s: HTTP %s — %s",
            assunto,
            excecao.response.status_code,
            excecao.response.text[:_TETO_DO_CORPO_NO_LOG],
        )
    else:
        logger.warning("Falha ao consultar %s.", assunto, exc_info=True)


# Sem a chave na URL: a mensagem de uma `HTTPStatusError` carrega a URL
# inteira, e o log a registraria em texto claro. A credencial vai no
# cabeçalho `x-goog-api-key` (design — decisão 4).
_ENDPOINT = "https://generativelanguage.googleapis.com/v1beta/models/{modelo}:generateContent"

# Só a foto sobe como mídia: a fala chega transcrita do aparelho e o núcleo
# nunca recebe áudio (`RF-05-76`, `RN-05-32`, design — decisão 3).
_MIME_DA_FOTO = "image/jpeg"

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
    por HTTP simples. Na **foto**, multimodal — a mesma passada lê e comenta,
    com metade da latência num encontro presencial; no texto e na fala já
    transcrita no aparelho, passada só de texto (`RF-05-76`, `RN-05-32`).
    Qualquer falha, demora ou resposta fora do formato esperado devolve
    `None`."""

    def __init__(self, *, chave_de_api: str, modelo: str) -> None:
        self._chave_de_api = chave_de_api
        self._modelo = modelo

    def ler(
        self, *, forma: str, texto: str | None, arquivo: bytes | None, producao_esperada: str
    ) -> LeituraDaProducao | None:
        if not self._chave_de_api:
            logger.warning("Chave de API do Gemini ausente: a leitura da produção não foi pedida.")
            return None

        partes: list[dict] = [{"text": _INSTRUCAO.format(producao_esperada=producao_esperada)}]
        if forma == "foto":
            partes.append(
                {
                    "inlineData": {
                        "mimeType": _MIME_DA_FOTO,
                        "data": base64.b64encode(arquivo or b"").decode("ascii"),
                    }
                }
            )
        else:
            partes.append({"text": f"Produção entregue pela equipe: {texto}"})

        try:
            resposta = httpx.post(
                _ENDPOINT.format(modelo=self._modelo),
                headers={"x-goog-api-key": self._chave_de_api},
                json={"contents": [{"parts": partes}]},
                timeout=20.0,
            )
            resposta.raise_for_status()
            texto_bruto = resposta.json()["candidates"][0]["content"]["parts"][0]["text"]
            dados = json.loads(_extrair_json(texto_bruto))
            validada = _validar_leitura(dados)
            if validada is None:
                logger.warning(
                    "Resposta do Gemini fora do formato esperado para a leitura da produção."
                )
            return validada
        except Exception as excecao:
            _registrar_falha("a leitura da produção no Gemini", excecao)
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
