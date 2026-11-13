# Tasks

## 1. App 09

- [x] 1.1 `trilhas/ListaDeMissoes.tsx`: extrair o corpo da missão (linha, materiais, atos,
      correção, blocos internos e pré-visualização) para uma função de render; com mais de uma
      missão, envolvê-lo num `BlocoRecolhivel` de título `"{posição}. {título}"` e resumo com
      sondagem, obrigatoriedade e dificuldade; com uma, render como hoje (`RF-09-142`,
      `RF-09-03`, design — decisões 1 a 4)
- [x] 1.2 `index.css` da App 09: ajuste de espaçamento do bloco externo da missão, só se a
      leitura do bloco aninhado pedir (`RF-09-142`, design — riscos). Não pediu: a lista não tem
      CSS próprio e o recuo do `cg-bloco-recolhivel__conteudo` já separa os blocos internos

## 2. Testes

- [x] 2.1 `trilhas/trilhas.test.tsx`: etapa com duas missões nasce com as duas recolhidas e
      sem atos alcançáveis; "Mostrar" abre só a escolhida e o controle vira "Ocultar"; etapa
      com uma missão fica aberta sem controle; a linha recolhida declara a sondagem
      (`RF-09-142`, `RF-09-03`)
- [x] 2.2 `trilhas/trilhas.test.tsx` e demais testes da App 09 que abrem etapa com várias
      missões: abrir a missão antes de interagir com o que fica dentro dela (`RF-09-142`)

## 3. Documentação

- [x] 3.1 Documento 15 §6.1 (uma frase: item que junta seus próprios blocos também recolhe,
      nasce fechado, e fica aberto quando sozinho), documento 09 §1 ("Já decididos"), PRD-09
      (`RF-09-142` no §6.1, "Decisões de 2026-11-13" no §13, linha no §15) e a fatia 32 como
      `implementado` em `openspec/cronograma-de-fatias.md`. Doc 99, `docs/prds/index.md` e
      `mkdocs.yml` não mudam (`RF-09-142`)
