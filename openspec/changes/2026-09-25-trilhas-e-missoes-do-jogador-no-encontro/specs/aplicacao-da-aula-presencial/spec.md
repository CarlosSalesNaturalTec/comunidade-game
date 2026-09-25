# Spec Delta

## MODIFIED Requirements

### Requirement: O Guerreiro(a) entra por nick e imagem, e só o caminho Presença registra a presença

A App 01 SHALL oferecer, nos caminhos que pedem o Guerreiro(a) — **presença**, **equipes**,
**quiz**, **troca** e **trilhas** —, a entrada por **nick e imagem**: o nick informado na tela e o
**descritor gerado no próprio aparelho**, na ordem prova de vivacidade e depois descritor
facial. Ao núcleo SHALL ir apenas o descritor; a fotografia SHALL ser descartada sem sair do
aparelho e NEVER SHALL ser gravada nem enviada.

A tela da entrada SHALL anunciar **qual caminho serve**, para que quem escolheu equipes, quiz
ou troca na tela inicial reconheça que chegou ao caminho escolhido, e não ao da presença. O
anúncio SHALL valer nas duas formas da entrada — a por nick e imagem e a por confirmação de
Mestre ou Admin —, que NEVER SHALL se apresentar com o mesmo enunciado nos quatro caminhos.
O que a entrada **faz** em cada caminho não muda com isso. (`RF-04-01`, `RF-04-67`,
`RF-04-68`)

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
atendimento; nos caminhos equipes, quiz, troca e trilhas a entrada NEVER SHALL registrar presença nem
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

- **WHEN** o Guerreiro(a) entra por nick e imagem pelo caminho das equipes, do quiz, da troca
  ou das trilhas
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

#### Scenario: A entrada anuncia o caminho que serve

- **WHEN** a entrada do Guerreiro(a) é aberta pelo caminho das equipes, do quiz, da troca ou
  das trilhas
- **THEN** a tela se anuncia pelo caminho escolhido, distinta da entrada do caminho da presença,
  tanto na forma por nick e imagem quanto na por confirmação de Mestre ou Admin

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

## ADDED Requirements

### Requirement: A App 01 apresenta o percurso do Guerreiro(a) e as atividades das equipes dele

A App 01 SHALL apresentar, a quem tem presença registrada no encontro, o **percurso do próprio
Guerreiro(a)**: as trilhas em que ele está inscrito e, na trilha escolhida, a **missão atual** e a
**seguinte trancada, com o motivo do bloqueio**. NEVER SHALL apresentar a lista inteira do percurso
nem classificar missão como realizada: é o mesmo recorte que a App 05 já atende, e ele vale aqui
sem alteração. (`RF-04-72`, `RF-05-08`, `RF-05-10`, `RF-05-17`)

Havendo **mais de uma** trilha inscrita, a aplicação SHALL apresentar a lista das trilhas e SHALL
abrir o percurso da que for escolhida. Havendo **uma**, SHALL abrir o percurso dela direto, sem
lista intermediária. Não havendo **nenhuma**, SHALL levar ao **catálogo de poderes do ciclo**, onde
o Guerreiro(a) escolhe o poder e **inscreve-se na trilha ali mesmo**. (`RF-04-72`, `RF-04-74`)

A inscrição no encontro SHALL seguir as mesmas regras da App 05: a escolha do poder NEVER SHALL ser
teto — ele SHALL poder inscrever-se em quantas trilhas quiser, de um ou de vários poderes — e a
aplicação NEVER SHALL oferecer desinscrição, porque a inscrição não se desfaz. Inscrever-se de novo
na mesma trilha SHALL devolver a inscrição existente, sem erro. Feita a inscrição, a aplicação SHALL
abrir o percurso daquela trilha no mesmo atendimento, na **sondagem**, que é a próxima missão dele.
(`RF-04-74`, `RF-05-09`, `RN-05-43`, `RN-05-44`)

Para quem acabou de se inscrever, a missão atual **é a sondagem**, porque é ela a próxima do
percurso: a aplicação NEVER SHALL calcular por conta própria onde o percurso começa — a posição vem
do núcleo. (`RF-04-72`, `RF-05-08`, invariante 5)

A aplicação SHALL apresentar, junto do percurso, as **atividades das equipes do Guerreiro(a) naquela
aula**, lidas com as equipes de que ele é integrante. Quem não integra equipe na aula SHALL ler que
não há equipe dele no encontro — enunciado **distinto** do encontro sem programação declarada, que é
outro fato. (`RF-04-72`, `RF-04-35`)

A aplicação SHALL permitir ao Guerreiro(a) **responder à sondagem** da trilha e **submeter o desafio
de desbloqueio** da missão no aparelho do encontro, pela mesma porta e com a mesma aferição da App
05: no quiz, a submissão leva a resposta de todas as perguntas de uma vez e passa quem acerta ao
menos 60%; no desafio prático, a submissão é a declaração de que cumpriu, e a missão **aguarda o
Mestre autor**, nunca reprovada. O desbloqueio é **do Guerreiro(a) na trilha, nunca da equipe**.
(`RF-04-73`, `RF-05-13`, `RF-05-14`, `RF-05-89`, `RN-05-20`, `RN-05-45` a `RN-05-47`, documento 11
§2.2)

