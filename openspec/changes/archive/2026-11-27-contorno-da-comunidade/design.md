# Design — Contorno da comunidade

## Context

A `ComunidadeVirtual` (spec `comunidade-virtual`) e as duas leituras públicas que a servem
(spec `leitura-publica-do-territorio`) já existem. Esta fatia acrescenta um atributo, uma rota
de escrita de Admin e dois campos de leitura, sem mexer em série, registro nem exportação. A
auditoria da escrita já vem do middleware de `auditoria/`, que grava toda escrita sob `/v1`.

## Decisions

1. **Geometria em coluna JSON, sem PostGIS nesta fatia.** O contorno fica como objeto GeoJSON
   em `comunidade_virtual.contorno` (`JSON`), com `contorno_origem_osm` (`String(32)`) e
   `contorno_copiado_em` (`DateTime` com fuso), todas anuláveis. Nenhuma consulta do Ciclo 01
   faz operação espacial: o contorno é gravado inteiro e lido inteiro. A extensão PostGIS,
   prevista no documento 03, entra quando a primeira consulta espacial aparecer.
   _Descartada:_ coluna `geometry` do PostGIS, que obrigaria a habilitar a extensão nos três
   ambientes e no banco de teste sem consulta que a use.
2. **Validação no núcleo, sem biblioteca nova.** `regra.py` confere o tipo (`Polygon` ou
   `MultiPolygon`), anel com ao menos quatro posições e fechado, posição como par numérico com
   longitude em [-180, 180] e latitude em [-90, 90]. O elemento de origem segue
   `^(way|relation)/[0-9]+$`: só via e relação formam área no OSM.
   _Descartada:_ `shapely`, dependência nativa para uma conferência de forma.
3. **Uma rota `PUT`, que cadastra e substitui.** `PUT /v1/comunidades/{id}/contorno` com
   corpo `{geometria, origem_osm}`; a data da cópia é a hora do servidor. Responde 200 com o
   contorno gravado. Não há remoção: o PRD-08 não a prevê.
4. **Saída como objeto aninhado e nulo quando não há contorno.** As duas leituras ganham
   `contorno: ContornoSaida | None`, com `geometria`, `origem_osm`, `copiado_em`, `credito` e
   `licenca`. O crédito e a licença são constantes do módulo, com o texto do documento 03 §8:
   o contorno é sempre cópia do OSM (documento 02 §1). O contorno não passa pela supressão do
   piso de coletores, que alcança só os quatro indicadores (`RN-08-28`).
5. **Exportação intocada.** O CSV e o dicionário não leem a comunidade além do identificador;
   um teste fixa que nenhum dos dois traz o contorno (`RN-08-31`).

## Risks / Trade-offs

- Contorno muito detalhado engorda a lista pública, que pagina 10 comunidades. Aceito no Ciclo
  01, com uma comunidade só; simplificar a geometria vira pergunta ao fundador se pesar.
