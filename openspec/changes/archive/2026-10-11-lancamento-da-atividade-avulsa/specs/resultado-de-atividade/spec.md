# Spec Delta

## ADDED Requirements

### Requirement: O Admin lança o resultado da atividade avulsa pelo ato por atividade

O núcleo SHALL aceitar do **Admin** o lançamento de uma **atividade avulsa**, declarando a aula
em que aconteceu, pelo mesmo ato **por atividade** que já serve o Mestre autor. O ato NEVER
SHALL converter reserva em baixa nem alterar a situação da aula, e por isso SHALL poder correr
**mais de uma vez** na mesma aula. Mestre em sessão SHALL receber **403**, qualquer que seja a
trilha de que é autor. (`RF-02-112`, `RF-02-29`, `RF-01-16`)

#### Scenario: Admin lança a avulsa sem mexer na aula

- **WHEN** um Admin lança uma atividade avulsa numa aula que tem reservas de recurso
- **THEN** os Resultados são gravados, as reservas permanecem como estão e a situação da aula
  não é alterada

#### Scenario: A avulsa é lançada duas vezes na mesma aula

- **WHEN** um Admin lança duas atividades avulsas diferentes na mesma aula
- **THEN** os dois lançamentos são gravados, sem que o segundo seja recusado

#### Scenario: Mestre não lança a avulsa pelo ato por atividade

- **WHEN** um Mestre em sessão tenta lançar uma atividade avulsa
- **THEN** o núcleo responde 403 e nenhum Resultado é gravado

#### Scenario: Atividade avulsa sem missão não derruba o lançamento

- **WHEN** chega o lançamento de uma atividade que não pertence a missão alguma
- **THEN** o núcleo o processa pela conferência de Admin, sem erro de servidor

### Requirement: O lançamento por equipe gera um Resultado por integrante, integral a cada um

O núcleo SHALL aceitar a **equipe da aula** como alternativa à lista de participantes. O
desfecho e a produção declarados SHALL ser **da equipe** e SHALL gerar um Resultado por
integrante, com o mesmo desfecho, a mesma produção e o valor do motor **integral a cada um** —
dividir puniria a colaboração (documento 11 §4). (`RF-02-112`, `RF-02-33`, `RN-02-32`)

#### Scenario: Os três integrantes presentes recebem o mesmo desfecho

- **WHEN** um Admin lança por equipe, com desfecho "realizada", uma avulsa de equipe com três
  integrantes presentes
- **THEN** o núcleo grava três Resultados com o mesmo desfecho e a mesma produção, e credita o
  valor integral a cada um

#### Scenario: Lançamento sem equipe e sem participantes é recusado

- **WHEN** chega um lançamento que não declara equipe nem lista de participantes
- **THEN** o núcleo responde 422 e nada é gravado

#### Scenario: Lançamento com equipe e participantes ao mesmo tempo é recusado

- **WHEN** chega um lançamento declarando a equipe e a lista de participantes
- **THEN** o núcleo responde 422 e nada é gravado

### Requirement: Integrante sem presença e quem não é Guerreiro(a) ficam fora do lançamento por equipe

Integrante **sem presença não anulada** naquela aula SHALL ser **pulado**, e o núcleo SHALL
informar quem ficou de fora. Integrante que não é **Guerreiro(a)** — o familiar da modalidade em
equipe com familiar — NEVER SHALL receber Resultado. (`RN-02-32`)

#### Scenario: Integrante sem presença é pulado

- **WHEN** um Admin lança por equipe uma equipe de quatro em que um integrante não tem presença
  naquela aula
- **THEN** o núcleo grava três Resultados e informa que aquele integrante ficou de fora

#### Scenario: Presença anulada não conta como presença

- **WHEN** um integrante da equipe tem a presença daquela aula anulada
- **THEN** o núcleo o trata como ausente e não grava Resultado para ele

#### Scenario: O familiar não recebe Resultado

- **WHEN** um Admin lança por equipe uma avulsa de modalidade em equipe com familiar, cuja
  equipe tem dois Guerreiros e um integrante de 17 anos ou mais
- **THEN** o núcleo grava dois Resultados, um por Guerreiro(a), com 20 pontos regulares cada, e
  nenhum para o familiar

### Requirement: A forma do lançamento segue a modalidade da atividade

O núcleo SHALL recusar com **422** o lançamento **por equipe** de atividade de modalidade
**individual** e o lançamento **por participante** de atividade de modalidade **em equipe** ou
**em equipe com familiar**. (`RN-02-33`)

#### Scenario: Atividade individual não se lança por equipe

- **WHEN** um Admin tenta lançar por equipe uma atividade avulsa de modalidade individual
- **THEN** o núcleo responde 422 e nenhum Resultado é gravado

#### Scenario: Atividade em equipe não se lança por participante

- **WHEN** um Admin tenta lançar por lista de participantes uma atividade avulsa de modalidade
  em equipe
- **THEN** o núcleo responde 422 e nenhum Resultado é gravado

### Requirement: O lançamento da avulsa recusa a equipe sem presentes e o Resultado repetido

O lançamento por equipe em que **nenhum** integrante tem presença SHALL ser recusado com
**422**: lançamento vazio é erro de operação, não resultado. O **segundo Resultado do mesmo par
(Guerreiro(a), atividade)** SHALL ser recusado com **422** — o ato roda várias vezes e o
Resultado não se edita nem se remove, então sem a guarda o ponto dobraria em silêncio.
(`RN-02-33`)

#### Scenario: Equipe sem nenhum presente recusa o lançamento

- **WHEN** um Admin lança por equipe uma equipe cujos integrantes nenhum tem presença naquela
  aula
- **THEN** o núcleo responde 422 e nenhum Resultado é gravado

#### Scenario: O mesmo Guerreiro(a) não recebe dois Resultados da mesma atividade

- **WHEN** chega um lançamento para um Guerreiro(a) que já tem Resultado naquela atividade
- **THEN** o núcleo responde 422 e nada é gravado, nem para os outros participantes da lista
