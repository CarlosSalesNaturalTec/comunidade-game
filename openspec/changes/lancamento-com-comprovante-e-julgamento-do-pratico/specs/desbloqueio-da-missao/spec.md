# Spec Delta

## ADDED Requirements

### Requirement: O julgamento no lançamento recai sobre a declaração que aguarda o Mestre

Quando o Guerreiro(a) tem declaração do prático **aguardando o Mestre**, o julgamento trazido
no lançamento da atividade SHALL recair **sobre ela**, com a comprovação que o Guerreiro(a)
entregou, pelas mesmas regras do julgamento na bancada. O comprovante do Resultado NEVER SHALL
substituir a comprovação já entregue. (`RF-09-150`, `RN-09-66`, `RF-09-117`, `RN-09-52` a
`RN-09-55`)

#### Scenario: A declaração pendente é julgada no lançamento

- **WHEN** o Guerreiro(a) entregou o prático em vídeo e o Mestre autor lança a atividade com o
  julgamento de que cumpriu e é publicável
- **THEN** a declaração do Guerreiro(a) é julgada com o vídeo dele, e o Resultado guarda o
  comprovante do lançamento à parte

#### Scenario: A entrega presencial pendente é julgada no lançamento

- **WHEN** o Guerreiro(a) escolheu entregar no encontro e o Mestre autor lança a atividade com o
  julgamento de que cumpriu
- **THEN** a declaração é julgada como cumprida, sem publicável e sem exigir motivo

### Requirement: O Mestre autor declara o prático em nome do Guerreiro(a) no lançamento

Sem declaração do Guerreiro(a), ou com declaração julgada que **não cumpriu**, o lançamento com
julgamento SHALL gravar a declaração **em nome do Guerreiro(a)**, com o **comprovante do
Resultado** como comprovação, e julgá-la no mesmo ato; a recusada SHALL ser **reaberta**, sem
segundo registro. Comprovante em forma **diferente** da aceita SHALL ser recusado com **422**,
nomeando a esperada. Vale a exigência de inscrição. (`RF-09-150`, `RN-09-66`, `RN-09-54`)

#### Scenario: Sem declaração, o Mestre declara e julga com o comprovante

- **WHEN** o prático aceita imagem, o Guerreiro(a) não declarou, e o Mestre autor lança a
  atividade com foto e o julgamento de que cumpriu e é publicável
- **THEN** nasce a declaração com a foto como comprovação, julgada cumprida e publicável, e a
  missão seguinte se abre

#### Scenario: A declaração recusada é reaberta pelo lançamento

- **WHEN** o prático do Guerreiro(a) foi julgado que não cumpriu e o Mestre autor lança a
  atividade com o comprovante e um novo julgamento
- **THEN** a mesma declaração recebe o comprovante e o novo veredito, sem segundo registro do
  par

#### Scenario: Comprovante em forma diferente da aceita é recusado

- **WHEN** o prático aceita vídeo e o Mestre autor lança com foto e julgamento, sem declaração
  do Guerreiro(a)
- **THEN** o núcleo responde **422** nomeando vídeo como a forma esperada, e nada é gravado

#### Scenario: Prático anterior à forma aceita segue sem comprovação

- **WHEN** o prático foi declarado antes da regra da forma aceita e o Mestre autor lança com
  julgamento, sem declaração do Guerreiro(a)
- **THEN** a declaração nasce sem comprovação, como a do Guerreiro(a) nasceria, e publicável é
  recusado com **422**

#### Scenario: Guerreiro(a) não inscrito é recusado

- **WHEN** o Mestre autor lança com julgamento para um Guerreiro(a) que não está inscrito na
  trilha da missão
- **THEN** o núcleo responde **422** e nada é gravado

### Requirement: O Mestre autor lê a situação do prático de um Guerreiro(a) na missão

O núcleo SHALL servir ao **Mestre autor** da trilha, e ao **Admin**, a situação do desafio da
missão para um Guerreiro(a): o tipo do desafio, a forma aceita, o critério de aceite, se há
declaração e em que estado — aguardando, não cumpriu ou cumpriu —, a comprovação entregue e
se o lançamento **exige julgamento**. Outro papel SHALL receber **403**. (`RF-09-150`,
`RN-09-65`)

#### Scenario: Prático pendente diz que o julgamento é exigido

- **WHEN** o Mestre autor pede a situação do prático de um Guerreiro(a) que ainda não o cumpriu
- **THEN** o núcleo devolve a forma aceita, o critério de aceite, a declaração se houver e que o
  julgamento é exigido

#### Scenario: Prático cumprido dispensa o julgamento

- **WHEN** o Mestre autor pede a situação de um prático que o Guerreiro(a) já cumpriu
- **THEN** o núcleo devolve que cumpriu e que o julgamento não é exigido

#### Scenario: Mestre que não é o autor é recusado

- **WHEN** um Mestre que não é o autor da trilha pede a situação do prático
- **THEN** o núcleo responde **403**
