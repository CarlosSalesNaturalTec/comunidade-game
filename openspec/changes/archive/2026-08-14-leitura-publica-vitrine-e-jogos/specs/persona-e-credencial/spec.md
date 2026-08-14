## ADDED Requirements

### Requirement: O Guerreiro(a) tem avatar, e é por ele que aparece em público

O núcleo SHALL guardar, em toda persona de Guerreiro(a), as **características do avatar** — a
representação pública dele, ao lado do nick. O avatar SHALL ser o **único** retrato do
Guerreiro(a) em qualquer superfície pública: a imagem do onboarding NEVER SHALL virar avatar,
nem ser exibida em lugar algum. (`RN-01-10`, `RN-01-15`, invariante 12 do documento 99 §6)

A rota que grava o avatar no cadastro é do PRD-04 (`RF-04-07`) e a que permite ao Guerreiro(a)
alterá-lo é do PRD-05 (`RF-05-51`); aqui nascem o atributo e a invariante que qualquer rota que
venha a gravá-lo respeita — a mesma divisão já aplicada ao nick.

#### Scenario: A persona de Guerreiro(a) carrega o avatar

- **WHEN** uma persona de Guerreiro(a) existe no núcleo
- **THEN** ela carrega as características do avatar dela

#### Scenario: A imagem do onboarding não vira avatar

- **WHEN** o _template_ biométrico de um Guerreiro(a) é gravado
- **THEN** nenhum avatar é derivado dele, e a imagem continua sem ser exibida em lugar algum

#### Scenario: O avatar é o que a superfície pública exibe

- **WHEN** uma superfície pública precisa retratar um Guerreiro(a)
- **THEN** ela usa o avatar e o nick, e nenhum outro retrato existe para ela usar
