## Purpose

O espaço físico onde a plataforma acontece: cadastrado pela gestão e pertencente a uma
comunidade, é onde o recurso fica guardado e onde a aula acontece. É a dimensão do saldo — o
recurso fica onde é usado — e não se confunde com o local do território, que é a hierarquia
geográfica da coleta e pode ser pedido por um Guerreiro(a).

## Requirements

### Requirement: O ponto de apoio é cadastrado por Admin, com nome e comunidade

O núcleo SHALL manter o **ponto de apoio** com **nome** e **comunidade** a que pertence, ambos
obrigatórios. Cadastrar ponto de apoio SHALL exigir persona **Admin** em sessão; persona de
qualquer outro papel SHALL receber **403**. Cadastro sem nome ou sem comunidade SHALL ser
recusado com **422**, indicando o campo em falta, e comunidade inexistente SHALL ser recusada com
**422**. A escrita SHALL gravar autoria, data e hora com fuso, como toda escrita do núcleo.
(`RF-07-47`, `RN-07-33`, `RF-01-16`, `RF-01-03`, `RF-01-27`, PRD-07 §8)

#### Scenario: Admin cadastra um ponto de apoio

- **WHEN** um Admin em sessão cadastra um ponto de apoio com nome e comunidade
- **THEN** o núcleo grava o ponto de apoio com o autor, a data e a hora com fuso

#### Scenario: Mestre não cadastra ponto de apoio

- **WHEN** um Mestre em sessão tenta cadastrar um ponto de apoio
- **THEN** o núcleo responde 403 e nada é gravado

#### Scenario: Ponto de apoio sem comunidade é recusado

- **WHEN** chega um cadastro de ponto de apoio sem comunidade declarada
- **THEN** o núcleo responde 422 indicando o campo em falta e nada é gravado

#### Scenario: Ponto de apoio de comunidade inexistente é recusado

- **WHEN** chega um cadastro de ponto de apoio apontando comunidade que não existe
- **THEN** o núcleo responde 422 e nada é gravado

### Requirement: O responsável pelo acervo é designado depois do cadastro

O núcleo SHALL permitir que o ponto de apoio **exista sem responsável designado**, e SHALL
oferecer operação de **Admin** para **designar ou trocar** o responsável pelo acervo a qualquer
tempo. Persona de qualquer outro papel SHALL receber **403** ao tentar designar. A designação
SHALL recair sobre persona de papel **Admin**, **Mestre** ou **Apoiador**; persona de papel
**Guerreiro(a)** ou **responsável** SHALL ser recusada com **422**. Trocar o responsável SHALL
substituir o designado anterior, e cada designação SHALL gravar autoria, data e hora com fuso.
(`RF-07-49`, `RN-07-34`, `RN-07-10`, `RF-01-16`, `RF-01-03`, documento 05 §3)

#### Scenario: Ponto de apoio nasce sem responsável

- **WHEN** um Admin cadastra um ponto de apoio sem informar responsável
- **THEN** o núcleo grava o ponto de apoio e o responsável fica em aberto

#### Scenario: Admin designa um Mestre como responsável

- **WHEN** um Admin designa um Mestre como responsável pelo acervo de um ponto de apoio
- **THEN** o núcleo grava a designação com o autor, a data e a hora com fuso

#### Scenario: Apoiador pode ser designado responsável

- **WHEN** um Admin designa um Apoiador como responsável pelo acervo
- **THEN** o núcleo grava a designação

#### Scenario: Guerreiro(a) não é designado responsável

- **WHEN** um Admin tenta designar um Guerreiro(a) como responsável pelo acervo
- **THEN** o núcleo responde 422 e a designação anterior permanece como estava

#### Scenario: Responsável familiar não é designado responsável pelo acervo

- **WHEN** um Admin tenta designar uma persona de papel responsável como responsável pelo acervo
- **THEN** o núcleo responde 422 e nada muda

#### Scenario: Troca do responsável substitui o anterior

- **WHEN** um Admin designa um responsável para um ponto de apoio que já tinha outro
- **THEN** o núcleo passa a apontar o novo designado, e o registro da designação anterior
  permanece na trilha de auditoria

#### Scenario: Mestre não designa responsável

- **WHEN** um Mestre em sessão tenta designar o responsável pelo acervo
- **THEN** o núcleo responde 403 e nada é gravado

### Requirement: A gestão lê os pontos de apoio, filtrados por comunidade

O núcleo SHALL devolver os pontos de apoio com **nome**, **comunidade** a que pertencem,
**responsável designado** — quando já houver — e se estão **ativos**. A leitura SHALL ser
paginada e SHALL aceitar filtro por **comunidade**.

A leitura SHALL exigir persona de gestão em sessão: o **Admin** SHALL ler todas as comunidades e
o **Mestre**, apenas as comunidades a que está vinculado. **Apoiador**, **Guerreiro(a)** e
**responsável** SHALL receber **403**.

O ponto de apoio ainda **sem responsável designado** SHALL sair na leitura assim mesmo — a
designação é posterior ao cadastro, e a ausência dela NEVER SHALL impedir que o espaço seja
lido ou escolhido no agendamento. (`RF-07-47`, `RF-07-49`, `RF-01-28`, `RF-01-18`, `RF-01-16`,
`RN-07-34`, PRD-07 §§8, 10)

#### Scenario: Admin lê os pontos de apoio de uma comunidade

- **WHEN** um Admin em sessão consulta os pontos de apoio filtrando por uma comunidade
- **THEN** vêm apenas os pontos de apoio daquela comunidade, com nome, responsável designado e
  se estão ativos

#### Scenario: Mestre lê apenas os pontos de apoio das suas comunidades

- **WHEN** um Mestre vinculado a uma comunidade consulta os pontos de apoio
- **THEN** vêm apenas os daquela comunidade

#### Scenario: Guerreiro(a) não lê os pontos de apoio da gestão

- **WHEN** um Guerreiro(a) em sessão consulta os pontos de apoio
- **THEN** o núcleo responde 403

#### Scenario: Ponto de apoio sem responsável designado é lido assim mesmo

- **WHEN** um ponto de apoio recém-cadastrado, ainda sem responsável pelo acervo, é consultado
- **THEN** ele vem na leitura, com o responsável ausente e sem que isso seja erro

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
