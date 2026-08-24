## MODIFIED Requirements

### Requirement: O Admin cadastra o Guerreiro(a) com nome, nascimento, nick e avatar

O núcleo SHALL expor rota de **Admin** que cria persona de Guerreiro(a) com **nome**, **data de
nascimento**, **nick** e **características do avatar**. Persona de qualquer outro papel SHALL
receber **403**. Cadastro sem um dos quatro SHALL ser recusado com **422**, indicando o campo em
falta, e nick já usado por qualquer persona SHALL ser recusado com **422** no campo `nick`, sem
dizer de quem é. A data de nascimento que resulte em idade **fora da faixa de 6 a 16 anos** SHALL
ser recusada com **422** no campo `nascimento`, pela mesma regra que o caminho do encontro
aplica — a faixa é invariante da plataforma, não requisito de uma aplicação. A escrita SHALL
gravar autoria, data e hora, como toda escrita do núcleo. (`RF-02-01`, `RF-01-19`, `RN-01-30`,
`RN-02-21`, `RN-04-11`, documento 99 §6 invariante 2)

O onboarding conduzido pelo App 01, em que a própria criança se cadastra, é do PRD-04; esta
rota é o caminho da gestão. A recusa por nick em uso **não** devolve variações neste caminho:
as variações de alcance total são exceção declarada apenas do cadastro do encontro, na
capacidade `persona-e-credencial`.

#### Scenario: Admin cadastra o Guerreiro(a)

- **WHEN** um Admin em sessão cadastra um Guerreiro(a) com nome, nascimento, nick e avatar
- **THEN** o núcleo grava a persona com o autor, a data e a hora

#### Scenario: Cadastro sem nick é recusado

- **WHEN** chega o cadastro de um Guerreiro(a) sem nick
- **THEN** o núcleo responde 422 indicando o campo em falta e nada é gravado

#### Scenario: Nick em uso é recusado sem revelar o dono

- **WHEN** chega o cadastro de um Guerreiro(a) com nick já usado por outra persona
- **THEN** o núcleo responde 422 no campo `nick`, sem dizer de quem é o nick nem de que papel

#### Scenario: Mestre não cadastra Guerreiro(a)

- **WHEN** um Mestre em sessão tenta cadastrar um Guerreiro(a)
- **THEN** o núcleo responde 403 e nada é gravado

#### Scenario: Idade fora da faixa é recusada também pela gestão

- **WHEN** um Admin cadastra um Guerreiro(a) cuja data de nascimento resulta em idade fora de 6
  a 16 anos
- **THEN** o núcleo responde 422 no campo `nascimento` e nada é gravado

#### Scenario: A gestão não recebe variações de nick

- **WHEN** o cadastro pela gestão é recusado por nick em uso
- **THEN** a recusa não traz variações sugeridas
