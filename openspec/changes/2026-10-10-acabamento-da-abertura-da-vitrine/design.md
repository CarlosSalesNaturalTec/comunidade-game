# Design

## Context

Ver `proposal.md` — Why. O que o desenho precisa levar em conta, e que não está lá:

- **O cabeçalho é de `comum/`.** `comum/react/Cabecalho.tsx` serve as **oito aplicações** e
  monta `<h1>{titulo}</h1>`, o subtítulo e, quando recebe `acao`, um `Botao` secundário. Nada
  do que esta change decide pode entrar nele.
- **A App 06 é Astro com ilhas.** `Heroi.tsx` é componente React **sem diretiva de cliente**:
  sai no documento servido e não custa JS. `CabecalhoDaVitrine.tsx` é ilha (`client:load`)
  porque guarda o estado do diálogo de entrada.
- **A composição de teste espelha a marcação à mão.** `src/testes/TelaDaVitrine.tsx` repete o
  `Cabecalho` da vitrine porque prop de função não atravessa a fronteira do Astro (achado da
  fatia 9). `saidaDoBuild.test.ts` a guarda contra desvio — as duas andam juntas, sempre.
- **Os tokens já cobrem tudo.** `--cor-marca`, `--cor-marca-contorno` e `--cor-sobre-marca`
  existem em `comum/tokens.css` desde o começo e nunca foram usados. A escala tipográfica e a
  de espaçamento do documento 15 §4 cobrem os tamanhos novos. Nenhum valor primitivo entra.

## Goals / Non-Goals

**Goals:**

- A abertura cabe no visor de um celular de 360 px sem nada encostando no corte.
- "Entrar" e "Quero participar" se leem como um par de iguais, e o "Entrar" continua sendo um
  só por tela.
- A navegação de recortes sai do padrão de link cru do navegador, em uma linha, sem perder o
  alvo de toque nem a marcação do corrente por peso e filete.

**Non-Goals:**

- Mexer em `comum/` — nem no `Cabecalho`, nem no `Botao`, nem nos tokens.
- Renomear o recorte *sociedade civil* no domínio. Troca-se o **rótulo**, não o conceito.
- Mudar a ordem das quatro figuras do elenco, travada pela spec de 2026-10-10.
- Arrumar o respiro da faixa de topo das outras sete aplicações. O mesmo padrão existe lá
  (`MarcaDoProjeto` fora da `cg-moldura` em `main.tsx`), mas elas estão fora desta fatia.

## Decisions

### 1. O "Entrar" migra por propriedade do layout, não por detecção de rota

`Vitrine.astro` ganha uma propriedade — a tela declara se tem herói — e deixa de passar
`acao` ao `CabecalhoDaVitrine` quando tem. O herói monta o seu próprio "Entrar", com o
mesmo `DialogoDeEntrada`.

Descartado: o herói inspecionar o caminho corrente para decidir. Repetiria a lógica de rota
em dois lugares e a fatia 9 já mostrou o preço disso.

Descartado: o `CabecalhoDaVitrine` renderizar o herói. Inverteria a composição e tornaria
ilha o que hoje sai no documento servido.

**Consequência:** o diálogo de entrada passa a ser montado pelo herói na abertura. Como o
herói não tem diretiva de cliente e o diálogo tem estado, **a parte acionável vira ilha** —
o par de ações, não o herói inteiro. A frase e a ilustração continuam saindo no documento
servido, que é o que o `RF-03-51` e o `RN-03-21` cobram.

### 2. O par é do herói, com classe própria da App 06

O par recebe classe própria em `src/index.css` e consome `cg-botao` para a forma. O "Entrar"
ganha um modificador local — não uma variante nova de `comum/react/Botao.tsx`.

Descartado: criar `cg-botao--marca` em `comum/react/estilos.css`. Ofereceria às outras sete
aplicações uma variante que nenhuma decisão pediu.

### 3. O laranja da marca pinta uma ação — leitura nova da paleta

O documento 15 §3.2 batiza a família azul de **Ação** e a laranja de **Marca**, e **não diz**
se uma ação pode ser pintada de laranja. **Decisão do fundador de 2026-10-10:** pode, para
este par, porque é o que distingue as duas ações sem apequenar nenhuma. Fica registrado aqui
como leitura nova, e não como regra: nenhuma outra tela ganha ação laranja por isto.

O contraste não é inventado: `cal-000` sobre `marca-600` mede **4,76:1**, acima do piso de
4,5:1, e já está na tabela do documento 15 §3.3. O contorno sai em `marca-700`, como o azul
sai em `acao-700` — é a regra de preenchimento com contorno do §3.2.

A cor **não é sinal único**: cada botão carrega o próprio rótulo, e o documento 15 §5 fica
cumprido.

