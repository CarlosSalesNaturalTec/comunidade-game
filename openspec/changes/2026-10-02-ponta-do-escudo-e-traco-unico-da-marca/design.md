# Design

## Context

O escudo existe em seis arquivos de `comum/marca/`, em três escalas, cada um com a aresta do
topo escrita à mão. `MarcaDoProjeto.tsx` embute `simbolo.svg` e `simbolo-mono.svg` por `?raw`
e não conhece a forma; nenhuma aplicação a conhece. Trocar a forma é, portanto, trocar
arquivo — não há código a adaptar.

A referência do fundador foi medida por varredura de máscara (129 × 146, limiar por matiz),
e é dela que saem os números abaixo.

## Decisão 1 — Variante A, de fidelidade ao modelo

O fundador escolheu, entre duas saídas, a que mantém a silhueta da referência.

| | **A — fidelidade** | C — ponta dentro da caixa |
| --- | --- | --- |
| Proporção | `1 : 1,172` (da referência) | `42 : 39` intacta |
| Ponta | 18,1% da altura | 18,1% da altura |
| Documento 15 | §§13.1 e 13.4 mudam | nada muda |
| Conjuntos | re-equilibrados | intactos |
| Silhueta | igual à da referência | mais atarracada |

Escolhida a **A**. A consequência que governa o desenho: com a proporção mais alta que larga,
o escudo passa a ser **limitado pela altura** da grade em todos os arquivos — ganha altura e
perde largura, nunca o contrário.

Os números finais, com margem para o contorno (metade da espessura, senão a ponta sai cortada):

| Arquivo | Escudo (L × A) | Ápice | Ombro | Base |
| --- | --- | --- | --- | --- |
| `simbolo`, `-mono` | 39,68 × 46,50 | y 0,75 | y 9,17 | y 47,25 |
| `favicon` | 39,68 × 46,50 | y 0,75 | y 9,17 | y 47,25 |
| `marca-empilhada` | 35,84 × 42,00 | y 5,00 | y 12,60 | y 47,00 |
| `marca-horizontal`, `-mono` | 25,60 × 30,00 | y 1,00 | y 6,43 | y 31,00 |

Nos dois conjuntos o escudo **mantém a altura que já ocupava** e estreita. Por isso a folga de
1 unidade acima do escudo na marca horizontal — que seria o gargalo se o escudo crescesse para
cima — não morde: ali ele não cresce, encolhe na largura. O que muda é a largura total da
horizontal, de `223,5` para ~`216,8`, e o recentramento do escudo na empilhada em `x = 80`.

## Decisão 2 — a monocromática é desenhada, não derivada

`simbolo-mono.svg` é **traço em `currentColor`, sem preenchimento** (documento 15 §13.3), e o
`README.md` §1 registra que é desenho próprio. A ponta, portanto, **se desenha duas vezes** —
na colorida e na monocromática —, e não se copia de uma para a outra trocando atributo.

Isso não contradiz a decisão 3: o que a forma única garante é que as duas descrevam a **mesma
silhueta**; o que muda entre elas é preenchimento e cor, não geometria.

## Decisão 3 — como a forma passa a ser uma só

Levantada a pedido do fundador. Três saídas, da mais barata à mais completa:

| | O que é | Custo | O que garante |
| --- | --- | --- | --- |
| **a. Guarda por teste** | `comum/marca.test.ts` normaliza o caminho do escudo de cada arquivo pela largura declarada e afirma que os seis coincidem dentro de tolerância | baixo — um teste, nenhum formato muda | Impede divergência futura; não impede o erro de digitação de hoje |
| **b. Geração em build** | Um módulo emite o caminho para uma escala dada; um script gera os seis SVG, no molde de `comum/marca/provisionamento.ts` | médio — muda como os arquivos nascem | Uma fonte; os seis deixam de ser editáveis à mão |
| **c. `<use>` entre arquivos** | Um `<symbol>` referenciado pelos demais | — | **Descartada**: o `README.md` §7 veda referência externa, e cada SVG precisa ser autossuficiente |

**Recomendação: (a) como piso desta change, (b) como fatia própria se o fundador quiser.** A
(a) resolve o risco real — seis cópias divergindo sem ninguém notar — e cabe no teste que já
existe e já confere orçamento de peso. A (b) é maior: muda o fluxo de entrega da marca, que
hoje é "o arquivo é o artefato", e isso merece decisão própria, não carona nesta fatia.

> **A definir:** qual das duas, ou as duas. Enquanto não houver resposta, as tarefas 3.x
> assumem a (a).

## Risks

| Risco | Tratamento |
| --- | --- |
| A ponta some no tamanho mínimo de 16 px | Na Variante A ela mede 8,42 na grade de 48 → **2,8 px** a 16 px. Conferência visual do fundador na tarefa 4.2 |
| A ponta sai cortada pelo contorno | Toda grade reserva metade da espessura do contorno acima do ápice; conferido por teste de caixa envolvente |
| A horizontal estreita demais ao lado do logotipo | O escudo perde 21% da largura; o equilíbrio do conjunto é conferido na tarefa 2.2 |
| O orçamento de peso estourar | Folga medida: `simbolo.svg` em 1.357 B de 3.072. Duas cúbicas custam ~50 B. Teste já existente cobre |
