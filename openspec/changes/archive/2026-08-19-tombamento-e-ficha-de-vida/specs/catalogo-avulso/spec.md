## MODIFIED Requirements

### Requirement: O item do catálogo avulso é cadastrado por Mestre ou por Apoiador

O núcleo SHALL manter o **item do catálogo avulso** com **nome**, **tipo de recurso**,
**estoque** declarado, **comunidade**, **ponto de apoio** e a **origem do cadastro**. O ponto de
apoio declarado SHALL pertencer à comunidade do item; ponto de apoio de outra comunidade SHALL
ser recusado com **422**. O tipo de recurso declarado NÃO SHALL ser de natureza **durável**:
o saldo durável é patrimônio e nunca lastreia recompensa, de modo que o item jamais poderia
ativar; o cadastro que o declare SHALL ser recusado com **422**, indicando o tipo. Essa recusa
convive com a regra do lastro sem contradizê-la: o item **sem lastro** nasce inativo e nunca é
recusado, porque o lastro ainda pode chegar; o item de tipo durável é recusado porque a
impossibilidade é estrutural. Cadastrar item SHALL exigir persona **Mestre** ou **Apoiador** em
sessão; **Admin**, **Guerreiro(a)** e **responsável** SHALL receber **403**. O Mestre SHALL só
cadastrar item em comunidade a que está vinculado. Cadastro sem nome, sem tipo de recurso, sem
estoque, sem comunidade ou sem ponto de apoio SHALL ser recusado com **422**, indicando o campo
em falta, e estoque menor que 1 SHALL ser recusado com **422**. A escrita SHALL gravar autoria,
data e hora com fuso. (`RF-07-33`, `RF-07-34`, `RN-07-07`, `RN-07-26`, `RF-09-99`, `RF-14-77`,
`RN-07-33`, `RF-01-16`, `RF-01-03`, `RF-01-27`, PRD-07 §8)

#### Scenario: Mestre cadastra item na sua comunidade

- **WHEN** um Mestre em sessão cadastra um item com nome, tipo de recurso, estoque, comunidade a
  que está vinculado e ponto de apoio dela
- **THEN** o núcleo grava o item com a origem de cadastro Mestre, o autor, a data e a hora com
  fuso

#### Scenario: Apoiador oferta item ao catálogo

- **WHEN** um Apoiador em sessão cadastra um item com nome, tipo de recurso, estoque, comunidade
  e ponto de apoio
- **THEN** o núcleo grava o item com a origem de cadastro Apoiador

#### Scenario: Ponto de apoio de outra comunidade é recusado

- **WHEN** chega um cadastro de item cujo ponto de apoio pertence a comunidade diferente da
  declarada no item
- **THEN** o núcleo responde 422 e nada é gravado

#### Scenario: Item de tipo durável é recusado no cadastro

- **WHEN** um Mestre em sessão cadastra um item cujo tipo de recurso é de natureza durável
- **THEN** o núcleo responde 422 indicando o tipo e nada é gravado

#### Scenario: Item de tipo consumível sem lastro segue aceito e inativo

- **WHEN** chega um cadastro de item de tipo consumível cujo ponto de apoio não tem saldo algum
  daquele tipo
- **THEN** o núcleo grava o item e ele nasce inativo, sem ser recusado

#### Scenario: Mestre não cadastra item em comunidade a que não está vinculado

- **WHEN** um Mestre em sessão tenta cadastrar item em comunidade a que não está vinculado
- **THEN** o núcleo responde 403 e nada é gravado

#### Scenario: Guerreiro(a) não cadastra item

- **WHEN** um Guerreiro(a) em sessão tenta cadastrar item do catálogo avulso
- **THEN** o núcleo responde 403 e nada é gravado

#### Scenario: Estoque menor que um é recusado

- **WHEN** chega um cadastro de item com estoque zero ou negativo
- **THEN** o núcleo responde 422 e nada é gravado
