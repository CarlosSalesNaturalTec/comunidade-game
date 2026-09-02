## ADDED Requirements

### Requirement: A fila do Mestre traz só o que ele tem a validar

O núcleo SHALL devolver ao **Mestre** em sessão os desafios extras em **em validação do
Mestre** cujas trilhas são de **autoria dele**, com o que cada proposta oferece — trilha,
missão quando houver, modalidade, recompensa, quantidade, critério de atribuição, pontos
extras, formato, custeio e vigência. A fila NEVER SHALL trazer desafio de trilha de outro
Mestre, nem desafio em **em aprovação do Admin**, **publicado** ou **recusado**. Persona de
qualquer outro papel SHALL receber **403**. Nenhuma resposta SHALL identificar Guerreiro(a):
do direcionado sai o **nick como o proponente o digitou**, e nada mais. (`RF-09-51`,
`RN-09-11`, `RN-14-20`)

#### Scenario: A fila traz o desafio da trilha do próprio Mestre

- **WHEN** o Mestre consulta a fila e há um desafio em validação vinculado a uma trilha de que
  ele é autor
- **THEN** o desafio aparece com a recompensa, a quantidade, o critério, os pontos extras, o
  formato, o custeio e a vigência

#### Scenario: Desafio de trilha de outro Mestre não aparece

- **WHEN** o Mestre consulta a fila e há um desafio em validação vinculado à trilha de outro
  Mestre
- **THEN** o desafio não aparece na fila

#### Scenario: O já validado sai da fila

- **WHEN** um desafio da trilha do Mestre é validado ou recusado por ele
- **THEN** a consulta seguinte à fila não o traz mais

#### Scenario: Quem não é Mestre não lê a fila

- **WHEN** uma persona de outro papel consulta a fila de desafios extras a validar
- **THEN** o núcleo responde 403

#### Scenario: A fila não identifica o destinatário do direcionado

- **WHEN** a fila traz um desafio direcionado
- **THEN** a resposta traz o nick como o proponente o digitou e nenhum outro dado do
  destinatário

### Requirement: O Mestre autor da trilha valida o desafio extra com parecer

O núcleo SHALL permitir ao **Mestre autor da trilha** validar um desafio extra em **em
validação do Mestre**, exigindo o **parecer** e gravando **quem validou**, e SHALL levar a
situação a **em aprovação do Admin**. Validação sem parecer SHALL ser recusada com **422**.
A validação por persona que não seja o Mestre autor daquela trilha SHALL ser recusada com
**403**, ainda que seja Mestre de outra trilha. A validação de desafio que não esteja em **em
validação do Mestre** SHALL ser recusada com **409**. (`RF-09-51`, `RN-09-11`)

#### Scenario: A validação com parecer leva o desafio ao Admin

- **WHEN** o Mestre autor da trilha valida um desafio em validação, com parecer
- **THEN** o desafio passa a em aprovação do Admin, com o parecer e o Mestre validador
  registrados

#### Scenario: Validação sem parecer não passa

- **WHEN** o Mestre autor valida um desafio sem informar o parecer
- **THEN** o núcleo responde 422 e o desafio permanece em validação do Mestre

#### Scenario: Mestre de outra trilha não valida

- **WHEN** um Mestre que não é autor da trilha valida o desafio dela
- **THEN** o núcleo responde 403 e o desafio permanece como estava

#### Scenario: Desafio já validado não se valida de novo

- **WHEN** o Mestre autor valida um desafio que já está em aprovação do Admin
- **THEN** o núcleo responde 409 e nada muda

### Requirement: O Mestre recusa o desafio extra com motivo, e o recusado não chega ao Admin

