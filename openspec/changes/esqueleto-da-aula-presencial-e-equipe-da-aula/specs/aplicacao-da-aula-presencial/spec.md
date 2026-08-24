## Purpose

A App 01 é a aplicação do encontro presencial, usada pelos próprios Guerreiros e Guerreiras no
aparelho do ponto de apoio. Esta capacidade cobre a sessão de trabalho do aparelho — que só
existe dentro da janela de uma aula agendada e é dela que sai a comunidade —, a tela inicial dos
dois caminhos, a entrada do Guerreiro(a) no encontro e a formação da equipe da aula.

## ADDED Requirements

### Requirement: A App 01 se identifica por chave e só opera dentro da janela de uma aula agendada

A App 01 SHALL apresentar a chave de aplicação dela em toda chamada ao núcleo. A aplicação
SHALL consultar as aulas vigentes para a data e a hora correntes e, **não havendo nenhuma**,
NEVER SHALL abrir: SHALL informar em **uma frase** que não há aula agendada, sem oferecer
caminho algum. (`RF-04-02`, `RN-04-01`, `RF-01-02`, PRD-04 §12)

#### Scenario: A chave acompanha toda chamada

- **WHEN** a aplicação chama qualquer rota de dados do núcleo
- **THEN** a chamada leva a chave de aplicação da App 01 do ambiente em que ela roda

#### Scenario: Sem aula vigente a aplicação não abre

- **WHEN** o aparelho é aberto fora da janela de qualquer aula agendada
- **THEN** a aplicação informa em uma frase que não há aula agendada, e nem o onboarding nem as
  trilhas ficam alcançáveis

#### Scenario: Nenhuma aula vigente não é erro

- **WHEN** a consulta de aulas vigentes devolve conjunto vazio
- **THEN** a aplicação trata a resposta como situação normal, sem apresentar código de erro cru

### Requirement: A comunidade vem da aula vigente, perguntada uma única vez

A App 01 SHALL adotar a comunidade da aula vigente sem perguntá-la a ninguém quando houver
**uma** aula. Havendo **mais de uma**, SHALL perguntar **uma única vez** em qual comunidade o
aparelho está operando e SHALL usar essa escolha até o fim da sessão de trabalho, sem repetir a
pergunta. O Guerreiro(a) NEVER SHALL informar a comunidade. (`RF-04-03`, `RN-04-02`, PRD-04 §12)

#### Scenario: Uma aula vigente dispensa a pergunta

- **WHEN** há exatamente uma aula vigente
- **THEN** a aplicação adota a comunidade daquela aula e não pergunta nada

#### Scenario: Duas aulas vigentes perguntam uma vez

- **WHEN** há duas aulas vigentes em comunidades diferentes
- **THEN** a aplicação pergunta uma única vez em qual comunidade opera

#### Scenario: A escolha não se repete na sessão

- **WHEN** a comunidade já foi escolhida e novos atendimentos acontecem na mesma sessão de
  trabalho
- **THEN** a aplicação segue na comunidade escolhida, sem perguntar de novo

### Requirement: A sessão de trabalho do aparelho é aberta por Mestre ou Admin e cai com a janela da aula

A App 01 SHALL exigir que a sessão de trabalho do aparelho seja aberta por **Mestre ou Admin**
autenticado por login social. A sessão SHALL valer pela **janela da aula agendada** e, encerrado
o horário final declarado no agendamento, a aplicação SHALL exigir nova autenticação do Mestre
ou do Admin antes de qualquer novo atendimento. (`RF-04-05`, `RN-04-29`, PRD-04 §13)

#### Scenario: Mestre abre a sessão de trabalho

- **WHEN** um Mestre autentica pela conta social no aparelho
- **THEN** a aplicação abre a sessão de trabalho e apresenta a tela inicial

#### Scenario: Admin abre a sessão de trabalho

- **WHEN** um Admin autentica pela conta social no aparelho
- **THEN** a aplicação abre a sessão de trabalho e apresenta a tela inicial

#### Scenario: Guerreiro(a) não abre a sessão de trabalho

- **WHEN** alguém tenta abrir a sessão de trabalho do aparelho com credencial de Guerreiro(a)
- **THEN** a aplicação recusa em linguagem simples e nenhuma sessão de trabalho é aberta

#### Scenario: Encerrada a janela, o aparelho exige nova autenticação

- **WHEN** o horário final da aula agendada passa
- **THEN** a aplicação encerra a sessão de trabalho e exige nova autenticação de Mestre ou Admin

### Requirement: A tela inicial oferece os dois caminhos e volta ao início a cada atendimento

A App 01 SHALL apresentar, na tela inicial, os dois caminhos — **onboarding** e **trilhas**. Ao
fim de cada atendimento, a aplicação SHALL voltar à tela inicial e NEVER SHALL exibir dado do
atendimento anterior. Quem escolhe **trilhas** sem sessão de Guerreiro(a) aberta SHALL ser
levado à entrada do Guerreiro(a), nunca ao cadastro. (`RF-04-01`, `RF-04-28`, PRD-04 §12)

#### Scenario: Os dois caminhos aparecem

- **WHEN** a sessão de trabalho está aberta
- **THEN** a tela inicial apresenta o caminho do onboarding e o caminho das trilhas

#### Scenario: Trilhas sem sessão leva à entrada, não ao cadastro

- **WHEN** alguém escolhe trilhas sem sessão de Guerreiro(a) aberta
- **THEN** a aplicação apresenta a entrada do Guerreiro(a), e nenhuma tela de cadastro aparece

