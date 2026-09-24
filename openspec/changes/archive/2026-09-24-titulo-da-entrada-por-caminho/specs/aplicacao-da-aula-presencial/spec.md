# Spec Delta

## MODIFIED Requirements

### Requirement: O Guerreiro(a) entra por nick e imagem, e só o caminho Presença registra a presença

A App 01 SHALL oferecer, nos caminhos que pedem o Guerreiro(a) — **presença**, **equipes**,
**quiz** e **troca** —, a entrada por **nick e imagem**: o nick informado na tela e o
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

#### Scenario: A entrada anuncia o caminho que serve

- **WHEN** a entrada do Guerreiro(a) é aberta pelo caminho das equipes, do quiz ou da troca
- **THEN** a tela se anuncia pelo caminho escolhido, distinta da entrada do caminho da presença,
  tanto na forma por nick e imagem quanto na por confirmação de Mestre ou Admin
