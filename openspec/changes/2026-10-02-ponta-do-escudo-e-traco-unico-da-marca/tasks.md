# Tasks

> A change não fecha recorte de `RF`: executa a decisão do fundador de 2026-10-02 sobre a forma
> do escudo. Cada tarefa cita a seção que atende.
>
> Os números do desenho — proporção, ápice, ombro e base por arquivo — estão na decisão 1 do
> `design.md`, e descem ao documento 15 na tarefa 4.1. Nenhuma tarefa os reinventa.

## 1. A forma nova, nas duas peças do símbolo

- [ ] 1.1 Redesenhar `simbolo.svg` — escudo `39,68 × 46,50` na grade `48 × 48`, ápice em
      `y 0,75`, ombro em `y 9,17`, base em `y 47,25`, topo por duas curvas côncavas. Manter
      monograma `CG`, degraus de cor e espessura de contorno. Conferir que cabe nos 3 KB do
      manifesto, não traz `<text>`, filtro nem referência externa, e nenhuma cor fora da paleta
      (documento 15 §§3.2, 13.1; `README.md` §§1, 7)
- [ ] 1.2 Redesenhar `simbolo-mono.svg` na mesma geometria — **em traço**, `currentColor`, sem
      preenchimento e sem declarar valor de cor algum, com o monograma cheio dentro. É desenho
      próprio, não derivação da colorida (documento 15 §13.3; `design.md` — decisão 2)

## 2. A forma nova, nas demais peças

- [ ] 2.1 `favicon.svg` fica **idêntico** a `simbolo.svg` — mesma forma, mesma grade `48 × 48`,
      mesma margem (decisão do fundador, 2026-10-02). Resolver antes a questão 1 da
      `proposal.md`: se os dois passam a ser **um arquivo só**, com `provisionamento.ts`
      copiando `simbolo.svg` para o `public/` sob o nome `favicon.svg`, ou se seguem dois com
      o mesmo conteúdo (documento 15 §13.4; `README.md` §§1, 7)
- [ ] 2.2 Redesenhar o escudo de `marca-horizontal.svg` e `marca-horizontal-mono.svg` —
      `25,60 × 30,00`, altura preservada e largura estreitando. Recalcular a posição do
      logotipo e a largura do `viewBox`, de `223,5` para o valor que o novo escudo pedir.
      Conferir que o conjunto segue equilibrado com o escudo 21% mais estreito (documento 15
      §13.5; `design.md` — decisão 1)
- [ ] 2.3 Redesenhar o escudo de `marca-empilhada.svg` — `35,84 × 42,00`, recentrado em
      `x = 80`, na caixa `160 × 96` preservada (documento 15 §13.5)
- [ ] 2.4 Conferir que as duas submarcas **não** foram tocadas: elas não carregam escudo, porque
      o escudo significa a plataforma (documento 15 §13.1)

## 3. A forma passa a ser uma só

> Assume a saída (a) da decisão 3 do `design.md` — guarda por teste. Se o fundador escolher
> também a (b), a geração entra em fatia própria.

- [ ] 3.1 Em `comum/marca.test.ts`, afirmar que o escudo das seis peças, **normalizado pela
      largura declarada**, descreve a mesma silhueta dentro de tolerância de arredondamento —
      e que raio de canto e espessura de contorno guardam a mesma razão com a largura em todas
      (spec: "O escudo tem uma forma só, em todas as peças da marca")
- [ ] 3.2 Afirmar que a silhueta da monocromática coincide com a da colorida na mesma escala, e
      que o que difere entre elas é preenchimento e cor (spec: mesmo requisito)
- [ ] 3.3 Afirmar que o ápice, somado a metade da espessura do contorno, cabe na grade de cada
      peça — a ponta nunca sai cortada (spec: "A ponta do escudo sobrevive ao tamanho mínimo")
- [ ] 3.4 Conferir que o orçamento de peso do manifesto segue valendo **sem alteração**, nas
      seis peças (`README.md` §1)

## 4. Documentação

- [ ] 4.1 Documento 15 §13.1: trocar a proporção `42 : 39` por `1 : 1,172` e descrever o topo em
      ponta por duas curvas, com a ponta a 18,1% da altura. Acertar o §13.4, cuja área de
      proteção é metade da altura do escudo
- [ ] 4.2 Conferência visual do fundador no tamanho mínimo de 16 px, antes de fechar: por
      cálculo a ponta mede 2,8 px, e o número não substitui o olho (documento 15 §13.4)
- [ ] 4.3 Documento 09 §1: gravar a decisão nova em "Já decididos" — a forma do escudo, a
      variante escolhida e a origem dela
- [ ] 4.4 `comum/marca/README.md` §8: corrigir a procedência, que descreve o símbolo como
      "escudo geométrico" sem ponta, e retirar a atribuição de "afinação óptica própria" ao
      favicon, que a medição mostrou não existir
- [ ] 4.5 `openspec/cronograma-de-fatias.md`: fechar a situação da linha desta fatia
- [ ] 4.6 Conferir os invariantes do documento 99 §6 — em especial o 24, que proíbe o
      temperamento mudar a marca — e a numeração contínua das seções do documento 15

## 5. Verificação

- [ ] 5.1 `vitest run` em `comum/` — a suíte da marca, uma vez, ao fechar as tarefas de código
- [ ] 5.2 `biome format --check .` e `biome check .` em `comum/`
- [ ] 5.3 `npm run fix`, `npm run lint` e `mkdocs build --strict` — a change toca `docs/`
