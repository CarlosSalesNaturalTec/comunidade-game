## ADDED Requirements

### Requirement: O Guerreiro(a) tem nick, único em toda a plataforma

O núcleo SHALL exigir **nick** em toda persona de Guerreiro(a), e o nick SHALL ser único em toda
a plataforma — não apenas dentro da comunidade. A unicidade SHALL alcançar o nick de qualquer
persona que o tenha, de modo que um nick de Guerreiro(a) e um de Apoiador NEVER SHALL coincidir.
Persona de Guerreiro(a) NEVER SHALL existir sem nick: é por ele que a criança entra e é por ele
que a família acompanha. (`RF-01-19`, `RN-01-22`, `RN-01-30`)

A rota que cria o Guerreiro(a) e a conferência de unicidade durante a conversa de cadastro são do
PRD-04; aqui nascem o atributo e a invariante que qualquer rota que venha a gravá-lo respeita.

#### Scenario: Guerreiro(a) sem nick não é criado

- **WHEN** uma criação de persona de Guerreiro(a) chega sem nick
- **THEN** o núcleo recusa a criação e nenhuma persona passa a existir

#### Scenario: Nick repetido é recusado

- **WHEN** uma criação de persona chega com nick já usado por outra persona, de qualquer papel
- **THEN** o núcleo recusa a criação, e a persona que já tinha o nick permanece intacta

### Requirement: O núcleo nunca descobre nem sugere um nick

O núcleo SHALL responder a busca por nick **apenas por correspondência exata**. O núcleo NEVER
SHALL expor listagem de nicks, busca parcial, ordenação por semelhança, contagem de resultados
ou sugestão de variação a partir de uma persona autenticada como adulto. A recusa por nick
inexistente NEVER SHALL ser distinguível da recusa por outro motivo. (`RN-01-22`)

A consulta pública por nick exato (`RF-01-33`) e a ausência de busca parcial na vitrine
(`RF-01-34`) são de outra fatia; esta grava a invariante que aquelas rotas herdam.

#### Scenario: Busca por nick é exata

- **WHEN** o núcleo procura uma persona por nick, em qualquer caminho interno ou de rota
- **THEN** a correspondência é exata, e nick parcial não alcança persona alguma

#### Scenario: Não existe rota que liste ou sugira nick

- **WHEN** se procura no núcleo uma rota que liste nicks, complete um nick parcial ou sugira
  variações
- **THEN** nenhuma existe
