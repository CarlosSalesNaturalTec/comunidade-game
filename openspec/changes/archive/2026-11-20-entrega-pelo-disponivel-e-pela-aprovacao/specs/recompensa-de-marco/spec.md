## MODIFIED Requirements

### Requirement: O lastro é reverificado no ato da entrega

O núcleo SHALL conferir o lastro **no ato da entrega**, contra o **disponível** do tipo no ponto
de apoio de onde o recurso sai — o saldo menos o que está reservado para aula ou desafio extra
—, e não na declaração do marco nem na publicação da trilha, porque a trilha é bem comum e o
saldo é de um ponto de apoio. A recompensa de marco NEVER SHALL reservar saldo. (`RF-07-13`,
`RN-07-01`, `RN-07-42`, `RN-09-27`, invariante 9, 02 §8.1)

#### Scenario: Lastro é reverificado no ato da entrega

- **WHEN** um Mestre confirma a entrega de uma recompensa de quantidade 1 num ponto de apoio
  cujo saldo disponível daquele tipo é zero
- **THEN** o núcleo responde 422 dizendo que falta lastro, e nada é gravado

#### Scenario: O saldo reservado não lastreia a entrega

- **WHEN** o ponto de apoio tem saldo 3 de um tipo, todo reservado para um desafio extra, e o
  Mestre confirma a entrega de uma recompensa daquele tipo
- **THEN** o núcleo responde 422 dizendo que falta lastro, e nada é gravado

## ADDED Requirements

### Requirement: Fora do encontro, a entrega sai do ponto de apoio da aula anterior

Sem aula declarada, o núcleo SHALL tirar o recurso do ponto de apoio da **aula imediatamente
anterior** da comunidade do Guerreiro(a): a de início mais recente até o momento da entrega,
não cancelada — o que inclui a aula em andamento. O Mestre NEVER SHALL escolher o ponto de
apoio, e a entrada que o declare SHALL ser recusada com **422**. Comunidade sem aula anterior
SHALL ter a entrega recusada com **422**, dizendo que não há aula de onde o recurso saia.
(`RF-09-76`, `RF-07-13`, 02 §8.1)

#### Scenario: A entrega fora do encontro baixa do ponto da aula anterior

- **WHEN** o Mestre confirma, sem declarar aula, a entrega a um Guerreiro(a) cuja comunidade teve
  aula ontem no Centro comunitário
- **THEN** o núcleo grava a entrega e o débito no Centro comunitário

#### Scenario: O ponto de apoio declarado é recusado

- **WHEN** a entrada da entrega traz o ponto de apoio
- **THEN** o núcleo responde 422 e nada é gravado

#### Scenario: Comunidade sem aula anterior não recebe a entrega

- **WHEN** o Mestre confirma a entrega a um Guerreiro(a) de comunidade que nunca teve aula
- **THEN** o núcleo responde 422 e nada é gravado

### Requirement: A aprovação do prático entrega a recompensa

Julgado que o Guerreiro(a) **cumpriu** o desafio prático, o núcleo SHALL entregar, no mesmo ato,
cada recompensa de marco da trilha cujo marco aquele julgamento alcançou e que o Guerreiro(a)
ainda não recebeu — com a baixa, a mesma conferência e o mesmo ponto de apoio da entrega fora do
encontro —, desde que quem julga seja **Mestre vinculado à comunidade** do Guerreiro(a) e haja
lastro. Faltando qualquer condição, a aprovação SHALL valer igual — a missão seguinte abre e os
pontos são creditados — e a entrega SHALL ficar na fila de entregas pendentes. A resposta do
julgamento SHALL dizer quais recompensas foram entregues. (`RF-09-146`, `RN-09-63`, `RN-07-44`)

#### Scenario: Mestre da comunidade aprova e entrega

- **WHEN** o Mestre autor, vinculado à comunidade do Guerreiro(a), julga cumprido o prático que
  alcança um marco com recompensa, havendo lastro
- **THEN** a entrega é gravada com o débito no mesmo ato, e a pendência não aparece na fila

#### Scenario: Sem lastro, a aprovação vale e a entrega fica pendente

- **WHEN** o Mestre julga cumprido o prático que alcança o marco, sem disponível no ponto de apoio
- **THEN** a missão seguinte abre, nenhuma entrega é gravada, e a pendência aparece na fila

#### Scenario: Quem julga sem vínculo com a comunidade não entrega

- **WHEN** o Mestre autor da trilha, sem vínculo com a comunidade do Guerreiro(a), julga cumprido
  o prático que alcança o marco
- **THEN** nenhuma entrega é gravada, e a pendência aparece na fila do Mestre vinculado
