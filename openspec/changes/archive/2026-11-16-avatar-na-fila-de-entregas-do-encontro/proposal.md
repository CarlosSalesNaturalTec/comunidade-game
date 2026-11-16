# Proposta — Avatar na fila de entregas do encontro

**PRD de origem:** PRD-04 — Aula presencial (App 01). **Fatia:** 36 do
`openspec/cronograma-de-fatias.md`. **Identificadores:** `RF-09-75`, `RF-04-55`, invariante 16.
Decisão do fundador de 2026-11-16, em `/opsx:propose`.

## Why

A fila de entregas do encontro imprime entre parênteses o objeto do avatar em texto cru (JSON)
ao lado do nick — conserto da fatia 31, mesmo defeito que a fatia 34 do PRD-09 consertou na
App 09.

## What Changes

- A fila de entregas do encontro desenha o avatar do Guerreiro(a) com `Avatar` de
  `comum/avatar`, ao lado do nick, e deixa de imprimir o texto do campo (`RF-09-75`,
  `RF-04-55`).
- Nenhuma mudança no núcleo nem na rota.

## Capabilities

### New Capabilities

Nenhuma.

### Modified Capabilities

- `aplicacao-da-aula-presencial`: o requisito da fila de entregas do encontro passa a exigir o
  desenho do avatar, nunca o texto do campo.

## Impact

- `apps/app-01-aula-presencial/src/entregas/TelaDeEntregasDoEncontro.tsx` e
  `entregas.test.tsx`.
- Documentação: só a linha da fatia no cronograma; nenhum documento de `docs/` muda.
