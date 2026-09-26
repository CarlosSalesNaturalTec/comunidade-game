# Design

## Context

Ver `proposal.md` — Why. O que molda a abordagem:

- As três telas de trilha vivem em `comum/trilha/`, promovidas na fatia 21 do PRD-04, e são
  consumidas pela App 01 e pela App 05. Não há como mexer numa aplicação só.
- O `BlocoRecolhivel` de `comum/react` já existe e já nasce fechado. Ele exige **título** e
  **resumo**, e o resumo fica visível com o bloco fechado — recolher, aqui, nunca esconde tudo.
- A tela da programação do encontro (`TelaDaProgramacao.tsx`, App 01) renderiza os conteúdos
  em código próprio, sem passar por `comum/trilha`. São dois paginadores a construir, não um.
- O `DesafioDeDesbloqueio` guarda as escolhas num `Record<string, number>` local e só submete
  no fim. A paginação não muda isso: muda o que a tela mostra, não quando ela envia.

## Goals / Non-Goals

**Goals:**

- Um único componente de paginação, usado pelos três lugares que percorrem sequência.
- A submissão do desafio segue idêntica: um envio, com todas as respostas.
- Nenhuma informação que um requisito manda apresentar deixa de existir na tela.

**Non-Goals:**

- Guardar a posição da sequência entre sessões. Quem sai e volta recomeça do primeiro item:
  nenhum requisito pede retomada, e inventá-la criaria estado que ninguém mandou existir.
- Paginar o Quiz ao Vivo, cujo ritmo é do Mestre.
- Mudar o `BlocoRecolhivel` no que a Operação já usa.

## Decisions

### 1. Um componente de paginação em `comum/react`, não três laços

O paginador entra na camada comum, ao lado do `BlocoRecolhivel`, e recebe os itens e o que
renderizar para cada um. Os três consumidores — conteúdo da missão, perguntas do desafio,
conteúdo do dia da equipe — passam a usá-lo.

Alternativa descartada: um `useState` de índice em cada tela. Daria três implementações do
mesmo "onde estou na sequência", três rótulos de avançar diferentes e três chances de errar o
alvo de toque de 48 px que o documento 15 §5 exige.

### 2. O paginador não conhece domínio

Ele percorre e diz a posição; não sabe o que é conteúdo, pergunta ou resposta. É a mesma
escolha que o `BlocoRecolhivel` já fez ao receber o resumo de fora (design daquela change —
decisão 2), e é o que permite que o desafio adicione o voltar sem que o conteúdo da missão
ganhe um botão que não lhe serve.

### 3. O desafio navega nos dois sentidos; o conteúdo, só adiante

`RN-05-45` afere 60% sobre o conjunto, então o Guerreiro(a) precisa poder rever e trocar uma
resposta antes de submeter — daí o voltar. O conteúdo da missão não tem nada a corrigir, e o
voltar ali seria botão sem consequência. O paginador oferece o retorno como opcional, e cada
tela liga o que lhe cabe.

### 4. Pergunta sem resposta leva até ela, em vez de só contá-la

Com todas as perguntas na tela, dizer "falta responder 2" bastava: elas estavam à vista. Uma
por vez, a mesma frase manda procurar. A sinalização passa a navegar até a primeira pendente.

### 5. Resumo neutro, escrito por quem monta o bloco

`"Crédito e licença"` e `"Próxima missão"` — nomeiam o que está dentro sem entregar o
conteúdo. O componente não os deriva: quem monta declara, como já faz na Operação.

### 6. O `BlocoRecolhivel` não ganha variante nova

A mudança é de **regra**, não de desenho: a spec o restringia à Operação. O componente já
cumpre o que a Arena precisa — nasce fechado, controle com rótulo, sem animação. Se o
temperamento Arena exigir ajuste visual, ele sai pelos tokens que a camada de tema já declara,
não por uma prop de aparência.

### 7. A paginação é estado de tela, não de sessão

Índice em `useState`, perdido ao desmontar. Ver Non-Goals: retomada não é requisito.

## Risks / Trade-offs

- **Sequência de um item só ganhando moldura de paginação** → o paginador omite o controle
  quando há um item, e a spec o exige em cenário próprio.
- **Testes existentes que afirmam ver tudo de uma vez** → são o sinal certo. Os de
  `comum/trilha/trilha.test.tsx` e os das duas aplicações que hoje conferem "as seis perguntas
  na tela" passam a conferir a sequência; o teste da submissão única não muda, e é ele que
  protege o `RN-05-45`.
- **Conteúdo recolhido invisível a quem precisa dele** → o crédito é obrigação de licença. O
  bloco mantém o conteúdo no documento e alcançável por leitor de tela, e a spec da camada
  comum passa a dizer que recolher nunca equivale a suprimir.
- **A App 05 muda sem que o PRD-05 tenha mudado** → é apresentação, não requisito, e foi
  decisão explícita do fundador de que as duas aplicações mudam juntas. O delta de
  `area-do-guerreiro` registra isso para que a próxima leitura não tome por regressão.

## Open Questions

Nenhuma.
