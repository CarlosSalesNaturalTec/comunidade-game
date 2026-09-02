# reserva-de-recurso Specification

## Purpose

A reserva é o que faz valer o invariante 9: ela compromete o recurso que uma aula vai consumir
no momento em que a aula é agendada, muito antes de o recurso sair do ponto de apoio, e só
larga esse compromisso por baixa ou por liberação — nunca pelo relógio.

## Requirements

### Requirement: A reserva compromete saldo sem movimentá-lo

O núcleo SHALL manter a **reserva** vinculando **uma aula ou um desafio extra** — exatamente um
dos dois, nunca os dois nem nenhum —, um **tipo de recurso**, uma **quantidade** e o **ponto de
apoio**: o da aula, quando a reserva é de aula; o que a proposta declarou, quando é de desafio
extra. A reserva SHALL estar em um de três estados: **reservada**, **consumida** ou
**liberada**. A reserva NÃO SHALL ser um lançamento do livro-razão: enquanto está reservada, ela
não credita, não debita e não altera o saldo derivado dos lançamentos. Tipo de recurso de
natureza **durável** NÃO SHALL ser reservável, seja pela aula, seja pela recompensa do desafio
extra: o saldo é patrimônio, não insumo de atividade, e a reserva que o declare SHALL ser
recusada com **422**, indicando o tipo. A recusa por natureza SHALL ser apurada antes da
conferência de disponível, e por isso NÃO SHALL produzir aula pendente de lastro nem necessidade
de recurso publicada. Toda reserva SHALL registrar autor e momento, como toda escrita do núcleo.
(`RF-07-08`, `RF-07-39`, `RN-07-01`, `RN-07-07`, `RF-01-03`, PRD-07 §8)

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

#### Scenario: A reserva do desafio extra fica no ponto de apoio que a proposta declarou

- **WHEN** um desafio extra é publicado reservando a recompensa
- **THEN** a reserva é gravada sem aula, presa ao desafio, no ponto de apoio da proposta

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

### Requirement: O saldo disponível é o derivado menos o reservado

O núcleo SHALL apurar, para cada par tipo de recurso e ponto de apoio, a **quantidade
reservada** — a soma das reservas no estado **reservada** — e a **quantidade disponível**, que
é o saldo derivado dos lançamentos **menos** a reservada. A decisão de reservar SHALL ser
tomada contra a **disponível**, nunca contra o saldo total. (`RF-07-07`, `RF-07-08`, PRD-07 §8)

#### Scenario: Reserva reduz o disponível sem reduzir o saldo

- **WHEN** o saldo de um tipo num ponto de apoio é 10 e uma aula reserva 4
- **THEN** o saldo continua 10 e a quantidade disponível passa a 6

#### Scenario: Segunda aula não reserva o que a primeira já comprometeu

- **WHEN** o saldo de um tipo num ponto de apoio é 10, uma aula já reservou 8 e outra aula
  pede 5
- **THEN** a segunda aula não reserva nada, porque a disponível é 2

### Requirement: A reserva sai por baixa ou por liberação, e nunca por decurso de prazo

O núcleo SHALL dar à reserva **de aula** exatamente duas saídas: a **baixa**, pelo lançamento da
atividade realizada, que a leva a **consumida** e gera o lançamento de débito correspondente; e a
**liberação**, pelo cancelamento da aula, que a leva a **liberada** e devolve a quantidade à
disponível. A reserva **de desafio extra** SHALL sair pela **liberação**, no **encerramento** do
desafio pelo Admin, que a leva a **liberada** e devolve a quantidade à disponível. Nenhuma
reserva SHALL mudar de estado por decurso de prazo: aula que passa da data sem lançamento nem
cancelamento SHALL manter as reservas no estado **reservada**, e desafio extra cuja vigência
venceu sem encerramento, também. Toda saída SHALL registrar autor e momento. (`RF-07-09`,
`RF-07-40`, `RF-01-03`, PRD-07 §5.3, documento 04 §1)

#### Scenario: Baixa leva a reserva a consumida

- **WHEN** a atividade realizada é lançada numa aula com reservas
- **THEN** cada reserva passa a consumida e o saldo cai pelo débito correspondente

#### Scenario: Cancelamento devolve a quantidade à disponível

- **WHEN** uma aula com 4 unidades reservadas é cancelada
- **THEN** as reservas passam a liberada e a quantidade disponível volta a incluir as 4

#### Scenario: Aula que passou da data mantém a reserva

- **WHEN** a data e o horário final de uma aula com reservas já passaram, sem lançamento nem
  cancelamento
- **THEN** as reservas seguem no estado reservada e a quantidade disponível segue reduzida

#### Scenario: Encerramento do desafio devolve a quantidade à disponível

- **WHEN** o Admin encerra um desafio extra publicado cuja recompensa segue reservada
- **THEN** a reserva passa a liberada e a quantidade disponível volta a incluir a recompensa

#### Scenario: Desafio com vigência vencida mantém a reserva

- **WHEN** a vigência de um desafio extra publicado termina sem que o Admin o encerre
- **THEN** a reserva segue no estado reservada e a quantidade disponível segue reduzida
