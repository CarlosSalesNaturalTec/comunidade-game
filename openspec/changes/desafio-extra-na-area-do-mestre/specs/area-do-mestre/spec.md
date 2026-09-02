## ADDED Requirements

### Requirement: A App 09 mostra ao Mestre autor os desafios extras a validar

A App 09 SHALL apresentar ao Mestre em sessão os desafios extras **em validação** propostos
para as trilhas de que ele é **autor**, cada um com a **trilha**, a **missão** quando houver, a
**modalidade**, a **recompensa e a quantidade**, o **critério de atribuição**, os **pontos
extras**, o **formato**, o **custeio** e a **vigência**. Desafio de trilha de outro Mestre NEVER
SHALL aparecer nesta lista. A tela NEVER SHALL identificar Guerreiro(a): do direcionado exibe o
**nick como o proponente o digitou**, e nada mais. (`RF-09-51`, `RN-09-11`, `RN-14-20`)

#### Scenario: A lista traz o que espera validação

- **WHEN** o Mestre autor abre a área de desafios extras
- **THEN** vê os desafios em validação das suas trilhas, com a recompensa, a quantidade, o
  critério, os pontos extras, o formato, o custeio e a vigência

#### Scenario: Desafio de trilha alheia não aparece

- **WHEN** o Mestre abre a área de desafios extras
- **THEN** nenhum desafio de trilha de que ele não é autor é listado

#### Scenario: O direcionado não identifica ninguém

- **WHEN** a lista traz um desafio direcionado
- **THEN** a tela exibe o nick como o proponente o digitou e nenhum outro dado do destinatário

### Requirement: O Mestre valida o desafio extra com parecer, ou recusa com motivo

A App 09 SHALL permitir ao Mestre autor **validar** um desafio extra da sua trilha escrevendo o
**parecer**, ou **recusá-lo** escrevendo o **motivo**. A tela SHALL exigir o texto em cada um
dos dois atos e SHALL dizer, em linguagem simples, que o validado **segue para a aprovação do
Admin** e que o recusado **não chega a ela**. Tratado o desafio, ele SHALL sair da lista do que
há por validar. (`RF-09-51`, `RF-09-52`, `RN-09-11`)

#### Scenario: Validar com parecer manda ao Admin

- **WHEN** o Mestre autor valida um desafio escrevendo o parecer
- **THEN** o desafio sai da lista e a tela informa que ele segue para a aprovação do Admin

#### Scenario: Recusar sem motivo não passa

- **WHEN** o Mestre autor tenta recusar um desafio sem escrever o motivo
- **THEN** a tela recusa o envio e diz que o motivo é exigido

#### Scenario: O recusado não segue para o Admin

- **WHEN** o Mestre autor recusa um desafio com motivo
- **THEN** o desafio sai da lista e a tela informa que ele não chega à aprovação do Admin

### Requirement: O Mestre propõe desafio extra pela App 09

A App 09 SHALL permitir ao Mestre propor um desafio extra vinculado a uma **trilha em
andamento**, presencial ou on-line, declarando a **recompensa**, a **quantidade**, o
**critério de atribuição**, os **pontos extras**, a **vigência** e o **custeio** — **absorção
dele** ou **saldo de recurso já existente** na plataforma. O formulário SHALL recusar pontos
extras acima de **10** dizendo o teto, e no **direcionado** SHALL exigir o **nick do
destinatário** e a **justificativa pedagógica**. A tela NEVER SHALL revelar se o nick existe.
(`RF-09-105`, `RF-09-106`, `RF-09-107`, `RF-09-111`, `RN-09-40`)

#### Scenario: A proposta completa é enviada

- **WHEN** o Mestre preenche a proposta com recompensa, quantidade, critério, pontos extras,
  formato, custeio e vigência, sobre uma trilha em andamento
- **THEN** a proposta é registrada e passa a constar entre as que ele propôs

#### Scenario: Acima de 10 pontos o formulário recusa

- **WHEN** o Mestre declara 11 pontos extras
- **THEN** a tela recusa o envio dizendo que o teto é de 10 pontos

#### Scenario: O direcionado exige a justificativa pedagógica

- **WHEN** o Mestre marca a proposta como direcionada e informa o nick sem a justificativa
  pedagógica
- **THEN** a tela recusa o envio e diz que a justificativa é exigida

#### Scenario: A tela não confirma o nick

- **WHEN** o Mestre envia uma proposta direcionada a um nick qualquer
- **THEN** a proposta é registrada e a tela em momento algum diz se aquele nick existe

### Requirement: A App 09 diz ao Mestre autor que a validação pedagógica foi dispensada

A App 09 SHALL informar ao Mestre, ao propor desafio extra à **trilha de que ele é autor**, que
a **validação pedagógica é dispensada** e que a proposta segue **direto para a aprovação do
Admin**; e, ao propor à trilha de **outro Mestre**, que ela passa antes pela **validação do
Mestre autor** daquela trilha. Em nenhum dos dois casos a tela SHALL sugerir que a **aprovação
do Admin** é dispensada. (`RF-09-108`, `RF-09-109`, `RF-09-110`, `RN-09-41`)

#### Scenario: Na trilha própria a tela anuncia a dispensa

- **WHEN** o Mestre propõe um desafio à trilha de que é autor
- **THEN** a tela informa que a validação pedagógica é dispensada e que a proposta vai à
  aprovação do Admin

#### Scenario: Na trilha alheia a tela anuncia a validação

- **WHEN** o Mestre propõe um desafio à trilha de outro Mestre
- **THEN** a tela informa que a proposta passa antes pela validação do Mestre autor daquela
  trilha

### Requirement: O Mestre acompanha os desafios extras que propôs

A App 09 SHALL listar ao Mestre os desafios extras que ele mesmo **propôs**, cada um com a
**situação** — em validação do Mestre, em aprovação do Admin, publicado ou recusado —, o
**motivo da recusa** quando houver e a **quantidade restante** quando publicado. A lista NEVER
SHALL trazer desafio proposto por outra persona, e NEVER SHALL identificar Guerreiro(a).
(`RF-09-105`, `RF-09-112`, `RN-14-20`)

#### Scenario: A lista mostra a situação de cada proposta

- **WHEN** o Mestre abre a lista do que propôs
- **THEN** vê cada desafio com a situação em que está

#### Scenario: A recusa aparece com o motivo

- **WHEN** um desafio que o Mestre propôs foi recusado
- **THEN** a lista o traz como recusado, com o motivo registrado

#### Scenario: O publicado mostra quanto resta

- **WHEN** um desafio que o Mestre propôs está publicado
- **THEN** a lista traz a quantidade de recompensas restante
