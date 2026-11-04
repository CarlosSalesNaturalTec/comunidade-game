# desbloqueio-da-missao Specification

## Purpose

O desafio de desbloqueio é o que abre a missão seguinte, e é dele que nasce o percurso: qual é
a próxima missão do Guerreiro(a), quais estão travadas e por quê. O desbloqueio é fato do
Guerreiro(a) na trilha — nunca da equipe.

## Requirements

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

### Requirement: O desbloqueio é fato do Guerreiro(a) na trilha

O núcleo SHALL registrar a **submissão do desafio de desbloqueio pelo Guerreiro(a)**, e o
desbloqueio resultante SHALL ser fato **dele na trilha** — nunca da equipe, e nunca derivado do
desbloqueio de um colega. Só o Guerreiro(a) **inscrito** naquela trilha SHALL submeter:
submissão sem inscrição SHALL ser recusada com **422**. No desafio em forma de **quiz**, a
submissão SHALL trazer a resposta de **todas as perguntas de uma vez**, e o núcleo SHALL
aferi-la pela **proporção de acertos**: **passa quem acerta ao menos 60%** das perguntas do
quiz. Passando, o núcleo SHALL marcar a missão como desbloqueada por ele **na mesma operação**,
de modo que a missão seguinte abra em seguida sem nenhum outro ato. A devolutiva SHALL dizer
**quantas perguntas ele acertou** e de quantas. Não passando, o Guerreiro(a) SHALL poder
**submeter de novo, sem limite de tentativas**, e NEVER SHALL ser eliminado, bloqueado ou
penalizado por isso.

O desbloqueio por **quiz** NEVER SHALL creditar ponto por si: o núcleo o afere sozinho, e dele
não nasce crédito algum. O desbloqueio por **desafio prático** SHALL creditar no **julgamento do
Mestre autor**, e só ali — a entrega que o Mestre ainda não julgou NEVER SHALL creditar.
(`RF-05-13`, `RF-05-14`, `RF-05-89`, `RF-09-135`, `RN-05-06`, `RN-05-20`, `RN-05-45`,
documento 11 §§2.2 e 5)

#### Scenario: Passar no quiz desbloqueia a missão para quem submeteu

- **WHEN** o Guerreiro(a) inscrito submete o quiz respondendo a todas as perguntas e acerta ao
  menos 60% delas
- **THEN** o núcleo marca a missão como desbloqueada **por ele**, e a seguinte passa a estar
  aberta para ele na mesma operação

#### Scenario: Acertar menos de 60% não desbloqueia

- **WHEN** o Guerreiro(a) submete um quiz de dez perguntas e acerta cinco
- **THEN** a missão segue travada, e a devolutiva diz que ele acertou cinco de dez

#### Scenario: O desbloqueio de um não desbloqueia os colegas

- **WHEN** um integrante da equipe passa no desafio de desbloqueio de uma missão
- **THEN** o percurso dos demais Guerreiros e Guerreiras permanece como estava

#### Scenario: Não passar permite repetir sem punição

- **WHEN** o Guerreiro(a) submete o desafio e não passa, no quiz ou no julgamento do prático
- **THEN** o núcleo registra a tentativa, a missão segue travada e ele pode submeter de novo,
  sem limite e sem perder nada

#### Scenario: Submissão sem inscrição é recusada

- **WHEN** um Guerreiro(a) não inscrito na trilha submete o desafio de uma missão dela
- **THEN** o núcleo responde 422 e nada é gravado

#### Scenario: Desbloqueio não credita ponto

- **WHEN** o Guerreiro(a) passa no desafio de desbloqueio em forma de quiz
- **THEN** nenhum ponto é creditado por esse ato, e o saldo dele não muda

#### Scenario: A declaração do prático ainda não julgada não credita ponto

- **WHEN** o Guerreiro(a) declara que cumpriu o prático e o Mestre autor ainda não julgou
- **THEN** nenhum ponto é creditado, e o saldo dele só muda quando o julgamento disser que
  cumpriu

