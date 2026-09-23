## ADDED Requirements

### Requirement: Quem integra a equipe a renomeia pelo aparelho

A App 01 SHALL oferecer **renomear** a equipe a quem a integra, na tela das equipes da aula e
na da equipe da trilha, com a mesma regra do nome da criação. A aplicação NEVER SHALL oferecer
renomear a quem não integra a equipe, nem à equipe da trilha já homologada. A recusa do núcleo
— nome repetido, em branco ou longo demais, aula encerrada — SHALL aparecer em linguagem
simples, e o nome anterior SHALL continuar na tela. (`RF-04-70`, `RN-04-39`, `RN-04-36`)

#### Scenario: Integrante troca o nome da equipe

- **WHEN** um integrante em sessão renomeia a equipe para um nome livre na aula
- **THEN** a tela passa a mostrar a equipe com o nome novo

#### Scenario: Quem não integra não vê a opção de renomear

- **WHEN** a tela das equipes mostra uma equipe de que o Guerreiro(a) em sessão não participa
- **THEN** a aplicação não oferece renomeá-la

#### Scenario: Nome repetido é recusado em linguagem simples

- **WHEN** um integrante tenta renomear a equipe com o nome de outra equipe da aula
- **THEN** a aplicação apresenta a recusa em linguagem simples e o nome anterior continua

#### Scenario: Equipe da trilha homologada não oferece renomear

- **WHEN** a tela da equipe da trilha já homologada é apresentada
- **THEN** a aplicação não oferece renomeá-la

## MODIFIED Requirements

### Requirement: O Guerreiro(a) forma a equipe da aula pelo aparelho, com o papel declarado

A App 01 SHALL permitir ao Guerreiro(a) em sessão **criar** equipe da aula vigente, **entrar**
em equipe já formada e **sair** da que integra, **sem aprovação de terceiro**, declarando o
**papel** que terá — que vale para o encontro inteiro e é opcional. Criar SHALL exigir o
**nome** da equipe, obrigatório e de até 20 caracteres: a aplicação NEVER SHALL enviar a
criação com o nome em branco, e SHALL limitar o campo a 20 caracteres. A aplicação SHALL
apresentar as recusas do núcleo — sexto integrante, segundo integrante de 17 anos ou mais e
nome repetido na aula — em linguagem simples, sem código de erro cru. (`RF-04-30`, `RF-04-31`,
`RF-04-59`, `RF-04-69`, `RN-04-15`, `RN-04-16`, `RN-04-30`, `RN-04-39`, PRD-04 §12)

#### Scenario: Guerreiro(a) cria a equipe e entra nela

- **WHEN** um Guerreiro(a) em sessão cria uma equipe da aula vigente, dando o nome dela
- **THEN** a equipe nasce com aquele nome e com ele como primeiro integrante, sem aprovação de
  ninguém

#### Scenario: Criar sem nome não sai do aparelho

- **WHEN** um Guerreiro(a) pede para criar a equipe com o nome em branco
- **THEN** a aplicação pede o nome e não envia a criação

#### Scenario: Nome repetido na aula é recusado em linguagem simples

- **WHEN** um Guerreiro(a) cria a equipe com o nome de outra equipe da mesma aula
- **THEN** a aplicação apresenta a recusa em linguagem simples e nenhuma equipe é criada

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

A App 01 SHALL apresentar as equipes já formadas na aula vigente pelo **nome** da equipe e, em
cada uma, os integrantes por **avatar e nick**, e NEVER SHALL exibir nome civil, data de
nascimento, imagem ou qualquer outro dado pessoal de um Guerreiro(a) para outro. (`RF-04-34`,
`RN-04-14`, documento 99 §6 invariante 11)

#### Scenario: As equipes da aula aparecem por avatar e nick

- **WHEN** o Guerreiro(a) em sessão abre a tela das equipes da aula vigente
- **THEN** cada equipe aparece com o nome dela e com o avatar e o nick de cada integrante, e
  nada além disso

#### Scenario: Nenhuma imagem de um Guerreiro(a) é exibida a outro

- **WHEN** a tela das equipes é apresentada
- **THEN** nenhuma fotografia de Guerreiro(a) aparece em tela alguma

#### Scenario: Equipes de outra aula não aparecem

- **WHEN** a tela das equipes da aula vigente é apresentada
- **THEN** as equipes formadas em outras aulas não estão entre as exibidas

### Requirement: A equipe forma a equipe da trilha pelo aparelho, a partir da programação

A App 01 SHALL oferecer, na programação do encontro, a formação da **equipe da trilha** da
atividade que a equipe escolheu: o Guerreiro(a) em sessão **cria** a equipe daquela trilha,
dando o **nome** dela com a mesma regra da equipe da aula, ou **entra** na que já existe,
declarando o **papel** que terá, sem aprovação de terceiro. A equipe da trilha SHALL aparecer
pelo nome.

A aplicação SHALL apresentar as recusas do núcleo em **linguagem simples**, sem código de erro
cru: o sexto integrante, o segundo integrante de 17 anos ou mais, a segunda equipe da mesma
trilha e o nome repetido na trilha. Enquanto a equipe da trilha **não** estiver homologada, a
aplicação SHALL oferecer a entrada e a saída; depois de homologada, NEVER SHALL oferecer
nenhuma das duas. (`RF-04-61`, `RF-04-69`, `RN-04-39`, `RN-01-44`, documento 99 §6
invariante 15)

#### Scenario: A formação parte da atividade escolhida

- **WHEN** a equipe declarou a atividade que está trabalhando e abre a formação da equipe da
  trilha
- **THEN** a aplicação forma a equipe da **trilha daquela atividade**, sem pedir que alguém a
  escolha de novo

#### Scenario: Guerreiro(a) cria a equipe da trilha e entra nela

- **WHEN** um Guerreiro(a) em sessão cria a equipe da trilha, dando o nome dela
- **THEN** a equipe nasce com aquele nome e com ele como primeiro integrante, sem aprovação de
  ninguém

#### Scenario: A segunda equipe da mesma trilha é recusada em linguagem simples

- **WHEN** um Guerreiro(a) que já integra uma equipe daquela trilha tenta criar outra
- **THEN** a aplicação apresenta a recusa em linguagem simples e ele segue na primeira

#### Scenario: Equipe homologada não oferece entrar nem sair

- **WHEN** a tela da equipe da trilha já homologada é apresentada
- **THEN** nenhuma ação de entrar ou de sair é oferecida
