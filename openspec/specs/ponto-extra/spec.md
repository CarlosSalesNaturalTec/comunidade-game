## Purpose

O ponto extra reconhece caráter — mérito, cuidado, colaboração e protagonismo — numa conta
separada do percurso, para que trocar por recompensa avulsa nunca enfraqueça o personagem nem
apague histórico.

## Requirements

### Requirement: Ponto extra vive em duas contas que nunca se confundem

O núcleo SHALL manter, por Guerreiro(a), duas contas de ponto extra: o **acumulado** — tudo o que
já foi ganho, que **nunca decresce** — e o **saldo disponível** — o que ainda não foi trocado, que
**nunca fica negativo**. Nesta fatia as duas contas **só recebem crédito**; a operação de débito
nasce com a troca por recompensa avulsa (PRD-07) e herda esta mesma trava de não ficar negativo.
(`RF-01-56`, `RN-01-39`, `RN-01-40`, 11 §5)

#### Scenario: Crédito aumenta as duas contas juntas

- **WHEN** um Resultado credita ponto extra a um Guerreiro(a)
- **THEN** o núcleo aumenta o acumulado e o saldo disponível pelo mesmo valor

#### Scenario: Acumulado nunca decresce

- **WHEN** qualquer operação tenta reduzir o acumulado de pontos extras
- **THEN** o núcleo recusa a operação

#### Scenario: Saldo disponível nunca aceita valor negativo

- **WHEN** qualquer operação resultaria em saldo disponível negativo
- **THEN** o núcleo recusa a operação

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