### Requirement: O desafio prático é julgado pelo Mestre autor

No desafio em forma de **desafio prático**, o núcleo NEVER SHALL aferir a submissão sozinho: o
Guerreiro(a) SHALL **declarar que cumpriu**, **entregando a comprovação** na forma aceita ou
declarando que a entrega ao Mestre no encontro, e o **Mestre autor da trilha** SHALL **julgar**.

O julgamento SHALL ter **dois vereditos**, declarados no mesmo ato e independentes em
significado:

- **cumpriu** — o Guerreiro(a) fez o que o desafio pedia. Cumprido, o núcleo SHALL marcar a
  missão como desbloqueada por aquele Guerreiro(a), abrindo a seguinte para ele, e SHALL
  creditar os pontos do julgamento. Não cumprido, o Guerreiro(a) SHALL poder entregar de novo,
  sem limite e sem punição.
- **publicável** — aquela entrega pode ir à **vitrine pública**. O publicável SHALL ficar
  gravado e NEVER SHALL, por si, abrir missão, creditar ponto ou alterar o percurso: ele é
  insumo do portão público, que exige também a autorização de divulgação do responsável
  (documento 02 §4).

Um veredito NEVER SHALL ser derivado do outro: cumprir sem ser publicável SHALL ser um
julgamento válido, e é para isso que os dois campos existem — com um só, o Mestre teria de
reprovar quem cumpriu e enquadrou mal, ou publicar o que não se pode publicar.

O julgamento SHALL ser **único** por par Guerreiro(a)–missão enquanto a entrega não for
refeita: julgar de novo uma declaração já julgada SHALL ser recusado com **422**. Persona que
não é o Mestre autor SHALL ser recusada com **403**. Enquanto o Mestre não julgar, o percurso
SHALL exibir a missão como **aguardando o Mestre**, nunca como reprovada. (`RF-05-13`,
`RF-05-14`, `RF-05-91`, `RF-09-26`, `RF-09-133`, `RN-05-06`, `RN-05-51`, `RN-09-52`, decisão do
fundador em 2026-08-27, ampliada em 2026-11-03 e recortada em 2026-11-04)

#### Scenario: O Mestre autor julga o prático e a missão desbloqueia

- **WHEN** o Guerreiro(a) declara ter cumprido o desafio prático e o Mestre autor julga que
  cumpriu
- **THEN** o núcleo marca a missão como desbloqueada por ele e abre a seguinte para ele

#### Scenario: Cumpriu sem ser publicável é julgamento válido

- **WHEN** o Mestre autor julga que o Guerreiro(a) cumpriu, mas que a entrega não é publicável
- **THEN** a missão desbloqueia, os pontos são creditados e a entrega fica gravada como não
  publicável

#### Scenario: Publicável fica gravado e não abre missão por si

- **WHEN** o Mestre autor marca uma entrega como publicável
- **THEN** o veredito fica gravado naquela declaração, e nenhum percurso, ponto ou nível muda
  por causa dele

#### Scenario: Enquanto o Mestre não julga, nada é reprovado

- **WHEN** o Guerreiro(a) declarou ter cumprido o desafio prático e o Mestre ainda não julgou
- **THEN** o percurso exibe a missão como aguardando o Mestre, e ela segue travada sem
  reprovação

#### Scenario: Quem não é o autor não julga

- **WHEN** um Mestre que não é o autor da trilha tenta julgar o desafio prático de uma missão
  dela
- **THEN** o núcleo responde 403 e nada é gravado

#### Scenario: Julgado como não passou, o Guerreiro(a) declara de novo

- **WHEN** o Mestre autor julga que o Guerreiro(a) não cumpriu o desafio prático
- **THEN** a missão segue travada e ele pode entregar de novo, sem limite e sem punição

#### Scenario: Julgar de novo o que já foi julgado é recusado

