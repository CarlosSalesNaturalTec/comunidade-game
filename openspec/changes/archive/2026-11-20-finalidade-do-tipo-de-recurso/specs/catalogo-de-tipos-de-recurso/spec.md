## ADDED Requirements

### Requirement: O tipo de recurso não durável tem uma finalidade

O núcleo SHALL guardar, em todo tipo de recurso de natureza **consumível, serviço ou
financeira**, uma **finalidade** — **consumo do encontro** ou **recompensa** —, uma só. O tipo de
natureza **durável** NEVER SHALL ter finalidade: é patrimônio, nem reservável nem recompensa.
Cadastro de tipo não durável sem finalidade, ou com finalidade fora das duas previstas, SHALL
ser recusado com **422**, indicando o campo; cadastro de tipo durável que declare finalidade
SHALL ser recusado com **422**. A leitura do catálogo SHALL trazer a finalidade de cada tipo.
(`RF-07-53`, `RF-07-01`, `RN-07-41`, PRD-07 §8)

#### Scenario: Admin cadastra tipo com finalidade

- **WHEN** um Admin em sessão cadastra um tipo consumível com a finalidade consumo do encontro
- **THEN** o núcleo grava o tipo com a finalidade, e a leitura do catálogo a traz

#### Scenario: Tipo não durável sem finalidade é recusado

- **WHEN** chega o cadastro de um tipo de serviço sem finalidade
- **THEN** o núcleo responde 422 indicando a finalidade e nada é gravado

#### Scenario: Tipo durável não tem finalidade

- **WHEN** chega o cadastro de um tipo durável que declara a finalidade recompensa
- **THEN** o núcleo responde 422 e nada é gravado

### Requirement: O Admin corrige a finalidade do tipo

O núcleo SHALL permitir ao **Admin** em sessão corrigir a finalidade de tipo não durável já
cadastrado, no mesmo ato que altera nome, unidade e exige comprovante, com autoria, data e hora.
Finalidade em tipo durável SHALL ser recusada com **422**. Persona de qualquer outro papel SHALL
receber **403**. A correção SHALL valer só para **escolha nova** do tipo: aula, reserva,
recompensa de marco, item do catálogo avulso e desafio extra já gravados com ele SHALL seguir
inalterados. (`RF-07-51`, `RF-07-53`, `RF-07-52`)

#### Scenario: Admin passa um tipo a consumo do encontro

- **WHEN** um Admin em sessão corrige a finalidade de um tipo de recompensa para consumo do
  encontro
- **THEN** o núcleo grava a finalidade nova com o autor, a data e a hora, e a aula passa a
  aceitar o tipo em agendamento novo

#### Scenario: A correção não alcança o que já foi gravado

- **WHEN** um Admin corrige para consumo do encontro um tipo usado por recompensa de marco já
  declarada
- **THEN** a recompensa segue declarada com o tipo, sem alteração

#### Scenario: Mestre não corrige a finalidade

- **WHEN** um Mestre em sessão tenta corrigir a finalidade de um tipo
- **THEN** o núcleo responde 403 e o tipo permanece como estava

### Requirement: Os tipos já cadastrados nascem com a finalidade recompensa

A migração que cria a finalidade SHALL dar **recompensa** a todo tipo de recurso não durável já
cadastrado e nenhuma ao durável; o Admin corrige depois, pela correção da finalidade, os que
forem de consumo do encontro. Nenhum registro gravado com o tipo SHALL mudar. (`RF-07-53`,
`RF-07-51`, decisão do fundador de 2026-11-20)

#### Scenario: Tipo existente recebe recompensa

- **WHEN** a migração roda sobre um catálogo com um tipo consumível e um durável
- **THEN** o consumível passa a ter a finalidade recompensa, e o durável segue sem finalidade
