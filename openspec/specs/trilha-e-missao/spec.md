## Purpose

A trilha é a unidade de organização do aprendizado e a missão é a menor unidade de progressão
dentro dela. Esta capacidade cobre a trilha de autoria de um Mestre e vinculada a um poder, a sua
natureza de bem comum da plataforma, as missões ordenadas com dificuldade declarada, a distinção
entre obrigatória e opcional e a missão de sondagem que abre toda trilha.

## Requirements

### Requirement: A trilha pertence a um poder e a um Mestre autor

O núcleo SHALL manter a trilha com nome, objetivo, área do conhecimento, o **poder** a que se
vincula e o **Mestre autor**. O poder SHALL ser obrigatório e SHALL vir do catálogo. Toda escrita
SHALL gravar autoria, data e hora. (`RF-01-20`, `RF-01-03`, PRD-01 §8, 02 §3, 11 §2.1)

#### Scenario: Trilha criada com poder e autor

- **WHEN** um Mestre em sessão cria uma trilha com nome, objetivo, área do conhecimento e um
  poder do catálogo
- **THEN** o núcleo grava a trilha com aquele Mestre como autor, com data e hora com fuso

#### Scenario: Trilha sem poder é recusada

- **WHEN** chega uma trilha sem poder vinculado
- **THEN** o núcleo responde 422 indicando o campo em falta e nada é gravado

### Requirement: A trilha é bem comum da plataforma

O núcleo NEVER SHALL vincular a trilha a uma Comunidade Virtual. A consulta de trilha NEVER SHALL
exigir filtro por comunidade nem restringir o resultado por ela: publicada, a trilha alcança todas
as comunidades. O filtro por comunidade de `RF-01-18` SHALL recair sobre o **percurso do
Guerreiro(a)**, nunca sobre a trilha. (`RN-01-42`, `RF-01-18`, 02 §3)

#### Scenario: Consulta de trilha sem informar comunidade

- **WHEN** chega uma consulta de trilhas sem parâmetro de comunidade
- **THEN** o núcleo responde normalmente, sem exigir o filtro e sem recusar por 422

#### Scenario: A mesma trilha alcança comunidades diferentes

- **WHEN** personas vinculadas a Comunidades Virtuais diferentes consultam as trilhas publicadas
- **THEN** as duas enxergam a mesma trilha publicada

#### Scenario: Não há comunidade na trilha

- **WHEN** se procura no núcleo um vínculo de comunidade na entidade trilha
- **THEN** nenhum existe: a comunidade é atributo do Guerreiro(a) e do percurso dele

### Requirement: Só o Mestre autor escreve na sua trilha

O núcleo SHALL restringir a escrita de uma trilha, das missões dela e das atividades dela ao
**Mestre autor** da trilha e a **Admin**. Mestre que não é o autor SHALL receber **403**, ainda
que o papel dele permita escrever trilhas em geral. A leitura de trilha publicada SHALL seguir a
regra da capacidade, não a autoria. (`RF-01-16`, PRD-01 §4)

#### Scenario: Mestre autor altera a sua trilha

- **WHEN** o Mestre autor de uma trilha altera a trilha ou uma missão dela
- **THEN** o núcleo executa a alteração e grava a autoria

#### Scenario: Outro Mestre é recusado

- **WHEN** um Mestre que não é o autor tenta alterar a trilha
- **THEN** o núcleo responde 403 e a trilha permanece como estava

#### Scenario: Admin alcança qualquer trilha

- **WHEN** um Admin altera uma trilha de que não é autor
- **THEN** o núcleo executa a alteração, porque a matriz do PRD-01 §4 dá tudo ao Admin

### Requirement: A trilha tem situação de rascunho ou publicada

O núcleo SHALL manter a situação da trilha entre **rascunho** e **publicada**. A trilha em
rascunho SHALL ser visível apenas ao Mestre autor e a Admin, e NEVER SHALL aparecer em consulta
pública. A transição entre as duas situações, as travas conferidas na publicação e a
despublicação são do PRD-09 — aqui nasce a situação, não o fluxo que a muda. (`RF-01-20`,
`RF-09-04`, PRD-01 §8)

