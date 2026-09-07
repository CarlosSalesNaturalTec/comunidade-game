## ADDED Requirements

### Requirement: A ficha do adulto mostra o artefato de cadastro que o Mestre editou

A App 03 SHALL marcar, na ficha do adulto, o artefato **declarado no cadastro** que o próprio
adulto editou, apresentando o **rótulo e o endereço originais** ao lado dos vigentes. Artefato
nunca editado NEVER SHALL exibir marca nem valor original. A ficha continua sendo de **leitura**:
NEVER SHALL oferecer à gestão editar, restaurar ou remover artefato. (`RF-02-04`, `RN-02-01`,
`RN-09-14`, decisão do fundador de 2026-09-06)

#### Scenario: O Admin vê o que foi mexido

- **WHEN** o Admin abre a ficha de um Mestre que editou um artefato do cadastro
- **THEN** aquele artefato aparece marcado, com o valor original ao lado do vigente

#### Scenario: Artefato intocado aparece limpo

- **WHEN** a ficha traz um artefato que ninguém editou
- **THEN** ele aparece sem marca e sem valor original

#### Scenario: A gestão continua sem editar

- **WHEN** o Admin percorre a ficha com um artefato editado
- **THEN** não lhe é oferecido editar, restaurar nem remover o artefato
