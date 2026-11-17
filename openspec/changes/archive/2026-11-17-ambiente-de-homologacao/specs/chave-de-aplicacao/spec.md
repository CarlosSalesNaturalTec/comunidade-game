## MODIFIED Requirements

### Requirement: A implantação semeia a chave de cada aplicação do projeto, por ambiente

O núcleo SHALL emitir, na implantação, uma chave para cada aplicação do próprio projeto **em
cada ambiente**, marcada com natureza "do projeto" e **sem prazo de apresentação de URL**. São
oito aplicações e três ambientes — desenvolvimento, homologação e produção —, logo vinte e
quatro chaves. A unicidade de uma chave vigente por aplicação e ambiente SHALL valer **apenas
para as chaves de natureza do projeto**: ela existe para garantir estas vinte e quatro, e a
chave de terceiro se identifica pela solicitação que a originou. (`RF-01-54`, `RN-01-51`,
documento 03 §§1, 1.13)

#### Scenario: Cada aplicação do projeto recebe a sua chave no ambiente

- **WHEN** a implantação de um ambiente é executada
- **THEN** existe uma chave vigente por aplicação do projeto naquele ambiente, cada uma
  identificando qual aplicação é e a qual ambiente pertence

#### Scenario: Chave do projeto não tem prazo de apresentação

- **WHEN** uma chave de natureza "do projeto" é conferida a qualquer tempo depois da emissão
- **THEN** ela segue vigente, sem cobrança de URL apresentada e sem revogação por decurso de
  prazo

#### Scenario: Chave de um ambiente não abre o outro

- **WHEN** uma chave semeada no ambiente de desenvolvimento é apresentada ao núcleo de produção
- **THEN** o núcleo de produção responde 401, como faria com uma chave desconhecida

#### Scenario: Chave de homologação não abre produção, nem a de produção abre homologação

- **WHEN** uma chave semeada no ambiente de homologação é apresentada ao núcleo de produção, ou
  uma de produção ao núcleo de homologação
- **THEN** o núcleo que a recebe responde 401, como faria com uma chave desconhecida

#### Scenario: Semear duas vezes não duplica a chave

- **WHEN** a implantação do mesmo ambiente é executada de novo
- **THEN** as chaves já vigentes daquele ambiente permanecem as mesmas, sem duplicata e sem
  invalidar as que as aplicações já carregam

#### Scenario: A unicidade não alcança a chave de terceiro

- **WHEN** duas chaves de terceiro vigentes existem no ambiente de produção declarando o mesmo
  nome de aplicação
- **THEN** o núcleo as mantém as duas, porque a unicidade por aplicação e ambiente vale só
  para as chaves do projeto