O núcleo SHALL permitir ao **Mestre autor da trilha** recusar um desafio extra em **em
validação do Mestre**, exigindo o **motivo** e gravando **quem recusou**, e SHALL levar a
situação a **recusado**. Recusa sem motivo SHALL ser recusada com **422**. O desafio recusado
pelo Mestre NEVER SHALL aparecer na fila de aprovação do Admin, e a leitura do proponente SHALL
devolver o motivo. Nenhuma reserva SHALL ser gravada pela recusa. (`RF-09-51`, `RF-09-52`,
`RN-09-11`)

#### Scenario: Recusa sem motivo não passa

- **WHEN** o Mestre autor recusa um desafio sem informar o motivo
- **THEN** o núcleo responde 422 e o desafio permanece em validação do Mestre

#### Scenario: O recusado pelo Mestre não chega à fila do Admin

- **WHEN** o Mestre autor recusa um desafio com motivo e o Admin consulta a fila dele
- **THEN** o desafio não aparece na fila do Admin

#### Scenario: O proponente lê o motivo da recusa do Mestre

- **WHEN** o proponente lê um desafio recusado pelo Mestre
- **THEN** a resposta traz a situação de recusado e o motivo que o Mestre registrou

### Requirement: A validação pedagógica é dispensada só para o Mestre autor da própria trilha

O núcleo SHALL nascer o `DesafioExtra` em **em aprovação do Admin** quando o proponente for o
**Mestre autor da trilha** a que ele se vincula, e em **em validação do Mestre** em qualquer
outro caso — proposta de Apoiador e proposta de **outro Mestre** que não seja o autor daquela
trilha. A dispensa NEVER SHALL alcançar a **aprovação do Admin**, exigida de toda proposta.
(`RF-09-108`, `RF-09-109`, `RF-09-110`, `RN-09-41`)

#### Scenario: A proposta do Mestre autor já nasce na fila do Admin

- **WHEN** o Mestre autor de uma trilha propõe um desafio extra a ela
- **THEN** a proposta nasce em aprovação do Admin, sem passar por validação pedagógica

#### Scenario: A proposta de outro Mestre passa pela validação do autor

- **WHEN** um Mestre propõe um desafio extra a uma trilha de que não é autor
- **THEN** a proposta nasce em validação do Mestre e aparece na fila do Mestre autor daquela
  trilha

#### Scenario: A dispensa não dispensa o Admin

- **WHEN** a proposta do Mestre autor chega à publicação sem que o Admin a tenha aprovado
- **THEN** a publicação é recusada, porque a aprovação do Admin é exigida de toda proposta

### Requirement: O direcionado proposto pelo Mestre exige justificativa pedagógica

O núcleo SHALL exigir do desafio **direcionado** proposto por Mestre, além do **nick do
destinatário**, a **justificativa pedagógica** registrada — no lugar da justificativa de
vínculo que o Apoiador declara —, recusando com **422** a proposta que não a traga. As demais
guardas do direcionado SHALL valer igual: NEVER SHALL o núcleo confirmar ao proponente se
aquele nick existe, nem devolver dado do destinatário. (`RF-09-111`, `RN-14-18`, `RN-14-20`,
04 §3)

#### Scenario: Direcionado do Mestre sem justificativa é recusado

- **WHEN** um Mestre propõe um desafio direcionado com o nick do destinatário e sem a
  justificativa pedagógica
- **THEN** o núcleo responde 422 e nenhuma proposta passa a existir

#### Scenario: Direcionado do Mestre não confirma o nick

- **WHEN** um Mestre propõe um desafio direcionado a um nick que não corresponde a
  Guerreiro(a) algum
- **THEN** o núcleo registra a proposta como qualquer outra, sem erro e sem indicar que o nick
  não existe

### Requirement: Cada proponente lê os desafios que propôs

O núcleo SHALL devolver a **Apoiador ou Mestre** em sessão os desafios extras que ele mesmo
propôs, com a **situação** de cada um, o **motivo da recusa** quando houver e a **quantidade
restante** do publicado. NEVER SHALL devolver a um proponente o desafio proposto por outro.
(`RF-09-105`, `RF-14-35`, `RF-14-38`)

