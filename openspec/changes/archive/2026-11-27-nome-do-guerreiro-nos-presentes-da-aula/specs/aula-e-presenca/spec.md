## MODIFIED Requirements

### Requirement: O Mestre lê as presenças registradas na aula

O núcleo SHALL servir ao Mestre em sessão as **presenças não anuladas** de uma aula das
comunidades dele, cada uma com o **nick**, o **nome** e o **avatar** do Guerreiro(a), o
**momento do fato** e o **modo de comprovação** — reconhecimento ou confirmação. O nome vem
nulo quando o Guerreiro(a) não o tem cadastrado. A saída NEVER SHALL trazer imagem
real nem descritor facial do Guerreiro(a) (`RN-09-18`), e a presença anulada NEVER SHALL
aparecer. Aula sem presença SHALL devolver lista vazia, nunca erro.

Aula de comunidade a que o Mestre não é vinculado SHALL responder **404**, como a aula
inexistente: a leitura não revela o que há fora do escopo dele (`RN-09-08`). O Admin lê a
presença de qualquer aula. A leitura exige a operação **suas turmas**: papel sem ela SHALL
receber **403**. (`RF-09-145`, `RF-09-42`, `RF-09-45`, `RN-09-08`, `RN-09-18`)

#### Scenario: O Mestre lê os presentes da sua aula

- **WHEN** o Mestre em sessão lê as presenças de uma aula da comunidade dele
- **THEN** o núcleo devolve cada presença com nick, nome, avatar, momento do fato e modo

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
