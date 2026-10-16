# Spec Delta

## MODIFIED Requirements

### Requirement: O caminho das trilhas leva a equipe à programação do encontro

A App 01 SHALL apresentar à equipe, no caminho das Equipes, em que **missão** da trilha ela
está, o **conteúdo** da missão e a **atividade do dia**, com a bibliografia de apoio
(`RF-04-35`, jornada 5.8).

Havendo mais de uma atividade no encontro, a aplicação SHALL apresentá-las como **escolha da
equipe** — nenhuma é eleita pela aplicação, e a escolha NEVER SHALL ser enviada ao núcleo. É o
encontro assíncrono do documento 05 §4: cada equipe avança no seu ritmo.

A aplicação SHALL mostrar o conteúdo da missão nos tipos que o núcleo serve — texto formatado,
imagem, link externo, vídeo e arquivo de apoio —, **um conteúdo por vez**, com um controle de
**avançar** que leva ao seguinte; avançar SHALL apenas percorrer, e NEVER SHALL gravar nem
enviar coisa alguma. A tela NEVER SHALL declarar a **posição na sequência** — nem escrita, nem
anunciada a quem usa leitor de tela —, e conteúdo **único** NEVER SHALL apresentar controle de
avançar. A **fonte** do conteúdo de terceiro SHALL acompanhar o conteúdo a que pertence, e
NEVER SHALL ser recolhida: é atribuição de autoria alheia, não metadado da obra do Mestre.
Encontro sem programação declarada SHALL exibir aviso em linguagem simples, e não erro nem tela
vazia. (documento 15 §6.4, decisão do fundador de 2026-09-26, revista em 2026-10-16)

Nenhuma tela deste caminho SHALL exibir dado pessoal de Guerreiro(a): a equipe segue
identificada por **avatar e nick**, como já vale para a tela das equipes (`RF-04-34`,
`RN-04-14`). (`RF-04-35`, `RF-04-29`, `RN-04-15`, documento 05 §4, PRD-04 §9)

#### Scenario: A equipe vê a missão, o conteúdo e a atividade do dia

- **WHEN** a equipe escolhida entra no caminho das trilhas num encontro com programação
  declarada
- **THEN** a aplicação mostra a missão, o primeiro conteúdo dela e a atividade do dia

#### Scenario: Duas atividades no encontro viram escolha da equipe

- **WHEN** a programação do encontro traz duas atividades, de trilhas diferentes
- **THEN** a aplicação apresenta as duas e a equipe escolhe, sem que a escolha seja enviada ao
  núcleo

#### Scenario: O conteúdo do dia sai um por vez

- **WHEN** a missão do dia traz três conteúdos
- **THEN** o primeiro aparece sozinho e o controle de avançar leva ao segundo

#### Scenario: A posição na sequência não é declarada

- **WHEN** a equipe percorre os conteúdos da missão do dia, com ou sem leitor de tela
- **THEN** nenhuma contagem de posição é apresentada nem anunciada

#### Scenario: O conteúdo de terceiro sai com a fonte

- **WHEN** a equipe alcança, na sequência, um conteúdo de terceiro
- **THEN** a aplicação exibe a fonte registrada junto do conteúdo, no fluxo de leitura, não
  recolhida

#### Scenario: Nenhum dado pessoal aparece no caminho das trilhas

- **WHEN** a equipe percorre as telas do caminho das trilhas
- **THEN** os integrantes aparecem apenas por avatar e nick, e nenhuma imagem de Guerreiro(a) é
  exibida

#### Scenario: Encontro sem programação avisa em linguagem simples

- **WHEN** a equipe entra no caminho das trilhas num encontro sem programação declarada
- **THEN** a tela avisa em linguagem simples, sem erro e sem tela vazia

## ADDED Requirements

### Requirement: A App 01 narra a pergunta do desafio de desbloqueio

A App 01 SHALL declarar à camada de narração, no caminho das trilhas, a **pergunta da vez** do
desafio de desbloqueio e da sondagem — enunciado e alternativas —, para que seja falada ao ser
alcançada, avançando ou voltando. A fala SHALL obedecer ao alternador da tela inicial: nascendo
a narração desligada, a pergunta NEVER SHALL ser falada antes de alguém ligá-la. (documento 15
§5.1, decisão do fundador de 2026-10-16)

#### Scenario: A pergunta da sondagem é falada no encontro

- **WHEN** a narração está ligada e o Guerreiro(a) recém-inscrito alcança uma pergunta da
  sondagem no aparelho do encontro
- **THEN** o enunciado e as alternativas daquela pergunta são falados

#### Scenario: Cada pergunta alcançada é falada uma vez

- **WHEN** a narração está ligada e o Guerreiro(a) avança pelas perguntas do quiz e volta a uma
  anterior
- **THEN** cada pergunta alcançada é falada ao ser alcançada, e a fala anterior é cancelada
  antes dela

#### Scenario: Com a narração desligada a pergunta não fala

- **WHEN** a narração está desligada e o Guerreiro(a) alcança uma pergunta do quiz
- **THEN** nada é falado, e a pergunta segue inteiramente legível na tela
