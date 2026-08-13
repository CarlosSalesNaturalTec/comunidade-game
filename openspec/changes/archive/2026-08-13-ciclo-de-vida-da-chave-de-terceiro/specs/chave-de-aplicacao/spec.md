## ADDED Requirements

### Requirement: A chave de terceiro nasce de solicitação aprovada, por ato de Admin

O núcleo SHALL emitir chave de natureza **de terceiro** apenas por ato de Admin sobre uma
solicitação de chave já **aprovada** na fila de avaliação. O núcleo SHALL recusar a emissão
sobre solicitação em outra situação, e cada solicitação aprovada SHALL render **uma única**
chave. A emissão SHALL devolver o **identificador** da chave e o **segredo**, este uma única
vez, na forma que a capacidade já exige — são os dois dados que o Admin entrega ao
solicitante, e é o identificador que ele apresenta ao registrar a URL. (`RF-01-50`,
`RN-01-35`, `RN-01-51`, `RF-02-89`)

#### Scenario: Solicitação aprovada rende a chave

- **WHEN** um Admin emite a chave de uma solicitação aprovada
- **THEN** o núcleo cria a chave de natureza de terceiro, vincula-a à solicitação e devolve o
  identificador e o segredo, este uma única vez

#### Scenario: Solicitação não aprovada não rende chave

- **WHEN** um Admin tenta emitir a chave de uma solicitação recebida, em avaliação ou recusada
- **THEN** o núcleo recusa a emissão e nenhuma chave é criada

#### Scenario: A mesma solicitação não rende duas chaves

- **WHEN** um Admin tenta emitir a chave de uma solicitação que já rendeu a sua
- **THEN** o núcleo recusa a emissão, e a chave existente permanece como está

#### Scenario: Quem não é Admin não emite

- **WHEN** uma persona que não é Admin chama a emissão
- **THEN** o núcleo recusa por falta de permissão do papel, e nenhuma chave é criada

### Requirement: A chave de terceiro é de produção e se identifica pela solicitação

O núcleo SHALL emitir toda chave de terceiro no ambiente de **produção** — desenvolvimento é
ambiente das aplicações do projeto. A identidade da chave de terceiro SHALL ser a solicitação
que a originou, e NEVER o nome da aplicação declarada, que dois solicitantes podem repetir.
A unicidade por aplicação e ambiente SHALL alcançar apenas as chaves de natureza **do
projeto**. (`RN-01-51`, `RF-01-54`)

#### Scenario: Dois terceiros declaram o mesmo nome

- **WHEN** duas solicitações aprovadas declaram aplicações de nome idêntico e ambas rendem
  chave
- **THEN** o núcleo emite as duas chaves, cada uma presa à sua solicitação, sem recusar a
  segunda por colisão de nome

#### Scenario: Terceiro não recebe chave de desenvolvimento

- **WHEN** a chave de uma solicitação aprovada é emitida
- **THEN** ela pertence ao ambiente de produção, qualquer que seja o ambiente em que o Admin
  operou

#### Scenario: A unicidade do projeto continua valendo

- **WHEN** a implantação semeia as chaves das aplicações do projeto
- **THEN** segue existindo uma única chave vigente por aplicação do projeto em cada ambiente

### Requirement: O prazo de apresentação corre da emissão e se cumpre com a URL

O núcleo SHALL gravar, na emissão da chave de terceiro, o **prazo de apresentação** contado da
data de emissão, e SHALL registrar a **URL apresentada** com data e hora. Apresentada a URL
dentro do prazo, a chave SHALL permanecer vigente por prazo indeterminado. Apresentação depois
de vencido o prazo SHALL ser recusada, com a orientação de solicitar nova chave. Apresentada
uma vez, nova apresentação para a mesma chave SHALL ser recusada. A chave de natureza do
projeto NEVER SHALL ter prazo de apresentação. (`RF-01-51`, `RN-01-36`, PRD-01 §§9, 12)

#### Scenario: URL apresentada dentro do prazo mantém a chave

- **WHEN** o solicitante apresenta a URL antes de vencido o prazo
- **THEN** o núcleo registra a URL com data e hora, e a chave segue vigente sem novo prazo

#### Scenario: URL apresentada depois do prazo é recusada

- **WHEN** o solicitante apresenta a URL depois de vencido o prazo
- **THEN** o núcleo recusa a apresentação e orienta a solicitar nova chave

#### Scenario: Segunda apresentação é recusada

- **WHEN** o solicitante apresenta URL para uma chave que já tem URL registrada
- **THEN** o núcleo recusa, e a URL registrada permanece a primeira

#### Scenario: Apresentar URL não é ato de persona

- **WHEN** a apresentação da URL chega sem credencial de persona, pela superfície pública
- **THEN** o núcleo a processa, porque a rota dispensa persona e exige apenas a chave da
  aplicação que faz a chamada

### Requirement: A chave só é apresentável por quem passou pela emissão

O núcleo SHALL identificar, na apresentação da URL, a chave alvo pelo seu **identificador**,
entregue ao solicitante na emissão e NEVER devolvido por rota pública. A chamada que informar
identificador desconhecido SHALL ser recusada sem revelar se a chave existe. A chave da
aplicação que faz a chamada NEVER SHALL ser confundida com a chave alvo: quem apresenta a URL
é o solicitante, por uma superfície pública, e a chave da chamada é a da aplicação que
hospeda essa superfície. (`RF-01-51`, `RN-01-33`)

#### Scenario: Identificador desconhecido não confirma nem nega

