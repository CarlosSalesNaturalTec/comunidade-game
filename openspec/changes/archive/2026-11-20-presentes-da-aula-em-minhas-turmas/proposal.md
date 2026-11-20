# Proposta — Presentes da aula em Minhas turmas

**PRD de origem:** PRD-09 — Área do Mestre (App 09). **Fatia:** 36 do
`openspec/cronograma-de-fatias.md`. **Identificadores:** `RF-09-42`, `RF-09-45`, `RF-09-73`
(reescrito), `RN-09-08`, `RN-09-18` e `RF-09-145` (novo). Decisão do fundador de 2026-11-20,
em `/opsx:propose`.

## Why

Na tela da aula de **Minhas turmas** (botão **Presença e ocorrência**), o Mestre confirma
presença e lança ocorrência sem ver quem já está presente: nenhuma rota lista as presenças de
uma aula, e o cenário da spec que diz que a presença confirmada "aparece na lista do encontro"
nunca teve lista. Na mesma área, a seção **Atividades presenciais** só repete títulos que a tela
da aula já oferece para lançamento, e as aulas **canceladas** ainda viajam do núcleo: a fatia 34
as descarta só no navegador, e a paginação conta o que a tela joga fora.

## What Changes

- **Núcleo** — `GET /v1/minhas-turmas` deixa de devolver aula de situação `cancelada`; a
  paginação passa a contar só as aulas devolvidas. O filtro da tela, da fatia 34, sai
  (`RF-09-42`).
- **Núcleo** — nasce `GET /v1/aulas/{id}/presencas`: as presenças **não anuladas** da aula, cada
  uma com nick, avatar, momento do fato e modo de comprovação (reconhecimento ou confirmação).
  Exige a operação `suas_turmas`; o Mestre só lê aula das comunidades dele, e a de fora
  responde como inexistente (`RF-09-145`, `RF-09-42`, `RN-09-08`, `RN-09-18`).
- **App 09** — a tela da aula abre com a lista **Presentes nesta aula**, por nick e avatar
  desenhado, com hora e modo; a lista se recarrega depois de uma confirmação de presença bem
  sucedida. O formulário de ocorrência segue como está (`RF-09-145`, `RF-09-45`).
- **App 09** — sai a seção **Atividades presenciais** de Minhas turmas. A seção **Atividades
  on-line** e o atalho de lançamento das presenciais dentro da tela da aula ficam
  (`RF-09-73`, reescrito).

## Capabilities

### New Capabilities

Nenhuma.

### Modified Capabilities

- `aula-e-presenca`: a leitura das turmas do Mestre deixa de trazer a aula cancelada; nasce a
  leitura das presenças da aula pelo Mestre.
- `area-do-mestre`: Minhas turmas deixa de listar as atividades presenciais à parte, e a tela
  da aula passa a listar os presentes.

## Impact

- `backend/src/nucleo/aulas/rotas.py` (rota nova e filtro em `listar_minhas_turmas_rota`) e
  `backend/tests/` das duas rotas. Sem migração.
- `apps/app-09-mestre/src/turmas/` — `api.ts`, `TelaDeMinhasTurmas.tsx`, `TelaDaAula.tsx` e
  `turmas.test.tsx`.
- A App 03 também lê `/v1/minhas-turmas`, na escolha da aula do Quiz ao Vivo: passa a não
  receber aula cancelada, que não tem partida a conduzir. Nenhum código da App 03 muda.
- Fora do escopo: escolher o Guerreiro(a) da ocorrência pela lista de presentes (decisão do
  fundador: só listar); anular presença, que segue do Admin na App 03 (`RF-02-36`).
- Documentação: PRD-09 (`RF-09-73` reescrito, `RF-09-145` novo, a rota em §9, a jornada §5.5 e
  "Decisões de 2026-11-20" em §13), linha nova no documento 09 §1 e a fatia 36 no cronograma.
