## Purpose

O cuidado com o bem recebido no encontro presencial: a validação da conservação da recompensa
de marco entregue, a fila do Mestre da aula e a regra de que cada bem pontua uma vez por
encontro, pela conservação ou pela customização.

## ADDED Requirements

### Requirement: O Mestre da aula valida a conservação do bem recebido

O núcleo SHALL aceitar, de **Mestre vinculado à comunidade da aula** informada, a validação da
**conservação** de um **bem recebido** — uma **recompensa de marco entregue** ao Guerreiro(a) —
de Guerreiro(a) com **presença registrada e não anulada** naquela aula, creditando **1 ponto
extra** e nenhum ponto regular. Item do catálogo avulso NEVER SHALL ser validado como bem
recebido. Persona que não é Mestre, ou Mestre de outra comunidade, SHALL receber **403**;
entrega que não é daquele Guerreiro(a), ou Guerreiro(a) sem presença na aula, SHALL ser recusada
com **422**. A validação SHALL gravar o Mestre, o papel e a data e hora com fuso. (`RF-01-87`,
`RF-09-113`, `RF-04-84`, documento 11 §5)

#### Scenario: A conservação validada credita 1 extra

- **WHEN** o Mestre da aula valida a conservação do livro entregue a um Guerreiro(a) presente
- **THEN** o núcleo credita 1 ponto extra no acumulado e no saldo disponível dele, e nenhum ponto
  regular

#### Scenario: Entrega de outro Guerreiro(a) é recusada

- **WHEN** o Mestre valida, para um Guerreiro(a), uma entrega de recompensa feita a outro
- **THEN** o núcleo responde **422**, e nada é creditado

#### Scenario: Sem presença na aula, sem validação

- **WHEN** o Mestre valida a conservação de Guerreiro(a) sem presença registrada naquela aula
- **THEN** o núcleo responde **422**, e nada é creditado

#### Scenario: Quem não é Mestre não valida

- **WHEN** um Admin ou um Guerreiro(a) tenta validar a conservação
- **THEN** o núcleo responde **403**, e nada é creditado

### Requirement: Cada bem pontua uma vez por encontro, pela conservação ou pela customização

O mesmo bem recebido SHALL render **no máximo uma** pontuação por aula: a validação da
conservação ou a aprovação da customização dele, **nunca as duas**, e nenhuma delas duas vezes.
A segunda tentativa no mesmo encontro SHALL ser recusada com **422**, dizendo por qual caminho o
bem já pontuou, e a regra SHALL valer também no banco, em qualquer via. Bens diferentes no mesmo
encontro, e o mesmo bem em encontros diferentes, pontuam cada um. Tratar o robô montado como um
bem só é escolha do Mestre da aula, ao validar um dos kits; o núcleo não agrupa entregas.
(`RN-01-66`, `RN-09-62`, documento 11 §5)

#### Scenario: Conservação depois da customização é recusada

- **WHEN** o Mestre aprovou a customização de um kit numa aula e tenta validar a conservação do
  mesmo kit na mesma aula
- **THEN** o núcleo responde **422** dizendo que o kit já pontuou pela customização, e nada é
  creditado

#### Scenario: Customização depois da conservação é recusada

- **WHEN** o Mestre validou a conservação de um kit numa aula e tenta aprovar a customização do
  mesmo kit na mesma aula
- **THEN** o núcleo responde **422**, e o registro segue pendente

#### Scenario: A mesma conservação não pontua duas vezes

- **WHEN** o Mestre valida duas vezes a conservação do mesmo livro na mesma aula
- **THEN** a segunda é recusada com **422**, e só 1 ponto extra foi creditado

#### Scenario: Outro encontro pontua de novo

- **WHEN** o Mestre valida a conservação do mesmo livro na aula seguinte
- **THEN** o núcleo credita 1 ponto extra de novo

#### Scenario: Três bens no mesmo encontro somam três

- **WHEN** o Mestre valida, na mesma aula, a conservação do livro, da camisa e do kit de um
  Guerreiro(a)
- **THEN** o núcleo credita 3 pontos extras, um por bem

### Requirement: O Mestre da aula lê a fila do cuidado no encontro

O núcleo SHALL devolver a **Mestre vinculado à comunidade da aula** a fila do encontro: cada
Guerreiro(a) com **presença registrada e não anulada** naquela aula, com nick e avatar, e os
**bens recebidos** dele — cada um com o tipo de recurso, a trilha, se **já pontuou** naquela aula
e por qual caminho, se a **customização está aberta**, o **registro pendente**, quando houver, e
o **último registro aprovado** do kit. Quem não tem presença na aula NEVER SHALL aparecer.
Persona que não é Mestre, ou Mestre de outra comunidade, SHALL receber **403**; aula sem ninguém
presente devolve fila vazia, nunca erro. (`RF-04-81`, `RF-04-84`)

#### Scenario: A fila traz os presentes e os bens deles

- **WHEN** o Mestre da aula lê a fila do encontro
- **THEN** o núcleo devolve cada Guerreiro(a) presente com os bens recebidos, o que já pontuou
  naquela aula, o registro pendente e o último aprovado de cada kit aberto

#### Scenario: Quem não registrou presença fica fora

- **WHEN** um Guerreiro(a) da comunidade tem registro pendente mas não registrou presença na aula
- **THEN** ele não aparece na fila daquele encontro

#### Scenario: Mestre de outra comunidade não lê a fila

- **WHEN** um Mestre pede a fila de uma aula de comunidade a que ele não está vinculado
- **THEN** o núcleo responde **403**
