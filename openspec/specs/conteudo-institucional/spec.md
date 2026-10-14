# conteudo-institucional Specification

## Purpose
O conteúdo institucional da vitrine — "Quem somos", "Contatos" e "Como apoiar" — é publicado
por Admin e lido por qualquer visitante. Esta capacidade cobre a entidade, a leitura pública, a
escrita de Admin e a semeadura do que a documentação já decidiu; a tela de edição é da App 03.

## Requirements

### Requirement: O conteúdo institucional tem três seções, cada uma com texto, autor e data

O núcleo SHALL guardar o conteúdo institucional em **três seções fixas** — "Quem somos",
"Contatos" e "Como apoiar" —, cada uma com o **texto** publicado, **quem publicou** e **quando**.
Cada seção SHALL ter **uma única versão vigente**: publicar de novo a substitui. O texto SHALL
ser simples, em parágrafos, e uma linha iniciada por `## ` SHALL abrir um bloco com título. Uma
seção que nunca foi publicada SHALL existir sem texto, e o núcleo NEVER SHALL inventá-lo.
(`RF-02-80`, `RF-03-45`, PRD-03 §8)

#### Scenario: A publicação grava o texto, o autor e a data

- **WHEN** um Admin publica o texto de uma seção
- **THEN** a seção passa a ter esse texto como o vigente, com o Admin e a data da publicação

#### Scenario: Publicar de novo substitui a versão vigente

- **WHEN** um Admin publica outro texto na mesma seção
- **THEN** só o novo texto é o vigente, e a leitura pública devolve apenas ele

#### Scenario: Seção nunca publicada não tem texto

- **WHEN** uma das três seções nunca recebeu publicação nem semeadura
- **THEN** a seção existe sem texto, e nenhum texto de exemplo ocupa o lugar

### Requirement: A leitura pública devolve as três seções, exige chave e nunca revela o autor

O núcleo SHALL responder `GET /v1/vitrine/conteudo-institucional` **sem token de sessão** e
**com chave de aplicação válida**, devolvendo as **três seções em ordem fixa** — texto e, em
"Quem somos", o link do vídeo —, publicadas ou não. NEVER SHALL devolver quem publicou. A rota
SHALL ser só de leitura. (`RF-03-45`, `RF-03-49`, `RF-01-02`, PRD-03 §9)

#### Scenario: Consulta pública responde sem token de sessão

- **WHEN** chega a consulta com chave de aplicação válida e sem token de sessão
- **THEN** o núcleo devolve as três seções, na mesma ordem em qualquer consulta

#### Scenario: Consulta sem chave é recusada

- **WHEN** chega a consulta sem chave de aplicação
- **THEN** o núcleo responde 401, sem diferenciar chave ausente, inválida e revogada

#### Scenario: A resposta não identifica quem publicou

- **WHEN** uma seção foi publicada por um Admin
- **THEN** a resposta pública não traz o Admin, nem por código

### Requirement: Só Admin publica, uma seção por vez, e a publicação fica auditada

O núcleo SHALL aceitar `PUT /v1/conteudo-institucional/{secao}` **somente de Admin**, com o
texto da seção, e SHALL recusar as demais personas. Seção que não é uma das três SHALL ser
recusada com o erro de corpo único, sem criar seção nova. O texto SHALL ser obrigatório. A
publicação SHALL entrar na trilha de auditoria como toda escrita sob `/v1`. (`RF-02-80`,
`RF-02-99`, PRD-02 §9)

#### Scenario: Admin publica uma seção

- **WHEN** um Admin em sessão envia o texto de "Como apoiar"
- **THEN** o núcleo grava a publicação e a leitura pública seguinte já a devolve

#### Scenario: Outra persona é recusada

- **WHEN** Mestre, Apoiador, responsável ou Guerreiro(a) tenta publicar uma seção
- **THEN** o núcleo responde 403 e nada é gravado

#### Scenario: Seção inexistente é recusada

- **WHEN** o Admin envia texto para uma seção que não é uma das três
- **THEN** o núcleo recusa com o erro de corpo único e nenhuma seção é criada

#### Scenario: Texto ausente é recusado

- **WHEN** o Admin envia a publicação sem texto
- **THEN** o núcleo responde 422 apontando o campo em falta

