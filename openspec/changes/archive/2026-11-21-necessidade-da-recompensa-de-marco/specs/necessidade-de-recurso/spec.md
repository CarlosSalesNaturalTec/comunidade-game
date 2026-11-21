## ADDED Requirements

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

## MODIFIED Requirements

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
