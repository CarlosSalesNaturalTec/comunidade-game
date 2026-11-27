# Contorno da comunidade

**PRD de origem:** PRD-08 — Comunidades Virtuais e território, fatia **1** do
`openspec/cronograma-de-fatias.md`.
**Requisitos atendidos:** `RF-08-33`, `RF-08-34`, `RN-08-31`, `RN-08-32`.

## Why

O mapa das Comunidades Virtuais na vitrine (fatia 15 do PRD-03) e a tela em que o Admin
cadastra o contorno (fatia 34 do PRD-02) dependem de o núcleo guardar e servir o contorno de
cada comunidade. Hoje a `ComunidadeVirtual` tem nome, localização e granularidade, e nenhuma
geometria. Decisão do fundador de 2026-11-27, já gravada nos documentos 02 §1, 03 §§8 e 12.3 e
no documento 09 ("Contorno da Comunidade Virtual"), e aplicada no PRD-08 v9.

## What Changes

- A `ComunidadeVirtual` ganha o **contorno** (polígono GeoJSON), o **elemento de origem no
  OSM** e a **data da cópia** (PRD-08 §8).
- Rota nova `PUT /v1/comunidades/{id}/contorno`, só de Admin, que cadastra ou substitui o
  contorno (`RF-08-33`, PRD-08 §9).
- `GET /v1/comunidades` e `GET /v1/comunidades/{id}` passam a devolver o contorno com o
  crédito e a licença do OSM; a comunidade sem contorno sai sem ele (`RF-08-34`).
- O contorno fica fora da exportação do território, que segue sob CC BY-SA (`RN-08-31`), e
  não carrega local, série nem registro (`RN-08-32`).

## Capabilities

### New Capabilities

Nenhuma.

### Modified Capabilities

- `comunidade-virtual`: o Admin cadastra e substitui o contorno da comunidade.
- `leitura-publica-do-territorio`: a lista e a leitura pública da comunidade devolvem o
  contorno e o crédito do OSM; a exportação não o inclui.

## Fora do escopo

Reproduz o PRD-08 §3.2:

- Georreferenciamento do **registro** por coordenada de GPS — o contorno é da comunidade.
- Leitura automática do OSM e envio de edição ao OSM — o Admin copia o contorno à mão.
- Telas: a do Admin é a fatia 34 do PRD-02; o mapa é a fatia 15 do PRD-03.

## Impact

- `backend/src/nucleo/comunidades/` — modelo, regra e rotas.
- `backend/src/nucleo/coletas/regra.py` — a linha da lista pública de comunidades.
- Uma migração Alembic, com três colunas anuláveis em `comunidade_virtual`.
- Contrato público: dois campos novos na leitura, sem quebra para quem já consome.
