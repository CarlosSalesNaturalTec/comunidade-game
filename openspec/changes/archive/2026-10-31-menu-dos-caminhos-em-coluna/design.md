# Design

## Context

Ver `proposal.md` — Why. O que o desenho precisa saber do estado atual:

- `apps/app-05-guerreiro/src/entrada/AreaDoGuerreiro.tsx` guarda o bloco aberto em estado, pinta
  `ListaDeCaminhos` e o conteúdo do bloco **na mesma tela**, e trata o encerramento por
  inatividade num efeito próprio, fora do bloco.
- `apps/app-01-aula-presencial/src/inicio/TelaInicial.tsx` já resolve exatamente a navegação que
  esta fatia quer: a tela inicial é o menu, e cada caminho **substitui a tela**, com
  `Cabecalho` cuja ação é Voltar. É padrão consolidado, não invenção desta fatia.
- `comum/react/ListaDeCaminhos.tsx` e `.cg-caminhos` em `comum/react/estilos.css` servem as duas
  aplicações desde a fatia 11.

## Goals / Non-Goals

**Goals:**

- A App 05 passa a navegar no mesmo idioma da App 01, sem introduzir idioma terceiro.
- A poda do `comum` sai junto com a fatia que a torna possível, e não como dívida.

**Non-Goals:**

- Roteador de URL. As duas aplicações navegam por estado, e esta fatia não abre essa discussão.
- Mexer no conteúdo ou na navegação interna de Trilha, Carteira, Desafios e Coleta.
- Mexer no `NavegacaoDeAreas`, que as Apps 03 e 09 usam e que continua marcando item corrente.

## Decisions

**1. A tela é escolhida por um estado `caminho`, com `"menu"` como valor inicial, e não por um
bloco que começa aberto.** O estado deixa de significar "qual aba está ativa" e passa a
significar "em que tela estou". `AreaDoGuerreiro` retorna cedo a tela do caminho quando há um, e
o menu quando não há — a forma da `TelaInicial` da App 01.
_Alternativa descartada:_ manter o bloco em estado e só esconder os caminhos — deixaria a tela
de conteúdo sem Voltar e o menu sem como ser o padrão.

**2. O Voltar é um único `definirCaminho("menu")`, e nenhum bloco recebe `aoVoltar`.** Volta-se
ao menu de qualquer profundidade porque o estado interno do bloco é desmontado junto com ele —
não há pilha a desempilhar. É o que a spec pede, e sai de graça.
_Alternativa descartada:_ propagar `aoVoltar` para dentro de cada bloco, o que daria "um passo
atrás" e exigiria tocar nos quatro blocos.

**3. O Sair é um item da mesma lista de caminhos, com `aoAcionar: sair` e glifo `encerrar`.**
Não é um componente à parte nem um cartão especial: a decisão do fundador é "igual aos demais".
_Alternativa descartada:_ o `fieldset` "Para quem opera o aparelho" da App 01 — ali o grupo
separa o adulto que opera o aparelho da criança atendida, e na App 05 quem sai é a própria
criança, então o agrupamento afirmaria uma distinção que não existe.

**4. A `ListaDeCaminhos` perde `rotulo`, e com ele o marco de navegação `<nav>`.** Com o menu
ocupando a tela sozinho, o marco não distingue nada — e o cartão de Sair é ação, não destino,
de modo que um `<nav>` em volta dele afirmaria errado. É o que o componente já faz pela App 01,
cujo comentário registra que "a tela inicial da App 01 é a tela inteira e não declara marco".

**5. O efeito de inatividade fica onde está, acima da escolha da tela, e o aviso é renderizado
nos dois ramos.** O efeito já vive no componente que decide a tela; só o JSX do aviso precisa
aparecer também na tela de conteúdo. Extraí-lo para um envoltório seria refatoração sem
requisito que a peça.

**6. A poda do `comum` entra nesta fatia, não depois.** `disposicao`/`DisposicaoDeCaminhos`,
`caminhoAtual` e o `aria-current` do cartão ficam com zero consumidores no instante em que a
App 05 muda — verificado: o único consumidor de ambos era a `AreaDoGuerreiro`. Saem com eles
`.cg-caminhos--grade`, as regras de grade do cartão, o `@media (min-width: 768px)` da grade e o
`.cg-caminho[aria-current]`.
_Alternativa descartada:_ deixar a grade declarada para uso futuro — decisão expressa do
fundador de tirar; código sem consumidor é dívida, e o documento 15 §6.5 encolhe junto.

## Risks / Trade-offs

**[A coleta do território e o Sair nascem abaixo da dobra]** → Trade-off aceito, não risco a
mitigar. Cinco cartões de `6` rem com os espaçamentos dão ~`576` px, e o celular modesto do
PRD-05 §10 — 360×640 — mostra ~500 px. O fundador foi avisado em `/opsx:explore` e decidiu
assim: agora os caminhos **são** a tela, rolar é o esperado, e o Sair longe do polegar protege
contra toque acidental de criança. Registrado aqui para não ser relido como defeito.

**[A criança perde um toque para chegar à missão]** → Mitigado pelo cartão da Trilha, que nomeia
a próxima missão e está em primeiro lugar: a tela diz o que fazer agora antes do toque. É o que
sustenta o `RF-05-08` reenunciado em vez de removido.

**[Os testes da fatia 11, de ontem, quebram em bloco]** → Esperado e desejável: eles afirmam o
comportamento que esta fatia reverte. `AreaDoGuerreiro.test.tsx` e os casos de grade e de
caminho corrente de `ListaDeCaminhos.test.tsx` são reescritos, não remendados.

**[O documento 09 §1 passa a ter duas linhas do mesmo dia dizendo o contrário]** → A linha da
fatia 11 é **corrigida** no mesmo PR, não deixada em pé ao lado da nova. É a regra de fonte
única do `CLAUDE.md`.
