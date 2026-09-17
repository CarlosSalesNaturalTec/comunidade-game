## MODIFIED Requirements

### Requirement: A App 03 abre a área Recursos, com o registro do aporte e as necessidades

A App 03 SHALL oferecer ao **Admin** uma área **Recursos**, alcançável pela navegação da gestão,
que reúne o **registro do aporte**, a **lista das necessidades de recurso em aberto** e o
**saldo disponível por tipo de recurso**, apurado por ponto de apoio como a rota do núcleo já o
devolve — a área NEVER SHALL somar ou recalcular o saldo entre pontos de apoio por conta
própria. Persona que não é Admin SHALL ler a recusa do núcleo em texto, no mesmo padrão das
demais áreas, e NEVER SHALL ver dado de gestão antes da sessão aberta. (`RF-02-57`,
`RF-02-58`, `RF-02-45`, `RF-02-97`, `RF-01-02`, PRD-02 §4)

#### Scenario: O Admin alcança a área Recursos

- **WHEN** um Admin em sessão escolhe Recursos na navegação
- **THEN** a área apresenta o registro do aporte, as necessidades em aberto e o saldo
  disponível por tipo de recurso

#### Scenario: Quem não é Admin lê a recusa

- **WHEN** um Mestre em sessão alcança a área Recursos
- **THEN** a aplicação apresenta a recusa em texto simples, sem dado de gestão

#### Scenario: O saldo disponível aparece por ponto de apoio

- **WHEN** a área Recursos carrega o saldo dos pontos de apoio das comunidades cadastradas
- **THEN** cada ponto de apoio aparece com o saldo de cada tipo de recurso que o núcleo
  devolveu para ele, sem soma entre pontos

#### Scenario: Sem saldo disponível a área diz isso

- **WHEN** nenhum ponto de apoio tem saldo de nenhum tipo de recurso
- **THEN** a área apresenta que não há saldo disponível, sem tratar como erro

### Requirement: A aplicação apresenta a agenda das aulas

A App 03 SHALL apresentar as aulas com **comunidade**, **ponto de apoio**, **data**, **horários**
e **situação**, em lista densa, filtráveis por comunidade e por período. A aula **pendente de
lastro** SHALL se distinguir da **confirmada** na apresentação, e a aula **cancelada** SHALL
exibir o **motivo** registrado.

A lista NEVER SHALL apresentar a aula cancelada por padrão; a aplicação SHALL oferecer um
controle, desmarcado ao abrir a área, que reexibe as aulas canceladas junto das demais quando
marcado. O filtro de comunidade e de período permanece sempre visível, independente desse
controle. Esconder ou reexibir a cancelada é apresentação sobre o que a rota já devolveu — a
aplicação NEVER SHALL deixar de buscar a aula cancelada do núcleo por causa dele.

O **Mestre** SHALL ler a agenda das comunidades a que está vinculado; a aplicação NEVER SHALL
lhe apresentar aula de comunidade a que não pertence. (`RF-02-12`, `RF-01-18`, `RN-02-09`,
`RN-02-20`, documento 15 §6)

#### Scenario: A agenda distingue as situações

- **WHEN** a agenda apresenta uma aula confirmada e uma pendente de lastro
- **THEN** cada uma aparece com a sua situação, distinguíveis sem depender só de cor

#### Scenario: Aula cancelada some da lista por padrão

- **WHEN** a agenda carrega e há aula cancelada entre as retornadas pelo núcleo
- **THEN** a lista não a apresenta até o controle de reexibição ser marcado

#### Scenario: Aula cancelada mostra o motivo

- **WHEN** o controle de reexibição é marcado e a agenda apresenta uma aula cancelada
- **THEN** o motivo registrado no cancelamento aparece junto dela

#### Scenario: Mestre lê só a agenda das suas comunidades

- **WHEN** um Mestre vinculado a uma comunidade abre a agenda
- **THEN** só aparecem as aulas daquela comunidade
