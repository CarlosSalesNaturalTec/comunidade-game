# Tasks

## 1. Leitura do acervo na App 06

- [ ] 1.1 Em `apps/app-06-vitrine/src/api/leituras.ts`, acrescentar `customizacao_do_kit` a
      `FonteDoAcervo` e trocar o ternário de `lerArquivoDoAcervo` por um
      `Record<FonteDoAcervo, string>` que leva cada fonte à rota dela (`criacoes`,
      `comprovacoes`, `customizacoes`); atualizar os comentários de "duas" para "três" fontes,
      ali e em `portfolio/linhaDoAcervo.tsx`, `portfolio/SecaoDoPortfolio.tsx` e
      `portfolio/ProducaoDoAcervo.tsx` (`RF-03-88`, `RF-03-85`). Verificação: `tsc` do pacote
      sem erro e `grep -n "duas fontes" apps/app-06-vitrine/src` vazio.

## 2. Testes

- [ ] 2.1 Em `apps/app-06-vitrine/src/testes/portfolioERanking.test.tsx`, item da fonte
      `customizacao_do_kit`: cenários "A customização aprovada traz a descrição e a trilha do
      kit", "A criação mais recente abre o portfólio" com as três fontes, e "A customização
      abre a mídia do kit" — o buscador recebe `{ id, fonte: "customizacao_do_kit" }` e a
      leitura de bytes vai a `/v1/vitrine/customizacoes/{id}/arquivo` (`RF-03-88`,
      `RF-03-85`, `RF-03-84`). Verificação: `vitest run` do arquivo verde.
- [ ] 2.2 Em `apps/app-06-vitrine/src/testes/guerreirosEPagina.test.tsx`, Guerreiro(a) com
      registro de customização aprovado: cenários "A customização aprovada aparece na carta"
      e "O portfólio da página traz a customização aprovada", com a mídia aberta na própria
      linha (`RF-03-86`, `RF-03-87`, `RF-03-88`). Verificação: `vitest run` do arquivo verde.

## 3. Documentação

- [ ] 3.1 Acrescentar à tabela de rotas do PRD-03 §9 a linha
      `GET /v1/vitrine/customizacoes/{id}/arquivo` — pública, bytes do registro aprovado da
      customização do kit —, logo abaixo da de comprovações (`RF-03-88`). Verificação: a linha
      está na tabela, com até ~95 caracteres fora dela intactos.
- [ ] 3.2 Marcar a fatia 14 do PRD-03 como `implementado` em `openspec/cronograma-de-fatias.md`,
      com o slug `2026-11-13-customizacao-do-kit-no-portfolio`. Sem decisão nova: documento 09,
      documento-fonte, documento 99, `docs/prds/index.md` e `nav` do `mkdocs.yml` não mudam.
      Verificação: a linha traz o slug e a situação.

## Workflow follow-up

- `/opsx:verify` e `/opsx:archive` depois do PR aprovado.
