## ADDED Requirements

### Requirement: Adulto desativado não abre sessão

O núcleo SHALL recusar a abertura de sessão de Mestre ou Apoiador **desativado** pela gestão,
por login social ou por usuário e senha, com a mesma resposta dada a login sem cadastro
correspondente, e NEVER SHALL criar persona nem reativar a existente por causa da tentativa.
(`RF-02-119`, `RN-02-35`, invariante 3 do documento 99 §6)

#### Scenario: Login do desativado é recusado

- **WHEN** um Apoiador desativado tenta entrar pelo login social
- **THEN** o núcleo recusa a sessão e a persona segue desativada
