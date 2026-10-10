# Tasks

> **O grupo 1 vem primeiro, e não é formalidade.** A hierarquia de autoridade manda a decisão
> nova descer ao documento-fonte antes do código: enquanto o documento 15 §13.6 disser "um
> arquivo por personagem em pose neutra", os arquivos do grupo 2 contrariam a regra vigente.
>
> As quatro decisões do fundador são de **2026-10-10** e estão na `proposal.md`. As medidas
> da leva anterior — keyline `#f7f5f0` a ≈ 3 px, grade de 1024, teto de 120 KB — estão no
> `design.md`, já medidas: não as reestime.

## 1. A decisão desce aos documentos-fonte

- [ ] 1.1 Documento 15 §13.6: gravar as **duas faixas etárias** de Susy e Otávio (o elenco
      segue sendo quatro personagens, e Trenell e Robô Educa não ganham variante), o
      **adereço que caracteriza** admitido na pose, e a **composição do herói** — alunos nas
      extremidades, professor ao lado da criatura que ele indica. Verificar que o resto da
      regra não afrouxou (contorno, preenchimento, fundo, keyline) e que a numeração do
      documento segue contínua
- [ ] 1.2 Documento 09: registrar as decisões de 2026-10-10 em "Já decididos" e **estreitar**
      a linha "Roteiro e narrativa do elenco" — ela não fecha, porque o roteiro e o
      personagem dos Rôbróders seguem pendentes. Conferir o documento 99: a linha "Elenco de
      personagens: composição, cor, contorno e keyline" já aponta o §13.6 como fonte, então
      só se mexe nela se a relação entre documentos mudar — verificar e, não mudando, não
      tocar

## 2. O elenco no repositório

- [ ] 2.1 `git mv` dos quatro arquivos de hoje para `susy-crianca.{avif,webp}` e
      `otavio-crianca.{avif,webp}`, **antes** de gravar qualquer arquivo novo. Verificar com
      `git status` que o Git registrou **rename**, e não remoção mais adição — conteúdo
      inalterado é o que preserva o histórico (documento 15 §13.6)
- [ ] 2.2 Produzir `susy.{avif,webp}` e `otavio.{avif,webp}` adolescentes pelo pipeline do
      `design.md` (recorte do magenta por distância de cor na faixa de borda, 3% de margem,
      1024 px de lado maior, keyline `#f7f5f0` a 3 px). Verificar cada arquivo contra o
      manifesto do `README.md` §3 — par completo, grade, teto de 120 KB — e **as seis figuras
      humanas lado a lado**, para o filete e o traço da leva nova casarem com os de
      2026-10-09 (documento 15 §13.6)
- [ ] 2.3 `comum/marca/README.md`: §3 passa a prever **variante por faixa etária** além de
      expressão, com a tabela refletindo os doze arquivos e a nota de que só o que se
      apresenta é provisionado; §8 recebe a procedência da leva de 2026-10-10 — Nano Banana
      sob direção do fundador, sem autor externo, titularidade da pessoa jurídica — e **o que
      mudou da origem para o arquivo**, como o §6 manda (documento 15 §13.6)
- [ ] 2.4 Caso novo em `comum/marca.test.ts` conferindo cada arquivo de `elenco/` contra o
      manifesto, por leitura de cabeçalho e sem dependência nova: par AVIF/WebP completo,
      dimensões iguais entre o par, 1024 px de lado maior, canal alfa declarado (`VP8X` no
      WebP, `auxC` no AVIF) e peso dentro do teto. Verificar que os doze arquivos passam, e
      que o teste falha se um par ficar incompleto. Cobre os cenários "O par de formatos está
      completo" e "Grade e peso cabem no manifesto" de `camada-visual-comum`

## 3. A composição do herói

- [ ] 3.1 `comum/marca/provisionamento.ts`: confirmar que `ELENCO` segue com os quatro nomes
      base e que os pares `-crianca` **não** são copiados. Verificar que o `public/` da App 06
      recebe oito arquivos, e nenhum `-crianca`. Cobre o cenário "A variante guardada não vai
      ao ar" de `camada-visual-comum` (`RF-03-51`)
- [ ] 3.2 `apps/app-06-vitrine/src/abertura/Heroi.tsx`: a ordem passa a
      `susy, robo-educa, trenell, otavio`, as larguras acompanham os arquivos de verdade
      (medir, não copiar do `design.md`), e o `aria-label` do grupo nomeia as quatro na mesma
      ordem visual. Verificar na saída do build que a sequência é essa (`RF-03-01`)
- [ ] 3.3 `apps/app-06-vitrine/src/index.css`: trocar o comentário "do mais novo ao mais
      velho", que deixou de valer, pela razão da composição — alunos nas extremidades,
      professor ao lado da criatura que a mão dele indica, e a dependência de o Trenell ficar
      vizinho ao Robô Educa. Verificar que nada do layout mudou junto: a regra de altura e o
      comportamento no celular seguem como estão (`RF-03-01`)
- [ ] 3.4 Testes da vitrine: atualizar a sequência literal do `srcset` em
      `saidaDoBuild.test.ts` (é ela que trava a ordem) e cobrir em `heroi.test.tsx` os dois
      cenários novos do delta de `aplicacao-da-vitrine` — a composição com o professor
      vizinho à criatura, e o rótulo único nomeando as quatro na ordem em que aparecem.
      Verificar que os casos existentes seguem passando sem reescrita (`RF-03-01`,
      `RF-03-51`)

## 4. Fechamento

- [ ] 4.1 `openspec/cronograma-de-fatias.md`: linha **sem número** no bloco do PRD-03, com o
      slug desta change e a situação `implementado`, no formato da correção de 2026-10-09.
      `docs/prds/index.md` **não muda** — o PRD-03 já está implementado; nenhum arquivo nasce
      em `docs/`, então a `nav` do `mkdocs.yml` também não muda. Verificar que as três coisas
      são verdade antes de fechar
