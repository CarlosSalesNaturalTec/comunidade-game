# Tasks

## 1. Lista de vínculos da App 09

- [x] 1.1 (`RF-09-63`) Em `apps/app-09-mestre/src/responsaveis/TelaDeResponsaveis.tsx`,
      resolver o nick pelo `guerreiro_id` do vínculo contra o estado `guerreiros`, e
      apresentar cada linha como `<nick> — <grau de parentesco>` (design — decisões 1 e 2).
      Verificável: dois vínculos de mesmo parentesco deixam de produzir linhas idênticas.
- [x] 1.2 (`RF-09-63`) Cobrir o caso sem correspondência no estado carregado — a linha
      permanece visível e marca o Guerreiro(a) como não identificado (design — decisão 3).
      Verificável: vínculo cujo `guerreiro_id` não está na lista ainda rende uma linha
      distinguível.

## 2. Testes da App 09

- [x] 2.1 (`RF-09-63`) Em `apps/app-09-mestre/src/responsaveis/responsaveis.test.tsx`,
      cobrir os três cenários novos do delta: o vínculo apresentado identifica o
      Guerreiro(a) pelo nick; dois vínculos de parentesco "Pai" continuam distinguíveis;
      Guerreiro(a) sem nick gravado não apaga a linha. Verificável: `vitest run` da App 09
      verde, e a asserção do nick falha se a tela voltar a imprimir só o parentesco.

## 3. Documentação

- [x] 3.1 Marcar a fatia 21 do PRD-09 como implementada em
      `openspec/cronograma-de-fatias.md`. Nada mais muda em `docs/`: a change não toma
      decisão nova, não altera requisito de PRD, não muda a situação do PRD-09 em
      `docs/prds/index.md`, não muda relação entre documentos e não cria arquivo.
