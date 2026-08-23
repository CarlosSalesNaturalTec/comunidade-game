## ADDED Requirements

### Requirement: O Mestre lê as suas turmas, separadas pelo formato da atividade

O núcleo SHALL servir ao **Mestre em sessão** as aulas das comunidades a que ele é vinculado e
as atividades **de que ele é autor**, e nada além: turma de outra comunidade e atividade de
outro Mestre NEVER SHALL aparecer na leitura (`RN-09-08`).

A leitura SHALL separar as atividades pelo **formato** — **presencial** do encontro e
**on-line** entre encontros —, para que o Mestre distinga o que conduz na sala do que corre
entre os encontros. A leitura exige a operação **suas turmas** da matriz de permissões: papel
sem ela SHALL receber **403**. (`RF-09-42`, `RF-09-73`, `RN-09-08`, `RF-01-16`)

#### Scenario: O Mestre vê as próprias turmas e atividades

- **WHEN** o Mestre em sessão lê as suas turmas
- **THEN** o núcleo devolve as aulas das comunidades dele com as atividades de que ele é autor

#### Scenario: Atividade de outro Mestre não aparece

- **WHEN** existe atividade autorada por outro Mestre numa aula da mesma comunidade
- **THEN** ela não aparece na leitura das turmas do Mestre em sessão

#### Scenario: As atividades saem separadas por formato

- **WHEN** a turma do Mestre tem atividades presenciais e on-line
- **THEN** a saída distingue as presenciais das on-line pelo formato de cada atividade

#### Scenario: Papel sem a operação é recusado

- **WHEN** uma persona cujo papel não tem a operação de suas turmas pede a leitura
- **THEN** o núcleo responde 403 e nada é devolvido

### Requirement: O Mestre registra presença apenas por confirmação

O núcleo SHALL aceitar do **Mestre** o registro de presença de um Guerreiro(a) na aula
**somente no modo confirmação**, gravando-o como quem confirmou. O modo **reconhecimento** é do
App 01 e NEVER SHALL ser aceito quando quem registra é o Mestre: a tentativa SHALL receber
**403**.

O recorte é o que concilia o `RF-09-45`, que dá a presença ao Mestre, com o PRD-01 §4, que não
a lista entre as escritas de gestão dele (`RF-01-17`): o Mestre a alcança pela **confirmação de
identidade do Guerreiro(a)**, operação que a matriz já lhe concede, e não por escrita de gestão
nova.

Permanecem valendo, sem alteração, a unicidade por aula e Guerreiro(a) e a recusa de presença
em comunidade alheia. (`RF-09-45`, `RF-01-20`, `RF-01-17`, `RF-01-03`)

#### Scenario: O Mestre confirma a presença que faltou

- **WHEN** o Mestre registra, no modo confirmação, a presença de um Guerreiro(a) da comunidade
  dele numa aula
- **THEN** o núcleo grava a presença com modo confirmação e o Mestre como confirmador

#### Scenario: O Mestre não registra presença por reconhecimento

- **WHEN** o Mestre tenta registrar presença no modo reconhecimento
- **THEN** o núcleo responde 403 e nada é gravado

#### Scenario: O reenvio da mesma presença não duplica

- **WHEN** o Mestre confirma novamente a presença de um Guerreiro(a) que já a tem naquela aula
- **THEN** o núcleo devolve a presença já gravada, sem duplicar e sem erro
