## ADDED Requirements

### Requirement: A lista da área Recursos traz a necessidade da recompensa com a trilha

A tabela de necessidades da App 03 SHALL apresentar também a necessidade da **recompensa de
marco**, na ordem em que o núcleo a devolve, com a **trilha** na coluna da aula, no lugar da
data e do horário, e as demais colunas — comunidade, ponto de apoio, recurso, falta e valor —
como na da aula. A linha SHALL identificar-se por comunidade, trilha e tipo, e a aplicação
NEVER SHALL somar nem recalcular a falta. (`RF-02-58`, `RF-07-54`, documento 04 §1)

#### Scenario: A necessidade da recompensa aparece com a trilha

- **WHEN** o núcleo devolve uma necessidade de recompensa
- **THEN** a linha mostra a trilha no lugar da aula, com comunidade, ponto de apoio, recurso,
  falta e valor

#### Scenario: O aporte que fecha a falta da recompensa a tira da lista

- **WHEN** um aporte registrado fecha a falta de uma necessidade de recompensa
- **THEN** a lista recarregada não traz mais aquela linha

### Requirement: A publicação da missão aceita a necessidade da recompensa

O seletor de necessidade de origem da publicação da missão SHALL oferecer também as
necessidades de recompensa, identificadas pela trilha, e a publicação SHALL enviar comunidade,
trilha e tipo no lugar da aula. (`RF-02-102`, `RF-02-103`, `RF-07-54`)

#### Scenario: O Admin publica missão pela necessidade da recompensa

- **WHEN** o Admin escolhe uma necessidade de recompensa e preenche os campos da missão
- **THEN** a aplicação envia comunidade, trilha e tipo, e a missão é publicada
