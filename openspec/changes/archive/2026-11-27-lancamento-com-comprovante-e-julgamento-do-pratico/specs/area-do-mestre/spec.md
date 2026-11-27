# Spec Delta

## REMOVED Requirements

### Requirement: O Mestre lança a atividade que propôs pela aplicação

**Reason**: decisão do fundador de 2026-11-27 — a App 09 passa a lançar um Guerreiro(a) por
envio, num formulário da tela da aula, com comprovante e julgamento do prático (`RF-09-74`
revisto, `RF-09-148`).
**Migration**: substituído por "O Mestre lança o resultado de uma atividade na tela da aula";
a API segue aceitando a lista de participantes, usada pela App 03.

## ADDED Requirements

### Requirement: O Mestre lança o resultado de uma atividade na tela da aula

A App 09 SHALL lançar a atividade do Mestre **na tela da aula**, num formulário no molde da
ocorrência de conduta: atividade numa **lista de seleção**, Guerreiro(a) **pelo nick**,
comprovante, momento do fato e **desfecho** entre os três valores, **um Guerreiro(a) por
envio**. NEVER SHALL listar as atividades com botão ao lado, nem pedir identificador técnico.
Recusa em linguagem simples (`RN-09-16`). (`RF-09-43`, `RF-09-44`, `RF-09-148`, `RF-09-49`,
`RN-09-18`)

#### Scenario: O Mestre lança o resultado de um Guerreiro(a)

- **WHEN** o Mestre escolhe a atividade na lista, digita o nick, anexa o comprovante, informa o
  momento e o desfecho e envia
- **THEN** a aplicação envia o lançamento daquele Guerreiro(a), confirma o registro e limpa o
  nick, o comprovante e o julgamento, mantendo a atividade escolhida

#### Scenario: Nick não encontrado é recusado na tela

- **WHEN** o Mestre envia com um nick que não está entre os Guerreiros e Guerreiras ativos das
  comunidades dele
- **THEN** a aplicação diz em linguagem simples que não encontrou o nick, sem enviar ao núcleo

#### Scenario: Sem atividade escolhida o envio é recusado na tela

- **WHEN** o Mestre envia sem escolher a atividade
- **THEN** a aplicação pede a atividade, sem enviar ao núcleo

#### Scenario: A recusa chega em linguagem simples

- **WHEN** o núcleo recusa o lançamento
- **THEN** a aplicação mostra o que impediu em linguagem simples, sem código nem jargão

### Requirement: O lançamento anexa o comprovante numa das seis formas

O formulário SHALL pedir a **forma** do comprovante — texto, imagem, áudio, vídeo, arquivo ou
link externo — e, conforme ela, o texto, o endereço ou o arquivo, que SHALL subir antes do
envio do lançamento. Sem comprovante, o envio SHALL ser recusado na tela. Falha do envio do
arquivo SHALL ser dita em linguagem simples, sem lançar. A tela SHALL exibir o aviso de coleta
do comprovante. (`RF-09-149`, `RN-09-64`, `RN-09-16`)

#### Scenario: O Mestre anexa uma foto

- **WHEN** o Mestre escolhe a forma imagem, seleciona a foto e envia o lançamento
- **THEN** a aplicação sobe a foto, lança o Resultado referenciando-a e confirma o registro

#### Scenario: Sem comprovante o envio é recusado na tela

- **WHEN** o Mestre envia o lançamento sem texto, endereço ou arquivo do comprovante
- **THEN** a aplicação pede o comprovante, sem enviar ao núcleo

### Requirement: O lançamento pede o julgamento do prático quando ele é exigido

Escolhidos a atividade e o nick, a App 09 SHALL consultar a situação do prático da missão e,
quando o julgamento é **exigido**, apresentar o critério de aceite, a forma aceita, a entrega
do Guerreiro(a) se houver, e os campos **cumpriu**, **publicável** e **motivo**. Sem prático
pendente, os campos NEVER SHALL aparecer. (`RF-09-150`, `RN-09-65`, `RN-09-66`, `RF-09-133`,
`RF-09-134`)

#### Scenario: Prático pendente abre o julgamento no formulário

- **WHEN** o Mestre escolhe uma atividade cuja missão tem prático que o Guerreiro(a) ainda não
  cumpriu
- **THEN** a aplicação mostra o critério de aceite, a forma aceita, a entrega do Guerreiro(a)
  quando houver, e os campos do julgamento

#### Scenario: Sem declaração, a tela avisa que o comprovante vira a comprovação

- **WHEN** o julgamento é exigido e o Guerreiro(a) não declarou o prático
- **THEN** a aplicação diz que o comprovante do lançamento será a comprovação do prático e que
  ele precisa estar na forma aceita

#### Scenario: Prático cumprido não mostra julgamento

- **WHEN** o Mestre escolhe uma atividade cuja missão não tem prático pendente para aquele
  Guerreiro(a)
- **THEN** a aplicação não mostra os campos do julgamento

### Requirement: A tela da aula lista os resultados lançados nela

A tela da aula SHALL listar os **resultados lançados nesta aula** nas atividades do Mestre —
nick, atividade, desfecho e o comprovante: o texto, o endereço, ou o arquivo aberto a pedido.
Lista vazia e falha da leitura SHALL ser ditas em linguagem simples, sem travar o formulário; a
lista SHALL se atualizar depois de cada lançamento. (`RF-09-151`, `RN-09-18`, `RN-09-16`)

#### Scenario: O Mestre vê o que lançou

- **WHEN** o Mestre lança o resultado de um Guerreiro(a)
- **THEN** a lista dos lançados nesta aula passa a mostrá-lo, com o comprovante

#### Scenario: O Mestre abre o comprovante em mídia

- **WHEN** o Mestre pede para abrir o comprovante em vídeo de um lançamento
- **THEN** a aplicação busca os bytes e os apresenta
