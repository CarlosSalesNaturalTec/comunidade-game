# Design

## Context

Ver `proposal.md` — Why. O que o desenho precisa levar em conta:

- **A change anterior não foi integrada.** `2026-10-10-acabamento-da-abertura-da-vitrine` está
  arquivada e no mesmo PR; esta a corrige antes de o PR entrar, e não depois.
- **O corte foi medido, não estimado.** No Chromium, num visor de 360 px, as quatro figuras
  saíam no tamanho natural — soma de 2254 px — e a última ficava partida na borda.
- **O `.cg-heroi` centra os filhos** (`align-items: center`), então o elenco não herda a
  largura do pai sem pedir.
- **O cabeçalho só era ilha por causa do diálogo.** Sem o "Entrar", `CabecalhoDaVitrine` não
  tem estado nenhum.

## Goals / Non-Goals

**Goals:**

- As quatro figuras inteiras em qualquer largura, sem rolagem horizontal, sem depender de
  quanto respiro a moldura tem.
- Um "Entrar" na vitrine inteira, na abertura, e a regra descida pelo fluxo até o documento 03.

**Non-Goals:**

- Mexer em `comum/`.
- Rever o par de ações, as cores, a saudação, o rótulo "Início" ou o tamanho da frase — tudo
  da change anterior, e mantido.
- Levar a regra do "Entrar" às outras sete aplicações: ela é da vitrine.

## Decisions

### 1. A altura do elenco vem da largura do herói, por consulta de contêiner

`.cg-heroi` declara `container-type: inline-size`, e as figuras recebem `height: 44cqw`.

As quatro somam `2254 × 1024`, então a fileira é **2,2 vezes mais larga do que alta** e a
altura que a faz caber é **45,4 %** da largura do herói. `44cqw` deixa cerca de 3 % de folga,
para arredondamento de sub-pixel nunca empurrar a última figura para fora.

Medido no Chromium, com a tela construída de verdade:

| Visor | Altura | Figuras | Rolagem horizontal |
| --- | --- | --- | --- |
| 320 px | 120 px | 36 → 284 | 0 |
| 360 px | 137 px | 37 → 323 | 0 |
| 412 px | 160 px | 38 → 374 | 0 |
| 768 px | 271 px | 94 → 674 | 0 |
| 1280 px | 271 px | 350 → 930 | 0 |

Contra os 96 px de antes da change anterior, são **+43 %** no celular — e nenhum corte.

**Três alternativas descartadas, duas delas por medição:**

- **`100vw` com `margin-inline: calc(50% - 50vw)`** — o que a change anterior entregou. A
  sangria exigia `overflow-x: clip` no herói para não vazar rolagem, e o corte recortava
  justamente a sangria. Era o defeito.
- **`aspect-ratio` na fileira com `height: 100%` nas figuras** — medido e reprovado:
  dependência circular. A altura do contêiner viria da proporção, mas a proporção precisa da
  altura definida, e a altura percentual da figura não resolve contra pai de altura
  indefinida. As figuras caíam no tamanho natural.
- **`calc` sobre `100vw` descontando os respiros** — funciona, mas grava na regra da figura
  quanto respiro a moldura tem. Qualquer mudança de respiro voltaria a cortar, em silêncio.

A sangria até a borda **sai**. Ela foi decidida em 2026-10-10 e é o que gerou as três
tentativas acima; o fundador, vendo o corte, pediu redimensionar ou voltar ao tamanho que não
cortasse. O elenco fica dentro da moldura, e cresce o quanto ela permite.

### 2. O cabeçalho da vitrine deixa de ser ilha

Sem o "Entrar", `CabecalhoDaVitrine` não guarda estado e não abre diálogo: perde o
`client:load` e passa a sair no documento servido. **Uma ilha a menos em toda tela pública** —
é o princípio 4 do documento 15 §1 ganhando por subtração.

A propriedade `comHeroi` de `Vitrine.astro`, criada pela change anterior só para calar o botão
do cabeçalho na abertura, deixa de ter uso e sai junto.

### 3. A entrada, fora da abertura, é alcançada pela marca

`MarcaDoProjeto href="/"` está em **toda** tela pública desde a fatia 9 e leva à abertura. É
o caminho que substitui o botão onde ele deixa de existir, e por isso vira cenário da spec —
sem ele, a regra nova deixaria o visitante de outro recorte sem rota até a entrada.

## Risks / Trade-offs

- **Quem chega por link direto a `/pesquisadores` não vê como entrar** → mitigado pela marca,
  que leva à abertura e está em toda tela; e a vitrine é feita para ser lida, não para
  autenticar. É a consequência aceita da decisão do fundador, registrada aqui para não se
  perder.
- **Consulta de contêiner é recurso recente** (Chrome 105, 2022; Safari 16) → o piso de
  aparelho do documento 15 §1 é celular modesto, não celular antigo, e a App 06 já usa
  `clamp`, `inset` e `isolation`. Onde a consulta não existisse, a figura cairia no tamanho
  natural, que é o defeito de hoje — por isso o guarda do elenco inteiro entra na suíte.
- **A medição vale para o Chromium** → é o motor do Chrome e do Samsung Internet, que é o que
  o público do projeto usa. Firefox e Safari implementam a mesma consulta.
- **Duas changes no mesmo PR** → o `CLAUDE.md` pede um PR por change. Esta corrige a anterior
  antes de o PR ser integrado, e separá-las em dois PRs faria o segundo depender de um ramo
  não integrado. Registrado como desvio consciente, não como descuido.

## Open Questions

Nenhuma.
