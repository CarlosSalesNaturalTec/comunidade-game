# Spec Delta

## MODIFIED Requirements

### Requirement: A tela inicial oferece os três caminhos e volta ao início a cada atendimento

A App 01 SHALL apresentar, na tela inicial, os três caminhos — **onboarding**, **presença** e
**equipes**. Ao fim de cada atendimento, a aplicação SHALL voltar à tela inicial e NEVER SHALL
exibir dado do atendimento anterior. Quem escolhe **presença** ou **equipes** sem sessão de
Guerreiro(a) aberta SHALL ser levado à entrada do Guerreiro(a), nunca ao cadastro. (`RF-04-01`,
`RF-04-28`)

O caminho **presença** SHALL terminar no registro da presença. Feito o registro, a aplicação
SHALL oferecer **dois** desfechos — voltar à tela inicial e seguir às **trilhas e missões** do
Guerreiro(a) que acabou de chegar —, e NEVER SHALL levar às **equipes**, que seguem sendo outro
momento. Seguir às trilhas NEVER SHALL pedir nick nem imagem de novo: a sessão do Guerreiro(a)
já está aberta quando o desfecho aparece. (`RF-04-67`, `RF-04-72`, PRD-04 §5.4)

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

A tela inicial SHALL apresentar ainda o caminho das **trilhas e missões**, para quem registrou a
presença em atendimento anterior. Como os caminhos das equipes, do quiz e da troca, ele SHALL
abrir a sessão pela entrada do Guerreiro(a) e SHALL passar pela guarda de presença, e NEVER SHALL
registrar presença. (`RF-04-72`, `RF-04-01`, `RN-04-40`)

Cada caminho SHALL apresentar, **ao lado do rótulo textual que já tem**, o glifo do sistema de
ícone da camada comum, para que a criança reconheça o caminho antes de ler a linha inteira. O
glifo NEVER SHALL substituir o rótulo nem ser a única forma de distinguir um caminho do outro.
(`RF-04-01`, documento 15 §§5, 11.1, decisão do fundador de 2026-09-25)

Os atos de **quem opera o aparelho** — a **medição do limiar**, abrir e fechar o momento de
troca, as **entregas pendentes do encontro** e encerrar a sessão de trabalho — SHALL ser
apresentados no **mesmo padrão dos
caminhos**, ao fim da lista e depois de todos eles, sob um rótulo de grupo que os separe do que
a criança escolhe. A ordem do grupo SHALL ser **medição do limiar**, momento de troca,
**entregas pendentes do encontro** e encerramento, e o **encerramento SHALL ser o último
do grupo**. As entregas pendentes SHALL acompanhar o momento de troca, por serem as duas
do encontro em curso, e SHALL aparecer **apenas quando quem abriu a sessão de trabalho é
Mestre** — o Admin nunca confirma entrega (`RF-07-13`, `RN-02-17`). A abertura e o fechamento do
momento de troca SHALL aparecer ali apenas para o aparelho que pode abri-lo; a medição SHALL
aparecer em toda sessão de trabalho, guardada pelo PIN do aparelho e não pelo papel. A medição
NEVER SHALL ser apresentada entre os caminhos que a criança escolhe: ela mede quem opera, nunca
um Guerreiro(a), fora do onboarding. (`RF-04-71`, `RF-04-49`, `RF-04-63`, `RN-04-33`,
`RN-04-41`, decisões do fundador de 2026-10-14 e 2026-10-15)

A ordem dos caminhos que a criança escolhe SHALL ser **onboarding**, **presença**, **trilhas e
missões**, **equipes**, **quiz** e, quando o momento de troca estiver aberto, **troca por
recompensa avulsa** — as trilhas e as equipes lado a lado, por serem o par de trabalhar a
trilha. (`RF-04-01`, decisão do fundador de 2026-10-15)

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

#### Scenario: O desfecho da presença oferece as trilhas

- **WHEN** a presença é registrada pelo caminho da presença
- **THEN** a tela do desfecho oferece voltar à tela inicial e seguir às trilhas e missões, e seguir
  às trilhas não pede nick nem imagem de novo

#### Scenario: A tela inicial leva às trilhas de quem já tem presença

- **WHEN** um Guerreiro(a) com presença registrada no encontro escolhe o caminho das trilhas na tela
  inicial
- **THEN** a aplicação abre a sessão dele pela entrada e apresenta o percurso, sem registrar
  presença de novo

#### Scenario: Sem presença, o caminho das trilhas não abre

- **WHEN** um Guerreiro(a) sem presença registrada escolhe o caminho das trilhas
- **THEN** a aplicação recusa do mesmo modo que nos caminhos das equipes, do quiz e da troca, e o
  encaminha ao caminho da presença

#### Scenario: O caminho da presença continua não levando às equipes

- **WHEN** a presença é registrada e quem chegou segue às trilhas
- **THEN** nenhuma tela de equipe da aula aparece nesse atendimento