- **WHEN** o Mestre autor julga uma declaração que ele já julgou, sem que o Guerreiro(a) tenha
  entregado de novo
- **THEN** o núcleo responde **422** e o julgamento gravado permanece como estava

### Requirement: O núcleo deriva o percurso do Guerreiro(a) na trilha

O núcleo SHALL derivar, para o Guerreiro(a) inscrito, o **percurso** da trilha: a **próxima
missão**, as **desbloqueadas** e as **bloqueadas**. Toda missão bloqueada SHALL vir acompanhada
do **motivo do bloqueio**, nomeando a missão que falta desbloquear — bloqueio sem motivo NEVER
SHALL ser servido. O percurso SHALL seguir a **ordem da posição** que o Mestre autor declarou.
O percurso NEVER SHALL ser servido a quem não é o Guerreiro(a) dele. (`RF-05-08`, `RF-05-10`,
`RN-05-21`)

#### Scenario: A próxima missão é a primeira ainda não desbloqueada

- **WHEN** o Guerreiro(a) inscrito lê o percurso de uma trilha
- **THEN** a próxima missão é a de menor posição que ele ainda não desbloqueou

#### Scenario: Missão bloqueada diz o que falta

- **WHEN** o percurso traz uma missão que o Guerreiro(a) ainda não pode abrir
- **THEN** ela vem marcada como bloqueada, com o motivo nomeando a missão que falta desbloquear

#### Scenario: Missão já desbloqueada permanece aberta

- **WHEN** o Guerreiro(a) lê o percurso depois de desbloquear uma missão
- **THEN** ela consta como desbloqueada, e assim permanece nas leituras seguintes

#### Scenario: Percurso de terceiro não é servido

- **WHEN** alguém pede o percurso de um Guerreiro(a) que não é ele
- **THEN** o núcleo responde 403 e nada do percurso alheio é servido

### Requirement: A sondagem abre a trilha e não define nível

Enquanto o Guerreiro(a) inscrito **não tiver respondido a missão de sondagem** da trilha, o
percurso SHALL apontá-la como a **próxima missão** — ela vem antes da primeira missão comum. A
sondagem SHALL ser dada por **respondida ao ser submetida**, acertando ou não: o corte de 60%
NEVER SHALL se aplicar a ela, porque ela mede de onde o Guerreiro(a) parte e não o que a trilha
já ensinou. A resposta da sondagem NEVER SHALL certificar nível, conceder badge nem creditar
ponto: ela mede de onde o Guerreiro(a) parte, para o Mestre ajustar. (`RF-05-72`, `RF-05-73`,
`RN-05-34`, `RN-05-46`)

#### Scenario: A sondagem é a próxima missão de quem acabou de se inscrever

- **WHEN** o Guerreiro(a) se inscreve numa trilha e lê o percurso
- **THEN** a próxima missão é a de sondagem, e as missões comuns aparecem bloqueadas

#### Scenario: Respondida a sondagem, a primeira missão abre

- **WHEN** o Guerreiro(a) responde a missão de sondagem
- **THEN** a próxima missão passa a ser a primeira missão comum da trilha

#### Scenario: Errar a sondagem não tranca a trilha

- **WHEN** o Guerreiro(a) responde a sondagem e erra todas as perguntas
- **THEN** a trilha abre do mesmo jeito, e a submissão fica gravada com o que ele errou

#### Scenario: A sondagem não muda nível nem saldo

- **WHEN** o Guerreiro(a) responde a missão de sondagem
- **THEN** nenhum nível é certificado, nenhum badge é concedido e nenhum ponto é creditado

### Requirement: Só a missão obrigatória conta no percurso do nível

O núcleo SHALL contar **apenas as missões obrigatórias** no que falta para o próximo nível —
numerador e denominador. A missão **opcional** SHALL aparecer no percurso **marcada como
opcional**, SHALL poder ser desbloqueada e pontuada como qualquer outra, e NEVER SHALL entrar
no cálculo do nível. (`RF-05-81`, `RN-05-33`)

