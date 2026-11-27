# Proposal

PRD-09 — Área do Mestre (App 09), **fatia 39** do `openspec/cronograma-de-fatias.md`. Alcança
`RF-09-25`, `RF-09-84`, `RF-09-131`, `RF-09-141`, `RN-05-45` e `RN-05-46`, sem identificador
novo: é decisão de exibição do fundador de 2026-11-27 sobre requisitos já entregues.

## Why

Em Minhas trilhas → missão → Pré-visualizar missão, o Mestre autor confere a missão antes de
publicar, mas a ficha não mostra parte do que ele declarou para o desbloqueio: a recompensa
que o desbloqueio libera, e, no prático, o título curto e o kit apresentado. Para conferir,
ele precisa reabrir cada bloco.

## What Changes

- **Recompensa pelo desbloqueio:** a pré-visualização lista o **nome do tipo de recurso** de
  cada recompensa de marco declarada para a missão, **sem a quantidade** (decisão de
  2026-11-27); sem recompensa, diz que nenhuma foi declarada (`RF-09-84`).
- **Desafio prático:** além de enunciado, forma e critério, mostra o **título curto** da
  vitrine (`RF-09-131`) e o **kit apresentado**, pelo nome do recurso (`RF-09-141`), quando
  declarados.
- **Quiz:** mostra o corte — passa quem acerta ao menos 60% (`RN-05-45`); na sondagem, que ela
  abre a trilha ao ser respondida (`RN-05-46`).
- Esses itens são do autor: ficam num trecho próprio da ficha, dito como o que o Guerreiro(a)
  não vê na missão, para a pré-visualização seguir fiel ao resto (`RF-09-25`).

Fora do escopo: campo de dado novo no desafio, núcleo, App 05 e a vitrine.

## Capabilities

### New Capabilities

Nenhuma.

### Modified Capabilities

- `area-do-mestre`: ganha o requisito "A pré-visualização mostra ao autor o que ele declarou
  para o desbloqueio".

## Impact

- `apps/app-09-mestre/src/trilhas/PreVisualizacaoDaMissao.tsx`, `ListaDeMissoes.tsx`
  (repassa recompensas e tipos de recurso) e `trilhas.test.tsx`.
- `openspec/cronograma-de-fatias.md` (linha da fatia 39).
- Sem rota, `Operacao`, entidade nem migração: `GET /v1/trilhas/minhas` e a listagem de
  recompensas de marco já trazem tudo. Nada em `docs/` muda.
