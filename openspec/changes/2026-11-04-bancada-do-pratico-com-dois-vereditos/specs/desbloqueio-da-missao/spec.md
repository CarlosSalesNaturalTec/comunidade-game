# Spec Delta

## MODIFIED Requirements

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

## ADDED Requirements

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

Julgado que **cumpriu**, a entrega SHALL estar encerrada: entregar ou enviar arquivo de novo
SHALL ser recusado com **422**, e a comprovação gravada SHALL permanecer como está. (`RN-05-52`,
`RN-05-20`, `RN-09-54`, decisão do fundador de 2026-11-04)

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

## REMOVED Requirements

### Requirement: Entrega nova antes do julgamento substitui a anterior

**Reason**: O julgamento passou a guardar o **motivo** em linguagem simples, e o requisito
mandava apagar a declaração reprovada — o motivo seria apagado no mesmo ato em que nasce, e o
Guerreiro(a) nunca o leria (decisão do fundador, 2026-11-04, `RN-09-54`). O requisito também
encerrava a entrega em **qualquer** julgamento, e agora só o "cumpriu" a encerra.

**Migration**: Substituído pelo requisito "A entrega se refaz até o Mestre dizer que cumpriu",
que mantém a substituição antes do julgamento e a entrega encerrada depois de cumprido, e troca
o apagamento pela reabertura da mesma declaração. Nenhum dado se perde na troca: a migração não
apaga nem cria declaração alguma, e as declarações já apagadas por esta regra não voltam.
