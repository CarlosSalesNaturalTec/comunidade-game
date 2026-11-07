# Proposal

PRD-03, **fatia 13** do `openspec/cronograma-de-fatias.md` — O acervo na carta e na página do
Guerreiro(a). Atende `RF-03-05`, `RF-03-86`, `RF-03-87`, `RN-03-41` e `RN-03-43`, e preserva
`RF-03-06`, `RF-03-84` e `RF-03-85`.

## Why

A fatia 12 uniu as duas fontes do acervo só na seção "Portfólio de criações originais". A carta
e o portfólio da página do Guerreiro(a) seguem lendo só a criação da culminância, e por isso
dizem "Nenhuma criação original validada ainda." a quem tem comprovações aprovadas no portfólio
da vitrine — contradição com o invariante 5 do documento 99 §6. Decisão do fundador de
2026-11-07, registrada no documento 09 §1 e no documento 11 §8.2.

## What Changes

- A projeção pública do Guerreiro(a), em `/vitrine/guerreiros` e em `/vitrine/guerreiros/{nick}`,
  passa a levar em `criacoes` o **acervo público** dele — a criação da culminância e as
  comprovações do prático —, sob o portão do `RN-03-41`, em ordem **decrescente** pela data de
  aprovação. Cada item ganha o formato do item do acervo da vitrine: identificador, fonte,
  título (`RN-03-43`), tipo, produção e autoria. Os campos `trilha` e `validada_em` de hoje
  continuam no item: a mudança no contrato é **aditiva**, mas o conjunto e a ordem mudam.
- A coluna "Criações originais" da carta lista cada item com **título e data**. (`RF-03-86`)
- O portfólio abaixo da carta, na página, passa a usar a **linha do portfólio da vitrine** —
  título, data, trilha fora da culminância, autoria por nick — e a **abrir a produção** na
  própria linha. (`RF-03-87`, `RF-03-85`)

**Fora do escopo** — o que o PRD-03 §3.2 já exclui, e o que a fatia 12 deixou nomeado: o
acervo na área do Guerreiro(a), que exibe tudo e é do PRD-05; o badge de autoria, que fica só
na culminância; e qualquer escrita pela vitrine (`RN-03-01`).

## Capabilities

### New Capabilities

Nenhuma.

### Modified Capabilities

- `leitura-publica-da-vitrine`: a carta pública do Guerreiro(a) passa a trazer o acervo
  público, nas duas fontes, em ordem decrescente e no formato do item do acervo.
- `aplicacao-da-vitrine`: a coluna da carta lista o acervo com título e data, e o portfólio da
  página usa a linha do portfólio da vitrine, que abre a produção.

## Impact

- Núcleo: `backend/src/nucleo/vitrine/publico.py` (a carta) e `rotas.py` (o montador do item do
  acervo, hoje preso à listagem). Sem migração e sem rota nova.
- App 06: `src/guerreiros/carta.ts`, `src/guerreiros/PaginaDoGuerreiro.tsx`,
  `src/portfolio/SecaoDoPortfolio.tsx` e `src/api/leituras.ts`.
- Contrato público: o item de `criacoes` ganha campos; quem consome `trilha` e `validada_em`
  não quebra.
