# Spec Delta

## ADDED Requirements

### Requirement: A abertura tem herói, com ilustração em primeiro plano

A abertura da vitrine SHALL apresentar, antes das seções, um **herói** com a ilustração
do projeto em primeiro plano, a frase que diz o que o projeto é, e as ações que a
vitrine já oferece — "Entrar" e "Quero participar". NEVER SHALL oferecer ação que a
vitrine não tenha em outra tela.

O que o herói comunica NEVER SHALL depender da ilustração: some a ilustração — rede
fora, preferência do aparelho —, e a frase e as ações continuam de pé. A ilustração
NEVER SHALL entrar no caminho crítico da tela nem exigir recurso de domínio de terceiro.
(documento 15 §§1, 6; `RF-03-01`, `RF-03-51`, `RF-03-58`, `RN-03-21`)

#### Scenario: A abertura apresenta o herói antes das seções

- **WHEN** a raiz do domínio é aberta
- **THEN** o herói aparece antes da primeira seção, com a frase do projeto e as duas
  ações

#### Scenario: Sem a ilustração, a abertura continua inteira

- **WHEN** a ilustração do herói não carrega
- **THEN** a frase e as duas ações continuam visíveis e acionáveis

#### Scenario: O herói não oferece ação que a vitrine não tenha

- **WHEN** o herói é apresentado
- **THEN** as ações dele são as mesmas que a vitrine oferece em outra tela, e nenhuma
  outra

#### Scenario: O herói não busca recurso de terceiro

- **WHEN** a abertura é servida
- **THEN** nenhuma requisição sai para domínio que não seja o próprio
