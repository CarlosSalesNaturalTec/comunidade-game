# Tasks

Nenhuma tarefa de esteira: o ritmo de verificação de `CLAUDE.md` já diz o que roda e quando.
A change não toca `docs/` nem `.md` da raiz, então `npm run lint` e `mkdocs build --strict`
ficam de fora — rodam Biome e Vitest da App 06.

## 1. Moldura e cabeçalho da vitrine

- [x] 1.1 `src/layouts/Vitrine.astro`: pôr marca, cabeçalho e navegação de recortes dentro de
      um elemento `cg-moldura cg-moldura--leitura`, o mesmo respiro e a mesma largura do
      `<main>` (design — decisão 5; `RF-03-51`, documento 15 §4). Verificação: num visor de
      360 px nada encosta na borda e não há rolagem horizontal na abertura.
- [x] 1.2 `src/layouts/Vitrine.astro` e `src/componentes/CabecalhoDaVitrine.tsx`: a tela passa
      a declarar se tem herói, e o cabeçalho deixa de receber a ação "Entrar" quando tem
      (design — decisão 1; `RF-03-58`). Verificação: a abertura traz um só "Entrar" e as
      demais telas públicas seguem com o do cabeçalho.
- [x] 1.3 `src/componentes/CabecalhoDaVitrine.tsx`: subtítulo passa a "Boas-vindas! Tudo aqui
      é aberto — sem cadastro e sem login." e o `titulo` duplicado sai do cabeçalho da
      vitrine — o nome fica na `MarcaDoProjeto` (`RF-03-51`, `RN-03-01`). Verificação:
      "Comunidade Game" aparece uma vez só no topo e a promessa de sem cadastro e sem login
      segue na tela.
- [x] 1.4 `src/testes/TelaDaVitrine.tsx`: espelhar as mudanças de 1.2 e 1.3 na composição de
      teste, que repete a marcação do cabeçalho à mão. Verificação: `saidaDoBuild.test.ts`
      passa — é ele que guarda a composição contra desvio.

## 2. O par de ações no herói

- [x] 2.1 `src/abertura/Heroi.tsx`: montar "Quero participar" e "Entrar" como par lado a lado,
      com o "Entrar" abrindo o mesmo `DialogoDeEntrada`; a parte acionável vira ilha e a
      frase e a ilustração continuam no documento servido (design — decisões 1 e 2;
      `RF-03-58`, `RF-03-51`, `RN-03-21`). Verificação: os cenários "A abertura apresenta o
      herói antes das seções" e "O 'Entrar' do herói é o único da tela" do delta.
- [x] 2.2 `src/index.css`: classe do par e o modificador local do "Entrar" na família Marca —
      `--cor-marca`, `--cor-marca-contorno`, `--cor-sobre-marca`, sem token novo e sem
      valor primitivo (design — decisões 2 e 3; documento 15 §§3.2, 3.3, 5). Verificação:
      os dois botões têm a mesma altura, forma e peso, e cada um se identifica pelo rótulo.
- [x] 2.3 `src/testes/heroi.test.tsx`: o caso "não repete o Entrar" passa a afirmar que o
      "Entrar" é **um só na tela**, e entram os cenários do par de iguais e de que sem a
      ilustração as duas ações continuam acionáveis (`RF-03-58`, `RF-03-01`). Verificação:
      os quatro cenários novos do delta do herói passam.
- [x] 2.4 `src/testes/entrada.test.tsx`, `entradaSemEnderecoPublicado.test.tsx`,
      `formularioDeParticipacao.test.tsx` e `semRastro.test.tsx`: acertar o alcance do
      "Entrar", que na abertura passa a ser o do herói (`RF-03-58`, `RF-03-60`,
      `RN-03-22`). Verificação: o cenário "A pergunta é a mesma venha o botão de onde vier"
      do delta, e a suíte dos quatro arquivos passa.

## 3. Navegação dos recortes

- [x] 3.1 `src/navegacao/recortes.ts`: `RECORTES[0].rotulo` passa a "Início"; `chave`,
      `caminho` e o tipo `ChaveDeRecorte` não mudam (design — decisão 6; `RF-03-25`,
      `RF-03-26`). Verificação: a raiz segue no recorte *sociedade civil* e os outros dois
      seguem alcançáveis.
- [x] 3.2 `src/index.css`: `.cg-recortes` em uma linha, a `--escala-0875`, sem `flex-wrap`;
      `.cg-recortes__item` ganha `color` e `text-decoration` — é a ausência dos dois que
      produz o link cru do navegador. O corrente segue marcado por peso e filete, nunca só
      por cor, e o alvo de toque de 48 px vem do respiro (design — decisão 7; documento 15
      §§4, 5). Verificação: os três links cabem numa linha no visor de 360 px, o corrente é
      reconhecível sem cor e cada um cumpre o alvo de toque.
- [x] 3.3 `src/testes/abertura.test.tsx`, `avisoDeColeta.test.tsx` e
      `portfolioRankingEPoderes.test.tsx`: trocar as asserções por nome de "Sociedade civil"
      para "Início" (`RF-03-25`, `RF-03-26`). Verificação: a busca por `Sociedade civil` em
      `apps/app-06-vitrine/src/` sai vazia, e a suíte dos três arquivos passa.

## 4. Herói: frase menor, elenco maior

- [x] 4.1 `src/index.css`: `.cg-heroi__frase` desce um degrau da escala, para
      `--escala-1125`, mantendo `--fonte-destaque` (documento 15 §4; `RF-03-01`).
      Verificação: a frase continua acima do corpo mínimo de leitura e abaixo do herói.
- [x] 4.2 `src/index.css`: `.cg-heroi__elenco` sangra até a borda do visor —
      `width: 100vw` com `margin-inline: calc(50% - 50vw)` —, `gap` a zero e
      `overflow-x: clip` no herói para a sangria não vazar rolagem horizontal; a `clamp` de
      altura sobe conforme a conta do design (design — decisão 4; documento 15 §§1, 6).
      Verificação: no visor de 360 px o elenco passa de 96 px para cerca de 163 px de altura
      e não há rolagem horizontal.
- [x] 4.3 `src/testes/heroi.test.tsx`: caso que afirma a **ordem** das quatro figuras
      inalterada e a ausência de rolagem horizontal na abertura (`RF-03-01`). Verificação: o
      cenário "A composição põe o professor ao lado da criatura que ele indica" segue
      passando.

## 5. Fechamento

- [x] 5.1 Varredura final: `Sociedade civil` e `A vitrine pública do projeto` não aparecem
      mais em `apps/app-06-vitrine/src/`, e `comum/` não foi tocado — `git diff --stat` não
      lista arquivo fora de `apps/app-06-vitrine/` e `openspec/`.
- [x] 5.2 Documentação: acrescentar ao `openspec/cronograma-de-fatias.md`, no bloco do
      PRD-03, a linha `—` desta change com o slug e a situação. Nada mais muda — nenhuma
      regra de negócio nova foi decidida, então documento 09, documentos-fonte,
      `docs/prds/index.md`, documento 99 e `mkdocs.yml` ficam como estão.
