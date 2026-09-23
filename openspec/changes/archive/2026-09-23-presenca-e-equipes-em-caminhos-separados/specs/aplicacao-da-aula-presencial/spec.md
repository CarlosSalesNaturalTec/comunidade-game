# Spec Delta

## RENAMED Requirements

- FROM: `### Requirement: O Guerreiro(a) entra por nick e imagem, e a presença é registrada na entrada`
- TO: `### Requirement: O Guerreiro(a) entra por nick e imagem, e só o caminho Presença registra a presença`

- FROM: `### Requirement: O Guerreiro(a) entra no caminho das trilhas por confirmação de Mestre ou Admin`
- TO: `### Requirement: O Guerreiro(a) entra por confirmação de Mestre ou Admin, em qualquer caminho`

## MODIFIED Requirements

### Requirement: O Guerreiro(a) entra por nick e imagem, e só o caminho Presença registra a presença

A App 01 SHALL oferecer, nos caminhos que pedem o Guerreiro(a) — **presença**, **equipes**,
**quiz** e **troca** —, a entrada por **nick e imagem**: o nick informado na tela e o
**descritor gerado no próprio aparelho**, na ordem prova de vivacidade e depois descritor
facial. Ao núcleo SHALL ir apenas o descritor; a fotografia SHALL ser descartada sem sair do
aparelho e NEVER SHALL ser gravada nem enviada.

A aplicação SHALL informar ao núcleo, no mesmo pedido, a **aula em curso** — é ela que determina
o ponto de apoio e, com ele, o limiar da comparação. A aula já é propriedade da tela da entrada,
herdada da sessão de trabalho do aparelho, e NEVER SHALL ser digitada nem escolhida por quem
opera. (`RF-04-18`, `RF-01-73`)

A tela SHALL apresentar o **visor ao vivo** da câmera enquanto a captura acontece, e SHALL
detectar **em laço** até a vivacidade passar ou o tempo se esgotar, em vez de julgar um único
quadro. O **quadro capturado** NEVER SHALL voltar à tela. (`RF-04-64`, `RN-04-34`)

O **retorno abstrato do laço** — rosto procurado, rosto encontrado, pessoa confirmada — SHALL
valer apenas enquanto a captura acontece, e NEVER SHALL permanecer na tela depois de a tentativa
ter desfecho. Nenhuma tela SHALL apresentar, ao mesmo tempo, o retorno do laço e o desfecho da
tentativa: quem opera leria as duas frases como um único julgamento contraditório. (`RF-04-64`,
`RN-04-34`)

Reconhecido o Guerreiro(a), a aplicação SHALL abrir a sessão dele. O registro da **presença do
dia no modo reconhecimento** SHALL acontecer **apenas no caminho presença**, no mesmo
atendimento; nos caminhos equipes, quiz e troca a entrada NEVER SHALL registrar presença nem
tratá-la como parte do reconhecimento. Presença já constante do encontro NEVER SHALL ser
duplicada nem tratada como erro: no caminho presença a aplicação SHALL avisar que ela já existe
e voltar à tela inicial. (`RF-04-18`, `RF-04-19`, `RF-04-29`, `RF-04-67`, `RN-04-12`,
`RN-04-06`, PRD-04 §5.4)

#### Scenario: Nick e imagem conferem

- **WHEN** o Guerreiro(a) informa o nick e a câmera captura a imagem dele na chegada, pelo
  caminho da presença
- **THEN** a aplicação abre a sessão do Guerreiro(a) e registra a presença do dia por
  reconhecimento

#### Scenario: Nos demais caminhos a entrada não registra presença

- **WHEN** o Guerreiro(a) entra por nick e imagem pelo caminho das equipes, do quiz ou da troca
- **THEN** a aplicação abre a sessão dele e nenhuma requisição de presença é enviada

#### Scenario: A entrada declara ao núcleo a aula em curso

