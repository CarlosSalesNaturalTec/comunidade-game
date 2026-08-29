## MODIFIED Requirements

### Requirement: A gestão lê o catálogo de tipos de recurso

O núcleo SHALL devolver os tipos de recurso cadastrados com **nome**, **natureza**,
**unidade**, se **exige comprovante** e o **valor em moedas vigente** na data da consulta,
ordenados por nome. A leitura SHALL exigir persona **Admin ou Mestre** em sessão — o Admin
porque cadastra, o Mestre porque escolhe entre os tipos ao assumir uma necessidade como
absorção e precisa saber a natureza do tipo, que decide se há valor de origem em reais a
declarar, e se o tipo exige comprovante. Persona de qualquer outro papel SHALL receber **403**.
A **escrita** do catálogo segue privativa do Admin. (`RF-07-01`, `RF-01-16`, `RF-09-56`,
`RF-09-57`)

Tipo de recurso sem valor de referência vigente na data da consulta NEVER SHALL quebrar a
leitura dos demais: ele SHALL sair da listagem, e os outros SHALL vir normalmente.

#### Scenario: Admin lê o catálogo com o valor vigente

- **WHEN** um Admin em sessão consulta os tipos de recurso
- **THEN** vêm todos os cadastrados, com nome, natureza, unidade e o valor em moedas da
  vigência corrente

#### Scenario: Mestre lê o catálogo para escolher o tipo que absorve

- **WHEN** um Mestre em sessão consulta os tipos de recurso
- **THEN** vêm os mesmos campos que o Admin lê, com a natureza e a marca de exige comprovante

#### Scenario: Quem não é Admin não lê o catálogo

- **WHEN** um Apoiador em sessão consulta os tipos de recurso
- **THEN** o núcleo responde 403

#### Scenario: O Mestre não cadastra tipo de recurso

- **WHEN** um Mestre em sessão tenta cadastrar um tipo de recurso
- **THEN** o núcleo responde 403 e nada é gravado
