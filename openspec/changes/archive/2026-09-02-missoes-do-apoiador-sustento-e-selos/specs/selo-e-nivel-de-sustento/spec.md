## Purpose

O reconhecimento de quem apoia corre em selos e níveis de sustento, nunca em pontos. Esta
capacidade cobre o selo creditado na conclusão da missão, as quatro famílias em que ele se
agrupa e o nível de sustento derivado das frentes de necessidade cobertas — um e outro sem
regressão e sem pódio por valor.

## ADDED Requirements

### Requirement: O selo é creditado na homologação que conclui a missão

O núcleo SHALL creditar o `SeloDoApoiador` — o selo que a missão declara — a **cada
participante** da missão no ato da homologação que a conclui, e NEVER SHALL creditá-lo por
aporte parcial que deixe a missão aberta. Participante SHALL ser quem tem ao menos um aporte
**homologado** naquela missão. O selo SHALL guardar a **família** — frente, modalidade, ato ou
multiplicação —, o selo, a missão de origem e a data do crédito. O registro SHALL ser **somente
inserção**: nenhuma rota SHALL retirá-lo. (`RF-14-66`, `RN-14-33`, `RN-14-36`, PRD-14 §8)

#### Scenario: O aporte parcial não credita selo

- **WHEN** um aporte homologado cobre parte da missão e ela segue aberta
- **THEN** nenhum selo é creditado, e as moedas do aporte já estão no Poder Sustentador de quem
  o fez

#### Scenario: Concluída a missão, todos os participantes recebem o selo

- **WHEN** a homologação que fecha o saldo conclui uma missão coberta por duas pessoas
- **THEN** cada uma recebe o selo da missão, com a família, a missão de origem e a data

#### Scenario: Não há rota que retire o selo

- **WHEN** se procura caminho para apagar ou revogar um selo creditado
- **THEN** nenhuma rota o oferece, e o selo permanece

### Requirement: A missão coberta por mais de uma pessoa rende também o selo de mutirão

Concluída uma missão com **mais de um participante**, cada um SHALL receber, além do selo que a
missão declara, o **selo de mutirão** — da família **ato**. Com um único participante, apenas o
selo da missão SHALL ser creditado. (`RF-14-66`, `RN-14-34`, PRD-14 §§5.4, 12)

#### Scenario: Duas pessoas fechando a mesma missão recebem o mutirão

- **WHEN** uma missão coberta por dois apoiadores é concluída
- **THEN** cada um recebe o selo da missão e o selo de mutirão, e nenhum vê o nome do outro

#### Scenario: O participante único não recebe mutirão

- **WHEN** uma missão coberta por um só Apoiador é concluída
- **THEN** ele recebe apenas o selo que a missão declara

### Requirement: O nível de sustento é derivado das frentes cobertas e não regride

O nível de sustento SHALL ser **derivado**, nunca armazenado, a partir dos **níveis de
necessidade** das missões concluídas pelo Apoiador e do primeiro aporte homologado dele, na
escada do documento 14 §7. Ele SHALL subir por **frentes de necessidade diferentes** cobertas e
NEVER SHALL subir por volume aportado. Nível e selo já alcançados NEVER SHALL regredir.

A escada derivada SHALL ir até o **nível 4**: as duas vias do nível 5 — virou Mestre e aporte
em código homologado — não são verificáveis no núcleo e seguem como pendência do documento 09.
A frente que falta a quem está no nível 4 SHALL ser dita como **virar Mestre**. (`RF-14-67`,
`RF-14-69`, `RN-14-35`, `RN-14-36`)

#### Scenario: Frentes diferentes valem mais que volume

- **WHEN** um Apoiador conclui uma missão de "acontecer" e outra de "permanecer", e outro
  conclui duas de "acontecer" por valor muito maior
- **THEN** o primeiro está no nível 3 e o segundo no nível 2

#### Scenario: O primeiro aporte homologado abre a escada

- **WHEN** o primeiro aporte de um Apoiador é homologado, sem missão concluída
- **THEN** ele está no nível 1

#### Scenario: A escada para no nível 4

- **WHEN** um Apoiador conclui missões em três níveis, um deles o permanecer
- **THEN** ele está no nível 4 e a frente que falta é virar Mestre

#### Scenario: O nível alcançado não cai

- **WHEN** uma missão que levou o Apoiador a um nível é despublicada ou vence depois de
  concluída
- **THEN** o nível dele permanece o que era

### Requirement: A leitura do sustento traz nível, selos e a frente que falta

O núcleo SHALL responder ao **Apoiador em sessão** o próprio nível de sustento, os selos
conquistados **agrupados por família** e a **frente que falta** para o próximo nível. A leitura
SHALL ser do próprio Apoiador: pedir a de outro SHALL responder **403**. A resposta NEVER SHALL
trazer valor em reais nem dado de Guerreiro(a). (`RF-14-67`, `RF-14-68`, `RN-14-09`)

#### Scenario: O Apoiador lê o próprio sustento

- **WHEN** o Apoiador em sessão consulta o sustento
- **THEN** a resposta traz o nível, os selos agrupados por família e a frente que falta para o
  próximo, sem nenhum valor em reais

#### Scenario: Ninguém lê o sustento de outro

- **WHEN** um Apoiador pede o sustento de outro Apoiador
- **THEN** o núcleo responde 403

### Requirement: Não há ranking de apoiadores por valor

Nenhuma leitura desta capacidade SHALL ordenar, classificar ou comparar apoiadores por valor
aportado, e NEVER SHALL existir pódio de valor: o que se coleciona é selo e nível.
(`RF-14-70`, `RN-14-38`)

#### Scenario: Nenhuma leitura ordena por valor

- **WHEN** se consulta qualquer leitura de selos ou níveis de sustento
- **THEN** nenhuma resposta traz ordenação, posição ou comparação por valor aportado
