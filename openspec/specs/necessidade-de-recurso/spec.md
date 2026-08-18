# necessidade-de-recurso Specification

## Purpose

Publica o que falta de recurso às aulas em pendente de lastro, para que a falta vire pedido em
vez de recusa silenciosa: é a superfície de leitura por onde a vitrine, o Apoiador e o Mestre
enxergam a diferença que um aporte pode fechar.

## Requirements

### Requirement: A necessidade é derivada da aula pendente de lastro, por tipo de recurso

O núcleo SHALL derivar a **necessidade de recurso** das aulas em situação **pendente de
lastro**, uma por par **aula + tipo de recurso**, sem gravar entidade alguma: a necessidade é
sempre recalculada da leitura, como o saldo. A quantidade que falta SHALL ser a **quantidade
declarada** pela aula para aquele tipo menos a **quantidade disponível** atribuível a ela no
ponto de apoio da aula. Par cuja falta seja zero NÃO SHALL aparecer na lista, ainda que a aula
siga pendente de lastro por outro tipo. Aula em qualquer outra situação — prevista, confirmada,
realizada ou cancelada — NÃO SHALL gerar necessidade, porque só a pendente de lastro tem falta:
a confirmada já detém as reservas. (`RF-07-18`, `RF-07-27`, `RN-07-01`, PRD-07 §8, documento
04 §1)

#### Scenario: A falta de uma aula pendente vira necessidade

- **WHEN** uma aula pendente de lastro declarou 10 unidades de um tipo e o ponto de apoio dela
  tem 4 disponíveis
- **THEN** a lista traz uma necessidade daquela aula e daquele tipo, com falta de 6

#### Scenario: Tipo já coberto não aparece

- **WHEN** uma aula pendente de lastro declarou dois tipos, e o ponto de apoio tem disponível
  bastante para um deles e não para o outro
- **THEN** a lista traz só o tipo em falta, e a aula segue pendente de lastro

#### Scenario: Aula confirmada não gera necessidade

- **WHEN** uma aula está confirmada, com as reservas efetivadas
- **THEN** ela não aparece na lista de necessidades

#### Scenario: Aula cancelada não gera necessidade

- **WHEN** uma aula pendente de lastro é cancelada
- **THEN** ela sai da lista de necessidades

### Requirement: A falta é contada na ordem do horário inicial da aula

Disputando o mesmo tipo de recurso no mesmo ponto de apoio, o núcleo SHALL atribuir a
quantidade disponível às aulas pendentes de lastro pelo **horário inicial da aula, da mais
próxima para a mais distante**: a aula mais próxima conta primeiro o que lhe cabe, e a seguinte
enxerga apenas o que sobrou. É a mesma ordem com que o aporte confirma a aula pendente
(`RN-07-37`), e é o que impede o mesmo disponível de ser contado como cobertura de duas aulas:
somadas, as faltas da lista SHALL dar a falta real do conjunto. A ordem NÃO SHALL depender da
data da leitura: aula cujo horário já passou continua contando primeiro, enquanto o núcleo a
considerar pendente de lastro. (`RF-07-18`, `RN-07-37`, documento 04 §1)

#### Scenario: A aula mais próxima conta primeiro

- **WHEN** duas aulas pendentes de lastro no mesmo ponto de apoio declaram 10 unidades do mesmo
  tipo cada, e há 6 disponíveis
- **THEN** a aula de horário inicial mais próximo aparece com falta de 4, e a mais distante,
  com falta de 10

#### Scenario: Aula cujo horário passou continua na lista

- **WHEN** uma aula segue pendente de lastro depois de o horário inicial dela ter passado
- **THEN** ela continua aparecendo na lista, com a falta dela

### Requirement: A necessidade publicada leva o recurso, a aula e o lugar, nunca reais

Cada necessidade SHALL sair com **tipo de recurso, quantidade que falta, valor em moedas,
comunidade, ponto de apoio, data e horário da aula**, e SHALL identificar-se pelo par **aula +
tipo de recurso**. A saída NÃO SHALL trazer valor em reais, em campo algum, nem dado de pessoa:
a necessidade descreve recurso, aula e lugar, e nada de quem participa dela. A mesma saída
SHALL valer para a rota pública e para a do Mestre. (`RF-07-27`, `RF-03-47`, `RN-07-05`,
invariante 16 do documento 99 §6, documento 04 §1)

#### Scenario: A necessidade traz os campos publicados

- **WHEN** uma necessidade é lida em qualquer das duas rotas
- **THEN** ela traz tipo de recurso, quantidade que falta, valor em moedas, comunidade, ponto
  de apoio, data e horário da aula, e identifica a aula e o tipo

#### Scenario: Nenhuma saída traz reais

- **WHEN** a lista de necessidades é lida
- **THEN** nenhum campo da resposta traz valor em reais

#### Scenario: Nenhuma saída traz pessoa

- **WHEN** a lista de necessidades é lida
- **THEN** nenhum campo da resposta identifica Guerreiro(a), responsável ou provedor

### Requirement: O valor em moedas sai pela vigência da data da leitura

O núcleo SHALL converter a quantidade que falta em **moedas** pelo valor de referência do tipo
**vigente na data da leitura**, com duas casas exatas — é a melhor estimativa corrente, porque
o aporte que fechará a falta ainda não existe e será valorado pela vigência da data dele
(`RF-07-05`). Tipo de recurso **sem vigência válida** na data da leitura SHALL sair **sem valor
em moedas**, e NUNCA com valor arbitrado. (`RN-07-04`, `RN-07-05`, `RF-07-02`, PRD-07 §8)

