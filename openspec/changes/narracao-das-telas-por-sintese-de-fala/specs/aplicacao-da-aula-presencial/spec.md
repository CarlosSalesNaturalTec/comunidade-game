# Spec Delta

## ADDED Requirements

### Requirement: A tela inicial liga e desliga a narração do aparelho

A App 01 SHALL oferecer, na **tela inicial**, o controle que liga e desliga a narração, com
rótulo textual e o alvo de toque que o documento 15 §5 exige. A tela inicial é onde ele mora
porque é a tela que aparece **entre atendimentos**: quem chega ao aparelho a encontra antes de
entrar no seu caminho. (documento 15 §5.1)

O estado SHALL valer para o **aparelho**, não para o atendimento: encerrar o atendimento e
voltar ao início NEVER SHALL religar nem desligar a narração por conta própria, e a escolha
SHALL sobreviver a recarregar a aplicação. Encerrar a **sessão de trabalho** NEVER SHALL
apagá-la: ela não é dado da sessão nem do Guerreiro(a).

#### Scenario: O controle está na tela inicial

- **WHEN** a tela inicial da App 01 é apresentada
- **THEN** o controle de ligar e desligar a narração aparece ali, com rótulo textual

#### Scenario: A escolha sobrevive ao atendimento seguinte

- **WHEN** alguém desliga a narração, conclui o atendimento e o aparelho volta ao início
- **THEN** a narração continua desligada, e o próximo atendimento pode religá-la

#### Scenario: Encerrar a sessão de trabalho não mexe na narração

- **WHEN** a sessão de trabalho do aparelho é encerrada
- **THEN** a escolha de narração do aparelho permanece como estava

### Requirement: A App 01 arma a narração na primeira interação

O navegador NEVER SHALL falar antes de um gesto da pessoa. A App 01 SHALL apresentar, depois de
carregada e antes da primeira fala, um controle de **iniciar** que arma a narração; acionado
ele, a narração passa a falar as telas dali em diante. Antes dele a aplicação NEVER SHALL
tentar falar, e NEVER SHALL apresentar erro por não ter falado. (documento 15 §5.1)

Estando a narração **desligada**, o controle de iniciar NEVER SHALL ser apresentado: não há o
que armar.

#### Scenario: Carregada e sem gesto, nada fala

- **WHEN** a App 01 é carregada com a narração ligada e ninguém tocou em nada
- **THEN** nada é falado, e a aplicação oferece o controle de iniciar

#### Scenario: Acionado o iniciar, as telas passam a falar

- **WHEN** alguém aciona o controle de iniciar
- **THEN** a narração é armada, e as telas seguintes falam o que declararam

#### Scenario: Desligada, não há o que iniciar

- **WHEN** a App 01 é carregada com a narração desligada
- **THEN** o controle de iniciar não é apresentado

### Requirement: No Quiz ao Vivo a App 01 fala o enunciado da pergunta no ar

Com a narração ligada, a App 01 SHALL falar o **enunciado** da pergunta que entrou no ar na
partida de Quiz ao Vivo. NEVER SHALL falar as **alternativas**, nem o resultado, nem os avisos
de rede da partida: a decisão do fundador de 2026-09-26 recortou o enunciado, e falar o resto
tomaria o tempo em que a equipe responde.

O enunciado SHALL ser falado **uma vez por pergunta**. A App 01 acompanha a partida por
sondagem periódica, e a mesma pergunta volta a cada leitura: repetir a fala a cada leitura
tornaria a tela inutilizável. Só a **pergunta nova** SHALL ser falada.

#### Scenario: A pergunta que entra no ar é falada

- **WHEN** uma pergunta nova entra no ar na partida e a narração está ligada
- **THEN** o enunciado dela é falado, e as alternativas não

#### Scenario: A sondagem que repete a pergunta não repete a fala

- **WHEN** a sondagem seguinte devolve a mesma pergunta que já está no ar
- **THEN** nada é falado de novo

#### Scenario: O resultado liberado não é falado

- **WHEN** o resultado da pergunta é liberado na tela
- **THEN** a narração não o fala

### Requirement: O conteúdo de missão em texto ganha o controle de ouvi-lo

Com a narração ligada, a App 01 SHALL oferecer, junto do conteúdo de missão em **texto**, um
controle próprio de **ouvir**, com rótulo textual. O conteúdo NEVER SHALL ser falado ao entrar
na tela: no encontro há **um aparelho por equipe** e meia dúzia deles lendo o conteúdo inteiro
ao mesmo tempo é ruído, não acessibilidade (documento 15 §5.1, documento 03 §4).

Conteúdo que não é texto — imagem, vídeo, link e arquivo de apoio — NEVER SHALL apresentar o
controle: não há o que ler em voz alta.

#### Scenario: O conteúdo em texto oferece ouvir

- **WHEN** a equipe ou o Guerreiro(a) alcança um conteúdo de missão em texto, com a narração
  ligada
- **THEN** um controle de ouvir aparece junto dele, e o conteúdo não foi falado sozinho

#### Scenario: Acionar o controle lê o conteúdo

- **WHEN** o controle de ouvir é acionado
- **THEN** o conteúdo daquele texto é falado

#### Scenario: Conteúdo que não é texto não oferece ouvir

- **WHEN** o conteúdo alcançado é imagem, vídeo, link externo ou arquivo de apoio
- **THEN** nenhum controle de ouvir é apresentado