### Requirement: O vídeo de apresentação é um link opcional de "Quem somos"

O núcleo SHALL aceitar, **somente na seção "Quem somos"**, o **link do vídeo de apresentação**
como campo opcional, que SHALL ser um endereço `https`. A publicação sem link SHALL ser válida e
SHALL retirar o link anterior. O link em outra seção, ou fora de `https`, SHALL ser recusado
(422). (`RF-03-49`)

#### Scenario: Link do vídeo em "Quem somos" é aceito

- **WHEN** o Admin publica "Quem somos" com um link `https` de vídeo
- **THEN** a leitura pública devolve o link junto do texto

#### Scenario: Publicar sem o link o retira

- **WHEN** o Admin publica de novo "Quem somos", sem o link
- **THEN** a leitura pública não devolve link de vídeo

#### Scenario: Link em outra seção ou fora de https é recusado

- **WHEN** o Admin envia link de vídeo em "Contatos", ou um link que não é `https`
- **THEN** o núcleo responde 422 e nada é gravado

### Requirement: O Admin lê o conteúdo institucional com autor e data

O núcleo SHALL responder `GET /v1/conteudo-institucional` **somente a Admin**, devolvendo as
**três seções em ordem fixa** — publicadas ou não — cada uma com o texto, o link do vídeo quando
houver, **quem publicou** e **quando**. Persona que não seja Admin SHALL receber **403**. A rota
SHALL ser só de leitura. (`RF-02-80`, decisão do fundador, 2026-10-02)

Esta rota existe porque a leitura pública NEVER SHALL revelar o autor, e a tela de edição do
Admin precisa dele: autor e data chegavam apenas na resposta do `PUT`, e recarregar a tela os
perdia. A rota pública SHALL permanecer exatamente como está. (`RF-03-45`)

Seção que nunca foi publicada SHALL vir sem texto, sem autor e sem data, e o núcleo NEVER SHALL
inventá-los.

#### Scenario: O Admin lê as três seções com a autoria

- **WHEN** um Admin lê o conteúdo institucional
- **THEN** a resposta traz as três seções em ordem fixa, cada uma com texto, autor e data do que
  foi publicado

#### Scenario: Seção nunca publicada vem vazia

- **WHEN** um Admin lê o conteúdo institucional e uma das seções nunca foi publicada
- **THEN** essa seção vem sem texto, sem autor e sem data, e as outras vêm completas

#### Scenario: Quem não é Admin não lê a autoria

- **WHEN** um Mestre, um Apoiador ou um responsável pede a leitura de Admin
- **THEN** o núcleo responde 403

#### Scenario: A leitura pública continua sem autor

- **WHEN** um visitante lê a rota pública do conteúdo institucional
- **THEN** a resposta traz as três seções sem quem publicou e sem quando

### Requirement: A semeadura traz as três seções com texto, sem sobrescrever edição

A semeadura da implantação SHALL criar o conteúdo das **três seções**, **só onde a seção ainda
não tem texto**. Nenhuma seção SHALL nascer com link de vídeo, porque o vídeo de apresentação
ainda não existe. Repetir a semeadura NEVER SHALL alterar seção já publicada por um Admin.
(`RF-03-45`, `RF-03-49`, decisão do fundador de 2026-10-14)

#### Scenario: Banco novo recebe as três seções com texto

- **WHEN** a semeadura roda sobre um banco sem conteúdo institucional
- **THEN** as três seções nascem com texto, nenhuma delas sem autor registrado como semeadura

#### Scenario: Nenhuma seção nasce com vídeo

- **WHEN** a semeadura roda sobre um banco sem conteúdo institucional
- **THEN** nenhuma das três seções tem link de vídeo, e a vitrine não oferece o link

#### Scenario: Repetir a semeadura não desfaz a edição de um Admin

- **WHEN** um Admin republicou "Como apoiar" e a semeadura roda de novo
- **THEN** o texto do Admin continua o vigente

### Requirement: "Quem somos" nasce com a apresentação e a nota de transparência final