#### Scenario: Missão opcional vem marcada e fora da conta

- **WHEN** o Guerreiro(a) lê o percurso de uma trilha que tem missão opcional
- **THEN** ela aparece marcada como opcional, e o que falta para o próximo nível é contado só
  sobre as obrigatórias

#### Scenario: Desbloquear a opcional não avança o nível

- **WHEN** o Guerreiro(a) desbloqueia uma missão opcional
- **THEN** o que falta para o próximo nível permanece o mesmo

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

### Requirement: O Guerreiro(a) entrega a comprovação do desafio prático

A submissão do desafio em forma de **desafio prático** SHALL trazer a **comprovação** na
**forma que o Mestre autor declarou aceitar**, e o núcleo SHALL gravá-la com a declaração, no
mesmo ato. Comprovação em forma **diferente** da aceita SHALL ser recusada com **422**,
nomeando a forma esperada. O núcleo NEVER SHALL aferir a comprovação: ela existe para o
**julgamento do Mestre autor**. O **quiz** NEVER SHALL trazer comprovação. (`RF-05-91`,
documento 02 §4, documento 11 §2.2)

#### Scenario: A comprovação é gravada com a declaração

- **WHEN** o Guerreiro(a) inscrito declara que cumpriu o prático cuja forma aceita é vídeo, e
  entrega o vídeo
- **THEN** o núcleo grava a declaração com a comprovação, e a missão segue aguardando o Mestre

#### Scenario: Comprovação em texto é gravada como o corpo escrito

- **WHEN** a forma aceita é texto e o Guerreiro(a) entrega o corpo escrito
- **THEN** o núcleo grava o texto com a declaração, sem interpretá-lo nem aferi-lo

#### Scenario: Comprovação em link externo é gravada como o endereço

- **WHEN** a forma aceita é link externo e o Guerreiro(a) entrega o endereço
- **THEN** o núcleo grava o endereço com a declaração

#### Scenario: Forma diferente da aceita é recusada

- **WHEN** a forma aceita é imagem e a submissão traz comprovação em link externo
- **THEN** o núcleo responde **422** nomeando a forma esperada, e nada é gravado

#### Scenario: O quiz não traz comprovação

- **WHEN** a submissão de um desafio em forma de quiz traz comprovação
- **THEN** o núcleo responde **422** dizendo que o campo não se aplica ao quiz, e nada é gravado

### Requirement: A comprovação é exigida, e a entrega no encontro é a alternativa

Declarar que cumpriu o prático SHALL exigir a comprovação, ou, em lugar dela, a declaração de
que **entrega ao Mestre no encontro** — gravada **sem mídia**, marcada como **entrega
presencial**, e que NEVER SHALL fazer perder a missão nem contar como tentativa falha. Faltarem
as duas, ou vierem as duas, SHALL ser recusado com **422**. (`RN-05-51`, `RF-05-78`, `RN-05-20`,
PRD-05 §11, decisão do fundador de 2026-11-04)

#### Scenario: Declaração sem o corpo e sem alternativa é recusada

- **WHEN** a forma aceita é texto e o Guerreiro(a) declara que cumpriu sem escrever o corpo e
  sem escolher a entrega no encontro
- **THEN** o núcleo responde **422** nomeando o que falta, e nada é gravado

#### Scenario: Entregar pelo aparelho e no encontro ao mesmo tempo é recusado

- **WHEN** a declaração traz o corpo da comprovação e também a entrega no encontro
- **THEN** o núcleo responde **422** dizendo que é uma ou a outra, e nada é gravado

#### Scenario: A entrega no encontro grava a declaração sem mídia

- **WHEN** o Guerreiro(a) declara que cumpriu escolhendo entregar ao Mestre no encontro
- **THEN** o núcleo grava a declaração sem comprovação, marcada como entrega presencial, e a
  missão segue aguardando o Mestre

#### Scenario: A entrega presencial não é tentativa falha

