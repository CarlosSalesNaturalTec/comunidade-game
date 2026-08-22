## MODIFIED Requirements

### Requirement: A aplicação apresenta ao Mestre as trilhas dele, com a situação de cada uma

A App 09 SHALL apresentar ao Mestre em sessão as trilhas de que ele é autor, com nome, poder,
área do conhecimento e **situação** — rascunho, publicada ou despublicada —, e NEVER SHALL
apresentar-lhe o rascunho de outro Mestre. Na trilha despublicada, a aplicação SHALL
apresentar o **motivo** registrado pelo Admin, para que o autor saiba o que corrigir.
(`RF-09-04`, `RF-09-10`)

#### Scenario: O Mestre lê os próprios rascunhos

- **WHEN** um Mestre em sessão abre a lista das trilhas dele
- **THEN** a aplicação apresenta as trilhas de que ele é autor, rascunhos inclusive, com a
  situação de cada uma

#### Scenario: Rascunho alheio não aparece

- **WHEN** um Mestre em sessão abre a lista das trilhas dele e outro Mestre tem trilha em
  rascunho
- **THEN** a trilha do outro Mestre não aparece na lista

#### Scenario: O motivo da despublicação aparece ao autor

- **WHEN** um Mestre em sessão abre a lista e uma trilha dele está despublicada
- **THEN** a aplicação apresenta a situação despublicada e o motivo registrado pelo Admin

## ADDED Requirements

### Requirement: O Mestre declara a culminância da trilha

A App 09 SHALL oferecer ao Mestre autor, dentro da trilha, a declaração da **culminância** —
descrição da criação original esperada, modalidade individual ou em equipe, e critério de
validação. A aplicação SHALL apresentar a culminância já declarada e permitir substituí-la, e
NEVER SHALL oferecer a declaração em trilha de outro Mestre. (`RF-09-29`, `RF-09-30`)

#### Scenario: Mestre declara a culminância

- **WHEN** o Mestre autor preenche descrição, modalidade e critério e confirma
- **THEN** a aplicação grava a culminância no núcleo e passa a apresentá-la na trilha

#### Scenario: Campo obrigatório em falta

- **WHEN** o Mestre confirma sem o critério de validação
- **THEN** a aplicação apresenta a recusa em linguagem simples e nada é gravado

#### Scenario: A declaração substitui a culminância anterior

- **WHEN** o Mestre autor declara a culminância de uma trilha que já tem uma
- **THEN** a aplicação apresenta os novos valores no lugar dos anteriores

### Requirement: O Mestre publica a própria trilha e lê o que falta quando é recusado

A App 09 SHALL oferecer ao Mestre autor a **publicação** da própria trilha, em rascunho ou
despublicada, sem passar por aprovação. Recusada a publicação, a aplicação SHALL apresentar,
em linguagem simples e sem jargão, **exatamente o que falta** — a missão de sondagem, o
desafio de coleta, a culminância, ou mais de uma delas —, e NEVER SHALL apresentar código de
erro nem mensagem técnica. (`RF-09-05`, `RF-09-08`, `RF-09-12`, `RF-09-82`)

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
