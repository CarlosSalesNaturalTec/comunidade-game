# Mapa das Comunidades Virtuais

**PRD de origem:** PRD-03 — Vitrine pública (App 06), fatia **15** do
`openspec/cronograma-de-fatias.md`.
**Requisitos atendidos:** `RF-03-89`, `RF-03-90`, `RF-03-91`, `RF-03-92`, `RN-03-44`,
`RN-03-45`, `RN-03-46`; alcança `RF-03-20` (a comunidade recém-criada aparece com o contorno).

## Why

O núcleo já serve o contorno de cada comunidade na lista e na leitura pública (fatia 1 do PRD-08)
e o Admin já o cadastra (fatia 34 do PRD-02), mas a vitrine não desenha mapa algum. Decisão do
fundador de 2026-11-27 (documento 09, "Mapa das comunidades na vitrine"), com a forma técnica do
fundo decidida em 2026-11-28, em `/opsx:propose`:

- fundo **vetorial**, desenhado com **MapLibre GL** sobre um arquivo **PMTiles**;
- o recorte cobre o **município de Salvador**;
- o arquivo é publicado no **Firebase Hosting da App 06**, pelo mesmo deploy, na mesma origem.

## What Changes

- Na seção Comunidades Virtuais, um **mapa** acima da lista com o contorno e o nome de cada
  comunidade que tenha contorno; tocar o contorno abre a página dela (`RF-03-89`, `RF-03-90`).
- Na página da comunidade, o mapa com o **contorno dela em destaque**, ao lado da representação
  visual genérica, que fica (`RF-03-91`, `RN-03-46`, `RF-03-20`).
- O mapa traz o crédito "© colaboradores do OpenStreetMap" e a licença ODbL (`RF-03-92`).
- O fundo é um recorte do OSM em PMTiles, servido pela própria App 06; nenhuma requisição sai para
  servidor de mapas de terceiros (`RN-03-45`). O mapa desenha só o contorno — nunca ponto de coleta,
  local abaixo da comunidade nem coletor (`RN-03-44`).
- Dependências novas na App 06: `maplibre-gl` e `pmtiles`. Um script versionado gera o recorte.
- Comunidade sem contorno segue na lista e na página como hoje, sem mapa vazio nem erro.

## Capabilities

### New Capabilities

Nenhuma.

### Modified Capabilities

- `aplicacao-da-vitrine`: requisitos novos — o mapa da listagem, o mapa da página da comunidade e o
  fundo servido pela plataforma, com crédito e licença.

## Fora do escopo

Reproduz o PRD-03 §3.2:

- **Ponto de coleta no mapa** e **leitura automática do OSM** — o mapa desenha só o contorno
  cadastrado na plataforma.
- **Dado abaixo do bairro**.
- A **frequência de atualização** do recorte segue pendente (PRD-03 §14, documento 09 §1) e não
  trava a fatia: o recorte nasce com a entrega, e regenerá-lo é rodar o script.

## Impact

- `apps/app-06-vitrine/` — `src/mapa/` novo, `SecaoDeComunidades.tsx`, `PaginaDaComunidade.tsx`,
  `api/leituras.ts`, `package.json`, `public/mapa/` (o recorte e o estilo) e
  `scripts/gerar-recorte-do-osm.sh`.
- Nenhuma rota, entidade ou migração no backend.
- Documentação: documento 03 §8 (forma do fundo) e documento 09 §1 (decisão de 2026-11-28).