A seção "Quem somos" semeada SHALL trazer a **apresentação institucional** (documentos 01 e 04)
e a **nota de transparência sobre IA** como **texto final**. A nota SHALL declarar a plataforma
**construída** com Claude, o atendimento por modelos de terceiros e que a IA **reescreve o
conteúdo do corpus do Mestre para crianças sem as perfilar**, e SHALL remeter ao bloco
"Licenças". (`RF-03-45`, `RF-03-48`, PRD-03 §14)

#### Scenario: A nota declara construção, atendimento e ausência de perfilamento

- **WHEN** se lê a nota semeada
- **THEN** ela diz que a plataforma é construída com Claude, que atende as pessoas com modelos
  de terceiros, que a IA reescreve o conteúdo do Mestre para crianças e não as perfila, e
  remete ao bloco "Licenças"

#### Scenario: A apresentação institucional acompanha a nota

- **WHEN** se lê o texto semeado de "Quem somos"
- **THEN** ele apresenta o projeto antes da nota, e a nota não é a abertura da seção

### Requirement: O título da nota de transparência é a âncora da etiqueta de IA

O bloco da nota SHALL ter o título **"Nota de transparência sobre IA"**, porque o identificador
derivado dele é o endereço para onde a **etiqueta do texto reescrito por IA** das Apps 01 e 05
aponta. Mudar esse título SHALL ser tratado como quebra de contrato, não como melhoria de
redação. (`RF-03-48`, documento 03 §7.1)

#### Scenario: O título da nota é o que a etiqueta de IA ancora

- **WHEN** se lê o texto semeado de "Quem somos"
- **THEN** o bloco da nota tem exatamente o título "Nota de transparência sobre IA", de modo que
  o endereço que a etiqueta das Apps 01 e 05 usa continua a encontrá-lo

### Requirement: O bloco "Licenças" declara o que é aberto, o auxílio de IA e a marca reservada

O bloco **"Licenças"**, que fecha "Quem somos", SHALL declarar as réguas do que é aberto —
código em AGPL, conteúdo educacional e conjunto de dados em CC BY-SA —, que o **auxílio de
ferramentas de IA não altera a licença** do artefato e que a **marca é reservada**, fora das
duas licenças, cabendo a quem replica trocá-la pela sua (documento 03 §1, princípio 4).
(`RF-03-48`)

#### Scenario: "Licenças" declara o auxílio de IA e a marca reservada

- **WHEN** se lê o bloco "Licenças" semeado
- **THEN** ele diz que o auxílio de ferramentas de IA não altera a licença do artefato e que a
  marca — nome, logotipo, símbolo, submarcas e personagens — fica fora da AGPL e da CC BY-SA, e
  que quem replica a plataforma troca a marca pela sua

### Requirement: "Contatos" nasce com um endereço único que não alcança criança

A seção "Contatos" semeada SHALL trazer os caminhos de contato do projeto e **um endereço
único**, que atende a direitos sobre dados, recibo, assunto institucional e conduta, e SHALL
declarar que **nenhum desses canais alcança um Guerreiro(a)**. O endereço SHALL sair como
texto, sem link. (`RF-03-45`, documento 99 §6, invariante 10)

#### Scenario: "Contatos" traz um endereço único, que não alcança criança

- **WHEN** se lê o texto semeado de "Contatos"
- **THEN** ele traz um só endereço do projeto, atendendo a direitos sobre dados, recibo,
  institucional e conduta, e declara que nenhum desses canais alcança um Guerreiro(a)

### Requirement: "Como apoiar" nasce com a chave PIX, o comprovante e a regra do recibo

A seção "Como apoiar" semeada SHALL trazer a **chave PIX** e o **titular** da pessoa jurídica
vinculada, idênticos aos do documento 04 §1, o **comprovante obrigatório** e a regra de que a
plataforma **não emite recibo**, com o endereço de quem o emite. (`RF-03-46`, documento 04 §1)

#### Scenario: Banco novo recebe a chave PIX e o titular

- **WHEN** a semeadura roda sobre um banco sem conteúdo institucional
- **THEN** "Como apoiar" traz a chave PIX e o titular do documento 04 §1

#### Scenario: A seção declara o comprovante e a ausência de recibo

- **WHEN** se lê o texto semeado de "Como apoiar"
- **THEN** ele pede o comprovante no pré-cadastro, diz que a plataforma não confirma PIX
  automaticamente e que não emite recibo, e indica o endereço de quem o emite
