## ADDED Requirements

### Requirement: A gestão lê a fila de solicitações de participação

O núcleo SHALL devolver as solicitações de participação com **nome**, **e-mail**,
**WhatsApp**, **pretensão** — Mestre ou Apoiador —, **apresentação**, **instituição** e
**links declarados**, mais a **situação**, o **prazo** e, quando já houver desfecho, **quem
avaliou**, o **parecer** e a **data**. Quando a pretensão for Apoiador, a leitura SHALL levar
também o **aporte declarado**, o **nick pretendido** e a indicação de que há **comprovante
anexado**. A leitura SHALL ser paginada.

A leitura SHALL marcar cada solicitação **em atraso** quando o prazo tiver vencido sem
desfecho. O atraso SHALL ser **derivado** do prazo no momento da consulta e NEVER SHALL ser
gravado como situação. (`RF-02-18`, `RF-02-65`, `RF-02-83`, `RF-01-25`, `RF-01-28`,
`RN-01-49`)

A leitura SHALL exigir **Admin** em sessão. Mestre, Apoiador, Guerreiro(a) e responsável SHALL
receber **403**. (`RF-01-16`, `RN-02-01`)

A leitura NEVER SHALL devolver o conteúdo do comprovante — apenas que ele existe. (`RN-01-28`)

#### Scenario: Admin lê a fila com as solicitações em aberto

- **WHEN** um Admin em sessão consulta a fila de solicitações de participação
- **THEN** vêm as solicitações com identificação, pretensão, apresentação, instituição, links,
  situação e prazo

#### Scenario: Solicitação de Apoiador traz o pré-cadastro

- **WHEN** a fila devolve uma solicitação com pretensão de Apoiador
- **THEN** ela vem com o aporte declarado, o nick pretendido e a indicação de comprovante
  anexado

#### Scenario: Solicitação com prazo vencido vem marcada em atraso

- **WHEN** um Admin consulta a fila e há solicitação sem desfecho cujo prazo de 7 dias já
  venceu
- **THEN** ela vem marcada como em atraso, e a situação gravada continua sendo **recebida**

#### Scenario: Solicitação já avaliada traz o desfecho

- **WHEN** a fila devolve uma solicitação que já teve desfecho
- **THEN** ela vem com a situação final, o parecer, quem avaliou e a data, e não vem marcada
  em atraso

#### Scenario: Quem não é Admin não lê a fila

- **WHEN** um Mestre, Apoiador, Guerreiro(a) ou responsável em sessão consulta a fila
- **THEN** o núcleo responde 403

#### Scenario: A fila não devolve o comprovante

- **WHEN** a fila devolve uma solicitação com comprovante anexado
- **THEN** vem apenas a indicação de que existe comprovante, e nunca o conteúdo do arquivo

### Requirement: O Admin registra o desfecho da solicitação de participação

O núcleo SHALL aceitar de um **Admin** em sessão o desfecho de uma solicitação de
participação, **aceita** ou **recusada**, gravando o **parecer**, o **autor da avaliação** e a
**data e hora**. Desfecho diferente de aceita ou recusada SHALL ser recusado com **422**.
(`RF-02-19`, `RF-02-86`, `RF-01-25`)

O desfecho NEVER SHALL criar persona, credencial ou qualquer acesso, nem na aprovação: o
cadastro correspondente SHALL depender de ato posterior do Admin. (`RN-01-03`, `RN-01-28`,
`RN-02-03`)

A solicitação **já avaliada** NEVER SHALL ser reavaliada: novo desfecho sobre ela SHALL ser
recusado com **409**, e o desfecho gravado SHALL permanecer intacto. (`RF-01-25`)

Quem não for Admin SHALL receber **403**. (`RN-02-01`, `RN-02-02`)

Toda escrita SHALL entrar na trilha de auditoria, com autor, papel, data e hora. (`RN-02-21`)

#### Scenario: Admin aceita a solicitação

- **WHEN** um Admin em sessão conclui uma solicitação como aceita, com parecer
- **THEN** o núcleo grava a situação aceita, o parecer, o autor e a data, e nenhuma persona é
  criada

#### Scenario: Admin recusa a solicitação com o motivo

- **WHEN** um Admin em sessão conclui uma solicitação como recusada, com o motivo no parecer
- **THEN** o núcleo grava a situação recusada com o motivo, o autor e a data

#### Scenario: Desfecho fora do vocabulário é recusado

- **WHEN** o desfecho enviado não é aceita nem recusada
- **THEN** o núcleo responde 422 e nada é gravado

#### Scenario: Solicitação avaliada não se reavalia

- **WHEN** um Admin envia novo desfecho para uma solicitação que já tem desfecho gravado
- **THEN** o núcleo responde 409 e o desfecho original permanece como estava

#### Scenario: Quem não é Admin não avalia

- **WHEN** um Mestre em sessão tenta concluir uma solicitação de participação
- **THEN** o núcleo responde 403 e nada é gravado

#### Scenario: O desfecho entra na trilha de auditoria

- **WHEN** um Admin conclui uma solicitação
- **THEN** a trilha de auditoria registra o ato com autor, papel, data e hora
