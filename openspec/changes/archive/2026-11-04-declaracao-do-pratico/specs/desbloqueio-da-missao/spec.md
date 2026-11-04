# Spec Delta

## MODIFIED Requirements

### Requirement: O Mestre autor declara o desafio de desbloqueio da missão

O núcleo SHALL registrar, para uma missão, o **desafio de desbloqueio** que abre a missão
seguinte, na forma de **quiz** ou de **desafio prático**, declarado pelo **Mestre autor da
trilha** a que a missão pertence. Persona que não é o Mestre autor SHALL ser recusada com
**403**. Declarar de novo o desafio de uma missão que já o tem SHALL **substituir** o
anterior, com as perguntas dele, como a cadência de retomada já faz. A substituição NEVER SHALL
apagar pergunta que alguma submissão já respondeu, nem falhar por causa dela: a pergunta
substituída **sai da leitura do desafio** e permanece guardada, para que o registro da
tentativa siga apontando o que o Guerreiro(a) respondeu (`RN-05-47`). Missão **sem** desafio de
desbloqueio declarado SHALL permanecer válida: o desafio não é trava de publicação da trilha.

A declaração do desafio inteiro SHALL **conviver** com a gravação de cada pergunta
isoladamente, sem substituí-la nem ser substituída por ela: é a declaração que fixa o **tipo**
do desafio, o que o **prático** declara — enunciado, forma de comprovação aceita, critério de
aceite e título curto — e a **ordem** das perguntas do quiz, e é a gravação por pergunta que
acrescenta, corrige e remove uma delas sem tocar nas demais (`RF-09-120`, `RF-09-129` a
`RF-09-131`, decisão do fundador de 2026-09-12).

No **quiz**, o desafio SHALL trazer **uma ou mais perguntas**, sem limite de quantidade, cada
uma com o seu enunciado, **quatro alternativas** e a indicação de qual é a correta; a **ordem**
declarada pelo Mestre autor SHALL ser preservada na leitura. Quiz declarado **sem nenhuma
pergunta** SHALL ser recusado com **422**. (`RF-09-26`, `RF-09-118`, `RN-09-43`)

A leitura do desafio pelo **Mestre autor** SHALL trazer, em cada pergunta, o **identificador**
dela e a **referência da imagem** que ela tem, e a declaração SHALL **aceitá-la de volta**: a
pergunta que volta com a referência **conserva a imagem**, e a que a omite nasce **sem imagem**
— é assim que o Mestre a remove. Substituir as perguntas NEVER SHALL, por si, obrigar o Mestre
a reenviar arquivo que ele já enviou. A referência que volta SHALL ser conferida contra as
imagens das perguntas **daquela mesma missão**: referência de qualquer outra origem SHALL ser
recusada com **422**, e NEVER SHALL alcançar arquivo de outra trilha, de outro Mestre ou de
fora do desafio. (`RF-09-119`, decisão do fundador de 2026-09-11)

O corpo da declaração SHALL aceitar, em cada pergunta, **apenas** os campos do contrato —
enunciado, alternativas, alternativa correta e referência da imagem. O **identificador** que a
leitura devolve é endereço da pergunta, não campo declarável: mandá-lo de volta no corpo SHALL
ser recusado, e a recusa SHALL chegar ao Mestre **com o motivo**, nunca como falha genérica.

#### Scenario: Mestre autor declara o desafio da sua missão

- **WHEN** o Mestre autor da trilha declara o desafio de desbloqueio de uma missão dela, como
  quiz ou como desafio prático
- **THEN** o núcleo grava o desafio vinculado àquela missão

#### Scenario: O quiz aceita quantas perguntas o Mestre declarar

- **WHEN** o Mestre autor declara um quiz com doze perguntas, cada uma com quatro alternativas
  e a correta indicada
- **THEN** o núcleo grava as doze, na ordem declarada

#### Scenario: Quiz sem pergunta é recusado

- **WHEN** o Mestre autor declara um desafio em forma de quiz sem nenhuma pergunta
- **THEN** o núcleo responde 422 e nada é gravado

#### Scenario: Quem não é o autor não declara

- **WHEN** um Mestre que não é o autor da trilha tenta declarar o desafio de uma missão dela
- **THEN** o núcleo responde 403 e nada é gravado

#### Scenario: Declarar de novo substitui o desafio anterior

- **WHEN** o Mestre autor declara o desafio de uma missão que já tinha um
- **THEN** o núcleo substitui o desafio anterior e as perguntas dele, sem criar um segundo

