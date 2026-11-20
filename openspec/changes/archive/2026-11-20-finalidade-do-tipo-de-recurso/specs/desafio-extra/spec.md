## ADDED Requirements

### Requirement: A recompensa do desafio extra declara só tipo de recompensa

A proposta do desafio extra, do Apoiador ou do Mestre, SHALL aceitar como recompensa só tipo de
recurso de finalidade **recompensa**; o de **consumo do encontro** SHALL ser recusado com
**422**, indicando o tipo, sem gravar a proposta — e o **durável**, que não tem finalidade,
passa a ser recusado já na proposta, e não só na aprovação. O desafio já proposto segue
inalterado. (`RF-07-53`, `RN-07-41`)

#### Scenario: Desafio com recompensa de consumo do encontro é recusado

- **WHEN** um Apoiador propõe desafio extra com recompensa de tipo consumo do encontro
- **THEN** o núcleo responde 422 indicando o tipo, e nada é gravado
