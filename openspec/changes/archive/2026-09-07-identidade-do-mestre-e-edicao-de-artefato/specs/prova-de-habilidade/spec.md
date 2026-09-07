## ADDED Requirements

### Requirement: O Mestre edita rótulo e endereço dos artefatos do próprio perfil

O núcleo SHALL permitir ao **Mestre em sessão** alterar o **rótulo** e o **endereço** de
qualquer artefato comprobatório do **próprio** perfil, **inclusive o declarado pelo Admin no
cadastro**. O artefato declarado no cadastro NEVER SHALL ser removível por ele. Tentativa
de editar artefato de outra persona SHALL receber 403, e artefato inexistente no perfil, 404.
(`RF-09-66`, `RN-09-14`, documento 02 §1, decisão do fundador de 2026-09-06)

#### Scenario: O Mestre corrige o que ele mesmo publicou

- **WHEN** o Mestre altera o rótulo e o endereço de um artefato que publicou
- **THEN** o artefato passa a valer com os novos valores

#### Scenario: O Mestre corrige o link errado do cadastro

- **WHEN** o Mestre altera o endereço de um artefato declarado pelo Admin no cadastro
- **THEN** a alteração é aceita, e o artefato continua constando do perfil

#### Scenario: A remoção do artefato do cadastro segue vedada

- **WHEN** o Mestre tenta remover um artefato declarado pelo Admin no cadastro
- **THEN** a remoção é recusada e o artefato permanece

#### Scenario: Perfil alheio não se edita

- **WHEN** o Mestre tenta editar artefato do perfil de outra persona
- **THEN** recebe 403 e nada é alterado

### Requirement: O artefato do cadastro editado guarda o valor original

O núcleo SHALL guardar o **rótulo e o endereço originais** de um artefato **declarado no
cadastro** na **primeira** vez que o adulto o editar, junto do momento da edição, e SHALL
servi-los à gestão ao lado dos valores vigentes. Edição posterior SHALL alterar apenas o valor
vigente, preservando o original já guardado. Artefato nunca editado NEVER SHALL apresentar valor
original. (`RN-09-14`, documento 02 §1, decisão do fundador de 2026-09-06)

#### Scenario: A primeira edição fixa o original

- **WHEN** o Mestre edita pela primeira vez um artefato declarado no cadastro
- **THEN** o rótulo e o endereço que o Admin declarou ficam guardados, com o momento da edição

#### Scenario: A segunda edição não apaga o original

- **WHEN** o Mestre edita de novo o mesmo artefato
- **THEN** o valor vigente muda e o original guardado permanece o que o Admin declarou

#### Scenario: Artefato intocado não tem original

- **WHEN** a gestão lê um artefato que ninguém editou
- **THEN** nenhum valor original é apresentado para ele
