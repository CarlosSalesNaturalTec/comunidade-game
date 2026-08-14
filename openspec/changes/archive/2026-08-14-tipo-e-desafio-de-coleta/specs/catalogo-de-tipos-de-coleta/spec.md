## Purpose

O catálogo do que se mede no território — a forma de registro, a unidade e a faixa esperada de
cada tipo —, cadastrado por Admin. É o vocabulário entre o qual o Mestre escolhe ao criar o
desafio de coleta, e a origem da faixa contra a qual a medição estranha será marcada para
auditoria.

## ADDED Requirements

### Requirement: O catálogo de tipos de coleta é cadastrado por Admin

O núcleo SHALL manter o catálogo de tipos de coleta a que o desafio se vincula. Cadastrar,
alterar e desativar tipo de coleta SHALL exigir persona **Admin** em sessão; persona de qualquer
outro papel SHALL receber **403**, inclusive o Mestre, que **escolhe** entre os tipos cadastrados
e NEVER SHALL criar tipo novo ao escrever o desafio. Toda escrita SHALL gravar autoria, data e
hora, como já vale para as demais escritas do núcleo. (`RF-08-05`, `RF-01-03`, `RF-01-16`,
PRD-08 §4)

#### Scenario: Admin cadastra um tipo de coleta

- **WHEN** um Admin em sessão cadastra um tipo de coleta com nome e forma de registro
- **THEN** o núcleo grava o tipo no catálogo com o autor, a data e a hora com fuso

#### Scenario: Mestre não cadastra tipo de coleta

- **WHEN** um Mestre em sessão tenta cadastrar, alterar ou desativar um tipo de coleta
- **THEN** o núcleo responde 403 e o catálogo permanece como estava

#### Scenario: Tipo sem nome é recusado

- **WHEN** um Admin tenta cadastrar um tipo de coleta sem nome
- **THEN** o núcleo responde 422 indicando o campo em falta e nada é gravado

### Requirement: O tipo declara a forma de registro entre número, foto e vídeo

O núcleo SHALL registrar, em cada tipo do catálogo, a **forma de registro**, que SHALL ser uma
entre **número**, **foto** e **vídeo** — é ela que define se aquele tipo se mede por valor ou por
evidência. Forma de registro fora dessas três SHALL ser recusada com **422**. (`RF-08-05`,
`RF-08-21`, PRD-08 §8, 02 §1)

#### Scenario: Tipo que se mede por número

- **WHEN** um Admin cadastra um tipo de coleta com forma de registro `número`
- **THEN** o núcleo grava o tipo, e o desafio que o escolher exigirá valor numérico do registro

#### Scenario: Tipo que se mede por evidência

- **WHEN** um Admin cadastra um tipo de coleta com forma de registro `foto` ou `vídeo`
- **THEN** o núcleo grava o tipo, e a mídia será o próprio registro daquele desafio

#### Scenario: Forma de registro fora da lista é recusada

- **WHEN** chega um tipo de coleta com forma de registro que não é número, foto nem vídeo
- **THEN** o núcleo responde 422 e nada é gravado

### Requirement: Unidade e faixa esperada acompanham o tipo que se mede por número

O núcleo SHALL exigir **unidade de medida** e **faixa esperada** — mínimo e máximo — do tipo cuja
forma de registro é **número**, e SHALL dispensá-las do tipo cuja forma é **foto** ou **vídeo**,
que não produz valor a comparar. Tipo de forma `número` sem unidade ou sem faixa esperada SHALL
ser recusado com **422**; faixa cujo mínimo é maior que o máximo SHALL ser recusada com **422**.
(`RF-08-05`, `RF-08-12`, PRD-08 §8)

#### Scenario: Tipo por número exige unidade e faixa

- **WHEN** um Admin cadastra um tipo de forma `número` com unidade "°C" e faixa de -10 a 55
- **THEN** o núcleo grava o tipo com a unidade e a faixa

#### Scenario: Tipo por número sem faixa é recusado

- **WHEN** um Admin tenta cadastrar um tipo de forma `número` sem faixa esperada
- **THEN** o núcleo responde 422 e nada é gravado

#### Scenario: Tipo por evidência dispensa unidade e faixa

- **WHEN** um Admin cadastra um tipo de forma `foto` sem unidade e sem faixa esperada
- **THEN** o núcleo grava o tipo

#### Scenario: Faixa invertida é recusada

- **WHEN** chega um tipo de forma `número` cuja faixa tem mínimo maior que o máximo
- **THEN** o núcleo responde 422 e nada é gravado

### Requirement: Só tipo ativo é escolhido por desafio novo

O núcleo SHALL manter em cada tipo do catálogo se ele está **ativo**, e SHALL recusar com **422**
o desafio de coleta que escolher um tipo desativado. A desativação NEVER SHALL alterar os
desafios já criados com aquele tipo: o catálogo governa a escolha, não o que já foi declarado.
(`RF-08-05`, `RF-08-06`, PRD-08 §9)

#### Scenario: Desafio escolhe tipo ativo

- **WHEN** o Mestre cria um desafio escolhendo um tipo ativo do catálogo
- **THEN** o núcleo aceita a escolha

#### Scenario: Desafio que escolhe tipo desativado é recusado

- **WHEN** o Mestre cria um desafio escolhendo um tipo desativado
- **THEN** o núcleo responde 422 e nenhum desafio é criado

#### Scenario: Desativar tipo não mexe no desafio já criado

- **WHEN** um Admin desativa um tipo de coleta que já foi escolhido por um desafio
- **THEN** o desafio segue com aquele tipo, inalterado
