# Spec Delta

## MODIFIED Requirements

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

## ADDED Requirements

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
