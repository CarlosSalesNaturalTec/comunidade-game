## ADDED Requirements

### Requirement: A recompensa de marco declara só tipo de recompensa

A declaração da recompensa de marco SHALL aceitar só tipo de recurso de finalidade
**recompensa**; tipo de **consumo do encontro** ou **durável** SHALL ser recusado com **422**,
indicando o tipo, sem gravar a recompensa. Recompensa já declarada com tipo que depois passou a
consumo do encontro SHALL seguir declarada. (`RF-09-71`, `RF-09-84`, `RF-07-53`, `RN-07-41`)

#### Scenario: Recompensa com tipo de consumo do encontro é recusada

- **WHEN** o Mestre autor declara a recompensa de um marco com tipo de consumo do encontro
- **THEN** o núcleo responde 422 indicando o tipo, e nada é gravado

#### Scenario: Recompensa com tipo de recompensa é aceita

- **WHEN** o Mestre autor declara a recompensa de um marco com tipo de finalidade recompensa
- **THEN** a recompensa é gravada
