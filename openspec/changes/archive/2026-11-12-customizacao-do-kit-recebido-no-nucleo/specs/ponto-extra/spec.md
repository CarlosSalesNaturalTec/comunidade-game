## ADDED Requirements

### Requirement: O cuidado com o bem recebido credita 1 ponto extra

A **conservação** validada de um bem recebido e a **customização** aprovada de um kit são fontes
**só extra** do documento 11 §5: cada uma SHALL creditar **1 ponto extra** — e **nenhum ponto
regular** — ao Guerreiro(a), no **acumulado** e no **saldo disponível**, na mesma operação que
grava a validação ou o julgamento. O crédito SHALL ocorrer uma única vez por ato, e o mesmo bem
SHALL pontuar no máximo uma vez por encontro, entre as duas fontes (capability
`conservacao-do-bem-recebido`). (`RF-01-85`, `RF-01-87`, `RN-01-66`, 11 §5)

#### Scenario: A conservação credita 1 extra e nenhum regular

- **WHEN** o Mestre da aula valida a conservação de um bem recebido
- **THEN** o acumulado e o saldo disponível do Guerreiro(a) sobem 1, e nenhum ponto regular é
  creditado

#### Scenario: A customização aprovada credita 1 extra e nenhum regular

- **WHEN** o Mestre da aula aprova a customização de um kit
- **THEN** o acumulado e o saldo disponível do Guerreiro(a) sobem 1, e nenhum ponto regular é
  creditado

#### Scenario: A reprovação não credita

- **WHEN** o Mestre da aula reprova a customização de um kit
- **THEN** o núcleo não credita ponto algum
