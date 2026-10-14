# Spec Delta

## MODIFIED Requirements

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

## REMOVED Requirements

### Requirement: A semeadura traz o que a documentação já decidiu, sem sobrescrever edição

**Reason**: O enunciado mandava semear a nota de transparência sobre IA como **rascunho** e
deixar **"Contatos" sem texto**, porque nenhum documento trazia contato algum. As duas coisas
deixaram de valer: a decisão do fundador de 2026-10-14 tornou a nota **texto final** — fechando
a pendência do PRD-03 §14 — e criou o **canal único de contato** do projeto, descido ao
documento 04 §1. Mantê-lo faria o requisito contradizer o que a semeadura passa a fazer.

**Migration**: Substituído por cinco requisitos, um por comportamento: a mecânica da semeadura
das três seções, e o conteúdo decidido de "Quem somos", do bloco "Licenças", de "Contatos" e de
"Como apoiar". Tudo o que este exigia continua exigido — a chave PIX e o titular do documento
04 §1, a nota com o que ela declara, o bloco "Licenças", a convergência só onde a seção não tem
texto e a garantia de que repetir a semeadura não desfaz a edição de um Admin.

## ADDED Requirements

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
