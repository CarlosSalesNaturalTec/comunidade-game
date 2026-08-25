## ADDED Requirements

### Requirement: A atividade presencial declara a aula em que acontece

O núcleo SHALL aceitar, em cada **atividade**, a **aula** em que ela acontece — o vínculo que
transforma a atividade avulsa em **programação de um encontro** (documento 05 §4). O vínculo
SHALL ser **opcional**: atividade sem aula declarada segue válida, e é o caso de tudo o que
corre entre encontros.

Só atividade de **formato presencial** SHALL declarar aula; atividade **on-line** ou
**assíncrona** que declare uma SHALL ser recusada com **422**. É o que torna concreto o
"presenciais **do encontro**" contra "on-line **entre** encontros" que o `RF-09-73` já pedia.

Quem declara é o **Mestre autor** da trilha a que a missão da atividade pertence, ou um
**Admin** — a mesma matriz de posse que já vale para a trilha, a missão e a atividade
(`RF-01-16`). Mestre que não é o autor SHALL receber **403**. Aula inexistente SHALL ser
recusada com **422**. (`RF-09-69`, `RF-09-73`, `RF-04-35`, `RF-01-16`, documento 05 §4)

#### Scenario: O Mestre autor declara a aula da sua atividade presencial

- **WHEN** o Mestre autor envia uma atividade de formato presencial declarando a aula em que
  ela acontece
- **THEN** o núcleo grava a atividade com a aula declarada e a devolve

#### Scenario: Atividade sem aula declarada segue válida

- **WHEN** o Mestre autor envia uma atividade sem declarar aula alguma
- **THEN** o núcleo grava a atividade sem vínculo com encontro algum

#### Scenario: Atividade on-line que declara aula é recusada

- **WHEN** chega uma atividade de formato on-line declarando uma aula
- **THEN** o núcleo responde 422 indicando o campo e nada é gravado

#### Scenario: Atividade assíncrona que declara aula é recusada

- **WHEN** chega uma atividade de formato assíncrono declarando uma aula
- **THEN** o núcleo responde 422 indicando o campo e nada é gravado

#### Scenario: Mestre que não é o autor não declara a aula

- **WHEN** um Mestre que não é o autor da trilha tenta declarar a aula de uma atividade dela
- **THEN** o núcleo responde 403 e a atividade não muda

#### Scenario: Aula inexistente é recusada

- **WHEN** chega uma atividade declarando uma aula que não existe
- **THEN** o núcleo responde 422 e nada é gravado
