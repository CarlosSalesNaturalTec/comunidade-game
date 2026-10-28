# Spec Delta

## ADDED Requirements

### Requirement: O Mestre autor corrige o conteúdo que já gravou

O núcleo SHALL aceitar do **Mestre autor da trilha** a correção de um `Conteudo` já gravado,
alcançando **corpo**, **endereço**, **autoria** e **fonte**. A correção SHALL valer em
**qualquer situação da trilha** — rascunho, publicada ou despublicada —, e NEVER SHALL apagar
nem alterar o que Guerreiros e Guerreiras já gravaram. Pedido de outro Mestre SHALL responder
**403**, e o Admin NEVER SHALL corrigir conteúdo: ele audita e despublica a trilha, não a
redige. (`RF-09-123`, PRD-09 §§8, 9)

#### Scenario: O Mestre autor corrige o corpo do texto

- **WHEN** o Mestre autor corrige o corpo de um conteúdo de texto de missão da própria trilha
- **THEN** o núcleo grava o corpo corrigido, e o conteúdo segue na mesma missão e na mesma ordem

#### Scenario: A correção alcança a trilha publicada

- **WHEN** o Mestre autor corrige a fonte de um conteúdo de missão de trilha já publicada
- **THEN** o núcleo grava a correção, e a situação da trilha permanece publicada

#### Scenario: Mestre que não é o autor é recusado

- **WHEN** um Mestre que não é o autor da trilha corrige conteúdo de missão dela
- **THEN** o núcleo responde **403** e nada é alterado

#### Scenario: Admin não corrige conteúdo

- **WHEN** um Admin corrige conteúdo de uma missão
- **THEN** o núcleo responde **403** e nada é alterado

#### Scenario: A correção confere a coerência do tipo

- **WHEN** o Mestre autor corrige um conteúdo de texto deixando o corpo vazio, ou um de link
  externo deixando o endereço vazio
- **THEN** o núcleo responde **422** e nada é alterado

#### Scenario: A correção confere a fonte do terceiro

- **WHEN** o Mestre autor passa a autoria de um conteúdo para terceiro sem informar a fonte
- **THEN** o núcleo responde **422** e nada é alterado

### Requirement: O tipo e o arquivo de um conteúdo não se alteram

O núcleo NEVER SHALL aceitar a troca do **tipo** de um `Conteudo` já gravado, nem a troca do
**arquivo** de um conteúdo de imagem, vídeo ou arquivo de apoio: trocar um deles é **remover**
o conteúdo e **cadastrar outro**. Tentativa de alterar o tipo SHALL responder **422**, dizendo
que o caminho é remover e cadastrar. A sessão de envio SHALL seguir aberta apenas para o
conteúdo que **ainda não** teve envio confirmado. (`RN-09-45`, `RF-09-124`, PRD-09 §8)

#### Scenario: Trocar o tipo é recusado

- **WHEN** o Mestre autor tenta corrigir um conteúdo de texto passando-o a conteúdo de vídeo
- **THEN** o núcleo responde **422** dizendo que o caminho é remover e cadastrar outro

#### Scenario: Reabrir envio de conteúdo já confirmado é recusado

- **WHEN** o Mestre autor pede sessão de envio para um conteúdo cujo envio já foi confirmado
- **THEN** o núcleo recusa, e os bytes gravados permanecem como estão

### Requirement: O Mestre autor remove o conteúdo, e o arquivo sai com ele

O núcleo SHALL aceitar do **Mestre autor da trilha** a remoção de um `Conteudo` já gravado, em
**qualquer situação da trilha**, e SHALL **apagá-lo**: nenhum registro aponta para o conteúdo da
missão. Havendo arquivo com envio confirmado, o núcleo SHALL **removê-lo do armazenamento** no
mesmo ato. Pedido de outro Mestre, ou de Admin, SHALL responder **403**.
(`RF-09-124`, `RF-09-20`, `RN-09-07`, PRD-09 §§8, 9)

#### Scenario: O conteúdo de texto é removido

- **WHEN** o Mestre autor remove um conteúdo de texto de missão da própria trilha
- **THEN** o núcleo apaga o conteúdo, e a missão passa a apresentar os demais

#### Scenario: Remover conteúdo com arquivo apaga os bytes

- **WHEN** o Mestre autor remove um conteúdo de vídeo cujo envio foi confirmado
- **THEN** o núcleo apaga o conteúdo e remove o arquivo do armazenamento

#### Scenario: Remover conteúdo sem envio confirmado não falha

- **WHEN** o Mestre autor remove um conteúdo de arquivo que nunca teve o envio confirmado
- **THEN** o núcleo apaga o conteúdo, e nenhuma remoção de arquivo é tentada

#### Scenario: A remoção alcança a trilha publicada

- **WHEN** o Mestre autor remove conteúdo de missão de trilha já publicada
- **THEN** o núcleo apaga o conteúdo, e a situação da trilha permanece publicada

#### Scenario: Quem não é o autor não remove

- **WHEN** um Mestre que não é o autor, ou um Admin, remove conteúdo de uma missão
- **THEN** o núcleo responde **403** e o conteúdo permanece

#### Scenario: Os restantes não são renumerados

- **WHEN** o segundo de três conteúdos de uma missão é removido
- **THEN** o primeiro e o terceiro conservam a ordem que tinham, e a leitura os traz nessa
  sequência

### Requirement: O Mestre autor move o conteúdo na ordem da missão

O núcleo SHALL aceitar do **Mestre autor da trilha** o pedido de **mover** um `Conteudo` para
cima ou para baixo entre os conteúdos da mesma missão, trocando a ordem dele com a do
**vizinho** naquele sentido. Mover o primeiro para cima, ou o último para baixo, SHALL ser
recusado sem alterar nada. A ordem resultante SHALL valer para toda leitura do conteúdo da
missão. (`RF-09-126`, PRD-09 §8)

#### Scenario: O conteúdo sobe uma posição

- **WHEN** o Mestre autor move para cima o segundo conteúdo de uma missão
- **THEN** ele passa à frente do primeiro, e a leitura da missão os traz na nova ordem

#### Scenario: Mover o primeiro para cima é recusado

- **WHEN** o Mestre autor move para cima o primeiro conteúdo da missão
- **THEN** o núcleo recusa em linguagem simples e nenhuma ordem é alterada

#### Scenario: Quem não é o autor não move

- **WHEN** um Mestre que não é o autor da trilha move um conteúdo de missão dela
- **THEN** o núcleo responde **403** e nenhuma ordem é alterada

### Requirement: Cada conteúdo novo nasce depois dos que a missão já tem

O núcleo SHALL atribuir a todo `Conteudo` novo uma **ordem posterior** à dos conteúdos que a
missão já tem, e NEVER SHALL deixar dois conteúdos da mesma missão com a **mesma ordem** — sem
o que a sequência que o Guerreiro(a) lê fica indefinida. Conteúdo gravado antes desta exigência
SHALL ser renumerado, uma vez, pela sequência de criação dentro de cada missão.
(`RF-09-126`, `RF-09-14`, PRD-09 §8)

#### Scenario: O conteúdo novo entra por último

- **WHEN** o Mestre autor cadastra o terceiro conteúdo de uma missão
- **THEN** ele nasce com ordem posterior à dos dois que já estavam, e a leitura o traz por último

#### Scenario: O conteúdo já gravado é renumerado

- **WHEN** uma missão gravada antes desta exigência tem três conteúdos todos com a mesma ordem
- **THEN** eles passam a ter ordens distintas, na sequência em que foram criados
