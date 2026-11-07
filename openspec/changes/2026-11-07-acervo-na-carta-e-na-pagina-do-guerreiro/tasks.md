# Tasks

## 1. Núcleo — o acervo na carta pública

- [x] 1.1 Mover `CriacaoPublicaSaida`, `FonteDoAcervo` e o montador do item do acervo de
      `vitrine/rotas.py` para `vitrine/publico.py`, como função que recebe criações e
      comprovações já filtradas e devolve os itens hidratados; `listar_criacoes_publicas`
      passa a chamá-la sem mudar resposta nem cursor. Verificar: os testes do acervo de
      `tests/test_vitrine.py` seguem verdes. (`RF-03-84`, `RN-03-41`, `RN-03-43`)
- [x] 1.2 Reescrever `_criacoes_na_carta` com as duas fontes, pelos portões
      `condicoes_de_criacao_publica` e `condicoes_de_comprovacao_publica`, agrupadas por
      Guerreiro(a) — a criação em equipe para cada integrante —, em ordem decrescente por
      `(data, id)`; `CartaPublicaDeGuerreiroSaida.criacoes` vira `list[CriacaoPublicaSaida]` e
      `CriacaoNaCartaSaida` sai. Verificar pela tarefa 1.3. (`RF-03-86`, `RF-03-87`, `RN-03-41`)
- [x] 1.3 Em `tests/test_vitrine.py`, cobrir os cenários do delta de `leitura-publica-da-vitrine`:
      a carta traz as duas fontes nas duas rotas; comprovação não julgada, não publicável ou
      entrega presencial fica fora; ordem decrescente; o item da carta é igual ao do acervo; e
      o número de consultas de uma página de `/vitrine/guerreiros` não cresce com o número de
      itens. (`RF-03-86`, `RF-03-87`, `RN-03-41`, `RN-03-43`)

## 2. App 06 — a carta e a página do Guerreiro(a)

- [x] 2.1 Em `src/api/leituras.ts`, `GuerreiroPublico.criacoes` passa a `CriacaoPublica[]` e
      `CriacaoNaCartaPublica` sai; `src/guerreiros/carta.ts` monta cada item como
      `título — data`. Verificar pela tarefa 2.4. (`RF-03-05`, `RF-03-86`, `RN-03-43`)
- [x] 2.2 Extrair de `src/portfolio/SecaoDoPortfolio.tsx` a linha do acervo para
      `src/portfolio/linhaDoAcervo.tsx`, usada pela seção sem mudar o que ela desenha.
      Verificar: `src/testes/portfolioERanking.test.tsx` segue verde. (`RF-03-85`, `RN-03-43`)
- [x] 2.3 Em `src/guerreiros/PaginaDoGuerreiro.tsx`, o portfólio abaixo da carta desenha os
      itens com `linhaDoAcervo`, na marcação da lista de registros e sem paginação, abrindo a
      produção na linha. Verificar pela tarefa 2.4. (`RF-03-87`, `RF-03-85`)
- [x] 2.4 Em `src/testes/guerreirosEPagina.test.tsx`, cobrir os cenários do delta de
      `aplicacao-da-vitrine`: só comprovações aparecem na coluna pelo título curto e pela data,
      sem a frase de vazio; culminância pelo nome da trilha; o mais recente primeiro; vazio em
      uma frase; o portfólio da página traz as duas fontes e abre a produção; a linha da página
      é a da vitrine. Ajustar o teste do `RF-03-05` ao novo item. (`RF-03-05`, `RF-03-86`,
      `RF-03-87`, `RF-03-85`)

## 3. Documentação

- [x] 3.1 Marcar a fatia 13 do PRD-03 como `implementado` em `openspec/cronograma-de-fatias.md`,
      com o slug da change. Documentos 09 e 11 §8.2, e o PRD-03 (`RF-03-05`, `RF-03-86`,
      `RF-03-87`), já receberam a decisão de 2026-11-07 antes da change; nada mais em `docs/`
      muda, e a situação do PRD-03 em `docs/prds/index.md` não muda.
