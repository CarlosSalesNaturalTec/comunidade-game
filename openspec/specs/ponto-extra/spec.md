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
