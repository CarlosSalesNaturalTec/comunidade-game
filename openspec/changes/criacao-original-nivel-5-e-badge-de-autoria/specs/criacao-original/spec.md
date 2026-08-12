## Purpose

A Criação Original é o registro de que um Guerreiro(a) entregou, ao final da trilha, algo
criado a partir do que aprendeu — a trava viva da regra "toda trilha termina em criação
original" (documento 99 §6 invariante 5), com autoria que nunca se perde.

## ADDED Requirements

### Requirement: Guerreiro(a) entrega a criação original contra uma trilha

O núcleo SHALL registrar a entrega de uma **criação original** de um Guerreiro(a) vinculada a
uma trilha, com a produção declarada e situação inicial **entregue**. Criação original sem
trilha, sem Guerreiro(a) ou sem produção declarada SHALL ser recusada com **422**, indicando o
campo em falta. (`RF-01-26`)

#### Scenario: Entrega registrada com produção declarada

- **WHEN** chega uma criação original com trilha, Guerreiro(a) e produção
- **THEN** o núcleo grava o registro com situação "entregue" e autoria do Guerreiro(a)

#### Scenario: Entrega sem produção é recusada

- **WHEN** chega uma criação original sem a produção do Guerreiro(a)
- **THEN** o núcleo responde 422 indicando o campo em falta e nada é gravado

### Requirement: Mestre autor da trilha valida ou devolve a criação original entregue

O núcleo SHALL restringir a validação e a devolução da criação original ao **Mestre autor** da
trilha a que ela pertence, ou a um **Admin** — a mesma matriz de posse que já vale para trilha,
missão, atividade e resultado. Mestre que não é o autor SHALL receber **403**, e a situação SHALL
permanecer inalterada. (`RF-01-26`, `RF-01-16`)

#### Scenario: Mestre autor valida a entrega

- **WHEN** o Mestre autor da trilha valida uma criação original com situação "entregue"
- **THEN** o núcleo muda a situação para "validada"

#### Scenario: Mestre autor devolve a entrega

- **WHEN** o Mestre autor da trilha devolve uma criação original com situação "entregue"
- **THEN** o núcleo muda a situação para "devolvida"

#### Scenario: Mestre que não é o autor é recusado

- **WHEN** um Mestre que não é o autor da trilha tenta validar ou devolver a criação original
  dela
- **THEN** o núcleo responde 403 e a situação não muda

### Requirement: Autoria da criação original nunca se perde

A criação original SHALL manter o mesmo autor por toda a vida do registro, inclusive quando
devolvida para ajuste — devolver muda a situação, nunca o autor. (`RN-01-13`)

#### Scenario: Devolução preserva a autoria

- **WHEN** uma criação original entregue é devolvida
- **THEN** o registro continua com o mesmo autor original, sem reatribuição
