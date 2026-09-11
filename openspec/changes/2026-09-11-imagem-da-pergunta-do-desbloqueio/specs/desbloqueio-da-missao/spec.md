## ADDED Requirements

### Requirement: A pergunta do quiz admite uma imagem opcional

O núcleo SHALL admitir, em cada pergunta do quiz do desbloqueio, **uma imagem opcional** — no
máximo uma por pergunta. Pergunta **sem** imagem SHALL permanecer válida: a imagem NEVER SHALL
ser exigida para declarar o desafio nem para publicar a trilha.

A imagem SHALL ser enviada pelo **mesmo padrão do conteúdo da missão**: o núcleo abre, a pedido
do **Mestre autor da trilha**, uma sessão de envio retomável e devolve o endereço ao cliente; os
bytes NEVER SHALL trafegar pelo núcleo, que guarda apenas a **referência**, o tipo e o tamanho.
Sessão pedida por quem não é o Mestre autor SHALL ser recusada com **403**. Encerrado o envio, o
Mestre autor SHALL confirmá-lo, e só então a pergunta passa a ter imagem.

O envio SHALL aceitar apenas os **formatos de imagem da lista fechada** — **JPG, PNG e WebP** —
e SHALL recusar qualquer outro com **422**, nomeando o que chegou e a lista aceita. SHALL
recusar com **413** a imagem **acima de 1 MB**, informando o tamanho recebido e o teto; o teto é
de **cada pergunta**, e a recusa SHALL acontecer na abertura da sessão, pelo tamanho declarado,
e de novo na confirmação, se o recebido divergir. (`RF-09-119`, `RF-09-115`, documento 03 §11)

#### Scenario: O Mestre autor anexa a imagem de uma pergunta

- **WHEN** o Mestre autor pede o envio da imagem de uma pergunta do quiz de uma missão sua, em
  PNG de 400 KB, e confirma o envio ao fim
- **THEN** o núcleo grava a referência da imagem naquela pergunta, sem guardar os bytes em
  tabela

#### Scenario: Pergunta sem imagem segue válida

- **WHEN** o Mestre autor declara um quiz cujas perguntas não têm imagem alguma
- **THEN** o núcleo grava o desafio, e a publicação da trilha segue pelas travas que já existem

#### Scenario: Formato fora da lista é recusado antes do envio

- **WHEN** o Mestre autor pede o envio de um GIF como imagem de uma pergunta
- **THEN** o núcleo responde **422** nomeando os formatos aceitos, e nenhuma sessão é aberta

#### Scenario: Imagem acima de 1 MB é recusada

- **WHEN** o Mestre autor pede o envio de uma imagem de 3 MB para uma pergunta
- **THEN** o núcleo responde **413** dizendo o tamanho recebido e o teto de 1 MB

#### Scenario: Envio que diverge do tamanho declarado é recusado ao fim

- **WHEN** o envio conclui com mais bytes do que o tamanho declarado na abertura
- **THEN** o núcleo responde **413**, e a pergunta NEVER SHALL passar a servir aquela imagem

#### Scenario: Quem não é o autor não anexa imagem

- **WHEN** um Mestre que não é o autor da trilha pede o envio da imagem de uma pergunta dela
- **THEN** o núcleo responde **403** e nenhuma sessão é aberta

#### Scenario: Pergunta sem envio confirmado não serve imagem

- **WHEN** a pergunta é lida depois de aberta a sessão e antes de o envio ser confirmado
- **THEN** ela é apresentada sem imagem, e nenhuma referência quebrada é servida

### Requirement: A imagem da pergunta é servida a quem pode ver a pergunta

O núcleo SHALL servir os **bytes** da imagem de uma pergunta do quiz ao **Mestre autor da
trilha** e ao **Guerreiro(a) inscrito** nela — os mesmos que já leem a pergunta —, com o tipo
declarado no envio. A quem não é um dos dois SHALL responder **403**, e NEVER SHALL servir a
imagem de trilha em que o Guerreiro(a) não está inscrito. Pergunta **sem imagem** SHALL
responder **404**. A leitura NEVER SHALL revelar a alternativa correta, que segue fora de toda
saída ao Guerreiro(a). (`RF-09-119`, `RF-05-89`, decisão do fundador de 2026-09-11)

#### Scenario: O Guerreiro(a) inscrito vê a imagem da pergunta

