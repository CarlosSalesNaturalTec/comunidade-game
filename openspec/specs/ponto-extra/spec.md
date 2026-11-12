## Purpose

O ponto extra reconhece caráter — mérito, cuidado, colaboração e protagonismo — numa conta
separada do percurso, para que trocar por recompensa avulsa nunca enfraqueça o personagem nem
apague histórico.

## Requirements

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

### Requirement: Fonte dupla credita ponto regular e ponto extra juntos

O núcleo SHALL creditar ponto extra, na mesma operação que credita ponto regular, quando a fonte
do documento 11 §5 é declarada **regular e extra** — Resultado com desfecho "realizada com
mérito" ou "mérito extra por auxílio aos colegas". (`RF-01-56`, 11 §5)

#### Scenario: "Realizada com mérito" credita as duas naturezas

- **WHEN** um Resultado é lançado com desfecho "realizada com mérito"
- **THEN** o núcleo credita o adicional de mérito ao ponto regular da trilha **e** ao acumulado e
  saldo disponível de ponto extra, na mesma operação

#### Scenario: "Mérito extra por auxílio aos colegas" credita as duas naturezas

- **WHEN** um Resultado é lançado com desfecho "mérito extra por auxílio aos colegas"
- **THEN** o núcleo credita o adicional ao ponto regular da trilha **e** ao acumulado e saldo
  disponível de ponto extra, na mesma operação

### Requirement: Fonte só extra credita ponto extra sem tocar o ponto regular

O núcleo SHALL creditar **apenas ponto extra**, sem creditar ponto regular algum, quando a
fonte do documento 11 §5 é declarada **só extra**. A **proposta de evolução adotada pela
gestão** é essa fonte no Ciclo 01: adotada a sugestão, o núcleo SHALL creditar **20 pontos
extras** ao autor, no **acumulado** e no **saldo disponível**, na mesma operação em que grava
o desfecho da fila de avaliação. O crédito SHALL ocorrer uma única vez por sugestão.
(`RF-01-56`, `RF-01-57`, 11 §5)

#### Scenario: Proposta adotada credita 20 extras e nenhum ponto regular

- **WHEN** um Admin conclui a avaliação de uma sugestão como **adotada**
- **THEN** o núcleo credita 20 ao acumulado e ao saldo disponível de ponto extra do autor, e
  **nenhum ponto regular** é creditado em trilha ou poder

#### Scenario: Sugestão não adotada não credita nada

- **WHEN** um Admin conclui a avaliação de uma sugestão como **não adotada**
- **THEN** o núcleo não credita ponto extra nem ponto regular

#### Scenario: Registrar a sugestão não pontua

- **WHEN** uma persona registra uma sugestão
- **THEN** o núcleo não credita ponto algum pelo registro

#### Scenario: Reavaliação não credita duas vezes

- **WHEN** o desfecho **adotada** é gravado para uma sugestão que já creditou os extras
- **THEN** o núcleo não credita novamente

### Requirement: O Guerreiro(a) lê as duas contas de ponto extra, e ninguém as lê por ele

O núcleo SHALL devolver ao **Guerreiro(a) em sessão** as suas duas contas de ponto extra — o
**acumulado** e o **saldo disponível** —, numa rota que NEVER SHALL receber identificador de
persona: ela alcança apenas quem está autenticado nela. Persona de papel **Mestre**, **Admin**,
**Apoiador** ou **responsável** SHALL receber **403**: nenhum adulto lê o saldo de uma criança,
nem o Mestre que entrega o item da troca.

Guerreiro(a) que ainda não recebeu ponto extra algum SHALL receber as duas contas em **zero**,
e não um erro — quem nunca ganhou tem saldo, e ele é nenhum.

A leitura NEVER SHALL alcançar o contrato de leitura dos jogos, que segue devolvendo apenas o
**acumulado**, sem persona e sem sessão: o saldo disponível continua fora dele, e trocar por
recompensa avulsa continua sem enfraquecer o personagem. (`RF-04-51`, `RF-05-82`, `RF-01-22`,
`RN-01-39`, `RN-01-40`, `RN-01-41`, invariantes 8 e 23)

#### Scenario: O Guerreiro(a) lê as próprias contas

- **WHEN** um Guerreiro(a) em sessão consulta os seus pontos extras
- **THEN** o núcleo devolve o acumulado e o saldo disponível dele, separados

#### Scenario: Guerreiro(a) sem ponto extra tem saldo zero

- **WHEN** um Guerreiro(a) que nunca recebeu ponto extra consulta os seus pontos extras
- **THEN** o núcleo devolve acumulado zero e saldo disponível zero, sem erro

#### Scenario: O Mestre não lê o saldo de uma criança

- **WHEN** um Mestre em sessão tenta consultar os pontos extras por essa rota
- **THEN** o núcleo responde 403 e nada do saldo é devolvido

#### Scenario: O Admin não lê o saldo por esta rota

- **WHEN** um Admin em sessão tenta consultar os pontos extras por essa rota
- **THEN** o núcleo responde 403 e nada do saldo é devolvido

#### Scenario: A rota não aponta para outra criança

- **WHEN** um Guerreiro(a) em sessão tenta alcançar o saldo de outro Guerreiro(a)
- **THEN** não há como fazê-lo: a rota não recebe identificador de persona e devolve sempre as
  contas de quem está em sessão

#### Scenario: O contrato dos jogos segue sem o saldo

- **WHEN** o App 04 lê o progresso de um Guerreiro(a) para montar o personagem
- **THEN** a resposta traz o acumulado de pontos extras e NÃO traz o saldo disponível

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

### Requirement: O cuidado com o bem recebido credita 1 ponto extra

A **conservação** validada de um bem recebido e a **customização** aprovada de um kit são fontes
**só extra** do documento 11 §5: cada uma SHALL creditar **1 ponto extra** — e **nenhum ponto
regular** — ao Guerreiro(a), no **acumulado** e no **saldo disponível**, na mesma operação que
grava a validação ou o julgamento. O crédito SHALL ocorrer uma única vez por ato, e o mesmo bem
SHALL pontuar no máximo uma vez por encontro, entre as duas fontes (capability
`conservacao-do-bem-recebido`). (`RF-01-85`, `RF-01-87`, `RN-01-66`, 11 §5)

#### Scenario: A conservação credita 1 extra e nenhum regular

- **WHEN** o Mestre da aula valida a conservação de um bem recebido
- **THEN** o acumulado e o saldo disponível do Guerreiro(a) sobem 1, e nenhum ponto regular é
  creditado

#### Scenario: A customização aprovada credita 1 extra e nenhum regular

- **WHEN** o Mestre da aula aprova a customização de um kit
- **THEN** o acumulado e o saldo disponível do Guerreiro(a) sobem 1, e nenhum ponto regular é
  creditado

#### Scenario: A reprovação não credita

- **WHEN** o Mestre da aula reprova a customização de um kit
- **THEN** o núcleo não credita ponto algum
