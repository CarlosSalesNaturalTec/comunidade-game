## Purpose

A persona é quem age no núcleo: os cinco papéis do PRD-01 §4, o vínculo de comunidade que
prende o Guerreiro(a) a um território, e as credenciais que ligam uma pessoa real a esse
registro. Esta capacidade cobre quem pode existir, quem cria quem, e o caso de exceção do
adulto que não tem conta social — inclusive a única persona que não é criada por ninguém: a do
fundador, semeada na implantação.

## ADDED Requirements

### Requirement: A persona existe nos cinco papéis

O núcleo SHALL manter a persona nos cinco papéis do PRD-01 §4 — Admin, Mestre, Guerreiro(a),
Responsável e Apoiador. Toda persona SHALL carregar o papel que exerce, e o papel SHALL ser o
que determina o que ela escreve e o que ela lê. (`RF-01-19`)

Vínculo de responsável e consentimento, que `RF-01-19` também nomeia, são da fatia seguinte:
esta cobre a persona.

#### Scenario: Persona carrega o papel que exerce

- **WHEN** uma persona é criada no núcleo, por qualquer caminho
- **THEN** o registro dela declara qual dos cinco papéis ela exerce

#### Scenario: Papel ausente não produz persona

- **WHEN** uma criação de persona chega sem papel declarado
- **THEN** o núcleo recusa a criação e nenhuma persona passa a existir

### Requirement: Só o Guerreiro(a) tem autocadastro

O núcleo SHALL aceitar autocadastro apenas do Guerreiro(a). Mestre e Apoiador SHALL ser
cadastrados por Admin; o responsável, por Admin ou Mestre; e Admin novo SHALL entrar apenas por
inclusão de outro Admin. Login NEVER SHALL criar persona. (`RN-01-01`, `RN-01-02`, `RN-01-04`)

#### Scenario: Adulto não se autocadastra

- **WHEN** uma criação de persona de Mestre, Apoiador ou responsável chega sem a autoria de um
  Admin — ou de um Mestre, no caso do responsável
- **THEN** o núcleo recusa a criação

#### Scenario: Admin novo exige Admin existente

- **WHEN** uma criação de persona de Admin chega sem a autoria de outro Admin
- **THEN** o núcleo recusa a criação, ressalvada a semeadura da implantação

### Requirement: Guerreiro(a) tem vínculo obrigatório a exatamente uma comunidade

O núcleo SHALL exigir que toda persona de Guerreiro(a) tenha vínculo a **exatamente uma**
Comunidade Virtual. A persona de Guerreiro(a) NEVER SHALL existir sem comunidade nem com mais de
uma vigente. (`RN-01-05`)

O comportamento da Comunidade Virtual — criação, hierarquia de locais, transferência — é do
PRD-08; aqui ela existe como entidade para que o vínculo e o filtro tenham a que apontar
(`RF-01-23`).

#### Scenario: Guerreiro(a) sem comunidade não é criado

- **WHEN** uma criação de persona de Guerreiro(a) chega sem comunidade
- **THEN** o núcleo recusa a criação

#### Scenario: Segundo vínculo vigente é recusado

- **WHEN** um segundo vínculo de comunidade vigente é pedido para o mesmo Guerreiro(a)
- **THEN** o núcleo recusa, e o vínculo existente permanece

### Requirement: A implantação semeia a persona Admin do fundador

O núcleo SHALL criar, na implantação, a persona Admin do fundador, a partir da identidade social
declarada no ambiente. Essa SHALL ser a única persona criada sem a autoria de outro Admin, e a
semeadura NEVER SHALL criar uma segunda persona de qualquer outro papel. (`RF-01-61`,
documento 02 §1)

#### Scenario: A implantação cria o Admin fundador

- **WHEN** a implantação de um ambiente é executada com a identidade social do fundador
  declarada
- **THEN** existe naquele ambiente uma persona Admin vinculada àquela identidade social

#### Scenario: Semear duas vezes não duplica a persona

- **WHEN** a implantação do mesmo ambiente é executada de novo
- **THEN** a persona Admin do fundador permanece a mesma, sem duplicata

#### Scenario: Sem identidade declarada não há semeadura

- **WHEN** a implantação é executada sem a identidade social do fundador declarada
- **THEN** o núcleo não cria persona alguma e a implantação falha de forma visível

#### Scenario: O Admin semeado entra pelo caminho comum

- **WHEN** o fundador autentica por login social com a identidade que foi semeada
- **THEN** o núcleo abre a sessão dele como abriria a de qualquer adulto com cadastro existente

### Requirement: Admin ou Mestre cria credencial de usuário e senha provisória

O núcleo SHALL permitir que Admin ou Mestre crie, para adulto sem conta social, uma credencial
de **usuário e senha provisória**, com o mesmo vínculo e as mesmas permissões que a persona já
tem. O usuário NOT SHALL precisar ser um e-mail. A senha SHALL ser guardada com hash, SHALL
valer para um único acesso e SHALL ser trocada pelo próprio adulto. (`RF-01-11`, `RN-01-18`)

#### Scenario: Credencial provisória nasce marcada para troca

- **WHEN** um Admin ou um Mestre cria a credencial de usuário e senha provisória de um adulto
- **THEN** a credencial nasce com a troca de senha pendente, e a senha é guardada apenas como
  hash

#### Scenario: Credencial não amplia o que a persona pode

- **WHEN** um adulto passa a ter credencial de usuário e senha além do vínculo que já tinha
- **THEN** o que ele escreve e lê continua sendo o do papel da persona, sem acréscimo

#### Scenario: Quem não é Admin nem Mestre não cria credencial

- **WHEN** uma persona de outro papel tenta criar credencial de usuário e senha
- **THEN** o núcleo responde 403 e nenhuma credencial é criada

#### Scenario: A senha em claro não é recuperável

- **WHEN** a credencial provisória já foi criada
- **THEN** nenhuma rota, consulta ou registro operacional devolve a senha em claro
