## Purpose

O Resultado é o registro de que um Guerreiro(a) realizou uma atividade da trilha — sem ele não
há o que pontuar, o que desbloquear nem o que autorar por trilha ou poder.

## Requirements

### Requirement: Resultado registra quem realizou qual atividade, quando e o quê produziu

O núcleo SHALL registrar, para cada Resultado, o **Guerreiro(a)**, a **atividade**, a **aula**
em que foi lançado, a **data do fato** (PRD-01 §9) e o que foi **produzido**, como o
**comprovante** do Resultado numa das **seis formas** — texto, imagem, áudio, vídeo, arquivo ou
link externo. Faltar atividade, Guerreiro(a), aula ou comprovante SHALL ser recusado com
**422**, indicando o campo. (`RF-01-20`, `RF-07-09`, `RF-02-35`, `RF-09-149`, `RN-09-64`, 11
§§2.2, 4)

#### Scenario: Resultado registrado com produção declarada

- **WHEN** chega um Resultado com Guerreiro(a), atividade, aula, data do fato e produção
- **THEN** o núcleo grava o Resultado vinculado àquela atividade, àquele Guerreiro(a) e àquela
  aula

#### Scenario: Resultado com comprovante em texto

- **WHEN** chega um Resultado com comprovante na forma texto e o corpo escrito
- **THEN** o núcleo grava o Resultado com o comprovante em texto

#### Scenario: Produção em texto simples vale como comprovante em texto

- **WHEN** chega um Resultado com a produção em texto, sem forma de comprovante declarada
- **THEN** o núcleo grava o Resultado com o comprovante em texto, como antes

#### Scenario: Resultado sem atividade é recusado

- **WHEN** chega um Resultado sem atividade vinculada
- **THEN** o núcleo responde 422 indicando o campo em falta e nada é gravado

#### Scenario: Resultado sem produção é recusado

- **WHEN** chega um Resultado sem comprovante e sem produção em texto
- **THEN** o núcleo responde 422 indicando o campo em falta e nada é gravado

#### Scenario: Resultado sem aula é recusado

- **WHEN** chega um Resultado sem a aula em que foi lançado
- **THEN** o núcleo responde 422 indicando o campo em falta e nada é gravado

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

### Requirement: O lançamento dos resultados da aula grava os Resultados sem baixar reserva

O núcleo SHALL expor o lançamento dos **resultados da aula** como ato **por aula**, de
**Admin**, que registra em uma operação os Resultados dos participantes, cada um com a atividade
a que pertence. O ato NEVER SHALL baixar reserva nem mudar a situação da aula: a baixa e a
passagem a realizada são do sistema, no fim do horário. O ato SHALL ser aceito durante e depois
da aula, e SHALL ser recusado com **422** só na aula **cancelada**; o Resultado repetido segue
recusado pela regra que já o recusa. (`RF-02-33`, `RF-02-35`, `RN-07-43`, `RF-01-16`,
`RF-01-03`)

#### Scenario: O lançamento grava os resultados sem baixar nada

- **WHEN** um Admin lança os resultados numa aula confirmada com duas reservas
- **THEN** o núcleo grava os Resultados, nenhum débito é gravado, as reservas seguem reservadas
  e a aula segue confirmada

#### Scenario: O lançamento é aceito depois do fim da aula

- **WHEN** um Admin lança os resultados de uma aula já realizada
- **THEN** o núcleo grava os Resultados

#### Scenario: Aula cancelada recusa o lançamento

- **WHEN** chega o lançamento de resultados de uma aula cancelada
- **THEN** o núcleo responde 422 e nada é gravado

#### Scenario: Mestre não lança pela aula

- **WHEN** um Mestre tenta lançar os resultados pela rota da aula
- **THEN** o núcleo responde 403 e nada é gravado

### Requirement: O comprovante em mídia sobe antes do lançamento

Comprovante em **imagem**, **áudio**, **vídeo** ou **arquivo** SHALL subir por **sessão de
envio retomável** aberta pelo Mestre autor ou pelo Admin **antes** do lançamento, que o
referencia. O lançamento SHALL ser recusado com **422** se o envio não concluiu ou se é de outra
persona. Valem a **mesma lista fechada de tipos** e os **mesmos tetos** da criação original
(**413** acima do teto). Texto e link vão no próprio lançamento. (`RF-09-149`, `RN-09-64`,
`RF-01-78`)

#### Scenario: Comprovante em foto entra pelo envio prévio

- **WHEN** o Mestre autor abre o envio de uma foto, conclui o envio e lança o Resultado
  referenciando-o
- **THEN** o núcleo grava o Resultado com o comprovante em imagem, com o tamanho e o tipo reais
  do arquivo