- **WHEN** o Guerreiro(a) escolhe a entrega no encontro
- **THEN** nada é contado contra ele, a missão segue sem reprovação e o percurso a exibe como
  aguardando o Mestre

### Requirement: A mídia da comprovação entra por envio retomável

Comprovação em **imagem**, **áudio**, **vídeo** ou **arquivo** SHALL nascer **sem o arquivo** e
recebê-lo por **sessão de envio retomável**, servindo bytes só quando o envio **conclui**; nessas
quatro formas a declaração NEVER SHALL carregar o corpo da comprovação. O núcleo SHALL aplicar a
**mesma lista fechada de tipos** e os **mesmos tetos** da criação original. (`RF-05-91`,
`RF-01-78`)

#### Scenario: A comprovação em mídia nasce sem arquivo e o recebe depois

- **WHEN** o Guerreiro(a) declara que cumpriu entregando comprovação em vídeo
- **THEN** o núcleo grava a declaração sem mídia, e ela passa a existir quando o envio do
  arquivo conclui

#### Scenario: A declaração em forma de mídia não carrega o corpo

- **WHEN** a forma aceita é vídeo e a declaração traz o corpo da comprovação escrito
- **THEN** o núcleo responde **422** dizendo que aquela comprovação vai pelo envio do arquivo

#### Scenario: A declaração repetida depois do julgamento não toca no que está gravado

- **WHEN** o Guerreiro(a) declara de novo um prático já julgado como cumprido
- **THEN** o núcleo devolve a situação do julgamento, e a comprovação gravada permanece como
  estava

#### Scenario: Tipo de arquivo fora da lista é recusado

- **WHEN** o envio da comprovação declara tipo de arquivo que não está na lista fechada
- **THEN** o núcleo responde **422** e nenhum byte é aceito

#### Scenario: Tamanho acima do teto é recusado

- **WHEN** o envio da comprovação declara tamanho acima do teto do tipo dela
- **THEN** o núcleo responde **413** dizendo o teto, e nenhum byte é aceito

### Requirement: A comprovação é servida a quem pode vê-la

O núcleo SHALL servir os **bytes** da comprovação em mídia ao **próprio Guerreiro(a)** que a
entregou e ao **Mestre autor** da trilha — a ele porque é quem julga, a ele porque foi avisado
de que a mídia fica guardada. Persona que não é nenhum dos dois SHALL ser recusada com **403**.
Comprovação **sem mídia**, ou com envio **não concluído**, SHALL responder **404**. (`RF-05-93`,
decisão do fundador de 2026-11-04)

#### Scenario: O Guerreiro(a) reencontra o que entregou

- **WHEN** o Guerreiro(a) pede a comprovação que entregou
- **THEN** o núcleo devolve os bytes dela, com o tipo do arquivo que guardou

#### Scenario: O Mestre autor alcança a comprovação

- **WHEN** o Mestre autor da trilha pede a comprovação entregue naquela missão
- **THEN** o núcleo devolve os bytes dela

#### Scenario: Quem não é o autor nem quem entregou é recusado

- **WHEN** outro Guerreiro(a), ou um Mestre que não é o autor da trilha, pede a comprovação
- **THEN** o núcleo responde **403** e nenhum byte é servido

#### Scenario: Comprovação sem mídia responde 404

- **WHEN** se pedem os bytes de uma declaração de entrega presencial, ou de uma cujo envio não
  concluiu
- **THEN** o núcleo responde **404**

### Requirement: A entrega se refaz até o Mestre dizer que cumpriu

Enquanto o Mestre autor **não julgou**, o Guerreiro(a) SHALL poder entregar de novo, e a entrega
nova SHALL **substituir** a anterior — o corpo e a mídia — em vez de criar segundo registro.

