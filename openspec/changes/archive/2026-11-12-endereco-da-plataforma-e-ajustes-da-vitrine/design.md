# Design

## Context

A porta do convite e o cabeçalho já existem (`openspec/specs/aplicacao-da-vitrine/spec.md`); a
change só reordena uma seção e troca uma frase. O domínio `comunidadegame.org` já está decidido
no documento 03 — nada a decidir sobre ele.

## Goals / Non-Goals

**Goals:** as três decisões da proposal, com os documentos emendados no mesmo PR.

**Non-Goals:** mexer na descrição de SEO, no conteúdo da chave PIX, no garfo ou nas
necessidades em aberto.

## Decisions

1. **"Doar sem se cadastrar" é `h2`, irmã de "Quero apoiar"** (decisão do fundador de
   2026-11-12). Fica dentro de `cg-vitrine cg-convite`, antes do `h2` "Quero apoiar", numa
   `<section>` própria. Descartado: `h3` acima de um `h2`, que quebra a hierarquia de títulos
   para leitor de tela.
2. **O parágrafo "O apoio é ao projeto, nunca a uma pessoa" fica sob "Quero apoiar"**, onde
   está: ele explica a chamada, não a doação.
3. **O subtítulo muda só em `CabecalhoDaVitrine`** e na composição de teste `TelaDaVitrine`, que
   o replica. A frase sai sem ponto final, como o fundador a escreveu. Os comentários que
   descrevem a saudação como "a promessa de que nada pede login" passam a descrever a frase
   nova; `RF-03-51` e `RN-03-01` seguem cumpridos pela vitrine, não pelo texto.
4. **O endereço entra como link** `https://comunidadegame.org`, em uma linha logo após o
   parágrafo de abertura de `docs/index.md` e do `README.md`. `docs/index.md` é o único
   documento de `docs/` autorizado a linkar; o `README.md` é da raiz.

## Risks / Trade-offs

- [O Lychee confere o link novo e a rede corporativa bloqueia `*.comunidadegame.org`, por
  domínio recém-registrado (comentários dos workflows de deploy)] → o CI roda no GitHub, fora
  dessa rede; se ainda assim falhar, o domínio entra no `.lycheeignore`, como os demais
  bloqueados, e é conferido à mão.
- [`saidaDoBuild.test.ts` e `convite.test.tsx` conferem a porta] → ganham a asserção de ordem;
  o restante segue valendo.
