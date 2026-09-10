import json
import logging

import httpx

from .porta import AtividadeSugerida, EstruturaSugerida, PortaDoTemplateDeMissao

logger = logging.getLogger("nucleo.template_de_missao")

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


_ENDPOINT = "https://api.deepseek.com/chat/completions"

_INSTRUCAO = (
    "Você ajuda um educador (Mestre) a montar a estrutura de uma missão educacional para "
    "crianças e adolescentes de 6 a 16 anos, a partir do tópico que ele quer ensinar. "
    "Responda apenas com um JSON no formato "
    '{{"atividades": [{{"titulo": str, "modalidade": "individual"|"em_equipe"|'
    '"em_equipe_com_familiar", "formato": "presencial"|"on_line_assincrona", '
    '"natureza": str, "producao_esperada": str, "desplugada": bool}}], '
    '"objetivo_ods": int|null, "meta_ods": str|null}}. '
    "Nunca escreva o conteúdo da missão, apenas a estrutura. "
    "{exigencia_desplugada}"
    "Tópico: {topico}"
)

_EXIGENCIA_DESPLUGADA = (
    "A primeira atividade da lista precisa ser desplugada (sem tela nem eletrônico). "
)


class TemplateDeMissaoNaNuvem(PortaDoTemplateDeMissao):
    """Adaptador de produção: fala com a API do DeepSeek por HTTP simples —
    sem SDK novo, o mesmo `httpx` que `sessoes.social` já usa. O DeepSeek
    atende a porta de texto do Ciclo 01 (documento 03 §1.12); a leitura da
    produção e o assistente seguem no Gemini, porque leem imagem e áudio.

    A credencial vai no cabeçalho, nunca na URL: a mensagem de uma
    `HTTPStatusError` carrega a URL inteira, e o log a registraria em texto
    claro. Qualquer falha, demora ou resposta fora do formato esperado
    devolve `None` — a indisponibilidade nunca vira exceção (`RF-09-91`)."""

    def __init__(self, *, chave_de_api: str, modelo: str) -> None:
        self._chave_de_api = chave_de_api
        self._modelo = modelo

    def sugerir_estrutura(
        self, *, topico: str, exigir_atividade_desplugada: bool
    ) -> EstruturaSugerida | None:
        if not self._chave_de_api:
            logger.warning(
                "Chave de API do DeepSeek ausente: a estrutura da missão não foi pedida."
            )
            return None

        prompt = _INSTRUCAO.format(
            exigencia_desplugada=_EXIGENCIA_DESPLUGADA if exigir_atividade_desplugada else "",
            topico=topico,
        )
        try:
            resposta = httpx.post(
                _ENDPOINT,
                headers={"Authorization": f"Bearer {self._chave_de_api}"},
                json={
                    "model": self._modelo,
                    "messages": [{"role": "user", "content": prompt}],
                    # O modo JSON do DeepSeek exige a palavra "json" no
                    # prompt, que o `_INSTRUCAO` já traz, e dispensa a cerca
                    # de código que o `_extrair_json` desembrulha.
                    "response_format": {"type": "json_object"},
                },
                timeout=10.0,
            )
            resposta.raise_for_status()
            texto = resposta.json()["choices"][0]["message"]["content"]
            dados = json.loads(_extrair_json(texto))
            validada = _validar_estrutura(dados)
            if validada is None:
                logger.warning(
                    "Resposta do DeepSeek fora do formato esperado para a estrutura da missão."
                )
            return validada
        except Exception as excecao:
            _registrar_falha("a estrutura da missão no DeepSeek", excecao)
            return None


def _extrair_json(texto: str) -> str:
    """O modelo às vezes envolve a resposta em cerca de código; extrai só o
    trecho entre a primeira `{` e a última `}`."""
    inicio = texto.index("{")
    fim = texto.rindex("}")
    return texto[inicio : fim + 1]


def _validar_estrutura(dados: dict) -> EstruturaSugerida | None:
    atividades_brutas = dados.get("atividades")
    if not isinstance(atividades_brutas, list) or not atividades_brutas:
        return None

    atividades = []
    for bruta in atividades_brutas:
        if not isinstance(bruta, dict):
            return None
        campos_obrigatorios = ("titulo", "modalidade", "formato", "natureza", "producao_esperada")
        if not all(isinstance(bruta.get(campo), str) for campo in campos_obrigatorios):
            return None
        atividades.append(
            AtividadeSugerida(
                titulo=bruta["titulo"],
                modalidade=bruta["modalidade"],
                formato=bruta["formato"],
                natureza=bruta["natureza"],
                producao_esperada=bruta["producao_esperada"],
                desplugada=bool(bruta.get("desplugada", False)),
            )
        )

    objetivo_ods = dados.get("objetivo_ods")
    if objetivo_ods is not None and not isinstance(objetivo_ods, int):
        return None
    meta_ods = dados.get("meta_ods")
    if meta_ods is not None and not isinstance(meta_ods, str):
        return None

    return EstruturaSugerida(atividades=atividades, objetivo_ods=objetivo_ods, meta_ods=meta_ods)
