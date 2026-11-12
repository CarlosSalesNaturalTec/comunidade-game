# Proposal

**PRD de origem:** PRD-03 — Vitrine pública (App 06). **Fatia:** nenhuma numerada — linha "—"
nova no bloco do PRD-03 do `openspec/cronograma-de-fatias.md`, como as demais correções por
decisão do fundador.

**Identificadores:** **muda o enunciado** do `RF-03-78`; preserva, sem mudar enunciado,
`RF-03-42`, `RF-03-43`, `RF-03-51` e `RN-03-01`.

## Why

Três decisões do fundador de 2026-11-12:

1. **O endereço da plataforma aparece onde o projeto se apresenta.** `comunidadegame.org` já é a
   raiz da vitrine (documento 03), mas não está escrito na página inicial da documentação nem
   no `README.md` do repositório — quem chega por eles não acha a plataforma.
2. **A saudação da vitrine troca a promessa técnica pela ideia do jogo.** O subtítulo "Tudo aqui
   é aberto — sem cadastro e sem login." passa a "Este é um jogo em que as partidas acontecem
   na vida real". A vitrine segue sem login (`RN-03-01`); só a frase muda.
3. **A porta "Quero apoiar" abre pela doação sem cadastro.** A seção "Doar sem se cadastrar"
   sobe ao início da página, antes de "Quero apoiar"; o garfo do que a pessoa traz vem em
   seguida. Contradiz o texto vigente — documento 02 §1, documento 08 e `RF-03-78` dizem que a
   porta **abre** pela pergunta do que a pessoa traz —, então desce pelo fluxo: documento 02 →
   documento 09 → PRD-03 → change (decisão confirmada pelo fundador em 2026-11-12).

## What Changes

- **Documentação (antes do código):** documento 02 §1 ("A pergunta de entrada…") e o trecho
  correspondente do documento 08 passam a dizer que a porta abre pela doação PIX e em seguida
  pergunta o que a pessoa traz; documento 09 — linha nova em "Já decididos"; PRD-03 §5.5
  itens 3 e 4 e o enunciado do `RF-03-78`; linha nova do cronograma.
- **Endereço:** `docs/index.md` e `README.md` ganham o link para `https://comunidadegame.org`.
- **App 06 — cabeçalho:** `CabecalhoDaVitrine` troca o subtítulo; a composição de teste
  `TelaDaVitrine` acompanha.
- **App 06 — porta do convite:** em `PortaDoConvite`, "Doar sem se cadastrar" passa a ser a
  primeira seção, com título de mesmo nível de "Quero apoiar" (h2). Nada mais muda na porta: o
  conteúdo da chave PIX, o garfo, as necessidades em aberto e o "voltar" ficam como estão.

## Capabilities

### New Capabilities

Nenhuma.

### Modified Capabilities

- `aplicacao-da-vitrine`: a porta passa a abrir pela doação sem cadastro, e o garfo do que a
  pessoa traz vem logo depois (`RF-03-78`, `RF-03-42`, `RF-03-43`).

## Impact

- **Código:** `apps/app-06-vitrine/src/componentes/CabecalhoDaVitrine.tsx`,
  `apps/app-06-vitrine/src/convite/PortaDoConvite.tsx` e os testes `abertura.test.tsx`,
  `convite.test.tsx`, `saidaDoBuild.test.ts` e a composição `testes/TelaDaVitrine.tsx`.
- **Documentação:** `README.md`, `docs/index.md`, documentos 02, 08 e 09, PRD-03 e o
  cronograma. Nenhum arquivo novo em `docs/`, nada muda na `nav` nem no documento 99.
- **Núcleo, rotas e dados:** nenhum. Sem migração.

## Fora do escopo

- A descrição de SEO de `pages/index.astro` ("Aberta, sem cadastro e sem login.") — o pedido é
  o subtítulo visível; a descrição segue verdadeira.
- O `site_url` do `mkdocs.yml`, que é o endereço do site da documentação, não o da plataforma.
