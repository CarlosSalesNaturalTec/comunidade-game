# Design

## Context

Ver `proposal.md` — Why. O padrão já está consolidado: a fatia 25 criou o grupo de quem
opera como um `fieldset` com `legend`, cujos itens são cartões `cg-caminho` iguais aos
caminhos, e a `legend` é que carrega a linha do separador (`border-top`). Esta fatia apenas
**move um cartão para dentro desse grupo** e reordena a lista — nenhum padrão novo.

O estado de navegação não muda: `caminho === "medicao"` e o `PedidoDePinDoAparelho` que o
guarda continuam exatamente como estão. Muda **onde o botão que define esse estado mora**.

## Goals / Non-Goals

**Goals:**

- A ordem do delta de spec passa a ser a ordem do JSX, e fica coberta por teste.
- O cartão da medição passa a ser filho do `fieldset`, depois da `legend`.

**Non-Goals:**

- Nenhuma mudança de comportamento, rótulo, glifo, guarda de PIN ou papel.
- Não transformar a lista em estrutura de dados iterada — ver Decisions.

## Decisions

**1. A ordem continua literal no JSX, não vira tabela iterada.**
Tentador, mas é refatoração fora da fatia: os itens têm condições heterogêneas
(`momentoDeTrocaAberto`, `podeAbrirMomentoDeTroca`), um deles tem rótulo que alterna em três
estados, e os dois do grupo não navegam — chamam `aoAbrirMomentoDeTroca` e
`definirCaminho("encerramento")`. A fatia 25 deixou a lista literal de propósito. *Alternativa
descartada:* array de objetos com `map`, que ganharia a ordem declarada num só lugar e perderia
a legibilidade das condições.

**2. A medição entra como primeiro cartão do grupo, mas a `legend` continua sendo o primeiro
filho do `fieldset`.**
A `legend` é `float: left` com `inline-size: 100%` e o `border-top` que desenha o separador: um
cartão antes dela joga a linha para o meio do grupo. A ordem dentro do `fieldset` é
`legend` → medição → chave da troca → encerramento.

**3. A medição antes da chave do momento de troca.**
Decisão do fundador: calibração é ato de preparo, raríssimo; a chave é do encontro em curso. Tem
consequência técnica favorável — os dois testes que asseguram a cauda por índice
(`cartoes[length - 2]` é a chave, `cartoes[length - 1]` é o encerramento) seguem válidos **sem
edição**, e passam a ser conferidos, não reescritos. *Alternativa descartada:* a medição por
último antes do encerramento, que obrigaria a reescrever os dois.

**4. O requirement da bancada não entra no delta.**
O cenário "A bancada não abre sem o PIN" diz "alguém escolhe o caminho da medição **na tela
inicial**" — continua verdadeiro: a medição segue alcançável da tela inicial, só que de dentro
do grupo. Nada ali fixa posição, então não há o que modificar. Registrado para que o
`/opsx:verify` não o leia como omissão.

**5. A ordem passa a ter teste próprio.**
O teste "cada caminho leva glifo ao lado do rótulo" lista os sete rótulos e **itera** sem asserir
ordem — a ordem nunca esteve protegida. O teste novo assere a sequência de `.cg-caminho` com o
momento de troca aberto, que é o único estado em que os seis caminhos aparecem juntos.

## Risks / Trade-offs

- **A linha do separador sobe para o meio do grupo** se a medição for inserida antes da `legend`
  → ordem fixada na decisão 2; o teste da `legend` já existente (`role="group"` nomeado) não
  pegaria isso, então a conferência é visual, no `/opsx:apply`.
- **Teste de ordem que engessa a lista** — cada fatia que acrescentar caminho passa a ter de
  atualizá-lo → é o custo aceito: a spec agora fixa a ordem, e teste que a confere é o que a
  torna verificável. O teste é um só, e a mensagem de falha mostra a lista inteira.
- **A medição é o único cartão do grupo visível a todo papel**, ao lado de uma chave que é só do
  Mestre → assimetria conhecida, mantida por decisão do fundador de 2026-10-15; a guarda dela é
  o PIN do aparelho (`RN-04-41`), não o papel. Não é pendência desta fatia.
