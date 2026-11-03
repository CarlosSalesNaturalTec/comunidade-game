# Design

## Context

Motivação em `proposal.md` — Why. Requisito em `specs/camada-visual-comum/spec.md`.

Três restrições já consolidadas moldam o desenho, e nenhuma se reabre aqui:

- A figura é **um `<path>` só**, vazado por `fill-rule="evenodd"`, porque a monocromática é
  traço e não tem segunda cor para pintar contraforma.
- O traçado usa **só `M`, `C`, `L` e `Z`** — sem arco —, para que todo número do `d` seja
  coordenada e os pares nunca escorreguem na leitura do teste.
- As cinco peças trazem o **mesmo `d` literal**; nos conjuntos a figura reencaixa por
  `transform`, que já existe e não muda.

Geometria medida no `simbolo.svg`, na grade de `48`: perna com `1,3` de largura e ~`3,1` de
comprimento, chão das duas em `y = 35,5`, vão livre entre elas `2,9`.

## Goals / Non-Goals

**Goals:**

- Dar aos pés uma forma que sobreviva ao `evenodd` sem virar buraco.
- Manter o vão entre as pernas não menor que a largura da perna.

**Non-Goals:**

- Legibilidade da garra nos conjuntos e no favicon. Ali ela fica em sub-pixel, e o requisito
  "O reconhecimento no tamanho mínimo é do escudo, não da figura" já cobre o caso.
- Qualquer alteração em silhueta do escudo, razões de contorno, cor ou área de proteção.

## Decisions

### 1. O pé é dobra do contorno externo, não traço sobreposto

Sob `evenodd`, uma segunda subpath cruzando a perna **vira buraco** na interseção — e na
monocromática não há cor para disfarçar:

```text
   traço sobreposto à perna            pé como dobra do contorno
   (duas subpaths)                     (uma subpath só)

        │███│                               │███│
     ▒▒▒┼───┼▒▒▒  ← interseção          ╱───┤███│
        │███│       vira BURACO        ╱────┤███│
                                            │███│
              ✗                                  ✓
```

O pedido fala em "traço perpendicular", mas a peça solta é impossível aqui. O pé entra como
dobra do próprio contorno externo, na base da perna.

**Descartado:** barra abutida à perna, compartilhando aresta — costura de meio pixel em
qualquer rasterização. **Descartado:** traço solto flutuando ao lado da perna — lê como
sujeira abaixo de 48 px.

### 2. Garra afilada, rente ao chão

A ponta afina de `1,4` na raiz para `0,75`, com a base plana em `y = 35,5`. A aresta
superior inclinada é o que dá a leitura de garra apoiada no chão; uma barra de altura
constante lê como degrau.

**Descartado:** barra recuada do chão, com a perna sobrando abaixo — é a leitura mais
literal de "traço perpendicular", mas parece estribo. **Descartado:** barra retangular rente
— vira bloco só com a perna.

### 3. `2,3` de comprimento, com a perna esquerda afastada `0,7`

A garra nasce na borda interna da perna e avança para a esquerda, comendo o vão. O piso
adotado é **contraforma nunca menor que o traço que a cerca** — aqui, `1,3`:

| Garra | Afastamento | Vão livre | |
| --- | --- | --- | --- |
| `1,8` | `0` | `1,1` | fecha a 32 px |
| `2,3` | `0` | `0,6` | fecha a 48 px |
| **`2,3`** | **`0,7`** | **`1,3`** | **adotado — no piso** |
| `2,6` | `0,7` | `1,0` | abaixo do piso |

`2,3` é por isso o **teto** da garra para o afastamento de `0,7`.

Afasta-se **só a perna esquerda**: o topo da direita é o fim da curva do ventre, e
deslocá-la alteraria a silhueta do corpo. Afastar não é translação — o topo da perna encosta
na barriga, que é recortada de novo, com os pontos de controle das curvas vizinhas
acompanhando na mesma fração.

**Descartado:** alongar as pernas em `0,8`. É o que mais compra legibilidade a 48 px, e foi
recusado pelo fundador: muda a proporção da ave.

### 4. O trecho que muda

Só o segmento inferior do contorno externo — da barriga à direita até a barriga à esquerda.
Cabeça, bico, ovo, cauda, penas e vazados ficam intactos.

**Antes:**

```text
C33 29.8 30.6 31.4 27.8 32.1L27.6 35.5L26.3 35.5L26.2 32.4
C25.2 32.6 24.4 32.6 23.6 32.6L23.4 35.5L22.1 35.5L22 32.5
C20.2 32.3 18.4 31.7 16.9 30.7
```

**Depois:**

```text
C33 29.8 30.6 31.4 27.8 32.1L27.6 35.5L24 35.5L24 34.75L26.3 34.1L26.2 32.4
C24.99 32.6 23.91 32.6 22.9 32.6L22.7 35.5L19.1 35.5L19.1 34.75L21.4 34.1L21.3 32.5
C19.78 32.3 18.4 31.7 16.9 30.7
```

## Risks / Trade-offs

- **O vão fica exatamente no piso (`1,3`), sem folga.** → É decisão, não descuido: é o maior
  pé que cabe no afastamento fechado. Qualquer pedido futuro de garra maior reabre o
  afastamento, não o piso.
- **A garra não resolve nos conjuntos nem no favicon.** → Coberto pelo requisito do tamanho
  mínimo; conferido por rasterização e registrado no `proposal.md` para a revisão do PR.
- **Cinco arquivos com o mesmo `d` copiado à mão divergem com facilidade.** → O caso
  `"traz a mesma figura do símbolo"` de `comum/marca.test.ts` já recusa a divergência; a
  cópia é literal, nunca redigitada.
- **A figura desce de `35,5` para o mesmo `35,5`** — a garra é rente e não alonga a caixa.
  → Nenhum ponto novo se aproxima do contorno do escudo; conferido ponto a ponto.