Julgado que **não cumpriu**, a declaração NEVER SHALL ser apagada: ela SHALL permanecer gravada
com o veredito e o **motivo**, para que o Guerreiro(a) leia por que não passou. Entregar de novo
depois desse julgamento SHALL **reabrir a mesma declaração** — voltando a aguardar o Mestre e
substituindo a comprovação, o veredito e o motivo anteriores —, sem criar segundo registro e sem
limite de vezes. Nada disso é reprovação persistida: o que fica gravado é a devolutiva do
Mestre, não uma contagem de fracassos, e NEVER SHALL ser apresentado, exportado ou contado como
tal (`RN-05-20`).

A declaração reaberta SHALL contar como **entrega nova** também no tempo: o **momento** dela
SHALL ser o da entrega que a reabriu, nunca o da primeira. É dele que a **cadência de retomada**
conta os prazos (`RF-05-79`), e guardar o momento da entrega recusada faria o Guerreiro(a) que
entrega de novo semanas depois receber as retomadas já vencidas no instante da aprovação.

Julgado que **cumpriu**, a entrega SHALL estar encerrada: entregar ou enviar arquivo de novo
SHALL ser recusado com **422**, e a comprovação gravada SHALL permanecer como está. (`RN-05-52`,
`RN-05-20`, `RN-09-54`, `RF-05-79`, decisão do fundador de 2026-11-04)

#### Scenario: Entregar de novo antes do julgamento substitui o que estava

- **WHEN** o Guerreiro(a) entrega a comprovação e, antes de o Mestre julgar, entrega outra
- **THEN** o núcleo guarda só a última, e segue havendo uma única declaração daquele par

#### Scenario: Julgado que não cumpriu, a declaração e o motivo permanecem

- **WHEN** o Mestre autor julga que o Guerreiro(a) não cumpriu
- **THEN** a declaração permanece gravada com o veredito e o motivo, e a comprovação que ele
  entregou segue guardada

#### Scenario: Entregar de novo depois da recusa reabre a mesma declaração

- **WHEN** o Guerreiro(a) entrega de novo depois de o Mestre ter julgado que não cumpriu
- **THEN** aquela declaração volta a aguardar o Mestre, com a comprovação nova no lugar da
  anterior, sem veredito e sem motivo, e sem que nasça segundo registro do par

#### Scenario: A reabertura recoloca o momento da entrega

- **WHEN** o Guerreiro(a) é recusado e entrega de novo semanas depois
- **THEN** o momento da declaração passa a ser o da entrega nova, e as retomadas daquela missão
  contam dali, não da entrega recusada

#### Scenario: Depois de cumprido, o envio da comprovação é recusado

- **WHEN** o Guerreiro(a) tenta enviar o arquivo da comprovação de um prático já julgado como
  cumprido
- **THEN** o núcleo responde **422** e a comprovação gravada permanece como estava

### Requirement: O julgamento do prático exige o motivo em todo veredito negativo

O julgamento SHALL guardar o **motivo**, escrito pelo Mestre autor em **linguagem simples**,
dirigido a uma criança de 6 a 16 anos. O motivo SHALL ser **exigido** sempre que o julgamento
negar algo ao Guerreiro(a) — quando **não cumpriu**, e quando cumpriu mas **não é publicável**
—, e julgamento negativo **sem motivo** SHALL ser recusado com **422**, nomeando o campo que
falta, como a devolução da criação original já é recusada (`RF-09-34`). Quando o julgamento
**cumpriu e é publicável**, o motivo SHALL ser dispensado, e o que vier SHALL ser guardado.

Não ser publicável só é **negativa** quando publicar **era possível** — quando a declaração tem
comprovação gravada. Na **entrega presencial**, e na declaração cujo envio de arquivo não
concluiu, não há o que publicar, e o motivo SHALL ser **dispensado**: cobrar que o Mestre
explique uma recusa que ele não escolheu seria exigir motivo de um fato estrutural.

O motivo SHALL ser servido ao **Mestre autor** e ao **próprio Guerreiro(a)** daquela declaração.
Persona que não é nenhum dos dois NEVER SHALL alcançá-lo. (`RF-09-134`, `RN-09-53`, decisão do
fundador de 2026-11-04)

