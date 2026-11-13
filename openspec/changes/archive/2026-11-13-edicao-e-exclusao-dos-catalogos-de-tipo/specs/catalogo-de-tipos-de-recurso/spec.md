## ADDED Requirements

### Requirement: O Admin altera o nome, a unidade e a marca de exige comprovante do tipo

O núcleo SHALL permitir ao **Admin** em sessão alterar, em tipo de recurso já cadastrado, o
**nome**, a **unidade** e a marca de **exige comprovante**, um, dois ou os três no mesmo ato.
A **natureza** NEVER SHALL ser alterada: ela decide se há valor de origem em reais a declarar, e
a alteração que a traga SHALL ser recusada com **422**. Nome ou unidade em branco SHALL ser
recusados com **422**, indicando o campo. Persona de qualquer outro papel SHALL receber **403**,
e tipo inexistente SHALL receber **404**. A escrita SHALL gravar autoria, data e hora com fuso.

A alteração NEVER SHALL mexer nas vigências do valor em moedas nem do preço em pontos extras, e
o que já foi gravado com o tipo — aporte, lançamento, reserva, recompensa, item avulso — SHALL
continuar apontando para ele, lido com o nome e a unidade atuais. A marca de exige comprovante
alterada SHALL valer para o aporte registrado **depois** da alteração, nunca para o já gravado.
(`RF-07-51`, `RF-07-01`, `RN-07-22`, `RF-01-03`, `RF-01-16`)

#### Scenario: Admin corrige o nome de um tipo

- **WHEN** um Admin em sessão altera o nome de um tipo de recurso
- **THEN** o núcleo grava o nome novo com o autor, a data e a hora com fuso, e a leitura do
  catálogo passa a trazê-lo

#### Scenario: A natureza não se altera

- **WHEN** um Admin tenta alterar a natureza de um tipo de recurso
- **THEN** o núcleo responde 422 e o tipo permanece como estava

#### Scenario: Unidade em branco é recusada

- **WHEN** um Admin tenta alterar a unidade de um tipo para texto em branco
- **THEN** o núcleo responde 422 indicando a unidade e nada é gravado

#### Scenario: Alterar não mexe nas vigências

- **WHEN** um Admin altera o nome de um tipo que tem valor em moedas e preço em pontos vigentes
- **THEN** as vigências permanecem exatamente como estavam

#### Scenario: Passar a exigir comprovante não alcança o aporte já gravado

- **WHEN** um Admin marca que um tipo passa a exigir comprovante e há aporte daquele tipo já
  gravado sem comprovante
- **THEN** o aporte gravado segue válido, e o aporte novo daquele tipo sem comprovante passa a ser
  recusado

#### Scenario: Mestre não altera tipo de recurso

- **WHEN** um Mestre em sessão tenta alterar um tipo de recurso
- **THEN** o núcleo responde 403 e o tipo permanece como estava

### Requirement: O Admin abre vigência nova do valor em moedas de tipo já cadastrado

O núcleo SHALL permitir ao **Admin** em sessão registrar **valor de referência em moedas novo**
para tipo de recurso já cadastrado, com **início de vigência**, pela mecânica de vigência já
definida neste catálogo: a vigente se encerra no dia de início da nova, e nenhuma vigência é
reescrita nem apagada. As recusas SHALL ser as do valor de referência — negativo ou com mais de
duas casas decimais, **422**; outro papel, **403** —, e tipo inexistente SHALL receber **404**.
(`RF-07-51`, `RF-07-02`, `RN-07-03`, `RN-07-04`)

#### Scenario: Admin abre vigência nova do valor

- **WHEN** um Admin em sessão registra valor novo para um tipo que já tinha valor vigente
- **THEN** a vigência anterior se encerra no dia de início da nova e permanece consultável com o
  valor que tinha

#### Scenario: Valor novo com três casas é recusado

- **WHEN** um Admin registra valor novo com três casas decimais
- **THEN** o núcleo responde 422 e a vigência anterior permanece aberta

### Requirement: O tipo de recurso tem marca de ativo, e o desativado só bloqueia escolha nova

O núcleo SHALL manter em cada tipo de recurso se ele está **ativo**; o tipo SHALL nascer ativo,
e todo tipo cadastrado antes desta marca SHALL ficar ativo. O **Admin** em sessão SHALL poder
**desativar** e **reativar** o tipo; persona de qualquer outro papel SHALL receber **403**, e
tipo inexistente SHALL receber **404**. Desativar tipo já desativado e reativar tipo já ativo
SHALL ser aceitos sem efeito.

Tipo desativado SHALL ser recusado com **422** em toda **escolha nova** de tipo de recurso:
agendar aula declarando o recurso, registrar aporte, homologar declaração de aporte, absorção sem
necessidade de origem, declarar recompensa de marco, cadastrar item do catálogo avulso e propor
desafio extra. A desativação NEVER SHALL alterar o que já existe
com o tipo — saldo, reserva, necessidade publicada, recompensa declarada, item avulso, desafio,
missão, lançamento —, e o ato que só **segue** um fato já existente — absorção de necessidade
publicada, missão do Apoiador sobre necessidade publicada, transferência de saldo, entrega de
recompensa declarada, troca de item já cadastrado — SHALL continuar aceito. O catálogo governa a escolha, não o que já foi declarado.
(`RF-07-52`, `RF-07-01`, `RF-01-16`)

