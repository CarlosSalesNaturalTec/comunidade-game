## ADDED Requirements

### Requirement: O Mestre declara a cadência de retomada, com 2, 7 e 21 dias sugeridos

A App 09 SHALL permitir ao Mestre autor declarar a **cadência de retomada** de uma missão ou
deixá-la **sem retomada**. Na missão sem cadência gravada, o campo SHALL abrir **preenchido com
2, 7 e 21 dias** como **sugestão**, alterável à vontade e NEVER gravada sem ele confirmar; a
missão com cadência gravada SHALL abrir com a dela. (`RF-09-83`, `RF-09-116`, `RF-09-101`)

#### Scenario: Mestre declara a cadência

- **WHEN** o Mestre autor declara a cadência de retomada de uma missão dele
- **THEN** a aplicação a grava na missão e a apresenta junto dela

#### Scenario: Missão sem retomada é aceita

- **WHEN** o Mestre autor deixa a missão sem cadência de retomada
- **THEN** a aplicação a aceita, e a missão fica sem retomada declarada

#### Scenario: A sugestão vem preenchida e alterável

- **WHEN** o Mestre autor abre o bloco de cadência de uma missão sem cadência gravada
- **THEN** o campo aparece preenchido com 2, 7 e 21 dias, a missão continua sem retomada
  declarada, e ele altera, apaga ou confirma o valor antes de qualquer gravação

#### Scenario: A cadência gravada prevalece sobre a sugestão

- **WHEN** o Mestre autor abre o bloco de cadência de uma missão que já tem cadência gravada
- **THEN** o campo traz a cadência gravada, e não a de 2, 7 e 21 dias

### Requirement: Os blocos da missão começam pelo conteúdo e fecham pela pré-visualização

A App 09 SHALL apresentar os blocos de cada missão nesta ordem: **conteúdo**, **bibliografia**,
**cadência de retomada**, **atividades**, **desafio de desbloqueio**, **recompensa pelo
desbloqueio**, **desafios de coleta** e **ODS da missão**, com a **pré-visualização** depois de
todos — a ordem da fatia 17, sem o template. (`RF-09-14`, `RF-09-21`, `RF-09-83`,
`RF-09-69`, `RF-09-26`, `RF-09-84`, `RF-09-27`, `RF-09-98`, `RF-09-25`)

#### Scenario: A missão abre pelo conteúdo e fecha pela pré-visualização

- **WHEN** o Mestre autor abre uma missão da sua trilha
- **THEN** o primeiro bloco é o conteúdo, o último é o ODS da missão, a pré-visualização vem
  depois de todos, e não há bloco de template da missão

#### Scenario: A condição vem antes do que ela paga

- **WHEN** o Mestre autor percorre os blocos da missão
- **THEN** o desafio de desbloqueio aparece antes da recompensa pelo desbloqueio

#### Scenario: Conteúdo e bibliografia ficam juntos

- **WHEN** o Mestre autor percorre os blocos da missão
- **THEN** a bibliografia vem imediatamente depois do conteúdo

## REMOVED Requirements

### Requirement: O Mestre declara a cadência de retomada da missão

**Reason**: A sugestão de 2, 7 e 21 dias vinha do template da missão, retirado pela decisão do
fundador de 2026-11-16; `RF-09-116` é reescrito.
**Migration**: Substituído por "O Mestre declara a cadência de retomada, com 2, 7 e 21 dias
sugeridos", em que a sugestão abre no próprio campo.

### Requirement: Os blocos da missão seguem a ordem em que o Mestre a escreve

**Reason**: A ordem abria pelo bloco do template da missão, retirado pela mesma decisão.
**Migration**: Substituído por "Os blocos da missão começam pelo conteúdo e fecham pela
pré-visualização", com a mesma sequência sem o template.

### Requirement: O Mestre cadastra o tópico e recebe a estrutura sugerida da missão

**Reason**: Decisão do fundador de 2026-11-16 — o template da missão sai da App 09 para
simplificar a autoria. `RF-09-85`, `RF-09-91` e `RF-09-95` saem do PRD-09.
**Migration**: O Mestre escreve a missão direto pelos blocos de autoria; a cadência sugerida
passa ao próprio bloco de cadência.

### Requirement: A App 09 mostra as lacunas e não grava nada sem o Mestre confirmar

**Reason**: Mesma decisão; `RF-09-86`, `RF-09-87`, `RF-09-89` e `RN-09-33` saem do PRD-09.
**Migration**: O painel permanente de pendências da publicação (fatia 17) segue mostrando as
travas que impedem publicar; nada mais o substitui.
