## ADDED Requirements

### Requirement: O Admin desativa e reativa o ponto de apoio

O núcleo SHALL expor operação de **Admin** que desativa um ponto de apoio e operação que o
reativa, ambas gravando **motivo**, autoria, data e hora com fuso. Persona de qualquer outro
papel SHALL receber **403**. A desativação NEVER SHALL apagar o ponto de apoio nem desfazer
vínculo algum: aula passada, lançamento e item patrimonial que o referenciam SHALL permanecer
intactos e continuar sendo lidos. Desativar ponto de apoio já inativo, ou reativar ponto já
ativo, SHALL ser recusado com **422**. (`RF-07-47`, `RN-07-33`, `RF-01-03`, `RF-01-27`,
`RN-02-21`, documento 05 §2)

#### Scenario: Admin desativa um ponto de apoio

- **WHEN** um Admin em sessão desativa um ponto de apoio sem aula futura e sem saldo, com
  motivo
- **THEN** o núcleo grava a desativação com o motivo, o autor, a data e a hora, e o ponto passa
  a sair como inativo na leitura da gestão

#### Scenario: Admin reativa um ponto de apoio

- **WHEN** um Admin em sessão reativa um ponto de apoio inativo, com motivo
- **THEN** o núcleo grava a reativação e o ponto volta a sair como ativo

#### Scenario: Mestre não desativa ponto de apoio

- **WHEN** um Mestre em sessão tenta desativar um ponto de apoio
- **THEN** o núcleo responde 403 e nada é gravado

#### Scenario: Desativação sem motivo é recusada

- **WHEN** chega uma desativação sem motivo declarado
- **THEN** o núcleo responde 422 indicando o campo em falta e nada é gravado

#### Scenario: A aula passada continua apontando o ponto desativado

- **WHEN** um ponto de apoio com aulas já realizadas é desativado
- **THEN** aquelas aulas continuam apontando o ponto de apoio, e a leitura delas não muda

### Requirement: Aula futura no ponto de apoio bloqueia a desativação

O núcleo SHALL recusar com **422** a desativação de ponto de apoio que tenha **aula agendada
ainda por acontecer** nele, e a recusa SHALL informar **quantas** aulas o prendem, para o Admin
saber o que remanejar. Aula já realizada e aula cancelada NEVER SHALL bloquear a desativação.

Como toda reserva de recurso herda a aula que a criou, o bloqueio por aula futura já alcança as
reservas ainda abertas: não existe reserva viva sem aula futura que a sustente. (`RF-07-47`,
`RN-07-01`, `RN-07-33`, PRD-07 §8)

#### Scenario: Ponto de apoio com aula futura não é desativado

- **WHEN** um Admin tenta desativar um ponto de apoio com uma aula agendada para depois de
  agora
- **THEN** o núcleo responde 422 informando quantas aulas o prendem, e o ponto continua ativo

#### Scenario: Aula já realizada não bloqueia

- **WHEN** um Admin desativa um ponto de apoio cujas aulas são todas passadas ou canceladas
- **THEN** o núcleo grava a desativação

#### Scenario: Cancelada a aula, a desativação passa

- **WHEN** a única aula futura de um ponto de apoio é cancelada e o Admin tenta desativá-lo de
  novo
- **THEN** o núcleo grava a desativação

### Requirement: Saldo guardado bloqueia a desativação até ser transferido

O núcleo SHALL recusar com **422** a desativação de ponto de apoio que ainda tenha **saldo de
qualquer tipo de recurso** guardado nele, e a recusa SHALL informar quais tipos ainda têm
saldo. O saldo sai do espaço pela **transferência** para outro ponto de apoio, que é lançamento
como qualquer outro movimento — nunca por edição, nunca por zeramento direto. (`RF-07-47`,
`RN-07-15`, `RN-07-33`, documento 05 §2)

#### Scenario: Ponto de apoio com saldo não é desativado

- **WHEN** um Admin tenta desativar um ponto de apoio com saldo de um tipo de recurso
- **THEN** o núcleo responde 422 informando os tipos com saldo, e o ponto continua ativo

#### Scenario: Transferido o saldo, a desativação passa

- **WHEN** todo o saldo de um ponto de apoio é transferido para outro e o Admin o desativa
- **THEN** o núcleo grava a desativação

#### Scenario: O saldo nunca é zerado por edição

- **WHEN** se procura no núcleo um caminho que zere o saldo de um ponto de apoio sem lançamento
- **THEN** nenhum existe
