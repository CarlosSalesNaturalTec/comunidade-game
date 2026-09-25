# Design

## Context

Ver `proposal.md` — Why. As specs alteradas são `camada-visual-comum` (o contrato de
acessibilidade dos componentes comuns) e `aplicacao-da-aula-presencial` (as telas que declaram o
campo inicial).

O `Campo` de `comum/react/Campo.tsx` já gera o próprio identificador e amarra rótulo, erro e
estado inválido ao `<input>`. Nenhuma das seis aplicações declara foco inicial em campo algum
hoje. A fatia aplica um padrão consolidado — propriedade opcional num componente comum, usada por
uma aplicação — e por isso o desenho é curto.

## Goals / Non-Goals

**Goals:**

- O `Campo` aceita foco inicial como propriedade opcional.
- As sete telas de propósito único da App 01 o declaram.

**Non-Goals:**

- Declarar foco inicial nas outras cinco aplicações.
- Mudar campo, validação, rótulo, texto ou desfecho de tela alguma.
- Focar o segundo campo de qualquer tela.

## Decisions

1. **A propriedade entra no `Campo`, não num componente novo nem num `ref` exposto a quem
   chama.** O `Campo` já é o dono do `<input>` e do identificador dele; expor o elemento para a
   tela focá-la de fora quebraria esse encapsulamento e daria a cada tela a chance de focar
   diferente. _Descartado:_ devolver o `ref` do `<input>`.

2. **`autoFocus` do React, em vez de `useEffect` com `ref`.** O React chama `focus()` na montagem,
   e cada uma das sete telas monta o campo quando a tela abre — inclusive as duas formas da
   entrada, que são ramos distintos e montam elementos distintos. O `useEffect` faria o mesmo com
   mais código. _Descartado:_ `useEffect` com `ref` próprio — só seria necessário se a
   propriedade pudesse mudar de valor com o campo já montado, o que nenhuma das telas faz.

3. **Opt-in, e a omissão é o comportamento de hoje.** Ligar por padrão alcançaria de uma vez as
   seis aplicações e toda tela que já usa `Campo`, inclusive as telas densas da Operação, em que
   o campo quase nunca é o propósito da tela. Fora que o `RF-04-26` põe o aviso de coleta na tela
   inicial e o documento 15 §5 exige que o conteúdo seja alcançável: foco que pula conteúdo é
   regressão de acessibilidade, não conveniência.

4. **Um campo por tela, sempre o primeiro do ato.** Na confirmação, o nick vem antes do PIN
   porque é a criança que fala o nick e o adulto que digita o PIN depois — focar o PIN inverteria
   a ordem do ato descrito no `RF-04-21`.

## Risks / Trade-offs

- **O teclado do celular cobrindo o visor da câmera** → na entrada por nick e imagem o visor fica
  abaixo do campo, e o teclado aberto pode cobri-lo até quem opera recolhê-lo. É o custo aceito
  da decisão: o nick é digitado antes de a captura começar, e a captura só corre ao acionar
  Entrar. Fica registrado para ser reavaliado no aparelho do encontro.
- **Teste que passa sem provar nada** → afirmar o foco pelo elemento ativo do documento
  (`document.activeElement`), não pela presença do atributo, que passaria mesmo se o React não
  focasse.
