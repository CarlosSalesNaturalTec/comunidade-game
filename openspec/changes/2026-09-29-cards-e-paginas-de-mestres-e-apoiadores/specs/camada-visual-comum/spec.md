# Spec Delta

## ADDED Requirements

### Requirement: A carta tem a variante Mestre, com a prova da habilidade

A camada comum SHALL entregar a variante **Mestre** da carta, com o que o documento 11 §8.2
atribui a ela: **avatar**, **nick**, **áreas de habilidade**, **artefatos comprobatórios**,
**trilhas de autoria** e o **selo de quem sustentou atividade sem recurso**. A variante SHALL
apresentar a prova como **link declarado**, cada um com o rótulo do que aponta — currículo,
portfólio, rede social ou documento externo —, que é a única forma da prova no Ciclo 01.

Não havendo nick, a variante SHALL apresentar o **nome** do Mestre, e NEVER SHALL apresentar
nome como se fosse nick (decisão do fundador, 2026-09-29). Faltando avatar, a variante SHALL
usar o **avatar padrão do projeto**, na mesma moldura (documento 15 §7.3).

A variante SHALL seguir a regra já vigente da carta pela metade: leitura que não devolve o que
a tabela do documento 11 §8.2 exige dela SHALL ser apresentada em outra forma, não em carta
incompleta. (`RF-03-02`, `RF-03-07`, documento 11 §8.2)

#### Scenario: A carta do Mestre traz os seis campos da variante

- **WHEN** a carta de um Mestre é apresentada
- **THEN** ela traz avatar, nick, áreas de habilidade, artefatos comprobatórios, trilhas de
  autoria e o selo de quem sustentou atividade sem recurso

#### Scenario: Sem nick, a carta apresenta o nome

- **WHEN** a carta de um Mestre que ainda não definiu nick é apresentada
- **THEN** ela traz o nome dele, apresentado como nome, e não no lugar reservado ao nick

#### Scenario: Sem avatar, entra o avatar padrão

- **WHEN** a carta de um Mestre sem avatar gravado é apresentada
- **THEN** ela traz o avatar padrão do projeto, na mesma moldura

#### Scenario: A prova do Mestre é link com rótulo

- **WHEN** a carta de um Mestre com três artefatos comprobatórios é apresentada
- **THEN** cada artefato aparece como link com o rótulo do que aponta, e nenhum anexo de
  arquivo é apresentado

#### Scenario: Mestre sem os campos da variante não vira carta incompleta

- **WHEN** a leitura de um Mestre não devolve o que a tabela do documento 11 §8.2 exige da
  variante
- **THEN** a tela apresenta o Mestre em outra forma, e nenhuma carta incompleta é apresentada

### Requirement: A carta tem a variante Apoiador, na moldura comum e com o total em moedas

A camada comum SHALL entregar a variante **Apoiador** da carta, com o que o documento 11 §8.2
atribui a ela: **avatar**, **nick** e o **total de moedas em destaque**, o **nível de
sustento**, os **selos**, os **desafios propostos** e a **efetividade agregada**.

A variante SHALL seguir a **identidade visual comum** do documento 11 §8.2: moldura comum,
avatar **centralizado em proporção fixa**, nick abaixo e o total de moedas em destaque, de modo
que a marca maior não domine a página. Avatares de Apoiador são logomarcas e imagens de origens
diferentes, e a variante NEVER SHALL variar a moldura de um para outro.

A variante NEVER SHALL exibir valor em reais nem dado de contato de Guerreiro(a). Abaixo do
piso de **10 moedas acumuladas** a variante SHALL usar o **avatar padrão do projeto**, na mesma
moldura, com o mesmo nick e o mesmo total em moedas e **nenhuma outra marca de diferença**.
Não havendo nick, a variante SHALL apresentar o **nome** do Apoiador, como nome (decisão do
fundador, 2026-09-29).

A variante SHALL seguir a regra já vigente da carta pela metade. (`RF-03-02`, `RF-03-10`,
`RF-03-55`, `RF-03-56`, `RF-03-66`, `RN-03-18`, `RN-03-26`, documentos 11 §8.2 e 15 §7.3)

#### Scenario: A carta do Apoiador traz o total em destaque na moldura comum

- **WHEN** a carta de um Apoiador é apresentada
- **THEN** ela traz avatar centralizado em proporção fixa, nick abaixo e o total de moedas em
  destaque, na mesma moldura de todas as cartas de Apoiador

#### Scenario: Nenhuma carta de Apoiador traz reais

- **WHEN** a carta de um Apoiador cujo aporte foi registrado em reais é apresentada
- **THEN** ela traz apenas o total em moedas, e nenhum valor em reais

#### Scenario: Abaixo do piso entra o avatar padrão, sem outra marca de diferença

- **WHEN** a carta de um Apoiador com menos de 10 moedas acumuladas é apresentada
- **THEN** ela traz o avatar padrão do projeto, na mesma moldura, com o nick e o total em
  moedas, e nenhuma outra diferença em relação às demais cartas

#### Scenario: A marca maior não domina a coleção

- **WHEN** duas cartas de Apoiador com logomarcas de proporções diferentes são apresentadas
  lado a lado
- **THEN** as duas ocupam a mesma moldura, com o avatar na mesma proporção fixa

#### Scenario: A efetividade na carta não alcança quem concluiu

- **WHEN** a carta de um Apoiador apresenta os desafios propostos com a efetividade deles
- **THEN** aparecem trilha, período e quantos concluíram, e nenhum nick, avatar ou dado de
  quem concluiu
