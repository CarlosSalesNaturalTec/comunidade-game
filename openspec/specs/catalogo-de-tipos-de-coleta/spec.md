## Purpose

O catálogo do que se mede no território — a forma de registro, a unidade e a faixa esperada de
cada tipo —, cadastrado por Admin. É o vocabulário entre o qual o Mestre escolhe ao criar o
desafio de coleta, e a origem da faixa contra a qual a medição estranha será marcada para
auditoria.

## Requirements

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

### Requirement: O catálogo é legível por quem escolhe entre os tipos

O núcleo SHALL expor o catálogo de tipos de coleta em **leitura**, para a persona autenticada
que escreve o desafio de coleta — o **Mestre** — e para o **Admin** que o cadastra. Sem essa
leitura o Mestre não tem entre o que escolher, e `RF-09-27` não se cumpre: o catálogo é o
vocabulário do desafio, e o Mestre NEVER SHALL criar tipo novo ao escrever o desafio.
(`RF-09-27`, `RF-08-05`, `RF-08-06`, `RF-01-28`, PRD-08 §4)

Cada tipo SHALL sair com o **nome**, a **forma de registro**, a **unidade** e a **faixa
esperada** quando houver, e a indicação de estar **ativo** — para que a aplicação nunca ofereça
um tipo desativado, que o núcleo recusaria na criação do desafio. A leitura SHALL ser paginada
como toda listagem do núcleo.

A leitura NEVER SHALL criar, alterar nem desativar tipo: o cadastro segue privativo do Admin.
Persona de papel que não escreve desafio nem cadastra tipo — Guerreiro(a), responsável e
Apoiador — SHALL receber **403**.

#### Scenario: O Mestre lê o catálogo para escolher o tipo

- **WHEN** um Mestre em sessão consulta o catálogo de tipos de coleta
- **THEN** o núcleo devolve os tipos cadastrados, cada um com nome, forma de registro, unidade
  e faixa esperada quando houver, e a indicação de estar ativo

#### Scenario: O tipo por evidência sai sem unidade e sem faixa

- **WHEN** a leitura devolve um tipo cuja forma de registro é `foto` ou `vídeo`
- **THEN** ele sai sem unidade e sem faixa esperada, porque não produz valor a comparar

#### Scenario: O tipo desativado sai assinalado

- **WHEN** o catálogo tem um tipo desativado e a leitura é consultada
- **THEN** o tipo aparece assinalado como não ativo, para que a aplicação não o ofereça

#### Scenario: O Admin lê o mesmo catálogo

- **WHEN** um Admin em sessão consulta o catálogo de tipos de coleta
- **THEN** o núcleo devolve a mesma listagem

#### Scenario: A leitura não altera o catálogo

- **WHEN** o catálogo é consultado
- **THEN** nenhum tipo é criado, alterado ou desativado por essa consulta

#### Scenario: Papel que não escolhe nem cadastra é recusado

- **WHEN** um Guerreiro(a), um responsável ou um Apoiador consulta o catálogo de tipos de coleta
- **THEN** o núcleo responde 403

### Requirement: O Admin altera todos os campos do tipo de coleta

O núcleo SHALL permitir ao **Admin** em sessão alterar, em tipo de coleta já cadastrado,
**qualquer** dos seus campos — **nome**, **forma de registro**, **unidade** e **faixa esperada**
—, um ou mais no mesmo ato. O tipo resultante SHALL passar pelas **mesmas validações do
cadastro**: nome em branco, forma fora de número, foto e vídeo, tipo por número sem unidade ou
sem faixa, faixa com mínimo maior que o máximo e tipo por evidência com unidade ou faixa SHALL ser
recusados com **422**, e nada SHALL ser gravado. Trocar a forma para **foto** ou **vídeo** SHALL
exigir que a unidade e a faixa saiam no mesmo ato; trocar para **número** SHALL exigir que
entrem. Persona de qualquer outro papel SHALL receber **403**, e tipo inexistente SHALL receber
**404**. A escrita SHALL gravar autoria, data e hora com fuso.

