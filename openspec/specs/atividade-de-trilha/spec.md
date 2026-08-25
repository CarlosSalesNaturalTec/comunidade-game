## Purpose

A atividade é o que o Guerreiro(a) realiza para aprender, e é dela que nascem a realização e, mais
tarde, o ponto. Esta capacidade cobre a atividade sempre pertencente a uma missão, a classificação
nos três eixos ortogonais do documento 11 §4 e a exigência de que toda atividade peça produção do
Guerreiro(a).

## Requirements

### Requirement: Toda atividade de trilha pertence a uma missão

O núcleo SHALL manter a atividade de trilha pertencente a **exatamente uma** missão. Atividade sem
missão SHALL ser recusada com **422**. A escrita SHALL ser restrita ao **Mestre autor** da trilha
a que a missão pertence e a **Admin**, como vale para a trilha e para a missão; outro Mestre SHALL
receber **403**. A atividade **avulsa, fora de trilha**, é cadastro da gestão e não é desta
capacidade. (`RF-01-20`, `RF-01-16`, `RF-01-03`, PRD-01 §4, 11 §4)

#### Scenario: Atividade criada dentro de uma missão

- **WHEN** o Mestre autor cria uma atividade informando a missão a que ela pertence
- **THEN** o núcleo grava a atividade naquela missão, com autoria, data e hora com fuso

#### Scenario: Atividade sem missão é recusada

- **WHEN** chega uma atividade de trilha sem missão
- **THEN** o núcleo responde 422 indicando o campo em falta e nada é gravado

#### Scenario: Mestre que não é o autor é recusado

- **WHEN** um Mestre que não é o autor da trilha tenta criar atividade em uma missão dela
- **THEN** o núcleo responde 403 e nada é gravado

### Requirement: A atividade é classificada nos três eixos

O núcleo SHALL exigir, em cada atividade, os três eixos do documento 11 §4: **modalidade**
(individual, em equipe, em equipe com familiar), **formato** (presencial, on-line ou assíncrona) e
**natureza**. Os três eixos SHALL ser **ortogonais** — qualquer combinação entre eles é válida. A
**natureza** SHALL ser lista aberta, porque trilhas de outras áreas acrescentam naturezas novas;
modalidade e formato SHALL ser fechados nos valores acima. Atividade sem modalidade ou sem formato
SHALL ser recusada com **422**. (`RF-01-20`, `RF-09-70`, 11 §4)

#### Scenario: Os eixos se combinam livremente

- **WHEN** o Mestre autor cria uma atividade em equipe, presencial e de construção
- **THEN** o núcleo aceita a combinação dos três eixos

#### Scenario: Atividade sem modalidade é recusada

- **WHEN** chega uma atividade sem modalidade declarada
- **THEN** o núcleo responde 422 indicando o campo em falta e nada é gravado

#### Scenario: Atividade sem formato é recusada

- **WHEN** chega uma atividade sem formato declarado
- **THEN** o núcleo responde 422 indicando o campo em falta e nada é gravado

#### Scenario: Natureza nova é aceita

- **WHEN** o Mestre autor cria uma atividade cuja natureza não está entre as do Ciclo 01
- **THEN** o núcleo a aceita, porque a natureza é lista aberta

#### Scenario: Modalidade fora dos valores previstos é recusada

- **WHEN** chega uma atividade com modalidade que não é individual, em equipe nem em equipe com
  familiar
- **THEN** o núcleo responde 422 e nada é gravado

### Requirement: Toda atividade exige produção do Guerreiro(a)

O núcleo SHALL exigir, em cada atividade, a declaração do que o Guerreiro(a) **produz** —
escrever, falar ou construir. Atividade sem produção declarada SHALL ser recusada com **422**:
consumir conteúdo não conclui missão. Quem lança o resultado da produção é o Mestre, e a leitura
automática dela é hipótese, nunca veredito — o resultado é de outra fatia. (`RF-01-20`,
documento 99 §6 invariante 19, 02 §4, 11 §2.2)

#### Scenario: Atividade com produção declarada

- **WHEN** o Mestre autor cria uma atividade declarando o que o Guerreiro(a) produz
- **THEN** o núcleo grava a atividade

#### Scenario: Atividade sem produção é recusada

- **WHEN** chega uma atividade sem a declaração de produção
- **THEN** o núcleo responde 422 indicando o campo em falta e nada é gravado

### Requirement: A atividade declara título e descrição

