# Tasks

## 1. Núcleo — ordem alfabética dos adultos

- [x] 1.1 Em `backend/tests/test_vitrine.py`, cobrir a ordem alfabética das listagens de
      Mestres e de Apoiadores: nick e nome na mesma ordenação, identificação com **acento** no
      lugar certo, e a paginação por cursor em páginas de dez percorrendo a lista inteira sem
      pular nem repetir (`RF-03-83`, `RF-03-79`, `RN-03-40`)
- [x] 1.2 Em `backend/src/nucleo/vitrine/publico.py`, `_paginar_adultos_publicos` passa a
      `LEFT JOIN` em `Nick` e a ordenar por `(COALESCE(nick.valor, persona.nome), persona.id)`
      com collation `pt-BR`, e o cursor passa a levar `{valor, id}` — verificado pelos casos de
      1.1 passando (`RF-03-83`, design — decisão 5)
- [x] 1.3 Conferir que a proibição de pódio segue válida: nenhuma resposta de Apoiador traz
      posição nem admite ordenação por valor, pelos casos já existentes de `RN-14-38` e
      `RN-03-26` em `test_vitrine.py` (`RN-03-40`)

## 2. Núcleo — portfólio em ordem decrescente

- [x] 2.1 Em `backend/tests/test_vitrine.py`, cobrir o portfólio respondendo da criação mais
      recente para a mais antiga, e o cursor percorrendo essa ordem sem pular nem repetir
      (`RF-03-08`, `RF-03-83`)
- [x] 2.2 Em `backend/src/nucleo/vitrine/rotas.py`, `listar_criacoes_publicas` inverte
      `order_by` para decrescente e o keyset de `>` para `<` — verificado pelos casos de 2.1
      passando (`RF-03-83`)

## 3. App 06 — a lista de registros paginada

- [x] 3.1 Criar o componente de lista de registros da App 06, genérico sobre o tipo do item:
      uma linha por registro em `<ol>`, avatar opcional, dados principais, a célula de
      identificação como `<a href>`, dez por página, avançar e voltar por pilha de cursores em
      `useState` e a posição em texto com `aria-live` (`RF-03-02`, `RF-03-03`, `RF-03-82`,
      design — decisões 1 a 4). Verificado por 3.3
- [x] 3.2 Em `apps/app-06-vitrine/src/api/leituras.ts`, as leituras de ranking, criações,
      mestres, apoiadores e comunidades passam a aceitar `tamanho=10` e `cursor`, e
      `listarGuerreiros` sai; `GuerreiroPublico` e as leituras individuais ficam (`RF-03-82`,
      design — decisões 6 e 7)
- [x] 3.3 Em `apps/app-06-vitrine/src/testes/`, cobrir o componente de lista: dez linhas na
      primeira página, lista curta sem controles, avançar e voltar percorrendo tudo sem pular
      nem repetir, linha sem avatar sem abrir buraco, ausência de cabeçalho de coluna e de
      grade, e nada gravado no aparelho (`RF-03-02`, `RF-03-82`, `RN-03-22`)

## 4. App 06 — as cinco seções que passam a lista

- [x] 4.1 `ranking/SecaoDoRanking.tsx` passa a lista de linhas com avatar, nick, posição e
      pontos regulares, e a linha abre `/guerreiros/{nick}` (`RF-03-09`, `RF-03-03`,
      `RN-03-02`)
- [x] 4.2 `portfolio/SecaoDoPortfolio.tsx` passa a lista de linhas com trilha, data e os
      autores por avatar e nick, **cada nick** abrindo a página dele, em ordem decrescente
      (`RF-03-08`, `RF-03-03`, `RF-03-83`)
- [x] 4.3 `SecaoDeMestres.tsx` e `SecaoDeApoiadores.tsx` passam a montar lista de linhas em vez
      de grade de cards — a linha do Apoiador leva o total em moedas, sem posição (`RF-03-02`,
      `RF-03-03`, `RF-03-07`, `RF-03-10`, `RN-03-26`, `RN-03-40`). `adultos/SecaoDeAdultos.tsx`
      **saiu**, substituído pelo componente de 3.1, como o `proposal` (Impact) e o `design`
      (decisão 2) determinam; as duas seções consomem o componente direto
- [x] 4.4 `territorio/SecaoDeComunidades.tsx` passa a lista de linhas **sem avatar**, com nome,
      localização e vinculados, e a representação visual fica só na página da comunidade
      (`RF-03-02`, `RF-03-15`)
- [x] 4.5 Em `apps/app-06-vitrine/src/testes/`, atualizar os casos das cinco seções para a
      forma de linha, cobrindo os critérios de aceite do PRD-03 §12: ordem alfabética em
      Mestres, Apoiadores e comunidades, portfólio pela mais recente, total em moedas sem
      posição nem controle de ordenação, e a linha abrindo a página individual (`RF-03-02`,
      `RF-03-03`, `RF-03-83`, `RN-03-40`)

## 5. App 06 — os Guerreiros e Guerreiras só com a consulta

- [x] 5.1 `guerreiros/SecaoDeGuerreiros.tsx` fica só com `BuscaPorNick` e a frase de que a
      vitrine não lista quem está cadastrado; sai o consumo de `SequenciaPaginada`, a rotação e
      a lista de cards (`RF-03-12`, `RF-03-13`, `RN-03-06`)
- [x] 5.2 Atualizar `testes/TelaDaVitrine.tsx` e os casos que afirmavam sobre os cards e a
      rotação dos Guerreiros — inclusive os de `arena.test.tsx` e `cardsEPagina.test.tsx` —,
      cobrindo que a seção traz a consulta e nenhum Guerreiro(a), que nada rotaciona em tela
      pública alguma e que a página individual segue alcançável pela consulta, pelo ranking e
      pelo nick do portfólio (`RF-03-03`, `RF-03-11`, `RF-03-12`, `RF-03-13`)
- [x] 5.3 Conferir que `comum/react` não foi tocado: `SequenciaPaginada` e `CartaDoPersonagem`
      seguem exportados e com os consumidores de fora da vitrine passando (design — decisão 2)

## 6. Verificação de integração

- [x] 6.1 Conferir pelo teste da saída do build que todo endereço público segue servido pelo
      arquivo publicado, que as páginas de pessoa seguem fora do `sitemap.xml` e `noindex`, e
      que nenhuma seção virou documento servido por engano (`RF-03-51`, PRD-03 §10)
- [x] 6.2 Conferir os invariantes 9, 10, 12, 16 e 21 do documento 99 §6 no que a change tocou:
      nenhuma tela traz imagem real, nome civil, rede social ou contato de Guerreiro(a); o
      ranking segue só com pontos regulares; nenhuma lista compara Apoiadores por valor

## 7. Documentação

- [x] 7.1 Marcar a linha da fatia em `openspec/cronograma-de-fatias.md` como `implementado`,
      com o slug desta change na coluna Recorte. Os documentos 03 §8, 08, 09 §1, 11 §§8.1 e
      8.2, 15 §5 e o PRD-03 **já foram atualizados** no commit `c0e6e05`, antes desta change;
      `docs/prds/index.md`, o documento 99 e a `nav` do `mkdocs.yml` **não mudam** — a situação
      do PRD-03 é a mesma, nenhuma relação entre documentos mudou e nenhum arquivo nasceu