### 4. A sangria do elenco é aritmética, não gosto

As quatro figuras somam `578 + 764 + 551 + 361 = 2254` px de largura para `1024` px de
altura. A fileira é, portanto, **2,2× mais larga do que alta**, e a altura dela num visor de
largura `L` é no máximo `(L − respiro − vãos) ÷ 2,2`:

| Situação | Largura útil (visor de 360 px) | Altura possível |
| --- | --- | --- |
| Hoje — dentro da moldura, vãos de 8 px | 328 − 24 = 304 px | 96 px (`clamp` corta antes) |
| Dentro da moldura, sem vãos | 328 px | ~148 px |
| **Sangrando até a borda, sem vãos** | **360 px** | **~163 px** |

A sangria sai por `width: 100vw` com `margin-inline: calc(50% - 50vw)`, que tira o elenco do
respiro da `.cg-vitrine` sem mexer na moldura. O `gap` vai a zero: as figuras encostam, o que
a composição agradece — o professor fica de fato ao lado da criatura que a mão dele indica.

No aparelho largo a `clamp` corta pelo teto, e a fileira para de crescer muito antes de a
coluna de leitura acabar. Nenhuma imagem nova, nenhum byte a mais: o piso de rede do
documento 15 §1, princípio 4, não é afrouxado.

### 5. A faixa de topo entra na moldura reaproveitando as classes que já existem

Marca, cabeçalho e navegação passam a ficar dentro de um elemento com
`cg-moldura cg-moldura--leitura`, as mesmas classes do `<main>`. Nenhuma classe nova, nenhum
valor novo — é o respiro que o `<main>` já tinha, estendido a quem estava fora dele.

Descartado: dar `padding` à `.cg-recortes` e ao `.cg-cabecalho`. Resolveria por fora e
deixaria a marca sem respiro, além de duplicar um valor que a moldura já define.

### 6. O rótulo "Início" mora em `recortes.ts`, a chave não muda

`RECORTES[0].rotulo` passa a `"Início"`. `chave` segue `"sociedade-civil"`, `caminho` segue
`"/"`, e o tipo `ChaveDeRecorte` não é tocado. O `<nav>` mantém `aria-label="Recortes de
leitura"`, que é o que dá o enquadramento a quem usa leitor de tela.

### 7. A navegação perde o link cru, mantém o alvo de toque

`.cg-recortes__item` ganha `color` e `text-decoration: none` — a ausência dos dois é a causa
do roxo sublinhado. Inativos em `--cor-texto-secundario`, corrente em `--cor-texto` com peso
de rótulo e filete inferior. `flex-wrap` sai: os três ficam em uma linha, a
`--escala-0875`.

O alvo de toque de 48 px vem do **respiro vertical**, não do corpo da fonte — o `min-height`
continua em `--alvo-de-toque` e a faixa clicável é a altura inteira, com a fonte pequena
dentro dela. A separação de 8 px entre vizinhos é a que a `.cg-recortes` já declara.

A conta de largura fecha: "Início · Pesquisadores · Gestores públicos" são 36 caracteres, que
a `--escala-0875` põe em cerca de 260 px, mais separadores — dentro dos 328 px úteis de um
visor de 360 px.

## Risks / Trade-offs

- **A ilha cresce de uma para duas no caminho da abertura** → o par de ações é ilha, o herói
  não. A ilustração e a frase continuam no documento servido, e o `saidaDoBuild.test.ts` é
  quem confirma isso: se o herói virar ilha inteiro, o teste acusa.
- **A sangria do elenco pode vazar barra de rolagem horizontal** → `width: 100vw` conta a
  barra de rolagem em alguns navegadores de mesa. Mitigação: `overflow-x: clip` no contêiner
  do herói, e caso de teste que afirma a ausência de rolagem horizontal na abertura.
- **"Início · Pesquisadores · Gestores públicos" pode estourar num visor mais estreito que
  360 px** → o `flex-wrap` sai, mas o `min-width: 0` e o respiro menor dão a folga; abaixo
  disso a linha comprime antes de cortar. Caso de teste no visor mais estreito que o projeto
  atende.
- **O laranja abre precedente** → mitigado por escrito na decisão 3: vale para este par, e
  qualquer outra ação laranja é decisão nova do fundador.
- **Oito arquivos de teste mudam de uma vez** → risco de um deles ficar afirmando o texto
  velho e passar por acidente. Mitigação: a busca por `"Sociedade civil"` e pelo subtítulo
  antigo tem de sair vazia na árvore ao fechar as tarefas.

## Open Questions

Nenhuma. As oito decisões do fundador de 2026-10-10 cobrem o recorte inteiro.
