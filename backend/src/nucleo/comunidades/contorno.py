"""O contorno da Comunidade Virtual: a linha que a delimita no mapa, copiada
do OpenStreetMap (OSM) pelo Admin (`RF-08-33`, `RF-08-34`, `RN-08-31`,
`RN-08-32`, documento 02 §1).

Módulo próprio, e não `regra.py`, porque a lista pública de comunidades mora
em `coletas/regra.py`, que já é importado por `comunidades/regra.py`: os dois
leem o contorno daqui sem ciclo de importação.
"""

import re
from datetime import datetime
from typing import Any

from pydantic import BaseModel

from ..erros import ErroDeValidacao, PermissaoNegada
from ..personas.modelo import Papel, Persona
from ..tempo import agora
from .modelo import ComunidadeVirtual

# O texto do crédito e a licença são os do documento 03 §8 e §12.3: o
# contorno é sempre cópia do OSM (documento 02 §1), então a atribuição não
# varia por comunidade (design — Decisão 4).
CREDITO_DO_OSM = "© colaboradores do OpenStreetMap"
LICENCA_DO_CONTORNO = "ODbL"

# Só via e relação formam área no OSM; nó é ponto (design — Decisão 2).
_PADRAO_DA_ORIGEM = re.compile(r"^(way|relation)/[0-9]+$")
_TIPOS_ACEITOS = ("Polygon", "MultiPolygon")


class ContornoSaida(BaseModel):
    """O que a leitura pública devolve do contorno: a geometria, de onde veio,
    quando foi copiada e a atribuição — nenhum local, série ou registro
    (`RF-08-34`, `RN-08-31`, `RN-08-32`)."""

    geometria: dict[str, Any]
    origem_osm: str
    copiado_em: datetime
    credito: str
    licenca: str


def saida_do_contorno(comunidade: ComunidadeVirtual) -> ContornoSaida | None:
    """Nulo enquanto o Admin não gravou contorno: a comunidade segue na
    leitura, sem ele (`RF-08-34`)."""
    if comunidade.contorno is None:
        return None
    return ContornoSaida(
        geometria=comunidade.contorno,
        origem_osm=comunidade.contorno_origem_osm,
        copiado_em=comunidade.contorno_copiado_em,
        credito=CREDITO_DO_OSM,
        licenca=LICENCA_DO_CONTORNO,
    )


def _recusar(mensagem: str, campo: str = "geometria") -> None:
    raise ErroDeValidacao(mensagem=mensagem, campo=campo)


def _e_numero(valor: Any) -> bool:
    return isinstance(valor, int | float) and not isinstance(valor, bool)


def _conferir_anel(anel: Any) -> None:
    if not isinstance(anel, list) or len(anel) < 4:
        _recusar("Cada anel do contorno precisa de ao menos quatro posições.")
    for posicao in anel:
        if (
            not isinstance(posicao, list)
            or len(posicao) < 2
            or not _e_numero(posicao[0])
            or not _e_numero(posicao[1])
        ):
            _recusar("Cada posição do contorno precisa ser [longitude, latitude].")
        longitude, latitude = posicao[0], posicao[1]
        if not -180 <= longitude <= 180 or not -90 <= latitude <= 90:
            _recusar("Coordenada do contorno fora da faixa de longitude e latitude.")
    if anel[0][:2] != anel[-1][:2]:
        _recusar("Cada anel do contorno precisa ser fechado: a última posição repete a primeira.")


def _conferir_poligono(aneis: Any) -> None:
    if not isinstance(aneis, list) or not aneis:
        _recusar("O polígono do contorno precisa de ao menos um anel.")
    for anel in aneis:
        _conferir_anel(anel)


def conferir_geometria(geometria: Any) -> None:
    """Polígono ou multipolígono GeoJSON, em longitude e latitude, com cada
    anel fechado e de ao menos quatro posições (design — Decisão 2)."""
    if not isinstance(geometria, dict) or geometria.get("type") not in _TIPOS_ACEITOS:
        _recusar("O contorno precisa ser um polígono ou multipolígono GeoJSON.")
    coordenadas = geometria.get("coordinates")
    if geometria["type"] == "Polygon":
        _conferir_poligono(coordenadas)
        return
    if not isinstance(coordenadas, list) or not coordenadas:
        _recusar("O multipolígono do contorno precisa de ao menos um polígono.")
    for poligono in coordenadas:
        _conferir_poligono(poligono)


def gravar_contorno(
    comunidade: ComunidadeVirtual,
    *,
    operador: Persona,
    geometria: Any,
    origem_osm: str | None,
) -> ComunidadeVirtual:
    """Só o Admin grava o contorno; gravar de novo substitui o anterior, com
    a origem e a data da nova cópia. Recusa nada grava: a validação inteira
    corre antes de tocar a comunidade (`RF-08-33`, `RN-08-32`)."""
    if operador.papel != Papel.admin:
        raise PermissaoNegada(mensagem="Só o Admin grava o contorno da comunidade.")
    conferir_geometria(geometria)
    if not origem_osm or not _PADRAO_DA_ORIGEM.match(origem_osm):
        _recusar(
            "A origem do contorno precisa ser uma via ou relação do OSM, como relation/12582832.",
            campo="origem_osm",
        )

    comunidade.contorno = {"type": geometria["type"], "coordinates": geometria["coordinates"]}
    comunidade.contorno_origem_osm = origem_osm
    comunidade.contorno_copiado_em = agora()
    return comunidade
