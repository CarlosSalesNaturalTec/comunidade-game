## ADDED Requirements

### Requirement: O Mestre autor lança a atividade que propôs, com todos os participantes num ato

O núcleo SHALL aceitar do **Mestre autor** da trilha o lançamento de uma **atividade** dele,
declarando a aula em que aconteceu e a **lista de participantes** — cada um com o Guerreiro(a),
o momento do fato, a produção e o desfecho. Os Resultados SHALL ser gravados **numa operação
só**, o que atende o lançamento da equipe inteira de uma vez sem repetir a chamada por
integrante (`RF-09-74`).

O ato é **por atividade** e NEVER SHALL converter reserva em baixa nem alterar a situação da
aula: essas são consequências do lançamento **por aula**, do Admin, que permanece inalterado
(`RF-02-33`, `RF-02-35`).

Mestre que não é o autor da trilha da atividade SHALL receber **403**, pela mesma conferência
de posse que já vale para a trilha, a missão e a atividade (`RN-09-08`). (`RF-09-43`,
`RF-09-44`, `RF-09-49`, `RF-09-74`, `RF-01-16`, `RF-01-20`)

#### Scenario: O Mestre autor lança a atividade com vários participantes

- **WHEN** o Mestre autor lança uma atividade sua com quatro participantes e o desfecho de cada
  um
- **THEN** o núcleo grava os quatro Resultados numa operação só, com a autoria dele, e credita
  a pontuação de cada um

#### Scenario: O lançamento por atividade não mexe na aula nem nas reservas

- **WHEN** o Mestre autor lança uma atividade de uma aula que tem reservas de recurso
- **THEN** as reservas permanecem como estão e a situação da aula não é alterada

#### Scenario: Mestre que não é o autor é recusado

- **WHEN** um Mestre que não é o autor da trilha tenta lançar uma atividade dela
- **THEN** o núcleo responde 403 e nenhum Resultado é gravado

#### Scenario: Um participante inválido recusa o lançamento inteiro

- **WHEN** chega um lançamento em que um dos participantes tem desfecho fora dos três valores
  fechados
- **THEN** o núcleo responde 422 e nenhum dos Resultados da lista é gravado

### Requirement: O lançamento gravado não se edita

O núcleo NEVER SHALL oferecer caminho de edição ou remoção de um Resultado já gravado. A
tentativa de editar um lançamento SHALL ser recusada com **405**. (`RF-09-47`, `RF-09-43`)

#### Scenario: Tentativa de editar lançamento é recusada

- **WHEN** chega uma requisição que tenta alterar um Resultado já gravado
- **THEN** o núcleo responde 405 e o Resultado permanece como está
