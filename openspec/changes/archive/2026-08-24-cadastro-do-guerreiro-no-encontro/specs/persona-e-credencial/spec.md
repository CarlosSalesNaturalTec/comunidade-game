## ADDED Requirements

### Requirement: A persona de Guerreiro(a) tem idade entre 6 e 16 anos

O núcleo SHALL recusar a criação de persona de Guerreiro(a) cuja **data de nascimento** resulte
em idade **fora da faixa de 6 a 16 anos**, apurada na data da criação, com **422** no campo
`nascimento`. A recusa SHALL valer para **todo** caminho que crie Guerreiro(a) — o autocadastro
do encontro e o cadastro pela gestão —, porque a faixa é invariante da plataforma e não regra de
uma aplicação. Os extremos SHALL ser aceitos. (`RN-04-11`, `RF-04-09`, documento 99 §6
invariante 2, documento 02 §1)

Decisão do fundador, 2026-08-24: a faixa passa a ser exigida na regra do núcleo, e vale também
para o caminho da gestão, que até aqui conferia apenas a presença da data de nascimento.

#### Scenario: Idade abaixo da faixa é recusada

- **WHEN** chega a criação de um Guerreiro(a) cuja data de nascimento resulta em idade menor que
  6 anos
- **THEN** o núcleo responde 422 no campo `nascimento` e nenhuma persona passa a existir

#### Scenario: Idade acima da faixa é recusada

- **WHEN** chega a criação de um Guerreiro(a) cuja data de nascimento resulta em idade maior que
  16 anos
- **THEN** o núcleo responde 422 no campo `nascimento` e nenhuma persona passa a existir

#### Scenario: Os extremos da faixa são aceitos

- **WHEN** chega a criação de um Guerreiro(a) com exatamente 6 anos, ou com exatamente 16
- **THEN** o núcleo cria a persona

#### Scenario: A faixa alcança o caminho da gestão

- **WHEN** um Admin cadastra pela gestão um Guerreiro(a) com idade fora da faixa
- **THEN** o núcleo responde 422 no campo `nascimento`, como responderia ao cadastro do encontro

## MODIFIED Requirements

### Requirement: Só o Guerreiro(a) tem autocadastro

O núcleo SHALL aceitar autocadastro apenas do Guerreiro(a). Mestre e Apoiador SHALL ser
cadastrados por Admin; o responsável, por Admin ou Mestre; e Admin novo SHALL entrar apenas por
inclusão de outro Admin. Login NEVER SHALL criar persona. (`RN-01-01`, `RN-01-02`, `RN-01-04`)

O autocadastro do Guerreiro(a) SHALL ser **autenticado pela sessão de trabalho do aparelho da
App 01**, aberta por Mestre ou Admin presente no encontro, e essa autenticação NEVER SHALL
tornar-se **autoria** do cadastro: a persona criada por esse caminho não tem adulto como criador,
e o cadastro segue sendo do próprio Guerreiro(a). O caminho da **gestão**, restrito a Admin e
com autoria dele, permanece existindo ao lado deste e NEVER SHALL ser confundido com ele.
(`RF-04-07`, `RN-04-04`, PRD-04 §9, documento 99 §6 invariante 3)

#### Scenario: Adulto não se autocadastra

- **WHEN** uma criação de persona de Mestre, Apoiador ou responsável chega sem a autoria de um
  Admin — ou de um Mestre, no caso do responsável
- **THEN** o núcleo recusa a criação

#### Scenario: Admin novo exige Admin existente

- **WHEN** uma criação de persona de Admin chega sem a autoria de outro Admin
- **THEN** o núcleo recusa a criação, ressalvada a semeadura da implantação

#### Scenario: A sessão de trabalho autentica o autocadastro sem ser autora dele

- **WHEN** um Guerreiro(a) é cadastrado pelo caminho do encontro, sob a sessão de trabalho de um
  Mestre ou de um Admin