#### Scenario: Redeclarar depois de alguém ter respondido não falha

- **WHEN** o Mestre autor declara de novo o desafio de uma missão cujo quiz Guerreiros e
  Guerreiras já responderam
- **THEN** o núcleo grava as perguntas novas, a leitura do desafio traz só elas, e nenhuma
  submissão já gravada é apagada ou alterada

#### Scenario: Redeclarar com a referência de volta conserva a imagem

- **WHEN** o Mestre autor corrige o enunciado de uma pergunta com imagem e declara o desafio de
  novo, devolvendo a referência daquela imagem
- **THEN** a pergunta gravada conserva a imagem, sem que nenhum byte seja reenviado

#### Scenario: Redeclarar sem a referência remove a imagem

- **WHEN** o Mestre autor declara o desafio de novo omitindo a referência da imagem de uma
  pergunta
- **THEN** a pergunta gravada fica sem imagem

#### Scenario: Referência de outra origem é recusada

- **WHEN** a declaração traz, numa pergunta, referência que não é de imagem de pergunta daquela
  missão
- **THEN** o núcleo responde **422** e nada é gravado

#### Scenario: O identificador da pergunta não volta no corpo da declaração

- **WHEN** o cliente declara o desafio devolvendo, em cada pergunta, o identificador que a
  leitura lhe deu
- **THEN** o núcleo recusa o corpo por campo fora do contrato, e o Mestre lê na tela o motivo
  da recusa

#### Scenario: A declaração e a gravação por pergunta convivem

- **WHEN** o Mestre autor declara o desafio inteiro de uma missão cujo quiz vinha sendo gravado
  pergunta a pergunta
- **THEN** a declaração substitui o conjunto, como já fazia, e as gravações por pergunta
  seguintes atuam sobre as perguntas que ela deixou

#### Scenario: Missão sem desafio continua válida

- **WHEN** uma trilha é publicada com missão que não declarou desafio de desbloqueio
- **THEN** a publicação segue pelas travas que já existem, sem exigir o desafio

## ADDED Requirements

### Requirement: O desafio prático declara a forma de comprovação aceita

A declaração do desafio em forma de **desafio prático** SHALL trazer a **forma de comprovação
aceita**: **uma** das seis formas de entrega do Guerreiro(a) — texto, imagem, áudio, vídeo,
arquivo e link externo (documento 02 §4). Forma fora das seis SHALL ser recusada com **422**.
Prático **sem** forma declarada SHALL ser recusado com **422**, nomeando o campo. O **quiz**
NEVER SHALL declarar forma de comprovação. (`RF-09-129`, `RN-09-50`)

#### Scenario: O Mestre autor declara o prático com a forma aceita

- **WHEN** o Mestre autor declara o desafio prático de uma missão sua, com a forma de
  comprovação em vídeo, o critério de aceite e o título curto
- **THEN** o núcleo grava o desafio com a forma declarada

#### Scenario: Forma fora das seis é recusada

- **WHEN** a declaração do prático traz forma de comprovação que não é uma das seis
- **THEN** o núcleo responde **422** e nada é gravado

#### Scenario: Prático sem forma declarada é recusado

- **WHEN** o Mestre autor declara o prático sem a forma de comprovação
- **THEN** o núcleo responde **422** nomeando o campo que falta, e nada é gravado

#### Scenario: O quiz não declara forma de comprovação

- **WHEN** a declaração de um desafio em forma de quiz traz forma de comprovação
- **THEN** o núcleo responde **422** dizendo que o campo não se aplica ao quiz, e nada é
  gravado

### Requirement: O desafio prático declara o critério de aceite

A declaração do desafio **prático** SHALL trazer o **critério de aceite**, em **texto livre**
escrito pelo Mestre autor, que diz o que a comprovação precisa mostrar e o que não pode
aparecer nela. Prático **sem** critério, ou com critério **em branco**, SHALL ser recusado com
**422**, nomeando o campo. O **quiz** NEVER SHALL declarar critério de aceite — nele o corte de
acertos é o critério, e o núcleo o afere sozinho. (`RF-09-130`, `RN-09-50`, documento 11 §2.2)

#### Scenario: O critério de aceite fica gravado como o Mestre o escreveu

- **WHEN** o Mestre autor declara o prático com o critério de que, em foto ou vídeo, não deve
  aparecer o rosto da criança, só a produção
- **THEN** o núcleo grava o critério em texto livre, sem interpretá-lo nem aferi-lo

