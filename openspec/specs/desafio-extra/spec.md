## Purpose

O desafio extra é o que o Apoiador propõe a uma trilha em andamento: uma tarefa a mais, com
recompensa provida por ele e pontos que correm à parte da pontuação regular. Esta capacidade
cobre a proposta — o que ela declara, o que a plataforma nunca confirma sobre o destinatário, o
lastro sem o qual ela não se publica e os estados por onde ela passa até virar desafio.

## Requirements

### Requirement: A proposta se vincula a uma trilha em andamento e declara o que oferece

O núcleo SHALL registrar o `DesafioExtra` vinculando **proponente** — **Apoiador ou Mestre** —,
**trilha em andamento** e, opcionalmente, **missão**, com **recompensa**, **quantidade
disponível**, **critério de atribuição** e **período de vigência**. Trilha que não esteja em
andamento SHALL ser recusada com **422**. Persona de qualquer outro papel SHALL ser recusada
com **403**. NEVER SHALL existir teto de desafios simultâneos: o controle é a aprovação caso a
caso. (`RF-14-29`, `RF-14-30`, `RN-14-15`, `RF-09-105`, PRD-14 §8, 04 §3)

#### Scenario: Proposta completa é registrada

- **WHEN** um Apoiador propõe um desafio a uma trilha em andamento, com recompensa, quantidade,
  critério de atribuição e vigência
- **THEN** o núcleo registra a proposta com o proponente, a trilha e o que ela oferece

#### Scenario: O Mestre propõe pela mesma mecânica

- **WHEN** um Mestre propõe um desafio a uma trilha em andamento, com recompensa, quantidade,
  critério de atribuição e vigência
- **THEN** o núcleo registra a proposta com ele como proponente, sob as mesmas exigências da
  proposta do Apoiador

#### Scenario: Trilha que não está em andamento é recusada

- **WHEN** a proposta declara uma trilha que não está em andamento
- **THEN** o núcleo responde 422 e nenhuma proposta passa a existir

#### Scenario: Papel que não propõe é recusado

- **WHEN** uma persona que não é Apoiador nem Mestre propõe um desafio extra
- **THEN** o núcleo responde 403 e nenhuma proposta passa a existir

#### Scenario: Não há teto de propostas simultâneas

- **WHEN** um Apoiador propõe um desafio tendo outros já propostos e ainda não desfeitos
- **THEN** o núcleo registra a proposta, sem recusar por quantidade

### Requirement: A proposta declara a modalidade, e o direcionado exige nick e justificativa

O núcleo SHALL exigir da proposta a **modalidade**: **aberto** ou **direcionado**. No
direcionado SHALL exigir o **nick do destinatário** e a **justificativa do vínculo**,
recusando com **422** a proposta que não os traga. No aberto NEVER SHALL barrar quem dispute:
o que é limitado é a **quantidade de recompensas**. (`RF-14-31`, `RF-14-32`, `RN-14-16`,
`RN-14-17`)

#### Scenario: Direcionado sem justificativa do vínculo é recusado

- **WHEN** uma proposta direcionada chega com o nick do destinatário e sem a justificativa do
  vínculo
- **THEN** o núcleo responde 422 e nenhuma proposta passa a existir

#### Scenario: Aberto não restringe quem dispute

- **WHEN** uma proposta é registrada na modalidade aberta
- **THEN** ela vale para todos os Guerreiros e Guerreiras da trilha, limitada apenas pela
  quantidade de recompensas declarada

### Requirement: A plataforma não confirma a existência do nick do destinatário

O núcleo SHALL guardar o **nick do destinatário como o proponente o digitou**, e NEVER SHALL
resolvê-lo em referência ao Guerreiro(a) no ato da proposta. NEVER SHALL revelar ao proponente
— na aceitação, na leitura ou na recusa — se aquele nick existe, e NEVER SHALL devolver avatar,
trilha, atividade ou qualquer outro dado do destinatário. A ligação com a pessoa SHALL ser
feita apenas na validação do Mestre. (`RF-14-33`, `RN-14-18`, `RN-14-20`, PRD-14 §§8, 12)

