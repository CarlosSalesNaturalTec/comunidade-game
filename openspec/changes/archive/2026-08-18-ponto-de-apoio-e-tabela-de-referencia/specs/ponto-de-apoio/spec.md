## Purpose

O espaço físico onde a plataforma acontece: cadastrado pela gestão e pertencente a uma
comunidade, é onde o recurso fica guardado e onde a aula acontece. É a dimensão do saldo — o
recurso fica onde é usado — e não se confunde com o local do território, que é a hierarquia
geográfica da coleta e pode ser pedido por um Guerreiro(a).

## ADDED Requirements

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
