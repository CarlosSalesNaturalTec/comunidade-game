# Tasks

Sem `RF`/`RN`: linha transversal da marca, pelo precedente de
`2026-10-30-sankofa-no-escudo-e-contorno-mais-grosso`. O que cada tarefa atende é o requisito
"A figura dentro do escudo é o pássaro Sankofa" de `camada-visual-comum`.

## 1. O desenho

- [ ] 1.1 Trocar o segmento inferior do contorno externo da figura no `comum/marca/simbolo.svg`
      pelo traçado do `design.md` §4 — garra de `2,3` afinando de `1,4` para `0,75`, rente em
      `y = 35,5`, perna esquerda afastada `0,7`. Verificar com
      `npx vitest run comum/marca.test.ts`: os casos de traçado só com `M`/`C`/`L`/`Z`, figura
      dentro do escudo, `<path>` único com `evenodd` e orçamento de peso passam.
- [ ] 1.2 Copiar o **mesmo `d` literal** para `simbolo-mono.svg`, `marca-horizontal.svg`,
      `marca-horizontal-mono.svg` e `marca-empilhada.svg`, sem tocar o `transform` dos
      conjuntos nem o primeiro `<path>` de cada arquivo. Verificar que o caso
      `"traz a mesma figura do símbolo"` passa para as cinco peças.

## 2. A conferência visual

- [ ] 2.1 Rasterizar o `simbolo.svg` em 48 px reais e conferir o cenário
      "A marcha aponta para o lado oposto ao olhar": os dois pés se distinguem, voltados para
      o lado oposto ao bico, e o vão entre as pernas não fecha. Anexar a imagem ao PR, porque
      a conferência final do desenho é do fundador (`proposal.md` — Open Questions).
- [ ] 2.2 Conferir as cinco peças aplicadas — os dois conjuntos nos tamanhos nominais
      (`marca-horizontal` a `32` de altura, `marca-empilhada` em `160×96`) e a monocromática
      sobre fundo escuro. Registrar no PR que a garra fica em sub-pixel nos conjuntos, o que o
      requisito do tamanho mínimo já admite.

## 3. A documentação

- [ ] 3.1 Acrescentar a linha transversal em `openspec/cronograma-de-fatias.md`, com `—` na
      coluna do número e situação `implementado`, logo após a da
      `2026-10-30-sankofa-no-escudo-e-contorno-mais-grosso`; e registrar o refinamento de
      2026-11-03 em **uma oração** na procedência do `comum/marca/README.md` §8. Verificar com
      `npm run lint` (a change toca `.md`). **Nada mais muda em `docs/`:** o documento 15 §13.1
      descreve o símbolo como "escudo com o pássaro Sankofa dentro", acima do nível do detalhe;
      o documento 09 já registra a decisão de 2026-10-30, de que esta é refinamento; nenhum
      arquivo nasce, nenhum PRD muda de situação e nenhuma relação entre documentos muda.