- **WHEN** uma apresentação de URL informa identificador que não corresponde a chave alguma
- **THEN** o núcleo recusa sem indicar se aquele identificador existe

#### Scenario: A chave da chamada não é a chave alvo

- **WHEN** a apresentação da URL chega com a chave de uma aplicação do projeto e o
  identificador de uma chave de terceiro
- **THEN** o núcleo registra a URL na chave de terceiro indicada, e nada na chave da chamada

#### Scenario: Chave do projeto não recebe URL

- **WHEN** uma apresentação de URL informa o identificador de uma chave de natureza do projeto
- **THEN** o núcleo recusa, porque essa chave não tem prazo a cumprir

### Requirement: Prazo vencido sem URL revoga a chave, sem ato humano

O núcleo SHALL tratar como **revogada** a chave de terceiro cujo prazo de apresentação venceu
sem URL registrada, sem depender de intervenção humana. A chamada seguinte ao vencimento SHALL
receber a mesma recusa de qualquer chave revogada. A situação registrada da chave SHALL
acompanhar o vencimento, de modo que a leitura de gestão mostre "revogada" mesmo que a chave
nunca mais seja apresentada ao núcleo. A revogação por decurso SHALL registrar o motivo e
SHALL NOT atribuir autoria a pessoa alguma. (`RF-01-52`, `RN-01-36`)

#### Scenario: Chamada seguinte ao vencimento é recusada

- **WHEN** uma aplicação de terceiro chama o núcleo depois de vencido o prazo, sem ter
  apresentado URL
- **THEN** a chamada recebe a mesma recusa das demais chaves revogadas, sem distinguir o
  motivo

#### Scenario: A leitura de gestão mostra a chave vencida como revogada

- **WHEN** um Admin lê as chaves emitidas depois de vencido o prazo de uma delas, e essa chave
  não voltou a chamar o núcleo
- **THEN** ela aparece como revogada, com o motivo do decurso e sem autoria de pessoa

#### Scenario: Chave com URL apresentada não é alcançada pelo decurso

- **WHEN** o prazo original de uma chave que já apresentou URL se esgota
- **THEN** a chave segue vigente, porque o prazo foi cumprido

#### Scenario: Revogada por decurso, nova solicitação é possível

- **WHEN** o interessado cuja chave foi revogada por decurso envia nova solicitação
- **THEN** o núcleo a aceita, e a aprovação dela rende uma chave nova, sem reabrir a revogada

### Requirement: Admin revoga chave a qualquer tempo, com motivo e autoria

O núcleo SHALL permitir a um Admin revogar chave a qualquer tempo, registrando **motivo** e
**autoria**. A aplicação alcançada SHALL perder o acesso na chamada seguinte. A revogação
NEVER SHALL desfazer registro algum, porque a chave de terceiro só lê. (`RF-01-53`,
`RN-01-36`)

#### Scenario: Revogação registra motivo e quem revogou

- **WHEN** um Admin revoga uma chave informando o motivo
- **THEN** o núcleo grava o motivo, a autoria e a data e hora da revogação

#### Scenario: Acesso cai na chamada seguinte

- **WHEN** a aplicação cuja chave foi revogada faz a chamada seguinte
- **THEN** ela recebe a mesma recusa das demais chaves revogadas

#### Scenario: Revogar não desfaz nada

- **WHEN** uma chave de terceiro é revogada
- **THEN** nenhum registro do núcleo é alterado ou removido em consequência da revogação

#### Scenario: Revogação sem motivo é recusada

- **WHEN** um Admin chama a revogação sem informar o motivo
- **THEN** o núcleo recusa e a chave permanece vigente

### Requirement: A gestão lê as chaves emitidas, nunca o segredo

O núcleo SHALL oferecer a Admin a leitura das chaves emitidas, com aplicação, natureza,
ambiente, prazo de apresentação, URL apresentada e situação. A leitura NEVER SHALL devolver o
segredo nem o seu resumo criptográfico. (`RF-01-53`, `RN-01-35`, PRD-01 §9)

#### Scenario: Leitura traz o estado do ciclo de vida

- **WHEN** um Admin lê as chaves emitidas
- **THEN** cada chave aparece com prazo, URL apresentada quando houver e situação atual

#### Scenario: Leitura nunca devolve o segredo

- **WHEN** um Admin lê uma chave recém-emitida
- **THEN** a resposta não contém o segredo em claro nem o seu resumo criptográfico

#### Scenario: Quem não é Admin não lê as chaves

- **WHEN** uma persona que não é Admin chama a leitura das chaves
- **THEN** o núcleo recusa por falta de permissão do papel

## MODIFIED Requirements

### Requirement: A implantação semeia a chave de cada aplicação do projeto, por ambiente

O núcleo SHALL emitir, na implantação, uma chave para cada aplicação do próprio projeto **em
cada ambiente**, marcada com natureza "do projeto" e **sem prazo de apresentação de URL**. São
oito aplicações e dois ambientes — desenvolvimento e produção —, logo dezesseis chaves. A
unicidade de uma chave vigente por aplicação e ambiente SHALL valer **apenas para as chaves de
natureza do projeto**: ela existe para garantir estas dezesseis, e a chave de terceiro se
identifica pela solicitação que a originou. (`RF-01-54`, `RN-01-51`, documento 03 §§1, 1.13)

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

#### Scenario: A unicidade não alcança a chave de terceiro

- **WHEN** duas chaves de terceiro vigentes existem no ambiente de produção declarando o mesmo
  nome de aplicação
- **THEN** o núcleo as mantém as duas, porque a unicidade por aplicação e ambiente vale só
  para as chaves do projeto
