## ADDED Requirements

### Requirement: A missão declara título, etapa do ciclo e cadência de retomada

O núcleo SHALL manter, em cada missão, o **título** declarado pelo Mestre autor, a **etapa do
ciclo** a que ela pertence — abertura, desenvolvimento, marcos ou fechamento — e a **cadência
de retomada**, que SHALL ser opcional: missão sem retomada declarada é válida. Missão sem
título SHALL ser recusada com **422**. A etapa do ciclo SHALL ser fechada nos quatro valores do
documento 11 §2.4; a cadência é declarada pelo Mestre e NEVER SHALL ser imposta pelo núcleo.
(`RF-09-02`, `RF-09-03`, `RF-09-83`, `RF-09-101`, PRD-09 §8, 11 §§2.2, 2.4)

#### Scenario: Missão criada com título e etapa

- **WHEN** o Mestre autor cria uma missão informando título e a etapa do ciclo dela
- **THEN** o núcleo grava os dois na missão

#### Scenario: Missão sem título é recusada

- **WHEN** chega uma missão sem título
- **THEN** o núcleo responde 422 indicando o campo em falta e nada é gravado

#### Scenario: Etapa fora dos quatro valores é recusada

- **WHEN** chega uma missão cuja etapa do ciclo não é abertura, desenvolvimento, marcos nem
  fechamento
- **THEN** o núcleo responde 422 e nada é gravado

#### Scenario: Missão sem retomada é aceita

- **WHEN** o Mestre autor cria uma missão sem declarar cadência de retomada
- **THEN** o núcleo a aceita, e a missão fica sem retomada declarada

#### Scenario: A cadência declarada depois substitui a anterior

- **WHEN** o Mestre autor declara a cadência de retomada de uma missão que já tinha uma
- **THEN** o núcleo grava a nova cadência no lugar da anterior

### Requirement: O Mestre alcança a própria autoria por porta HTTP

O núcleo SHALL expor a criação de trilha, a de missão e a declaração da cadência de retomada a
**persona em sessão**, aplicando as mesmas recusas da regra: poder obrigatório e de natureza de
Guerreiro(a), posse do Mestre autor, sondagem única e na primeira posição, e declaração de
obrigatória ou opcional. A escrita por Mestre que não é o autor SHALL responder **403**;
chamada sem persona em sessão SHALL ser recusada. (`RF-09-01`, `RF-09-02`, `RF-09-81`,
`RF-01-16`, PRD-09 §9)

#### Scenario: Mestre cria a trilha pela porta

- **WHEN** um Mestre em sessão envia nome, objetivo, área do conhecimento e um poder de
  Guerreiro(a)
- **THEN** o núcleo grava a trilha em rascunho, com ele como autor, e a devolve

#### Scenario: Trilha em poder que não é de Guerreiro(a) é recusada

- **WHEN** chega uma trilha vinculada ao Poder Sustentador
- **THEN** o núcleo responde 422 e nada é gravado

#### Scenario: Missão em trilha alheia é recusada

- **WHEN** um Mestre que não é o autor envia missão para a trilha
- **THEN** o núcleo responde 403 e a trilha permanece como estava

#### Scenario: Chamada sem persona em sessão é recusada

- **WHEN** a criação de trilha é chamada sem credencial de persona
- **THEN** o núcleo recusa a chamada e nenhuma trilha é gravada

### Requirement: O Mestre lê as próprias trilhas, rascunhos inclusive

O núcleo SHALL expor ao Mestre em sessão as trilhas de que ele é **autor**, com a situação de
cada uma, incluindo as em rascunho. A leitura NEVER SHALL trazer rascunho de outro Mestre e
NEVER SHALL exigir filtro por comunidade, porque a trilha é bem comum da plataforma.
(`RF-09-04`, `RN-01-42`, PRD-09 §9)

#### Scenario: O Mestre lê os próprios rascunhos

- **WHEN** um Mestre em sessão consulta as trilhas dele
- **THEN** o núcleo devolve as trilhas de que ele é autor, rascunhos inclusive, com a situação
  de cada uma

#### Scenario: Rascunho de outro Mestre não sai na leitura

- **WHEN** um Mestre em sessão consulta as trilhas dele e outro Mestre tem trilha em rascunho
- **THEN** a trilha do outro Mestre não é devolvida

#### Scenario: A leitura não exige comunidade

- **WHEN** a consulta chega sem parâmetro de comunidade
- **THEN** o núcleo responde normalmente, sem exigir o filtro
