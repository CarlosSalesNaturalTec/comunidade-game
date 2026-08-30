import json
import logging

import httpx

from .porta import AtividadeSugerida, EstruturaSugerida, PortaDoTemplateDeMissao

logger = logging.getLogger("nucleo.template_de_missao")

_ENDPOINT = (
    "https://generativelanguage.googleapis.com/v1beta/models/{modelo}:generateContent?key={chave}"
)

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
    """Adaptador de produção (documento 03 §1.12): fala com a API do Gemini
    por HTTP simples — sem SDK novo, o mesmo `httpx` que `sessoes.social`
    já usa para verificar o login social. Qualquer falha, demora ou
    resposta fora do formato esperado devolve `None`: a indisponibilidade
    nunca vira exceção (`RF-09-91`, design — decisões 2, 3)."""

    def __init__(self, *, chave_de_api: str, modelo: str) -> None:
        self._chave_de_api = chave_de_api
        self._modelo = modelo

    def sugerir_estrutura(
        self, *, topico: str, exigir_atividade_desplugada: bool
    ) -> EstruturaSugerida | None:
        if not self._chave_de_api:
            return None

        prompt = _INSTRUCAO.format(
            exigencia_desplugada=_EXIGENCIA_DESPLUGADA if exigir_atividade_desplugada else "",
            topico=topico,
        )
        try:
            resposta = httpx.post(
                _ENDPOINT.format(modelo=self._modelo, chave=self._chave_de_api),
                json={"contents": [{"parts": [{"text": prompt}]}]},
                timeout=10.0,
            )
            resposta.raise_for_status()
            texto = resposta.json()["candidates"][0]["content"]["parts"][0]["text"]
            dados = json.loads(_extrair_json(texto))
            return _validar_estrutura(dados)
        except Exception:
            logger.warning("Falha ao consultar o template da missão no Gemini.", exc_info=True)
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
