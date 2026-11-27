# Tasks

## 1. App 09

- [x] 1.1 Em `apps/app-09-mestre/src/trilhas/ListaDeMissoes.tsx`, passar a
      `PreVisualizacaoDaMissao` as recompensas de marco da missão e o catálogo de tipos de
      recurso (`RF-09-25`, `RF-09-84`); verificável pela tarefa 2.1.
- [x] 1.2 Em `apps/app-09-mestre/src/trilhas/PreVisualizacaoDaMissao.tsx`, acrescentar o
      trecho "O que só você vê", depois do desafio: nomes distintos dos tipos de recurso das
      recompensas, sem quantidade, ou "Nenhuma recompensa pelo desbloqueio declarada ainda."
      (`RF-09-84`); no prático, título curto e kit apresentado quando não nulos (`RF-09-131`,
      `RF-09-141`, `RN-09-50`); no quiz, o corte de 60% ou, na sondagem, a abertura ao
      responder (`RN-05-45`, `RN-05-46`); verificável pela tarefa 2.1.

## 2. Testes

- [x] 2.1 Em `apps/app-09-mestre/src/trilhas/trilhas.test.tsx`, no grupo "pré-visualização da
      missão (RF-09-25)", cobrir os cenários do delta: recompensa pelo nome sem quantidade e
      sem repetição; sem recompensa; prático com título curto e kit; prático sem os dois;
      corte do quiz; sondagem sem corte (`RF-09-25`, `RF-09-84`, `RF-09-131`, `RF-09-141`,
      `RN-05-45`, `RN-05-46`, `RN-09-50`).

## 3. Documentação

- [x] 3.1 Na linha da fatia 39 de `openspec/cronograma-de-fatias.md`, a situação vira
      `implementado`. Nada em `docs/`, `docs/prds/index.md`, doc 99 ou `nav` muda: decisão de
      exibição sem requisito novo.

## Workflow follow-up

- `/opsx:verify` e `/opsx:archive` ao fim; um PR com artefatos, código, testes e cronograma.
