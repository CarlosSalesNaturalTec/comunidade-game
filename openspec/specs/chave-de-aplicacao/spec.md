# chave-de-aplicacao Specification

## Purpose
A chave de aplicação é o porteiro do Backend API: identifica **a aplicação** que faz a chamada,
nunca a pessoa, e sem ela nenhuma rota de dados responde — nem as de consulta pública. Esta
capacidade cobre a conferência da chave em toda chamada, a recusa que não entrega informação a
quem tenta adivinhar, e as chaves das oito aplicações do próprio projeto, semeadas na
implantação em cada ambiente.
## Requirements
### Requirement: Chave válida é condição de toda rota de dados

O núcleo SHALL exigir chave de aplicação válida em toda chamada a rota de dados sob o prefixo
de versão, inclusive nas rotas de consulta pública. Chamada sem chave, com chave desconhecida
ou com chave cuja situação não seja vigente SHALL ser recusada com 401. (`RF-01-48`,
`RN-01-32`)

#### Scenario: Chamada com chave vigente é processada

- **WHEN** uma aplicação chama uma rota de dados apresentando uma chave vigente
- **THEN** o núcleo processa a chamada segundo as demais regras da rota

#### Scenario: Chamada sem chave é recusada

- **WHEN** uma aplicação chama uma rota de dados sem apresentar chave
- **THEN** o núcleo responde 401 e não executa nada da rota

#### Scenario: Consulta pública também exige a chave

- **WHEN** uma chamada a uma rota de consulta pública chega sem chave
- **THEN** o núcleo responde 401, mesmo a rota não exigindo credencial de persona

#### Scenario: Chave revogada perde o acesso na chamada seguinte

- **WHEN** uma aplicação apresenta uma chave cuja situação passou a revogada
- **THEN** o núcleo responde 401 na chamada seguinte à revogação, sem período de tolerância

### Requirement: A recusa não diferencia os motivos

O núcleo SHALL responder chave ausente, chave inválida e chave revogada com a **mesma** resposta
401, sem indicar no código, na mensagem ou no tempo de resposta qual dos três ocorreu. (PRD-01
§9 e §12)

#### Scenario: Os três motivos produzem a mesma resposta

- **WHEN** três chamadas chegam à mesma rota, uma sem chave, uma com chave inexistente e uma
  com chave revogada
- **THEN** as três recebem 401 com corpo idêntico, e nenhuma revela qual foi o motivo

#### Scenario: Recusa não confirma a existência de uma chave

- **WHEN** alguém tenta descobrir uma chave válida por tentativa e erro
- **THEN** nenhuma resposta do núcleo distingue "essa chave não existe" de "essa chave existe e
  foi revogada"

### Requirement: Rota pública dispensa credencial de persona, nunca a chave

O núcleo SHALL distinguir rota **pública** de rota **autenticada**. Pública significa que a
rota dispensa a credencial da persona; ela NEVER dispensa a chave de aplicação. Rota
autenticada SHALL exigir chave e credencial de persona. (`RF-01-02`, `RN-01-34`)

#### Scenario: Rota pública responde sem credencial de persona

- **WHEN** uma chamada a uma rota pública chega com chave vigente e sem credencial de persona
- **THEN** o núcleo processa a chamada e o chamador segue anônimo

#### Scenario: Rota autenticada exige as duas coisas

- **WHEN** uma chamada a uma rota autenticada chega com chave vigente e sem credencial de
  persona
- **THEN** o núcleo recusa a chamada, e a recusa não é a mesma da chave ausente

### Requirement: A chave é da aplicação e não amplia direito

O núcleo SHALL tratar a chave como identificação **da aplicação**, nunca da pessoa. A chave
NEVER identifica um visitante, NEVER autoriza escrita e NEVER concede a uma aplicação direito
que ela não teria: quem só lê continua só lendo, e escrita segue exigindo credencial de
persona. (`RN-01-33`, `RN-01-34`)

#### Scenario: Chave não vira identidade de visitante

- **WHEN** uma chamada a uma rota pública é processada mediante chave
- **THEN** o núcleo não atribui persona alguma ao chamador e não registra o visitante

#### Scenario: Chave não abre escrita

- **WHEN** uma aplicação apresenta chave vigente e tenta uma rota de escrita sem credencial de
  persona
- **THEN** o núcleo recusa a escrita, qualquer que seja a natureza da chave

### Requirement: A implantação semeia a chave de cada aplicação do projeto, por ambiente

O núcleo SHALL emitir, na implantação, uma chave para cada aplicação do próprio projeto **em
cada ambiente**, marcada com natureza "do projeto" e **sem prazo de apresentação de URL**. São
oito aplicações e dois ambientes — desenvolvimento e produção —, logo dezesseis chaves.
(`RF-01-54`, documento 03 §§1, 1.13)

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

#### Scenario: Semear duas vezes não duplica a chave

- **WHEN** a implantação do mesmo ambiente é executada de novo
- **THEN** as chaves já vigentes daquele ambiente permanecem as mesmas, sem duplicata e sem
  invalidar as que as aplicações já carregam

### Requirement: O segredo é devolvido uma única vez e nunca recuperável

O núcleo SHALL guardar apenas o **resumo criptográfico** do segredo da chave. O segredo em
claro SHALL ser apresentado uma única vez, no momento da emissão, e NEVER SHALL ser recuperável
depois — por rota, por consulta ou por leitura da base. (`RN-01-35`)

#### Scenario: Base guarda só o resumo

- **WHEN** uma chave é emitida
- **THEN** o registro da chave contém o resumo criptográfico do segredo, e o segredo em claro
  não é gravado em lugar nenhum

#### Scenario: Segunda leitura não recupera o segredo

- **WHEN** alguém consulta uma chave já emitida
- **THEN** a resposta traz os dados da chave e nunca o segredo, mesmo para um Admin

#### Scenario: Segredo não aparece em registro operacional

- **WHEN** uma chamada com chave é processada, aceita ou recusada
- **THEN** nenhum registro operacional do núcleo contém o segredo em claro

