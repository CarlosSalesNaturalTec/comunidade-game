## ADDED Requirements

### Requirement: O item do catálogo avulso declara só tipo de recompensa

O cadastro do item do catálogo avulso, pelo Mestre ou pela oferta do Apoiador, SHALL aceitar só
tipo de recurso de finalidade **recompensa**; o de **consumo do encontro** e o **durável**, que não
tem finalidade, SHALL ser recusados com **422**, indicando o tipo, sem gravar o item. O item já
cadastrado segue inalterado. (`RF-07-53`, `RN-07-41`)

#### Scenario: Item com tipo de consumo do encontro é recusado

- **WHEN** um Mestre cadastra item do catálogo avulso com tipo de consumo do encontro
- **THEN** o núcleo responde 422 indicando o tipo, e nada é gravado
