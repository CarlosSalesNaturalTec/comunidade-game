# Spec Delta

## ADDED Requirements

### Requirement: O Admin edita o conteúdo institucional da vitrine pela gestão

A App 03 SHALL oferecer ao Admin a edição das **três seções** do conteúdo institucional —
"Quem somos", "Contatos" e "Como apoiar" —, apresentando o texto vigente de cada uma e **quem
publicou e quando**. Publicar uma seção SHALL substituir a versão vigente dela, uma seção por
vez. (`RF-02-80`)

O **link do vídeo** de apresentação SHALL ser oferecido **somente em "Quem somos"**, como campo
opcional. A tela NEVER SHALL oferecê-lo nas outras duas seções. (`RF-03-49`)

Seção que nunca foi publicada SHALL ser apresentada como vazia e editável, sem autor e sem data,
e a tela NEVER SHALL inventar texto para ela. A recusa de quem não é Admin SHALL ser legível, não
um erro cru.

#### Scenario: As três seções aparecem com a autoria

- **WHEN** um Admin abre a edição do conteúdo institucional
- **THEN** as três seções aparecem na ordem fixa, cada uma com o texto vigente e quem publicou e
  quando

#### Scenario: Publicar substitui a versão vigente

- **WHEN** um Admin edita o texto de uma seção e publica
- **THEN** a seção passa a valer com o texto novo, e a autoria apresentada passa a ser dele

#### Scenario: O vídeo só existe em "Quem somos"

- **WHEN** um Admin abre "Contatos" ou "Como apoiar"
- **THEN** nenhum campo de link de vídeo é oferecido

#### Scenario: Seção vazia é editável

- **WHEN** um Admin abre uma seção que nunca foi publicada
- **THEN** a seção aparece sem texto, sem autor e sem data, e aceita a primeira publicação

### Requirement: A gestão anexa o comprobatório que o Apoiador declarou

A App 03 SHALL apresentar ao Admin a **fila dos documentos comprobatórios que esperam
anexação** — os que Apoiadores declararam pela App 08 e ainda não foram publicados —,
identificando o Apoiador, o rótulo e o endereço de cada um. A fila NEVER SHALL exibir documento
já publicado como se estivesse esperando. (`RF-02-101`)

O Admin SHALL anexar o documento pela própria fila, e a anexação SHALL ser o que o publica na
página do Apoiador. Anexado, o documento SHALL sair da fila. A recusa da anexação SHALL ser
apresentada em linguagem legível, sem código cru. (`RF-02-101`, `RF-14-19`)

A fila NEVER SHALL oferecer edição do endereço ou do rótulo que o Apoiador declarou: o ato do
Admin aqui é anexar, e a edição do artefato do cadastro é outra tela.

#### Scenario: A fila mostra o que espera anexação

- **WHEN** um Admin abre a fila dos comprobatórios e há documentos declarados e não anexados
- **THEN** a fila os apresenta, com o Apoiador, o rótulo e o endereço de cada um

#### Scenario: Anexar publica e esvazia a linha

- **WHEN** um Admin anexa um documento da fila
- **THEN** o documento é publicado e deixa de aparecer entre os que esperam

#### Scenario: Documento já publicado não aparece na fila

- **WHEN** um Apoiador tem um documento já anexado
- **THEN** esse documento não aparece na fila dos que esperam anexação

#### Scenario: A fila vazia se explica

- **WHEN** um Admin abre a fila e nenhum documento espera anexação
- **THEN** a tela informa que não há nada esperando, como informação e não como erro
