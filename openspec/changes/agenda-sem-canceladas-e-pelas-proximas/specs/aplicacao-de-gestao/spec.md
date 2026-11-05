## MODIFIED Requirements

### Requirement: A aplicação apresenta a agenda das aulas

A App 03 SHALL apresentar as aulas com **comunidade**, **ponto de apoio**, **data**, **horários**
e **situação**, em lista densa, filtráveis por comunidade e por período, na ordem das **próximas
aulas** em que o núcleo as devolve. A aula **pendente de lastro** SHALL se distinguir da
**confirmada** na apresentação, e a aula **cancelada** SHALL exibir o **motivo** registrado.

A lista NEVER SHALL apresentar a aula cancelada por padrão; a aplicação SHALL oferecer um
controle, desmarcado ao abrir a área, que reexibe as aulas canceladas junto das demais quando
marcado. O filtro de comunidade e de período permanece sempre visível, independente desse
controle. Desmarcado, a aplicação NEVER SHALL buscar a aula cancelada do núcleo; marcado, SHALL
pedi-la ao núcleo (`incluir_canceladas=true`) em vez de filtrar localmente.

O **Mestre** SHALL ler a agenda das comunidades a que está vinculado; a aplicação NEVER SHALL
lhe apresentar aula de comunidade a que não pertence. (`RF-02-12`, `RF-01-18`, `RN-02-09`,
`RN-02-20`, documento 15 §6, documento 09 §1 "Agenda sem canceladas e pelas próximas aulas")

#### Scenario: A agenda distingue as situações

- **WHEN** a agenda apresenta uma aula confirmada e uma pendente de lastro
- **THEN** cada uma aparece com a sua situação, distinguíveis sem depender só de cor

#### Scenario: Aula cancelada some da lista por padrão

- **WHEN** a agenda abre com o controle de reexibição desmarcado
- **THEN** a aplicação consulta o núcleo sem pedir as canceladas, e nenhuma aparece na lista

#### Scenario: Marcar o controle busca as canceladas

- **WHEN** o controle de reexibição é marcado
- **THEN** a aplicação consulta o núcleo pedindo as canceladas e as apresenta junto das demais

#### Scenario: Aula cancelada mostra o motivo

- **WHEN** o controle de reexibição é marcado e a agenda apresenta uma aula cancelada
- **THEN** o motivo registrado no cancelamento aparece junto dela

#### Scenario: Aula prevista aparece mesmo com muitas canceladas

- **WHEN** a comunidade tem mais aulas canceladas do que cabem numa página e uma aula prevista,
  e a agenda abre sem filtro de período
- **THEN** a aula prevista aparece na lista

#### Scenario: Mestre lê só a agenda das suas comunidades

- **WHEN** um Mestre vinculado a uma comunidade abre a agenda
- **THEN** só aparecem as aulas daquela comunidade
