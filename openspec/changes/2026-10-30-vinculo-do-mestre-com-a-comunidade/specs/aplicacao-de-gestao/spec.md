# Spec Delta

## MODIFIED Requirements

### Requirement: O Admin agenda a aula com comunidade, data e horários

A App 03 SHALL permitir ao Admin agendar a aula informando **comunidade**, **data**, **horário
inicial**, **horário final**, o **ponto de apoio** em que ela acontece e **um ou mais Mestres**
que a ministram. A data e os horários SHALL trafegar com **fuso**, e a aplicação NEVER SHALL
enviar horário sem ele.

A aplicação SHALL oferecer, como ponto de apoio, apenas os da **comunidade escolhida**, e SHALL
apresentar no próprio campo a recusa do núcleo a horário final não posterior ao inicial e a
ponto de apoio de outra comunidade. Aula agendada sem recurso declarado SHALL nascer
**confirmada**, e a aplicação SHALL apresentar a situação como ela vem do núcleo, sem
recalculá-la.

A aplicação SHALL oferecer, como Mestres, os do **cadastro de Mestres da gestão**, sem recorte
por comunidade — é este agendamento que dá comunidade ao Mestre, de modo que filtrar por ela
deixaria o primeiro agendamento sem candidato algum. A aplicação NEVER SHALL confirmar
agendamento **sem Mestre**, apontando a falta no próprio campo. (`RF-02-30`)

O formulário SHALL permitir declarar, no mesmo ato, os **recursos que a aula consome**, como
pares de **tipo de recurso** e **quantidade**, escolhidos no catálogo de tipos da gestão. A
aplicação SHALL aceitar nenhum, um ou vários pares, SHALL permitir remover um par antes de
confirmar e NEVER SHALL enviar par com quantidade menor ou igual a zero, apontando a recusa no
próprio campo. Confirmado o agendamento, é o núcleo que reserva o que a aula consome; a
aplicação NEVER SHALL calcular saldo, reserva ou falta por conta própria. (`RF-02-12`,
`RF-02-30`, `RF-02-31`, `RN-02-09`, PRD-02 §5.1, documento 04 §1)

#### Scenario: Admin agenda a aula

- **WHEN** um Admin em sessão informa comunidade, data, horário inicial, horário final, ponto
  de apoio e ao menos um Mestre, e confirma
- **THEN** a aula passa a existir, confirmada, e a aplicação a apresenta na agenda

#### Scenario: Agendamento sem Mestre é apontado no campo

- **WHEN** o Admin confirma o agendamento sem escolher Mestre algum
- **THEN** a aplicação aponta a falta no próprio campo e nenhuma aula passa a existir

#### Scenario: Os Mestres oferecidos não são recortados por comunidade

- **WHEN** o Admin escolhe a comunidade e abre o campo de Mestres
- **THEN** todos os Mestres do cadastro lhe são oferecidos, vinculados àquela comunidade ou não

#### Scenario: Horário final anterior ao inicial é apontado no campo

- **WHEN** o Admin confirma o agendamento com horário final não posterior ao inicial
- **THEN** a aplicação aponta o erro no próprio campo e nenhuma aula passa a existir

#### Scenario: O ponto de apoio oferecido é o da comunidade escolhida

- **WHEN** o Admin escolhe a comunidade no formulário
- **THEN** só os pontos de apoio daquela comunidade lhe são oferecidos

#### Scenario: Quem não é Admin não alcança o agendamento

- **WHEN** um Mestre em sessão abre a agenda
- **THEN** o caminho de agendamento não lhe é oferecido

#### Scenario: O agendamento declara os recursos que a aula consome

- **WHEN** o Admin acrescenta dois pares de tipo de recurso e quantidade e confirma o
  agendamento
- **THEN** a aula passa a existir com os dois recursos declarados, e a aplicação apresenta a
  situação que o núcleo devolveu

#### Scenario: Quantidade não positiva é apontada no campo

- **WHEN** o Admin declara um recurso com quantidade zero
- **THEN** a aplicação aponta o erro no próprio campo e nenhuma aula passa a existir

#### Scenario: Aula sem saldo nasce pendente de lastro

- **WHEN** o Admin agenda a aula declarando mais de um recurso do que há disponível no ponto de
  apoio
- **THEN** a aplicação apresenta a aula como pendente de lastro, tal como o núcleo a devolveu