#### Scenario: Recusar sem motivo é recusado

- **WHEN** o Mestre autor julga que o Guerreiro(a) não cumpriu, sem escrever o motivo
- **THEN** o núcleo responde **422** nomeando o motivo como o que falta, e nada é gravado

#### Scenario: Negar a publicação sem motivo é recusado

- **WHEN** o Mestre autor julga que o Guerreiro(a) cumpriu, mas marca a entrega como não
  publicável sem escrever o motivo
- **THEN** o núcleo responde **422** nomeando o motivo, e nada é gravado

#### Scenario: Cumpriu e publicável dispensa o motivo

- **WHEN** o Mestre autor julga que o Guerreiro(a) cumpriu e que a entrega é publicável, sem
  motivo
- **THEN** o julgamento é gravado, a missão desbloqueia e nada é recusado

#### Scenario: A entrega presencial cumprida dispensa o motivo

- **WHEN** o Mestre autor confere no encontro e julga que o Guerreiro(a) cumpriu, sem marcar
  publicável e sem escrever motivo
- **THEN** o julgamento é gravado e nada é recusado, porque não havia o que publicar

#### Scenario: O motivo não é servido a terceiro

- **WHEN** outro Guerreiro(a), ou um Mestre que não é o autor da trilha, pede o julgamento
  daquela declaração
- **THEN** o núcleo não serve o veredito nem o motivo

### Requirement: Publicável só alcança entrega cumprida e com comprovação gravada

O veredito **publicável** SHALL ser aceito **somente** junto de **cumpriu** e **somente** quando
a declaração tem **comprovação gravada** — corpo escrito, endereço ou arquivo cujo envio
concluiu. Marcá-lo sobre entrega que o Mestre julga **não cumprida**, ou sobre **entrega
presencial**, que nasce sem mídia e não tem o que publicar, SHALL ser recusado com **422**,
dizendo qual das duas condições falta. (`RN-09-52`, `RN-05-51`, decisão do fundador de
2026-11-04)

#### Scenario: Publicável sobre o que não cumpriu é recusado

- **WHEN** o Mestre autor julga que o Guerreiro(a) não cumpriu e marca a entrega como
  publicável
- **THEN** o núcleo responde **422**, e nenhum dos dois vereditos é gravado

#### Scenario: Publicável sobre entrega presencial é recusado

- **WHEN** o Mestre autor julga uma declaração de entrega no encontro, sem mídia, e a marca
  como publicável
- **THEN** o núcleo responde **422** dizendo que não há comprovação a publicar, e nada é gravado

#### Scenario: A entrega presencial é julgada como cumprida, sem publicável

- **WHEN** o Mestre autor confere no encontro e julga que o Guerreiro(a) cumpriu, sem marcar
  publicável
- **THEN** o julgamento é gravado, a missão desbloqueia e os pontos são creditados

### Requirement: O julgamento que cumpriu credita 5 pontos regulares

Julgar que o Guerreiro(a) **cumpriu** o desafio prático SHALL creditar a ele **5 pontos
regulares** na **trilha da missão** — nunca em outra trilha, nunca num poder e nunca
globalmente —, na **mesma operação** do julgamento (documento 11 §5). O crédito SHALL alcançar
**somente** o Guerreiro(a) que entregou: a declaração é fato dele na trilha, e os colegas de
equipe NEVER SHALL receber nada por ela.

O crédito SHALL ser **único** por par Guerreiro(a)–missão: a declaração reaberta e julgada como
cumprida depois de uma recusa SHALL creditar os 5 pontos **uma vez**, e nenhum julgamento
posterior SHALL creditar segunda vez. O julgamento que diz **não cumpriu** NEVER SHALL creditar,
e NEVER SHALL debitar — ponto regular só debita por fato desfeito.

