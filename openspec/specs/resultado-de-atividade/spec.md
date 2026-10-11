## Purpose

O Resultado é o registro de que um Guerreiro(a) realizou uma atividade da trilha — sem ele não
há o que pontuar, o que desbloquear nem o que autorar por trilha ou poder.

## Requirements

### Requirement: Resultado registra quem realizou qual atividade, quando e o quê produziu

O núcleo SHALL registrar, para cada Resultado, o **Guerreiro(a)** que realizou, a **atividade**
realizada, a **aula** em que foi lançado, a **data do fato** (nunca substituída pela do
registro, PRD-01 §9) e o que foi **produzido**, em referência à `producao_esperada` já declarada
na atividade. Resultado sem atividade, sem Guerreiro(a), **sem aula** ou sem produção declarada
SHALL ser recusado com **422**, indicando o campo em falta. A aula é o que liga o resultado às
reservas que a baixa consome (documento 04 §1). (`RF-01-20`, `RF-07-09`, `RF-02-35`, 11 §§2.2, 4)

#### Scenario: Resultado registrado com produção declarada

- **WHEN** chega um Resultado com Guerreiro(a), atividade, aula, data do fato e produção
- **THEN** o núcleo grava o Resultado vinculado àquela atividade, àquele Guerreiro(a) e àquela
  aula

#### Scenario: Resultado sem atividade é recusado

- **WHEN** chega um Resultado sem atividade vinculada
- **THEN** o núcleo responde 422 indicando o campo em falta e nada é gravado

#### Scenario: Resultado sem produção é recusado

- **WHEN** chega um Resultado sem a produção do Guerreiro(a)
- **THEN** o núcleo responde 422 indicando o campo em falta e nada é gravado

#### Scenario: Resultado sem aula é recusado

- **WHEN** chega um Resultado sem a aula em que foi lançado
- **THEN** o núcleo responde 422 indicando o campo em falta e nada é gravado

### Requirement: O lançamento da atividade realizada é ato por aula e converte as reservas em baixa

O núcleo SHALL expor o **lançamento da atividade realizada** como ato **por aula**, de
**Admin**, que registra em uma operação os Resultados de todos os participantes daquela aula.
Na mesma operação, o núcleo SHALL converter **cada reserva** da aula em **baixa**: a reserva
passa a **consumida** e um **lançamento de débito** é gravado, com o tipo de recurso, a
quantidade e o **ponto de apoio da aula**. Não há operação de baixa separada deste ato. A aula
SHALL passar à situação **realizada**. (`RF-07-09`, `RF-02-35`, `RN-07-36`, `RN-07-01`,
`RF-01-16`, `RF-01-03`, documento 04 §1, PRD-07 §5.3)

#### Scenario: Lançamento gera um débito por reserva

- **WHEN** um Admin lança a atividade realizada numa aula com duas reservas
- **THEN** o núcleo grava dois lançamentos de débito, um por reserva, no ponto de apoio da aula,
  e ambas as reservas passam a consumida

#### Scenario: O débito derruba o saldo do ponto de apoio da aula

- **WHEN** a atividade realizada é lançada numa aula que reservou 3 unidades de um tipo
- **THEN** o saldo daquele tipo no ponto de apoio da aula cai em 3

#### Scenario: Lançamento de aula sem reservas apenas registra os resultados

- **WHEN** um Admin lança a atividade realizada numa aula que não declarou recurso algum
- **THEN** o núcleo grava os Resultados, não gera débito algum e a aula passa a realizada

#### Scenario: Mestre não lança a atividade da aula

- **WHEN** um Mestre tenta lançar a atividade realizada de uma aula
- **THEN** o núcleo responde 403 e nada é gravado

### Requirement: O desfecho do Resultado é lançado pela gestão, em três valores fechados

O núcleo SHALL exigir, em todo Resultado, um **desfecho** entre exatamente três valores:
**realizada**, **realizada com mérito** ou **mérito extra por auxílio aos colegas** (11 §4).
Quem lança o desfecho é o **Mestre autor** da trilha a que a atividade pertence, ou um **Admin**
— a mesma matriz de posse que já vale para a trilha, a missão e a atividade (`RF-01-16`). Mestre
que não é o autor SHALL receber **403**. O desfecho SHALL ser gravado com a autoria de quem
lançou (`RN-01-13`).

Na **atividade avulsa**, que não pertence a missão nem a trilha, NÃO há posse de Mestre a
conferir: o lançamento SHALL ser restrito ao **Admin**, e Mestre em sessão SHALL receber **403**
qualquer que seja a trilha de que ele é autor. O crédito do ponto regular SHALL seguir o **poder
declarado** pela atividade, e não uma trilha. (`RF-01-20`, `RF-01-16`, `RF-01-03`, `RF-02-29`,
`RF-02-33`, 11 §4)

#### Scenario: Mestre autor lança desfecho "realizada com mérito"

- **WHEN** o Mestre autor da trilha lança o desfecho "realizada com mérito" para um Resultado
- **THEN** o núcleo grava o desfecho com a autoria, data e hora de quem lançou

#### Scenario: Desfecho fora dos três valores é recusado

- **WHEN** chega um Resultado com desfecho que não é nenhum dos três valores fechados
- **THEN** o núcleo responde 422 e nada é gravado

#### Scenario: Mestre que não é o autor é recusado

- **WHEN** um Mestre que não é o autor da trilha tenta lançar o desfecho de um Resultado dela
- **THEN** o núcleo responde 403 e nada é gravado

#### Scenario: Admin lança o desfecho da atividade avulsa

- **WHEN** um Admin lança o desfecho de um Resultado de atividade avulsa
- **THEN** o núcleo grava o Resultado e credita o ponto regular no poder declarado pela
  atividade

#### Scenario: Mestre não lança atividade avulsa

- **WHEN** um Mestre em sessão tenta lançar o desfecho de um Resultado de atividade avulsa
- **THEN** o núcleo responde 403 e nada é gravado

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

### Requirement: A forma do lançamento segue a modalidade da atividade avulsa

O núcleo SHALL recusar com **422** o lançamento **por equipe** de atividade **avulsa** de
modalidade **individual** e o lançamento **por participante** de atividade **avulsa** de
modalidade **em equipe** ou **em equipe com familiar**. A recusa é da avulsa: o `RN-02-33` é
regra do PRD-02, e o ato por atividade **de trilha**, do Mestre na App 09, segue como está —
a equipe da aula NEVER SHALL ser aceita nele, e a lista de participantes segue valendo
qualquer que seja a modalidade. (`RN-02-33`)

#### Scenario: Atividade individual não se lança por equipe

- **WHEN** um Admin tenta lançar por equipe uma atividade avulsa de modalidade individual
- **THEN** o núcleo responde 422 e nenhum Resultado é gravado

#### Scenario: Atividade em equipe não se lança por participante

- **WHEN** um Admin tenta lançar por lista de participantes uma atividade avulsa de modalidade
  em equipe
- **THEN** o núcleo responde 422 e nenhum Resultado é gravado

#### Scenario: A atividade de trilha não se lança pela equipe da aula

- **WHEN** chega um lançamento declarando a equipe da aula para uma atividade que pertence a
  uma missão
- **THEN** o núcleo responde 422, e a lista de participantes dela segue aceita como antes

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
