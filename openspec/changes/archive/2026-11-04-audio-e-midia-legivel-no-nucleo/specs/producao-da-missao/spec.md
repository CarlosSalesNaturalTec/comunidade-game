# Spec Delta

## REMOVED Requirements

### Requirement: A foto é descartada na leitura, e o áudio nunca chega ao núcleo

**Reason**: Revertida por decisão do fundador de 2026-11-03 (documento 09 §1). A produção da
missão passa a **guardar** a foto e o áudio: mídia descartada na leitura não pode ser exibida
depois, e o Guerreiro(a) precisa rever o que produziu.

**Migration**: A transcrição **continua**, porque é sobre ela que a devolutiva se faz; o que
muda é a mídia deixar de ser descartada. Produções gravadas antes desta change seguem sem
mídia, e a leitura responde **404** para elas — não há arquivo a recuperar.

### Requirement: A equipe entrega a produção por texto, fala ou foto do manuscrito

**Reason**: Substituída por "A equipe entrega a produção por texto, fala ou foto, e a mídia fica guardada", que admite o arquivo do áudio ao lado da transcrição. O
enunciado antigo proibia arquivo na forma "áudio".

**Migration**: Entregas em texto e em foto não mudam. Entrega em áudio passa a trazer a
transcrição **e** o arquivo; cliente que mande só a transcrição é recusado com 422.

### Requirement: O Guerreiro(a) entrega sozinho a produção de uma missão do próprio percurso

**Reason**: Substituída por "O Guerreiro(a) entrega sozinho a produção da missão, e a mídia fica guardada", pela mesma razão da porta da equipe.

**Migration**: A mesma da porta da equipe. As duas mudam juntas, para não abrir divergência
entre entregar na aula e entregar em casa.

## ADDED Requirements

### Requirement: A equipe entrega a produção por texto, fala ou foto, e a mídia fica guardada

O núcleo SHALL aceitar, de uma equipe, a entrega da produção da missão em **uma** destas três
formas: **texto** digitado, **áudio** da fala ou **foto** do que a equipe fez à mão. A forma da
entrega SHALL ser **declarada na chamada** e gravada com a produção — é ela que distingue a
fala do texto digitado, que chegam ambos como texto.

Entrega em **texto** SHALL trazer o **texto** e NEVER SHALL trazer arquivo. Entrega em
**áudio** SHALL trazer a **transcrição** feita no aparelho **e** o **arquivo** do áudio, que o
núcleo passa a guardar. Entrega em **foto** SHALL trazer o **arquivo** e NEVER SHALL trazer
texto. Entrega sem o conteúdo da forma declarada, ou com o
conteúdo de outra forma junto, SHALL ser recusada com **422**.

A produção SHALL ser ancorada na **atividade corrente** que a equipe declarou na programação
do encontro, e SHALL guardar a **missão** daquela atividade. Equipe sem atividade corrente
declarada SHALL ser recusada com **422** — não há missão a que a produção pertença.
(`RF-04-45`, `RF-05-76`, `RN-05-32`, documento 03 §§1.12, 4.2, documento 11 §2.2)

#### Scenario: Entrega por texto

- **WHEN** uma equipe com atividade corrente declarada entrega a produção em texto
- **THEN** o núcleo grava a produção com a forma "texto", a missão e a atividade daquela
  escolha

#### Scenario: Entrega por fala

- **WHEN** uma equipe entrega a produção falada, já transcrita no aparelho
- **THEN** o núcleo grava a produção com a forma "áudio", a transcrição recebida e o arquivo
  do áudio

#### Scenario: Entrega por foto do manuscrito

- **WHEN** uma equipe entrega a foto do que fez à mão
- **THEN** o núcleo grava a produção com a forma "foto" e a leitura do manuscrito em texto

#### Scenario: Entrega sem conteúdo é recusada

- **WHEN** chega uma entrega sem texto e sem arquivo
- **THEN** o núcleo responde 422 e nada é gravado

#### Scenario: Entrega com duas formas ao mesmo tempo é recusada

- **WHEN** chega uma entrega com texto e foto juntos
- **THEN** o núcleo responde 422 e nada é gravado

#### Scenario: Entrega por fala sem a transcrição é recusada

- **WHEN** chega uma entrega com a forma "áudio" trazendo o arquivo e nenhuma transcrição
- **THEN** o núcleo responde 422 e nada é gravado, porque a devolutiva se faz sobre o texto

#### Scenario: Equipe sem atividade corrente não entrega

- **WHEN** uma equipe que ainda não declarou a atividade que está trabalhando tenta entregar
- **THEN** o núcleo responde 422 e nada é gravado

### Requirement: O Guerreiro(a) entrega sozinho a produção da missão, e a mídia fica guardada

O núcleo SHALL aceitar, de um **Guerreiro(a) em sessão**, a entrega da produção de uma missão
em **uma** destas três formas: **texto** digitado, **áudio** da fala ou **foto** do que ele fez
à mão. A forma SHALL ser declarada na chamada e gravada com a produção.

Entrega em **texto** SHALL trazer o **texto** e NEVER SHALL trazer arquivo; entrega em
**áudio** SHALL trazer a **transcrição** e o **arquivo** do áudio;
entrega em **foto** SHALL trazer o **arquivo** e NEVER SHALL trazer texto. Entrega sem o
conteúdo da forma declarada, ou com o conteúdo de outra forma junto, SHALL ser recusada com
**422** — as mesmas recusas da entrega da equipe.

A produção SHALL ser ancorada em uma **atividade daquela missão**, declarada na entrega.
Atividade que não pertence à missão SHALL ser recusada com **422**.

