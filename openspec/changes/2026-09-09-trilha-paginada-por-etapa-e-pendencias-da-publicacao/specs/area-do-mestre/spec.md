## MODIFIED Requirements

### Requirement: O Mestre acrescenta missões à trilha, ordenadas e declaradas

A App 09 SHALL permitir ao Mestre autor acrescentar missão à trilha informando **título**,
**posição** na sequência, **nível de dificuldade**, a declaração de **obrigatória ou opcional**
e a **etapa do ciclo** a que ela pertence. A aplicação SHALL apresentar as missões **paginadas
pelas quatro etapas do ciclo** — abertura, desenvolvimento, marcos e fechamento —, e dentro de
cada etapa na ordem da posição. Etapa sem missão SHALL permanecer visível, declarando que
ainda não tem missão. (`RF-09-02`, `RF-09-03`, `RF-09-80`)

#### Scenario: Mestre acrescenta missão

- **WHEN** o Mestre autor informa título, posição, dificuldade, obrigatoriedade e etapa do
  ciclo e confirma
- **THEN** a missão passa a existir naquela posição da trilha e a aplicação a apresenta na
  etapa que ele declarou

#### Scenario: As missões aparecem separadas pela etapa do ciclo

- **WHEN** o Mestre autor abre trilha cujas missões estão em etapas diferentes
- **THEN** a aplicação apresenta uma etapa por vez, e cada missão aparece apenas na etapa que
  ela declara

#### Scenario: Dentro da etapa vale a ordem da posição

- **WHEN** o Mestre autor abre uma etapa com mais de uma missão
- **THEN** a aplicação as apresenta na ordem crescente da posição

#### Scenario: Etapa sem missão continua visível

- **WHEN** o Mestre autor abre trilha em que nenhuma missão declara a etapa de fechamento
- **THEN** a aplicação apresenta a etapa de fechamento assim mesmo, declarando que ela ainda
  não tem missão

#### Scenario: A nova missão nasce na etapa que o Mestre está lendo

- **WHEN** o Mestre autor abre a etapa de marcos e pede uma nova missão
- **THEN** o formulário já traz marcos como etapa declarada, e o Mestre pode alterá-la antes
  de confirmar

#### Scenario: Declaração de obrigatoriedade em falta

- **WHEN** o Mestre confirma a missão sem declarar se ela é obrigatória ou opcional
- **THEN** a aplicação aponta a declaração em falta e nenhuma missão passa a existir

#### Scenario: Missão de trilha alheia é recusada

- **WHEN** um Mestre que não é o autor tenta acrescentar missão à trilha
- **THEN** a aplicação apresenta a recusa do núcleo e a trilha permanece como estava

### Requirement: O Mestre publica a própria trilha e lê o que falta quando é recusado

A App 09 SHALL oferecer ao Mestre autor a **publicação** da própria trilha, em rascunho ou
despublicada, sem passar por aprovação. Onde oferece a publicação, a aplicação SHALL
apresentar **permanentemente** quais das três travas ainda faltam — a **missão de sondagem**,
o **desafio de coleta de dados reais** e a **culminância** —, sem exigir que o Mestre tente
publicar primeiro, e SHALL acompanhar o que ele acabou de declarar. Esse painel NEVER SHALL
impedir a tentativa de publicar: quem recusa é o núcleo. Recusada a publicação, a aplicação
SHALL apresentar, em linguagem simples e sem jargão, **exatamente o que falta** — a missão de
sondagem, o desafio de coleta, a culminância, ou mais de uma delas —, e NEVER SHALL apresentar
código de erro nem mensagem técnica. (`RF-09-05`, `RF-09-06`, `RF-09-07`, `RF-09-08`,
`RF-09-12`, `RF-09-82`)

#### Scenario: O painel diz o que falta antes de qualquer tentativa

- **WHEN** o Mestre autor abre trilha em rascunho sem sondagem, sem desafio de coleta e sem
  culminância, e não tenta publicar
- **THEN** a aplicação já apresenta as três travas como pendentes

#### Scenario: O painel deixa de apontar a trava que acabou de ser declarada

- **WHEN** o Mestre autor declara a culminância da trilha
- **THEN** o painel deixa de apontar a culminância como pendente, sem que ele recarregue a
  tela

#### Scenario: O painel declara a trilha pronta para publicar

- **WHEN** o Mestre autor abre trilha em rascunho que atende às três travas
- **THEN** o painel declara que não falta nada para publicar

#### Scenario: O painel não impede a tentativa de publicar

- **WHEN** o Mestre autor publica trilha com trava pendente no painel
- **THEN** a aplicação leva o pedido ao núcleo e apresenta a recusa que ele devolve

#### Scenario: Trilha completa é publicada

- **WHEN** o Mestre autor publica trilha que atende às três travas
- **THEN** a aplicação apresenta a trilha como publicada

#### Scenario: A recusa diz em linguagem simples o que falta

- **WHEN** a publicação é recusada por faltar a culminância
- **THEN** a aplicação apresenta que falta a culminância, em linguagem simples

#### Scenario: A recusa lista todas as travas que faltam

- **WHEN** a publicação é recusada por faltarem as três travas
- **THEN** a aplicação apresenta as três, e não apenas uma

#### Scenario: O Mestre republica a trilha corrigida

- **WHEN** o Mestre autor corrige a trilha despublicada e publica de novo
- **THEN** a aplicação apresenta a trilha como publicada e deixa de apresentar o motivo

#### Scenario: A publicação não é oferecida em trilha alheia

- **WHEN** um Mestre abre uma trilha de que não é autor
- **THEN** a aplicação não oferece a ação de publicar

## ADDED Requirements

### Requirement: Os blocos da missão seguem a ordem em que o Mestre a escreve

A App 09 SHALL apresentar os blocos de declaração de cada missão nesta ordem: **template da
missão**, **conteúdo**, **bibliografia**, **cadência de retomada**, **atividades**, **desafio
de desbloqueio**, **recompensa pelo desbloqueio**, **desafios de coleta** e **ODS da missão**.
A **pré-visualização** da missão SHALL fechar o conjunto, depois de todos eles.

A ordem não cria, remove nem altera nenhuma declaração: ela arranja os blocos que
`RF-09-85`, `RF-09-14`, `RF-09-21`, `RF-09-83`, `RF-09-69`, `RF-09-26`, `RF-09-84`, `RF-09-27`
e `RF-09-98` já exigem, com a pré-visualização de `RF-09-25` fechando. A sequência é decisão do
fundador de 2026-09-09, registrada no recorte da fatia 17 do `openspec/cronograma-de-fatias.md`.

#### Scenario: A missão abre pelo template e fecha pela pré-visualização

- **WHEN** o Mestre autor abre uma missão da sua trilha
- **THEN** o primeiro bloco é o template da missão, o último é o ODS da missão, e a
  pré-visualização vem depois de todos

#### Scenario: A condição vem antes do que ela paga

- **WHEN** o Mestre autor percorre os blocos da missão
- **THEN** o desafio de desbloqueio aparece antes da recompensa pelo desbloqueio

#### Scenario: Conteúdo e bibliografia ficam juntos

- **WHEN** o Mestre autor percorre os blocos da missão
- **THEN** a bibliografia vem imediatamente depois do conteúdo
