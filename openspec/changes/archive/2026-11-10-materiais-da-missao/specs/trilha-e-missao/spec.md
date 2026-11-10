## ADDED Requirements

### Requirement: A missão declara os materiais da aula, como lista de nomes

O núcleo SHALL aceitar, na **criação** (`POST /v1/trilhas/{id}/missoes`) e na **correção**
(`PATCH /v1/missoes/{id}`) da missão, o campo `materiais`: a lista dos **nomes** do que a aula da
missão pede, na ordem em que o Mestre os declarou. Cada nome SHALL ser gravado sem os espaços
das pontas; nome vazio ou só de espaços SHALL ser recusado com **422**, apontando o campo. A
lista é **opcional**: missão criada sem ela SHALL nascer com a lista **vazia**, e a correção que
manda lista vazia SHALL apagar os materiais declarados. Na correção, `materiais` ausente SHALL
conservar o gravado, e `materiais` nulo SHALL ser recusado com **422**, como os demais campos.

A correção dos materiais SHALL seguir a **autoria estrita** da correção da missão — o Admin
recebe **403** — e SHALL valer em **qualquer situação** da trilha, publicada inclusive. Os
materiais NEVER SHALL ser trava de publicação nem SHALL mudar a situação da trilha.
(`RF-09-140`, `RN-09-61`, `RN-09-56`, documento 11 §2.2)

A leitura da autoria (`GET /v1/trilhas/minhas`) e as respostas da criação e da correção SHALL
devolver `materiais`. A **duplicação** da trilha SHALL copiar os materiais de cada missão.
(`RF-09-140`, `RF-09-13`)

#### Scenario: Missão criada com materiais

- **WHEN** o Mestre autor cria uma missão com `materiais` igual a `[" cola ", "jumpers"]`
- **THEN** o núcleo grava `["cola", "jumpers"]` e os devolve na resposta

#### Scenario: Missão criada sem materiais

- **WHEN** o Mestre autor cria uma missão sem o campo `materiais`
- **THEN** a missão nasce com a lista vazia

#### Scenario: Nome vazio é recusado

- **WHEN** o Mestre autor manda `materiais` com um item só de espaços
- **THEN** o núcleo responde **422** apontando o campo `materiais`, e nada é gravado

#### Scenario: A correção substitui a lista

- **WHEN** o Mestre autor corrige uma missão de trilha publicada mandando só `materiais`
- **THEN** a lista gravada é substituída, os demais campos ficam como estavam e a trilha segue
  publicada

#### Scenario: Lista vazia apaga os materiais

- **WHEN** o Mestre autor corrige a missão com `materiais` igual a `[]`
- **THEN** a missão fica sem materiais

#### Scenario: Admin não corrige os materiais

- **WHEN** um Admin corrige os materiais de uma missão
- **THEN** o núcleo responde **403**

#### Scenario: Materiais não travam a publicação

- **WHEN** o Mestre autor publica trilha cujas missões não declaram materiais
- **THEN** a publicação confere só as travas que já existiam

#### Scenario: A duplicação copia os materiais

- **WHEN** um Mestre duplica uma trilha cuja missão declara `["papel", "cola"]`
- **THEN** a missão correspondente da cópia declara `["papel", "cola"]`
