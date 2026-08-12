## Purpose

O motor de pontuação regular — pontos, níveis e badges por trilha ou poder, derivados do
Resultado — é o que a vitrine, os cards públicos e o App 04 vão ler sobre a progressão de cada
Guerreiro(a).

## ADDED Requirements

### Requirement: Ponto regular é creditado por trilha ou poder e nunca debitado

O núcleo SHALL creditar **ponto regular** por **trilha ou poder** — nunca globalmente — a partir
de um Resultado, conforme a fonte e o valor da tabela do documento 11 §5. O ponto regular SHALL
**nunca ser debitado**, em nenhuma operação. (`RF-01-21`, `RN-01-38`, 11 §5)

#### Scenario: Resultado "realizada" credita o valor da atividade

- **WHEN** um Resultado é lançado com desfecho "realizada"
- **THEN** o núcleo credita, à trilha ou ao poder correspondente, o ponto regular da fonte da
  atividade

#### Scenario: Resultado "realizada com mérito" credita o valor mais o adicional de mérito

- **WHEN** um Resultado é lançado com desfecho "realizada com mérito"
- **THEN** o núcleo credita o ponto regular da atividade acrescido do adicional de mérito da
  tabela do documento 11 §5

#### Scenario: Ponto regular não aceita débito

- **WHEN** qualquer operação tenta reduzir o saldo de ponto regular de um Guerreiro(a)
- **THEN** o núcleo recusa a operação

### Requirement: Nível é percurso por trilha ou poder e nunca regride

O núcleo SHALL manter o **nível** por trilha ou poder, derivado do **percurso das missões
obrigatórias desbloqueadas** — nunca do total de pontos acumulado (11 §6). Nesta capacidade o
núcleo SHALL certificar os níveis **1** (inscrito na trilha e primeira atividade realizada), **2**
(um terço das missões obrigatórias desbloqueadas) e **4** (todas as obrigatórias desbloqueadas e
ao menos um Resultado com mérito extra por auxílio aos colegas). Nível conquistado SHALL **nunca
regredir**. (`RF-01-21`, 11 §6)

#### Scenario: Primeira atividade realizada alcança o nível 1

- **WHEN** o Guerreiro(a) tem a primeira atividade da trilha com Resultado registrado
- **THEN** o núcleo certifica o nível 1 naquela trilha

#### Scenario: Um terço das obrigatórias desbloqueadas alcança o nível 2

- **WHEN** o Guerreiro(a) tem Resultado registrado para um terço das missões obrigatórias da
  trilha
- **THEN** o núcleo certifica o nível 2 naquela trilha

#### Scenario: Nível conquistado não regride

- **WHEN** um Guerreiro(a) já certificado num nível deixa de atender ao critério que o levou lá
- **THEN** o núcleo mantém o nível já certificado

### Requirement: Badge é conquistado por trilha ou por poder, nunca global

O núcleo SHALL conceder **badge** sempre vinculado a uma trilha ou a um poder, nunca de forma
global (11 §7). Nesta capacidade o núcleo SHALL conceder o **badge de nível** a cada nível
certificado e o **badge de valores/causas** a Resultado de atividade de natureza "valores e
temas transversais". O badge de conquista **Guardião do Acervo** não nasce de Resultado — ele
depende de encontro presencial identificável (`Aula/Agenda`) — e fica para a fatia que o
entregar. (`RF-01-21`, 11 §7)

#### Scenario: Badge de nível concedido ao certificar um nível

- **WHEN** o núcleo certifica um nível numa trilha
- **THEN** o núcleo concede o badge de nível correspondente àquela trilha

#### Scenario: Badge de valores/causas concedido por atividade da natureza

- **WHEN** o Guerreiro(a) tem Resultado de atividade de natureza "valores e temas transversais"
- **THEN** o núcleo concede o badge de valores/causas correspondente à trilha ou ao poder
