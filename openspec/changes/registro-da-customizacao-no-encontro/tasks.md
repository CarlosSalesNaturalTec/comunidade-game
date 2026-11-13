# Tasks

## 1. `comum/customizacao` — a situação e a ação do kit

- [ ] 1.1 `comum/customizacao/CustomizacaoDoKit.tsx`: o bloco e `ultimoRegistroDoKit` movidos de
      `apps/app-05-guerreiro/src/carteira/Conquistas.tsx`, com as mesmas frases e props e o tipo
      `FormularioAberto`, exportados no `indice.ts`; entrada `./customizacao/api` no
      `comum/package.json` (`RF-05-103`, `RF-04-80`, design — decisões 1 e 2). Verificação:
      tarefa 1.2.
- [ ] 1.2 Testes em `comum/customizacao/customizacaoDoKit.test.tsx`: os oito cenários do delta
      de `camada-visual-comum` — as cinco situações do último registro, o último decide a ação,
      as mesmas palavras nas duas aplicações e a recusa ao cancelar (`RF-05-103`, `RF-04-80`).
      Verificação: `npx vitest run` no recorte, verde.

## 2. App 05 — consumo do bloco

- [ ] 2.1 `apps/app-05-guerreiro/src/carteira/Conquistas.tsx` passa a importar `CustomizacaoDoKit`
      e `ultimoRegistroDoKit` do `comum/customizacao`, sem cópia local; em
      `Conquistas.test.tsx` muda só o alvo dos espiões da customização para
      `comum/customizacao/api`, sem editar asserção (`RF-05-103`, design — decisão 2).
      Verificação: o teste do recorte verde.

## 3. App 01 — o registro no percurso

- [ ] 3.1 `apps/app-01-aula-presencial/src/trilhas/TelaDeTrilhasDoGuerreiro.tsx`: leitura de
      `lerMinhasCustomizacoes` junto com as do percurso, em `catch` próprio; seção
      "Customização dos seus kits" nos três estados do percurso, um item por kit com
      `customizacao_aberta`, identificado por kit e trilha, com o `CustomizacaoDoKit` e um
      formulário aberto por vez; releitura só da customização depois de cada ato; seção ausente
      sem kit aberto; aviso único na falha só da customização (`RF-04-80`, PRD-04 §5.13.1,
      design — decisões 3 e 4). Verificação: tarefa 3.2.
- [ ] 3.2 Testes em `trilhas/trilhas.test.tsx`: os cinco cenários do delta de
      `aplicacao-da-aula-presencial` — kit aberto oferece o registro, sem kit o percurso não
      muda, registro confirmado passa a aguardar a aula, o pendente se cancela, a customização
      não carrega sem esconder trilhas e atividades —, com as chamadas sob o `token` da sessão
      do Guerreiro(a) (`RF-04-80`). Verificação: `npx vitest run` no recorte, verde.

## 4. Documentação

- [ ] 4.1 PRD-04 §9: tabela das rotas da customização em que o ato é do Guerreiro(a) — as
      cinco que o PRD-05 §9 já lista, na sessão do Guerreiro(a) (`RF-04-80`); e a linha da fatia
      35 em `openspec/cronograma-de-fatias.md` como `implementado`, com o slug. Sem decisão
      nova: documento 09, `docs/prds/index.md`, documento 99 e `mkdocs.yml` não mudam.

## Workflow follow-up

- `/opsx:apply`, depois `/opsx:verify` e `/opsx:archive`.
