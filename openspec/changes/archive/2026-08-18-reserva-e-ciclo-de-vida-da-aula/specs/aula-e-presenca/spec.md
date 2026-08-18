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

Os **recursos que a aula consome** SHALL ser declarados no agendamento, como pares de tipo de
recurso e quantidade, e NÃO SHALL ser derivados da atividade prevista. A lista SHALL poder ser
vazia — aula que não consome recurso algum é agendada e nasce **confirmada**. Quantidade menor
ou igual a zero, ou tipo de recurso inexistente, SHALL ser recusada com **422**.

O agendamento SHALL ser exposto em rota de **Admin**, e é ele que dispara a reserva.
(`RF-01-20`, `RF-01-71`, `RF-01-16`, `RF-01-03`, `RF-07-08`, `RF-02-31`, `RN-07-33`,
`RN-07-01`, invariante 4 do documento 99 §6, PRD-01 §8, documento 04 §1, documento 05 §2)

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

#### Scenario: Horário final anterior ao inicial é recusado

- **WHEN** chega uma aula cujo horário final é anterior ou igual ao inicial
- **THEN** o núcleo responde 422 e nada é gravado

#### Scenario: Aula com recurso de quantidade zero é recusada

- **WHEN** chega uma aula declarando um recurso com quantidade zero ou negativa
- **THEN** o núcleo responde 422 indicando o campo e nada é gravado

#### Scenario: Aula sem recursos declarados nasce confirmada

- **WHEN** um Admin agenda uma aula sem declarar recurso algum
- **THEN** o núcleo grava a aula na situação confirmada, sem reserva alguma

## ADDED Requirements

### Requirement: O agendamento reserva, e a falta de saldo deixa a aula pendente de lastro

O núcleo SHALL avaliar, no agendamento, a **quantidade disponível** de cada tipo de recurso
declarado no ponto de apoio da aula. Havendo disponível para **todos** os recursos declarados,
o núcleo SHALL reservar cada quantidade e gravar a aula na situação **confirmada**. Faltando
disponível para **qualquer** parcela, o núcleo SHALL gravar a aula na situação **pendente de
lastro** e NÃO SHALL reservar quantidade alguma — nem a dos tipos que tinham saldo. A aula
pendente de lastro SHALL ser agendada assim mesmo, não recusada. (`RF-07-08`, `RN-07-01`,
`RF-02-31`, `RF-02-32`, invariante 9 do documento 99 §6, PRD-07 §5.3)

#### Scenario: Saldo suficiente confirma a aula

- **WHEN** um Admin agenda uma aula cujos recursos declarados têm todos disponível bastante
- **THEN** o núcleo reserva cada quantidade e grava a aula como confirmada

#### Scenario: Falta em um tipo deixa a aula pendente de lastro

- **WHEN** um Admin agenda uma aula com dois recursos declarados e apenas um deles tem
  disponível bastante
- **THEN** o núcleo grava a aula como pendente de lastro e não reserva nenhum dos dois

#### Scenario: Aula pendente de lastro não é recusada

- **WHEN** um Admin agenda uma aula sem disponível para o que ela consome
- **THEN** o núcleo grava a aula e responde com sucesso, indicando o que falta

### Requirement: A situação da aula tem cinco valores e o desfecho não se repete

O núcleo SHALL manter a **situação** da aula entre exatamente cinco valores: **prevista**,
**pendente de lastro**, **confirmada**, **realizada** e **cancelada**. A aula SHALL passar a
**realizada** pelo lançamento da atividade e a **cancelada** por ato de cancelamento. Aula já
**realizada** ou já **cancelada** SHALL recusar com **422** tanto um novo lançamento quanto um
novo cancelamento: o desfecho é único. (`RF-01-72`, `RF-07-09`, PRD-01 §8)

#### Scenario: Lançamento leva a aula a realizada

- **WHEN** a atividade realizada é lançada numa aula confirmada
- **THEN** a aula passa à situação realizada

#### Scenario: Aula realizada recusa novo lançamento

- **WHEN** chega um segundo lançamento de atividade para uma aula já realizada
- **THEN** o núcleo responde 422 e nada muda

#### Scenario: Aula cancelada recusa lançamento

- **WHEN** chega o lançamento de atividade de uma aula já cancelada
- **THEN** o núcleo responde 422 e nada muda

### Requirement: O cancelamento é de Admin ou de Mestre da comunidade da aula

O núcleo SHALL aceitar o cancelamento de aula agendada de um **Admin** ou de um **Mestre
vinculado à comunidade da aula**, sempre com **motivo** registrado. Mestre de outra comunidade
SHALL receber **403**, e qualquer outro papel SHALL receber **403**. Cancelamento sem motivo
SHALL ser recusado com **422**. O cancelamento SHALL **liberar** todas as reservas da aula,
devolvendo as quantidades à disponível, e SHALL ser gravado com autoria, data e hora. Esta é a
única escrita de gestão do Mestre, pela exceção do `RF-01-17`. (`RF-01-72`, `RF-01-17`,
`RF-02-95`, `RF-07-09`, `RF-01-03`, documento 05 §4)

#### Scenario: Mestre da comunidade cancela a aula

- **WHEN** um Mestre vinculado à comunidade da aula a cancela com motivo
- **THEN** o núcleo grava o cancelamento com a autoria dele e libera as reservas da aula

#### Scenario: Mestre de outra comunidade é recusado

- **WHEN** um Mestre não vinculado à comunidade da aula tenta cancelá-la
- **THEN** o núcleo responde 403 e nada é gravado

#### Scenario: Cancelamento sem motivo é recusado

- **WHEN** chega um cancelamento de aula sem motivo declarado
- **THEN** o núcleo responde 422 e nada é gravado

#### Scenario: Guerreiro(a) não cancela aula

- **WHEN** um Guerreiro(a) tenta cancelar uma aula
- **THEN** o núcleo responde 403 e nada é gravado