#### Scenario: Proposta com nick inexistente é aceita

- **WHEN** uma proposta direcionada declara um nick que não corresponde a Guerreiro(a) algum
- **THEN** o núcleo registra a proposta como qualquer outra, sem erro e sem indicar que o nick
  não existe

#### Scenario: A leitura do proponente não devolve dado do destinatário

- **WHEN** o proponente lê a proposta direcionada que registrou
- **THEN** a resposta traz o nick como ele o digitou e nenhum dado do destinatário

### Requirement: Os pontos extras têm teto de 10 e correm isolados da pontuação regular

O núcleo SHALL exigir da proposta os **pontos extras** que o desafio vale e SHALL recusar com
**422** valor acima de **10**, de qualquer proponente. Os pontos do desafio extra SHALL ser
computados **isoladamente** da pontuação regular do Guerreiro(a). (`RF-14-74`, `RN-14-41`,
`RN-14-19`)

#### Scenario: Proposta acima do teto é recusada

- **WHEN** uma proposta declara 11 pontos extras
- **THEN** o núcleo responde 422, indicando o teto de 10, e nenhuma proposta passa a existir

#### Scenario: Ponto extra do desafio não entra na pontuação regular

- **WHEN** uma proposta é registrada com pontos extras
- **THEN** esses pontos ficam registrados como extras do desafio, sem alterar a pontuação
  regular de ninguém

### Requirement: A proposta declara o formato e o custeio da recompensa

O núcleo SHALL exigir da proposta o **formato** do desafio — **presencial** ou **on-line** — e o
**custeio** da recompensa, em uma de duas formas: **aporte do proponente** ou **saldo de
recurso existente** na plataforma. Proposta sem formato ou sem custeio SHALL ser recusada com
**422**. (`RF-14-75`, `RF-14-76`, `RF-07-41`)

#### Scenario: Proposta sem custeio declarado é recusada

- **WHEN** uma proposta chega sem declarar o custeio da recompensa
- **THEN** o núcleo responde 422 e nenhuma proposta passa a existir

#### Scenario: Custeio por saldo existente é aceito

- **WHEN** uma proposta declara custeio por saldo de recurso existente na plataforma
- **THEN** o núcleo registra a proposta com esse custeio

### Requirement: Sem lastro provido a recompensa não se publica

O núcleo SHALL manter, em cada `DesafioExtra`, se o **lastro da recompensa** está provido, e
NEVER SHALL permitir que o desafio chegue a **publicado** sem ele. A leitura do proponente
SHALL informar **o que falta prover**. (`RF-14-34`, `RF-07-15`, `RN-14-14`, PRD-14 §12)

#### Scenario: Proposta sem lastro provido não alcança a publicação

- **WHEN** um desafio sem lastro provido chega ao ato que o publicaria
- **THEN** a publicação é recusada, e a recusa informa que falta o lastro da recompensa

#### Scenario: A leitura mostra o que falta prover

- **WHEN** o proponente lê um desafio cujo lastro não está provido
- **THEN** a resposta informa que o lastro falta e o que precisa ser provido

### Requirement: A situação percorre validação do Mestre, aprovação do Admin e publicação

O núcleo SHALL manter a **situação** do `DesafioExtra` entre **em validação do Mestre**, **em
aprovação do Admin**, **publicado** e **recusado**. A situação de nascimento SHALL ser decidida
pelo proponente: **em aprovação do Admin** quando ele for o Mestre autor da trilha, **em
validação do Mestre** em qualquer outro caso. NEVER SHALL publicar desafio que não tenha
passado pela aprovação de Admin, nem desafio que, não sendo do Mestre autor da trilha, não
tenha passado pela validação do Mestre dela. A recusa em qualquer etapa SHALL guardar o
**motivo**, e a leitura do proponente SHALL devolvê-lo. (`RF-14-35`, `RF-14-36`, `RN-14-13`,
`RF-09-108`, `RN-09-11`, `RN-09-41`)

