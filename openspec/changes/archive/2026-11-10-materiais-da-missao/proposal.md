# Proposal

Origem: **PRD-09 — Área do Mestre (App 09)**, **fatia 30** do `openspec/cronograma-de-fatias.md`,
com o lado da leitura no **PRD-04 — Aula presencial (App 01)**.

Atende identificadores **novos**, criados por esta change na revisão dos dois PRDs: `RF-09-140`,
`RN-09-61` e `RF-04-79`. Aplica a decisão do fundador de **2026-11-10**, tomada no
`/opsx:propose` que abriu a change.

## Why

A aula da missão pede material físico — cola, jumpers, papel —, e hoje o Mestre não tem onde
registrá-lo. Quem aplica a trilha em outra comunidade só descobre o que faltou quando a aula já
começou. A missão passa a dizer o que separar antes.

O mesmo pedido trazia o **pré-requisito de aplicação da trilha**; o fundador o **descartou** na
elicitação, e ele não entra nesta change.

## What Changes

- **Documento 11 §2.2**: a tabela "Toda missão declara" ganha a linha **Materiais** — a lista
  do que a aula da missão pede, só nomes, declarada quando o Mestre quiser.
- **Documento 09 §1**: a decisão entra em "Já decididos".
- **PRD-09**: nascem `RF-09-140` (o Mestre autor declara e corrige os materiais da missão) e
  `RN-09-61` (lista só de nomes, opcional, fora das travas de publicação, corrigível em
  qualquer situação da trilha com a autoria estrita do `RN-09-56`); §8 (`Missao`), §9
  (`POST /v1/trilhas/{id}/missoes` e `PATCH /v1/missoes/{id}`) e §15 acompanham.
- **PRD-04**: nasce `RF-04-79` (a programação do encontro mostra os materiais da missão); §9
  (`GET /v1/equipes/{id}/missao`) e §15 acompanham.
- **Núcleo**: `Missao` ganha `materiais`, lista de nomes, vazia por padrão. Criar e corrigir a
  missão passam a aceitá-la; a leitura da autoria, a resposta da criação e da correção, a
  programação do encontro e a **duplicação da trilha** a carregam. Leva migração Alembic.
- **App 09**: o formulário da missão ganha o campo dos materiais, na criação e na correção, e a
  linha da missão os mostra.
- **App 01**: a programação do encontro mostra os materiais junto da missão.

## Capabilities

### New Capabilities

Nenhuma.

### Modified Capabilities

- `trilha-e-missao`: a missão declara materiais, e a duplicação da trilha os copia.
- `area-do-mestre`: o Mestre declara e corrige os materiais no formulário da missão.
- `aplicacao-da-aula-presencial`: a programação do encontro mostra os materiais da missão.

## Fora do escopo

- O **pré-requisito de aplicação da trilha** — descartado pelo fundador em 2026-11-10.
- Ligação dos materiais ao catálogo de tipos de recurso, à necessidade de recurso ou ao
  patrimônio: o fundador escolheu lista só de nomes, sem quantidade.
- Exibição em outra aplicação que não as Apps 09 e 01 (vitrine, Área do Guerreiro(a)).
- O que o PRD-09 §3.2 e o PRD-04 §3.2 já excluem.

## Impact

- `backend/src/nucleo/trilhas/` (`modelo.py`, `regra.py`, `rotas.py`) e
  `backend/src/nucleo/equipes/rotas.py`; migração em `backend/alembic/versions/`.
- `apps/app-09-mestre/src/trilhas/` (`api.ts`, `FormularioDeMissao.tsx`, `ListaDeMissoes.tsx`).
- `apps/app-01-aula-presencial/src/` (`api/programacao.ts`, `trilhas/TelaDaProgramacao.tsx`).
- Documentos 09 e 11, PRD-09 e PRD-04. Nenhuma relação entre documentos muda: o doc 99 fica
  como está.
