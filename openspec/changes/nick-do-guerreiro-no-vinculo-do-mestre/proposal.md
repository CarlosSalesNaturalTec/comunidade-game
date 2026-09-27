# Proposal

Fatia 21 do **PRD-09 — Área do Mestre (App 09)**, conforme
`openspec/cronograma-de-fatias.md`. Atende `RF-09-63`. Correção de defeito: nenhum
requisito, rota ou entidade nova.

## Why

Na App 09, a lista "Vínculos já criados" da tela de Responsáveis imprime apenas o **grau de
parentesco**. Um responsável vinculado a dois Guerreiros como "Pai" produz duas linhas
idênticas, e o Mestre não sabe a quem cada uma se refere. É o mesmo defeito relatado pelo
fundador na App 03 em 2026-09-26, e na App 09 ele contrasta com o seletor logo acima, que já
apresenta cada Guerreiro(a) por nick e avatar.

O dado já está na tela: o nick vem do estado que alimenta o seletor, e o `guerreiro_id` já
vem na resposta do vínculo criado.

## What Changes

- Cada linha da lista de vínculos já criados passa a identificar o **Guerreiro(a) pelo
  nick**, ao lado do grau de parentesco.
- Nada mais: cadastro, vínculo, teto de três e credencial provisória seguem como estão.

## Capabilities

### New Capabilities

Nenhuma.

### Modified Capabilities

- `area-do-mestre`: o requisito "O Mestre vincula os Guerreiros e Guerreiras declarando o
  parentesco" (`RF-09-63`) ganha a exigência de que o vínculo apresentado entre os já
  criados identifique o Guerreiro(a), não só o parentesco.

## Impact

- `apps/app-09-mestre/src/responsaveis/TelaDeResponsaveis.tsx` — a lista de vínculos.
- `apps/app-09-mestre/src/responsaveis/responsaveis.test.tsx` — cobertura do caso de dois
  vínculos com o mesmo parentesco.
- Backend: nenhum. Rotas, contratos e migrações: nenhum.
- Documentação MkDocs: nenhuma. Fecha a fatia 21 no `openspec/cronograma-de-fatias.md`.

## Fora do escopo

- A App 03 tem o mesmo defeito e é a **fatia 23 do PRD-02**, change própria — decisão do
  fundador de 2026-09-26, uma fatia por aplicação.
- Listar os responsáveis já cadastrados na Área do Mestre: **fatia 22 do PRD-09**
  (`RF-09-122`), que depende da fatia 24 do PRD-02.
