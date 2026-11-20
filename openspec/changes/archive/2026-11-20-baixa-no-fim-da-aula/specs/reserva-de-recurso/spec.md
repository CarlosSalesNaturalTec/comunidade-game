## REMOVED Requirements

### Requirement: A reserva sai por baixa ou por liberação, e nunca por decurso de prazo

**Reason**: a reserva da aula passou a ser baixada pelo sistema no fim do horário, e não mais pelo lançamento (`RF-07-09`, `RN-07-43`).

**Migration**: substituído por "A reserva da aula sai pela baixa no fim do horário ou pela liberação".

## ADDED Requirements

### Requirement: A reserva da aula sai pela baixa no fim do horário ou pela liberação

O núcleo SHALL dar à reserva **de aula** exatamente duas saídas: a **baixa**, feita pelo
**sistema** quando passa o horário de fim da aula, que a leva a **consumida** e gera o lançamento
de débito correspondente; e a **liberação**, pelo cancelamento da aula, que a leva a
**liberada** e devolve a quantidade à disponível. A reserva **de desafio extra** SHALL sair pela
**liberação**, no **encerramento** do desafio pelo Admin. Nenhum ato humano SHALL dar baixa na
reserva de aula, e o desafio extra cuja vigência venceu sem encerramento SHALL manter a reserva.
Toda saída SHALL registrar autor e momento; na baixa do sistema, o autor é o da aula com o papel
**sistema**. (`RF-07-09`, `RN-07-43`, `RF-07-40`, `RF-01-03`, PRD-07 §5.3, documento 04 §1)

#### Scenario: O fim do horário leva a reserva a consumida

- **WHEN** passa o horário de fim de uma aula confirmada com reservas e a varredura roda
- **THEN** cada reserva passa a consumida e o saldo cai pelo débito correspondente, com o papel
  sistema

#### Scenario: Cancelamento devolve a quantidade à disponível

- **WHEN** uma aula com 4 unidades reservadas é cancelada
- **THEN** as reservas passam a liberada e a quantidade disponível volta a incluir as 4

#### Scenario: Encerramento do desafio devolve a quantidade à disponível

- **WHEN** o Admin encerra um desafio extra publicado cuja recompensa segue reservada
- **THEN** a reserva passa a liberada e a quantidade disponível volta a incluir a recompensa

#### Scenario: Desafio com vigência vencida mantém a reserva

- **WHEN** a vigência de um desafio extra publicado termina sem que o Admin o encerre
- **THEN** a reserva segue no estado reservada e a quantidade disponível segue reduzida