#### Scenario: A falta é valorada pela vigência corrente

- **WHEN** falta 3 unidades de um tipo cujo valor de referência vigente hoje é 0,50 moeda
- **THEN** a necessidade sai com 1,50 moeda

#### Scenario: Tipo sem vigência sai sem valor

- **WHEN** o tipo de recurso em falta não tem valor de referência vigente na data da leitura
- **THEN** a necessidade sai com a quantidade que falta e sem valor em moedas

### Requirement: A cobertura parcial encolhe a necessidade, e o saldo que fecha a apaga

O aporte homologado menor que a falta NÃO SHALL ser recusado: ele credita, e a necessidade
SHALL aparecer na leitura seguinte com a falta **abatida** do que entrou. A necessidade SHALL
sair da lista somente quando o saldo fechar — o que é o mesmo ato que confirma a aula
(`RN-07-37`). Cada provedor SHALL receber as moedas do que ele mesmo aportou, e NUNCA crédito
pelo que outro deu, o que já decorre de cada aporte gerar o crédito do seu próprio provedor.
(`RF-07-31`, `RN-07-23`, `RN-07-37`, documento 04 §1)

#### Scenario: Aporte parcial abate a falta

- **WHEN** uma necessidade de 6 unidades recebe um aporte homologado de 2 unidades
- **THEN** a leitura seguinte traz a mesma necessidade com falta de 4, e a aula segue pendente
  de lastro

#### Scenario: O aporte que fecha o saldo apaga a necessidade

- **WHEN** um aporte homologado cobre a última parcela que faltava a uma aula
- **THEN** a necessidade some da lista e a aula passa a confirmada no mesmo ato

#### Scenario: Cada provedor recebe as moedas do que aportou

- **WHEN** dois provedores cobrem em partes a mesma necessidade
- **THEN** cada um recebe as moedas do que aportou, e nenhum recebe crédito pelo que o outro
  deu

### Requirement: A absorção que atende a necessidade declara qual aula cobre

A absorção registrada a partir de uma necessidade publicada SHALL declarar a **aula** cuja
necessidade atende, e o núcleo SHALL abater a falta daquela aula pelo que a absorção credita,
confirmando-a quando o saldo fechar — o mesmo caminho de cobertura parcial que a necessidade já
segue para qualquer aporte homologado.

A necessidade SHALL permanecer **derivada**: a declaração liga o aporte à aula, e NÃO SHALL
existir registro de necessidade a que o aporte se refira. A necessidade de destinação
ressarcimento NÃO SHALL existir — o aporte de destinação ressarcimento não abate falta alguma
nem confirma aula. (`RF-07-28`, `RF-07-27`, `RF-07-31`, `RN-07-37`, `RN-07-38`, PRD-07 §8)

#### Scenario: A absorção declarada abate a falta da aula que atende

- **WHEN** um Mestre absorve, declarando a aula cuja necessidade atende, uma quantidade menor do
  que a falta
- **THEN** a necessidade daquela aula e daquele tipo continua publicada com a falta abatida, e a
  aula segue pendente de lastro

#### Scenario: A absorção que fecha a falta confirma a aula

- **WHEN** a absorção declarada cobre exatamente o que faltava à aula
- **THEN** a necessidade sai da lista e a aula passa a confirmada no mesmo ato

#### Scenario: A receita destinada a ressarcir não abate necessidade

- **WHEN** entra um aporte de destinação ressarcimento do mesmo tipo que falta a uma aula
  pendente de lastro
- **THEN** a necessidade daquela aula permanece publicada com a mesma falta

### Requirement: A leitura pública dispensa credencial de persona, nunca a chave

O núcleo SHALL servir a lista de necessidades em **rota pública**, sem credencial de persona, e
SHALL continuar exigindo a **chave da aplicação**, como em toda rota de dados. A rota SHALL
responder sob o prefixo de leitura pública que o núcleo já usa. (`RF-07-27`, `RF-03-47`,
`RF-01-02`, `RF-01-16`, documento 03 §1)

#### Scenario: Visitante sem persona lê a lista

- **WHEN** a lista de necessidades é pedida com chave de aplicação válida e sem credencial de
  persona
- **THEN** o núcleo responde a lista

#### Scenario: Sem chave a rota não responde

- **WHEN** a lista de necessidades é pedida sem chave de aplicação válida
- **THEN** o núcleo recusa, como em toda rota de dados

### Requirement: A lista do Mestre alcança as comunidades a que ele está vinculado

O núcleo SHALL servir ao **Mestre em sessão** a lista das necessidades das aulas das
**comunidades a que ele está vinculado**, e NÃO SHALL alcançar aula de outra comunidade. O
filtro é o **vínculo de comunidade** — o mesmo que governa o cancelamento da aula —, e não a
autoria de trilha: a aula não declara trilha. (`RF-07-27`, `RF-01-72`, documento 04 §1)

#### Scenario: O Mestre vê as necessidades da comunidade dele

- **WHEN** um Mestre em sessão pede as suas necessidades
- **THEN** o núcleo responde as das aulas das comunidades a que ele está vinculado

#### Scenario: A comunidade alheia fica de fora

- **WHEN** existe aula pendente de lastro numa comunidade a que o Mestre não está vinculado
- **THEN** ela não aparece na lista dele
