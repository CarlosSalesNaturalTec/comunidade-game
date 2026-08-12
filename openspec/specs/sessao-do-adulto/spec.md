## Purpose

O adulto — Mestre, Apoiador, responsável ou Admin — entra por login social, ou por usuário e
senha quando não tem conta social. Esta capacidade cobre como essa sessão abre, o que acontece
com quem não tem cadastro, a trava que a senha provisória impõe até ser trocada, e como a
sessão termina.

## Requirements

### Requirement: Adulto abre sessão por login social vinculado a cadastro existente

O núcleo SHALL abrir sessão para o adulto que autentica por login social **associado a uma
persona já cadastrada**. O login SHALL apenas autenticar: NEVER SHALL criar persona, papel ou
vínculo. (`RF-01-09`, `RN-01-04`)

#### Scenario: Conta social com cadastro abre sessão

- **WHEN** um adulto autentica por login social e a identidade corresponde a uma persona
  cadastrada
- **THEN** o núcleo abre a sessão dele com o papel que a persona já tinha

#### Scenario: O login não altera a persona

- **WHEN** a sessão de um adulto é aberta por login social
- **THEN** o papel, o vínculo e os demais dados da persona permanecem como estavam

### Requirement: Login sem cadastro correspondente é recusado sem criar persona

O núcleo SHALL recusar com **403** o login social ou o usuário que não corresponda a uma persona
cadastrada, e NEVER SHALL criar persona nessa recusa. A resposta SHALL orientar quem quer ser
Mestre ou Apoiador a usar o formulário de solicitação da vitrine. (`RF-01-10`, `RN-01-04`,
PRD-01 §§5.2, 9 e 12)

#### Scenario: Conta social sem cadastro é recusada

- **WHEN** um adulto autentica por login social com identidade que não corresponde a nenhuma
  persona
- **THEN** o núcleo responde 403, com a orientação de solicitar participação pela vitrine, e
  nenhuma persona passa a existir

#### Scenario: Usuário inexistente é recusado do mesmo modo

- **WHEN** uma autenticação por usuário e senha chega com usuário que não corresponde a nenhuma
  credencial
- **THEN** o núcleo responde 403 e nenhuma persona passa a existir

### Requirement: Adulto sem conta social abre sessão por usuário e senha

O núcleo SHALL abrir sessão para o adulto que autentica com o usuário e a senha da credencial
criada por Admin ou Mestre, com **o mesmo vínculo e as mesmas permissões** da persona.
(`RF-01-11`, `RN-01-18`, PRD-01 §5.2)

#### Scenario: Credencial válida abre sessão

- **WHEN** um adulto autentica com usuário e senha corretos de uma credencial ativa
- **THEN** o núcleo abre a sessão dele com o papel da persona vinculada

#### Scenario: Senha errada não abre sessão

- **WHEN** um adulto autentica com usuário existente e senha incorreta
- **THEN** o núcleo recusa e nenhuma sessão é aberta

### Requirement: Senha provisória trava a sessão até ser trocada

Enquanto a troca de senha estiver pendente, o núcleo SHALL aceitar da sessão **apenas** a rota
de troca de senha. Qualquer outra rota SHALL responder **403**. Trocada a senha, a pendência
SHALL cessar e a sessão SHALL passar a valer para o que o papel permite. (`RF-01-12`, PRD-01
§§9 e 12)

#### Scenario: Qualquer outra rota responde 403

- **WHEN** um adulto com troca de senha pendente chama uma rota que não é a da troca
- **THEN** o núcleo responde 403 e não executa nada da rota

#### Scenario: A rota de troca responde normalmente

- **WHEN** o mesmo adulto chama a rota de troca de senha
- **THEN** o núcleo processa a troca

#### Scenario: Trocada a senha, a trava cai

- **WHEN** o adulto conclui a troca da senha provisória
- **THEN** a pendência deixa de existir e as demais rotas passam a responder segundo o papel
  dele

#### Scenario: A senha provisória não serve para um segundo acesso

- **WHEN** a senha provisória já foi trocada e alguém tenta autenticar com ela de novo
- **THEN** o núcleo recusa a autenticação

### Requirement: A sessão termina por encerramento ou por expiração

O núcleo SHALL permitir que a persona encerre a própria sessão, e SHALL expirar a sessão ao fim
da sua duração. Chamada com sessão expirada ou encerrada SHALL receber **401**. A duração SHALL
ser parâmetro de configuração do ambiente, não valor fixado em código. (PRD-01 §§9, 10 e 14)

#### Scenario: A persona encerra a própria sessão

- **WHEN** uma persona autenticada pede o encerramento da sessão atual
- **THEN** o núcleo encerra a sessão, registrando quando ela foi encerrada

#### Scenario: Sessão encerrada não responde mais

- **WHEN** uma chamada chega com o token de uma sessão já encerrada
- **THEN** o núcleo responde 401

#### Scenario: Sessão expirada não responde mais

- **WHEN** uma chamada chega com o token de uma sessão cuja expiração já passou
- **THEN** o núcleo responde 401

#### Scenario: Uma sessão não alcança outra

- **WHEN** duas personas têm sessões abertas ao mesmo tempo e uma delas expira
- **THEN** a outra segue válida, e nenhum dado de uma sessão aparece na outra