- **WHEN** a aplicação pede a abertura da sessão por reconhecimento
- **THEN** o pedido carrega a aula do encontro, além do nick e do descritor, e quem opera não
  digitou nem escolheu aula alguma

#### Scenario: A presença do encontro já constava

- **WHEN** um Guerreiro(a) já com presença registrada naquela aula é reconhecido de novo pelo
  caminho da presença
- **THEN** a aplicação avisa que a presença já existe, não duplica registro algum e volta à tela
  inicial

#### Scenario: Nenhuma imagem de criança sai do aparelho

- **WHEN** a entrada por nick e imagem acontece
- **THEN** nenhuma requisição carrega fotografia, e nenhuma imagem fica gravada no aparelho
  compartilhado

#### Scenario: Quem chega se vê no visor antes de a captura julgar

- **WHEN** a entrada por nick e imagem abre a câmera
- **THEN** o visor ao vivo aparece na tela, e a detecção segue em laço até aprovar ou o tempo se
  esgotar

#### Scenario: O retorno do laço não sobrevive à recusa do núcleo

- **WHEN** a vivacidade é confirmada e, em seguida, o núcleo recusa a abertura da sessão
- **THEN** a tela apresenta apenas a frase da recusa, e o retorno do laço já não está na tela

#### Scenario: O retorno do laço não sobrevive à falha de preparo nem à vivacidade reprovada

- **WHEN** a tentativa termina por preparo que falhou ou por vivacidade reprovada
- **THEN** a tela apresenta apenas a frase daquele desfecho, sem o retorno do laço ao lado

#### Scenario: Sem câmera, a entrada segue pela confirmação humana

- **WHEN** o aparelho não tem câmera disponível
- **THEN** a aplicação não oferece a captura e encaminha o Guerreiro(a) à confirmação de Mestre
  ou Admin, sem deixá-lo fora da aula

### Requirement: O Guerreiro(a) entra por confirmação de Mestre ou Admin, em qualquer caminho

A App 01 SHALL abrir a sessão do Guerreiro(a) pela **confirmação de identidade** feita pelo
Mestre ou Admin **que abriu a sessão de trabalho**, presente ao lado da criança, com registro de
quem confirmou. No **caminho presença**, a aplicação SHALL registrar, no mesmo ato, a **presença
do dia no modo confirmação**, com o mesmo adulto como confirmador; nos caminhos equipes, quiz e
troca a confirmação NEVER SHALL registrar presença (`RF-04-67`). A recusa de biometria e a
ausência de _template_ NEVER SHALL deixar o Guerreiro(a) fora da aula: a confirmação humana é a
alternativa equivalente.

A confirmação humana é o que o `RN-04-09` sempre disse que ela era — a alternativa de quem não
tem _template_, de quem recusou a biometria e de quem a câmera não reconheceu. A sessão que ela
abre SHALL ter os mesmos direitos da aberta por reconhecimento. (`RF-04-29`, `RF-04-15`,
`RF-04-21`, `RN-04-09`, PRD-04 §§5.3, 5.5)

Tocar em "Chamar Mestre ou Admin" SHALL levar a uma tela que pede o **nick** da criança e o
**PIN** do adulto, com o PIN mascarado. A sessão de trabalho aberta no aparelho, sozinha, NEVER
SHALL confirmar: sem o PIN digitado no ato, o botão de confirmar não age. PIN errado SHALL ser
dito como PIN errado, sem apagar o nick; PIN bloqueado e PIN não cadastrado SHALL ser ditos como
o que são — o bloqueado manda refazer o login Google, e o não cadastrado manda cadastrar o PIN
na App 09 ou na App 03. O campo do PIN SHALL ser limpo a cada tentativa e ao fim de cada
atendimento, e o PIN NEVER SHALL ser gravado no aparelho. (`RF-04-21`, `RN-04-37`, `RN-04-38`)

#### Scenario: Mestre confirma e a sessão do Guerreiro(a) abre

- **WHEN** o Guerreiro(a) informa o nick e o Mestre que abriu a sessão de trabalho digita o
  próprio PIN, no caminho da presença
