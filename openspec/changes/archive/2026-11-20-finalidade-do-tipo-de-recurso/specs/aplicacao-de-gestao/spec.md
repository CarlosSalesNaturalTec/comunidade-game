## ADDED Requirements

### Requirement: A área Catálogos cadastra, mostra e corrige a finalidade do tipo de recurso

A área Catálogos da App 03 SHALL pedir a **finalidade** — consumo do encontro ou recompensa — no
cadastro de tipo de recurso não durável, e não SHALL pedi-la no durável. A lista SHALL mostrar a
finalidade de cada tipo, e a alteração do tipo SHALL permitir corrigi-la no mesmo formulário de
nome, unidade e exige comprovante. Recusa do núcleo SHALL aparecer em linguagem simples, no
campo. (`RF-02-107`, `RF-02-113`, `RF-07-53`)

#### Scenario: O catálogo mostra a finalidade

- **WHEN** o Admin abre a área Catálogos
- **THEN** cada tipo de recurso não durável aparece com a finalidade, e o durável sem ela

#### Scenario: O Admin corrige a finalidade pela aplicação

- **WHEN** o Admin altera a finalidade de um tipo de recompensa para consumo do encontro
- **THEN** a aplicação envia a correção ao núcleo e a lista passa a mostrar a finalidade nova

### Requirement: O seletor de recursos da aula oferece só consumo do encontro

O formulário de agendamento da App 03 SHALL oferecer, entre os recursos que a aula consome, só
tipo de recurso ativo de finalidade **consumo do encontro**. (`RF-02-31`, `RF-07-53`)

#### Scenario: O kit de recompensa não aparece no agendamento

- **WHEN** o Admin abre o formulário de agendamento com um tipo de recompensa e um de consumo do
  encontro no catálogo
- **THEN** o seletor de recursos oferece só o de consumo do encontro
