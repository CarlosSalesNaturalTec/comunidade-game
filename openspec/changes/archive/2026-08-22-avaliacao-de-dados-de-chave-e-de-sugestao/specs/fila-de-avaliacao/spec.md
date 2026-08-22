## ADDED Requirements

### Requirement: A gestão lê a fila de solicitações de dados

O núcleo SHALL devolver as solicitações de dados com **solicitante**, **instituição**,
**finalidade declarada** e **recorte pedido**, mais a **situação**, o **prazo** e, quando já
houver desfecho, **quem avaliou**, o **parecer** e a **data**. A leitura SHALL ser paginada e
SHALL marcar como **em atraso** a solicitação sem desfecho cujo prazo tenha vencido, derivando
o atraso do prazo no momento da consulta. (`RF-02-77`, `RF-01-46`, `RN-01-49`)

A leitura SHALL exigir **Admin** em sessão; os demais papéis SHALL receber **403**.
(`RF-01-16`, `RN-02-01`)

#### Scenario: Admin lê a fila de pedidos de dados

- **WHEN** um Admin em sessão consulta a fila de solicitações de dados
- **THEN** vêm as solicitações com solicitante, instituição, finalidade declarada, recorte
  pedido, situação e prazo

#### Scenario: Pedido de dados com prazo vencido vem em atraso

- **WHEN** há solicitação de dados sem desfecho cujo prazo de 7 dias já venceu
- **THEN** ela vem marcada em atraso, e a situação gravada continua sendo **recebida**

#### Scenario: Quem não é Admin não lê a fila de dados

- **WHEN** um Mestre em sessão consulta a fila de solicitações de dados
- **THEN** o núcleo responde 403

### Requirement: O Admin aprova ou recusa a solicitação de dados sob os três critérios

O núcleo SHALL aceitar de um **Admin** em sessão o desfecho da solicitação de dados,
**aceita** ou **recusada**, com **parecer obrigatório**. A aprovação SHALL exigir, além do
parecer, o **compromisso de não tentar reidentificar ninguém**, afirmado no ato do desfecho;
sem ele o núcleo SHALL recusar com **422**. O parecer vazio SHALL ser recusado com **422**,
tanto na aprovação quanto na recusa. (`RF-02-78`, `RF-02-93`, `RF-01-46`, `RN-01-48`)

Os três critérios de aprovação SHALL ser: **solicitante identificado** — garantido no registro
—, **finalidade declarada compatível** — apurada pelo Admin no parecer — e **compromisso de não
reidentificação** — afirmado no desfecho. (`RF-02-93`, `RN-02-26`)

**Nenhum conjunto de dados** SHALL sair sem aprovação de Admin registrada, e a entrega SHALL
ser **gratuita** e **anonimizada**. O núcleo SHALL registrar **o que foi entregue e a quem**.
(`RF-02-79`, `RF-01-47`, `RN-02-26`, invariante 17 do documento 99 §6)

A solicitação já avaliada NEVER SHALL ser reavaliada: novo desfecho SHALL ser recusado com
**409**. Quem não for Admin SHALL receber **403**, e toda escrita SHALL entrar na trilha de
auditoria. (`RN-02-01`, `RN-02-21`)

#### Scenario: Admin aprova com o compromisso afirmado

- **WHEN** um Admin conclui a solicitação de dados como aceita, com parecer e afirmando o
  compromisso de não reidentificação
- **THEN** o núcleo grava a situação aceita, o parecer, o autor e a data

#### Scenario: Aprovação sem o compromisso é recusada

- **WHEN** um Admin conclui como aceita, com parecer, mas sem afirmar o compromisso de não
  reidentificação
- **THEN** o núcleo responde 422 e nada é gravado

#### Scenario: Desfecho sem parecer é recusado

- **WHEN** um Admin conclui a solicitação de dados com o parecer vazio
- **THEN** o núcleo responde 422 e nada é gravado

#### Scenario: Nenhum conjunto sai sem aprovação registrada