- **THEN** a aplicação abre a sessão do Guerreiro(a), registra quem confirmou e grava a presença
  do dia por confirmação

#### Scenario: A confirmação fora do caminho da presença não registra presença

- **WHEN** a confirmação com PIN abre a sessão pelo caminho das equipes, do quiz ou da troca
- **THEN** a aplicação abre a sessão e nenhuma requisição de presença é enviada

#### Scenario: A recusa não exclui ninguém da aula

- **WHEN** um Guerreiro(a) sem _template_ gravado chega à entrada do Guerreiro(a)
- **THEN** a aplicação o encaminha à confirmação humana, sem impedi-lo de participar

#### Scenario: A presença confirmada guarda quem confirmou

- **WHEN** a sessão é aberta por confirmação presencial no caminho da presença
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

## REMOVED Requirements

### Requirement: A tela inicial oferece os dois caminhos e volta ao início a cada atendimento

**Reason**: A decisão do fundador de 2026-09-23 (documento 09 §1, "Presença e equipes em
caminhos separados, e a equipe com nome") separou o registro da presença do trabalho em equipe:
onde havia dois caminhos — onboarding e trilhas — passam a existir três, e o caminho das
trilhas, que registrava a presença e levava às equipes no mesmo atendimento, deixa de existir
com esse nome e com esse desfecho (`RF-04-01`, `RF-04-67`). O substituto é "A tela inicial
oferece os três caminhos e volta ao início a cada atendimento", que preserva o que continua
valendo: a volta ao início a cada atendimento, a entrada que nunca leva ao cadastro e os
caminhos do quiz e da troca.

**Migration**: Nenhuma no dado. Quem operava pelo botão Trilhas passa a usar **Presença** para
registrar a presença e **Equipes** para trabalhar a trilha; nenhuma presença registrada muda e
nenhuma equipe formada se perde.

## ADDED Requirements

### Requirement: A tela inicial oferece os três caminhos e volta ao início a cada atendimento

A App 01 SHALL apresentar, na tela inicial, os três caminhos — **onboarding**, **presença** e
**equipes**. Ao fim de cada atendimento, a aplicação SHALL voltar à tela inicial e NEVER SHALL
exibir dado do atendimento anterior. Quem escolhe **presença** ou **equipes** sem sessão de
Guerreiro(a) aberta SHALL ser levado à entrada do Guerreiro(a), nunca ao cadastro. (`RF-04-01`,
`RF-04-28`)

O caminho **presença** SHALL terminar no registro da presença: feito o registro, a aplicação
SHALL voltar à tela inicial e NEVER SHALL levar às equipes, que são outro momento (`RF-04-67`,
PRD-04 §5.4).

O caminho **equipes** SHALL levar à formação da equipe da aula e, escolhida a equipe, ao
trabalho da trilha — programação, missão, produção e assistente. Trabalhar a trilha NEVER SHALL
ser alcançável fora dele (`RF-04-68`, PRD-04 §§5.7, 5.8).

Com o **momento de troca aberto**, a tela inicial SHALL apresentar também o caminho da **troca
por recompensa avulsa**, ao lado dos três. Fechado o momento — que é o estado em que a aplicação
começa —, o caminho NEVER SHALL aparecer.

A tela inicial SHALL apresentar ainda o caminho do **quiz**, sempre disponível na sessão de
trabalho: diferentemente da troca, o PRD-04 não põe a partida atrás de um momento aberto por
Mestre, e é a própria tela do quiz que diz não haver partida quando não há. (`RF-04-01`,
`RF-04-28`, `RF-04-41`, `RF-04-49`, PRD-04 §12)

#### Scenario: Os três caminhos aparecem

- **WHEN** a sessão de trabalho está aberta
- **THEN** a tela inicial apresenta o caminho do onboarding, o da presença e o das equipes

#### Scenario: Equipes sem sessão leva à entrada, não ao cadastro

- **WHEN** alguém escolhe equipes sem sessão de Guerreiro(a) aberta
- **THEN** a aplicação apresenta a entrada do Guerreiro(a), e nenhuma tela de cadastro aparece

#### Scenario: O caminho da presença termina no registro

- **WHEN** a presença é registrada pelo caminho da presença
- **THEN** a aplicação volta à tela inicial, e nenhuma tela de equipe aparece no mesmo
  atendimento

#### Scenario: Trabalhar a trilha acontece dentro das equipes

- **WHEN** a equipe do momento é escolhida no caminho das equipes
- **THEN** a aplicação mostra a programação do encontro, e esse é o único caminho que chega a
  ela

#### Scenario: O atendimento seguinte começa limpo

- **WHEN** um atendimento termina e a aplicação volta à tela inicial
- **THEN** nenhum dado do atendimento anterior aparece em tela alguma

#### Scenario: O caminho da troca só existe com o momento de troca aberto

- **WHEN** o Mestre abre o momento de troca
- **THEN** a tela inicial passa a apresentar também o caminho da troca, e volta a escondê-lo
  quando o momento é fechado

#### Scenario: O caminho do quiz não depende de momento aberto

- **WHEN** a sessão de trabalho está aberta e o momento de troca está fechado
- **THEN** a tela inicial apresenta o caminho do quiz

### Requirement: Os caminhos Equipes, Quiz e Troca só abrem para quem tem presença registrada

Aberta a sessão do Guerreiro(a) nos caminhos **equipes**, **quiz** e **troca**, a App 01 SHALL
consultar o núcleo sobre a presença dele na **aula em curso** e SHALL recusar o caminho a quem
não a tem, dizendo em linguagem simples que é preciso registrar a presença antes e oferecendo o
caminho **presença** ali mesmo. A recusa NEVER SHALL deixar o Guerreiro(a) sem desfecho na tela.
Quiz e troca entram nessa exigência por decisão do fundador de 2026-09-23, que estende o
`RN-04-40` aos dois. (`RF-04-68`, `RN-04-40`)

A aplicação SHALL encerrar a sessão aberta quando recusar o caminho, para que o atendimento
seguinte comece limpo (`RF-04-28`).

A recusa do núcleo à formação de equipe por falta de presença SHALL ser apresentada como o que
é, nunca como recusa do reconhecimento nem como falha de rede (`RN-04-36`).

Sem rede, esses três caminhos SHALL seguir indisponíveis como já são, e NEVER SHALL enfileirar
presença: a fila local é do caminho **presença** (`RF-04-23`, `RF-04-58`).

#### Scenario: Sem presença, o caminho das equipes não abre

- **WHEN** um Guerreiro(a) sem presença registrada no encontro entra pelo caminho das equipes
- **THEN** a aplicação diz que é preciso registrar a presença antes, oferece o caminho da
  presença e não mostra equipe alguma

#### Scenario: Com presença registrada, a volta às equipes passa

- **WHEN** um Guerreiro(a) que já registrou a presença no encontro volta pelo caminho das
  equipes
- **THEN** a aplicação abre a sessão dele e mostra as equipes da aula, sem aviso de presença já
  registrada

#### Scenario: Quiz e troca seguem a mesma exigência

- **WHEN** um Guerreiro(a) sem presença registrada entra pelo caminho do quiz ou pelo da troca
- **THEN** a aplicação recusa do mesmo modo e o encaminha ao caminho da presença

#### Scenario: A recusa do núcleo aparece como falta de presença

- **WHEN** o núcleo recusa a formação de equipe por falta de presença
- **THEN** a aplicação apresenta a falta de presença, e não a frase da recusa do reconhecimento

#### Scenario: Recusado o caminho, o atendimento não deixa sessão aberta

- **WHEN** o caminho é recusado por falta de presença e a tela volta ao início
- **THEN** nenhuma sessão de Guerreiro(a) segue aberta no aparelho