#### Scenario: O Mestre lê o que propôs

- **WHEN** um Mestre lê os seus desafios extras
- **THEN** a resposta traz os que ele propôs, com a situação de cada um

#### Scenario: O proponente não lê o desafio alheio

- **WHEN** um proponente lê os seus desafios extras e há desafio proposto por outra persona
- **THEN** esse desafio não aparece na resposta

## MODIFIED Requirements

### Requirement: A proposta se vincula a uma trilha em andamento e declara o que oferece

O núcleo SHALL registrar o `DesafioExtra` vinculando **proponente** — **Apoiador ou Mestre** —,
**trilha em andamento** e, opcionalmente, **missão**, com **recompensa**, **quantidade
disponível**, **critério de atribuição** e **período de vigência**. Trilha que não esteja em
andamento SHALL ser recusada com **422**. Persona de qualquer outro papel SHALL ser recusada
com **403**. NEVER SHALL existir teto de desafios simultâneos: o controle é a aprovação caso a
caso. (`RF-14-29`, `RF-14-30`, `RN-14-15`, `RF-09-105`, PRD-14 §8, 04 §3)

#### Scenario: Proposta completa é registrada

- **WHEN** um Apoiador propõe um desafio a uma trilha em andamento, com recompensa, quantidade,
  critério de atribuição e vigência
- **THEN** o núcleo registra a proposta com o proponente, a trilha e o que ela oferece

#### Scenario: O Mestre propõe pela mesma mecânica

- **WHEN** um Mestre propõe um desafio a uma trilha em andamento, com recompensa, quantidade,
  critério de atribuição e vigência
- **THEN** o núcleo registra a proposta com ele como proponente, sob as mesmas exigências da
  proposta do Apoiador

#### Scenario: Trilha que não está em andamento é recusada

- **WHEN** a proposta declara uma trilha que não está em andamento
- **THEN** o núcleo responde 422 e nenhuma proposta passa a existir

#### Scenario: Papel que não propõe é recusado

- **WHEN** uma persona que não é Apoiador nem Mestre propõe um desafio extra
- **THEN** o núcleo responde 403 e nenhuma proposta passa a existir

#### Scenario: Não há teto de propostas simultâneas

- **WHEN** um Apoiador propõe um desafio tendo outros já propostos e ainda não desfeitos
- **THEN** o núcleo registra a proposta, sem recusar por quantidade

### Requirement: A situação percorre validação do Mestre, aprovação do Admin e publicação

O núcleo SHALL manter a **situação** do `DesafioExtra` entre **em validação do Mestre**, **em
aprovação do Admin**, **publicado** e **recusado**. A situação de nascimento SHALL ser decidida
pelo proponente: **em aprovação do Admin** quando ele for o Mestre autor da trilha, **em
validação do Mestre** em qualquer outro caso. NEVER SHALL publicar desafio que não tenha
passado pela aprovação de Admin, nem desafio que, não sendo do Mestre autor da trilha, não
tenha passado pela validação do Mestre dela. A recusa em qualquer etapa SHALL guardar o
**motivo**, e a leitura do proponente SHALL devolvê-lo. (`RF-14-35`, `RF-14-36`, `RN-14-13`,
`RF-09-108`, `RN-09-11`, `RN-09-41`)

#### Scenario: Proposta nasce em validação do Mestre

- **WHEN** um Apoiador registra uma proposta
- **THEN** a situação dela é "em validação do Mestre"

#### Scenario: A proposta do Mestre autor nasce em aprovação do Admin

- **WHEN** o Mestre autor da trilha registra uma proposta a ela
- **THEN** a situação dela é "em aprovação do Admin"

#### Scenario: O proponente lê o motivo da recusa

- **WHEN** o proponente lê um desafio recusado
- **THEN** a resposta traz a situação de recusado e o motivo registrado