#### Scenario: O atendimento seguinte começa limpo

- **WHEN** um atendimento termina e a aplicação volta à tela inicial
- **THEN** nenhum dado do atendimento anterior aparece em tela alguma

### Requirement: O Guerreiro(a) entra no caminho das trilhas por confirmação de Mestre ou Admin

A App 01 SHALL abrir a sessão do Guerreiro(a) pela **confirmação de identidade** feita por
Mestre ou Admin presente no encontro, com registro de quem confirmou. A recusa de biometria e a
ausência de _template_ NEVER SHALL deixar o Guerreiro(a) fora da aula: a confirmação humana é a
alternativa equivalente. (`RF-04-29`, `RF-04-15`, `RN-04-09`, PRD-04 §§5.3, 5.5)

Nesta fatia a captura por nick e imagem não é oferecida — a entrada por imagem entra com o
caminho do onboarding, e até lá **toda** entrada passa pela confirmação humana.

#### Scenario: Mestre confirma e a sessão do Guerreiro(a) abre

- **WHEN** o Guerreiro(a) informa o nick e o Mestre presente confirma a identidade dele
- **THEN** a aplicação abre a sessão do Guerreiro(a) e registra quem confirmou

#### Scenario: A recusa não exclui ninguém da aula

- **WHEN** um Guerreiro(a) sem _template_ gravado chega ao caminho das trilhas
- **THEN** a aplicação o encaminha à confirmação humana, sem tentativa de captura e sem
  impedi-lo de participar

#### Scenario: Nenhuma imagem de criança sai do aparelho nesta fatia

- **WHEN** qualquer entrada de Guerreiro(a) acontece
- **THEN** nenhuma requisição da aplicação carrega fotografia, e nenhuma imagem é gravada no
  aparelho compartilhado

### Requirement: O Guerreiro(a) forma a equipe da aula pelo aparelho, com o papel declarado

A App 01 SHALL permitir ao Guerreiro(a) em sessão **criar** equipe da aula vigente, **entrar**
em equipe já formada e **sair** da que integra, **sem aprovação de terceiro**, declarando o
**papel** que terá — que vale para o encontro inteiro e é opcional. A aplicação SHALL apresentar
as recusas do núcleo — sexto integrante e segundo integrante de 17 anos ou mais — em linguagem
simples, sem código de erro cru. (`RF-04-30`, `RF-04-31`, `RF-04-59`, `RN-04-15`, `RN-04-16`,
`RN-04-30`, PRD-04 §12)

#### Scenario: Guerreiro(a) cria a equipe e entra nela

- **WHEN** um Guerreiro(a) em sessão cria uma equipe da aula vigente
- **THEN** a equipe nasce com ele como primeiro integrante, sem aprovação de ninguém

#### Scenario: Papel declarado na entrada

- **WHEN** um Guerreiro(a) entra numa equipe declarando o papel que terá
- **THEN** a aplicação envia o papel junto da entrada

#### Scenario: Papel é opcional

- **WHEN** um Guerreiro(a) entra numa equipe sem declarar papel
- **THEN** a aplicação registra a entrada assim mesmo

#### Scenario: A sexta pessoa lê a recusa em linguagem simples

- **WHEN** uma sexta pessoa tenta entrar numa equipe de cinco
- **THEN** a aplicação apresenta a recusa em linguagem simples e a composição não muda

#### Scenario: Guerreiro(a) sai da equipe por conta própria

- **WHEN** um integrante pede para sair da equipe que integra
- **THEN** a aplicação registra a saída, sem aprovação de terceiro

### Requirement: A tela das equipes mostra apenas avatar e nick

A App 01 SHALL apresentar as equipes já formadas na aula vigente por **avatar e nick**, e
NEVER SHALL exibir nome, data de nascimento, imagem ou qualquer outro dado pessoal de um
Guerreiro(a) para outro. (`RF-04-34`, `RN-04-14`, documento 99 §6 invariante 11)

#### Scenario: As equipes da aula aparecem por avatar e nick

- **WHEN** o Guerreiro(a) em sessão abre a tela das equipes da aula vigente
- **THEN** cada equipe aparece com o avatar e o nick de cada integrante, e nada além disso

#### Scenario: Nenhuma imagem de um Guerreiro(a) é exibida a outro

- **WHEN** a tela das equipes é apresentada
- **THEN** nenhuma fotografia de Guerreiro(a) aparece em tela alguma

#### Scenario: Equipes de outra aula não aparecem

- **WHEN** a tela das equipes da aula vigente é apresentada
- **THEN** as equipes formadas em outras aulas não estão entre as exibidas

### Requirement: A App 01 não forma equipe pela gestão nem homologa equipe da trilha

A App 01 NEVER SHALL oferecer a Mestre ou Admin a formação ou a alteração da composição de
equipe: a sessão de trabalho do aparelho autentica o encontro, e quem forma equipe é o
Guerreiro(a) em sessão. A **homologação da equipe da trilha** NEVER SHALL aparecer nesta
aplicação — é ato do Mestre, na App 09. (`RN-04-18`, `RF-01-16`, `RF-01-63`, documento 99 §6
invariante 15)

#### Scenario: A sessão de trabalho não forma equipe

- **WHEN** a sessão de trabalho do aparelho está aberta e nenhum Guerreiro(a) tem sessão
- **THEN** a aplicação não oferece criar equipe, entrar nem sair

#### Scenario: A homologação não aparece na App 01

- **WHEN** qualquer tela de equipe é apresentada
- **THEN** nenhuma ação de homologar equipe da trilha é oferecida
