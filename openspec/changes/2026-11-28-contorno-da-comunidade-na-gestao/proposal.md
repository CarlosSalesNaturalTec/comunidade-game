# Contorno da comunidade na gestão

**PRD de origem:** PRD-02 — Frontend de gestão (App 03), fatia **34** do
`openspec/cronograma-de-fatias.md`.
**Requisitos atendidos:** `RF-02-122`, servindo `RF-08-33` e `RN-08-31` (PRD-08).

## Why

O núcleo já guarda e serve o contorno da Comunidade Virtual (fatia 1 do PRD-08,
`2026-11-27-contorno-da-comunidade`), mas nenhuma tela chama `PUT /v1/comunidades/{id}/contorno`:
sem ela o Admin não cadastra contorno algum, e o mapa da vitrine (fatia 15 do PRD-03) não tem o
que desenhar. Decisão do fundador de 2026-11-27, já gravada nos documentos 02 §1 e 03 §12.3 e no
documento 09 ("Contorno da Comunidade Virtual").

## What Changes

- Na lista de Comunidades Virtuais da App 03, cada comunidade passa a dizer se **tem contorno** —
  com o elemento de origem no OSM, a data da cópia e o crédito e a licença devolvidos pelo
  núcleo — ou que ainda não tem (`RF-02-122`, `RN-08-31`).
- Só para o Admin, cada comunidade ganha a ação **Cadastrar contorno** (ou **Substituir
  contorno**, quando já há um), que abre um formulário com o **GeoJSON** colado do OSM e o
  **elemento de origem** (`way/<número>` ou `relation/<número>`) e grava pelo `PUT` do núcleo
  (`RF-02-122`, `RF-08-33`).
- A recusa do núcleo — 422 com o campo, 403 de papel — aparece no campo ou no aviso do
  formulário; gravado, a lista recarrega com o contorno novo.

## Capabilities

### New Capabilities

Nenhuma.

### Modified Capabilities

- `aplicacao-de-gestao`: requisito novo — o Admin cadastra e substitui o contorno da comunidade
  pela App 03, e a lista mostra a situação do contorno de cada uma.

## Fora do escopo

Reproduz o PRD-02 §3.2 e o PRD-08 §3.2 no que alcança esta fatia:

- **Leitura automática do OSM** e envio de edição ao OSM — o Admin copia o contorno à mão.
- **Mapa** com o contorno desenhado — é da vitrine, fatia 15 do PRD-03.
- Regras do contorno (tipo de geometria, anel fechado, faixa de coordenada, padrão da origem) —
  são do núcleo, já entregues pela fatia 1 do PRD-08; a tela não as repete.

## Impact

- `apps/app-03-gestao/src/comunidades/` — `api.ts`, a lista e um formulário novo do contorno,
  com os testes.
- Nenhuma rota, entidade, migração nem mudança no backend: o `PUT` e o campo `contorno` da
  leitura já existem.
- Nada em `docs/` muda além da linha da fatia no cronograma.
