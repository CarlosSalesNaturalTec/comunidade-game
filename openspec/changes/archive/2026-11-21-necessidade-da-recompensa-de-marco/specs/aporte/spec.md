## ADDED Requirements

### Requirement: O aporte por absorção aponta a aula ou a comunidade e a trilha

O aporte por absorção SHALL guardar a necessidade que atende: a **aula**, na necessidade da
aula, ou a **comunidade** e a **trilha**, na necessidade da recompensa de marco — nunca as
duas. Só o aporte por absorção SHALL declarar comunidade e trilha; o registrado pela gestão
que as declare SHALL ser recusado com **422**. O tipo de recurso da absorção pela necessidade
da recompensa SHALL ser aceito mesmo desativado, como o da aula, porque segue a necessidade já
publicada. (`RF-07-28`, `RF-07-54`, `RF-09-57`, `RF-07-52`)

#### Scenario: A absorção da recompensa guarda comunidade e trilha

- **WHEN** um Mestre registra absorção declarando comunidade e trilha de uma necessidade de
  recompensa
- **THEN** o aporte é gravado com a comunidade e a trilha, sem aula, e credita o ponto de apoio

#### Scenario: Aporte da gestão não declara trilha

- **WHEN** o Admin registra aporte que não é absorção declarando comunidade e trilha
- **THEN** o núcleo responde 422 e nada é gravado

### Requirement: A declaração por necessidade aponta a aula ou a comunidade e a trilha

A declaração do Apoiador de origem **necessidade** SHALL guardar, com o tipo de recurso, a
**aula**, na necessidade da aula, ou a **comunidade** e a **trilha**, na necessidade da
recompensa de marco — uma das duas, nunca as duas nem nenhuma. Como na da aula, a declaração
pendente NEVER SHALL abater a falta. (`RF-14-25`, `RF-07-54`, `RN-14-07`)

#### Scenario: A declaração pela necessidade da recompensa é aceita

- **WHEN** o Apoiador declara aporte escolhendo uma necessidade de recompensa
- **THEN** a declaração guarda a comunidade, a trilha e o tipo, nasce pendente, e a necessidade
  continua com a mesma falta

#### Scenario: Declaração por necessidade sem aula nem trilha é recusada

- **WHEN** a declaração de origem necessidade não traz aula nem comunidade e trilha
- **THEN** o núcleo responde 422 e nada é gravado
