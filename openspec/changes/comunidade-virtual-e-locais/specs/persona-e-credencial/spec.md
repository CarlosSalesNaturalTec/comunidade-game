## MODIFIED Requirements

### Requirement: Guerreiro(a) tem vínculo obrigatório a exatamente uma comunidade

O núcleo SHALL exigir que toda persona de Guerreiro(a) tenha vínculo a **exatamente uma**
Comunidade Virtual. A persona de Guerreiro(a) NEVER SHALL existir sem comunidade nem com mais de
uma vigente. (`RN-01-05`)

O vínculo NEVER SHALL ser atributo da persona: ele vive na entidade própria da capacidade
`comunidade-virtual`, com data de início, data de fim e histórico, e a comunidade vem da
**aula agendada** em que o Guerreiro(a) se cadastra, nunca de quem o cadastra (`RF-08-02`,
`RN-08-02`).

O comportamento da Comunidade Virtual — criação, hierarquia de locais, transferência — é do
PRD-08 (`RF-01-23`).

#### Scenario: Guerreiro(a) sem comunidade não é criado

- **WHEN** uma criação de persona de Guerreiro(a) chega sem comunidade
- **THEN** o núcleo recusa a criação

#### Scenario: Segundo vínculo vigente é recusado

- **WHEN** um segundo vínculo de comunidade vigente é pedido para o mesmo Guerreiro(a)
- **THEN** o núcleo recusa, e o vínculo existente permanece

#### Scenario: A comunidade do Guerreiro(a) continua consultável pelo vínculo vigente

- **WHEN** se consulta a comunidade de um Guerreiro(a) já cadastrado
- **THEN** o núcleo a resolve pelo vínculo vigente, e o resultado é o mesmo de antes da
  mudança
