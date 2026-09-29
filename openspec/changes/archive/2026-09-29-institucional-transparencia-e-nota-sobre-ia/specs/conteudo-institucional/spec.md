## Purpose

O conteúdo institucional da vitrine — "Quem somos", "Contatos" e "Como apoiar" — é publicado
por Admin e lido por qualquer visitante. Esta capacidade cobre a entidade, a leitura pública, a
escrita de Admin e a semeadura do que a documentação já decidiu; a tela de edição é da App 03.

## ADDED Requirements

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

- **WHEN** nenhuma publicação foi feita em "Contatos"
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

### Requirement: A semeadura traz o que a documentação já decidiu, sem sobrescrever edição

A semeadura da implantação SHALL criar, **só onde a seção ainda não tem texto**, o conteúdo já
decidido: em "Como apoiar", a **chave PIX** e o **titular** da pessoa jurídica vinculada
(documento 04 §1); em "Quem somos", o **rascunho da nota de transparência sobre IA** e o bloco
**"Licenças"**. A nota SHALL declarar a plataforma **construída** com Claude, o atendimento por
modelos de terceiros, que a IA **reescreve conteúdo do corpus do Mestre para crianças e não as
perfila**, e SHALL remeter ao bloco "Licenças" quanto ao gerado com auxílio de IA. "Contatos"
SHALL ficar sem texto. Repetir a semeadura NEVER SHALL alterar seção já publicada. (`RF-03-46`,
`RF-03-48`, PRD-03 §14)

#### Scenario: Banco novo recebe a chave PIX e o rascunho da nota

- **WHEN** a semeadura roda sobre um banco sem conteúdo institucional
- **THEN** "Como apoiar" traz a chave PIX e o titular do documento 04 §1, "Quem somos" traz a
  nota com o bloco "Licenças", e "Contatos" fica sem texto

#### Scenario: A nota declara construção, atendimento e ausência de perfilamento

- **WHEN** se lê a nota semeada
- **THEN** ela diz que a plataforma é construída com Claude, que atende as pessoas com modelos
  de terceiros, que a IA reescreve o conteúdo do Mestre para crianças e não as perfila, e
  remete ao bloco "Licenças"

#### Scenario: Repetir a semeadura não desfaz a edição de um Admin

- **WHEN** um Admin republicou "Como apoiar" e a semeadura roda de novo
- **THEN** o texto do Admin continua o vigente
