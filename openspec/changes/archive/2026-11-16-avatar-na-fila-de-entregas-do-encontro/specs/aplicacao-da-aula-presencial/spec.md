## MODIFIED Requirements

### Requirement: A App 01 apresenta as entregas pendentes do encontro

A App 01 SHALL apresentar, a quem opera o aparelho, as **entregas pendentes do encontro em
curso**: cada Guerreiro(a) com **presença registrada naquela aula** que alcançou marco com
recompensa declarada e ainda não a recebeu. Cada pendência SHALL trazer o Guerreiro(a) por
**nick e avatar**, a trilha, a missão que é o marco, o tipo de recurso e a quantidade, e
NEVER SHALL trazer valor em moedas ou em reais. O avatar SHALL ser **desenhado** ao lado do nick, e o conteúdo
do campo do avatar NEVER SHALL aparecer como texto (decisão do fundador de 2026-11-16). (`RF-09-75`, `RF-04-55`, invariantes 12 e 16)

#### Scenario: Quem chegou e conquistou aparece na fila do encontro

- **WHEN** um Guerreiro(a) com presença registrada naquela aula alcançou marco com recompensa
  e ainda não a recebeu
- **THEN** a pendência dele aparece na fila do encontro, com nick, avatar, trilha, marco, tipo
  de recurso e quantidade

#### Scenario: Quem não registrou presença não aparece

- **WHEN** um Guerreiro(a) da mesma comunidade alcançou o marco, mas não tem presença
  registrada naquela aula
- **THEN** a pendência dele não aparece na fila do encontro — ela segue na App 09

#### Scenario: Encontro sem pendência alguma diz que não há

- **WHEN** ninguém com presença registrada tem entrega pendente
- **THEN** a aplicação diz que não há entrega pendente no encontro, e não apresenta erro

#### Scenario: O avatar é desenhado, não impresso como texto

- **WHEN** a fila do encontro apresenta uma pendência
- **THEN** o desenho do avatar aparece ao lado do nick, e nenhum trecho do objeto do avatar
  aparece como texto na tela
