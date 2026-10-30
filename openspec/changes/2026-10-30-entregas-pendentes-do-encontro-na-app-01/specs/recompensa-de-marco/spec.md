# Spec Delta

## ADDED Requirements

### Requirement: A fila de entregas pendentes aceita o recorte por aula

O núcleo SHALL aceitar, na fila de entregas pendentes do Mestre, o recorte por **aula**: pedida
assim, a fila SHALL alcançar somente os Guerreiros e Guerreiras com **presença registrada e não
anulada** naquela aula, e não a comunidade inteira. Sem o recorte, a fila segue alcançando as
comunidades do Mestre. A aula SHALL pertencer a uma comunidade do Mestre; pertencendo a outra,
o núcleo SHALL recusar com **403**. (`RF-09-75`, `RF-04-55`, decisão do fundador de 2026-10-30)

#### Scenario: A fila da aula traz só quem registrou presença

- **WHEN** o Mestre pede a fila recortada por uma aula, e há na comunidade dois Guerreiros com
  marco alcançado, um com presença registrada naquela aula e outro sem
- **THEN** a fila traz apenas o que tem presença registrada

#### Scenario: Presença anulada tira a pendência da fila da aula

- **WHEN** a presença de um Guerreiro(a) naquela aula é anulada
- **THEN** a pendência dele sai da fila recortada por aquela aula

#### Scenario: Sem recorte, a fila segue sendo das comunidades

- **WHEN** o Mestre pede a fila sem declarar aula
- **THEN** a fila traz as pendências de todas as comunidades dele, como já trazia

#### Scenario: Aula de outra comunidade é recusada

- **WHEN** o Mestre pede a fila recortada por aula de comunidade a que não está vinculado
- **THEN** o núcleo responde **403** e nada da fila é servido

### Requirement: A entrega no encontro sai do ponto de apoio da aula

O núcleo SHALL aceitar a confirmação da entrega **declarando a aula** em lugar do ponto de
apoio: o recurso SHALL sair do **ponto de apoio daquela aula**, e o lastro SHALL ser
reverificado contra o saldo dele, como já é contra o escolhido. (`RF-09-76`, `RF-07-13`,
documento 02 §8.1, decisão do fundador de 2026-10-30)

#### Scenario: A entrega declarada por aula baixa do ponto de apoio dela

- **WHEN** o Mestre confirma a entrega declarando a aula em curso
- **THEN** o núcleo grava a entrega, emite o débito contra o ponto de apoio daquela aula e a
  pendência sai da fila

#### Scenario: Sem lastro no ponto de apoio da aula, a entrega é recusada

- **WHEN** o ponto de apoio da aula não tem saldo do tipo de recurso da recompensa
- **THEN** o núcleo recusa a entrega em linguagem simples e nada é gravado

#### Scenario: O Admin não confirma a entrega no encontro

- **WHEN** a sessão de trabalho aberta por um Admin tenta confirmar a entrega
- **THEN** o núcleo responde **403** e nada é gravado

### Requirement: A entrega declarada por aula exige presença registrada

A entrega confirmada com a aula declarada SHALL exigir **presença registrada e não anulada**
do Guerreiro(a) naquela aula: no encontro entrega-se a quem chegou. (`RF-09-76`, `RF-04-55`,
decisão do fundador de 2026-10-30)

#### Scenario: Entrega por aula a quem não registrou presença é recusada

- **WHEN** o Mestre confirma, declarando a aula, a entrega a um Guerreiro(a) sem presença
  registrada nela
- **THEN** o núcleo recusa com **422** e nada é gravado

#### Scenario: Presença anulada depois do registro recusa a entrega

- **WHEN** a presença do Guerreiro(a) naquela aula foi anulada e o Mestre tenta confirmar
- **THEN** o núcleo recusa com **422** e nada é gravado
