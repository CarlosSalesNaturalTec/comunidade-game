## MODIFIED Requirements

### Requirement: O Guerreiro(a) entra no caminho das trilhas por confirmação de Mestre ou Admin

A App 01 SHALL abrir a sessão do Guerreiro(a) pela **confirmação de identidade** feita pelo
Mestre ou Admin **que abriu a sessão de trabalho**, presente ao lado da criança, com registro de
quem confirmou, e SHALL registrar, no
mesmo ato, a **presença do dia no modo confirmação**, com o mesmo adulto como confirmador. A
recusa de biometria e a ausência de _template_ NEVER SHALL deixar o Guerreiro(a) fora da aula:
a confirmação humana é a alternativa equivalente.

A confirmação humana deixa de ser o único caminho de entrada e passa a ser o que o `RN-04-09`
sempre disse que ela era — a alternativa de quem não tem _template_, de quem recusou a
biometria e de quem a câmera não reconheceu. A sessão que ela abre SHALL ter os mesmos direitos
da aberta por reconhecimento. (`RF-04-29`, `RF-04-15`, `RF-04-21`, `RN-04-09`, PRD-04 §§5.3,
5.5)

Tocar em "Chamar Mestre ou Admin" SHALL levar a uma tela que pede o **nick** da criança e o
**PIN** do adulto, com o PIN mascarado. A sessão de trabalho aberta no aparelho, sozinha, NEVER
SHALL confirmar: sem o PIN digitado no ato, o botão de confirmar não age. PIN errado SHALL ser
dito como PIN errado, sem apagar o nick; PIN bloqueado e PIN não cadastrado SHALL ser ditos
como o que são — o bloqueado manda refazer o login Google, e o não cadastrado manda cadastrar o
PIN na App 09 ou na App 03. O campo do PIN SHALL ser limpo a cada tentativa e ao fim de cada
atendimento, e o PIN NEVER SHALL ser gravado no aparelho. (`RF-04-21`, `RN-04-37`, `RN-04-38`)

#### Scenario: Mestre confirma e a sessão do Guerreiro(a) abre

- **WHEN** o Guerreiro(a) informa o nick e o Mestre que abriu a sessão de trabalho digita o
  próprio PIN
- **THEN** a aplicação abre a sessão do Guerreiro(a), registra quem confirmou e grava a
  presença do dia por confirmação

#### Scenario: A recusa não exclui ninguém da aula

- **WHEN** um Guerreiro(a) sem _template_ gravado chega ao caminho das trilhas
- **THEN** a aplicação o encaminha à confirmação humana, sem impedi-lo de participar

#### Scenario: A presença confirmada guarda quem confirmou

- **WHEN** a sessão é aberta por confirmação presencial
- **THEN** a presença gravada aponta o adulto que confirmou, e não o modo reconhecimento

#### Scenario: Nenhuma imagem de criança sai do aparelho nesta fatia

- **WHEN** a entrada acontece por confirmação humana
- **THEN** nenhuma requisição da aplicação carrega fotografia, e nenhuma imagem é gravada no
  aparelho compartilhado

#### Scenario: Sem PIN, a confirmação não acontece

- **WHEN** alguém toca em "Chamar Mestre ou Admin" e digita um nick sem digitar o PIN
- **THEN** a aplicação não confirma, não abre sessão e não registra presença

#### Scenario: PIN errado é dito como tal e o nick fica

- **WHEN** o PIN digitado não confere
- **THEN** a aplicação diz que o PIN está errado, limpa o PIN e mantém o nick

#### Scenario: PIN bloqueado manda refazer o login

- **WHEN** o núcleo responde que o PIN está bloqueado
- **THEN** a aplicação diz que o PIN foi bloqueado naquele aparelho e que é preciso entrar de
  novo pelo Google, e não oferece nova tentativa

#### Scenario: O PIN não fica no aparelho

- **WHEN** se examina o que a aplicação guardou no aparelho depois de uma confirmação
- **THEN** não há PIN em armazenamento algum

