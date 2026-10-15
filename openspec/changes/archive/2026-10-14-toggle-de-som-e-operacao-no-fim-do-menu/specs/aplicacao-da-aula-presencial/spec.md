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

As duas ações de **quem opera o aparelho** — abrir e fechar o momento de troca, e encerrar a
sessão de trabalho — SHALL ser apresentadas no **mesmo padrão dos caminhos**, ao fim da lista e
depois de todos eles, sob um rótulo de grupo que as separe do que a criança escolhe. O
**encerramento SHALL ser o último** dos dois. A abertura e o fechamento do momento de troca
SHALL aparecer ali apenas para o aparelho que pode abri-lo. (`RF-04-71`, `RF-04-49`, decisão do
fundador de 2026-10-14)

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
- **THEN** depois de todos os caminhos aparecem, sob um rótulo de grupo que as separa deles e no
  mesmo padrão dos caminhos, a abertura do momento de troca e, por último, o encerramento da
  sessão de trabalho

#### Scenario: O aparelho que não abre a troca mostra só o encerramento

- **WHEN** a tela inicial é apresentada num aparelho que não pode abrir o momento de troca
- **THEN** o encerramento da sessão de trabalho aparece ao fim da lista, e nenhuma abertura de
  momento de troca é oferecida

### Requirement: A tela inicial liga e desliga a narração do aparelho

A App 01 SHALL oferecer, na **tela inicial**, o alternador que liga e desliga a narração, no
**canto do cabeçalho** da tela, apresentado **só pelo glifo** do sistema de ícone da camada
comum e cumprindo o alvo de toque que o documento 15 §5 exige. A tela inicial é onde ele mora
porque é a tela que aparece **entre atendimentos**: quem chega ao aparelho a encontra antes de
entrar no seu caminho. O alternador NEVER SHALL ser apresentado nas demais telas da aplicação.
(documento 15 §5.1, decisão do fundador de 2026-10-14)

O estado SHALL ser dito pela **forma** — um glifo para ligado e outro para desligado — e pelo
estado de pressionado do controle, e NEVER SHALL depender de cor nem de frase escrita na tela. O
rótulo SHALL alcançar quem navega por leitor de tela.

O estado SHALL valer para o **aparelho**, não para o atendimento: encerrar o atendimento e
voltar ao início NEVER SHALL religar nem desligar a narração por conta própria. Encerrar a
**sessão de trabalho** NEVER SHALL apagá-la: ela não é dado da sessão nem do Guerreiro(a).
Recarregar a aplicação SHALL devolvê-la ao **desligado**, que é como ela nasce.

#### Scenario: O controle está na tela inicial

- **WHEN** a tela inicial da App 01 é apresentada
- **THEN** o alternador da narração aparece no canto do cabeçalho, só pelo glifo, e nenhuma
  frase descreve o estado dele em tela

#### Scenario: As demais telas não o apresentam

- **WHEN** qualquer outra tela da App 01 é apresentada
- **THEN** o alternador da narração não aparece nela

#### Scenario: A escolha sobrevive ao atendimento seguinte

- **WHEN** alguém liga a narração, conclui o atendimento e o aparelho volta ao início
- **THEN** a narração continua ligada, e o próximo atendimento pode desligá-la

#### Scenario: Encerrar a sessão de trabalho não mexe na narração

- **WHEN** a sessão de trabalho do aparelho é encerrada
- **THEN** a escolha de narração do aparelho permanece como estava

#### Scenario: A recarga devolve a narração ao desligado

- **WHEN** a narração está ligada e a aplicação é recarregada
- **THEN** ela volta a estar desligada

### Requirement: O conteúdo de missão em texto ganha o controle de ouvi-lo

Havendo síntese de fala no navegador, a App 01 SHALL oferecer, junto do conteúdo de missão em
**texto**, um controle próprio de **ouvir**. O controle NEVER SHALL depender de a narração das
telas estar ligada: quem o aciona está pedindo aquela leitura, e o próprio acionamento é o gesto
que o navegador exige. (documento 15 §5.1, decisão do fundador de 2026-10-14)

O conteúdo NEVER SHALL ser falado ao entrar na tela: no encontro há **um aparelho por equipe** e
meia dúzia deles lendo o conteúdo inteiro ao mesmo tempo é ruído, não acessibilidade (documento
15 §5.1, documento 03 §4).

Conteúdo que não é texto — imagem, vídeo, link e arquivo de apoio — NEVER SHALL apresentar o
controle: não há o que ler em voz alta.

#### Scenario: O conteúdo em texto oferece ouvir

- **WHEN** a equipe ou o Guerreiro(a) alcança um conteúdo de missão em texto
- **THEN** um controle de ouvir aparece junto dele, e o conteúdo não foi falado sozinho

#### Scenario: Acionar o controle lê o conteúdo

- **WHEN** o controle de ouvir é acionado
- **THEN** o conteúdo daquele texto é falado

#### Scenario: Com a narração desligada o controle continua lá

- **WHEN** a narração das telas está desligada e um conteúdo de missão em texto é alcançado
- **THEN** o controle de ouvir aparece, e acioná-lo lê aquele texto

#### Scenario: Conteúdo que não é texto não oferece ouvir

- **WHEN** o conteúdo alcançado é imagem, vídeo, link externo ou arquivo de apoio
- **THEN** nenhum controle de ouvir é apresentado

## REMOVED Requirements

### Requirement: A App 01 arma a narração na primeira interação

**Reason**: A narração passa a nascer **desligada** e a escolha deixa de sobreviver à recarga
da aplicação (decisão do fundador de 2026-10-14), então o estado "ligada e ainda não armada"
— o único que este controle cobria — deixa de existir. O acionamento que liga a narração é o
gesto que o navegador exige.

**Migration**: O controle de iniciar sai da aplicação. Quem quer a narração a liga pelo
alternador da tela inicial, e esse mesmo toque a arma. O conteúdo de missão em texto continua
se ouvindo pelo controle próprio dele, que também arma o que ele fala.