#### Scenario: Proposta nasce em validação do Mestre

- **WHEN** um Apoiador registra uma proposta
- **THEN** a situação dela é "em validação do Mestre"

#### Scenario: A proposta do Mestre autor nasce em aprovação do Admin

- **WHEN** o Mestre autor da trilha registra uma proposta a ela
- **THEN** a situação dela é "em aprovação do Admin"

#### Scenario: O proponente lê o motivo da recusa

- **WHEN** o proponente lê um desafio recusado
- **THEN** a resposta traz a situação de recusado e o motivo registrado

### Requirement: A fila do Mestre traz só o que ele tem a validar

O núcleo SHALL devolver ao **Mestre** em sessão os desafios extras em **em validação do
Mestre** cujas trilhas são de **autoria dele**, com o que cada proposta oferece — trilha,
missão quando houver, modalidade, recompensa, quantidade, critério de atribuição, pontos
extras, formato, custeio e vigência. A fila NEVER SHALL trazer desafio de trilha de outro
Mestre, nem desafio em **em aprovação do Admin**, **publicado** ou **recusado**. Persona de
qualquer outro papel SHALL receber **403**. Nenhuma resposta SHALL identificar Guerreiro(a):
do direcionado sai o **nick como o proponente o digitou**, e nada mais. (`RF-09-51`,
`RN-09-11`, `RN-14-20`)

#### Scenario: A fila traz o desafio da trilha do próprio Mestre

- **WHEN** o Mestre consulta a fila e há um desafio em validação vinculado a uma trilha de que
  ele é autor
- **THEN** o desafio aparece com a recompensa, a quantidade, o critério, os pontos extras, o
  formato, o custeio e a vigência

#### Scenario: Desafio de trilha de outro Mestre não aparece

- **WHEN** o Mestre consulta a fila e há um desafio em validação vinculado à trilha de outro
  Mestre
- **THEN** o desafio não aparece na fila

#### Scenario: O já validado sai da fila

- **WHEN** um desafio da trilha do Mestre é validado ou recusado por ele
- **THEN** a consulta seguinte à fila não o traz mais

#### Scenario: Quem não é Mestre não lê a fila

- **WHEN** uma persona de outro papel consulta a fila de desafios extras a validar
- **THEN** o núcleo responde 403

#### Scenario: A fila não identifica o destinatário do direcionado

- **WHEN** a fila traz um desafio direcionado
- **THEN** a resposta traz o nick como o proponente o digitou e nenhum outro dado do
  destinatário

### Requirement: O Mestre autor da trilha valida o desafio extra com parecer

O núcleo SHALL permitir ao **Mestre autor da trilha** validar um desafio extra em **em
validação do Mestre**, exigindo o **parecer** e gravando **quem validou**, e SHALL levar a
situação a **em aprovação do Admin**. Validação sem parecer SHALL ser recusada com **422**.
A validação por persona que não seja o Mestre autor daquela trilha SHALL ser recusada com
**403**, ainda que seja Mestre de outra trilha. A validação de desafio que não esteja em **em
validação do Mestre** SHALL ser recusada com **409**. (`RF-09-51`, `RN-09-11`)

#### Scenario: A validação com parecer leva o desafio ao Admin

- **WHEN** o Mestre autor da trilha valida um desafio em validação, com parecer
- **THEN** o desafio passa a em aprovação do Admin, com o parecer e o Mestre validador
  registrados

#### Scenario: Validação sem parecer não passa

- **WHEN** o Mestre autor valida um desafio sem informar o parecer
- **THEN** o núcleo responde 422 e o desafio permanece em validação do Mestre

#### Scenario: Mestre de outra trilha não valida

- **WHEN** um Mestre que não é autor da trilha valida o desafio dela
- **THEN** o núcleo responde 403 e o desafio permanece como estava

#### Scenario: Desafio já validado não se valida de novo

