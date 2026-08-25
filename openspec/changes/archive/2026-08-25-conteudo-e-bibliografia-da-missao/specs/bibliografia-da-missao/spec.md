## Purpose

O vínculo entre a missão e o acervo didático: o título e o capítulo que aprofundam aquele
conteúdo, o exemplar tombado apontado quando existe, a disponibilidade no ponto de apoio do
Guerreiro(a) e o crédito ao Apoiador que forneceu o material.

## ADDED Requirements

### Requirement: A bibliografia liga a missão a um título e a um capítulo

O núcleo SHALL vincular toda `BibliografiaDaMissao` a uma **missão** e SHALL exigir dela o
**título** e o **capítulo recomendado**, ambos em texto. A escrita SHALL ser privativa do
**Mestre autor da trilha**: pedido de outro Mestre SHALL responder **403**. Uma missão SHALL
admitir mais de uma entrada de bibliografia. (`RF-09-21`, documento 05 §3, PRD-09 §§8, 9)

#### Scenario: Mestre autor declara a bibliografia

- **WHEN** o Mestre autor declara título e capítulo numa missão da própria trilha
- **THEN** o núcleo grava a entrada vinculada àquela missão

#### Scenario: Bibliografia sem capítulo é recusada

- **WHEN** chega bibliografia com título e sem capítulo
- **THEN** o núcleo responde **422** e nada é gravado

#### Scenario: Mestre que não é o autor é recusado

- **WHEN** um Mestre que não é o autor declara bibliografia numa missão da trilha
- **THEN** o núcleo responde **403** e nada é gravado

#### Scenario: A missão admite mais de uma entrada

- **WHEN** o Mestre autor declara um segundo título na mesma missão
- **THEN** o núcleo grava as duas entradas

### Requirement: O vínculo com o exemplar tombado é opcional

O núcleo SHALL admitir que a bibliografia aponte um **exemplar tombado** do acervo, e o vínculo
SHALL ser **opcional** — decisão do fundador de 2026-08-25. Sem vínculo, a bibliografia é
título e capítulo em texto e nada mais promete. Havendo vínculo, o exemplar apontado SHALL
existir; exemplar inexistente SHALL responder **422**. O núcleo NEVER SHALL exigir que o
título declarado coincida com o do exemplar apontado: quem declara o que apoia a missão é o
Mestre. (`RF-09-21`, documento 05 §3)

#### Scenario: Bibliografia sem vínculo é aceita

- **WHEN** o Mestre autor declara título e capítulo sem apontar exemplar algum
- **THEN** o núcleo grava a entrada, e nada é recusado

#### Scenario: Bibliografia com vínculo é aceita

- **WHEN** o Mestre autor declara título e capítulo apontando um exemplar tombado existente
- **THEN** o núcleo grava a entrada com o vínculo

#### Scenario: Exemplar inexistente é recusado

- **WHEN** chega bibliografia apontando exemplar que não existe
- **THEN** o núcleo responde **422** e nada é gravado

### Requirement: A disponibilidade só é dita quando há vínculo

A leitura da bibliografia SHALL informar se há **exemplar disponível no ponto de apoio** do
Guerreiro(a) **somente** quando a entrada estiver vinculada a exemplar tombado — a
disponibilidade deriva do ponto de apoio em que o exemplar está tombado. Sem vínculo, a leitura
NEVER SHALL afirmar nem negar disponibilidade: o dado não existe. (`RF-09-22`, documento 05 §3)

#### Scenario: Entrada vinculada informa a disponibilidade

- **WHEN** a bibliografia vinculada é lida por um Guerreiro(a) cujo ponto de apoio tem o exemplar
- **THEN** a leitura informa que há exemplar disponível ali

#### Scenario: Exemplar tombado em outro ponto de apoio

- **WHEN** a bibliografia vinculada é lida por um Guerreiro(a) de ponto de apoio onde o exemplar
  não está tombado
- **THEN** a leitura informa que não há exemplar disponível ali

#### Scenario: Entrada sem vínculo nada afirma

- **WHEN** a bibliografia sem vínculo é lida
- **THEN** a leitura NEVER SHALL afirmar nem negar disponibilidade de exemplar

### Requirement: O crédito ao Apoiador deriva do exemplar, e pode não existir

A leitura da bibliografia SHALL creditar o **Apoiador que forneceu o material** quando a
entrada estiver vinculada a exemplar tombado **e** esse exemplar tiver aporte de origem com
Apoiador identificado. Faltando o vínculo, ou tendo o exemplar entrado sem aporte de origem, a
leitura NEVER SHALL creditar Apoiador algum, e NEVER SHALL inventar crédito. O crédito NEVER
SHALL ser digitado pelo Mestre. (`RF-09-23`, documento 05 §3)

#### Scenario: Exemplar com aporte de origem credita o Apoiador

- **WHEN** a bibliografia vinculada a exemplar cujo aporte de origem é de um Apoiador é lida
- **THEN** a leitura credita aquele Apoiador

#### Scenario: Exemplar sem aporte de origem não credita ninguém

- **WHEN** a bibliografia vinculada a exemplar sem aporte de origem é lida
- **THEN** a leitura não credita Apoiador algum

#### Scenario: Entrada sem vínculo não credita ninguém

- **WHEN** a bibliografia sem vínculo é lida
- **THEN** a leitura não credita Apoiador algum

#### Scenario: O Mestre não digita o crédito

- **WHEN** chega bibliografia com Apoiador declarado pelo Mestre
- **THEN** o núcleo NEVER SHALL gravá-lo: o crédito deriva do exemplar, nunca da digitação
