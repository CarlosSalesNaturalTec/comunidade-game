## Purpose

O Resultado é o registro de que um Guerreiro(a) realizou uma atividade da trilha — sem ele não
há o que pontuar, o que desbloquear nem o que autorar por trilha ou poder.

## Requirements

### Requirement: Resultado registra quem realizou qual atividade, quando e o quê produziu

O núcleo SHALL registrar, para cada Resultado, o **Guerreiro(a)** que realizou, a **atividade**
realizada, a **aula** em que foi lançado, a **data do fato** (nunca substituída pela do
registro, PRD-01 §9) e o que foi **produzido**, em referência à `producao_esperada` já declarada
na atividade. Resultado sem atividade, sem Guerreiro(a), **sem aula** ou sem produção declarada
SHALL ser recusado com **422**, indicando o campo em falta. A aula é o que liga o resultado às
reservas que a baixa consome (documento 04 §1). (`RF-01-20`, `RF-07-09`, `RF-02-35`, 11 §§2.2, 4)

#### Scenario: Resultado registrado com produção declarada

- **WHEN** chega um Resultado com Guerreiro(a), atividade, aula, data do fato e produção
- **THEN** o núcleo grava o Resultado vinculado àquela atividade, àquele Guerreiro(a) e àquela
  aula

#### Scenario: Resultado sem atividade é recusado

- **WHEN** chega um Resultado sem atividade vinculada
- **THEN** o núcleo responde 422 indicando o campo em falta e nada é gravado

#### Scenario: Resultado sem produção é recusado

- **WHEN** chega um Resultado sem a produção do Guerreiro(a)
- **THEN** o núcleo responde 422 indicando o campo em falta e nada é gravado

#### Scenario: Resultado sem aula é recusado

- **WHEN** chega um Resultado sem a aula em que foi lançado
- **THEN** o núcleo responde 422 indicando o campo em falta e nada é gravado

### Requirement: O lançamento da atividade realizada é ato por aula e converte as reservas em baixa

O núcleo SHALL expor o **lançamento da atividade realizada** como ato **por aula**, de
**Admin**, que registra em uma operação os Resultados de todos os participantes daquela aula.
Na mesma operação, o núcleo SHALL converter **cada reserva** da aula em **baixa**: a reserva
passa a **consumida** e um **lançamento de débito** é gravado, com o tipo de recurso, a
quantidade e o **ponto de apoio da aula**. Não há operação de baixa separada deste ato. A aula
SHALL passar à situação **realizada**. (`RF-07-09`, `RF-02-35`, `RN-07-36`, `RN-07-01`,
`RF-01-16`, `RF-01-03`, documento 04 §1, PRD-07 §5.3)

#### Scenario: Lançamento gera um débito por reserva

- **WHEN** um Admin lança a atividade realizada numa aula com duas reservas
- **THEN** o núcleo grava dois lançamentos de débito, um por reserva, no ponto de apoio da aula,
  e ambas as reservas passam a consumida

#### Scenario: O débito derruba o saldo do ponto de apoio da aula

- **WHEN** a atividade realizada é lançada numa aula que reservou 3 unidades de um tipo
- **THEN** o saldo daquele tipo no ponto de apoio da aula cai em 3

#### Scenario: Lançamento de aula sem reservas apenas registra os resultados

- **WHEN** um Admin lança a atividade realizada numa aula que não declarou recurso algum
- **THEN** o núcleo grava os Resultados, não gera débito algum e a aula passa a realizada

#### Scenario: Mestre não lança a atividade da aula

- **WHEN** um Mestre tenta lançar a atividade realizada de uma aula
- **THEN** o núcleo responde 403 e nada é gravado

### Requirement: O desfecho do Resultado é lançado pela gestão, em três valores fechados

O núcleo SHALL exigir, em todo Resultado, um **desfecho** entre exatamente três valores:
**realizada**, **realizada com mérito** ou **mérito extra por auxílio aos colegas** (11 §4).
Quem lança o desfecho é o **Mestre autor** da trilha a que a atividade pertence, ou um **Admin**
— a mesma matriz de posse que já vale para a trilha, a missão e a atividade (`RF-01-16`). Mestre
que não é o autor SHALL receber **403**. O desfecho SHALL ser gravado com a autoria de quem
lançou (`RN-01-13`). (`RF-01-20`, `RF-01-16`, `RF-01-03`, 11 §4)

#### Scenario: Mestre autor lança desfecho "realizada com mérito"

- **WHEN** o Mestre autor da trilha lança o desfecho "realizada com mérito" para um Resultado
- **THEN** o núcleo grava o desfecho com a autoria, data e hora de quem lançou

#### Scenario: Desfecho fora dos três valores é recusado

- **WHEN** chega um Resultado com desfecho que não é nenhum dos três valores fechados
- **THEN** o núcleo responde 422 e nada é gravado

#### Scenario: Mestre que não é o autor é recusado

- **WHEN** um Mestre que não é o autor da trilha tenta lançar o desfecho de um Resultado dela
- **THEN** o núcleo responde 403 e nada é gravado
