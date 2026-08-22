## ADDED Requirements

### Requirement: A área Filas serve as quatro naturezas sob o mesmo filtro

A App 03 SHALL apresentar, na área Filas já existente, também as solicitações de **dados**, as
de **chave** e as **sugestões e propostas**, sob o mesmo filtro por natureza e com a mesma
apresentação do atraso. A aplicação NEVER SHALL abrir área separada para nenhuma delas.
(`RF-02-25`, `RF-02-77`, `RF-02-87`, PRD-02 §6.2)

Cada natureza SHALL mostrar o que lhe é próprio: a de dados, o solicitante, a instituição, a
finalidade declarada e o recorte pedido; a de chave, quem pediu e o que pretende construir; a
sugestão, o autor, a persona dele e o teor. (`RF-02-77`, `RF-02-87`, `RF-02-25`)

#### Scenario: O filtro alcança as quatro naturezas

- **WHEN** um Admin em sessão abre a área Filas e percorre o filtro por natureza
- **THEN** pode ver participação, dados, chave e sugestões, cada uma com os seus campos

#### Scenario: Cada natureza mostra o que lhe é próprio

- **WHEN** o Admin filtra pela natureza dados
- **THEN** cada item traz solicitante, instituição, finalidade declarada e recorte pedido

### Requirement: A tela da solicitação de dados apresenta ao Admin os três critérios

A App 03 SHALL apresentar, na avaliação da solicitação de dados, os **três critérios de
aprovação** — solicitante identificado, finalidade compatível e não reidentificação — e SHALL
exigir do Admin a afirmação do **compromisso de não reidentificação** antes de aprovar. O
parecer SHALL ser obrigatório na aprovação e na recusa, apontado no próprio campo antes de
chamar o núcleo. (`RF-02-93`, `RF-02-78`, `RN-02-26`)

A aplicação SHALL apresentar, depois do desfecho, **o que foi entregue e a quem**, e SHALL
deixar claro que a entrega é **gratuita e anonimizada**. (`RF-02-79`)

#### Scenario: Os critérios aparecem antes da decisão

- **WHEN** um Admin abre uma solicitação de dados para avaliar
- **THEN** a tela apresenta os três critérios de aprovação antes de oferecer aprovar ou recusar

#### Scenario: Aprovar exige afirmar o compromisso

- **WHEN** o Admin escolhe aprovar sem marcar o compromisso de não reidentificação
- **THEN** a aplicação aponta a falta junto do rótulo e nada é enviado ao núcleo

#### Scenario: A entrega registrada aparece na tela

- **WHEN** o Admin abre uma solicitação de dados já aprovada e entregue
- **THEN** a tela mostra o que foi entregue e a quem, e diz que a entrega foi gratuita e
  anonimizada

### Requirement: A aprovação do pedido de chave e a emissão são dois atos na tela

A App 03 SHALL oferecer ao Admin, sobre a solicitação de chave, primeiro o **desfecho** —
aprovar ou recusar, com parecer — e só depois, sobre a solicitação aprovada, a **emissão**. A
aplicação NEVER SHALL emitir a chave no mesmo ato da aprovação. (`RF-02-88`, `RF-02-89`)

A emissão SHALL apresentar o **identificador** e o **segredo**, com o aviso de que o segredo
aparece **uma única vez** e não é recuperável depois. A aplicação NEVER SHALL guardar o segredo
nem reapresentá-lo em consulta posterior. (`RF-02-89`, `RN-02-28`)

A solicitação que já rendeu chave NEVER SHALL oferecer emissão de novo.

#### Scenario: Aprovar não emite

- **WHEN** um Admin aprova uma solicitação de chave
- **THEN** a tela mostra o desfecho gravado e passa a oferecer a emissão como ato seguinte

#### Scenario: O segredo é mostrado uma vez, com o aviso

- **WHEN** o Admin emite a chave
- **THEN** a tela apresenta o identificador e o segredo, avisando que o segredo não será
  mostrado de novo

#### Scenario: O segredo não volta numa consulta posterior

- **WHEN** o Admin volta à mesma solicitação depois de sair da tela de emissão
- **THEN** o segredo não aparece, e a tela mostra apenas que a chave foi emitida

#### Scenario: Solicitação que já rendeu chave não emite outra

- **WHEN** o Admin abre uma solicitação aprovada cuja chave já foi emitida
- **THEN** a tela não oferece emitir de novo

### Requirement: A aplicação apresenta o painel das chaves emitidas

A App 03 SHALL apresentar ao Admin as chaves emitidas com **prazo de apresentação**, **URL
apresentada** quando houver e **situação**, e SHALL **destacar** as que estão com o prazo a
vencer e as **revogadas automaticamente por prazo vencido**. O destaque SHALL ser legível sem
distinguir cores. (`RF-02-90`, `RF-02-91`, `RN-02-29`, documento 15 §5)

A App 03 SHALL oferecer ao Admin a **revogação a qualquer tempo, com motivo**, exigido antes de
chamar o núcleo. (`RF-02-92`)

O painel NEVER SHALL apresentar o segredo nem o seu resumo criptográfico. (`RN-02-28`)

#### Scenario: O painel mostra o ciclo de vida de cada chave

- **WHEN** um Admin em sessão abre o painel de chaves
- **THEN** cada chave aparece com prazo, URL apresentada quando houver e situação

#### Scenario: Prazo a vencer e revogação por decurso são destacados por rótulo

- **WHEN** o painel traz uma chave com prazo a vencer e outra revogada por prazo vencido
- **THEN** as duas vêm com rótulo textual que diz isso, legível também sem distinguir cores

#### Scenario: Revogar exige o motivo

- **WHEN** o Admin escolhe revogar uma chave e confirma sem informar o motivo
- **THEN** a aplicação aponta o campo em falta e nada é enviado ao núcleo

#### Scenario: O painel nunca mostra o segredo

- **WHEN** o painel apresenta qualquer chave
- **THEN** o segredo não aparece em campo algum

### Requirement: O Admin avalia a sugestão e a tela mostra o retorno a quem propôs

A App 03 SHALL oferecer ao Admin o desfecho da sugestão — **adotada** ou **não adotada** —, com
o **motivo do retorno** exigido na não adotada, em linguagem simples, apontado antes de chamar
o núcleo. A tela SHALL apresentar, depois do desfecho, o retorno que chegará a quem propôs.
(`RF-02-26`, `RN-02-25`)

A aplicação SHALL apresentar, na sugestão adotada, que **20 pontos extras e o badge de
protagonismo** foram creditados a quem propôs. (`RF-01-56`, `RN-01-50`)

Todo o retorno SHALL acontecer **dentro da plataforma**: a aplicação NEVER SHALL oferecer envio
por e-mail. (`RN-02-25`)

#### Scenario: Não adotada exige o motivo do retorno

- **WHEN** o Admin escolhe não adotar e confirma sem o motivo do retorno
- **THEN** a aplicação aponta o campo em falta e nada é enviado ao núcleo

#### Scenario: Adotada mostra o que foi creditado

- **WHEN** o Admin adota uma sugestão
- **THEN** a tela mostra que 20 pontos extras e o badge de protagonismo foram creditados a quem
  propôs

#### Scenario: O retorno não sai por e-mail

- **WHEN** o Admin conclui a avaliação de uma sugestão
- **THEN** a aplicação não oferece envio por e-mail, e o retorno fica dentro da plataforma
