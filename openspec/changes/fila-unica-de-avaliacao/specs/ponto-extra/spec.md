## ADDED Requirements

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
