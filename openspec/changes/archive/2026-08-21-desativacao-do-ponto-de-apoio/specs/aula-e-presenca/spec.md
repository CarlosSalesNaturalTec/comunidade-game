## MODIFIED Requirements

### Requirement: Aula é agendada com comunidade, data e horários

O núcleo SHALL manter a **aula** com **comunidade**, **ponto de apoio**, **data**, **horário
inicial**, **horário final**, os **recursos que ela consome** e a **situação**. Agendar aula
SHALL ser operação de **Admin**; qualquer outro papel SHALL receber **403**. Aula sem
comunidade, **sem ponto de apoio**, sem data ou sem um dos horários SHALL ser recusada com
**422**, indicando o campo em falta, e aula cujo horário final não seja posterior ao inicial
SHALL ser recusada com **422**.

O **ponto de apoio** declarado SHALL pertencer à **mesma comunidade** da aula; aula cujo ponto de
apoio seja de outra comunidade SHALL ser recusada com **422**. É o ponto de apoio que liga a
aula ao saldo de recursos guardado naquele espaço.

O ponto de apoio declarado SHALL estar **ativo**; aula que declare ponto de apoio **inativo**
SHALL ser recusada com **422**. Espaço que saiu de operação não recebe aula nova, e aula já
agendada antes da desativação NEVER SHALL perder o vínculo com ele — a desativação é bloqueada
justamente enquanto houver aula futura ali.

Os **recursos que a aula consome** SHALL ser declarados no agendamento, como pares de tipo de
recurso e quantidade, e NÃO SHALL ser derivados da atividade prevista. A lista SHALL poder ser
vazia — aula que não consome recurso algum é agendada e nasce **confirmada**. Quantidade menor
ou igual a zero, ou tipo de recurso inexistente, SHALL ser recusada com **422**.

O agendamento SHALL ser exposto em rota de **Admin**, e é ele que dispara a reserva.
(`RF-01-20`, `RF-01-71`, `RF-01-16`, `RF-01-03`, `RF-07-08`, `RF-07-47`, `RF-02-31`,
`RN-07-33`, `RN-07-01`, invariante 4 do documento 99 §6, PRD-01 §8, documento 04 §1,
documento 05 §2)

#### Scenario: Admin agenda a aula

- **WHEN** um Admin agenda uma aula com comunidade, ponto de apoio, data, horário inicial e
  horário final
- **THEN** o núcleo grava a aula com a autoria de quem a agendou

#### Scenario: Mestre não agenda aula

- **WHEN** um Mestre tenta agendar uma aula
- **THEN** o núcleo responde 403 e nada é gravado

#### Scenario: Aula sem comunidade é recusada

- **WHEN** chega uma aula sem comunidade declarada
- **THEN** o núcleo responde 422 indicando o campo em falta e nada é gravado

#### Scenario: Aula sem ponto de apoio é recusada

- **WHEN** chega uma aula sem ponto de apoio declarado
- **THEN** o núcleo responde 422 indicando o campo em falta e nada é gravado

#### Scenario: Ponto de apoio de outra comunidade é recusado

- **WHEN** chega uma aula cujo ponto de apoio pertence a comunidade diferente da comunidade da
  aula
- **THEN** o núcleo responde 422 e nada é gravado

#### Scenario: Ponto de apoio inativo é recusado

- **WHEN** chega uma aula cujo ponto de apoio está inativo
- **THEN** o núcleo responde 422 e nenhuma aula passa a existir

#### Scenario: Horário final anterior ao inicial é recusado

- **WHEN** chega uma aula cujo horário final é anterior ou igual ao inicial
- **THEN** o núcleo responde 422 e nada é gravado

#### Scenario: Aula com recurso de quantidade zero é recusada

- **WHEN** chega uma aula declarando um recurso com quantidade zero ou negativa
- **THEN** o núcleo responde 422 indicando o campo e nada é gravado

#### Scenario: Aula sem recursos declarados nasce confirmada

- **WHEN** um Admin agenda uma aula sem declarar recurso algum
- **THEN** o núcleo grava a aula na situação confirmada, sem reserva alguma
