## Purpose

O desafio extra é o que o Apoiador propõe a uma trilha em andamento: uma tarefa a mais, com
recompensa provida por ele e pontos que correm à parte da pontuação regular. Esta capacidade
cobre a proposta — o que ela declara, o que a plataforma nunca confirma sobre o destinatário, o
lastro sem o qual ela não se publica e os estados por onde ela passa até virar desafio.

## Requirements

### Requirement: A proposta se vincula a uma trilha em andamento e declara o que oferece

O núcleo SHALL registrar o `DesafioExtra` vinculando **proponente**, **trilha em andamento** e,
opcionalmente, **missão**, com **recompensa**, **quantidade disponível**, **critério de
atribuição** e **período de vigência**. Trilha que não esteja em andamento SHALL ser recusada
com **422**. NEVER SHALL existir teto de desafios simultâneos: o controle é a aprovação caso a
caso. (`RF-14-29`, `RF-14-30`, `RN-14-15`, PRD-14 §8)

#### Scenario: Proposta completa é registrada

- **WHEN** um Apoiador propõe um desafio a uma trilha em andamento, com recompensa, quantidade,
  critério de atribuição e vigência
- **THEN** o núcleo registra a proposta com o proponente, a trilha e o que ela oferece

#### Scenario: Trilha que não está em andamento é recusada

- **WHEN** a proposta declara uma trilha que não está em andamento
- **THEN** o núcleo responde 422 e nenhuma proposta passa a existir

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
aprovação do Admin**, **publicado** e **recusado**, nascendo toda proposta em validação do
Mestre. NEVER SHALL publicar desafio que não tenha passado pela validação do Mestre da trilha e
pela aprovação de Admin. A recusa em qualquer etapa SHALL guardar o **motivo**, e a leitura do
proponente SHALL devolvê-lo. (`RF-14-35`, `RF-14-36`, `RN-14-13`)

#### Scenario: Proposta nasce em validação do Mestre

- **WHEN** uma proposta é registrada
- **THEN** a situação dela é "em validação do Mestre"

#### Scenario: O proponente lê o motivo da recusa

- **WHEN** o proponente lê um desafio recusado
- **THEN** a resposta traz a situação de recusado e o motivo registrado

### Requirement: A conclusão do desafio extra fica registrada

O núcleo SHALL manter o registro da **conclusão** de um `DesafioExtra` por um Guerreiro(a),
com o desafio, quem concluiu, a **data do fato**, se a recompensa foi entregue e quantos
**pontos extras** o desafio rendeu. O registro SHALL ser **somente inserção**: NEVER SHALL
haver rota que o altere ou o retire. Um mesmo Guerreiro(a) NEVER SHALL ter duas conclusões
registradas para o mesmo desafio. NEVER SHALL existir conclusão de desafio que não esteja
**publicado**. (`RF-14-42`, `RF-14-37`, 04 §3)

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

### Requirement: Nenhuma leitura do desafio identifica Guerreiro(a)

Nenhuma resposta de `DesafioExtra` SHALL conter nome real, contato ou qualquer dado de
identificação de Guerreiro(a) — nem do destinatário do direcionado, nem de quem dispute o
aberto. (`RF-14-39`, `RN-14-20`, PRD-14 §12)

#### Scenario: A leitura do proponente não identifica ninguém

- **WHEN** o proponente lê os desafios que propôs
- **THEN** nenhuma resposta traz nome real, telefone, e-mail ou outro dado de identificação de
  Guerreiro(a)
