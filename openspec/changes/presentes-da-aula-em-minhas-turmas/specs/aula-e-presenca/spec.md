## MODIFIED Requirements

### Requirement: O Mestre lê as suas turmas, separadas pelo formato da atividade

O núcleo SHALL servir ao **Mestre em sessão** as aulas das comunidades a que ele é vinculado e
as atividades **de que ele é autor**, e nada além: turma de outra comunidade e atividade de
outro Mestre NEVER SHALL aparecer na leitura (`RN-09-08`).

A aula de situação **cancelada** NEVER SHALL ser devolvida: não há encontro, presença nem
ocorrência a lançar nela, e a paginação SHALL contar só as aulas devolvidas (decisão do
fundador de 2026-11-20).

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

#### Scenario: Aula cancelada não é devolvida

- **WHEN** o Mestre lê as suas turmas e uma das aulas das comunidades dele está cancelada
- **THEN** o núcleo devolve as demais aulas e não devolve a cancelada

#### Scenario: A página não é ocupada por aula cancelada

- **WHEN** as aulas canceladas se intercalam com as demais e o Mestre lê as turmas em páginas
- **THEN** cada página traz até o tamanho pedido de aulas não canceladas, e o cursor segue a
  partir da última devolvida

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

## ADDED Requirements

### Requirement: O Mestre lê as presenças registradas na aula

O núcleo SHALL servir ao Mestre em sessão as **presenças não anuladas** de uma aula das
comunidades dele, cada uma com o **nick** e o **avatar** do Guerreiro(a), o **momento do fato**
e o **modo de comprovação** — reconhecimento ou confirmação. A saída NEVER SHALL trazer imagem
real nem descritor facial do Guerreiro(a) (`RN-09-18`), e a presença anulada NEVER SHALL
aparecer. Aula sem presença SHALL devolver lista vazia, nunca erro.

Aula de comunidade a que o Mestre não é vinculado SHALL responder **404**, como a aula
inexistente: a leitura não revela o que há fora do escopo dele (`RN-09-08`). O Admin lê a
presença de qualquer aula. A leitura exige a operação **suas turmas**: papel sem ela SHALL
receber **403**. (`RF-09-145`, `RF-09-42`, `RF-09-45`, `RN-09-08`, `RN-09-18`)

#### Scenario: O Mestre lê os presentes da sua aula

- **WHEN** o Mestre em sessão lê as presenças de uma aula da comunidade dele
- **THEN** o núcleo devolve cada presença com nick, avatar, momento do fato e modo

#### Scenario: Presença anulada não aparece

- **WHEN** uma das presenças da aula foi anulada pelo Admin
- **THEN** ela não aparece na leitura

#### Scenario: Aula sem presença devolve lista vazia

- **WHEN** o Mestre lê as presenças de uma aula sua em que ninguém foi registrado
- **THEN** o núcleo devolve a lista vazia, sem erro

#### Scenario: Aula de outra comunidade responde como inexistente

- **WHEN** o Mestre pede as presenças de uma aula de comunidade a que não é vinculado
- **THEN** o núcleo responde 404, com a mesma mensagem da aula inexistente

#### Scenario: Papel sem a operação é recusado na leitura das presenças

- **WHEN** uma persona cujo papel não tem a operação de suas turmas pede as presenças da aula
- **THEN** o núcleo responde 403 e nada é devolvido
