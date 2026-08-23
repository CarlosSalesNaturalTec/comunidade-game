## ADDED Requirements

### Requirement: O Mestre etiqueta a trilha com os ODS que ela toca

A App 09 SHALL oferecer ao Mestre autor, dentro da trilha, a declaração das **etiquetas ODS**
da trilha — o **objetivo**, escolhido de 1 a 18, e a **meta** opcional, quando ele souber. A
aplicação SHALL apresentar as etiquetas já declaradas e permitir **acrescentar, alterar e
remover** antes de confirmar, gravando o conjunto resultante de uma vez. A aplicação NEVER
SHALL exigir que o Mestre digite código, sigla técnica ou identificador, e NEVER SHALL oferecer
a declaração em trilha de outro Mestre. (`RF-09-92`, `RF-09-12`)

#### Scenario: Mestre etiqueta a trilha

- **WHEN** o Mestre autor escolhe o objetivo 4, informa a meta "4.7" e confirma
- **THEN** a aplicação grava a etiqueta no núcleo e passa a apresentá-la na trilha

#### Scenario: Mestre etiqueta sem saber a meta

- **WHEN** o Mestre autor escolhe o objetivo 13 e confirma sem informar a meta
- **THEN** a aplicação grava a etiqueta apenas com o objetivo, e nada é recusado

#### Scenario: Mestre declara mais de um objetivo na trilha

- **WHEN** o Mestre autor acrescenta os objetivos 4 e 13 e confirma
- **THEN** a aplicação apresenta os dois objetivos na trilha

#### Scenario: O que o Mestre remove some da trilha

- **WHEN** o Mestre autor remove um dos objetivos declarados e confirma
- **THEN** a aplicação deixa de apresentar aquele objetivo na trilha

#### Scenario: O Mestre retira todas as etiquetas

- **WHEN** o Mestre autor remove todos os objetivos e confirma
- **THEN** a aplicação apresenta a trilha sem etiqueta, e a trilha segue publicável

#### Scenario: A etiquetagem não é oferecida em trilha alheia

- **WHEN** um Mestre abre uma trilha de que não é autor
- **THEN** a aplicação não oferece a ação de etiquetar

### Requirement: O Mestre etiqueta uma missão à parte quando ela toca objetivo diferente

A App 09 SHALL oferecer ao Mestre autor, dentro de cada missão, a declaração das **etiquetas
ODS da missão**, pelo mesmo caminho da trilha e igualmente opcional. A aplicação SHALL deixar
claro que a etiqueta da missão só é necessária quando ela toca objetivo **diferente** do da
trilha, e que a missão sem etiqueta própria responde pela da trilha. A confirmação na missão
NEVER SHALL alterar as etiquetas da trilha. (`RF-09-98`, `RF-09-12`)

#### Scenario: Mestre etiqueta uma missão

- **WHEN** o Mestre autor escolhe o objetivo 13 dentro de uma missão e confirma
- **THEN** a aplicação grava a etiqueta na missão e passa a apresentá-la ali

#### Scenario: Missão sem etiqueta responde pela da trilha

- **WHEN** o Mestre autor abre uma missão sem etiqueta própria numa trilha etiquetada
- **THEN** a aplicação apresenta que a missão responde pela etiqueta da trilha

#### Scenario: Etiquetar a missão não mexe na trilha

- **WHEN** o Mestre autor confirma as etiquetas de uma missão
- **THEN** a aplicação continua apresentando as etiquetas da trilha inalteradas

### Requirement: O Mestre vê a cobertura de ODS da sua trilha

A App 09 SHALL apresentar ao Mestre autor, na trilha, a **cobertura de ODS resultante** do que
ele etiquetou — os objetivos distintos da trilha e das missões dela, reunidos. A cobertura
SHALL ser apresentada como resultado agregado da trilha, e NEVER SHALL ser apresentada por
Guerreiro(a). (`RF-09-94`, `RN-01-24`)

#### Scenario: A cobertura reúne trilha e missões

- **WHEN** o Mestre autor etiquetou a trilha com o objetivo 4 e uma missão com o objetivo 13
- **THEN** a aplicação apresenta a cobertura da trilha com os objetivos 4 e 13

#### Scenario: A cobertura acompanha o que o Mestre acabou de declarar

- **WHEN** o Mestre autor acrescenta um objetivo novo e confirma
- **THEN** a aplicação apresenta a cobertura já com o objetivo novo

#### Scenario: Trilha sem etiqueta apresenta cobertura vazia

- **WHEN** a trilha e as missões dela não têm etiqueta
- **THEN** a aplicação apresenta a cobertura vazia, sem apresentar erro