#### Scenario: Envio não concluído é recusado

- **WHEN** o lançamento referencia um envio que ainda não terminou
- **THEN** o núcleo responde **422** dizendo que o envio do comprovante não terminou, e nenhum
  Resultado é gravado

#### Scenario: Envio aberto por outra persona é recusado

- **WHEN** o lançamento referencia um envio aberto por outro Mestre
- **THEN** o núcleo responde **422** e nenhum Resultado é gravado

#### Scenario: Tipo fora da lista e tamanho acima do teto são recusados

- **WHEN** o envio do comprovante declara tipo fora da lista fechada, ou tamanho acima do teto
  do tipo
- **THEN** o núcleo responde **422** ou **413**, e nenhum byte é aceito

#### Scenario: Mídia escrita no corpo é recusada

- **WHEN** o lançamento declara comprovante em vídeo e manda o corpo escrito em vez do envio
- **THEN** o núcleo responde **422** dizendo que aquele comprovante vai pelo envio do arquivo

### Requirement: O lançamento traz o julgamento do prático da missão quando ele não foi cumprido

Quando a missão da atividade tem desafio **prático** que o Guerreiro(a) ainda **não cumpriu**,
o lançamento dele **pelo ato por atividade** SHALL trazer o **julgamento** — cumpriu, publicável e motivo —, sob pena de
**422**. Julgamento onde não há o que julgar — quiz, sem desafio, avulsa ou prático cumprido —
SHALL ser recusado com **422**. Resultado e julgamento SHALL ser gravados **na mesma
transação**. (`RF-09-150`, `RN-09-65`, `RF-09-133`)

#### Scenario: Lançamento sem o julgamento exigido é recusado

- **WHEN** o Mestre autor lança a atividade de uma missão com prático que o Guerreiro(a) não
  cumpriu, sem o julgamento
- **THEN** o núcleo responde **422** nomeando o julgamento como o que falta, e nada é gravado

#### Scenario: Julgamento onde não há prático a julgar é recusado

- **WHEN** o lançamento traz julgamento numa atividade cuja missão tem desafio em quiz, ou cujo
  prático o Guerreiro(a) já cumpriu
- **THEN** o núcleo responde **422** e nada é gravado

#### Scenario: Sem prático pendente, o lançamento segue sem julgamento

- **WHEN** o Mestre autor lança uma atividade cuja missão não tem desafio prático pendente para
  o Guerreiro(a)
- **THEN** o núcleo grava o Resultado sem pedir julgamento

#### Scenario: Julgamento recusado não grava o Resultado

- **WHEN** o lançamento traz julgamento negativo sem motivo
- **THEN** o núcleo responde **422** pelo motivo, e nem o Resultado nem o julgamento são gravados

#### Scenario: Cumpriu credita o Resultado e os 5 pontos no mesmo ato

- **WHEN** o lançamento traz o julgamento de que o Guerreiro(a) cumpriu
- **THEN** o núcleo grava o Resultado com a pontuação dele e credita os 5 pontos do prático, e a
  missão seguinte se abre

### Requirement: O Mestre autor e o Admin leem os resultados lançados numa aula

O núcleo SHALL servir os **Resultados de uma aula** — Guerreiro(a) por nick, atividade,
desfecho, momento do fato e o comprovante: a forma, o texto ou o endereço, e se há arquivo. O
**Mestre autor** SHALL ver só os das atividades de que é autor; o **Admin** vê todos. Outro
papel SHALL receber **403**. Os **bytes** do comprovante em mídia SHALL ser servidos aos mesmos
dois, com **404** para comprovante sem arquivo. (`RF-09-151`, `RN-09-18`)

#### Scenario: O Mestre autor vê os resultados das atividades dele

- **WHEN** o Mestre autor pede os resultados de uma aula em que ele e outro Mestre lançaram
- **THEN** o núcleo devolve só os Resultados das atividades dele, com o comprovante de cada um

#### Scenario: O Mestre autor abre a foto do comprovante

- **WHEN** o Mestre autor pede os bytes do comprovante em imagem de um Resultado da atividade
  dele
- **THEN** o núcleo devolve os bytes, com o tipo do arquivo guardado

#### Scenario: Quem não é autor nem Admin é recusado

- **WHEN** um Guerreiro(a), ou um Mestre que não é o autor da atividade, pede os bytes do
  comprovante
- **THEN** o núcleo responde **403** e nenhum byte é servido

#### Scenario: Comprovante sem arquivo responde 404

- **WHEN** se pedem os bytes de um comprovante em texto ou link
- **THEN** o núcleo responde **404**
