## ADDED Requirements

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
