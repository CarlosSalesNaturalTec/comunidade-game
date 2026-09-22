## ADDED Requirements

### Requirement: Operação com escopo confere o vínculo, além do papel

A matriz do PRD-01 §4 diz o que **cada papel** pode. Algumas operações SHALL ter, além disso,
**escopo**: o papel abre a porta, e o vínculo diz sobre **quem** ela se abre. A primeira é a
**confirmação de identidade do Guerreiro(a) pelo responsável**, que alcança apenas os Guerreiros
e Guerreiras sob a responsabilidade dele, por vínculo de responsável **vigente**. (`RF-01-74`,
`RF-01-16`, PRD-01 §4)

O escopo SHALL ser conferido **no núcleo**, nunca pela aplicação que chama, e NEVER SHALL
depender de qual aplicação fez a chamada — a conferência é sobre a persona em sessão e o
vínculo dela, como toda a matriz. (`RF-01-16`)

A recusa por **falta de escopo** SHALL ser indistinguível da recusa por sujeito inexistente
sempre que distinguir as duas revelaria a existência do sujeito. Na confirmação de identidade,
onde o sujeito é um nick de criança, ela SHALL seguir o `RN-01-22`: mesmo código, mesma mensagem
e mesmo trabalho da recusa por nick inexistente. (`RN-01-58`, `RN-01-22`)

#### Scenario: O papel abre a porta e o vínculo diz sobre quem

- **WHEN** um responsável em sessão pede uma operação com escopo sobre um Guerreiro(a) sob a
  responsabilidade dele
- **THEN** o núcleo a executa, porque o papel permite e o vínculo alcança

#### Scenario: Papel certo, vínculo ausente

- **WHEN** um responsável em sessão pede a mesma operação sobre um Guerreiro(a) que não está sob
  a responsabilidade dele
- **THEN** o núcleo a recusa, ainda que a matriz permita a operação ao papel dele

#### Scenario: A falta de escopo não denuncia a existência do sujeito

- **WHEN** se comparam a recusa por nick que não está sob a responsabilidade de quem pede e a
  recusa por nick que não existe
- **THEN** as duas são indistinguíveis no código, na mensagem e no trabalho feito

#### Scenario: O escopo não depende da aplicação que chamou

- **WHEN** a mesma operação com escopo chega de aplicações diferentes, com a mesma persona em
  sessão
- **THEN** a conferência do vínculo é a mesma nas duas, e o resultado não muda
