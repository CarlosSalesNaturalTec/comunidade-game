## ADDED Requirements

### Requirement: O Admin cadastra o ponto de apoio da comunidade

A App 03 SHALL permitir ao Admin cadastrar o ponto de apoio informando **nome** e a
**comunidade** a que ele pertence, e SHALL apresentar os pontos de apoio já cadastrados antes
de oferecer o cadastro, para que ele saiba o que já há. A apresentação SHALL ser **lista
densa**, no temperamento Operação, como a das comunidades.

O ponto de apoio SHALL nascer **sem responsável pelo acervo**, e a aplicação NEVER SHALL
apresentar essa ausência como falha: a designação é ato posterior e não é desta fatia.
(`RF-07-47`, `RF-07-49`, `RN-07-34`, documento 15 §6)

#### Scenario: Admin cadastra o ponto de apoio

- **WHEN** um Admin em sessão informa nome e comunidade e confirma
- **THEN** o ponto de apoio passa a existir e a aplicação o apresenta entre os existentes

#### Scenario: Campo obrigatório em falta

- **WHEN** o Admin confirma o cadastro com nome ou comunidade vazios
- **THEN** a aplicação aponta o campo em falta, no próprio campo, e nenhum ponto de apoio
  passa a existir

#### Scenario: Ponto de apoio sem responsável não é apresentado como pendência

- **WHEN** a lista apresenta um ponto de apoio ainda sem responsável pelo acervo
- **THEN** a ausência aparece como informação, e não como aviso de erro

#### Scenario: Quem não é Admin não alcança o cadastro

- **WHEN** um Mestre em sessão abre a área de pontos de apoio
- **THEN** o caminho de cadastro não lhe é oferecido, e a recusa do núcleo, se ocorrer, é
  apresentada em linguagem simples

### Requirement: O Admin agenda a aula com comunidade, data e horários

A App 03 SHALL permitir ao Admin agendar a aula informando **comunidade**, **data**, **horário
inicial**, **horário final** e o **ponto de apoio** em que ela acontece. A data e os horários
SHALL trafegar com **fuso**, e a aplicação NEVER SHALL enviar horário sem ele.

A aplicação SHALL oferecer, como ponto de apoio, apenas os da **comunidade escolhida**, e SHALL
apresentar no próprio campo a recusa do núcleo a horário final não posterior ao inicial e a
ponto de apoio de outra comunidade. Aula agendada sem recurso declarado SHALL nascer
**confirmada**, e a aplicação SHALL apresentar a situação como ela vem do núcleo, sem
recalculá-la. (`RF-02-12`, `RF-02-30`, `RN-02-09`, PRD-02 §5.1)

#### Scenario: Admin agenda a aula

- **WHEN** um Admin em sessão informa comunidade, data, horário inicial, horário final e ponto
  de apoio, e confirma
- **THEN** a aula passa a existir, confirmada, e a aplicação a apresenta na agenda

#### Scenario: Horário final anterior ao inicial é apontado no campo

- **WHEN** o Admin confirma o agendamento com horário final não posterior ao inicial
- **THEN** a aplicação aponta o erro no próprio campo e nenhuma aula passa a existir

#### Scenario: O ponto de apoio oferecido é o da comunidade escolhida

- **WHEN** o Admin escolhe a comunidade no formulário
- **THEN** só os pontos de apoio daquela comunidade lhe são oferecidos

#### Scenario: Quem não é Admin não alcança o agendamento

- **WHEN** um Mestre em sessão abre a agenda
- **THEN** o caminho de agendamento não lhe é oferecido

### Requirement: A aplicação apresenta a agenda das aulas

A App 03 SHALL apresentar as aulas com **comunidade**, **ponto de apoio**, **data**, **horários**
e **situação**, em lista densa, filtráveis por comunidade e por período. A aula **pendente de
lastro** SHALL se distinguir da **confirmada** na apresentação, e a aula **cancelada** SHALL
exibir o **motivo** registrado.

O **Mestre** SHALL ler a agenda das comunidades a que está vinculado; a aplicação NEVER SHALL
lhe apresentar aula de comunidade a que não pertence. (`RF-02-12`, `RF-01-18`, `RN-02-09`,
`RN-02-20`, documento 15 §6)

#### Scenario: A agenda distingue as situações

- **WHEN** a agenda apresenta uma aula confirmada e uma pendente de lastro
- **THEN** cada uma aparece com a sua situação, distinguíveis sem depender só de cor

#### Scenario: Aula cancelada mostra o motivo

- **WHEN** a agenda apresenta uma aula cancelada
- **THEN** o motivo registrado no cancelamento aparece junto dela

#### Scenario: Mestre lê só a agenda das suas comunidades

- **WHEN** um Mestre vinculado a uma comunidade abre a agenda
- **THEN** só aparecem as aulas daquela comunidade

### Requirement: A aula agendada é cancelada com motivo

A App 03 SHALL permitir o cancelamento da aula agendada ao **Admin** e ao **Mestre da comunidade
da aula**, exigindo o **motivo** e NEVER SHALL aceitar o cancelamento sem ele. A aplicação SHALL
apresentar, antes de confirmar, que o cancelamento **libera os recursos reservados** e que ele
não se desfaz.

Cancelada a aula, a aplicação SHALL apresentá-la com a situação cancelada e o motivo, e NEVER
SHALL oferecer o cancelamento de aula que já teve desfecho. (`RF-02-95`, `RF-01-72`,
`RN-02-20`, PRD-02 §5.4)

#### Scenario: Admin cancela a aula com motivo

- **WHEN** um Admin em sessão confirma o cancelamento informando o motivo
- **THEN** a aula passa a cancelada, com o motivo, e a agenda a apresenta assim

#### Scenario: Cancelamento sem motivo é recusado no campo

- **WHEN** quem cancela confirma sem informar o motivo
- **THEN** a aplicação aponta o campo em falta e a aula segue como estava

#### Scenario: Mestre da comunidade da aula cancela

- **WHEN** um Mestre vinculado à comunidade da aula confirma o cancelamento com motivo
- **THEN** a aula passa a cancelada, e a aplicação não lhe oferece nenhuma outra escrita da
  agenda

#### Scenario: Aula com desfecho não oferece cancelamento

- **WHEN** a agenda apresenta uma aula já cancelada ou já realizada
- **THEN** o caminho de cancelamento não é oferecido para ela