- **WHEN** alguém tenta liberar um conjunto de dados de uma solicitação sem desfecho ou
  recusada
- **THEN** o núcleo recusa a liberação

#### Scenario: A entrega aprovada fica registrada

- **WHEN** um conjunto de dados é liberado sobre uma solicitação aprovada
- **THEN** o núcleo registra o que foi entregue e a quem, e a entrega é gratuita e anonimizada

#### Scenario: Solicitação de dados avaliada não se reavalia

- **WHEN** um Admin envia novo desfecho para uma solicitação de dados já avaliada
- **THEN** o núcleo responde 409 e o desfecho original permanece

### Requirement: A gestão lê a fila de solicitações de chave

O núcleo SHALL devolver as solicitações de chave com **quem pediu** e **o que pretende
construir**, mais a **situação**, o **prazo** e, quando já houver desfecho, **quem avaliou**, o
**parecer** e a **data**. A leitura SHALL ser paginada, SHALL marcar o **atraso** derivado do
prazo e SHALL indicar se a solicitação **já rendeu chave**. (`RF-02-87`, `RF-01-49`,
`RN-01-49`, `RN-01-51`)

A leitura SHALL exigir **Admin** em sessão; os demais papéis SHALL receber **403**.
(`RF-01-16`, `RN-02-27`)

A leitura NEVER SHALL devolver o segredo da chave, em nenhuma situação. (`RN-02-28`,
`RN-01-35`)

#### Scenario: Admin lê a fila de pedidos de chave

- **WHEN** um Admin em sessão consulta a fila de solicitações de chave
- **THEN** vêm as solicitações com quem pediu, o que pretende construir, situação e prazo

#### Scenario: Solicitação que já rendeu chave vem marcada

- **WHEN** a fila devolve uma solicitação aceita sobre a qual a chave já foi emitida
- **THEN** ela vem indicando que a chave já foi emitida

#### Scenario: A fila de chaves nunca devolve o segredo

- **WHEN** a fila devolve uma solicitação que já rendeu chave
- **THEN** o segredo não aparece em nenhum campo

### Requirement: O Admin aprova ou recusa a solicitação de chave, e a emissão vem depois

O núcleo SHALL aceitar de um **Admin** em sessão o desfecho da solicitação de chave,
**aceita** ou **recusada**, gravando o **parecer**, o **autor** e a **data**. O desfecho
NEVER SHALL emitir chave: a emissão SHALL continuar sendo ato separado, sobre solicitação já
aceita, e SHALL devolver o segredo uma única vez. (`RF-02-88`, `RF-02-89`, `RF-01-49`,
`RF-01-50`, `RN-02-27`, `RN-01-51`)

Decisão do fundador em 2026-08-22, que completa o PRD-02 §9: o desfecho da solicitação de
chave é rota própria, simétrica às das outras naturezas, e `POST /v1/chaves` segue emitindo
apenas sobre solicitação já aceita.

A solicitação já avaliada NEVER SHALL ser reavaliada: novo desfecho SHALL ser recusado com
**409**. Quem não for Admin SHALL receber **403**, e toda escrita SHALL entrar na trilha de
auditoria. (`RN-02-01`, `RN-02-21`)

#### Scenario: Admin aprova o pedido de chave sem emitir nada

- **WHEN** um Admin conclui a solicitação de chave como aceita, com parecer
- **THEN** o núcleo grava o desfecho e **nenhuma chave é emitida** por esse ato

#### Scenario: A emissão só alcança solicitação aceita

- **WHEN** um Admin tenta emitir a chave de uma solicitação recusada ou ainda sem desfecho
- **THEN** o núcleo recusa a emissão

#### Scenario: Aprovada, a emissão passa a ser possível

- **WHEN** um Admin emite a chave de uma solicitação que ele aprovou
- **THEN** o núcleo emite a chave e devolve o segredo uma única vez

#### Scenario: Admin recusa o pedido de chave com o motivo

- **WHEN** um Admin conclui a solicitação de chave como recusada, com o motivo no parecer
- **THEN** o núcleo grava a recusa com o motivo, o autor e a data, e nenhuma chave existe

