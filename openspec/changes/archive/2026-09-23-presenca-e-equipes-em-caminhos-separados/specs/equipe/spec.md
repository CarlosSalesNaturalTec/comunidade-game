# Spec Delta

## ADDED Requirements

### Requirement: Formar ou entrar em equipe da aula exige presença registrada naquela aula

O núcleo SHALL recusar, com **422**, a **criação** de equipe da aula e a **entrada** em equipe
vinculada a uma aula quando o Guerreiro(a) em sessão não tiver presença **não anulada** naquela
aula. A recusa SHALL dizer o que é — falta a presença do encontro —, e NEVER SHALL ser
apresentada como recusa de composição nem como falha de rede (`RN-04-36`). (`RF-04-68`,
`RN-04-40`)

A guarda SHALL alcançar apenas as rotas em que a aula do encontro é determinável: a criação de
equipe da aula e a entrada em equipe cujo vínculo é uma aula. **Sair** da equipe e
**renomeá-la** NEVER SHALL exigir presença — quem já está dentro não é barrado por ela —, e a
equipe da **trilha**, cujas rotas não carregam a aula do encontro, SHALL seguir sem essa guarda
no núcleo; no App 01 ela só é alcançada dentro do caminho das equipes, já atrás da guarda do
aparelho.

#### Scenario: Sem presença, a equipe da aula não se cria

- **WHEN** um Guerreiro(a) sem presença registrada naquela aula pede a criação de equipe
- **THEN** o núcleo responde 422, dizendo que falta a presença do encontro, e nenhuma equipe é
  criada

#### Scenario: Sem presença, não se entra em equipe da aula

- **WHEN** um Guerreiro(a) sem presença registrada naquela aula pede entrada numa equipe dela
- **THEN** o núcleo responde 422 e a composição não muda

#### Scenario: Com presença registrada, a formação corre como antes

- **WHEN** um Guerreiro(a) com presença registrada naquela aula cria equipe ou entra em uma
- **THEN** o núcleo responde como já respondia, sem recusa nova

#### Scenario: Presença anulada barra a formação

- **WHEN** a presença do Guerreiro(a) naquela aula foi anulada e ele pede entrada numa equipe
- **THEN** o núcleo responde 422 e a composição não muda

#### Scenario: Quem já está dentro sai e renomeia sem presença

- **WHEN** um integrante cuja presença foi anulada pede a própria saída da equipe ou a troca do
  nome dela
- **THEN** o núcleo atende, como já atendia, sem exigir presença

#### Scenario: A equipe da trilha não recebe a guarda no núcleo

- **WHEN** um Guerreiro(a) cria equipe da trilha ou entra numa equipe vinculada a uma trilha
- **THEN** o núcleo não confere presença alguma, porque a rota não carrega a aula do encontro
