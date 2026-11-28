#!/usr/bin/env bash
# Gera o recorte do OSM que serve de fundo ao mapa das Comunidades Virtuais
# (`RN-03-45`, design da change 2026-11-28-mapa-das-comunidades-virtuais).
#
# Lê o OSM pela Overpass só aqui, na geração; em tempo de execução a vitrine
# lê apenas `public/mapa/salvador.pmtiles`, da própria origem. Atualizar o
# recorte é rodar este script e abrir PR — ato revisado.
#
# Requisitos: curl, npx (Node) e tippecanoe 2.x (gera PMTiles direto).
# Uso: apps/app-06-vitrine/scripts/gerar-recorte-do-osm.sh
set -euo pipefail

# Município de Salvador no OSM (relação 362362): a área do recorte.
RELACAO_DO_MUNICIPIO=362362
AREA=$((3600000000 + RELACAO_DO_MUNICIPIO))
OVERPASS="https://overpass-api.de/api/interpreter"
OSMTOGEOJSON="osmtogeojson@3.0.0-beta.5"

RAIZ="$(cd "$(dirname "$0")/.." && pwd)"
SAIDA="$RAIZ/public/mapa/salvador.pmtiles"
TRABALHO="$(mktemp -d)"
trap 'rm -rf "$TRABALHO"' EXIT
mkdir -p "$(dirname "$SAIDA")"

consultar() {
  local nome="$1" corpo="$2"
  curl -sS --fail --retry 3 -A "comunidade-game-recorte/1.0" \
    --data-urlencode "data=[out:json][timeout:300];${corpo}" "$OVERPASS" \
    -o "$TRABALHO/$nome.osm.json"
  npx --yes "$OSMTOGEOJSON" "$TRABALHO/$nome.osm.json" >"$TRABALHO/$nome.geojson"
}

consultar municipio "rel(${RELACAO_DO_MUNICIPIO});out geom;"
consultar agua "area(${AREA})->.a;(nwr[natural=water](area.a);nwr[landuse=reservoir](area.a);nwr[waterway=riverbank](area.a););out geom;"
consultar verde "area(${AREA})->.a;(nwr[leisure=park](area.a);nwr[landuse~\"^(forest|grass|meadow)$\"](area.a);nwr[natural~\"^(wood|scrub)$\"](area.a););out geom;"
consultar ruas "area(${AREA})->.a;way[highway~\"^(motorway|trunk|primary|secondary|tertiary|unclassified|residential|living_street|service|pedestrian)(_link)?$\"](area.a);out geom;"

# Só a geometria e a classe da via seguem para o recorte: nenhum nome, para
# não precisar de glifo (design — Decisão 3).
tippecanoe --force -o "$SAIDA" -Z9 -z15 \
  --drop-densest-as-needed --extend-zooms-if-still-dropping \
  -y highway \
  -L municipio:"$TRABALHO/municipio.geojson" \
  -L agua:"$TRABALHO/agua.geojson" \
  -L verde:"$TRABALHO/verde.geojson" \
  -L ruas:"$TRABALHO/ruas.geojson"

echo "Recorte gravado em $SAIDA ($(du -h "$SAIDA" | cut -f1))."