- **WHEN** o Mestre autor valida um desafio que já está em aprovação do Admin
- **THEN** o núcleo responde 409 e nada muda

### Requirement: O Mestre recusa o desafio extra com motivo, e o recusado não chega ao Admin

O núcleo SHALL permitir ao **Mestre autor da trilha** recusar um desafio extra em **em
validação do Mestre**, exigindo o **motivo** e gravando **quem recusou**, e SHALL levar a
situação a **recusado**. Recusa sem motivo SHALL ser recusada com **422**. O desafio recusado
pelo Mestre NEVER SHALL aparecer na fila de aprovação do Admin, e a leitura do proponente SHALL
devolver o motivo. Nenhuma reserva SHALL ser gravada pela recusa. (`RF-09-51`, `RF-09-52`,
`RN-09-11`)

#### Scenario: Recusa sem motivo não passa

- **WHEN** o Mestre autor recusa um desafio sem informar o motivo
- **THEN** o núcleo responde 422 e o desafio permanece em validação do Mestre

#### Scenario: O recusado pelo Mestre não chega à fila do Admin

- **WHEN** o Mestre autor recusa um desafio com motivo e o Admin consulta a fila dele
- **THEN** o desafio não aparece na fila do Admin

#### Scenario: O proponente lê o motivo da recusa do Mestre

- **WHEN** o proponente lê um desafio recusado pelo Mestre
- **THEN** a resposta traz a situação de recusado e o motivo que o Mestre registrou

### Requirement: A validação pedagógica é dispensada só para o Mestre autor da própria trilha

O núcleo SHALL nascer o `DesafioExtra` em **em aprovação do Admin** quando o proponente for o
**Mestre autor da trilha** a que ele se vincula, e em **em validação do Mestre** em qualquer
outro caso — proposta de Apoiador e proposta de **outro Mestre** que não seja o autor daquela
trilha. A dispensa NEVER SHALL alcançar a **aprovação do Admin**, exigida de toda proposta.
(`RF-09-108`, `RF-09-109`, `RF-09-110`, `RN-09-41`)

#### Scenario: A proposta do Mestre autor já nasce na fila do Admin

- **WHEN** o Mestre autor de uma trilha propõe um desafio extra a ela
- **THEN** a proposta nasce em aprovação do Admin, sem passar por validação pedagógica

#### Scenario: A proposta de outro Mestre passa pela validação do autor

- **WHEN** um Mestre propõe um desafio extra a uma trilha de que não é autor
- **THEN** a proposta nasce em validação do Mestre e aparece na fila do Mestre autor daquela
  trilha

#### Scenario: A dispensa não dispensa o Admin

- **WHEN** a proposta do Mestre autor chega à publicação sem que o Admin a tenha aprovado
- **THEN** a publicação é recusada, porque a aprovação do Admin é exigida de toda proposta

### Requirement: O direcionado proposto pelo Mestre exige justificativa pedagógica

O núcleo SHALL exigir do desafio **direcionado** proposto por Mestre, além do **nick do
destinatário**, a **justificativa pedagógica** registrada — no lugar da justificativa de
vínculo que o Apoiador declara —, recusando com **422** a proposta que não a traga. As demais
guardas do direcionado SHALL valer igual: NEVER SHALL o núcleo confirmar ao proponente se
aquele nick existe, nem devolver dado do destinatário. (`RF-09-111`, `RN-14-18`, `RN-14-20`,
04 §3)

#### Scenario: Direcionado do Mestre sem justificativa é recusado

- **WHEN** um Mestre propõe um desafio direcionado com o nick do destinatário e sem a
  justificativa pedagógica
- **THEN** o núcleo responde 422 e nenhuma proposta passa a existir

#### Scenario: Direcionado do Mestre não confirma o nick

- **WHEN** um Mestre propõe um desafio direcionado a um nick que não corresponde a
  Guerreiro(a) algum
- **THEN** o núcleo registra a proposta como qualquer outra, sem erro e sem indicar que o nick
  não existe

### Requirement: A fila do Admin traz só quem já passou pela validação do Mestre

