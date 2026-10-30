# Design

## Context

Ver `proposal.md` — Why. O que molda o desenho técnico:

- A silhueta do escudo **não muda**, então o bloco de casos `"o escudo tem uma forma só"` do
  `comum/marca.test.ts` — silhueta normalizada, proporção `1 : 1,172`, ponta no topo, ápice
  contra a grade — continua valendo **sem alteração**. Foi o argumento decisivo contra trocar
  o escudo pelo coração.
- `comum/marca.test.ts` lê o **primeiro** `<path>` de cada peça como escudo e o **segundo**
  como figura interna. A figura precisa, portanto, ser **um `<path>` só**.
- A versão monocromática é **traço vazado sem preenchimento**, em `currentColor`, e o teste
  proíbe que declare qualquer cor. Não existe segunda cor disponível para desenhar contraforma.
- O contorno monta sobre a linha de centro: **metade cresce para dentro** e come largura útil
  da figura. Por isso a espessura foi decidida antes do desenho.
- A caixa útil dentro do escudo foi **medida**, não estimada:

| `y` | Largura entre linhas de centro | Útil sob o contorno mono de (a) |
| --- | --- | --- |
| 9,65 | 38,4 | 35,7 |
| 14 | 38,1 | 35,4 |
| 20 | 36,3 | 33,6 |
| 27,6 | 31,6 | 28,9 |
| 32 | 27,2 | 24,5 |
| 36 | 22,0 | 19,3 |

Acima de `y ≈ 10` o ombro do escudo fecha rápido — a `y 8` a forma tem metade da largura. A
figura **não pode crescer para cima**.

## Goals / Non-Goals

**Goals:**

- Trocar a figura interna nas cinco peças sem tocar a geometria do escudo.
- Engrossar o contorno sem que o ápice saia cortado pela grade em peça alguma.
- Deixar a figura verificável pelo teste que já existe, com o mínimo de caso novo.

**Non-Goals:**

- Reabrir a silhueta do escudo, a proporção ou a área de proteção.
- Mexer nas submarcas, que não carregam escudo.
- Reabrir o losango do badge de nível, que o escudo liberaria — a troca já está entregue e
  voltar atrás seria churn sem ganho.
- Afinação específica por tamanho: o `favicon.svg` deixou de existir em 2026-10-02 e o
  `provisionamento.ts` serve o `simbolo.svg`. **Não reintroduzir arquivo por tamanho.**

## Decisions

### 1. O contorno vai a `2,0/42` (colorida) e `3,0/42` (mono)

O teto é `3,28/42`, imposto pelo caso do ápice contra a grade no `simbolo.svg` (ápice em
`y 1,5`, logo `sw ≤ 3,0` em grade de 48, logo razão `≤ 3,28/42`).

| Arquivo | `stroke-width` hoje | Novo |
| --- | --- | --- |
| `simbolo.svg` | 1,37 | **1,83** |
| `simbolo-mono.svg` | 2,29 | **2,74** |
| `marca-horizontal.svg` | 0,90 | **1,20** |
| `marca-horizontal-mono.svg` | 1,50 | **1,80** |
| `marca-empilhada.svg` | 1,28 | **1,71** |

A relação de peso entre mono e colorida cai de 1,67× para 1,50×. **Alternativas descartadas:**
preservar 1,67× exigiria mono a `3,17/42`, a 97% do teto, sem margem; engrossar só a colorida
deixaria a relação em 1,25×, invertendo a razão de a mono ser mais pesada.

A `RAZAO_DE_CONTORNO` do teste muda junto — é ela que guarda os dois números.

### 2. A figura é um `<path>` só, com `fill-rule="evenodd"`

Olho, penas da cauda e vazados do corpo são **subcaminhos do mesmo path**. **Alternativas
descartadas:** elementos `<circle>` separados com cor de fundo — impossível na mono, que não
tem segunda cor; dois ou mais `<path>` — quebra a leitura do teste, que pega o segundo.

É como o monograma `CG` já funcionava: os contornos do `C` e do `G` nascem do enrolamento do
próprio traçado.

### 3. Pernas e apêndices são traçados dentro do contorno

Sob `evenodd`, subcaminho sobreposto ao corpo vira **buraco** na área de encontro. Uma haste
colada por cima abriria emenda branca na junta com a barriga. As pernas entram no traçado da
barriga: descendo pela lateral direita, atravessando a base e subindo pela esquerda.

### 4. As penas da cauda são vazadas por dentro, não entalhadas no contorno

Tentado e **descartado por medição visual**: entalhe raso em silhueta pequena lê como
serrilha, não como pena. A cauda passa a ser massa cheia e larga, com três lentes vazadas
abrindo o leque por dentro — silhueta limpa e leque visível.

### 5. O caso do teste deixa de falar em monograma

`"%s mantém o monograma dentro do escudo"` passa a conferir a **figura**. A mecânica não muda:
amostra o contorno do escudo em polígono e pergunta se os cantos da caixa da figura estão
dentro. Segue rodando só em `simbolo.svg` e `simbolo-mono.svg`, porque nos conjuntos a figura
reencaixa por `transform`.

**Lacuna conhecida, não coberta pelo teste:** ele mede contra a **linha de centro** do escudo,
não contra a borda interna do traço. Figura que passe no teste ainda pode encostar
visualmente no contorno engrossado. A conferência é de entrada, como o filete do elenco.