- **THEN** a persona é criada sem adulto algum como criador dela

#### Scenario: Sem sessão de trabalho não há autocadastro

- **WHEN** chega uma criação de Guerreiro(a) pelo caminho do encontro sem sessão de trabalho de
  Mestre ou Admin
- **THEN** o núcleo recusa a criação e nenhuma persona passa a existir

#### Scenario: O caminho da gestão continua sendo de Admin e com autoria dele

- **WHEN** um Admin cadastra um Guerreiro(a) pelo caminho da gestão
- **THEN** a persona é criada com o Admin como criador dela

### Requirement: O núcleo nunca descobre nem sugere um nick

O núcleo SHALL responder a busca por nick **apenas por correspondência exata**. O núcleo NEVER
SHALL expor listagem de nicks, busca parcial, ordenação por semelhança, contagem de resultados
ou sugestão de variação que **alcance nick de Guerreiro(a)** — a vedação é definida pelo que a
resposta alcança, não por quem pergunta, e por isso vale igualmente para persona autenticada
como adulto e para visitante sem sessão. A recusa por nick inexistente NEVER SHALL ser
distinguível da recusa por outro motivo. (`RN-01-22`, `RN-14-23`, invariante 12 do documento
99 §6)

Há **duas** exceções declaradas, e nenhuma outra:

1. A conferência de disponibilidade restrita a **nicks de adulto**, da capacidade
   `identidade-do-adulto`, que existe precisamente porque não alcança nick de Guerreiro(a).
2. A **recusa de gravação** do cadastro do Guerreiro(a) no encontro, que SHALL devolver, no
   corpo da própria recusa por nick em uso, até três **variações** conferidas contra **todos os
   papéis**. Esta exceção SHALL existir apenas como resposta a uma tentativa de escrita
   recusada, e o núcleo NEVER SHALL expor rota de **consulta** com esse alcance. Decisão do
   fundador, 2026-08-24: o que sobra de oráculo exige, cumulativamente, a chave da App 01,
   sessão de trabalho aberta, aula agendada vigente e Mestre ou Admin autenticado no encontro —
   é a presencialidade pagando o que a rota pública não pode pagar. (`RF-04-08`, `RN-04-05`)

#### Scenario: Busca por nick é exata

- **WHEN** o núcleo procura uma persona por nick, em qualquer caminho interno ou de rota
- **THEN** a correspondência é exata, e nick parcial não alcança persona alguma

#### Scenario: Não existe rota que liste ou sugira nick

- **WHEN** se procura no núcleo uma rota de **consulta** que liste nicks de Guerreiro(a),
  complete um nick parcial de Guerreiro(a) ou sugira variações a partir dele
- **THEN** nenhuma existe — a única sugestão de alcance total do núcleo é a que acompanha a
  recusa de uma tentativa de escrita, nunca a resposta de uma consulta

#### Scenario: Adulto autenticado não descobre nick de Guerreiro(a)

- **WHEN** uma persona autenticada como adulto consulta um nick que não é de adulto
- **THEN** a resposta não distingue nick inexistente de nick de Guerreiro(a)

#### Scenario: A recusa do cadastro do encontro devolve variações de alcance total

- **WHEN** o cadastro de um Guerreiro(a) pelo caminho do encontro é recusado por nick já usado
- **THEN** a recusa traz até três variações, nenhuma delas em uso por persona de qualquer papel

#### Scenario: A conferência pública segue alcançando só nick de adulto

- **WHEN** a conferência pública de disponibilidade recebe um nick usado por um Guerreiro(a)
- **THEN** ela responde como responderia a um nick livre, sem alcançar a persona que o tem

#### Scenario: A recusa não diz de quem é o nick

- **WHEN** a recusa por nick em uso é devolvida, em qualquer dos caminhos de cadastro
- **THEN** ela não identifica a persona que tem o nick nem o papel dela
