# Design

## Context

Ver `proposal.md` — Why. O que o desenho precisa levar em conta:

- `comum/narracao/ProvedorDeNarracao.tsx` guarda três sinais no contexto: `ligada` (escolha,
  hoje lida de `localStorage`), `armada` (o gesto já aconteceu) e `disponivel` (o navegador
  oferece síntese). `narrar` exige os três; `ouvir` exige `ligada` e marca `armada`.
- Sem provedor montado, `useNarracao` devolve `INERTE`, com todos os sinais em `false`. É o que
  mantém inalteradas as sete aplicações que ainda não receberam a camada — só a App 01 monta o
  provedor. Qualquer guarda nova precisa continuar fechada no inerte.
- `comum/react/Botao.tsx` sempre exigiu `children` textual, e `comum/react/Icone.tsx` é
  `aria-hidden` por desenho, sem onde pôr rótulo: "quem o usa é dono do rótulo".
- `comum/react/Cabecalho.tsx` tem um slot de ação só (`acao`), usado por cerca de vinte telas
  das oito aplicações.
- `cg-caminho` já existe com alvo de toque de 6 rem, glifo que não encolhe e estado
  `:disabled`.

## Goals / Non-Goals

**Goals**

- Um controle de som só na App 01, de glifo, no canto do cabeçalho da tela inicial.
- Apagar o estado "ligada e muda" da camada, não escondê-lo: `armada` sai da interface.
- As duas ações de operação no mesmo padrão dos caminhos, sem perder o PIN nem a restrição de
  papel que cada uma já tinha.

**Non-Goals**

- Mexer no que a camada fala, em qual voz escolhe, ou no recorte de dado que admite (só o
  nick) — nada disso muda.
- Levar o alternador às demais telas da App 01 ou às outras sete aplicações.
- Mudar a aparência do `cg-caminho`: o separador agrupa, o cartão fica idêntico.

## Decisions

### 1. `armada` sai do contexto, e não vira detalhe interno

Com o arranque desligado e sem persistência, não existe caminho que chegue a "ligada sem gesto":
o único jeito de `ligada` ficar `true` é alguém clicar, e o clique é o gesto. Então `armada` e
`armarNarracao` saem de `ContextoDeNarracaoValor` e de `INERTE`, e `armar()` é chamado dentro do
`alternarNarracao` que liga. `narrar` passa a exigir `ligada && voz`.

Descartado guardar `armada` como estado interno "por segurança": sinal que nenhum caminho põe em
`false` é sinal morto, e sinal morto engana quem lê o código depois.

### 2. A escolha não é gravada em lugar algum

`lerEscolhaDoAparelho`, `gravarEscolhaDoAparelho` e `CHAVE_DA_NARRACAO_NO_APARELHO` saem.
`useState(false)` basta, e com isso cai também o `try/catch` que existia porque aba privativa
faz `localStorage` lançar.

Descartado `sessionStorage`: sobreviveria à recarga e recriaria exatamente o estado que esta
change existe para apagar. Descartado manter `localStorage` só para desligado: gravar metade da
escolha é mais difícil de explicar do que não gravar nenhuma.

### 3. `ouvir` deixa de olhar `ligada`; a guarda do controle passa a `disponivel`

Em `ProvedorDeNarracao`, `ouvir` troca `if (!ligada || !voz) return` por `if (!voz) return`. Em
`comum/trilha/Missao.tsx`, `ControleDeOuvirOConteudo` troca `if (!ligada) return null` por
`if (!disponivel) return null`.

A troca de guarda é o ponto a não errar: `ligada` era `false` no `INERTE`, e é isso que esconde
o botão nas aplicações sem provedor. `disponivel` também é `false` no `INERTE`, então a App 05 —
que usa `comum/trilha` e não monta o provedor — segue sem o botão, como hoje. Trocar por
`true` fixo, ou remover a guarda, acenderia o botão lá.

### 4. Botão de alternância só de ícone, novo em `comum/react`

Nasce `BotaoDeAlternancia` em `comum/react`, com `rotulo` **obrigatório** (vai para
`aria-label`), `glifo` por estado e `ligado` que alimenta `aria-pressed`. Reaproveita a classe
`cg-botao` pelo alvo de toque e pelo foco, com um modificador para a caixa quadrada do ícone.

