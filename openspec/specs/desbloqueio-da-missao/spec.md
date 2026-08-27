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
anterior, como a cadência de retomada já faz. Missão **sem** desafio de desbloqueio declarado
SHALL permanecer válida: o desafio não é trava de publicação da trilha. (`RF-09-26`)

#### Scenario: Mestre autor declara o desafio da sua missão

- **WHEN** o Mestre autor da trilha declara o desafio de desbloqueio de uma missão dela, como
  quiz ou como desafio prático
- **THEN** o núcleo grava o desafio vinculado àquela missão

#### Scenario: Quem não é o autor não declara

- **WHEN** um Mestre que não é o autor da trilha tenta declarar o desafio de uma missão dela
- **THEN** o núcleo responde 403 e nada é gravado

#### Scenario: Declarar de novo substitui o desafio anterior

- **WHEN** o Mestre autor declara o desafio de uma missão que já tinha um
- **THEN** o núcleo substitui o desafio anterior, sem criar um segundo

#### Scenario: Missão sem desafio continua válida

- **WHEN** uma trilha é publicada com missão que não declarou desafio de desbloqueio
- **THEN** a publicação segue pelas travas que já existem, sem exigir o desafio

### Requirement: O desbloqueio é fato do Guerreiro(a) na trilha

O núcleo SHALL registrar a **submissão do desafio de desbloqueio pelo Guerreiro(a)**, e o
desbloqueio resultante SHALL ser fato **dele na trilha** — nunca da equipe, e nunca derivado do
desbloqueio de um colega. Só o Guerreiro(a) **inscrito** naquela trilha SHALL submeter:
submissão sem inscrição SHALL ser recusada com **422**. No desafio em forma de **quiz**, o
núcleo SHALL aferir a submissão e, passando, marcar a missão como desbloqueada por ele **na
mesma operação**, de modo que a missão seguinte abra em seguida sem nenhum outro ato. Não
passando, o Guerreiro(a) SHALL poder **submeter de novo, sem limite de
tentativas**, e NEVER SHALL ser eliminado, bloqueado ou penalizado por isso. O desbloqueio
NEVER SHALL creditar pontos por si: ponto de atividade só nasce do Resultado que o Mestre
lança. (`RF-05-13`, `RF-05-14`, `RN-05-06`, `RN-05-20`, documento 11 §2.2)

#### Scenario: Passar no quiz desbloqueia a missão para quem submeteu

- **WHEN** o Guerreiro(a) inscrito submete o desafio em forma de quiz e passa
- **THEN** o núcleo marca a missão como desbloqueada **por ele**, e a seguinte passa a estar
  aberta para ele na mesma operação

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

### Requirement: O desafio prático é julgado pelo Mestre autor

No desafio em forma de **desafio prático**, o núcleo NEVER SHALL aferir a submissão sozinho: o
Guerreiro(a) SHALL **declarar que cumpriu**, e o **Mestre autor da trilha** SHALL **julgar se
passou**. Passando o julgamento, o núcleo SHALL marcar a missão como desbloqueada por aquele
Guerreiro(a), abrindo a seguinte para ele. Não passando, o Guerreiro(a) SHALL poder declarar de
novo, sem limite e sem punição. Persona que não é o Mestre autor SHALL ser recusada com
**403**. Enquanto o Mestre não julgar, o percurso SHALL exibir a missão como **aguardando o
Mestre**, nunca como reprovada. (`RF-05-13`, `RF-05-14`, `RF-09-26`, `RN-05-06`, decisão do
fundador em 2026-08-27)

#### Scenario: O Mestre autor julga o prático e a missão desbloqueia

- **WHEN** o Guerreiro(a) declara ter cumprido o desafio prático e o Mestre autor julga que
  passou
- **THEN** o núcleo marca a missão como desbloqueada por ele e abre a seguinte para ele

#### Scenario: Enquanto o Mestre não julga, nada é reprovado

- **WHEN** o Guerreiro(a) declarou ter cumprido o desafio prático e o Mestre ainda não julgou
- **THEN** o percurso exibe a missão como aguardando o Mestre, e ela segue travada sem
  reprovação

#### Scenario: Quem não é o autor não julga

- **WHEN** um Mestre que não é o autor da trilha tenta julgar o desafio prático de uma missão
  dela
- **THEN** o núcleo responde 403 e nada é gravado

#### Scenario: Julgado como não passou, o Guerreiro(a) declara de novo

- **WHEN** o Mestre autor julga que o Guerreiro(a) não passou no desafio prático
- **THEN** a missão segue travada e ele pode declarar de novo, sem limite e sem punição

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
resposta da sondagem NEVER SHALL certificar nível, conceder badge nem creditar ponto: ela mede
de onde o Guerreiro(a) parte, para o Mestre ajustar. (`RF-05-72`, `RF-05-73`, `RN-05-34`)

#### Scenario: A sondagem é a próxima missão de quem acabou de se inscrever

- **WHEN** o Guerreiro(a) se inscreve numa trilha e lê o percurso
- **THEN** a próxima missão é a de sondagem, e as missões comuns aparecem bloqueadas

#### Scenario: Respondida a sondagem, a primeira missão abre

- **WHEN** o Guerreiro(a) responde a missão de sondagem
- **THEN** a próxima missão passa a ser a primeira missão comum da trilha

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
