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

Cada necessidade SHALL sair com a **espécie** — da aula ou da recompensa de marco —, **tipo de
recurso, quantidade que falta, valor em moedas, comunidade e ponto de apoio**. A da aula SHALL
trazer a **data e o horário da aula** e identificar-se pelo par **aula + tipo de recurso**; a da
recompensa SHALL trazer a **trilha** no lugar da aula, sem data nem horário, e identificar-se
por **comunidade + trilha + tipo de recurso**. O tipo de recurso, a comunidade, o ponto de
apoio e a trilha SHALL sair com o **nome** ao lado do identificador, para que a leitura se
apresente a quem não tem acesso às rotas de cadastro da gestão. A saída NÃO SHALL trazer valor
em reais, em campo algum, nem dado de pessoa: a necessidade descreve recurso, aula ou trilha e
lugar, e nada de quem participa dela. A mesma saída SHALL valer para a rota pública e para a do
Mestre, com as necessidades de aula primeiro, pela data, e as de recompensa depois.
(`RF-07-27`, `RF-07-54`, `RF-03-47`, `RN-07-05`, `RF-14-24`, `RN-14-09`, invariante 16 do
documento 99 §6, documento 04 §1)

#### Scenario: A necessidade traz os campos publicados

- **WHEN** uma necessidade de aula é lida em qualquer das duas rotas
- **THEN** ela traz espécie, tipo de recurso, quantidade que falta, valor em moedas,
  comunidade, ponto de apoio, data e horário da aula, e identifica a aula e o tipo

#### Scenario: A necessidade da recompensa traz a trilha no lugar da aula

- **WHEN** uma necessidade de recompensa é lida em qualquer das duas rotas
- **THEN** ela traz espécie, tipo de recurso, quantidade que falta, valor em moedas,
  comunidade, ponto de apoio e trilha, sem aula, data nem horário

#### Scenario: Os nomes acompanham os identificadores

- **WHEN** uma necessidade é lida em qualquer das duas rotas
- **THEN** o tipo de recurso, a comunidade, o ponto de apoio e, na de recompensa, a trilha saem
  com o nome ao lado do identificador

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

O núcleo SHALL servir ao **Mestre em sessão** a lista das necessidades — das aulas e das
recompensas de marco — das **comunidades a que ele está vinculado**, e NÃO SHALL alcançar
necessidade de outra comunidade. O filtro é o **vínculo de comunidade** — o mesmo que governa o
cancelamento da aula —, e não a autoria de trilha. (`RF-07-27`, `RF-09-56`, `RF-01-72`,
documento 04 §1)

#### Scenario: O Mestre vê as necessidades da comunidade dele

- **WHEN** um Mestre em sessão pede as suas necessidades
- **THEN** o núcleo responde as das aulas e as das recompensas das comunidades a que ele está
  vinculado

#### Scenario: A comunidade alheia fica de fora

- **WHEN** existe necessidade de aula ou de recompensa numa comunidade a que o Mestre não está
  vinculado
- **THEN** ela não aparece na lista dele

### Requirement: A recompensa de marco gera necessidade por comunidade, ponto de apoio, tipo e trilha

O núcleo SHALL derivar uma segunda espécie de necessidade, a **da recompensa de marco**, sem
gravar entidade alguma, uma por **comunidade, ponto de apoio, tipo de recurso e trilha**. A
quantidade pedida SHALL ser, somada sobre as recompensas de marco da trilha daquele tipo, o
número de **Guerreiros(as) com vínculo vigente na comunidade** que **ainda não receberam**
aquela recompensa, vezes a **quantidade de cada entrega** dela. A falta SHALL ser essa
quantidade menos o **disponível** — saldo menos o reservado — atribuível a ela no ponto de
apoio. Item cuja falta seja zero NÃO SHALL aparecer na lista. (`RF-07-54`, `RF-07-18`,
`RN-07-42`, documento 04 §1)

#### Scenario: A falta da recompensa vira necessidade

- **WHEN** a comunidade tem 12 Guerreiros(as) com vínculo vigente, 2 deles já receberam a
  recompensa de 1 kit da trilha, e o ponto de apoio da aula anterior tem 4 kits disponíveis
- **THEN** a lista traz uma necessidade daquela comunidade, ponto de apoio, tipo e trilha, com
  falta de 6

#### Scenario: Duas recompensas do mesmo tipo na trilha somam

- **WHEN** a trilha declara duas recompensas do mesmo tipo, em marcos diferentes
- **THEN** a necessidade daquela trilha e tipo soma o que cada uma ainda pede

