## ADDED Requirements

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