### 6. A geometria apurada

Figura na grade de 48, caixa `x 13,8–36,2` por `y 9,5–35,5`:

| Elemento | Medida |
| --- | --- |
| Bico — comprimento da dobradiça à ponta | 3,6 un., **igual nas duas mandíbulas** |
| Bico — ângulo em relação ao eixo | 18°, **igual para cada lado** |
| Ovo | ø 2,6 un., no eixo do bico, folga 0,98 e 0,94 até as pontas |
| Olho vazado | ø 3,2 un., em cabeça de 6,5 un. de altura |
| Cabeça × pescoço | ~8 un. contra ~4,7 un. de largura |
| Pernas | 2, largura ~1,5 un., sem pés, base em `y 35,5` |

O traçado corrente (v6 dos esboços), para a implementação partir dele:

```text
M13.8 26C13.6 23.4 14.4 21 15.9 19.8C16.6 18.8 16.3 16.2 16.3 14.6C16.3 12.6 17 10.9 18.8
10.2C20.6 9.4 22.6 9.8 23.8 11.2C24.8 12.4 24.8 13.2 24.4 14.2C25.6 15 26.9 16.1 28
17.15C26.9 16.9 25.7 16.4 24.6 16C25.3 16.9 26.1 17.9 26.7 18.95C25.4 18.3 24 17.4 22.95
16.4C22.4 16.5 21.9 16.6 21.4 16.6C21 18.2 21 19.6 21 20.8C23.4 21.8 26.2 22.4 28.8
21.8C31 21.2 33 18.8 35.2 15.4C36.6 19.2 36.2 24 34.2 27.6C33 29.8 30.6 31.4 27.8
32.1L27.6 35.5L26.3 35.5L26.2 32.4C25.2 32.6 24.4 32.6 23.6 32.6L23.4 35.5L22.1 35.5L22
32.5C20.2 32.3 18.4 31.7 16.9 30.7C15.5 29.8 14.3 28.2 13.8 26ZM19.3 12.9a1.6 1.6 0 1 0
3.2 0a1.6 1.6 0 1 0-3.2 0ZM27.6 19.25a1.3 1.3 0 1 0 2.6 0a1.3 1.3 0 1 0-2.6 0ZM30.8 23C32
21.2 33.4 19.2 34.8 17.4C34.1 19.8 32.7 21.9 30.8 23ZM31.4 25.2C32.8 23.9 34 22.8 35.2
21.8C34.2 23.6 33 24.8 31.4 25.2ZM31.6 27.6C32.6 26.9 33.6 26.2 34.4 25.6C33.7 26.9 32.8
27.6 31.6 27.6ZM18.4 27.2C20.8 25.4 24 24.2 26.8 24C24.4 25.9 21.2 27.1 18.4 27.2ZM19.6
29.4C22 27.8 25.2 26.7 28 26.6C25.6 28.4 22.4 29.4 19.6 29.4ZM21.8 31.2C23.8 30 26.2 29.2
28.2 29.1C26.4 30.4 24 31.2 21.8 31.2Z
```

**O orçamento de peso não é problema:** a figura mede **1.087 B** de atributo `d` contra
**1.034 B** do monograma. O `simbolo.svg` passa de 1.395 B para ~1.448 B, de 3.072 do teto.

### 7. Nos conjuntos a figura reencaixa por `transform`

Os três conjuntos levam o escudo em escalas diferentes (38,4 · 25,26 · 35,84 de largura). A
figura **não é redesenhada** em cada um: entra o mesmo traçado, reposicionado por `transform`,
como o monograma já fazia. É o que mantém o requisito de a figura ser a mesma em todas.

## Risks / Trade-offs

- **O desenho acumulou seis rodadas e segue com acabamentos apontados** — pontas da cauda
  arredondadas, ausência das serrilhas da crista, silhueta puxando para pato → são ajuste de
  traço dentro das tarefas, não bloqueio; a revisão final acontece no PR, com a figura aplicada
  nas cinco peças.
- **O contorno engrossado come ~0,45 un. na faixa baixa** → a figura foi desenhada já sob a
  espessura nova; nenhuma tarefa deve engrossar depois.
- **A mono fica a 0,13 un. da borda da grade** no ápice, contra 0,355 hoje → passa no teste,
  mas é a folga que some se alguém engrossar mais. O teto está registrado no design e na
  `RAZAO_DE_CONTORNO`.
- **A figura tem mais detalhe que o monograma e fecha a 16 px** → aceito e virou requisito: o
  reconhecimento no tamanho mínimo é do escudo e da cor. O `CG` de hoje também fecha.
- **A imagem de referência tem licença desconhecida** → é **medida, não traçada**; o desenho é
  produzido pelo projeto, como o `README.md` §8 declara dos demais arquivos.

## Migration Plan

Não se aplica: a marca é arquivo versionado servido no build, sem dado gravado e sem estado.
Nenhuma aplicação conhece a figura — `MarcaDoProjeto` embute por `?raw` e o favicon nasce da
cópia do `simbolo.svg` pelo `provisionamento.ts`. Reverter é reverter o commit.

## Open Questions

Nenhuma que mude specs, abordagem ou recorte de tarefas. Os três acabamentos de traço
apontados em `proposal.md` — Open Questions resolvem-se dentro das tarefas, com o fundador
revisando no PR.
