## Purpose

As rotas de Admin que criam e editam a persona de cada papel no núcleo, o artefato
comprobatório que o adulto precisa declarar e a gravação do nick pelo Admin quando o nick
pretendido já pertence a alguém.

## ADDED Requirements

### Requirement: O Admin cadastra o Guerreiro(a) com nome, nascimento, nick e avatar

O núcleo SHALL expor rota de **Admin** que cria persona de Guerreiro(a) com **nome**, **data de
nascimento**, **nick** e **características do avatar**. Persona de qualquer outro papel SHALL
receber **403**. Cadastro sem um dos quatro SHALL ser recusado com **422**, indicando o campo em
falta, e nick já usado por qualquer persona SHALL ser recusado com **422** no campo `nick`, sem
dizer de quem é. A escrita SHALL gravar autoria, data e hora, como toda escrita do núcleo.
(`RF-02-01`, `RF-01-19`, `RN-01-30`, `RN-02-21`)

O onboarding conduzido pelo App 01, em que a própria criança se cadastra, é do PRD-04; esta
rota é o caminho da gestão.

#### Scenario: Admin cadastra o Guerreiro(a)

- **WHEN** um Admin em sessão cadastra um Guerreiro(a) com nome, nascimento, nick e avatar
- **THEN** o núcleo grava a persona com o autor, a data e a hora

#### Scenario: Cadastro sem nick é recusado

- **WHEN** chega o cadastro de um Guerreiro(a) sem nick
- **THEN** o núcleo responde 422 indicando o campo em falta e nada é gravado

#### Scenario: Nick em uso é recusado sem revelar o dono

- **WHEN** chega o cadastro de um Guerreiro(a) com nick já usado por outra persona
- **THEN** o núcleo responde 422 no campo `nick`, sem dizer de quem é o nick nem de que papel

#### Scenario: Mestre não cadastra Guerreiro(a)

- **WHEN** um Mestre em sessão tenta cadastrar um Guerreiro(a)
- **THEN** o núcleo responde 403 e nada é gravado

### Requirement: O Admin edita o Guerreiro(a) já cadastrado

O núcleo SHALL expor rota de **Admin** que edita nome, data de nascimento, nick e avatar de um
Guerreiro(a) existente, com as mesmas recusas do cadastro. A edição NEVER SHALL apagar a
persona nem trocar o papel dela, e SHALL entrar na trilha de auditoria como qualquer escrita.
(`RF-02-01`, `RN-02-21`)

#### Scenario: Admin corrige o nome do Guerreiro(a)

- **WHEN** um Admin em sessão edita o nome de um Guerreiro(a) existente
- **THEN** o núcleo grava o nome novo e a persona continua a mesma

#### Scenario: Edição para nick em uso é recusada

- **WHEN** um Admin edita um Guerreiro(a) atribuindo-lhe nick já usado por outra persona
- **THEN** o núcleo responde 422 no campo `nick` e o nick anterior permanece

### Requirement: O Admin cadastra Mestre e Apoiador com artefato comprobatório

O núcleo SHALL expor rota de **Admin** que cria persona de **Mestre** ou de **Apoiador** com
nome, e-mail, **WhatsApp opcional** e os **artefatos comprobatórios declarados** — cada um com
endereço e rótulo do que aponta. O cadastro SHALL exigir **ao menos um** artefato comprobatório
e SHALL ser recusado com **422** sem ele. O núcleo NEVER SHALL aceitar anexo de arquivo como
artefato no Ciclo 01: a prova é link declarado. (`RF-02-02`, `RF-02-03`, `RF-02-04`,
`RN-02-01`, invariante 3 do documento 99 §6, documento 02 §1)

O nick NÃO SHALL ser exigido no cadastro: o do Apoiador vem do pré-cadastro e o do Mestre é
definido por ele no primeiro acesso, e a persona existe sem ele.

#### Scenario: Admin cadastra Mestre com link comprobatório

- **WHEN** um Admin em sessão cadastra um Mestre com nome, e-mail e um link de currículo
- **THEN** o núcleo grava a persona com o artefato declarado

#### Scenario: Cadastro de adulto sem artefato é recusado

- **WHEN** chega o cadastro de um Mestre ou de um Apoiador sem artefato comprobatório algum
- **THEN** o núcleo responde 422 e nenhuma persona passa a existir

#### Scenario: Adulto é cadastrado sem nick

- **WHEN** um Admin cadastra um Mestre ou um Apoiador sem informar nick
- **THEN** o núcleo cria a persona sem nick, e ela existe à espera de recebê-lo

#### Scenario: Apoiador cadastrado diretamente recebe o nick do Admin

- **WHEN** um Admin cadastra um Apoiador informando um nick disponível
- **THEN** o núcleo grava o nick naquela persona

### Requirement: Novo Admin entra por inclusão manual de outro Admin

O núcleo SHALL expor rota de **Admin** que cria persona de **Admin**, com nome, e-mail e
WhatsApp opcional. Persona de qualquer outro papel SHALL receber **403**, e NEVER SHALL existir
caminho de autocadastro de Admin nem criação de Admin por login. (`RF-02-05`, `RN-02-02`,
invariante 3 do documento 99 §6)

#### Scenario: Admin inclui outro Admin

- **WHEN** um Admin em sessão cadastra outro Admin com nome e e-mail
- **THEN** o núcleo grava a persona de Admin com a autoria de quem a incluiu

#### Scenario: Apoiador não inclui Admin

- **WHEN** um Apoiador em sessão tenta cadastrar um Admin
- **THEN** o núcleo responde 403 e nada é gravado

### Requirement: O Admin grava o nick do adulto quando a escolha dele colidiu

O núcleo SHALL expor rota de **Admin** que define ou troca o nick de uma persona de **Apoiador
ou Mestre**, sujeita à mesma unicidade global de qualquer gravação de nick. É o desfecho da
colisão: o nick pretendido pertencia a outra persona, o cadastro nasceu sem nick, e o Admin
grava aqui o nick que a pessoa lhe passou por canal fora da plataforma. A rota NEVER SHALL
alcançar persona de Guerreiro(a) — o nick da criança se edita pela rota de edição dela — e
SHALL entrar na trilha de auditoria. (`RF-02-01`, `RN-01-30`, `RN-14-10`, `RN-02-21`)

#### Scenario: Admin grava o nick de um Apoiador que estava sem

- **WHEN** um Admin em sessão grava um nick disponível numa persona de Apoiador sem nick
- **THEN** o núcleo grava o nick, com autoria, data e hora

#### Scenario: Admin troca o nick de um Mestre

- **WHEN** um Admin em sessão troca o nick de um Mestre por outro disponível
- **THEN** o núcleo grava o nick novo e o anterior deixa de estar em uso

#### Scenario: Nick em uso é recusado também para o Admin

- **WHEN** um Admin tenta gravar num adulto um nick já usado por outra persona
- **THEN** o núcleo responde 422 no campo `nick` e nada é gravado

#### Scenario: A rota do Admin não alcança Guerreiro(a)

- **WHEN** um Admin usa esta rota apontando uma persona de Guerreiro(a)
- **THEN** o núcleo recusa a operação e nada é gravado
