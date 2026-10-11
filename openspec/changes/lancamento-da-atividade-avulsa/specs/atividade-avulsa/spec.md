# Spec Delta

## MODIFIED Requirements

### Requirement: A atividade avulsa é cadastrada por Admin, fora de trilha e sem missão

O núcleo SHALL registrar a **atividade avulsa** com **título**, **descrição**, **modalidade**,
**formato**, **natureza**, **produção esperada**, o **poder** que ela desenvolve e a **aula** do
encontro em que acontece, **sem missão** — é o que a distingue da atividade de trilha, que
sempre pertence a uma. Cadastrar atividade avulsa SHALL exigir persona **Admin** em sessão;
persona de qualquer outro papel SHALL receber **403**, inclusive o Mestre, cuja bancada de
autoria é a App 09.

Cadastro sem título, sem modalidade, sem formato, sem natureza, sem produção esperada, sem
poder ou **sem aula** SHALL ser recusado com **422**, indicando o campo em falta. Modalidade e
formato SHALL ficar fechados nos valores do documento 11 §4, e valor fora deles SHALL ser
recusado com **422**; a natureza SHALL seguir aberta, como na atividade de trilha. A escrita
SHALL gravar autoria, data e hora com fuso. (`RF-02-29`, `RF-01-16`, `RF-01-03`, `RF-01-27`,
documento 11 §4, PRD-02 §3.2)

A aula declarada SHALL existir e NÃO SHALL estar **cancelada**; aula inexistente ou cancelada
SHALL ser recusada com **422**. O **formato** da atividade avulsa SHALL ser **presencial**:
declarar aula é o que a prende ao encontro, e a regra da capacidade `atividade-de-trilha` já
recusa com **422** a atividade on-line ou assíncrona que declare uma. A **comunidade** da
avulsa SHALL ser a da aula declarada, e o cadastro NEVER SHALL receber campo de comunidade
próprio — a aula já a declara (documento 11 §4, documento 09 §1).

#### Scenario: Admin cadastra a atividade avulsa

- **WHEN** um Admin em sessão cadastra uma atividade com título, modalidade, formato, natureza,
  produção esperada, poder e a aula do encontro
- **THEN** o núcleo grava a atividade sem missão, com autor, data e hora com fuso

#### Scenario: Mestre não cadastra atividade avulsa

- **WHEN** um Mestre em sessão tenta cadastrar uma atividade avulsa
- **THEN** o núcleo responde 403 e nada é gravado

#### Scenario: Cadastro sem produção esperada é recusado

- **WHEN** chega um cadastro de atividade avulsa sem a produção esperada
- **THEN** o núcleo responde 422 indicando o campo em falta e nada é gravado

#### Scenario: Modalidade fora dos valores previstos é recusada

- **WHEN** chega um cadastro de atividade avulsa com modalidade que não é nenhum dos valores do
  documento 11 §4
- **THEN** o núcleo responde 422 e nada é gravado

#### Scenario: Cadastro sem aula é recusado

- **WHEN** chega um cadastro de atividade avulsa sem a aula do encontro
- **THEN** o núcleo responde 422 indicando o campo em falta e nada é gravado

#### Scenario: Aula cancelada é recusada

- **WHEN** chega um cadastro de atividade avulsa declarando uma aula já cancelada
- **THEN** o núcleo responde 422 e nada é gravado

#### Scenario: Formato on-line é recusado na avulsa

- **WHEN** chega um cadastro de atividade avulsa de formato on-line ou assíncrono
- **THEN** o núcleo responde 422 indicando o campo e nada é gravado

#### Scenario: O cadastro não recebe comunidade própria

- **WHEN** chega um cadastro de atividade avulsa declarando uma comunidade
- **THEN** o núcleo recusa o campo, e a comunidade da atividade é a da aula declarada

## ADDED Requirements

### Requirement: A leitura das atividades avulsas filtra por aula

O núcleo SHALL servir ao **Admin** a lista das atividades avulsas com filtro opcional pela
**aula**, para que a área Lançamentos da App 03 alcance as da aula vigente sem passar pela
programação do encontro. Sem o filtro, a lista SHALL seguir devolvendo todas as avulsas.
Persona que não é Admin SHALL receber **403**, como já vale para a leitura sem filtro.
(`RF-02-29`, `RF-02-112`)

#### Scenario: A lista traz só as avulsas da aula pedida

- **WHEN** um Admin lê as atividades avulsas filtrando por uma aula que tem duas delas
- **THEN** o núcleo devolve essas duas e nenhuma avulsa de outra aula

#### Scenario: Sem filtro, a lista traz todas

- **WHEN** um Admin lê as atividades avulsas sem declarar aula
- **THEN** o núcleo devolve todas as avulsas cadastradas

#### Scenario: Aula sem avulsa devolve lista vazia

- **WHEN** um Admin filtra por uma aula que não tem atividade avulsa alguma
- **THEN** o núcleo responde 200 com lista vazia, nunca erro

#### Scenario: Quem não é Admin não lê

- **WHEN** um Mestre em sessão lê a lista filtrando por aula
- **THEN** o núcleo responde 403 e nada é devolvido
