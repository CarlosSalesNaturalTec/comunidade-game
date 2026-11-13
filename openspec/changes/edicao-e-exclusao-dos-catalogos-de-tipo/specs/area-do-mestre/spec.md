## ADDED Requirements

### Requirement: A declaração de recompensa não oferece tipo de recurso desativado

O seletor de tipo de recurso da **declaração de recompensa** do desbloqueio NEVER SHALL oferecer
tipo **desativado** no catálogo. A recompensa já declarada com um tipo que foi desativado depois
SHALL seguir apresentada junto da missão, com o nome do tipo, e a fila de entregas pendentes
SHALL seguir apresentando-a. (`RF-07-52`, `RF-09-84`)

#### Scenario: O seletor da recompensa não oferece tipo desativado

- **WHEN** o Mestre autor abre a declaração de recompensa e há um tipo de recurso desativado
- **THEN** o tipo desativado não aparece entre os tipos que ele pode escolher

#### Scenario: A recompensa já declarada segue com o nome do tipo

- **WHEN** a missão tem recompensa declarada com um tipo que foi desativado depois
- **THEN** a recompensa segue apresentada junto da missão, com o nome do tipo