A alteração NEVER SHALL reescrever **registro de coleta já gravado**: ele guarda o que foi
registrado sob a forma que valia. O desafio que já escolheu o tipo SHALL seguir apontando para
ele, e o **registro novo** desse desafio SHALL ser conferido pela forma, unidade e faixa
**atuais** do tipo. (`RF-08-32`, `RF-08-05`, `RF-08-12`, `RF-08-21`, `RF-01-03`, `RF-01-16`)

#### Scenario: Admin corrige a faixa esperada

- **WHEN** um Admin em sessão altera a faixa esperada de um tipo por número de -10 a 55 para
  -5 a 50
- **THEN** o núcleo grava a faixa nova com o autor, a data e a hora com fuso

#### Scenario: Admin troca a forma de número para foto

- **WHEN** um Admin altera a forma de registro de um tipo por número para foto, retirando no
  mesmo ato a unidade e a faixa
- **THEN** o núcleo grava o tipo como foto, sem unidade e sem faixa

#### Scenario: Trocar para número sem faixa é recusado

- **WHEN** um Admin altera a forma de registro de um tipo por foto para número sem informar a
  faixa esperada
- **THEN** o núcleo responde 422 e o tipo permanece como estava

#### Scenario: O registro já gravado não muda com a forma

- **WHEN** um Admin altera a forma de registro de um tipo que já tem registros de coleta gravados
- **THEN** os registros gravados permanecem exatamente como foram registrados, e o registro novo
  do mesmo desafio passa a ser conferido pela forma nova

#### Scenario: Mestre não altera tipo de coleta

- **WHEN** um Mestre em sessão tenta alterar um tipo de coleta
- **THEN** o núcleo responde 403 e o tipo permanece como estava

### Requirement: O Admin desativa e reativa o tipo de coleta

O núcleo SHALL permitir ao **Admin** em sessão **desativar** e **reativar** tipo de coleta. O
tipo reativado SHALL voltar a ser aceito em desafio novo. Desativar tipo já desativado e reativar
tipo já ativo SHALL ser aceitos sem efeito. Persona de qualquer outro papel SHALL receber **403**,
e tipo inexistente SHALL receber **404**. A escrita SHALL gravar autoria, data e hora com fuso.
(`RF-08-32`, `RF-08-05`, `RF-08-06`)

#### Scenario: Admin desativa o tipo de coleta

- **WHEN** um Admin em sessão desativa um tipo de coleta ativo
- **THEN** o núcleo grava o tipo como não ativo, e o desafio novo que o escolher passa a ser
  recusado

#### Scenario: Admin reativa o tipo de coleta

- **WHEN** um Admin em sessão reativa um tipo de coleta desativado
- **THEN** o tipo volta a ser aceito em desafio novo

### Requirement: Só o tipo de coleta nunca usado é excluído

O núcleo SHALL permitir ao **Admin** em sessão **excluir** tipo de coleta **nunca usado** — que
nenhum desafio de coleta escolheu. Tipo **já usado** SHALL ser recusado com **422**, dizendo que
o tipo está em uso e que o caminho é desativá-lo, e nada SHALL ser apagado. Persona de qualquer
outro papel SHALL receber **403**, e tipo inexistente SHALL receber **404**. (`RN-08-30`,
`RF-08-05`)

#### Scenario: Admin exclui tipo cadastrado por engano

- **WHEN** um Admin em sessão exclui um tipo de coleta que nenhum desafio escolheu
- **THEN** o tipo deixa de existir, e o catálogo não o traz mais

#### Scenario: Tipo escolhido por desafio não é excluído

- **WHEN** um Admin tenta excluir um tipo de coleta que um desafio já escolheu
- **THEN** o núcleo responde 422 dizendo que o tipo está em uso e pode ser desativado, e nada é
  apagado

#### Scenario: Mestre não exclui tipo de coleta

- **WHEN** um Mestre em sessão tenta excluir um tipo de coleta
- **THEN** o núcleo responde 403 e o tipo permanece