#### Scenario: Vínculo encerrado não conta

- **WHEN** um Guerreiro(a) teve o vínculo com a comunidade encerrado
- **THEN** ele não entra na quantidade pedida

#### Scenario: Recompensa coberta não aparece

- **WHEN** o disponível no ponto de apoio cobre tudo o que a trilha ainda pede daquele tipo
- **THEN** a trilha não aparece na lista para aquele tipo

### Requirement: Contam as trilhas com atividade em aula não cancelada da comunidade

O núcleo SHALL gerar necessidade de recompensa só para a trilha que tenha **atividade não
removida** ligada a **aula não cancelada** da comunidade — passada, em andamento ou futura.
(`RF-07-54`, documento 04 §1, decisão do fundador de 2026-11-21)

#### Scenario: Trilha sem atividade em aula da comunidade fica de fora

- **WHEN** uma trilha tem recompensa de marco e nenhuma atividade em aula da comunidade
- **THEN** a comunidade não tem necessidade daquela trilha

#### Scenario: Aula passada conta

- **WHEN** a única atividade da trilha na comunidade foi numa aula já realizada
- **THEN** a trilha conta para a necessidade da comunidade

#### Scenario: Aula cancelada não conta

- **WHEN** a única atividade da trilha na comunidade está numa aula cancelada
- **THEN** a trilha não conta para a necessidade da comunidade

### Requirement: O ponto de apoio é o da aula imediatamente anterior da comunidade

A necessidade da recompensa SHALL usar o ponto de apoio da **aula imediatamente anterior** da
comunidade — a de início mais recente até o momento da leitura, não cancelada —, o mesmo de
onde sai a entrega fora do encontro. **Comunidade sem aula anterior** NÃO SHALL gerar
necessidade de recompensa. (`RF-07-54`, `RF-09-76`, documento 04 §1, decisão do fundador de
2026-11-21)

#### Scenario: A necessidade sai no ponto da aula anterior

- **WHEN** a aula de início mais recente da comunidade aconteceu no ponto de apoio A
- **THEN** a necessidade da recompensa daquela comunidade aparece no ponto de apoio A, contra o
  disponível de A

#### Scenario: Comunidade sem aula anterior não gera necessidade

- **WHEN** a comunidade só tem aulas futuras ou canceladas
- **THEN** nenhuma necessidade de recompensa daquela comunidade aparece

### Requirement: Entre trilhas, o disponível é contado pela atividade em aula mais antiga

Disputando o mesmo tipo de recurso no mesmo ponto de apoio, o núcleo SHALL atribuir o
disponível às necessidades de recompensa em **ordem fixa**: primeiro a trilha cuja atividade
em aula da comunidade é a **mais antiga**, e a seguinte enxerga só o que sobrou. Somadas, as
faltas SHALL dar a falta real do conjunto. (`RF-07-54`, documento 04 §1, decisão do fundador de
2026-11-21)

#### Scenario: A trilha mais antiga conta primeiro

- **WHEN** duas trilhas da comunidade pedem 10 kits do mesmo tipo cada, no mesmo ponto de apoio
  com 6 disponíveis, e a trilha A tem atividade em aula anterior à da trilha B
- **THEN** a trilha A aparece com falta de 4, e a trilha B, com falta de 10

### Requirement: A absorção que atende a necessidade da recompensa declara comunidade e trilha

A absorção registrada a partir de uma necessidade de recompensa SHALL declarar a
**comunidade** e a **trilha** cuja necessidade atende, no lugar da aula, e SHALL ser recusada
com **422** quando o ponto de apoio não for o da aula imediatamente anterior da comunidade ou
quando a trilha não declarar recompensa de marco daquele tipo. A declaração de aula e a de
comunidade e trilha NÃO SHALL vir juntas. A absorção credita o ponto de apoio, e a falta
SHALL aparecer abatida na leitura seguinte. (`RF-07-28`, `RF-07-54`, `RF-09-57`)

#### Scenario: A absorção abate a falta da recompensa

- **WHEN** um Mestre absorve 3 kits, declarando a comunidade e a trilha de uma necessidade de
  recompensa com falta de 6
- **THEN** a necessidade continua publicada com falta de 3

#### Scenario: Ponto de apoio diferente do da aula anterior é recusado

- **WHEN** a absorção declara comunidade e trilha com outro ponto de apoio
- **THEN** o núcleo responde 422 e nada é creditado

#### Scenario: Aula e trilha juntas são recusadas

- **WHEN** a absorção declara a aula e também a comunidade e a trilha
- **THEN** o núcleo responde 422 e nada é creditado
