## Purpose

A Criação Original é o registro de que um Guerreiro(a) entregou, ao final da trilha, algo
criado a partir do que aprendeu — a trava viva da regra "toda trilha termina em criação
original" (documento 99 §6 invariante 5), com autoria que nunca se perde.
## Requirements
### Requirement: Guerreiro(a) entrega a criação original contra uma trilha

O núcleo SHALL registrar a entrega de uma **criação original** da **equipe da trilha** a que ela
pertence, com a produção declarada e situação inicial **entregue**. A entrega SHALL ser feita por
um **integrante** daquela equipe, e vale pela equipe inteira. Criação original sem trilha, sem
equipe da trilha ou sem produção declarada SHALL ser recusada com **422**, indicando o campo em
falta. O núcleo SHALL aceitar **no máximo uma** criação original por equipe da trilha; como cada
Guerreiro(a) tem uma só equipe por trilha (`RN-01-44`), nenhum deles entrega duas criações
originais na mesma trilha. (`RF-01-26`, `RF-01-64`)

#### Scenario: Entrega registrada com produção declarada

- **WHEN** um integrante da equipe da trilha entrega uma criação original com produção
- **THEN** o núcleo grava o registro com situação "entregue", vinculado àquela equipe

#### Scenario: Entrega sem produção é recusada

- **WHEN** chega uma criação original sem a produção declarada
- **THEN** o núcleo responde 422 indicando o campo em falta e nada é gravado

#### Scenario: Entrega sem equipe da trilha é recusada

- **WHEN** chega uma criação original sem a equipe da trilha vinculada
- **THEN** o núcleo responde 422 indicando o campo em falta e nada é gravado

#### Scenario: Segunda entrega da mesma equipe é recusada

- **WHEN** um integrante entrega uma criação original numa trilha em que a equipe dele já entregou
- **THEN** o núcleo responde 422 e a entrega existente permanece

#### Scenario: Quem não é integrante não entrega pela equipe

- **WHEN** um Guerreiro(a) que não integra a equipe tenta entregar a criação original dela
- **THEN** o núcleo responde 403 e nada é gravado

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

A criação original SHALL manter a mesma **equipe da trilha** e os mesmos **integrantes**, cada um
com o papel que teve, por toda a vida do registro, inclusive quando devolvida para ajuste —
devolver muda a situação, nunca a autoria. Como a composição fica fixa na homologação
(`RN-01-44`), a autoria creditada é a que estava registrada naquele momento. (`RN-01-13`,
`RF-01-64`)

#### Scenario: Devolução preserva a autoria

- **WHEN** uma criação original entregue é devolvida
- **THEN** o registro continua com a mesma equipe e os mesmos integrantes, sem reatribuição

#### Scenario: A autoria é a composição homologada

- **WHEN** se lê a autoria de uma criação original
- **THEN** ela traz cada integrante da equipe homologada, com o papel de cada um

