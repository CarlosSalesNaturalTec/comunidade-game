## ADDED Requirements

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
