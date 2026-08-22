## ADDED Requirements

### Requirement: O Admin desativa e reativa o ponto de apoio pela aplicação

A App 03 SHALL oferecer ao Admin, no ponto de apoio já cadastrado, as ações de **desativar** e
**reativar**, cada uma exigindo motivo antes de confirmar. A lista de pontos de apoio SHALL
distinguir o ativo do inativo, e o inativo SHALL continuar visível — é histórico, não some. As
ações NEVER SHALL ser oferecidas a quem não é Admin. (`RF-07-47`, `RN-07-33`, `RN-02-21`,
PRD-02 §4)

#### Scenario: Admin desativa um ponto de apoio

- **WHEN** um Admin em sessão desativa um ponto de apoio informando o motivo
- **THEN** o ponto passa a aparecer como inativo na lista, e o motivo fica registrado

#### Scenario: Inativo continua na lista

- **WHEN** um Admin abre a lista de pontos de apoio de uma comunidade que tem um inativo
- **THEN** o inativo aparece, distinguido do ativo

#### Scenario: Mestre não vê a ação

- **WHEN** um Mestre em sessão abre um ponto de apoio
- **THEN** as ações de desativar e reativar não lhe são oferecidas

#### Scenario: Sem motivo não confirma

- **WHEN** o Admin tenta confirmar a desativação com o motivo vazio
- **THEN** a aplicação aponta o campo em falta e nada é enviado ao núcleo

### Requirement: A recusa da desativação diz o que está prendendo o espaço

A App 03 SHALL apresentar em linguagem simples por que a desativação foi recusada: **quantas
aulas futuras** prendem o ponto de apoio, ou **quais tipos de recurso** ainda têm saldo nele. A
aplicação SHALL oferecer, na recusa por saldo, o caminho da **transferência**, e NEVER SHALL
apresentar código de erro cru. (`RF-07-47`, `RN-07-01`, `RN-07-15`, PRD-02 §10)

#### Scenario: Recusa por aula futura é explicada

- **WHEN** o núcleo recusa a desativação porque há aulas futuras no ponto de apoio
- **THEN** a aplicação diz quantas aulas o prendem, sem jargão de TI

#### Scenario: Recusa por saldo oferece a transferência

- **WHEN** o núcleo recusa a desativação porque ainda há saldo no ponto de apoio
- **THEN** a aplicação diz quais tipos têm saldo e oferece o caminho de transferi-los

### Requirement: O Admin transfere o saldo de um ponto de apoio para outro

A App 03 SHALL oferecer ao Admin a **transferência** de um tipo de recurso de um ponto de apoio
para outro, informando tipo, quantidade, destino e motivo. A aplicação SHALL apresentar o saldo
disponível na origem antes de confirmar, NEVER SHALL oferecer como destino um ponto de apoio
inativo nem o próprio ponto de origem, e SHALL apresentar a transferência confirmada como **um
fato só**, não como dois lançamentos soltos. (`RF-07-19`, `RN-07-15`, `RN-07-33`)

#### Scenario: Admin transfere um tipo de recurso

- **WHEN** um Admin informa tipo, quantidade, ponto de apoio de destino e motivo, e confirma
- **THEN** a transferência acontece e os saldos dos dois pontos de apoio aparecem atualizados

#### Scenario: O destino inativo não é oferecido

- **WHEN** o Admin escolhe o destino da transferência
- **THEN** os pontos de apoio inativos e o próprio ponto de origem não aparecem entre as
  opções

#### Scenario: Quantidade acima do saldo é barrada antes de enviar

- **WHEN** o Admin informa quantidade maior que o saldo disponível na origem
- **THEN** a aplicação aponta o limite e nada é enviado ao núcleo
