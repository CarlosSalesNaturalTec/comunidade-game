## ADDED Requirements

### Requirement: Toda tentativa do desafio de desbloqueio fica registrada

O núcleo SHALL registrar **toda submissão** do desafio de desbloqueio — a que passa e a que
não passa, na missão de sondagem como nas demais —, guardando o instante, quantas perguntas
foram acertadas, o total e, **por pergunta**, a alternativa que o Guerreiro(a) escolheu e se
ela era a correta. Repetir o desafio SHALL acrescentar uma submissão nova, e NEVER SHALL
apagar nem sobrescrever as anteriores. O registro NEVER SHALL ser servido a quem não é o
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

#### Scenario: Registro de terceiro não é servido

- **WHEN** alguém que não é o Guerreiro(a) nem o Mestre autor da trilha pede as submissões dele
- **THEN** o núcleo responde 403 e nada é servido

## MODIFIED Requirements

### Requirement: O Mestre autor declara o desafio de desbloqueio da missão

O núcleo SHALL registrar, para uma missão, o **desafio de desbloqueio** que abre a missão
seguinte, na forma de **quiz** ou de **desafio prático**, declarado pelo **Mestre autor da
trilha** a que a missão pertence. Persona que não é o Mestre autor SHALL ser recusada com
**403**. Declarar de novo o desafio de uma missão que já o tem SHALL **substituir** o
anterior, com as perguntas dele, como a cadência de retomada já faz. Missão **sem** desafio de
desbloqueio declarado SHALL permanecer válida: o desafio não é trava de publicação da trilha.

No **quiz**, o desafio SHALL trazer **uma ou mais perguntas**, sem limite de quantidade, cada
uma com o seu enunciado, **quatro alternativas** e a indicação de qual é a correta; a **ordem**
declarada pelo Mestre autor SHALL ser preservada na leitura. Quiz declarado **sem nenhuma
pergunta** SHALL ser recusado com **422**. (`RF-09-26`, `RF-09-118`, `RN-09-43`)

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

#### Scenario: Missão sem desafio continua válida

- **WHEN** uma trilha é publicada com missão que não declarou desafio de desbloqueio
- **THEN** a publicação segue pelas travas que já existem, sem exigir o desafio

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
penalizado por isso. O desbloqueio NEVER SHALL creditar pontos por si: ponto de atividade só
nasce do Resultado que o Mestre lança. (`RF-05-13`, `RF-05-14`, `RF-05-89`, `RN-05-06`,
`RN-05-20`, `RN-05-45`, documento 11 §2.2)

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

- **WHEN** o Guerreiro(a) passa no desafio de desbloqueio
- **THEN** nenhum ponto é creditado por esse ato, e o saldo dele não muda

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