A missão SHALL ser do **percurso do próprio Guerreiro(a)**: em trilha em que ele está
**inscrito** e por ele **desbloqueada**. Missão de trilha em que não está inscrito SHALL ser
recusada com **422**, e missão que ele ainda não desbloqueou SHALL ser recusada com **422** —
o percurso é o mesmo que já governa a leitura da missão, e a entrega não o atravessa.
(`RF-05-74`, `RF-05-76`, `RN-05-32`, `RN-05-35`, PRD-05 §9)

#### Scenario: Entrega individual por texto

- **WHEN** o Guerreiro(a) em sessão entrega, em texto, a produção de uma atividade de missão
  que ele desbloqueou em trilha em que está inscrito
- **THEN** o núcleo grava a produção com a forma "texto", a missão e a atividade declaradas

#### Scenario: Entrega individual por fala

- **WHEN** o Guerreiro(a) entrega a produção falada, já transcrita no aparelho
- **THEN** o núcleo grava a produção com a forma "áudio", a transcrição recebida e o arquivo
  do áudio

#### Scenario: Entrega individual por foto do manuscrito

- **WHEN** o Guerreiro(a) entrega a foto do que fez à mão
- **THEN** o núcleo grava a produção com a forma "foto" e a leitura do manuscrito em texto

#### Scenario: Entrega individual sem conteúdo é recusada

- **WHEN** chega uma entrega individual sem texto e sem arquivo
- **THEN** o núcleo responde 422 e nada é gravado

#### Scenario: Entrega individual com duas formas ao mesmo tempo é recusada

- **WHEN** chega uma entrega individual com texto e foto juntos
- **THEN** o núcleo responde 422 e nada é gravado

#### Scenario: Entrega individual por fala sem a transcrição é recusada

- **WHEN** chega uma entrega individual com a forma "áudio" sem a transcrição
- **THEN** o núcleo responde 422 e nada é gravado

#### Scenario: Atividade de outra missão é recusada

- **WHEN** o Guerreiro(a) declara, na entrega, uma atividade que não pertence à missão indicada
- **THEN** o núcleo responde 422 e nada é gravado

#### Scenario: Missão de trilha não inscrita é recusada

- **WHEN** o Guerreiro(a) tenta entregar a produção de uma missão de trilha em que não está
  inscrito
- **THEN** o núcleo responde 422 e nada é gravado

#### Scenario: Missão ainda não desbloqueada é recusada

- **WHEN** o Guerreiro(a) tenta entregar a produção de uma missão que ele ainda não desbloqueou
- **THEN** o núcleo responde 422 e nada é gravado

### Requirement: A mídia da produção da missão é guardada

O núcleo SHALL **guardar** o arquivo entregue na produção da missão — a **foto** do manuscrito
e o **áudio** da fala —, nas duas portas. O arquivo SHALL chegar na **mesma requisição** da
entrega, em `multipart/form-data`, como a foto já chega: é dela que o núcleo tira a
transcrição, e guardar é deixar de descartar o que ele já recebeu. A **transcrição** SHALL
continuar gravada. (`RF-01-79`, `RN-01-61`, `RF-04-45`, `RF-05-76`)

#### Scenario: A foto entregue fica guardada

- **WHEN** uma equipe entrega a foto do manuscrito
- **THEN** a produção fica com a mídia guardada, e a transcrição continua gravada com ela

#### Scenario: O áudio entregue fica guardado

- **WHEN** o Guerreiro(a) entrega a produção falada, com a transcrição e o arquivo do áudio
- **THEN** a produção fica com a mídia guardada, e a transcrição continua gravada com ela

#### Scenario: A entrega em texto não ganha mídia

- **WHEN** chega uma entrega na forma texto
- **THEN** a produção é gravada sem mídia, e a leitura dela responde 404

#### Scenario: A devolutiva continua a ser feita sobre o texto

- **WHEN** a produção tem transcrição e arquivo
- **THEN** a devolutiva é construída a partir da transcrição, e nunca a partir do arquivo

### Requirement: A mídia da produção da missão é servida a quem pode ver a produção

O núcleo SHALL servir os **bytes** da mídia de uma produção a quem já pode vê-la: quem a
entregou ou os **integrantes da equipe** dona dela, o **Mestre** da trilha e o **Admin**. Fora
desse conjunto SHALL responder **403**; produção sem mídia, **404**. NEVER SHALL haver rota
pública: a produção da missão não é item de acervo. (`RF-01-80`, `RN-01-62`)

#### Scenario: O integrante da equipe lê a mídia da produção dela

- **WHEN** um integrante da equipe dona da produção pede a mídia dela
- **THEN** o núcleo devolve os bytes com o tipo MIME gravado no envio

#### Scenario: O Mestre lê a mídia da produção da sua trilha

- **WHEN** o Mestre da trilha pede a mídia de uma produção dela
- **THEN** o núcleo devolve os bytes com o tipo MIME gravado no envio

#### Scenario: Quem não é da equipe nem Mestre é recusado

- **WHEN** um Guerreiro(a) de fora da equipe pede a mídia da produção dela
- **THEN** o núcleo responde 403 e nenhum byte é servido

#### Scenario: Produção sem mídia responde 404

- **WHEN** se pede a mídia de uma produção entregue em texto, ou gravada antes desta change
- **THEN** o núcleo responde 404

#### Scenario: Não há rota pública para a mídia da produção

- **WHEN** se procura a mídia de uma produção da missão sem sessão
- **THEN** não há rota pública que a sirva, porque a produção não é item de acervo
