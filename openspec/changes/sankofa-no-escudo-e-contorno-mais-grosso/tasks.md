# Tasks

> A change não fecha recorte de `RF`: executa a decisão do fundador de 2026-10-30 sobre a
> figura dentro do escudo e a espessura do contorno. Cada tarefa cita a seção que atende.
>
> Os números — espessura por arquivo, caixa útil, medidas do bico e o traçado corrente —
> estão nas decisões 1 e 6 do `design.md`. Nenhuma tarefa os reinventa.
>
> **A ordem importa:** o contorno engrossa **antes** da figura entrar. Metade da espessura
> cresce para dentro e come ~0,45 un. da largura útil; a figura foi desenhada já sob a
> espessura nova.

## 1. O contorno mais grosso

- [ ] 1.1 Aplicar o `stroke-width` novo nas cinco peças com escudo, pela tabela da decisão 1
      do `design.md` — `simbolo` 1,83, `simbolo-mono` 2,74, `marca-horizontal` 1,20,
      `marca-horizontal-mono` 1,80, `marca-empilhada` 1,71. Nenhuma coordenada do escudo
      muda (documento 15 §13.2)
- [ ] 1.2 Atualizar `RAZAO_DE_CONTORNO` em `comum/marca.test.ts` para `2/42` (colorida) e
      `3/42` (mono). Conferir que os casos de razão de contorno e de ápice contra a grade
      passam nas cinco peças — é o caso do ápice que fixa o teto de `3,28/42`
      (`design.md` — decisão 1)

## 2. A figura nova, nas duas peças do símbolo

- [ ] 2.1 Substituir o monograma `CG` pelo pássaro Sankofa em `simbolo.svg`, partindo do
      traçado da decisão 6 do `design.md` — **um `<path>` só**, com `fill-rule="evenodd"`,
      preenchimento em `tinta-900`. Conferir que cabe nos 3 KB do manifesto (projetado
      ~1.448 B), não traz `<text>`, filtro nem referência externa, e nenhuma cor fora da
      paleta (documento 15 §§3.2, 13.1; `README.md` §§1, 7)
- [ ] 2.2 Substituir o monograma em `simbolo-mono.svg` com a mesma geometria — em
      `currentColor`, sem declarar valor de cor algum. Conferir que olho, penas e vazados
      aparecem como **abertura** sobre o fundo escuro, e não como mancha
      (documento 15 §13.3; spec — "As contraformas da figura são vazadas, nunca pintadas")
- [ ] 2.3 Conferir à mão, a 16, 24 e 48 px nas duas versões, que a cabeça virada e o ovo se
      distinguem no tamanho do cabeçalho e que a 16 px a marca segue reconhecível pelo escudo
      e pela cor (spec — "O reconhecimento no tamanho mínimo é do escudo, não da figura")

## 3. A figura nova, nos três conjuntos

- [ ] 3.1 Levar a mesma figura a `marca-horizontal.svg`, `marca-horizontal-mono.svg` e
      `marca-empilhada.svg`, reposicionada por `transform` — **não redesenhada**, como o
      monograma já fazia. Conferir que os três seguem no orçamento de 10 KB e que a figura
      não encosta no contorno engrossado (`design.md` — decisão 7; `README.md` §1)
- [ ] 3.2 Conferir que o equilíbrio do conjunto com o logotipo não se perdeu: a figura é mais
      alta que o monograma, e o alinhamento vertical do texto ao lado do escudo pode precisar
      de ajuste (documento 15 §13.1)

## 4. O teste

- [ ] 4.1 Reescrever o caso `"%s mantém o monograma dentro do escudo"` para falar da
      **figura**, mantendo a mecânica — amostragem do escudo em polígono e cantos da caixa da
      figura dentro dele — e seguir rodando só em `simbolo.svg` e `simbolo-mono.svg`
      (`design.md` — decisão 5)
- [ ] 4.2 Acrescentar caso que recusa letra dentro do escudo e caso que confere a figura como
      **um `<path>` só** com `fill-rule="evenodd"` nas cinco peças — são os dois comportamentos
      que a spec acrescenta e que nenhum caso de hoje cobre (spec — "A figura dentro do escudo
      é o pássaro Sankofa", "As contraformas da figura são vazadas, nunca pintadas")

## 5. Documentação

- [ ] 5.1 Documento 15: §13.1 troca o monograma `CG` pela figura do Sankofa na linha do
      Símbolo; §13.2 troca a linha "Monograma" por "Figura" e registra as razões de contorno
      novas; §13.3 deixa de dizer "com o monograma cheio dentro". Conferir que §§13.4 e 13.5
      seguem corretos sem alteração e que o §8.3 não é tocado — o escudo continua sendo forma
      da marca e de mais nada
- [ ] 5.2 Documento 09 §1: **linha nova** em "Já decididos" para a figura e o contorno, pelo
      precedente da linha "Ponta no topo do escudo" — **não reescrever** a linha "Logotipo e
      marca gráfica" de 2026-10-02
- [ ] 5.3 `comum/marca/README.md`: §1 atualiza a descrição do símbolo; §8 registra a
      procedência — desenho produzido pelo projeto a partir de referência do fundador
      **medida, não traçada** — e declara que o que a marca reserva (documento 03 §1,
      princípio 4) é o desenho do projeto, não o símbolo Sankofa, patrimônio adinkra akan
- [ ] 5.4 `openspec/cronograma-de-fatias.md`: linha transversal nova no bloco
      "Infraestrutura transversal (sem PRD)", com `—` no número da fatia, o slug da change e a
      situação. `docs/prds/index.md` **não muda** — nenhum PRD mudou de situação; o documento
      99 **não muda** — nenhuma relação entre documentos mudou; a `nav` do `mkdocs.yml`
      **não muda** — nenhum arquivo novo em `docs/`
