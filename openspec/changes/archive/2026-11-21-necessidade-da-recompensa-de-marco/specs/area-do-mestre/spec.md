## ADDED Requirements

### Requirement: A App 09 apresenta a necessidade da recompensa com a trilha

A lista de necessidades da App 09 SHALL apresentar também a necessidade da **recompensa de
marco** das comunidades do Mestre, com a **trilha** no lugar da data e do horário da aula, e o
tipo de recurso, a quantidade que falta, o valor em moedas e o ponto de apoio, sem reais e sem
pessoa. (`RF-09-56`, `RF-07-54`)

#### Scenario: O Mestre vê a falta da recompensa da comunidade dele

- **WHEN** o Mestre abre a área de recursos e falta recompensa de marco na comunidade dele
- **THEN** a aplicação apresenta a necessidade com a trilha, o tipo, a quantidade que falta,
  o valor em moedas e o ponto de apoio

### Requirement: O Mestre absorve a necessidade da recompensa no mesmo ato

A absorção a partir da necessidade da recompensa SHALL declarar a **comunidade** e a
**trilha** no lugar da aula, com o tipo e o ponto de apoio da necessidade, nunca escolhidos à
parte, e SHALL seguir o mesmo ato de confirmação, valor de origem e comprovante da absorção da
aula. A tela NEVER SHALL dizer que confirma aula, porque a necessidade da recompensa não tem
aula. (`RF-09-57`, `RF-07-28`, `RF-07-54`)

#### Scenario: A absorção da recompensa envia comunidade e trilha

- **WHEN** o Mestre confirma a absorção de uma necessidade de recompensa
- **THEN** a aplicação envia a comunidade, a trilha, o tipo e o ponto de apoio dela, sem aula