O núcleo SHALL devolver ao **Admin** em sessão a fila dos desafios extras em **aprovação do
Admin**, com o que cada proposta oferece — trilha, missão quando houver, modalidade, recompensa,
quantidade, critério de atribuição, pontos extras, formato, custeio, vigência —, se o **lastro
está provido** e **o que falta prover** quando não está. A fila NEVER SHALL trazer desafio em
**validação do Mestre**, **publicado** ou **recusado**. Persona de qualquer outro papel SHALL
receber **403**. Nenhuma resposta SHALL identificar Guerreiro(a): do direcionado sai o **nick
como o proponente o digitou**, e nada mais. (`RF-02-27`, `RN-02-10`, `RF-14-39`, `RN-14-20`)

#### Scenario: Desafio sem validação do Mestre não aparece na fila

- **WHEN** o Admin consulta a fila e há uma proposta ainda em validação do Mestre
- **THEN** a proposta não aparece na fila

#### Scenario: A fila mostra o que a proposta oferece e o que falta de lastro

- **WHEN** o Admin consulta a fila e há um desafio em aprovação do Admin sem lastro provido
- **THEN** o desafio aparece com a recompensa, a quantidade, o critério, os pontos extras e a
  informação do que falta prover

#### Scenario: O publicado e o recusado saem da fila

- **WHEN** um desafio é aprovado ou recusado
- **THEN** a consulta seguinte à fila não o traz mais

#### Scenario: Quem não é Admin não lê a fila

- **WHEN** uma persona de outro papel consulta a fila de desafios extras
- **THEN** o núcleo responde 403

### Requirement: O Admin aprova o desafio, e a aprovação exige validação do Mestre e lastro

O núcleo SHALL permitir ao **Admin** aprovar um desafio extra em **aprovação do Admin**,
gravando **quem aprovou** e levando a situação a **publicado**. A aprovação de desafio que ainda
esteja em **validação do Mestre** SHALL ser recusada com **409**, e a de desafio **publicado** ou
**recusado**, com **409** também. Sem o **lastro da recompensa** provido, a aprovação SHALL ser
recusada com **422**, informando o que falta prover, e o desafio SHALL permanecer na fila.
(`RF-02-28`, `RN-02-10`, `RN-02-11`, `RF-07-15`, `RN-07-12`, invariante 9)

#### Scenario: Aprovação de desafio sem validação do Mestre é recusada

- **WHEN** o Admin aprova um desafio que segue em validação do Mestre
- **THEN** o núcleo responde 409 e o desafio permanece como estava

#### Scenario: Aprovação sem lastro é recusada e o desafio fica na fila

- **WHEN** o Admin aprova um desafio validado pelo Mestre cujo lastro não está provido
- **THEN** o núcleo responde 422 informando o que falta prover, e o desafio segue em aprovação
  do Admin

#### Scenario: Aprovação com lastro publica o desafio

- **WHEN** o Admin aprova um desafio validado pelo Mestre e com lastro provido
- **THEN** o desafio passa a publicado, com o Admin aprovador registrado

### Requirement: O Admin recusa o desafio com motivo

O núcleo SHALL permitir ao **Admin** recusar um desafio extra em **aprovação do Admin**,
exigindo o **motivo** e levando a situação a **recusado**. Recusa sem motivo SHALL ser recusada
com **422**. A leitura do proponente SHALL devolver o motivo, e nenhuma reserva SHALL ser
gravada pela recusa. (`RF-02-28`, `RF-14-36`, `RN-14-13`)

#### Scenario: Recusa sem motivo não passa

- **WHEN** o Admin recusa um desafio sem informar o motivo
- **THEN** o núcleo responde 422 e o desafio permanece em aprovação do Admin

#### Scenario: A recusa registra o motivo que o proponente lê

- **WHEN** o Admin recusa um desafio com motivo
- **THEN** o desafio passa a recusado, e a leitura do proponente traz esse motivo

### Requirement: A publicação reserva a recompensa, e sem disponível não publica

