## MODIFIED Requirements

### Requirement: Ponto extra vive em duas contas que nunca se confundem

O núcleo SHALL manter, por Guerreiro(a), duas contas de ponto extra: o **acumulado** — tudo o que
já foi ganho, que **nunca decresce**, salvo o **estorno da presença anulada** — e o **saldo
disponível** — o que ainda não foi trocado, que **nunca fica negativo**. O acumulado SHALL
receber crédito e, como **única redução**, o estorno da presença anulada; qualquer outra
redução SHALL ser recusada, em qualquer via — inclusive fora do ORM. O saldo disponível SHALL
receber crédito e dois débitos: a **troca por recompensa avulsa**, que debita o preço cobrado
sem tocar o acumulado, e o **estorno da presença anulada**. Débito de troca que deixaria o
saldo disponível negativo SHALL ser recusado, em qualquer via — inclusive fora do ORM.
(`RF-01-56`, `RN-01-39`, `RN-01-40`, `RN-01-64`, `RF-07-36`, 11 §5, invariante 23)

#### Scenario: Crédito aumenta as duas contas juntas

- **WHEN** um Resultado credita ponto extra a um Guerreiro(a)
- **THEN** o núcleo aumenta o acumulado e o saldo disponível pelo mesmo valor

#### Scenario: Acumulado nunca decresce

- **WHEN** qualquer operação que não seja o estorno da presença anulada tenta reduzir o
  acumulado de pontos extras
- **THEN** o núcleo recusa a operação

#### Scenario: Saldo disponível nunca aceita valor negativo

- **WHEN** qualquer operação resultaria em saldo disponível negativo
- **THEN** o núcleo recusa a operação

#### Scenario: A troca debita só o saldo disponível

- **WHEN** uma troca por recompensa avulsa cobra 40 pontos extras de um Guerreiro(a) com
  acumulado 300 e saldo disponível 100
- **THEN** o saldo disponível passa a 60 e o acumulado permanece 300

#### Scenario: A troca não debita além do saldo disponível

- **WHEN** uma troca cobraria mais pontos extras do que o saldo disponível do Guerreiro(a)
- **THEN** o núcleo recusa o débito e o saldo permanece exatamente como estava

## ADDED Requirements

### Requirement: A presença registrada credita 5 pontos extras, e a anulação os estorna

O núcleo SHALL creditar **5 pontos extras** — e **nenhum ponto regular** — ao Guerreiro(a), no
**acumulado** e no **saldo disponível**, na mesma operação que grava a presença dele numa aula
presencial, **qualquer que seja o modo de comprovação** (reconhecimento ou confirmação). O
crédito SHALL ocorrer **uma vez por presença**: o reenvio que devolve a presença já gravada
NEVER SHALL creditar de novo.

Anulada a presença, o núcleo SHALL **estornar** o que ela creditou, na mesma operação que grava
a anulação: o acumulado SHALL perder exatamente esse valor, e o saldo disponível SHALL perder o
mesmo valor **até parar em zero**, sem recusar a anulação por falta de saldo. A presença
correta registrada em seguida, para o mesmo par (aula, Guerreiro(a)), SHALL creditar como
qualquer outra.

Presença gravada **antes da entrega desta regra** NEVER SHALL creditar nem estornar: não há
crédito retroativo, e a anulação dela não toca o ponto extra. (`RF-01-82`, `RF-01-83`,
`RN-01-64`, `RN-01-65`, `RF-01-20`, 11 §§1 e 5, invariante 23)

#### Scenario: Presença por reconhecimento credita 5 extras

- **WHEN** a presença de um Guerreiro(a) é registrada por reconhecimento
- **THEN** o núcleo grava a presença e aumenta em 5 o acumulado e o saldo disponível dele, sem
  creditar ponto regular

#### Scenario: Presença por confirmação credita 5 extras

- **WHEN** um Mestre confirma pelo nick a presença de um Guerreiro(a)
- **THEN** o núcleo aumenta em 5 o acumulado e o saldo disponível dele

#### Scenario: O reenvio da mesma presença não credita duas vezes

- **WHEN** o App 01 reenvia a presença de um Guerreiro(a) numa aula em que ela já está gravada
- **THEN** o núcleo devolve a presença existente e as duas contas permanecem como estavam

#### Scenario: Anulação estorna das duas contas

- **WHEN** um Admin anula a presença de um Guerreiro(a) com acumulado 30 e saldo disponível 12,
  e a presença creditou 5
- **THEN** o acumulado passa a 25 e o saldo disponível a 7

#### Scenario: Estorno com o saldo já trocado para em zero

- **WHEN** um Admin anula a presença de um Guerreiro(a) com saldo disponível 2, e a presença
  creditou 5
- **THEN** o núcleo grava a anulação, o acumulado perde 5 e o saldo disponível fica em zero

#### Scenario: A presença correta, depois da anulação, credita de novo

- **WHEN** a presença de um Guerreiro(a) numa aula é anulada e a presença correta é registrada
  em seguida para o mesmo par
- **THEN** a nova presença credita 5 extras, e o saldo final é o de uma presença só

#### Scenario: Presença anterior à regra não estorna

- **WHEN** um Admin anula uma presença gravada antes da entrega desta regra
- **THEN** o núcleo grava a anulação e as duas contas de ponto extra permanecem como estavam
