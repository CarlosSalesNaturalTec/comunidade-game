## Purpose

O Resultado é o registro de que um Guerreiro(a) realizou uma atividade da trilha — sem ele não
há o que pontuar, o que desbloquear nem o que autorar por trilha ou poder.

## Requirements

### Requirement: Resultado registra quem realizou qual atividade, quando e o quê produziu

O núcleo SHALL registrar, para cada Resultado, o **Guerreiro(a)** que realizou, a **atividade**
realizada, a **data do fato** (nunca substituída pela do registro, PRD-01 §9) e o que foi
**produzido**, em referência à `producao_esperada` já declarada na atividade. Resultado sem
atividade, sem Guerreiro(a) ou sem produção declarada SHALL ser recusado com **422**, indicando o
campo em falta. (`RF-01-20`, 11 §§2.2, 4)

#### Scenario: Resultado registrado com produção declarada

- **WHEN** chega um Resultado com Guerreiro(a), atividade, data do fato e produção
- **THEN** o núcleo grava o Resultado vinculado àquela atividade e àquele Guerreiro(a)

#### Scenario: Resultado sem atividade é recusado

- **WHEN** chega um Resultado sem atividade vinculada
- **THEN** o núcleo responde 422 indicando o campo em falta e nada é gravado

#### Scenario: Resultado sem produção é recusado

- **WHEN** chega um Resultado sem a produção do Guerreiro(a)
- **THEN** o núcleo responde 422 indicando o campo em falta e nada é gravado

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