O núcleo SHALL, no mesmo ato que publica o desafio extra, **reservar** a quantidade disponível
da recompensa — o tipo de recurso, no ponto de apoio que a proposta declarou. A publicação SHALL
ser recusada com **422**, sem gravar reserva alguma e sem mudar a situação, quando a **quantidade
disponível** daquele par tipo e ponto de apoio não cobrir a recompensa, ainda que o lastro tenha
sido apurado. Recompensa de tipo de recurso de natureza **durável** SHALL ser recusada com
**422**, porque patrimônio não sofre baixa por consumo. (`RF-07-39`, `RN-07-01`, `RN-07-07`,
invariante 9)

#### Scenario: A publicação grava a reserva da recompensa

- **WHEN** o Admin aprova um desafio cuja recompensa cabe na quantidade disponível
- **THEN** o desafio passa a publicado e a recompensa fica reservada naquele ponto de apoio

#### Scenario: Sem disponível a publicação é recusada

- **WHEN** o Admin aprova um desafio cuja recompensa não cabe na quantidade disponível, porque
  outra reserva já comprometeu o saldo
- **THEN** o núcleo responde 422, nenhuma reserva é gravada e o desafio segue em aprovação do
  Admin

#### Scenario: A reserva do desafio reduz o disponível dos demais

- **WHEN** um desafio é publicado reservando a recompensa
- **THEN** a quantidade disponível daquele tipo naquele ponto de apoio passa a excluir o que o
  desafio reservou, e o saldo derivado dos lançamentos segue o mesmo

#### Scenario: Recompensa de tipo durável não publica

- **WHEN** o Admin aprova um desafio cuja recompensa é de tipo de recurso de natureza durável
- **THEN** o núcleo responde 422 indicando o tipo, e nenhuma reserva é gravada

### Requirement: O Admin encerra o desafio publicado, e o encerramento libera a reserva

O núcleo SHALL permitir ao **Admin** encerrar um desafio extra **publicado**, gravando **quem
encerrou e quando**, e SHALL levar a **liberada** toda reserva daquele desafio que ainda esteja
**reservada**, devolvendo a quantidade à disponível. O encerramento de desafio que não esteja
publicado SHALL ser recusado com **409**, e o de desafio já encerrado, com **409** também.
Desafio encerrado NEVER SHALL receber conclusão nova. O encerramento NEVER SHALL desfazer
conclusão já registrada nem a baixa que ela produziu, e NEVER SHALL acontecer por decurso da
vigência: só por este ato. (`RF-07-40`, `RF-02-106`, `RF-07-09`)

#### Scenario: O encerramento devolve o saldo à disponível

- **WHEN** o Admin encerra um desafio publicado cuja recompensa segue reservada
- **THEN** a reserva passa a liberada e a quantidade disponível volta a incluir a recompensa

#### Scenario: Desafio não publicado não se encerra

- **WHEN** o Admin encerra um desafio que está em aprovação do Admin
- **THEN** o núcleo responde 409 e nada muda

#### Scenario: Encerrar duas vezes não passa

- **WHEN** o Admin encerra um desafio já encerrado
- **THEN** o núcleo responde 409 e a reserva permanece liberada uma única vez

#### Scenario: A vigência vencida sozinha não encerra

- **WHEN** a vigência de um desafio publicado termina sem que o Admin o encerre
- **THEN** o desafio segue publicado e a recompensa segue reservada

### Requirement: A conclusão do desafio extra fica registrada

O núcleo SHALL manter o registro da **conclusão** de um `DesafioExtra` por um Guerreiro(a),
com o desafio, quem concluiu, a **data do fato**, se a recompensa foi entregue e quantos
**pontos extras** o desafio rendeu. O registro SHALL ser **somente inserção**: NEVER SHALL
haver rota que o altere ou o retire. Um mesmo Guerreiro(a) NEVER SHALL ter duas conclusões
registradas para o mesmo desafio. NEVER SHALL existir conclusão de desafio que não esteja
**publicado**, nem de desafio **encerrado** — encerrado o desafio, a recompensa já voltou à
disponível e não há o que entregar. (`RF-14-42`, `RF-14-37`, `RF-07-40`, 04 §3)