Respondida a sondagem, a trilha SHALL abrir — ela abre **ao ser respondida, não ao ser acertada** —, e
a aplicação SHALL apresentar o percurso já aberto sem exigir novo atendimento. (`RF-04-73`,
documento 11 §2.2, invariante 5)

A aplicação NEVER SHALL **entregar produção individual** da missão pelo caminho das trilhas
(`RF-05-74`): a entrega por **equipe** do `RF-04-45` segue sendo a desta aplicação e NEVER SHALL
sair do caminho das equipes, e duas entregas sobre a mesma missão exigiriam regra que nenhum
documento declara. Decisão do fundador de 2026-09-25.

Sem rede, o percurso SHALL ficar indisponível como os demais caminhos que pedem o Guerreiro(a), e
NEVER SHALL enfileirar nada. (`RF-04-58`, `RF-04-68`)

#### Scenario: Uma trilha inscrita abre direto no percurso

- **WHEN** o Guerreiro(a) com uma única trilha inscrita alcança as trilhas e missões
- **THEN** a aplicação apresenta o percurso daquela trilha, sem lista de trilhas no caminho

#### Scenario: Mais de uma trilha inscrita apresenta a lista

- **WHEN** o Guerreiro(a) inscrito em duas trilhas ou mais alcança as trilhas e missões
- **THEN** a aplicação apresenta a lista das trilhas, e a escolhida abre o percurso dela

#### Scenario: Sem inscrição, a tela leva ao catálogo de poderes

- **WHEN** o Guerreiro(a) sem inscrição alguma alcança as trilhas e missões
- **THEN** a aplicação apresenta os poderes do ciclo e as trilhas publicadas de cada um, com o
  caminho de se inscrever

#### Scenario: Inscrito no encontro, o percurso abre na sondagem

- **WHEN** o Guerreiro(a) escolhe um poder e inscreve-se numa trilha pelo aparelho do encontro
- **THEN** o percurso daquela trilha abre no mesmo atendimento, apresentando a missão de sondagem

#### Scenario: A inscrição não se desfaz e não tem teto

- **WHEN** o Guerreiro(a) já inscrito escolhe outra trilha, ou a mesma de novo
- **THEN** a nova inscrição acontece e a repetida devolve a que já existe, sem erro; em nenhum
  momento a tela oferece desinscrever-se

#### Scenario: Quem acabou de se inscrever começa na sondagem

- **WHEN** o Guerreiro(a) recém-inscrito abre o percurso da trilha
- **THEN** a missão apresentada é a sondagem, porque é a próxima do percurso segundo o núcleo

#### Scenario: A missão seguinte aparece trancada, com o motivo

- **WHEN** o percurso de uma trilha é apresentado
- **THEN** a missão atual aparece e a seguinte aparece trancada, dizendo por que está trancada

#### Scenario: As atividades da aula vêm pelas equipes do Guerreiro(a)

- **WHEN** o Guerreiro(a) integra equipe na aula em curso
- **THEN** as atividades daquela equipe aparecem junto do percurso

#### Scenario: Sem equipe na aula, a tela distingue os dois vazios

- **WHEN** o Guerreiro(a) não integra equipe alguma na aula em curso
- **THEN** a tela diz que não há equipe dele no encontro, com enunciado distinto do de encontro sem
  programação declarada

#### Scenario: O Guerreiro(a) responde à sondagem no encontro

- **WHEN** o Guerreiro(a) recém-inscrito abre a trilha no aparelho do encontro e responde à sondagem
- **THEN** a trilha abre, independentemente de quantas ele acertou, e o percurso aberto é apresentado
  no mesmo atendimento

#### Scenario: O quiz do desbloqueio é aferido pelo núcleo

- **WHEN** o Guerreiro(a) submete o quiz de desbloqueio de uma missão pelo aparelho do encontro
- **THEN** a submissão leva todas as perguntas de uma vez, e a devolutiva diz quantas ele acertou

#### Scenario: O desafio prático fica aguardando o Mestre

- **WHEN** o Guerreiro(a) declara ter cumprido um desafio prático de desbloqueio
- **THEN** a missão passa a aguardar o Mestre autor, e em nenhum momento aparece como reprovada

#### Scenario: A entrega individual não acontece por este caminho

- **WHEN** o percurso é apresentado no aparelho do encontro
- **THEN** não há como entregar produção individual da missão por essa tela, e a entrega por equipe
  segue no caminho das equipes

#### Scenario: Sem rede, o percurso não abre

- **WHEN** a rede está fora e alguém escolhe o caminho das trilhas
- **THEN** a aplicação diz que o caminho precisa de rede, como já faz nos caminhos das equipes, do
  quiz e da troca, e nada é enfileirado
