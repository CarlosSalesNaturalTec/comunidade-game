## ADDED Requirements

### Requirement: A pré-visualização mostra ao autor o que ele declarou para o desbloqueio

A pré-visualização da missão SHALL apresentar, num trecho próprio dito como o que o
Guerreiro(a) não vê na missão, a recompensa pelo desbloqueio e os detalhes do desafio que o
Mestre autor declarou, sem gravar coisa alguma: da recompensa, só o **nome do tipo de
recurso**, NEVER a quantidade (`RF-09-84`); no prático, o **título curto** e o **kit
apresentado** (`RF-09-131`, `RF-09-141`); no quiz, o **corte** de aprovação, que a sondagem não
tem (`RN-05-45`, `RN-05-46`). (`RF-09-25`)

#### Scenario: A pré-visualização traz a recompensa pelo desbloqueio, sem quantidade

- **WHEN** o Mestre autor pré-visualiza uma missão com recompensa pelo desbloqueio declarada
- **THEN** a pré-visualização mostra o nome do tipo de recurso de cada recompensa, sem a
  quantidade

#### Scenario: A pré-visualização diz que não há recompensa

- **WHEN** o Mestre autor pré-visualiza uma missão sem recompensa pelo desbloqueio
- **THEN** a pré-visualização diz que nenhuma recompensa pelo desbloqueio foi declarada

#### Scenario: A pré-visualização traz o título curto e o kit do prático

- **WHEN** o Mestre autor pré-visualiza uma missão cujo prático tem título curto e kit
  apresentado declarados
- **THEN** a pré-visualização mostra o título curto e o nome do recurso do kit

#### Scenario: Prático antigo, sem título nem kit

- **WHEN** o Mestre autor pré-visualiza um prático declarado sem título curto nem kit
  (`RN-09-50`)
- **THEN** a pré-visualização não mostra nenhum dos dois, e o resto do desafio segue exibido

#### Scenario: A pré-visualização traz o corte do quiz

- **WHEN** o Mestre autor pré-visualiza uma missão com quiz de desbloqueio
- **THEN** a pré-visualização diz que passa quem acerta ao menos 60% das perguntas

#### Scenario: A sondagem não tem corte

- **WHEN** o Mestre autor pré-visualiza a missão de sondagem
- **THEN** a pré-visualização diz que a trilha abre assim que o Guerreiro(a) responde, sem o
  corte de 60%