Descartado dar um `rotuloAcessivel` opcional ao `Botao` existente: opcional é o que se esquece,
e o requisito do ícone da camada não admite botão sem rótulo. Descartado dar rótulo ao `Icone`:
ele é decorativo nas outras duas dúzias de usos, e furar isso espalharia `aria-label` duplicado
pelo lado do texto que o acompanha.

### 5. O `Cabecalho` ganha um slot, e quem passa o alternador é a tela

`Cabecalho` recebe um slot novo ao lado de `acao` — opcional, para o controle que fica no canto.
A App 01 passa o alternador nele **só na tela inicial**; as outras vinte telas que montam
`Cabecalho` não passam nada e ficam como estão.

Descartado montar o alternador dentro do próprio `Cabecalho` a partir de `useNarracao`: ele
apareceria nas vinte telas de uma vez, e o documento 15 §5.1 o quer na tela inicial. Descartado
a tela inicial montar um cabeçalho próprio: duplicaria o `h1`, o subtítulo e a narração do
título que o `Cabecalho` já declara.

### 6. Os dois cartões de operação, e por que o separador basta

Os dois entram na lista `cg-caminhos`, com o separador entre eles e os caminhos: um título de
grupo, com o cartão idêntico ao dos caminhos — foi o que o fundador pediu. O risco de misturar
a linguagem visual de quem opera com a da criança está em Risks, e o que o contém é o PIN que o
encerramento já exige (`RF-04-71`, `RN-04-41`), intocado por esta change.

O cartão da chave da troca é um **alternador**, não navegação como os demais `cg-caminho`. O que
o distingue é o glifo próprio e o rótulo, que diz o ato ("Abrir"/"Fechar") em vez de nomear um
destino — e o separador, que já o tirou do meio dos caminhos. Não ganha `aria-pressed`: o
rótulo muda e diz o estado por escrito, que é o que a camada pede.

### 7. "Abrindo…" e o erro da abertura da troca

O "Abrindo…" fica no próprio cartão, com `cg-caminho:disabled`, que já existe. O `Aviso
tipo="erro"` vai **abaixo da lista**, não entre os cartões: `cg-caminhos` é uma coluna de alvos
de toque, e um bloco vermelho no meio dela empurra o cartão seguinte para debaixo do dedo que
já estava indo. Abaixo da lista o aviso continua anunciado por `role="alert"`, que é o que leva
a falha a quem não está olhando para aquele ponto da tela.

### 8. Os quatro glifos

Entram na união `NomeDeGlifo` de `comum/react/Icone.tsx`, na grade de 24 px e com traço de 2 px
de `currentColor`, como os demais: `som` (alto-falante com ondas), `som-desligado`
(alto-falante com corte), `encerrar` (porta com flecha) e `momento-de-troca` (a chave do
momento, desenho distinto do `troca` do caminho). `Icone.test.tsx` lista os glifos à mão e
cresce junto.

## Risks / Trade-offs

- **O cartão de encerrar fica com o mesmo peso visual dos caminhos da criança** → O PIN de quem
  abriu o aparelho continua exigido no ato, e o separador "Para quem opera o aparelho" marca a
  fronteira. Foi o que o fundador pediu, vista a alternativa.
- **A narração nasce desligada, e quem precisa dela pode não achar um botão sem texto** → O
  controle de ouvir o texto longo deixa de depender do alternador (decisão 3), que é por onde a
  leitura alcança quem não lê; e o piso de acessibilidade do documento 15 §5 segue cumprido com
  a narração desligada, por leitor de tela.
- **Recarregar a aba apaga a escolha de som** → Aceito: a sessão de trabalho sobrevive à recarga
  e a aba fica aberta o encontro todo, então o custo é um toque esporádico. Em troca, o estado
  "ligado e mudo" deixa de existir.
- **Os dois cartões de troca encostados confundem com o momento aberto** → Glifo próprio para a
  chave, rótulo que diz o ato e não o destino, e o separador entre eles.
- **Trocar a guarda do controle de ouvir pode acender o botão na App 05** → A guarda vira
  `disponivel`, que é `false` no `INERTE`; há teste em `comum/trilha/trilha.test.tsx` cobrindo a
  camada inerte, e ele passa a cobrir este caminho.

## Migration Plan

Nada a migrar: a narração não tem dado no núcleo, e a chave `cg:narracao` que fica órfã no
`localStorage` dos aparelhos em uso é lixo inerte — ninguém mais a lê, e não vale um passo de
limpeza. Reverter é reverter o PR.
