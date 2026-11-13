# Proposal

Origem: **PRD-09 — Área do Mestre (App 09)**, **fatia 32** do `openspec/cronograma-de-fatias.md`.

Atende o identificador **novo** `RF-09-142`, criado por esta change na revisão do PRD-09, junto
de `RF-09-03` (paginação pelas etapas), já atendido. Aplica a decisão do fundador de
**2026-11-13**, tomada no `/opsx:propose` que abriu a change.

## Why

Em Minhas trilhas, cada missão da etapa aberta aparece por inteiro — atos, materiais, nove
blocos recolhíveis e a pré-visualização —, uma embaixo da outra. Com duas ou mais missões na
etapa, a tela vira uma rolagem longa em que o Mestre não acha a missão que quer escrever. O
bloco recolhível (documento 15 §6.1) já resolve isso dentro da missão; falta aplicá-lo à missão
inteira.

## What Changes

- **Documento 15 §6.1**: uma frase — tela que empilha itens que juntam, cada um, seus próprios
  blocos recolhe também o item inteiro, que nasce fechado; item sozinho fica aberto.
- **Documento 09 §1**: a decisão entra em "Já decididos".
- **PRD-09**: nasce `RF-09-142` (com mais de uma missão na etapa, cada missão inteira se
  mostra e se oculta, e nasce oculta); §13 e §15 acompanham.
- **App 09**: `ListaDeMissoes` envolve cada missão num `BlocoRecolhivel` quando recebe mais de
  uma — título com posição e nome, resumo com sondagem, obrigatoriedade e dificuldade. Com uma
  missão só, a tela fica como está.

## Capabilities

### New Capabilities

Nenhuma.

### Modified Capabilities

- `area-do-mestre`: a missão inteira se recolhe na etapa que tem mais de uma.

## Fora do escopo

- Núcleo, contrato de API e migração: a mudança é só de tela.
- Lembrar entre visitas qual missão estava aberta — o bloco nasce fechado a cada montagem,
  como o documento 15 §6.1 já fixa.
- Recolher missões em outras telas ou aplicações (pré-visualização, App 01, App 05).
- O que o PRD-09 §3.2 já exclui.

## Impact

- `apps/app-09-mestre/src/trilhas/ListaDeMissoes.tsx` e `trilhas.test.tsx`; CSS da App 09 só se
  o bloco externo pedir ajuste.
- Documentos 09 e 15 e PRD-09. Nenhuma relação entre documentos muda: o doc 99 fica como está
  (a linha "Bloco recolhível" já aponta para o documento 15 §6.1).
