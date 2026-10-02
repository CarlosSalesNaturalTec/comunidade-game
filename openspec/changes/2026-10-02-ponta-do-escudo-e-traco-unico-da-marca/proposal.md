# Proposal

Origem: a **linha transversal da marca** do `openspec/cronograma-de-fatias.md` — não é fatia
de PRD. O escudo é a forma da marca do projeto (documento 15 §13) e serve o cabeçalho das
**oito** aplicações.

A change não fecha recorte de `RF`: executa a decisão do fundador de **2026-10-02** sobre a
forma do escudo, que desce aos documentos 09 e 15 aqui.

## Why

**O topo do escudo é uma aresta reta.** O fundador trouxe um modelo de referência em que o
topo são **duas curvas côncavas que se encontram numa ponta central**, e decidiu adotá-lo.
O desenho de hoje — `M6 4.5 H42` — é a aresta reta que sai.

A referência foi **medida**, não estimada, para que a decisão não dependesse de olhômetro:

| Medida da referência | Valor | Normalizado |
| --- | --- | --- |
| Largura | 99 px | `1,000` |
| Altura | 116 px | `1,172` |
| Ápice acima do ombro | 21 px | `0,181` |

A taxa de abertura acelera do ápice para o ombro — meia-largura a cada 3 linhas de varredura:
`3,5 → 3 → 3 → 4 → 5 → 7,5` —, o que caracteriza a curva como **côncava**, e não convexa.

**A proporção vigente não comporta a ponta.** O escudo é hoje `42 : 39`, mais largo que alto;
a referência é `1 : 1,172`, mais alta que larga. O documento 15 §13.1 fixa `42 : 39`, e o
§13.4 deriva a área de proteção da altura do escudo. Adotar a ponta com a proeminência da
referência cresce a altura em 26% e move os dois números.

**E há uma segunda coisa, que só aparece ao ir mexer:** a aresta do topo está escrita **à mão
em seis arquivos, em três escalas**. A medição mostra que são **escalamento puro** — não há
variação intencional a preservar:

| Escala | Arquivos | Raio do canto | Contorno |
| --- | --- | --- | --- |
| 32,31 | `marca-horizontal`, `-mono` | 7,149% | 3,559% |
| 42,00 | `simbolo`, `-mono` | 7,143% | 3,571% |
| 45,24 | `favicon`, `marca-empilhada` | 7,139% | 3,581% |

Raio a ~7,14% e contorno a ~3,57% da largura em todas; a variação é ruído de arredondamento.
A **afinação óptica própria** que a change `2026-10-02-marca-do-projeto-e-silhueta-de-nivel`
atribuiu ao favicon na tarefa 1.1 **não foi executada**: ele é o símbolo ampliado em 7,71%,
com as mesmas razões. Mudar a forma do escudo sem tratar isso é repetir a cópia manual seis
vezes e deixar as seis divergirem depois sem ninguém notar — a duplicidade que o
`comum/marca/README.md` §7 proíbe entre arquivos, acontecendo dentro deles.

## What Changes

- **O topo do escudo passa a ter ponta**, por duas curvas côncavas, em **todas** as peças que
  o carregam. Monograma `CG`, cores, contorno e base em ponta ficam como estão.
- **Variante A — fidelidade ao modelo** (decisão do fundador): o escudo adota a proporção
  `1 : 1,172` da referência, com a ponta a **18,1%** da altura. Com isso ele passa a ser
  limitado pela **altura** da grade em todo arquivo: ganha altura e perde largura.
- **O documento 15 §13.1 muda a proporção** de `42 : 39` para `1 : 1,172`, e descreve o topo
  em ponta. O **§13.4** acompanha, porque a área de proteção é metade da altura do escudo.
- **O favicon acompanha a mesma forma** (decisão do fundador).
- **A forma do escudo passa a ser uma só**, verificável, em vez de seis cópias manuais. O
  **como** — guarda por teste ou geração a partir de um traço — é a decisão 3 do `design.md`,
  levantada a pedido do fundador.
- **O documento 09 §1** recebe a decisão nova, em "Já decididos".

## Impact

- `comum/marca/`: seis arquivos redesenhados — `simbolo`, `simbolo-mono`, `favicon`,
  `marca-horizontal`, `marca-horizontal-mono`, `marca-empilhada`. As submarcas não têm escudo
  e não são tocadas.
- `comum/marca.test.ts`: o orçamento de peso **não muda** — `simbolo.svg` usa 1.357 B de
  3.072, e duas cúbicas no lugar de `H42` custam ~50 B. Ganha a verificação da forma única.
- `docs/15-identidade-visual.md` §§13.1 e 13.4; `docs/09-topicos-em-aberto-e-sugestoes.md` §1.
- Nenhuma aplicação muda de comportamento: `MarcaDoProjeto` embute os arquivos por `?raw` e
  não conhece a forma.

## Decisões recebidas na elicitação

- **`favicon.svg` e `simbolo.svg` ficam idênticos** sob a Variante A (decisão do fundador,
  2026-10-02). Os dois são limitados pela mesma grade de 48, e o favicon perde a ampliação de
  7,71% que tinha para preencher a grade. A alternativa — favicon com margem menor, seguindo
  maior — foi descartada.

## Open Questions

1. **Dois arquivos idênticos, ou um só?** É a consequência direta da decisão acima, e ela não
   se resolve sozinha: `simbolo.svg` e `favicon.svg` passam a ter o mesmo conteúdo, e manter
   dois é a duplicidade que o `README.md` §7 proíbe e que esta própria change combate no §3.
   `comum/marca/provisionamento.ts` copia o arquivo para o `public/` de cada aplicação sob o
   nome `favicon.svg`, e **a origem dele pode ser `simbolo.svg`** — o nome de destino não
   depende do nome de origem. Contra: manter o arquivo separado preserva o gancho para uma
   afinação a 16 px, se um dia ela for mesmo feita. Decisão do fundador.
2. **A legibilidade a 16 px foi conferida por cálculo, não por olho.** Na Variante A a ponta
   mede 8,42 unidades na grade de 48, o que dá **2,8 px** no tamanho mínimo do documento 15
   §13.4. É o dobro do que daria um meio-termo, e por isso a Variante A é a que **sobrevive**
   ao tamanho mínimo; ainda assim, a conferência final é visual e é do fundador.
