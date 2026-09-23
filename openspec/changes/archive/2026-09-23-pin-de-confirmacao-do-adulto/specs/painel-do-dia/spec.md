## RENAMED Requirements

- FROM: `### Requirement: O painel lista quem chegou e quem ainda aguarda aparelho`
- TO: `### Requirement: O painel lista quem chegou e quem está sem equipe`

## MODIFIED Requirements

### Requirement: O painel lista quem chegou e quem está sem equipe

O painel SHALL listar os Guerreiros e Guerreiras com **presença registrada** naquela aula, com o
**modo de comprovação** de cada uma — a que a App 01 registrou por reconhecimento e a que foi
confirmada por Mestre ou Admin — sem que a gestão precise lançar coisa alguma para vê-las
(`RF-02-41`, PRD-02 §12).

O painel SHALL listar à parte, sob o rótulo **"Sem equipe"**, quem chegou e ainda não formou
equipe: o Guerreiro(a) com presença registrada
naquela aula e **ainda sem equipe formada** nela. É lista **derivada**, e NEVER SHALL existir
entidade, coluna ou fila explícita de espera — no Ciclo 01 a plataforma não controla aparelhos
(documento 05 §5), e o aparelho é da equipe (documento 05 §4). Quem entra numa equipe SHALL
deixar a lista no mesmo instante, sem ato de ninguém. (`RF-02-43`, decisão do fundador,
2026-08-25; rótulo "Sem equipe", decisão do fundador, 2026-09-23)

#### Scenario: A presença do reconhecimento aparece sem lançamento manual

- **WHEN** a App 01 registra a presença de um Guerreiro(a) por reconhecimento
- **THEN** ele aparece no painel como chegado, com o modo de comprovação, sem lançamento da
  gestão

#### Scenario: A presença confirmada mostra quem confirmou

- **WHEN** a presença foi confirmada por um Mestre depois de falha de identificação
- **THEN** o painel a mostra com o modo de comprovação e quem confirmou

#### Scenario: Presente sem equipe aparece aguardando aparelho

- **WHEN** um Guerreiro(a) tem presença registrada e não integra equipe alguma daquela aula
- **THEN** ele aparece na lista "Sem equipe"

#### Scenario: Entrar numa equipe tira da espera

- **WHEN** um Guerreiro(a) que estava sem equipe entra numa equipe da aula
- **THEN** a consulta seguinte não o traz mais em "Sem equipe", e ninguém precisou marcá-lo

#### Scenario: Quem não chegou não aparece em lista alguma

- **WHEN** um Guerreiro(a) da comunidade não tem presença registrada naquela aula
- **THEN** ele não aparece nem como chegado nem em "Sem equipe"
