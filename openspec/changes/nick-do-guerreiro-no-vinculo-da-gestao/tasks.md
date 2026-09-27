# Tasks

## 1. Lista de vínculos da App 03

- [ ] 1.1 (`RF-02-06`) Em `apps/app-03-gestao/src/personas/FormularioDeResponsavel.tsx`,
      resolver o nick pelo `guerreiro_id` do vínculo contra o estado `guerreiros`, e
      apresentar cada linha como `<nick> — <grau de parentesco>` (design — decisões 1 e 2).
      Verificável: dois vínculos de mesmo parentesco deixam de produzir linhas idênticas na
      tela.
- [ ] 1.2 (`RF-02-06`) Cobrir o caso sem correspondência no estado carregado — a linha
      permanece visível e marca o Guerreiro(a) como não identificado, em vez de exibir o
      parentesco sozinho (design — decisão 3). Verificável: vínculo cujo `guerreiro_id` não
      está na lista ainda rende uma linha distinguível.

## 2. Testes da App 03

- [ ] 2.1 (`RF-02-06`) Em `apps/app-03-gestao/src/personas/personas.test.tsx`, cobrir os
      três cenários novos do delta: o vínculo confirmado identifica o Guerreiro(a) pelo
      nick; dois vínculos de parentesco "Pai" continuam distinguíveis; Guerreiro(a) sem
      nick gravado não apaga a linha. Verificável: `vitest run` da App 03 verde, e a
      asserção do nick falha se a tela voltar a imprimir só o parentesco.

## 3. Documentação

- [ ] 3.1 Marcar a fatia 23 do PRD-02 como implementada em
      `openspec/cronograma-de-fatias.md`. Nada mais muda em `docs/`: a change não toma
      decisão nova, não altera requisito de PRD, não muda a situação do PRD-02 em
      `docs/prds/index.md`, não muda relação entre documentos e não cria arquivo.
