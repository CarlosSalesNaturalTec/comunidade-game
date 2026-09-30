# Tasks

## 1. A moldura da Arena

- [x] 1.1 Envolver o conteúdo de `src/layouts/Vitrine.astro` em `FundoDeComunidade`,
      renderizado no build e com `imagem={null}` enquanto a foto não existir na
      plataforma; verificar que toda rota do `dist/` sai com a moldura e que nenhuma
      requisição a terceiro entra com ela (documento 15 §6.3, `RF-03-51`, design —
      decisões 1 e 2)
- [x] 1.2 Acrescentar a mesma moldura a `src/testes/TelaDaVitrine.tsx`, para a
      composição de teste não desviar do layout; verificar que os 176 casos seguem
      verdes (design — decisão 6)

## 2. A carta dominando a página individual

- [x] 2.1 Pôr `PalcoDoPersonagem` na página do Guerreiro(a), com a carta como
      apresentação, "Quero participar" como a decisão única e portfólio e desempenho em
      `apoio`; verificar que a carta é o elemento maior e que sair não conta como
      decisão (`RF-03-03`, `RF-03-05`)
- [x] 2.2 Fazer o mesmo nas páginas de Mestre, de Apoiador e de comunidade, com a
      variante de carta que cada uma já usa; verificar que as três mantêm o que exibiam
      e passam a apresentar uma decisão só (`RF-03-07`, `RF-03-15`, `RF-03-03`)

## 3. Ícone, e o peso da Arena

- [x] 3.1 Levar o `Icone` às ações e aos estados da vitrine que hoje não têm glifo,
      sempre ao lado do rótulo; verificar que nenhum alvo de toque encolhe e que nenhum
      estado passa a depender do glifo (documento 15 §§5, 11.1)
- [x] 3.2 Dar peso de Arena aos cards e às seções em `src/index.css` — carta maior, cor
      chapada com presença, espaçamento da escala do §4 —, consumindo só as camadas
      semântica e de tema; verificar que nenhum valor primitivo é referenciado e que
      nenhum número que o documento 15 não fixe é declarado (documento 15 §§4, 6, 12)

## 4. Testes

- [x] 4.1 Escrever os casos de nível 1 do palco e do ícone: a carta é o elemento maior
      da página individual, a página pede uma decisão só, o ícone nunca aparece sem
      rótulo e nenhum estado depende dele
- [x] 4.2 Acrescentar ao teste da saída do build os casos da moldura: ela sai em toda
      rota indexável e na casca de pessoa, e nenhuma requisição a domínio de terceiro
      entra com ela

## 5. Documentação

- [x] 5.1 Marcar a fatia 10 como `implementado` no `openspec/cronograma-de-fatias.md`,
      com o slug da change. Nenhuma decisão nova foi tomada, nenhum PRD muda, a situação
      do PRD-03 em `docs/prds/index.md` não muda, nenhuma relação entre documentos muda
      e nenhum arquivo nasce em `docs/` — nada mais a atualizar
