## MODIFIED Requirements

### Requirement: O painel mostra o previsto, o provido e o saldo do ponto de apoio

O painel SHALL mostrar a **atividade prevista** da aula e os **recursos providos** — as reservas
que o agendamento constituiu, com tipo de recurso e quantidade (`RF-02-44`).

O painel SHALL mostrar o **saldo dos tipos de recurso do ponto de apoio da aula**, derivado dos
lançamentos como todo saldo do livro-razão (`RN-07-36`). Os tipos SHALL vir do **catálogo
configurável** da gestão: o núcleo NEVER SHALL fixar tipo de recurso em código. "Kits MDF" e
"exemplares da linha Alpha" são exemplo de operação, não catálogo — decisão do fundador,
2026-08-25, que corrige o texto do `RF-02-45`. (`RF-02-44`, `RF-02-45`, `RN-07-36`, PRD-02 §6.4)

Em recursos providos e no saldo, cada tipo de recurso SHALL aparecer pelo **nome** e pela
**unidade** do catálogo; o painel NEVER SHALL exibir o identificador interno do tipo.
(`RF-02-44`, `RF-02-45`, PRD-02 §5.5.3)

#### Scenario: O previsto e o provido saem juntos

- **WHEN** o painel é consultado numa aula que reservou dois tipos de recurso
- **THEN** ele mostra a atividade prevista e as duas reservas, com tipo e quantidade

#### Scenario: O saldo é o do ponto de apoio da aula

- **WHEN** o painel mostra o saldo de um tipo de recurso
- **THEN** o valor é o saldo daquele tipo no ponto de apoio em que a aula acontece

#### Scenario: Tipo novo do catálogo aparece sem tocar em código

- **WHEN** a gestão cadastra um tipo de recurso novo e ele tem saldo no ponto de apoio da aula
- **THEN** o painel passa a mostrá-lo, sem que nenhum tipo esteja fixado no núcleo

#### Scenario: Aula sem recurso declarado mostra o previsto e nenhuma reserva

- **WHEN** a aula não declarou recurso algum
- **THEN** o painel mostra a atividade prevista e nenhuma reserva, sem erro

#### Scenario: O tipo de recurso aparece pelo nome e pela unidade

- **WHEN** a aula reservou um tipo de recurso do catálogo e o ponto de apoio tem saldo dele
- **THEN** a reserva e o saldo aparecem com o nome, a quantidade e a unidade do tipo
- **AND** o identificador interno do tipo não aparece na tela
