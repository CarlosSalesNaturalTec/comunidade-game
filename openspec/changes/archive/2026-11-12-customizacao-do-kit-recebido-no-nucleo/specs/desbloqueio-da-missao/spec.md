## ADDED Requirements

### Requirement: O desafio prático declara, opcional, o kit que apresenta

A declaração do desafio **prático** SHALL aceitar, **opcional**, o **kit apresentado**: uma
**recompensa de marco da mesma trilha** da missão. O núcleo NEVER SHALL distinguir kit de
camisa ou livro pelo tipo de recurso — o que é kit é a declaração do Mestre autor. Recompensa
**inexistente** ou de **outra trilha** SHALL ser recusada com **422** nomeando o campo, e nada
é gravado. Declarar de novo **substitui** o kit anterior, inclusive para nenhum. O **quiz**
NEVER SHALL declarar kit, e declarar quiz sobre um prático que tinha kit SHALL apagá-lo, como
já apaga os demais campos do prático. Prático declarado antes desta regra segue sem kit, sem
_backfill_. (`RF-09-141`, documento 11 §2.2)

#### Scenario: O Mestre autor declara o kit que o prático apresenta

- **WHEN** o Mestre autor declara o prático de uma missão apontando uma recompensa de marco da
  mesma trilha como kit apresentado
- **THEN** o núcleo grava o kit junto do prático, e a leitura do desafio o devolve

#### Scenario: O kit é opcional

- **WHEN** o Mestre autor declara o prático sem kit apresentado
- **THEN** o núcleo grava o prático normalmente, com o kit nulo

#### Scenario: Recompensa de outra trilha é recusada

- **WHEN** o Mestre autor aponta como kit uma recompensa de marco de outra trilha
- **THEN** o núcleo responde **422** nomeando o campo, e o desafio anterior permanece como
  estava

#### Scenario: O quiz não declara kit

- **WHEN** a declaração de um desafio em forma de quiz traz kit apresentado
- **THEN** o núcleo responde **422** dizendo que o campo não se aplica ao quiz, e nada é
  gravado

### Requirement: A leitura do desafio prático traz o kit declarado

Toda leitura que já serve a forma aceita, o critério de aceite e o título curto do prático SHALL
trazer também o **kit apresentado** — o identificador da recompensa de marco e o nome do tipo de
recurso dela —, dentro de `desafio_de_desbloqueio` como `kit_apresentado`. Sem kit declarado, e
no quiz, o campo SHALL vir **nulo**. (`RF-09-141`)

#### Scenario: O Mestre autor reencontra o kit que declarou

- **WHEN** o Mestre autor lê as trilhas dele depois de declarar o kit de um prático
- **THEN** a missão traz o kit apresentado, com o identificador da recompensa e o nome do tipo
  de recurso

#### Scenario: Sem kit, o campo vem nulo

- **WHEN** alguém lê uma missão cujo prático não declarou kit, ou cujo desbloqueio é quiz
- **THEN** o kit apresentado vem nulo
