## MODIFIED Requirements

### Requirement: O painel mostra cada equipe com a missão em que ela está

O painel SHALL listar as **equipes formadas na App 01** naquela aula, cada uma pelo **nome**,
com os seus integrantes — cada um por **nick e avatar** e com o **papel** que declarou na
formação, ou sem papel quando não declarou — e com a **missão em que ela está**: a da atividade
da programação que a equipe declarou como corrente. Equipe que ainda não declarou escolha SHALL
aparecer **sem missão**, e não com erro nem com missão suposta pelo núcleo.

A gestão SHALL ler a composição e NEVER SHALL alterá-la: a composição é dos Guerreiros e
Guerreiras, formada na App 01 (documento 02 §5, `RF-02-09`). (`RF-02-42`, `RF-02-08`, `RN-02-07`,
PRD-02 §6.4)

#### Scenario: A equipe sai pelo nome, com o papel de cada integrante

- **WHEN** a equipe "Leões" tem um integrante que declarou "quem registra" e outro sem papel
- **THEN** o painel a mostra como "Leões", o primeiro com o papel "quem registra" e o segundo
  sem papel

#### Scenario: A troca do nome aparece na consulta seguinte

- **WHEN** um integrante renomeia a equipe durante o encontro
- **THEN** a consulta seguinte do painel a mostra com o nome novo

#### Scenario: A equipe sai com a missão que declarou

- **WHEN** uma equipe da aula declarou a atividade da programação que está trabalhando
- **THEN** o painel a mostra com a missão daquela atividade

#### Scenario: Duas equipes em trilhas diferentes saem cada uma com a sua

- **WHEN** duas equipes do mesmo encontro declararam atividades de trilhas diferentes
- **THEN** o painel mostra cada uma com a missão que ela declarou

#### Scenario: Equipe sem escolha aparece sem missão

- **WHEN** uma equipe formada ainda não declarou atividade alguma
- **THEN** ela aparece no painel sem missão, e o núcleo não supõe nenhuma

#### Scenario: Trocar de atividade muda o que o painel mostra

- **WHEN** a equipe declara outra atividade da programação durante o encontro
- **THEN** a consulta seguinte do painel a mostra na missão nova
