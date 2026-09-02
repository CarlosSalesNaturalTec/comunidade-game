## ADDED Requirements

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

## MODIFIED Requirements

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
