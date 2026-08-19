## MODIFIED Requirements

### Requirement: A reserva compromete saldo sem movimentá-lo

O núcleo SHALL manter a **reserva** vinculando uma **aula**, um **tipo de recurso**, uma
**quantidade** e o **ponto de apoio** da aula, em um de três estados: **reservada**,
**consumida** ou **liberada**. A reserva NÃO SHALL ser um lançamento do livro-razão: enquanto
está reservada, ela não credita, não debita e não altera o saldo derivado dos lançamentos.
Tipo de recurso de natureza **durável** NÃO SHALL ser reservável: o seu saldo é patrimônio, não
insumo de atividade, e a reserva que o declare SHALL ser recusada com **422**, indicando o tipo.
A recusa por natureza SHALL ser apurada antes da conferência de disponível, e por isso NÃO SHALL
produzir aula pendente de lastro nem necessidade de recurso publicada. Toda reserva SHALL
registrar autor e momento, como toda escrita do núcleo. (`RF-07-08`, `RN-07-01`, `RN-07-07`,
`RF-01-03`, PRD-07 §8)

#### Scenario: Reserva não altera o saldo derivado

- **WHEN** uma aula reserva 3 unidades de um tipo de recurso num ponto de apoio
- **THEN** o saldo daquele tipo naquele ponto de apoio, derivado dos lançamentos, continua o
  mesmo de antes da reserva

#### Scenario: Reserva nasce no estado reservada

- **WHEN** o agendamento de uma aula reserva os recursos que ela consome
- **THEN** cada reserva é gravada no estado reservada, com autor e momento

#### Scenario: Reserva herda o ponto de apoio da aula

- **WHEN** uma aula de um ponto de apoio reserva um tipo de recurso
- **THEN** a reserva é gravada naquele ponto de apoio, e não em outro

#### Scenario: Aula que declara tipo durável é recusada

- **WHEN** o agendamento de uma aula declara consumir um tipo de recurso de natureza durável
- **THEN** o núcleo responde 422 indicando o tipo, nenhuma reserva é gravada e a aula não é
  agendada

#### Scenario: Tipo durável com saldo de sobra continua recusado

- **WHEN** o agendamento declara um tipo durável cujo saldo no ponto de apoio cobre a
  quantidade pedida
- **THEN** o núcleo responde 422 do mesmo modo, porque a recusa é pela natureza e não pela
  falta

#### Scenario: Tipo durável não vira aula pendente de lastro

- **WHEN** o agendamento de uma aula é recusado por declarar tipo durável
- **THEN** a aula não nasce pendente de lastro e nenhuma necessidade de recurso é publicada
  por ela
