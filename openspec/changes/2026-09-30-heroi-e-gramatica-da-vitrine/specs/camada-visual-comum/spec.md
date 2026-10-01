# Spec Delta

## ADDED Requirements

### Requirement: O cabeçalho apresenta a marca do projeto, nas oito aplicações

A camada comum SHALL apresentar a **marca do projeto** no cabeçalho das oito
aplicações, servida pelo **próprio domínio** — nunca de domínio de terceiro.

A marca SHALL ter versão que atenda o **modo claro e o escuro** e o uso **sobre a foto
de comunidade**, e o contraste dela SHALL ser medido sobre superfície opaca, como o de
qualquer outro elemento. A marca NEVER SHALL ser a única via ao nome do projeto: o nome
continua em texto no cabeçalho, e quem não vê a imagem lê o nome.

Nenhuma aplicação SHALL servir marca de terceiro: o favicon e o cabeçalho apresentam a
marca do projeto ou nada. (documento 15 §§1, 3.3, 5, 6.3, princípios 3 e 6)

#### Scenario: O cabeçalho apresenta a marca

- **WHEN** qualquer uma das oito aplicações é aberta
- **THEN** o cabeçalho apresenta a marca do projeto, servida pelo próprio domínio

#### Scenario: O nome não depende da imagem

- **WHEN** a marca não carrega
- **THEN** o nome do projeto continua legível em texto no cabeçalho

#### Scenario: A marca atende os dois modos

- **WHEN** a aplicação é apresentada no modo escuro
- **THEN** a marca apresentada é a versão que cumpre o contraste nesse modo

#### Scenario: Nenhuma aplicação serve marca de terceiro

- **WHEN** o favicon de qualquer aplicação é buscado
- **THEN** ele é a marca do projeto, e nunca a de outro produto
