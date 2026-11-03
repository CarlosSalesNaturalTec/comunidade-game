# Spec Delta

## REMOVED Requirements

### Requirement: A produção da criação original é texto, imagem, vídeo, arquivo ou link

**Reason**: Substituída pela versão de **seis** tipos. Decisão do fundador de 2026-11-03
(documento 09 §1): o áudio entra como sexto tipo de produção do aluno, e o enunciado antigo
fixava "cinco valores fechados" e os declarava "os mesmos que o conteúdo da missão já usa" —
as duas afirmações deixam de valer.

**Migration**: Nada a migrar nos dados: o conjunto só cresce, e toda criação já gravada tem
tipo que continua válido. Quem **envia** não muda; quem **lista** os tipos passa a receber
seis. O `TipoDeConteudo` do Mestre segue com cinco.

## ADDED Requirements

### Requirement: A produção da criação original é texto, imagem, áudio, vídeo, arquivo ou link

A criação original SHALL declarar o **tipo da produção** entre os seis valores fechados —
**texto**, **imagem**, **áudio**, **vídeo**, **arquivo** e **link externo**. Tipo fora dos seis
SHALL ser recusado com **422**. O tipo do **conteúdo da missão**, que é do Mestre, segue com os
cinco dele e NEVER SHALL ganhar áudio por esta regra. (`RF-05-40`, `RF-01-77`, documento 02 §4)

#### Scenario: Entrega em texto traz o corpo escrito

- **WHEN** o Guerreiro(a) entrega a criação original declarando tipo texto e o corpo
- **THEN** o núcleo grava a produção escrita com o registro

#### Scenario: Entrega em link externo traz o endereço

- **WHEN** o Guerreiro(a) entrega a criação original declarando tipo link externo e o endereço
- **THEN** o núcleo grava o endereço com o registro

#### Scenario: Entrega em mídia nasce sem o arquivo e o recebe depois

- **WHEN** o Guerreiro(a) entrega a criação original declarando tipo imagem, áudio, vídeo ou
  arquivo
- **THEN** o núcleo grava o registro sem mídia, e ela passa a existir quando o envio do arquivo
  conclui

#### Scenario: Entrega em áudio é aceita

- **WHEN** o Guerreiro(a) entrega a criação original declarando tipo áudio
- **THEN** o núcleo grava o registro, que recebe a mídia quando o envio conclui

#### Scenario: Tipo fora dos seis valores é recusado

- **WHEN** chega uma criação original com tipo de produção diferente dos seis
- **THEN** o núcleo responde 422 e nada é gravado

#### Scenario: O conteúdo da missão não ganha o tipo áudio

- **WHEN** o Mestre autor declara um conteúdo de missão com tipo áudio
- **THEN** o núcleo o recusa, porque o tipo do conteúdo segue com os cinco valores dele

### Requirement: A mídia da criação original é servida a quem pode ver a criação

O núcleo SHALL servir os **bytes** da mídia de uma criação original a quem já pode ver aquela
criação: o **Guerreiro(a) creditado**, o **Mestre autor** da trilha e o **Admin**. Persona fora
desse conjunto SHALL receber **403**, e criação **sem mídia**, **404**. (`RF-01-78`,
`RN-01-60`, `RF-05-43`)

#### Scenario: O autor lê a mídia da própria criação

- **WHEN** o Guerreiro(a) creditado numa criação original pede a mídia dela
- **THEN** o núcleo devolve os bytes com o tipo MIME gravado no envio

#### Scenario: O Mestre autor lê a mídia da criação que lhe cabe julgar

- **WHEN** o Mestre autor da trilha pede a mídia de uma criação original dela
- **THEN** o núcleo devolve os bytes com o tipo MIME gravado no envio

#### Scenario: Quem não é creditado nem autor é recusado

- **WHEN** um Guerreiro(a) que não é creditado na criação pede a mídia dela
- **THEN** o núcleo responde 403 e nenhum byte é servido

#### Scenario: Criação sem mídia responde 404

- **WHEN** se pede a mídia de uma criação original de tipo texto ou link externo
- **THEN** o núcleo responde 404

#### Scenario: Criação cujo envio não concluiu responde 404

- **WHEN** se pede a mídia de uma criação original cujo envio foi aberto e não confirmado
- **THEN** o núcleo responde 404, porque a mídia ainda não existe
