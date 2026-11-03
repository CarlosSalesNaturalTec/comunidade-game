# Proposal

Origem: a **linha transversal da marca** do `openspec/cronograma-de-fatias.md` — não é fatia
de PRD. A change não fecha recorte de `RF`: executa a decisão do fundador de **2026-11-03**
sobre a figura dentro do escudo, pelo mesmo molde de
`2026-10-30-sankofa-no-escudo-e-contorno-mais-grosso` e de
`2026-10-02-ponta-do-escudo-e-traco-unico-da-marca`, e pelo precedente de que desenho de
marca não gera identificador novo.

## Why

**O pássaro ficou sem pés, e com eles perdeu metade do próprio gesto.** A change de
2026-10-30 entregou a figura com "pernas sem pés", declarado em proposta. O Sankofa é a ave
que **anda para a frente com a cabeça virada para trás** — e o desenho hoje mostra só a
cabeça virada. A direção da marcha não aparece em lugar nenhum: as pernas descem retas e
terminam cegas.

**Os pés voltados para o lado oposto ao bico são o que torna a marcha visível.** O bico
aponta para a direita, alcançando o ovo; a garra aponta para a esquerda. É a oposição entre
as duas pontas que diz, numa figura parada, que a ave avança enquanto olha para trás. Por
isso a direção não é detalhe de acabamento: ela carrega o sentido, como a cabeça virada e o
ovo já carregam.

**O vão entre as pernas não comporta a garra como as pernas estão hoje.** Medido no
`simbolo.svg`: o vão livre entre as pernas é `2,9` e cada perna tem `1,3` de largura. A
garra de `2,3` nasce na borda interna da perna direita e avança para a esquerda, o que
deixaria o vão em `0,6` — menos da metade do traço que o cerca, e fechado já a 32 px. Daí o
afastamento, que é consequência da garra e não decisão à parte.

## What Changes

- **Cada perna ganha uma garra** — traço perpendicular à perna, voltado para o lado oposto
  ao bico, rente ao chão em `y = 35,5`. Comprimento `2,3`, altura `1,4` na raiz afinando
  para `0,75` na ponta.
- **A perna esquerda é afastada em `0,7`**, o que devolve o vão livre a `1,3` — igual à
  largura da perna, que é o piso adotado: contraforma nunca menor que o traço que a cerca.
  Afastar não é translação: o topo da perna encosta na curva da barriga, que é recortada de
  novo, com os pontos de controle das curvas vizinhas acompanhando.
- **A perna direita não se move.** O topo dela é o fim da curva do ventre, e deslocá-la
  alteraria a silhueta do corpo.
- **As pernas não são alongadas.** Alongá-las em `0,8` foi levantado — é o que mais compra
  legibilidade a 48 px — e **descartado pelo fundador**: muda a proporção da ave, e o pedido
  era pé maior, não ave mais alta.
- **`2,3` é o teto da garra** para este afastamento. Passar dele exige reabrir o
  afastamento, que está fechado em `0,7`.
- Só o **segundo `<path>`** de cada um dos cinco arquivos muda, com o mesmo `d` literal. A
  silhueta do escudo, a proporção `1 : 1,172`, a ponta no topo, as razões de contorno, as
  cores e a área de proteção **não mudam**.

## Capabilities

### New Capabilities

Nenhuma. A change altera o requisito de uma capacidade existente.

### Modified Capabilities

- `camada-visual-comum`: o requisito **"A figura dentro do escudo é o pássaro Sankofa"** é
  **substituído**. Ele exige hoje que a figura preserve *"os dois elementos que dão o
  sentido do símbolo — a cabeça virada para trás e o ovo"*. Entra um terceiro: a **direção
  da marcha**, dada pelos pés voltados para o lado oposto ao bico. É o elemento que faltava
  para o gesto estar inteiro, e escrevê-lo em spec é o que impede que um redesenho futuro o
  descarte em silêncio — que foi o que aconteceu com os pés em 2026-10-30.

## Impact

- `comum/marca/`: cinco arquivos — `simbolo.svg`, `simbolo-mono.svg`,
  `marca-horizontal.svg`, `marca-horizontal-mono.svg`, `marca-empilhada.svg` —, todos com o
  mesmo `d`, literalmente idêntico. Nos três conjuntos a figura reencaixa pelo `transform`
  **que já existe**, sem alteração. As submarcas não carregam escudo e não são tocadas.
- `comum/marca.test.ts`: **nenhum caso muda e nenhum caso entra.** Os invariantes já
  valem sobre o `d` novo — traçado só com `M`, `C`, `L` e `Z`, número par de coordenadas,
  todo ponto dentro do escudo, um `<path>` só com `fill-rule="evenodd"`, mesma figura nas
  cinco peças, peso dentro do orçamento.
- Orçamento de peso: `simbolo.svg` vai de 1.676 B para ~1.721 B, contra teto de 3.072.
- `comum/marca/README.md` §8: uma oração na procedência, registrando o refinamento de
  2026-11-03. É o lugar onde a história do desenho já mora.
- `openspec/cronograma-de-fatias.md`: linha transversal nova, com `—` na coluna do número,
  logo após a da `2026-10-30-sankofa-no-escudo-e-contorno-mais-grosso`.
- Nenhuma aplicação muda de comportamento: `MarcaDoProjeto` embute os arquivos por `?raw` e
  não conhece a figura; o favicon acompanha sozinho, porque `provisionamento.ts` copia o
  `simbolo.svg`.
- **Fora do escopo:** a silhueta do escudo, as razões de contorno, as submarcas, o badge de
  nível em losango, o elenco, a moldura circular do avatar e os três acabamentos que a
  change de 2026-10-30 deixou apontados (pontas da cauda, serrilhas da crista, silhueta que
  puxa para pato).

## Open Questions

1. **`docs/15-identidade-visual.md` §13.1 não é tocado, e `docs/09` não recebe linha nova.**
   No §13.1 o símbolo é "escudo com o pássaro Sankofa dentro": pé é detalhe abaixo desse
   nível de abstração, e descrevê-lo ali contraria a regra da concisão. No documento 09 a
   decisão de 2026-10-30 já está registrada, e esta é refinamento dela, não regra nova —
   linha nova seria o crescimento de diário que as regras de redação proíbem. A decisão fica
   no `proposal.md`/`design.md` desta change, no cronograma e na procedência do README.
   **Se o fundador preferir o registro no documento 09, é uma linha a acrescentar.**
2. **A conferência final do desenho é visual e é do fundador.** A garra foi julgada em
   rasterização de 48 px reais, com o pixel ampliado, e nos cinco arquivos aplicados. O que
   o estudo mostra e convém dizer no PR: nos dois conjuntos — horizontal a `32` de altura e
   empilhada — a garra fica em **sub-pixel e não resolve**. Isso **não é defeito**: o
   requisito "O reconhecimento no tamanho mínimo é do escudo, não da figura" já admite que
   a figura feche. O detalhe vive do símbolo a 48 px para cima.
