# Proposal

PRD de origem: **PRD-09**. Correção de defeito, sem fatia numerada — linha "—" no bloco do
PRD-09 do `openspec/cronograma-de-fatias.md`, no precedente da fatia 21 e de "Agenda sem
canceladas". Identificadores atendidos: `RF-09-45`, `RF-09-46`, `RN-09-18`. Relatado pelo
fundador em 2026-11-26.

## Why

Na tela **Presença e ocorrência** (Minhas turmas), os formulários "Confirmar presença" e
"Lançar ocorrência de conduta" pedem o **Guerreiro(a)** num campo de texto livre rotulado
"Identificador do Guerreiro(a)", que vai ao núcleo como `guerreiro_id` (UUID). O Mestre digita
o nick e o núcleo recusa com `Input should be a valid UUID, invalid character: found 'J' at 0`:
a presença que o App 01 não capturou não se confirma, e a ocorrência não se lança.

## What Changes

- O campo de texto "Identificador do Guerreiro(a)" sai dos dois formulários da tela da aula e
  dá lugar a um **seletor por nick**, alimentado por `GET /v1/guerreiros/vinculaveis` — rota já
  autorizada ao Mestre, que devolve só nick e avatar dos Guerreiros e Guerreiras ativos das
  comunidades dele (`RF-09-62`, `RN-09-18`).
- No formulário de presença, quem **já está na lista de presentes** desta aula não aparece no
  seletor.
- Enviar sem escolher o Guerreiro(a) é impedido na tela, com mensagem em linguagem simples.
- Só a App 09: nenhuma rota, entidade ou migração nova no núcleo.

## Capabilities

### New Capabilities

Nenhuma.

### Modified Capabilities

- `area-do-mestre`: o requisito "O Mestre confirma a presença e lança a ocorrência de
  conduta" passa a dizer que o Guerreiro(a) é escolhido pelo nick, nunca digitado como
  identificador.

## Impact

- `apps/app-09-mestre/src/turmas/TelaDaAula.tsx` e o teste `turmas.test.tsx`.
- Reaproveita `listarGuerreirosVinculaveis` de `apps/app-09-mestre/src/responsaveis/api.ts`.
- `docs/`: nada muda — não há decisão nova nem requisito novo.