O núcleo SHALL manter, em cada atividade de trilha, o **título** e a **descrição** declarados
pelo Mestre autor. Atividade sem título SHALL ser recusada com **422**; a descrição SHALL ser
opcional, porque o título e a **produção esperada** já dizem o que a atividade é. O título
NEVER SHALL ser deduzido da missão nem da posição. (`RF-09-69`, PRD-09 §8)

#### Scenario: Atividade criada com título e descrição

- **WHEN** o Mestre autor cria uma atividade informando título e descrição
- **THEN** o núcleo grava os dois na atividade

#### Scenario: Atividade sem título é recusada

- **WHEN** chega uma atividade sem título
- **THEN** o núcleo responde 422 indicando o campo em falta e nada é gravado

#### Scenario: Atividade sem descrição é aceita

- **WHEN** o Mestre autor cria uma atividade com título e sem descrição
- **THEN** o núcleo a aceita, porque a descrição é opcional

### Requirement: O Mestre cria a atividade da missão por porta HTTP

O núcleo SHALL expor a criação de atividade dentro de uma missão a **persona em sessão**,
aplicando as recusas que a regra já tem: missão obrigatória, modalidade e formato obrigatórios
e fechados nos valores do documento 11 §4, natureza em lista aberta e produção esperada
obrigatória. A criação por Mestre que não é o autor da trilha a que a missão pertence SHALL
responder **403**. (`RF-09-69`, `RF-09-70`, `RF-01-16`, PRD-09 §9)

#### Scenario: Mestre autor cria a atividade pela porta

- **WHEN** o Mestre autor envia título, modalidade, formato, natureza e produção esperada para
  uma missão da trilha dele
- **THEN** o núcleo grava a atividade naquela missão e a devolve

#### Scenario: Atividade sem formato é recusada

- **WHEN** chega uma atividade sem formato declarado
- **THEN** o núcleo responde 422 indicando o campo em falta e nada é gravado

#### Scenario: Atividade em missão de trilha alheia é recusada

- **WHEN** um Mestre que não é o autor da trilha envia atividade para uma missão dela
- **THEN** o núcleo responde 403 e nada é gravado

#### Scenario: Chamada sem persona em sessão é recusada

- **WHEN** a criação de atividade é chamada sem credencial de persona
- **THEN** o núcleo recusa a chamada e nenhuma atividade é gravada

### Requirement: A atividade presencial declara a aula em que acontece

O núcleo SHALL aceitar, em cada **atividade**, a **aula** em que ela acontece — o vínculo que
transforma a atividade avulsa em **programação de um encontro** (documento 05 §4). O vínculo
SHALL ser **opcional**: atividade sem aula declarada segue válida, e é o caso de tudo o que
corre entre encontros.

Só atividade de **formato presencial** SHALL declarar aula; atividade **on-line** ou
**assíncrona** que declare uma SHALL ser recusada com **422**. É o que torna concreto o
"presenciais **do encontro**" contra "on-line **entre** encontros" que o `RF-09-73` já pedia.

Quem declara é o **Mestre autor** da trilha a que a missão da atividade pertence, ou um
**Admin** — a mesma matriz de posse que já vale para a trilha, a missão e a atividade
(`RF-01-16`). Mestre que não é o autor SHALL receber **403**. Aula inexistente SHALL ser
recusada com **422**. (`RF-09-69`, `RF-09-73`, `RF-04-35`, `RF-01-16`, documento 05 §4)

#### Scenario: O Mestre autor declara a aula da sua atividade presencial

- **WHEN** o Mestre autor envia uma atividade de formato presencial declarando a aula em que
  ela acontece
- **THEN** o núcleo grava a atividade com a aula declarada e a devolve

#### Scenario: Atividade sem aula declarada segue válida

- **WHEN** o Mestre autor envia uma atividade sem declarar aula alguma
- **THEN** o núcleo grava a atividade sem vínculo com encontro algum

#### Scenario: Atividade on-line que declara aula é recusada

- **WHEN** chega uma atividade de formato on-line declarando uma aula
- **THEN** o núcleo responde 422 indicando o campo e nada é gravado

#### Scenario: Atividade assíncrona que declara aula é recusada

- **WHEN** chega uma atividade de formato assíncrono declarando uma aula
- **THEN** o núcleo responde 422 indicando o campo e nada é gravado

#### Scenario: Mestre que não é o autor não declara a aula

- **WHEN** um Mestre que não é o autor da trilha tenta declarar a aula de uma atividade dela
- **THEN** o núcleo responde 403 e a atividade não muda

#### Scenario: Aula inexistente é recusada

- **WHEN** chega uma atividade declarando uma aula que não existe
- **THEN** o núcleo responde 422 e nada é gravado