#### Scenario: Cada caminho leva glifo ao lado do rótulo

- **WHEN** a tela inicial é apresentada
- **THEN** cada caminho apresenta um glifo junto do rótulo textual, o rótulo continua legível por
  inteiro e nenhum caminho se identifica só pelo desenho

#### Scenario: As ações de quem opera fecham a lista, com o encerramento por último

- **WHEN** a tela inicial é apresentada num aparelho que pode abrir o momento de troca
- **THEN** depois de todos os caminhos aparecem, sob um rótulo de grupo que os separa deles e no
  mesmo padrão dos caminhos, a medição do limiar, a abertura do momento de troca e, por último,
  o encerramento da sessão de trabalho

#### Scenario: O aparelho que não abre a troca mostra a medição e o encerramento

- **WHEN** a tela inicial é apresentada num aparelho que não pode abrir o momento de troca
- **THEN** o grupo de quem opera apresenta a medição do limiar e, por último, o encerramento da
  sessão de trabalho, e nenhuma abertura de momento de troca é oferecida

#### Scenario: Os caminhos aparecem na ordem decidida

- **WHEN** a tela inicial é apresentada com o momento de troca aberto
- **THEN** os caminhos aparecem na ordem onboarding, presença, trilhas e missões, equipes, quiz
  e troca por recompensa avulsa, antes do rótulo do grupo de quem opera

#### Scenario: A medição do limiar não fica entre os caminhos da criança

- **WHEN** a tela inicial é apresentada
- **THEN** a medição do limiar aparece dentro do grupo de quem opera o aparelho, nomeado por ele,
  e nenhum caminho que a criança escolhe aparece depois dela

#### Scenario: As entregas pendentes aparecem ao Mestre que abriu o aparelho

- **WHEN** a sessão de trabalho foi aberta por um Mestre
- **THEN** o grupo de quem opera traz as entregas pendentes do encontro, entre o momento de
  troca e o encerramento

#### Scenario: O aparelho aberto por Admin não oferece as entregas

- **WHEN** a sessão de trabalho foi aberta por um Admin
- **THEN** o caminho das entregas pendentes não aparece, e o encerramento segue por último

## ADDED Requirements

### Requirement: A App 01 apresenta as entregas pendentes do encontro

A App 01 SHALL apresentar, a quem opera o aparelho, as **entregas pendentes do encontro em
curso**: cada Guerreiro(a) com **presença registrada naquela aula** que alcançou marco com
recompensa declarada e ainda não a recebeu. Cada pendência SHALL trazer o Guerreiro(a) por
**nick e avatar**, a trilha, a missão que é o marco, o tipo de recurso e a quantidade, e
NEVER SHALL trazer valor em moedas ou em reais. (`RF-09-75`, `RF-04-55`, invariantes 12 e 16)

#### Scenario: Quem chegou e conquistou aparece na fila do encontro

- **WHEN** um Guerreiro(a) com presença registrada naquela aula alcançou marco com recompensa
  e ainda não a recebeu
- **THEN** a pendência dele aparece na fila do encontro, com nick, avatar, trilha, marco, tipo
  de recurso e quantidade

#### Scenario: Quem não registrou presença não aparece

- **WHEN** um Guerreiro(a) da mesma comunidade alcançou o marco, mas não tem presença
  registrada naquela aula
- **THEN** a pendência dele não aparece na fila do encontro — ela segue na App 09

#### Scenario: Encontro sem pendência alguma diz que não há

- **WHEN** ninguém com presença registrada tem entrega pendente
- **THEN** a aplicação diz que não há entrega pendente no encontro, e não apresenta erro

### Requirement: A entrega no encontro sai do ponto de apoio da aula, sob a sessão de trabalho

Confirmada a entrega na App 01, o recurso SHALL sair do **ponto de apoio da aula**, e a
aplicação NEVER SHALL oferecer seletor de ponto de apoio — a aula já o declara
obrigatoriamente (`RF-01-71`). A confirmação SHALL ser enviada sob a **sessão de trabalho** do
aparelho, e a pendência confirmada SHALL **sair** da fila. (`RF-09-76`, `RF-07-13`,
`RN-02-17`, documento 02 §8.1, decisão do fundador de 2026-10-30)

#### Scenario: A entrega confirmada sai da fila do encontro

- **WHEN** o Mestre confirma a entrega de uma pendência do encontro
- **THEN** o recurso sai do ponto de apoio da aula, a baixa é lançada e a pendência deixa a
  fila

#### Scenario: Não há escolha de ponto de apoio no encontro

- **WHEN** o Mestre abre uma pendência do encontro para confirmar
- **THEN** nenhum seletor de ponto de apoio lhe é oferecido

#### Scenario: A recusa do núcleo é apresentada em linguagem simples

- **WHEN** o núcleo recusa a entrega por falta de lastro no ponto de apoio da aula
- **THEN** a aplicação apresenta a recusa como ela veio, sem recalcular saldo por conta
  própria
