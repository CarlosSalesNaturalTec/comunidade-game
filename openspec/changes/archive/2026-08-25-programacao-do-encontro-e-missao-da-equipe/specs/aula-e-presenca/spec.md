## MODIFIED Requirements

### Requirement: O Mestre lê as suas turmas, separadas pelo formato da atividade

O núcleo SHALL servir ao **Mestre em sessão** as aulas das comunidades a que ele é vinculado e
as atividades **de que ele é autor**, e nada além: turma de outra comunidade e atividade de
outro Mestre NEVER SHALL aparecer na leitura (`RN-09-08`).

A leitura SHALL separar as atividades pelo **formato** — **presencial** do encontro e
**on-line** entre encontros —, para que o Mestre distinga o que conduz na sala do que corre
entre os encontros. Em cada atividade presencial, a leitura SHALL trazer a **aula que ela
declarou**, quando houver: é como o Mestre confere a programação que montou e reconhece a
atividade que ainda não foi vinculada a encontro algum. Atividade sem aula declarada SHALL
aparecer na mesma lista, com o vínculo em branco.

A leitura exige a operação **suas turmas** da matriz de permissões: papel sem ela SHALL receber
**403**. (`RF-09-42`, `RF-09-73`, `RN-09-08`, `RF-01-16`, documento 05 §4)

#### Scenario: O Mestre vê as próprias turmas e atividades

- **WHEN** o Mestre em sessão lê as suas turmas
- **THEN** o núcleo devolve as aulas das comunidades dele com as atividades de que ele é autor

#### Scenario: Atividade de outro Mestre não aparece

- **WHEN** existe atividade autorada por outro Mestre numa aula da mesma comunidade
- **THEN** ela não aparece na leitura das turmas do Mestre em sessão

#### Scenario: As atividades saem separadas por formato

- **WHEN** a turma do Mestre tem atividades presenciais e on-line
- **THEN** a saída distingue as presenciais das on-line pelo formato de cada atividade

#### Scenario: A atividade presencial sai com a aula que declarou

- **WHEN** o Mestre lê as suas turmas e uma atividade presencial dele declarou uma aula
- **THEN** a saída traz aquela aula junto da atividade

#### Scenario: Atividade ainda sem encontro sai com o vínculo em branco

- **WHEN** o Mestre lê as suas turmas e uma atividade presencial dele não declarou aula alguma
- **THEN** ela aparece na lista com o vínculo em branco

#### Scenario: Papel sem a operação é recusado

- **WHEN** uma persona cujo papel não tem a operação de suas turmas pede a leitura
- **THEN** o núcleo responde 403 e nada é devolvido
