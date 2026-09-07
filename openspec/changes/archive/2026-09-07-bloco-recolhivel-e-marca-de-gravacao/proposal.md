## Why

Fatia **transversal, sem PRD** (`openspec/cronograma-de-fatias.md`, bloco *Infraestrutura
transversal*). Entra na capability `camada-visual-comum`, ancorada em **PRD-02 §10** e no
**documento 15 §§5, 6, 6.1 e 6.2**. Nenhum `RF`/`RN` novo: a fatia faz o código cumprir o que
o documento 15 acabou de decidir.

Duas decisões do fundador, de 2026-09-07 (documento 09 §1), nasceram do defeito relatado na
tela da trilha da Área do Mestre, e nenhuma tem componente que a sirva:

- **Nada recolhe.** `ListaDeMissoes.tsx` monta **dez blocos abertos por missão** — cadência de
  retomada, template por IA, recompensa de marco, desafio de desbloqueio, desafios de coleta,
  etiquetas ODS, atividades, conteúdo, bibliografia e pré-visualização —, repetidos num `map`
  sobre as missões. Trilha de seis missões é uma página de mais de sessenta blocos, sem
  hierarquia entre o esqueleto da missão e o detalhe opcional. O documento 15 §6 dimensiona a
  Operação pelo **uso raro, que precisa ser entendido sem aprendizado acumulado** — escrever
  trilha é o uso mais raro que o Mestre faz.
- **Nada confirma que gravou.** São **onze escritas** na tela da trilha que gravam sozinhas,
  cada uma com seu próprio botão e sua própria rota — cadência, ODS da trilha, ODS da missão,
  recompensa, desbloqueio, culminância, missão, coleta, conteúdo, bibliografia e atividade —,
  e **nenhuma** delas diz ao Mestre que chegou ao servidor. O PRD-09 §10 exige rascunho salvo
  automaticamente; a implementação cumpre a letra e não dá ao Mestre como confiar no que não vê.

`comum/react` exporta dez símbolos e **nenhum** é bloco recolhível ou marca de gravação.

## What Changes

- **`comum/react` ganha `BlocoRecolhivel`** (documento 15 §6.1): bloco que **nasce fechado**,
  com o **resumo do estado** na linha fechada, controle em botão com rótulo textual e
  `aria-expanded`, sem animação de altura. O resumo é dado por quem monta o bloco — o
  componente não conhece o domínio.
- **`comum/react` ganha `MarcaDeGravacao`** (documento 15 §6.2): texto persistente que declara
  a gravação no próprio bloco que gravou e fica até a escrita seguinte, sem depender de cor,
  sem movimento e sem sumir por tempo. Bloco que não gravou nada não recebe marca.
- **`comum/react/estilos.css` recebe os estilos dos dois**, na camada semântica e de tema dos
  tokens, como os demais componentes.
- **A tela da trilha da Área do Mestre adota os dois** — é a adoção que prova que servem, como
  a tabela de direitos provou a `Tabela` na fatia anterior. Os dez blocos por missão passam a
  recolher, e as onze escritas passam a declarar que gravaram.
- **O tópico do template da missão ganha a nota de que não é guardado.** O campo "O que você
  quer ensinar nesta missão?" vive em estado local, viaja no pedido da sugestão e é descartado;
  nada é gravado sem o Mestre aceitar (`RN-09-33`). A tela passa a dizê-lo, em uma linha.

**Fora do escopo:** a **paginação da trilha pelas etapas do ciclo** (`RF-09-03`) e o **painel
permanente das travas de publicação** (`RF-09-06`, `RF-09-07`), que são a fatia 17 do PRD-09 e
dependem desta; as Apps 01, 03, 04, 05, 06, 07 e 08, que adotarão os dois componentes quando a
tela delas pedir; o temperamento Arena, que o documento 15 §6.1 exclui por ter densidade baixa;
e qualquer critério de completude da missão, que documento nenhum define.

## Capabilities

### New Capabilities

Nenhuma.

### Modified Capabilities

- `camada-visual-comum`: dois requisitos novos — o bloco recolhível das telas da Operação
  (documento 15 §6.1) e a marca de gravação das escritas que gravam sozinhas (documento 15
  §6.2). Nenhum requisito existente muda.

## Impact

- `comum/react/`: dois componentes novos, `estilos.css` e o `indice.ts` que os exporta.
- `apps/app-09-mestre/src/trilhas/`: `TelaDaTrilha.tsx`, `ListaDeMissoes.tsx` e os componentes
  de bloco que ela monta passam a recolher e a declarar a gravação; `TemplateDaMissao.tsx`
  ganha a nota do tópico descartável.
- Testes: `comum/react/` ganha os testes dos dois componentes; `trilhas.test.tsx` acompanha o
  que a tela passa a apresentar.
- Sem rota nova, sem campo novo no núcleo e sem migração — a fatia é de camada visual.