#### Scenario: Rascunho não aparece a quem não é o autor

- **WHEN** uma persona que não é o Mestre autor nem Admin consulta as trilhas
- **THEN** as trilhas em rascunho não aparecem no resultado

#### Scenario: O Mestre autor vê o próprio rascunho

- **WHEN** o Mestre autor consulta as suas trilhas
- **THEN** as trilhas dele em rascunho aparecem no resultado

### Requirement: A missão é ordenada dentro da trilha e declara dificuldade

O núcleo SHALL manter a missão pertencente a **exatamente uma** trilha, com **posição** na
sequência e **nível de dificuldade** declarado pelo Mestre autor. A dificuldade NEVER SHALL
derivar da idade do Guerreiro(a): a progressão é por dificuldade, e a faixa de 6 a 16 anos não
entra no cálculo. (`RF-01-20`, documento 99 §6 invariante 2, 02 §3, 11 §2.2)

#### Scenario: Missão criada com posição e dificuldade

- **WHEN** o Mestre autor cria uma missão informando a trilha, a posição e a dificuldade
- **THEN** o núcleo grava a missão naquela posição da sequência

#### Scenario: Missão sem trilha é recusada

- **WHEN** chega uma missão sem trilha
- **THEN** o núcleo responde 422 indicando o campo em falta e nada é gravado

#### Scenario: A idade não determina a dificuldade

- **WHEN** se procura no núcleo um caminho que derive a dificuldade da missão da idade do
  Guerreiro(a)
- **THEN** nenhum existe: a dificuldade é declarada pelo Mestre autor e nada mais

### Requirement: A missão é declarada obrigatória ou opcional

O núcleo SHALL exigir, em cada missão, a declaração de **obrigatória** ou **opcional**. A
distinção SHALL ficar disponível para o percurso do nível, em que só a obrigatória entra no
denominador; a conta dos níveis é de outra fatia, e aqui nasce o dado de que ela depende.
(`RF-01-20`, documento 99 §6 invariante 18, 02 §3, 11 §§2.2, 6)

#### Scenario: Missão declarada obrigatória

- **WHEN** o Mestre autor declara uma missão como obrigatória
- **THEN** o núcleo grava a declaração e a missão fica distinguível das opcionais

#### Scenario: Missão sem a declaração é recusada

- **WHEN** chega uma missão sem a declaração de obrigatória ou opcional
- **THEN** o núcleo responde 422 indicando o campo em falta e nada é gravado

### Requirement: A trilha abre com uma missão de sondagem

O núcleo SHALL aceitar **no máximo uma** missão de sondagem por trilha, e ela SHALL ocupar a
**primeira posição** da sequência. A sondagem mede de onde a turma parte e NEVER SHALL definir
nível. A recusa de **publicar** trilha sem sondagem é `RF-09-82`, da aplicação que publica: uma
trilha em rascunho SHALL poder existir sem ela. (`RF-01-20`, documento 99 §6 invariante 5, 02 §3,
11 §2.2)

#### Scenario: Sondagem na primeira posição

- **WHEN** o Mestre autor marca como sondagem a missão que ocupa a primeira posição da trilha
- **THEN** o núcleo aceita a marcação

#### Scenario: Segunda sondagem na mesma trilha é recusada

- **WHEN** o Mestre autor marca como sondagem uma segunda missão da mesma trilha
- **THEN** o núcleo responde 422 e a sondagem existente permanece

#### Scenario: Sondagem fora da primeira posição é recusada

- **WHEN** o Mestre autor marca como sondagem uma missão que não ocupa a primeira posição
- **THEN** o núcleo responde 422 e nada é gravado

#### Scenario: Rascunho existe sem sondagem

- **WHEN** o Mestre autor cria uma trilha em rascunho e ainda não declarou a missão de sondagem
- **THEN** o núcleo aceita a trilha, porque a trava é conferida na publicação
