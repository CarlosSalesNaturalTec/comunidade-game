## ADDED Requirements

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

#### Scenario: Desafio encerrado não recebe conclusão

- **WHEN** chega uma conclusão para um desafio encerrado
- **THEN** o núcleo a recusa

#### Scenario: A vigência vencida sozinha não encerra

- **WHEN** a vigência de um desafio publicado termina sem que o Admin o encerre
- **THEN** o desafio segue publicado e a recompensa segue reservada

## MODIFIED Requirements

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
