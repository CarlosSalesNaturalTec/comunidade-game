## ADDED Requirements

### Requirement: A aula declara só tipo de recurso de consumo do encontro

O agendamento da aula SHALL aceitar, entre os recursos que ela consome, só tipo de recurso de
finalidade **consumo do encontro**; o de finalidade **recompensa** SHALL ser recusado com **422**,
indicando os recursos declarados, sem gravar a aula; o durável segue recusado como já é. Aula
já agendada com tipo que depois passou a recompensa SHALL seguir inalterada, com a reserva que
tem. (`RF-07-53`, `RF-07-08`, `RF-02-31`, `RN-07-41`)

#### Scenario: Aula que declara kit de recompensa é recusada

- **WHEN** a gestão agenda uma aula declarando um tipo de finalidade recompensa
- **THEN** o núcleo responde 422 indicando os recursos declarados, e nenhuma aula nem reserva é
  gravada

#### Scenario: Aula que declara lanche é aceita

- **WHEN** a gestão agenda uma aula declarando um tipo de finalidade consumo do encontro com
  saldo bastante
- **THEN** a aula é gravada confirmada, com a reserva do lanche