#### Scenario: A conclusão guarda quem, quando e quanto rendeu

- **WHEN** uma conclusão é registrada para um desafio publicado
- **THEN** ela guarda o desafio, o Guerreiro(a), a data do fato, a entrega da recompensa e os
  pontos extras

#### Scenario: A mesma pessoa não conclui duas vezes o mesmo desafio

- **WHEN** chega uma segunda conclusão do mesmo Guerreiro(a) para o mesmo desafio
- **THEN** o núcleo a recusa

#### Scenario: Desafio não publicado não recebe conclusão

- **WHEN** chega uma conclusão para desafio que ainda não foi publicado
- **THEN** o núcleo a recusa

#### Scenario: Desafio encerrado não recebe conclusão

- **WHEN** chega uma conclusão para desafio que o Admin já encerrou
- **THEN** o núcleo a recusa

### Requirement: Desafio publicado não se edita, e mostra a quantidade restante

O núcleo SHALL recusar com **405** toda alteração de `DesafioExtra` **publicado**: a correção é
**proposta nova**, e a proposta anterior SHALL permanecer registrada com o desfecho que teve. A
leitura do publicado SHALL trazer a **quantidade de recompensas restante**, que é a quantidade
disponível **menos as conclusões registradas com recompensa entregue**, e NEVER SHALL ficar
negativa. (`RF-14-37`, `RF-14-38`, PRD-14 §8)

#### Scenario: Edição de desafio publicado é recusada

- **WHEN** chega uma alteração de um desafio já publicado
- **THEN** o núcleo responde 405 e o desafio permanece como estava

#### Scenario: A proposta anterior permanece registrada

- **WHEN** um Apoiador propõe de novo para corrigir um desafio publicado
- **THEN** nasce uma proposta nova e a anterior continua registrada com o desfecho que teve

#### Scenario: O publicado informa quanto resta

- **WHEN** o proponente lê um desafio publicado
- **THEN** a resposta traz a quantidade de recompensas restante

#### Scenario: A conclusão com recompensa entregue desconta o que resta

- **WHEN** uma conclusão com recompensa entregue é registrada para o desafio
- **THEN** a leitura seguinte traz a quantidade restante descontada dela

#### Scenario: A quantidade restante não fica negativa

- **WHEN** as conclusões com recompensa entregue alcançam a quantidade disponível
- **THEN** a quantidade restante é zero

### Requirement: Cada proponente lê os desafios que propôs

O núcleo SHALL devolver a **Apoiador ou Mestre** em sessão os desafios extras que ele mesmo
propôs, com a **situação** de cada um, o **motivo da recusa** quando houver e a **quantidade
restante** do publicado. NEVER SHALL devolver a um proponente o desafio proposto por outro.
(`RF-09-105`, `RF-14-35`, `RF-14-38`)

#### Scenario: O Mestre lê o que propôs

- **WHEN** um Mestre lê os seus desafios extras
- **THEN** a resposta traz os que ele propôs, com a situação de cada um

#### Scenario: O proponente não lê o desafio alheio

- **WHEN** um proponente lê os seus desafios extras e há desafio proposto por outra persona
- **THEN** esse desafio não aparece na resposta

### Requirement: Nenhuma leitura do desafio identifica Guerreiro(a)

Nenhuma resposta de `DesafioExtra` SHALL conter nome real, contato ou qualquer dado de
identificação de Guerreiro(a) — nem do destinatário do direcionado, nem de quem dispute o
aberto. (`RF-14-39`, `RN-14-20`, PRD-14 §12)

#### Scenario: A leitura do proponente não identifica ninguém

- **WHEN** o proponente lê os desafios que propôs
- **THEN** nenhuma resposta traz nome real, telefone, e-mail ou outro dado de identificação de
  Guerreiro(a)
