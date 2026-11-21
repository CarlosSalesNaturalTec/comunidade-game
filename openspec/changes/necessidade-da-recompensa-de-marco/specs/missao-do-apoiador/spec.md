## ADDED Requirements

### Requirement: A missão nasce também da necessidade da recompensa de marco

A missão do Apoiador SHALL aceitar como necessidade de origem a **da recompensa de marco**,
apontando **comunidade, trilha e tipo de recurso** no lugar da aula e do tipo. A publicação
SHALL ser recusada com **422** quando aquela combinação não estiver entre as necessidades
publicadas no momento do ato, ou quando vier a aula junto com a comunidade e a trilha. A
missão aberta SHALL sair da leitura pública quando a necessidade da recompensa por trás dela
deixar de existir, como a da aula. (`RF-02-102`, `RF-02-103`, `RN-14-31`, `RF-14-71`,
`RF-07-54`, documento 04 §1)

#### Scenario: A missão aponta a necessidade da recompensa

- **WHEN** um Admin publica a missão apontando comunidade, trilha e tipo de uma necessidade de
  recompensa em aberto
- **THEN** a missão é gravada aberta, com a comunidade, a trilha e o tipo, sem aula

#### Scenario: Recompensa sem necessidade publicada é recusada

- **WHEN** a publicação aponta comunidade, trilha e tipo sem necessidade de recompensa em
  aberto
- **THEN** o núcleo responde 422 e nada é gravado

#### Scenario: A missão some quando a falta da recompensa se fecha

- **WHEN** a necessidade da recompensa por trás de uma missão aberta deixa de existir
- **THEN** a missão sai da leitura pública
