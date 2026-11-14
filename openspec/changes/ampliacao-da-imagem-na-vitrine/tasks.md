# Tasks

## 1. Vitrine

- [x] 1.1 Ligar `ampliavel` no `MidiaDoNucleo` de
      `apps/app-06-vitrine/src/portfolio/ProducaoDoAcervo.tsx` e ajustar o comentário do
      componente, que hoje diz "sem camada sobreposta", para dizer que a imagem aberta na linha
      amplia em tela cheia (`RF-03-85`, `RF-03-88`, decisão do fundador de 2026-11-14)
- [x] 1.2 Atualizar o comentário de `ampliavel` em `comum/react/MidiaDoNucleo.tsx`, que diz que
      a vitrine não a pede (`RF-03-85`)

## 2. Testes

- [x] 2.1 Em `apps/app-06-vitrine/src/testes/portfolioERanking.test.tsx`, casos da ampliação:
      tocar na imagem aberta a amplia sem nova busca ao núcleo; "Fechar", `Esc` e toque fora
      fecham, devolvem o foco e mantêm a produção aberta; o vídeo não ganha controle de ampliar;
      a imagem de uma customização do kit também amplia (`RF-03-85`, `RF-03-88`, `RN-03-22`)

## 3. Documentação

- [x] 3.1 Documento 15 §12: a ampliação em tela cheia alcança também a App 06, com a decisão
      de 2026-11-14; documento 09 §1: tirar "e a vitrine (App 06) não muda" da linha de
      2026-11-11 e registrar a decisão de 2026-11-14 em "Já decididos"; acrescentar ao bloco
      PRD-03 de `openspec/cronograma-de-fatias.md` a linha "—" desta change, implementada. O
      PRD-03, `docs/prds/index.md`, o documento 99 e a `nav` não mudam
