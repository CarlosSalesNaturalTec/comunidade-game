## MODIFIED Requirements

### Requirement: O catálogo de tipos de recurso é cadastrado por Admin

O núcleo SHALL manter o catálogo de **tipos de recurso** com **nome**, **natureza** — consumível,
durável, serviço ou financeiro —, **unidade** e a marca de **exige comprovante**. Cadastrar tipo
de recurso SHALL exigir persona **Admin** em sessão; persona de qualquer outro papel SHALL
receber **403**. Cadastro sem nome, sem natureza ou sem unidade SHALL ser recusado com **422**,
indicando o campo em falta, e natureza fora das quatro previstas SHALL ser recusada com **422**.
A marca de **exige comprovante** SHALL ser opcional no cadastro e SHALL nascer **falsa** quando
não declarada; quando verdadeira, o aporte daquele tipo sem comprovante SHALL ser recusado. O
cadastro SHALL ser operação **avulsa**, que não depende de nenhum outro fluxo em andamento. A
escrita SHALL gravar autoria, data e hora com fuso. (`RF-07-01`, `RF-07-03`, `RN-07-22`,
`RF-01-16`, `RF-01-03`, `RF-01-27`, PRD-07 §8)

#### Scenario: Admin cadastra um tipo de recurso

- **WHEN** um Admin em sessão cadastra um tipo de recurso com nome, natureza e unidade
- **THEN** o núcleo grava o tipo no catálogo com o autor, a data e a hora com fuso

#### Scenario: Mestre não cadastra tipo de recurso

- **WHEN** um Mestre em sessão tenta cadastrar um tipo de recurso
- **THEN** o núcleo responde 403 e o catálogo permanece como estava

#### Scenario: Tipo sem unidade é recusado

- **WHEN** chega um cadastro de tipo de recurso sem unidade
- **THEN** o núcleo responde 422 indicando o campo em falta e nada é gravado

#### Scenario: Natureza fora das quatro previstas é recusada

- **WHEN** chega um cadastro de tipo de recurso com natureza que não é consumível, durável,
  serviço nem financeiro
- **THEN** o núcleo responde 422 e nada é gravado

#### Scenario: Tipo nasce sem exigir comprovante

- **WHEN** um Admin cadastra um tipo de recurso sem declarar a marca de exige comprovante
- **THEN** o núcleo grava o tipo com a marca falsa

#### Scenario: Tipo cadastrado exigindo comprovante

- **WHEN** um Admin cadastra um tipo de recurso declarando que ele exige comprovante
- **THEN** o núcleo grava o tipo com a marca verdadeira, e o aporte daquele tipo sem comprovante
  passa a ser recusado