#### Scenario: Critério em branco é recusado

- **WHEN** o Mestre autor declara o prático com o critério de aceite vazio ou só com espaços
- **THEN** o núcleo responde **422** nomeando o campo, e nada é gravado

#### Scenario: O quiz não declara critério de aceite

- **WHEN** a declaração de um desafio em forma de quiz traz critério de aceite
- **THEN** o núcleo responde **422** dizendo que o campo não se aplica ao quiz, e nada é
  gravado

### Requirement: O desafio prático declara o título curto

A declaração do desafio **prático** SHALL trazer um **título curto**, campo **próprio** e
distinto do enunciado, de no máximo **60 caracteres**, que é o que a vitrine exibe ao lado do
nick. Título **ausente**, **em branco** ou **acima de 60 caracteres** SHALL ser recusado com
**422**, dizendo o teto. O título NEVER SHALL ser derivado do enunciado, que é texto livre sem
teto. O **quiz** NEVER SHALL declarar título curto. (`RF-09-131`, `RN-09-50`, `RN-09-51`,
documento 11 §8.2)

#### Scenario: O título curto fica gravado em campo próprio

- **WHEN** o Mestre autor declara o prático com o título curto e um enunciado longo
- **THEN** o núcleo grava os dois em campos distintos, e a leitura os devolve separados

#### Scenario: Título acima do teto é recusado

- **WHEN** o Mestre autor declara o prático com título curto de 80 caracteres
- **THEN** o núcleo responde **422** dizendo o teto de 60 caracteres, e nada é gravado

#### Scenario: Título em branco é recusado

- **WHEN** o Mestre autor declara o prático sem título curto, ou com ele só em espaços
- **THEN** o núcleo responde **422** nomeando o campo, e nada é gravado

#### Scenario: O quiz não declara título curto

- **WHEN** a declaração de um desafio em forma de quiz traz título curto
- **THEN** o núcleo responde **422** dizendo que o campo não se aplica ao quiz, e nada é
  gravado

### Requirement: A leitura do desafio prático traz os três campos declarados

Toda leitura que já serve o **desafio de desbloqueio** SHALL trazer, no prático, a **forma de
comprovação aceita**, o **critério de aceite** e o **título curto**, ao lado do enunciado que
ela já serve: a das trilhas do Mestre autor, a resposta da própria declaração e a do percurso
do Guerreiro(a) inscrito.
Nenhum dos três é segredo do Mestre — é deles que o Guerreiro(a) sabe o que entregar e sob que
critério será julgado. No quiz os três SHALL vir **nulos**. (`RF-09-129` a `RF-09-131`)

#### Scenario: O Mestre autor reencontra o que declarou

- **WHEN** o Mestre autor lê as trilhas dele depois de declarar o prático de uma missão
- **THEN** a missão traz o tipo, o enunciado, a forma aceita, o critério de aceite e o título
  curto, como ele os declarou

#### Scenario: O Guerreiro(a) inscrito lê a forma e o critério

- **WHEN** o Guerreiro(a) inscrito na trilha lê a missão cujo desbloqueio é prático
- **THEN** o desafio vem com a forma de comprovação aceita e o critério de aceite

#### Scenario: No quiz os três campos vêm nulos

- **WHEN** alguém lê uma missão cujo desbloqueio é quiz
- **THEN** a forma de comprovação, o critério de aceite e o título curto vêm nulos

### Requirement: O prático declarado antes desta regra segue valendo

Desafio prático gravado **antes** desta regra NEVER SHALL deixar de valer por não ter a forma
aceita, o critério de aceite nem o título curto: a missão segue com o desbloqueio dela, a
leitura devolve os três campos **nulos**, e o percurso do Guerreiro(a) segue como está. Os três
passam a existir quando o Mestre autor **redeclarar** aquele desafio, e a redeclaração SHALL
exigi-los como qualquer declaração nova. (`RN-09-50`, decisão do fundador de 2026-11-04)

#### Scenario: Prático antigo continua servido, com os campos nulos

- **WHEN** se lê a missão de um prático declarado antes desta regra
- **THEN** o desafio vem com o tipo e o enunciado que tinha, e os três campos novos nulos

#### Scenario: Redeclarar o prático antigo exige os três campos

- **WHEN** o Mestre autor declara de novo o desafio prático de uma missão que o tinha
  incompleto, sem informar os três campos
- **THEN** o núcleo responde **422** nomeando o que falta, e o desafio anterior permanece como
  estava
