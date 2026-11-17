## ADDED Requirements

### Requirement: Adulto desativado não aparece na vitrine

As leituras públicas de Mestres e de Apoiadores — listagem e leitura por identificador — SHALL
omitir o adulto **desativado** pela gestão; a leitura por identificador SHALL responder
como a de identificador inexistente. Reativado, ele volta pelas mesmas regras de antes.
(`RF-02-119`, `RN-02-35`)

#### Scenario: Desativado some da listagem

- **WHEN** a vitrine lista os Apoiadores e um deles está desativado
- **THEN** ele não aparece na página, e a paginação não o conta

#### Scenario: Página individual do desativado

- **WHEN** alguém abre a página de um Mestre desativado
- **THEN** o núcleo responde como a um identificador inexistente
