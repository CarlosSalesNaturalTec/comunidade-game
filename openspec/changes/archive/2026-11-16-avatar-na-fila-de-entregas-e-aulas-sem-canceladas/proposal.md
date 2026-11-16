# Proposta — Avatar na fila de entregas e aulas sem as canceladas

**PRD de origem:** PRD-09 — Área do Mestre (App 09). **Fatia:** 34 do
`openspec/cronograma-de-fatias.md`. **Identificadores:** `RF-09-75`, `RF-09-42`, `RN-09-18`.
Decisão do fundador de 2026-11-16, em `/opsx:propose`.

## Why

Em **Minhas turmas**, a fila de **Entregas pendentes** imprime entre parênteses o objeto do
avatar em texto cru (JSON) ao lado do nick — conserto da fatia 13, que repassou o campo
`guerreiro_avatar` direto para a tela. A seção **Aulas** da mesma área lista também as aulas
canceladas, que não têm o que o Mestre fazer nelas.

## What Changes

- A fila de Entregas pendentes da App 09 desenha o avatar do Guerreiro(a) com o componente
  `Avatar` de `comum/avatar`, ao lado do nick, e deixa de imprimir o texto do campo
  (`RF-09-75`, `RN-09-18`).
- A seção Aulas de Minhas turmas deixa de listar a aula de situação `cancelada`; quando todas
  as aulas forem canceladas, vale a mesma mensagem de lista vazia (`RF-09-42`).
- Nenhuma mudança no núcleo nem na rota: o filtro e o desenho são de apresentação.

## Capabilities

### New Capabilities

Nenhuma.

### Modified Capabilities

- `area-do-mestre`: o requisito de Minhas turmas passa a excluir da lista a aula cancelada.
- `recompensa-de-marco`: o requisito da fila de entregas pendentes passa a exigir que a App 09
  desenhe o avatar, nunca o texto do campo.

## Impact

- `apps/app-09-mestre/src/recompensas/FilaDeEntregasPendentes.tsx` e o teste dela.
- `apps/app-09-mestre/src/turmas/TelaDeMinhasTurmas.tsx` e `turmas.test.tsx`.
- Fora do escopo: a App 01 tem o mesmo defeito em `TelaDeEntregasDoEncontro.tsx`, e a fila do
  encontro é outra tela (PRD-04); fica para fatia própria, se o fundador quiser.
- Documentação: só a linha da fatia no cronograma; nenhum documento de `docs/` muda.
