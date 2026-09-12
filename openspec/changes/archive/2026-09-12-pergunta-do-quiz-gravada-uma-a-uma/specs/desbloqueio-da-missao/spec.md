## ADDED Requirements

### Requirement: O Mestre autor grava cada pergunta do quiz isoladamente

O núcleo SHALL aceitar **acrescentar**, **corrigir** e **remover uma pergunta** do quiz do
desbloqueio **sem tocar nas demais**, como ato próprio, distinto da declaração do desafio
inteiro. O ato SHALL ser privativo do **Mestre autor da trilha** a que a missão pertence;
persona que não é o autor SHALL ser recusada com **403**, e nada SHALL ser gravado. O que vale
para a missão comum SHALL valer igual para a missão de **sondagem**, que é quiz pelo
`RF-09-81`. (`RF-09-120`)

Gravar uma pergunta isolada SHALL exigir que ela esteja **completa** — enunciado preenchido,
**quatro** alternativas preenchidas e a indicação de qual é a correta entre elas. Pergunta
incompleta SHALL ser recusada com **422**, nomeando o que falta, e nada SHALL ser gravado: a
pergunta nasce válida ou não nasce. É a mesma exigência que `RN-09-43` faz do quiz, aplicada à
unidade menor. (`RN-09-44`, decisão do fundador de 2026-09-12)

A pergunta acrescentada SHALL entrar **ao fim** da ordem vigente do quiz. Corrigir uma pergunta
NEVER SHALL alterar a ordem dela nem a das demais. **Reordenar** as perguntas segue sendo da
declaração do desafio inteiro, que permanece. (`RF-09-118`, `RF-09-120`)

Acrescentar pergunta a missão que **ainda não tem desafio declarado** SHALL declará-la **quiz**,
pelo mesmo ato: é o efeito que a declaração do desafio teria, alcançado pela unidade menor, e
sem ele a primeira pergunta de um quiz novo não teria como nascer isolada. Missão que já tem
desafio **prático** declarado NEVER SHALL receber pergunta por este caminho: SHALL ser recusada
com **422**, dizendo que o desafio dela é prático. (`RF-09-120`, `RF-09-26`)

Corrigir ou remover pergunta que alguma submissão já respondeu NEVER SHALL apagá-la nem
alterá-la, nem falhar por causa dela: a pergunta anterior **sai da leitura do desafio** e
permanece guardada, para que o registro da tentativa siga apontando o que o Guerreiro(a)
respondeu — o mesmo cuidado que a substituição do desafio inteiro já observa (`RN-05-47`). A
correção SHALL ocupar a mesma posição da pergunta que substituiu, e SHALL **conservar a
imagem** dela sem que nenhum byte seja reenviado.

Remover a **única** pergunta de um quiz SHALL ser recusado com **422**, dizendo que o quiz
precisa de ao menos uma pergunta: o quiz sem nenhuma pergunta é o estado que `RN-09-43` já
recusa na declaração, e a remoção por pergunta NEVER SHALL alcançá-lo por outro caminho.

A pergunta acrescentada isoladamente SHALL admitir **imagem** pelo mesmo caminho das demais,
assim que existe — sem que o Mestre precise declarar o desafio inteiro antes. (`RF-09-119`,
`RF-09-120`)

#### Scenario: O Mestre autor acrescenta uma pergunta ao quiz declarado

- **WHEN** o Mestre autor acrescenta uma pergunta completa ao quiz de uma missão sua, que já
  tem três perguntas
- **THEN** o núcleo grava a quarta ao fim da ordem, e as três anteriores seguem intactas, com
  os mesmos identificadores e as mesmas imagens

#### Scenario: A primeira pergunta declara a missão como quiz

- **WHEN** o Mestre autor acrescenta uma pergunta a uma missão que ainda não tem desafio de
  desbloqueio declarado
- **THEN** o núcleo grava a pergunta e a missão passa a ter desafio em forma de quiz

#### Scenario: Missão de desafio prático não recebe pergunta

- **WHEN** o Mestre autor acrescenta uma pergunta a uma missão cujo desafio declarado é prático
- **THEN** o núcleo responde **422** dizendo que o desafio daquela missão é prático, e nada é
  gravado

#### Scenario: Corrigir uma pergunta não toca nas demais

- **WHEN** o Mestre autor corrige o enunciado da segunda pergunta de um quiz de cinco
- **THEN** o núcleo grava a correção na segunda posição, e as outras quatro seguem como
  estavam

#### Scenario: Pergunta incompleta é recusada

- **WHEN** o Mestre autor grava uma pergunta com enunciado e apenas três alternativas
  preenchidas
- **THEN** o núcleo responde **422** dizendo o que falta, e nada é gravado

#### Scenario: Pergunta sem alternativa correta indicada é recusada

- **WHEN** o Mestre autor grava uma pergunta completa de texto, mas sem indicar qual das
  quatro alternativas é a correta
- **THEN** o núcleo responde **422** e nada é gravado

#### Scenario: Quem não é o autor não grava pergunta

- **WHEN** um Mestre que não é o autor da trilha acrescenta, corrige ou remove uma pergunta do
  quiz de uma missão dela
- **THEN** o núcleo responde **403** e nada é gravado

#### Scenario: Corrigir pergunta já respondida não apaga a tentativa

- **WHEN** o Mestre autor corrige uma pergunta que Guerreiros e Guerreiras já responderam
- **THEN** a leitura do desafio traz a pergunta corrigida na mesma posição, a anterior sai da
  leitura e permanece guardada, e nenhuma submissão gravada é apagada ou alterada

#### Scenario: Corrigir o texto conserva a imagem da pergunta

- **WHEN** o Mestre autor corrige o enunciado de uma pergunta que tem imagem
- **THEN** a pergunta corrigida continua com a mesma imagem, sem que nenhum byte seja reenviado

#### Scenario: Remover uma pergunta tira só ela do quiz

- **WHEN** o Mestre autor remove a terceira pergunta de um quiz de quatro
- **THEN** a leitura do desafio traz as três restantes, na ordem em que ficaram

#### Scenario: Remover a única pergunta do quiz é recusado

- **WHEN** o Mestre autor remove a última pergunta que resta no quiz
- **THEN** o núcleo responde **422** dizendo que o quiz precisa de ao menos uma pergunta, e a
  pergunta segue no quiz

#### Scenario: Pergunta acrescentada isoladamente aceita imagem

- **WHEN** o Mestre autor acrescenta uma pergunta ao quiz e, em seguida, pede o envio da imagem
  dela
- **THEN** o núcleo abre a sessão de envio daquela pergunta, sem exigir que o desafio inteiro
  seja declarado antes

#### Scenario: A sondagem grava pergunta a pergunta como qualquer quiz

- **WHEN** o Mestre autor acrescenta, corrige e remove perguntas da missão marcada como
  sondagem
- **THEN** o núcleo trata cada ato como no quiz do desbloqueio, com as mesmas recusas

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
do desafio, o **enunciado do prático** e a **ordem** das perguntas do quiz, e é a gravação por
pergunta que acrescenta, corrige e remove uma delas sem tocar nas demais (`RF-09-120`, decisão
do fundador de 2026-09-12).

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