- **WHEN** o Guerreiro(a) inscrito na trilha pede a imagem de uma pergunta do quiz de uma
  missão dela
- **THEN** o núcleo devolve os bytes da imagem, com o tipo declarado no envio

#### Scenario: O Mestre autor vê a imagem que anexou

- **WHEN** o Mestre autor pede a imagem de uma pergunta da sua trilha
- **THEN** o núcleo devolve os bytes da imagem

#### Scenario: Quem não é inscrito nem autor é recusado

- **WHEN** um Guerreiro(a) não inscrito na trilha pede a imagem de uma pergunta dela
- **THEN** o núcleo responde **403** e nenhum byte é servido

#### Scenario: Pergunta sem imagem responde 404

- **WHEN** alguém que pode ver a pergunta pede a imagem de uma pergunta que não tem imagem
- **THEN** o núcleo responde **404**

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

No **quiz**, o desafio SHALL trazer **uma ou mais perguntas**, sem limite de quantidade, cada
uma com o seu enunciado, **quatro alternativas** e a indicação de qual é a correta; a **ordem**
declarada pelo Mestre autor SHALL ser preservada na leitura. Quiz declarado **sem nenhuma
pergunta** SHALL ser recusado com **422**. (`RF-09-26`, `RF-09-118`, `RN-09-43`)

A leitura do desafio pelo **Mestre autor** SHALL trazer, em cada pergunta, a **referência da
imagem** que ela tem, e a declaração SHALL **aceitá-la de volta**: a pergunta que volta com a
referência **conserva a imagem**, e a que a omite nasce **sem imagem** — é assim que o Mestre a
remove. Substituir as perguntas NEVER SHALL, por si, obrigar o Mestre a reenviar arquivo que
ele já enviou. A referência que volta SHALL ser conferida contra as imagens das perguntas
**daquela mesma missão**: referência de qualquer outra origem SHALL ser recusada com **422**, e
NEVER SHALL alcançar arquivo de outra trilha, de outro Mestre ou de fora do desafio. (`RF-09-119`,
decisão do fundador de 2026-09-11)

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

#### Scenario: Missão sem desafio continua válida

- **WHEN** uma trilha é publicada com missão que não declarou desafio de desbloqueio
- **THEN** a publicação segue pelas travas que já existem, sem exigir o desafio

### Requirement: Toda tentativa do desafio de desbloqueio fica registrada

O núcleo SHALL registrar **toda submissão** do desafio de desbloqueio — a que passa e a que
não passa, na missão de sondagem como nas demais —, guardando o instante, quantas perguntas
foram acertadas, o total e, **por pergunta**, a alternativa que o Guerreiro(a) escolheu e se
ela era a correta. Repetir o desafio SHALL acrescentar uma submissão nova, e NEVER SHALL
apagar nem sobrescrever as anteriores. **Redeclarar o desafio** da missão NEVER SHALL apagar,
alterar nem quebrar submissão já gravada: a pergunta que ela aponta permanece guardada, ainda
que tenha saído do desafio vigente. O registro NEVER SHALL ser servido a quem não é o
Guerreiro(a) dele nem o Mestre autor da trilha, e NEVER SHALL creditar ponto, alterar nível ou
aparecer como reprovação no percurso. (`RN-05-47`)

#### Scenario: A tentativa que não passa fica gravada

- **WHEN** o Guerreiro(a) submete o quiz de uma missão e não alcança o corte
- **THEN** o núcleo grava a submissão com os acertos, o total e a resposta de cada pergunta, e
  a missão segue travada

#### Scenario: Repetir acrescenta, não substitui

- **WHEN** o Guerreiro(a) submete o quiz da mesma missão pela segunda vez
- **THEN** as duas submissões constam do registro, cada uma com o seu instante e as suas
  respostas

#### Scenario: A sondagem também fica gravada

- **WHEN** o Guerreiro(a) responde a missão de sondagem
- **THEN** a submissão dela fica gravada com a resposta de cada pergunta e se acertou

#### Scenario: A submissão sobrevive à troca das perguntas

- **WHEN** o Mestre autor redeclara o quiz de uma missão que já tinha submissões
- **THEN** as submissões anteriores continuam no registro, cada uma apontando a pergunta que
  foi respondida

#### Scenario: Registro de terceiro não é servido

- **WHEN** alguém que não é o Guerreiro(a) nem o Mestre autor da trilha pede as submissões dele
- **THEN** o núcleo responde 403 e nada é servido
