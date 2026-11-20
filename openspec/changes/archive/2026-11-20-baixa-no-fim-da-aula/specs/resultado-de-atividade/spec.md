## REMOVED Requirements

### Requirement: O lançamento da atividade realizada é ato por aula e converte as reservas em baixa

**Reason**: a baixa e a passagem a realizada passaram ao sistema, no fim do horário (`RF-07-09`, `RN-07-43`, `RF-02-35`).

**Migration**: substituído por "O lançamento dos resultados da aula grava os Resultados sem baixar reserva".

## ADDED Requirements

### Requirement: O lançamento dos resultados da aula grava os Resultados sem baixar reserva

O núcleo SHALL expor o lançamento dos **resultados da aula** como ato **por aula**, de
**Admin**, que registra em uma operação os Resultados dos participantes, cada um com a atividade
a que pertence. O ato NEVER SHALL baixar reserva nem mudar a situação da aula: a baixa e a
passagem a realizada são do sistema, no fim do horário. O ato SHALL ser aceito durante e depois
da aula, e SHALL ser recusado com **422** só na aula **cancelada**; o Resultado repetido segue
recusado pela regra que já o recusa. (`RF-02-33`, `RF-02-35`, `RN-07-43`, `RF-01-16`,
`RF-01-03`)

#### Scenario: O lançamento grava os resultados sem baixar nada

- **WHEN** um Admin lança os resultados numa aula confirmada com duas reservas
- **THEN** o núcleo grava os Resultados, nenhum débito é gravado, as reservas seguem reservadas
  e a aula segue confirmada

#### Scenario: O lançamento é aceito depois do fim da aula

- **WHEN** um Admin lança os resultados de uma aula já realizada
- **THEN** o núcleo grava os Resultados

#### Scenario: Aula cancelada recusa o lançamento

- **WHEN** chega o lançamento de resultados de uma aula cancelada
- **THEN** o núcleo responde 422 e nada é gravado

#### Scenario: Mestre não lança pela aula

- **WHEN** um Mestre tenta lançar os resultados pela rota da aula
- **THEN** o núcleo responde 403 e nada é gravado
