## ADDED Requirements

### Requirement: O desafio de coleta herda a etiqueta ODS da missão, ou da trilha

O núcleo SHALL resolver a etiqueta ODS do desafio de coleta pela etiqueta declarada na **missão**
a que ele se vincula e, na falta dela, pela etiqueta da **trilha** — a mesma resolução que já vale
para qualquer vínculo que dependa da etiqueta de uma missão. A herança SHALL ser **derivada**, não
declarada: o Mestre NEVER SHALL declarar etiqueta própria no desafio, e a etiqueta do desafio
SHALL acompanhar a da missão ou da trilha quando ela mudar. Missão e trilha ambas sem etiqueta
SHALL produzir desafio **sem etiqueta**, situação normal no Ciclo 01, em que a etiqueta ainda não
é obrigatória. (`RF-08-25`, `RF-01-41`, `RN-08-21`, 11 §2.1)

#### Scenario: Desafio herda a etiqueta da missão que o criou

- **WHEN** a missão a que o desafio se vincula tem etiqueta própria de objetivo 13, e a trilha tem
  etiqueta de objetivo 4
- **THEN** o núcleo resolve, para aquele desafio, o objetivo 13

#### Scenario: Desafio recua para a etiqueta da trilha

- **WHEN** a missão a que o desafio se vincula não tem etiqueta própria e a trilha tem etiqueta de
  objetivo 4
- **THEN** o núcleo resolve, para aquele desafio, o objetivo 4

#### Scenario: Sem etiqueta na missão nem na trilha, o desafio fica sem etiqueta

- **WHEN** nem a missão nem a trilha têm etiqueta declarada
- **THEN** o desafio é criado sem etiqueta, e nada é recusado por causa disso

#### Scenario: A etiqueta do desafio não é declarada pelo Mestre

- **WHEN** chega um desafio de coleta com etiqueta ODS declarada nele
- **THEN** o núcleo responde 422, porque a etiqueta do desafio é derivada da missão ou da trilha

#### Scenario: Mudar a etiqueta da missão muda a do desafio

- **WHEN** o Mestre autor troca a etiqueta da missão depois de o desafio já existir
- **THEN** o desafio passa a resolver a etiqueta nova, sem alteração no próprio desafio

### Requirement: A etiqueta herdada pelo desafio não altera pontuação, cadência nem validade

O núcleo NEVER SHALL usar a etiqueta ODS do desafio de coleta para creditar ou negar ponto,
alterar a cadência declarada no desafio ou decidir a validade de um registro. A etiqueta é
**descritiva**: serve à cobertura agregada, e a mudança dela NEVER SHALL reprocessar pontuação
alguma. (`RN-08-21`, `RN-01-23`, 11 §2.1)

#### Scenario: Desafio etiquetado pontua igual ao não etiquetado

- **WHEN** dois desafios de coleta idênticos, um etiquetado e outro não, recebem o mesmo registro
  válido
- **THEN** os dois creditam exatamente o mesmo valor

#### Scenario: Trocar a etiqueta não reprocessa pontuação

- **WHEN** a etiqueta da trilha de um desafio muda depois de já haver registros creditados
- **THEN** nenhum ponto é recalculado, estornado ou creditado por causa da troca