#### Scenario: Admin desativa um tipo de recurso

- **WHEN** um Admin em sessão desativa um tipo de recurso
- **THEN** o núcleo grava o tipo como não ativo, com o autor, a data e a hora com fuso

#### Scenario: Agendar aula com tipo desativado é recusado

- **WHEN** um Admin agenda uma aula declarando recurso de um tipo desativado
- **THEN** o núcleo responde 422 e nenhuma aula é agendada

#### Scenario: Declarar recompensa com tipo desativado é recusado

- **WHEN** um Mestre autor declara recompensa de marco de um tipo desativado
- **THEN** o núcleo responde 422 e nenhuma recompensa é declarada

#### Scenario: Desativar não mexe no que já existe

- **WHEN** um Admin desativa um tipo que tem saldo em ponto de apoio e recompensa declarada
- **THEN** o saldo e a recompensa seguem inalterados, e a entrega daquela recompensa continua
  aceita

#### Scenario: A absorção da necessidade já publicada segue aceita

- **WHEN** um Mestre assume como absorção a necessidade publicada de um tipo que foi desativado
  depois da publicação
- **THEN** o núcleo aceita a absorção pelas regras de sempre

#### Scenario: Admin reativa o tipo

- **WHEN** um Admin em sessão reativa um tipo de recurso desativado
- **THEN** o tipo volta a ser aceito em escolha nova

#### Scenario: Mestre não desativa tipo de recurso

- **WHEN** um Mestre em sessão tenta desativar ou reativar um tipo de recurso
- **THEN** o núcleo responde 403 e o tipo permanece como estava

### Requirement: Só o tipo de recurso nunca usado é excluído

O núcleo SHALL permitir ao **Admin** em sessão **excluir** tipo de recurso **nunca usado** — sem
nenhum registro, de qualquer entidade, que aponte para ele além das suas próprias vigências de
valor e de preço, que saem com ele. Tipo **já usado** SHALL ser recusado com **422**, dizendo que
o tipo está em uso e que o caminho é desativá-lo, e nada SHALL ser apagado. Persona de qualquer
outro papel SHALL receber **403**, e tipo inexistente SHALL receber **404**. A exclusão NEVER
SHALL apagar nem reescrever lançamento do livro-razão. (`RN-07-40`, `RF-07-01`, `RF-01-16`)

#### Scenario: Admin exclui tipo cadastrado por engano

- **WHEN** um Admin em sessão exclui um tipo de recurso que nenhum registro usa
- **THEN** o tipo e as suas vigências deixam de existir, e o catálogo não o traz mais

#### Scenario: Tipo usado não é excluído

- **WHEN** um Admin tenta excluir um tipo de recurso que já tem aporte, reserva, recompensa ou
  item avulso
- **THEN** o núcleo responde 422 dizendo que o tipo está em uso e pode ser desativado, e nada é
  apagado

#### Scenario: Mestre não exclui tipo de recurso

- **WHEN** um Mestre em sessão tenta excluir um tipo de recurso
- **THEN** o núcleo responde 403 e o tipo permanece

## MODIFIED Requirements

### Requirement: A gestão lê o catálogo de tipos de recurso

O núcleo SHALL devolver os tipos de recurso cadastrados com **nome**, **natureza**,
**unidade**, se **exige comprovante**, se está **ativo** e o **valor em moedas vigente** na data
da consulta, ordenados por nome. A leitura SHALL exigir persona **Admin ou Mestre** em sessão — o
Admin porque cadastra, o Mestre porque escolhe entre os tipos ao assumir uma necessidade como
absorção e precisa saber a natureza do tipo, que decide se há valor de origem em reais a
declarar, e se o tipo exige comprovante. Persona de qualquer outro papel SHALL receber **403**.
A **escrita** do catálogo segue privativa do Admin. (`RF-07-01`, `RF-07-52`, `RF-01-16`,
`RF-09-56`, `RF-09-57`)

Tipo de recurso sem valor de referência vigente na data da consulta NEVER SHALL quebrar a
leitura dos demais: ele SHALL sair da listagem, e os outros SHALL vir normalmente. O tipo
**desativado** SHALL sair na listagem, assinalado como não ativo, para que a aplicação o leia
pelo nome e não o ofereça em escolha nova.

#### Scenario: Admin lê o catálogo com o valor vigente

- **WHEN** um Admin em sessão consulta os tipos de recurso
- **THEN** vêm todos os cadastrados, com nome, natureza, unidade, a marca de ativo e o valor em
  moedas da vigência corrente

#### Scenario: Mestre lê o catálogo para escolher o tipo que absorve

- **WHEN** um Mestre em sessão consulta os tipos de recurso
- **THEN** vêm os mesmos campos que o Admin lê, com a natureza e a marca de exige comprovante

#### Scenario: O tipo desativado sai assinalado

- **WHEN** o catálogo tem um tipo de recurso desativado com valor vigente e a leitura é
  consultada
- **THEN** o tipo aparece assinalado como não ativo

#### Scenario: Quem não é Admin não lê o catálogo

- **WHEN** um Apoiador em sessão consulta os tipos de recurso
- **THEN** o núcleo responde 403

#### Scenario: O Mestre não cadastra tipo de recurso

- **WHEN** um Mestre em sessão tenta cadastrar um tipo de recurso
- **THEN** o núcleo responde 403 e nada é gravado
