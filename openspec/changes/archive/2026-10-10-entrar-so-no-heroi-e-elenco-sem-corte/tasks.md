# Tasks

A change toca `docs/`, então `npm run lint` e `mkdocs build --strict` entram no ritmo de
verificação, além de Biome e Vitest da App 06. Nenhuma tarefa diz "rodar esteira": o
`CLAUDE.md` já define o que roda e quando.

## 1. A decisão desce pelo fluxo, antes do código

- [x] 1.1 `docs/03-plataforma-e-arquitetura.md` §8: "Botão **Entrar**, sempre visível" passa a
      situá-lo **na abertura, no herói**, mantendo intactos o encaminhamento das seis personas,
      o não autenticar, o não guardar a escolha e o não revelar quem existe. Verificação: a
      regra de origem do `RF-03-58` não diz mais "sempre visível".
- [x] 1.2 `docs/08-base-para-prds.md`: as duas menções ao "Entrar" acompanham a regra nova em
      **uma frase**, sem repetir a tabela nem a lista de destinos — o documento-fonte é o 03.
      Verificação: nenhuma das duas afirma que o botão está em toda tela.
- [x] 1.3 `docs/09-topicos-em-aberto-e-sugestoes.md` §1: linha nova em "Já decididos", com a
      decisão, a razão e o documento que ela alterou. Verificação: a linha nomeia o documento
      03 §8 e o `RF-03-58`.
- [x] 1.4 `docs/prds/prd-03-vitrine-publica.md`: o enunciado do `RF-03-58` e o passo 1 da
      jornada §5.9 passam a dizer que o botão é da abertura, e §5.9 ganha como se alcança a
      entrada de outra tela. Verificação: o PRD **aplica** a regra do documento 03, sem criar
      regra própria.

## 2. O "Entrar" passa a ser só do herói

- [x] 2.1 `src/componentes/CabecalhoDaVitrine.tsx`: perde o botão, o estado e o diálogo —
      sobra a saudação (`RF-03-58`). Verificação: o componente não importa mais
      `DialogoDeEntrada` nem `useState`.
- [x] 2.2 `src/layouts/Vitrine.astro`: o cabeçalho deixa de ser ilha (`client:load` sai) e a
      propriedade `comHeroi` sai junto, por não ter mais uso (`RF-03-51`, documento 15 §1,
      princípio 4). Verificação: nenhuma página passa `comHeroi`, e o cabeçalho sai no
      documento servido.
- [x] 2.3 `src/testes/TelaDaVitrine.tsx`: a composição acompanha — cabeçalho sem ação e sem
      diálogo no topo. Verificação: `saidaDoBuild.test.ts` passa, que é quem guarda a
      composição contra desvio.
- [x] 2.4 `src/testes/entrada.test.tsx`, `entradaSemEnderecoPublicado.test.tsx`,
      `formularioDeParticipacao.test.tsx` e `semRastro.test.tsx`: os casos que acionam o
      "Entrar" passam a alcançá-lo na abertura (`RF-03-58`, `RF-03-60`, `RN-03-22`).
      Verificação: os cenários "O botão está na abertura", "O botão pergunta antes de
      encaminhar" e "A pergunta apresenta as seis personas" do delta.
- [x] 2.5 `src/testes/saidaDoBuild.test.ts`: o guarda "as demais telas públicas seguem com o
      Entrar do cabeçalho" vira **"nenhuma tela além da abertura traz Entrar"**, e entra o
      caso da marca alcançável em toda tela (`RF-03-58`). Verificação: os cenários "Nenhuma
      outra tela pública traz o botão" e "A marca leva de volta à abertura" do delta.

## 3. O elenco inteiro em qualquer largura

- [x] 3.1 `src/index.css`: `.cg-heroi` ganha `container-type: inline-size`; as figuras passam
      a `height: 44cqw`; saem o `100vw`, a margem negativa, o `aspect-ratio` e o
      `overflow-x: clip` (design — decisão 1; `RF-03-01`, documento 15 §§1, 4, 6).
      Verificação: medido no Chromium em 320, 360, 412, 768 e 1280 px — nenhuma figura cortada
      e `scrollWidth` igual a `clientWidth` em todas.
- [x] 3.2 `src/testes/heroi.test.tsx`: caso que afirma que a altura das figuras é tirada da
      largura do herói e não do visor, e que nenhuma regra do elenco volta a depender de
      `100vw` ou de `overflow` (`RF-03-01`). Verificação: o cenário "As quatro figuras
      aparecem inteiras, em qualquer largura de tela" do delta.

## 4. Fechamento

- [x] 4.1 Varredura: nenhum arquivo fora de `apps/app-06-vitrine/`, `docs/` e `openspec/` no
      `git diff --stat`; `comum/` intacto.
- [x] 4.2 Documentação da change: linha `—` nova no `openspec/cronograma-de-fatias.md`, no
      bloco do PRD-03. `docs/prds/index.md` não muda — a situação do PRD-03 é a mesma —, e o
      documento 99 não muda, porque nenhuma relação entre documentos se altera.
