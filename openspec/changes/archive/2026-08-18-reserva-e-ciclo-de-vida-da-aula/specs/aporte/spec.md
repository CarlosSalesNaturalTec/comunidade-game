## ADDED Requirements

### Requirement: O aporte que fecha a diferença confirma a aula pendente de lastro

O núcleo SHALL, ao creditar um aporte, verificar as aulas em situação **pendente de lastro** no
**ponto de apoio** daquele aporte. Toda aula cuja lista inteira de recursos declarados passe a
ter **quantidade disponível** bastante SHALL ser **confirmada no mesmo ato**, com as reservas
efetivadas — sem ato humano de confirmação à parte. Aula cuja falta continue em qualquer parcela
SHALL permanecer **pendente de lastro**, sem reserva alguma. Havendo mais de uma aula
confirmável pelo mesmo aporte e disponível para menos que todas, o núcleo SHALL atendê-las pelo
**horário inicial da aula, da mais próxima para a mais distante**. A confirmação SHALL registrar autor e momento, como toda escrita.
(`RN-07-37`, `RF-07-08`, `RN-07-01`, `RF-01-03`, invariante 9 do documento 99 §6, documento
04 §1)

#### Scenario: Aporte que fecha a falta confirma a aula

- **WHEN** um aporte homologado entra no ponto de apoio de uma aula pendente de lastro e cobre
  toda a falta dela
- **THEN** a aula passa a confirmada e as reservas dela são efetivadas no mesmo ato

#### Scenario: Aporte insuficiente não confirma nada

- **WHEN** um aporte homologado cobre parte da falta de uma aula pendente de lastro
- **THEN** a aula segue pendente de lastro e nenhuma reserva é gravada

#### Scenario: Aporte em outro ponto de apoio não confirma a aula

- **WHEN** um aporte do tipo que falta entra num ponto de apoio diferente do da aula
- **THEN** a aula segue pendente de lastro

#### Scenario: Aula de data mais próxima é atendida primeiro

- **WHEN** um aporte fecha a falta de duas aulas pendentes de lastro, mas só tem disponível
  para uma
- **THEN** o núcleo confirma a aula cujo horário inicial é o mais próximo e mantém a outra
  pendente de lastro

#### Scenario: Absorção também confirma

- **WHEN** um aporte por absorção, que credita no ato, cobre a falta de uma aula pendente de
  lastro
- **THEN** a aula passa a confirmada e as reservas são efetivadas