#### Scenario: Quem não é Admin não avalia pedido de chave

- **WHEN** um Apoiador em sessão tenta concluir uma solicitação de chave
- **THEN** o núcleo responde 403 e nada é gravado

### Requirement: A gestão lê a fila única de sugestões e propostas

O núcleo SHALL devolver as sugestões e propostas com o **autor** e a **persona** de quem
propôs, o teor, a **situação**, o **prazo** e, quando já houver desfecho, **quem avaliou**, o
**parecer**, o **motivo do retorno** e a **data**. A leitura SHALL ser paginada, SHALL reunir
numa fila só o que vem das Apps 05, 07, 08 e 09 e SHALL marcar o **atraso** derivado do prazo.
(`RF-02-25`, `RF-01-25`, `RN-01-49`)

A leitura SHALL exigir **Admin** em sessão; os demais papéis SHALL receber **403**.
(`RF-01-16`, `RN-02-01`)

#### Scenario: Admin lê a fila de sugestões das quatro aplicações

- **WHEN** um Admin em sessão consulta a fila de sugestões
- **THEN** vêm as sugestões das Apps 05, 07, 08 e 09 numa lista só, cada uma identificando o
  autor e a persona dele

#### Scenario: Sugestão com prazo vencido vem em atraso

- **WHEN** há sugestão sem desfecho cujo prazo de 7 dias já venceu
- **THEN** ela vem marcada em atraso

### Requirement: O Admin avalia a sugestão e o retorno chega a quem propôs

O núcleo SHALL aceitar de um **Admin** em sessão o desfecho da sugestão, **adotada** ou **não
adotada**, gravando o **parecer**, o **autor** e a **data**. A sugestão **não adotada** SHALL
exigir o **motivo do retorno** em linguagem simples, sem o qual o núcleo SHALL recusar com
**422**, e SHALL marcar a data de descarte da transcrição, 90 dias à frente. A sugestão
**adotada** SHALL creditar **20 pontos extras** e o **badge de protagonismo** a quem propôs, na
mesma operação, e SHALL guardar transcrição e autoria de forma permanente. (`RF-02-26`,
`RF-01-25`, `RF-01-56`, `RN-01-50`)

O crédito SHALL ser **idempotente**: regravar o desfecho adotada NEVER SHALL creditar de novo.

O retorno a quem propôs SHALL acontecer **dentro da plataforma**, e o núcleo NEVER SHALL
enviar e-mail por causa dele. (`RN-02-25`)

A sugestão já avaliada NEVER SHALL ser reavaliada: novo desfecho SHALL ser recusado com
**409**. Quem não for Admin SHALL receber **403**, e toda escrita SHALL entrar na trilha de
auditoria. (`RN-02-01`, `RN-02-21`)

#### Scenario: Sugestão adotada credita os extras e o badge

- **WHEN** um Admin conclui uma sugestão como adotada
- **THEN** o núcleo grava o desfecho e credita 20 pontos extras e o badge de protagonismo a
  quem propôs, na mesma operação

#### Scenario: O crédito da sugestão adotada não se repete

- **WHEN** o desfecho adotada é gravado sobre uma sugestão que já foi creditada
- **THEN** nenhum ponto extra e nenhum badge são creditados de novo

#### Scenario: Sugestão não adotada exige o motivo do retorno

- **WHEN** um Admin conclui uma sugestão como não adotada sem informar o motivo do retorno
- **THEN** o núcleo responde 422 e nada é gravado

#### Scenario: Sugestão não adotada marca o descarte da transcrição

- **WHEN** um Admin conclui uma sugestão como não adotada com o motivo do retorno
- **THEN** o núcleo grava o motivo e a data de descarte da transcrição, 90 dias à frente

#### Scenario: Sugestão avaliada não se reavalia

- **WHEN** um Admin envia novo desfecho para uma sugestão já avaliada
- **THEN** o núcleo responde 409 e o desfecho original permanece
