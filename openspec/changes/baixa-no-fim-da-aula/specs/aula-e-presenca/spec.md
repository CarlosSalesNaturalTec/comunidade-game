## REMOVED Requirements

### Requirement: A situação da aula tem cinco valores e o desfecho não se repete

**Reason**: a aula não tem mais fechamento; o lançamento não leva a aula a realizada, e a
situação ganha o sexto valor, realizada sem lastro (`RF-01-91`, `RN-07-43`).

**Migration**: substituído por "A situação da aula tem seis valores e o horário encerra a aula".

## ADDED Requirements

### Requirement: A situação da aula tem seis valores e o horário encerra a aula

O núcleo SHALL manter a **situação** da aula entre exatamente seis valores: **prevista**,
**pendente de lastro**, **confirmada**, **realizada**, **realizada sem lastro** e **cancelada**.
Passado o horário de fim, a aula confirmada ou prevista SHALL passar a **realizada** e a
pendente de lastro a **realizada sem lastro**, pela varredura do sistema, sem ato de fechamento;
a aula passa a **cancelada** só por ato de cancelamento. Aula realizada, realizada sem lastro ou
cancelada SHALL recusar novo cancelamento com **422**, e a aula cujo horário de fim já passou
também. (`RF-01-91`, `RF-07-55`, `RN-07-43`, `RF-01-72`, `RN-02-09`, PRD-01 §8)

#### Scenario: O fim do horário leva a aula confirmada a realizada

- **WHEN** passa o horário de fim de uma aula confirmada e a varredura roda
- **THEN** a aula passa à situação realizada

#### Scenario: A aula pendente vira realizada sem lastro e sai das necessidades

- **WHEN** passa o horário de fim de uma aula pendente de lastro e a varredura roda
- **THEN** a aula passa a realizada sem lastro, nada é baixado, e a falta dela some das
  necessidades

#### Scenario: Aula que já terminou não se cancela

- **WHEN** chega o cancelamento de uma aula cujo horário de fim já passou
- **THEN** o núcleo responde 422 e nada muda

### Requirement: A varredura das aulas vencidas roda no comando periódico e sob demanda

O núcleo SHALL encerrar as aulas vencidas por uma **varredura** idempotente, que roda no comando
periódico `python -m nucleo.manutencao` e no começo da leitura da agenda, das necessidades e do
saldo do ponto de apoio, do agendamento, do cancelamento e da tentativa de reserva. Duas
varreduras simultâneas NEVER SHALL baixar a mesma reserva duas vezes, e a aula que não se pode
valorar fica para a próxima, sem derrubar a operação que disparou a varredura.
(`RF-01-91`, `RF-07-09`, decisão do fundador de 2026-11-20)

#### Scenario: A leitura da agenda encerra a aula vencida

- **WHEN** a gestão lê a agenda depois do fim de uma aula confirmada que nenhuma varredura
  alcançou
- **THEN** a aula vem realizada e a reserva dela já está baixada

#### Scenario: A varredura repetida não baixa de novo

- **WHEN** a varredura roda duas vezes sobre a mesma aula vencida
- **THEN** só existe um débito por reserva

### Requirement: A aula terminada antes da implantação tem a reserva liberada

A migração que implanta a baixa no fim da aula SHALL tratar a aula cujo horário de fim já passou
e que ainda não tem desfecho: a reserva **reservada** SHALL passar a **liberada**, sem débito, e a
aula SHALL passar a **realizada** — ou a **realizada sem lastro**, se estava pendente de lastro.
Aula já realizada ou cancelada SHALL ficar como está. (`RF-07-56`)

#### Scenario: A aula antiga não recebe baixa

- **WHEN** a migração roda sobre uma aula confirmada já terminada que reserva 20 unidades
- **THEN** a reserva passa a liberada, nenhum débito é gravado, o saldo não muda e a aula passa a
  realizada
