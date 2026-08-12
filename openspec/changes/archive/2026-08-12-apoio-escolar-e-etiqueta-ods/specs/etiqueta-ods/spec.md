## Purpose

A etiqueta ODS é o rótulo descritivo que liga trilha e missão aos Objetivos de Desenvolvimento
Sustentável — sem pesar no motor de pontuação — e a base da cobertura que a plataforma agrega.

## ADDED Requirements

### Requirement: Etiqueta ODS presa a uma trilha ou a uma missão, nunca as duas

O núcleo SHALL manter a etiqueta ODS com um **objetivo** de **1 a 18** e uma **meta** opcional em
texto livre (`4.7`, `13.3`), presa a **exatamente uma** trilha **ou** a **exatamente uma**
missão — nunca as duas ao mesmo tempo, nem nenhuma das duas. Uma trilha ou missão SHALL aceitar
**mais de uma** etiqueta. Só o **Mestre autor** da trilha declara a etiqueta, dela ou de uma
missão dela — a mesma posse já aplicada à trilha; outro Mestre SHALL receber **403**. Etiqueta
com objetivo fora de 1 a 18, ou sem trilha nem missão, ou com as duas, SHALL ser recusada com
**422**. (`RF-01-40`, `RF-01-45`, `RF-01-16`, 11 §2.1)

#### Scenario: Mestre autor etiqueta a trilha

- **WHEN** o Mestre autor declara uma etiqueta com objetivo 4 e meta "4.7" na própria trilha
- **THEN** o núcleo grava a etiqueta vinculada àquela trilha

#### Scenario: Mestre autor etiqueta uma missão da trilha

- **WHEN** o Mestre autor declara uma etiqueta em uma missão da própria trilha
- **THEN** o núcleo grava a etiqueta vinculada àquela missão, não à trilha

#### Scenario: Trilha aceita mais de uma etiqueta

- **WHEN** o Mestre autor declara uma segunda etiqueta, com objetivo diferente, na mesma trilha
- **THEN** o núcleo grava as duas etiquetas

#### Scenario: Etiqueta com objetivo fora da faixa é recusada

- **WHEN** chega uma etiqueta com objetivo 0 ou 19
- **THEN** o núcleo responde 422 e nada é gravado

#### Scenario: Etiqueta sem trilha nem missão é recusada

- **WHEN** chega uma etiqueta sem trilha e sem missão vinculada
- **THEN** o núcleo responde 422 e nada é gravado

#### Scenario: Etiqueta com trilha e missão ao mesmo tempo é recusada

- **WHEN** chega uma etiqueta vinculada a uma trilha e a uma missão ao mesmo tempo
- **THEN** o núcleo responde 422 e nada é gravado

#### Scenario: Mestre que não é o autor é recusado

- **WHEN** um Mestre que não é o autor da trilha tenta declarar etiqueta nela ou em uma missão
  dela
- **THEN** o núcleo responde 403 e nada é gravado

### Requirement: A etiqueta de missão prevalece sobre a da trilha nos vínculos dela

O núcleo SHALL resolver, para qualquer vínculo que dependa da etiqueta de uma missão, a etiqueta
**declarada na própria missão** quando existir; na falta dela, a etiqueta da **trilha**. (`RF-01-
45`, 11 §2.1)

#### Scenario: Missão com etiqueta própria prevalece sobre a da trilha

- **WHEN** uma missão tem etiqueta própria diferente da etiqueta da trilha
- **THEN** o núcleo resolve, para aquela missão, a etiqueta própria dela

#### Scenario: Missão sem etiqueta própria herda a da trilha

- **WHEN** uma missão não tem etiqueta própria e a trilha tem etiqueta declarada
- **THEN** o núcleo resolve, para aquela missão, a etiqueta da trilha

### Requirement: A etiqueta não pontua e não é poder

O núcleo NEVER SHALL creditar ponto, certificar nível ou conceder badge a partir de uma etiqueta
ODS, e a etiqueta NEVER SHALL ser confundida com um poder do catálogo. (`RN-01-23`, 11 §2.1)

#### Scenario: Declarar etiqueta não credita pontuação

- **WHEN** o Mestre autor declara uma etiqueta em uma trilha ou missão
- **THEN** nenhum ponto, nível ou badge é concedido a ninguém por causa dela

### Requirement: Cobertura de ODS agrega por trilha, poder e comunidade, nunca por Guerreiro(a)

O núcleo SHALL agregar a cobertura de ODS — o conjunto de objetivos distintos etiquetados — por
**trilha**, por **poder** (a união das etiquetas das trilhas vinculadas a ele) e por
**comunidade** (a união das etiquetas das trilhas em que há Guerreiro(a) daquela comunidade com
Resultado registrado). A cobertura NEVER SHALL ser exposta nem calculada por Guerreiro(a)
individual. (`RF-01-42`, `RN-01-24`, 11 §2.1)

#### Scenario: Cobertura por trilha soma os objetivos da trilha e das missões dela

- **WHEN** a trilha tem etiqueta de objetivo 4 e uma missão dela tem etiqueta de objetivo 13
- **THEN** a cobertura da trilha inclui os objetivos 4 e 13

#### Scenario: Cobertura por poder soma as trilhas vinculadas a ele

- **WHEN** duas trilhas do mesmo poder têm etiquetas de objetivos diferentes
- **THEN** a cobertura do poder inclui os dois objetivos

#### Scenario: Cobertura por comunidade soma as trilhas em curso na comunidade

- **WHEN** um Guerreiro(a) de uma comunidade tem Resultado registrado numa trilha etiquetada
- **THEN** a cobertura daquela comunidade inclui o objetivo da trilha

#### Scenario: Cobertura nunca é calculada por Guerreiro(a)

- **WHEN** se procura no núcleo uma função que agregue cobertura de ODS por Guerreiro(a)
- **THEN** nenhuma existe: as três agregações são por trilha, poder e comunidade
