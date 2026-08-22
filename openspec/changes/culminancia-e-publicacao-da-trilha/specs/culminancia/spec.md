## Purpose

Guarda o que a criação original de uma trilha precisa ser — a descrição esperada, se é
individual ou de equipe e o critério pelo qual o Mestre autor a validará. É a especificação da
produção final; a entrega e a validação dela são de `criacao-original`.

## ADDED Requirements

### Requirement: Toda trilha tem no máximo uma culminância, declarada pelo Mestre autor

O núcleo SHALL guardar, por trilha, uma **culminância** com descrição da criação original
esperada, **modalidade** — individual ou em equipe — e **critério de validação**. A declaração
SHALL ser privativa do **Mestre autor** da trilha; outro Mestre SHALL receber **403** e Admin
NEVER SHALL declará-la, porque o Admin não edita a trilha de um Mestre. Uma segunda declaração
na mesma trilha SHALL substituir a anterior, e NEVER SHALL criar uma segunda culminância.
(`RF-09-29`, `RF-09-30`, PRD-09 §4, §8)

#### Scenario: Mestre autor declara a culminância

- **WHEN** o Mestre autor envia descrição, modalidade e critério de validação para a trilha
- **THEN** o núcleo grava a culminância vinculada àquela trilha e a devolve

#### Scenario: Modalidade fora dos dois valores é recusada

- **WHEN** chega uma culminância com modalidade diferente de individual ou em equipe
- **THEN** o núcleo responde 422 e nada é gravado

#### Scenario: Culminância sem critério de validação é recusada

- **WHEN** chega uma culminância sem critério de validação declarado
- **THEN** o núcleo responde 422 e nada é gravado

#### Scenario: Mestre que não é o autor é recusado

- **WHEN** um Mestre que não é o autor declara a culminância da trilha
- **THEN** o núcleo responde 403 e a trilha permanece como estava

#### Scenario: A segunda declaração substitui a primeira

- **WHEN** o Mestre autor declara a culminância de uma trilha que já tem uma
- **THEN** o núcleo grava os novos valores e a trilha segue com uma única culminância

### Requirement: A criação original se resolve pela trilha, sem referência própria à culminância

Com uma culminância por trilha, a `CriacaoOriginal` SHALL continuar referenciando **a trilha**,
e o núcleo SHALL resolver por ela a culminância aplicável. Nenhuma referência nova SHALL ser
exigida da criação original já gravada. (PRD-09 §8)

#### Scenario: A culminância aplicável vem da trilha da criação

- **WHEN** uma criação original entregue contra uma trilha que tem culminância é consultada
- **THEN** a culminância aplicável é a daquela trilha

#### Scenario: Criação anterior à culminância continua válida

- **WHEN** existe criação original entregue antes de a trilha ter culminância declarada
- **THEN** o registro dela permanece íntegro e nada nele é exigido a mais
