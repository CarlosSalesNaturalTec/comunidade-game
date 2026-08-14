## ADDED Requirements

### Requirement: O papel do poder é declarado no catálogo, nunca deduzido do nome

O núcleo SHALL registrar, em cada poder do catálogo, o **papel** que ele exerce nas regras da
plataforma, declarado por Admin ao lado da natureza e da vigência. O papel **do Território**
SHALL identificar o poder a que a coleta de dados credita, e o núcleo NEVER SHALL deduzir esse
papel do **nome** do poder — o nome é rótulo de exibição, alterável por Admin, e não identifica
regra. Entre os poderes do catálogo SHALL haver **no máximo um** com o papel do Território; a
tentativa de marcar um segundo SHALL ser recusada com **409**. Poder sem papel declarado SHALL
ser aceito: o papel é opcional, e a maioria dos poderes não exerce nenhum. (`RN-01-54`,
`RF-01-62`, `RN-08-15`, 02 §2)

#### Scenario: Admin marca o poder do Território

- **WHEN** um Admin em sessão cadastra o Poder do Território declarando o papel do Território
- **THEN** o núcleo grava o poder com o papel declarado, e o crédito da coleta passa a
  encontrá-lo

#### Scenario: Segundo poder com o papel do Território é recusado

- **WHEN** um Admin tenta declarar o papel do Território num segundo poder do catálogo
- **THEN** o núcleo responde 409 e o papel do primeiro permanece como estava

#### Scenario: Poder sem papel é aceito

- **WHEN** um Admin cadastra um poder sem declarar papel algum
- **THEN** o núcleo grava o poder normalmente

#### Scenario: O nome não identifica o papel

- **WHEN** existe no catálogo um poder chamado "Poder do Território" sem o papel declarado, e
  outro com o papel do Território declarado sob nome diverso
- **THEN** o crédito da coleta recai sobre o que tem o papel declarado

#### Scenario: Renomear o poder não muda o papel

- **WHEN** um Admin altera o nome do poder que exerce o papel do Território
- **THEN** o papel permanece com ele e o crédito da coleta segue chegando ao mesmo poder

### Requirement: A coleta sem poder do Território declarado é recusada

O núcleo SHALL recusar com **409** a gravação de registro de coleta quando **nenhum** poder do
catálogo exercer o papel do Território, e SHALL informar em linguagem simples que o catálogo
precisa desse poder. O núcleo NEVER SHALL gravar registro sem creditar, nem creditar a um poder
escolhido por aproximação de nome. (`RN-01-54`, `RN-08-15`, `RF-08-09`)

#### Scenario: Registro sem poder do Território no catálogo é recusado

- **WHEN** um Guerreiro(a) grava medição e nenhum poder do catálogo exerce o papel do Território
- **THEN** o núcleo responde 409, nada é gravado e nenhum ponto é creditado