O julgamento NEVER SHALL certificar nível nem conceder badge: o nível é **percurso**, e o badge
de autoria é **só da culminância** (documento 02 §4, documento 09 §1). Os desbloqueios práticos
julgados **antes** desta regra NEVER SHALL receber crédito retroativo. (`RF-09-135`, `RN-09-55`,
decisão do fundador de 2026-11-04)

#### Scenario: Cumprido, o Guerreiro(a) recebe 5 pontos regulares na trilha da missão

- **WHEN** o Mestre autor julga que o Guerreiro(a) cumpriu o desafio prático de uma missão da
  trilha 1
- **THEN** o núcleo credita 5 pontos regulares a ele na trilha 1, e em nenhuma outra trilha nem
  poder

#### Scenario: O crédito alcança só quem entregou

- **WHEN** um integrante de equipe tem o prático julgado como cumprido
- **THEN** só ele recebe os 5 pontos, e o saldo dos colegas de equipe não muda

#### Scenario: Recusado e depois cumprido credita uma única vez

- **WHEN** o Guerreiro(a) é julgado como não cumprido, entrega de novo e é julgado como
  cumprido
- **THEN** ele recebe 5 pontos no total daquela missão, e não dez

#### Scenario: Não cumprido não credita e não debita

- **WHEN** o Mestre autor julga que o Guerreiro(a) não cumpriu
- **THEN** o saldo de ponto regular dele permanece exatamente como estava

#### Scenario: O julgamento não mexe no nível nem no badge

- **WHEN** o Mestre autor julga que o Guerreiro(a) cumpriu o desafio prático
- **THEN** nenhum nível é certificado e nenhum badge é concedido por esse ato

#### Scenario: O julgado antes desta regra não recebe crédito retroativo

- **WHEN** a regra passa a valer e existem desbloqueios práticos já julgados como aprovados
- **THEN** nenhum ponto é creditado por eles, e o saldo de quem passou antes não muda

### Requirement: O veredito e o motivo são servidos ao Guerreiro(a) no percurso

O **percurso** do Guerreiro(a) SHALL trazer, na missão cujo prático ele declarou ter cumprido, o
**veredito** do Mestre autor — cumpriu, não cumpriu ou ainda não julgado —, o **motivo** quando
houver e **quando** foi julgado, ao lado da comprovação que ele entregou. Nada do julgamento
SHALL ficar gravado sem ser servido a ele: é dele que o motivo fala.

O veredito **publicável** SHALL ser servido ao Guerreiro(a) junto dos demais, porque é o que
diz se aquela produção pode ir à vitrine, de que ele foi avisado ao entregar (`RF-05-92`). O
percurso NEVER SHALL ser servido a quem não é o Guerreiro(a) dele. (`RF-05-94`, `RF-05-93`,
`RN-05-21`, decisão do fundador de 2026-11-04)

#### Scenario: O Guerreiro(a) lê que cumpriu e que a entrega é publicável

- **WHEN** o Guerreiro(a) abre o percurso depois de o Mestre autor ter julgado que ele cumpriu
  e que a entrega é publicável
- **THEN** o percurso traz os dois vereditos e quando foi julgado, ao lado da comprovação que
  ele entregou

#### Scenario: O Guerreiro(a) lê por que não cumpriu

- **WHEN** o Guerreiro(a) abre o percurso depois de o Mestre autor ter julgado que ele não
  cumpriu, com motivo
- **THEN** o percurso traz o veredito e o motivo escrito pelo Mestre, e a missão segue como a
  próxima dele

#### Scenario: Antes do julgamento, o veredito vem em aberto

- **WHEN** o Guerreiro(a) abre o percurso tendo declarado e sem o Mestre ter julgado
- **THEN** o percurso diz que a missão aguarda o Mestre, sem veredito e sem motivo

#### Scenario: O percurso alheio não é servido

- **WHEN** alguém pede o percurso de um Guerreiro(a) que não é ele
- **THEN** o núcleo responde 403 e nenhum veredito nem motivo alheio é servido