### Requirement: Sem rede, a presença confirmada pelo Mestre entra na fila local

A App 01 SHALL continuar registrando a **presença** com a rede fora: o Mestre ou o Admin da
sessão de trabalho confirma a criança **pelo nick**, e o registro SHALL entrar na **fila local**
do aparelho, com a **hora do fato** — a hora em que a criança chegou. A confirmação sem rede
SHALL pedir o **PIN** de quem abriu a sessão de trabalho e conferi-lo **no aparelho**, contra o
verificador recebido na abertura; só com o PIN conferido o registro entra na fila. Cada erro
conta, no aparelho, para o bloqueio: no **quinto erro seguido** a aplicação SHALL parar de
confirmar até um novo login Google, com ou sem rede. Sem verificador — o adulto não tinha PIN
cadastrado quando abriu a sessão —, a confirmação sem rede SHALL ficar indisponível, com aviso
que diz por quê. (`RF-04-23`, `RN-04-38`)

A fila SHALL guardar **apenas presença**: nick, hora do fato e a aula do encontro. Ela NEVER
SHALL guardar imagem, fotografia, descritor ou _template_ de criança, nem o PIN, e NEVER SHALL enfileirar
cadastro, resposta de quiz, produção da missão, troca ou consulta ao assistente. (`RF-04-23`,
`RN-04-12`, `RN-04-13`, PRD-04 §8)

#### Scenario: A criança que chega sem rede entra na aula

- **WHEN** a rede está fora e o Mestre confirma a criança que chegou pelo nick e pelo PIN
  certo
- **THEN** a aplicação enfileira a presença com a hora do fato e diz à criança que ela está na
  aula

#### Scenario: A fila não guarda imagem

- **WHEN** se examina o que a aplicação guardou no aparelho durante a queda
- **THEN** há apenas presença enfileirada, e nenhuma imagem, descritor ou _template_

#### Scenario: Só a presença é enfileirada

- **WHEN** a rede cai durante um cadastro, uma partida, uma entrega de produção ou uma troca
- **THEN** nada disso vai para a fila local

#### Scenario: PIN errado sem rede não enfileira

- **WHEN** a rede está fora e o PIN digitado não confere com o verificador
- **THEN** nada entra na fila, e a aplicação diz que o PIN está errado

#### Scenario: O quinto erro sem rede bloqueia o aparelho

- **WHEN** o PIN é errado cinco vezes seguidas sem rede
- **THEN** a aplicação para de confirmar, com ou sem rede, até um novo login Google

#### Scenario: A sincronização não abre sessão

- **WHEN** a rede volta e a fila sincroniza
- **THEN** cada presença é registrada sem abrir sessão de Guerreiro(a)

## ADDED Requirements

### Requirement: A sessão de trabalho recebe o verificador do PIN de quem a abriu

Ao abrir a sessão de trabalho, com rede, a App 01 SHALL pedir ao núcleo o **verificador** do
PIN de quem se autenticou e guardá-lo **só enquanto durar aquela sessão de trabalho**, no mesmo
lugar do token dela, descartando-o quando ela encerra ou expira. O aparelho NEVER SHALL receber
nem guardar o PIN. Sem PIN cadastrado, a sessão de trabalho SHALL abrir mesmo assim, com aviso
de que confirmar identidade exige cadastrar o PIN na App 09 ou na App 03. (`RN-04-38`,
`RF-04-23`, PRD-04 §5.1)

#### Scenario: O verificador chega com a sessão de trabalho

- **WHEN** um Mestre com PIN cadastrado abre a sessão de trabalho com rede
- **THEN** o aparelho guarda o verificador do PIN dele, e nenhum PIN

#### Scenario: O verificador sai com a sessão

- **WHEN** a sessão de trabalho encerra ou expira
- **THEN** o verificador é apagado do aparelho

#### Scenario: Sem PIN, o aparelho abre e avisa

- **WHEN** um Admin sem PIN cadastrado abre a sessão de trabalho
- **THEN** o aparelho abre, e a tela avisa que confirmar identidade exige cadastrar o PIN
