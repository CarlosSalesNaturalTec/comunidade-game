## MODIFIED Requirements

### Requirement: A gestão lê a agenda, filtrada por comunidade e por período

O núcleo SHALL devolver as aulas com **comunidade**, **ponto de apoio**, **data**, **horário
inicial**, **horário final**, **situação** e, quando cancelada, o **motivo do cancelamento**. A
leitura SHALL ser paginada e SHALL aceitar filtro por **comunidade** e por **período**.

A aula **cancelada** NEVER SHALL vir na leitura por padrão; o núcleo SHALL devolvê-la junto das
demais apenas quando a consulta declara `incluir_canceladas=true`. Valor diferente de `true` ou
`false` nesse filtro SHALL ser recusado com **422**.

A leitura SHALL vir ordenada pelas **próximas aulas**: primeiro as que ainda não terminaram, da
de horário inicial mais próximo à mais distante; depois as já terminadas, da mais recente à mais
antiga. A divisão entre os dois grupos SHALL usar o mesmo momento em todas as páginas de uma
mesma leitura.

A leitura SHALL exigir persona de gestão em sessão: o **Admin** SHALL ler todas as comunidades e
o **Mestre**, apenas as comunidades a que está vinculado. **Apoiador**, **Guerreiro(a)** e
**responsável** SHALL receber **403**.

A aula **pendente de lastro** SHALL sair com a situação que a distingue da confirmada, sem que a
leitura altere situação alguma. (`RF-02-12`, `RF-01-28`, `RF-01-18`, `RF-01-16`, `RN-02-09`,
PRD-02 §9, documento 09 §1 "Agenda sem canceladas e pelas próximas aulas")

#### Scenario: Admin lê a agenda das comunidades

- **WHEN** um Admin em sessão consulta a agenda
- **THEN** vêm as aulas com comunidade, ponto de apoio, data, horários e situação

#### Scenario: Mestre lê apenas a agenda das suas comunidades

- **WHEN** um Mestre vinculado a uma comunidade consulta a agenda
- **THEN** vêm apenas as aulas daquela comunidade

#### Scenario: Apoiador não lê a agenda da gestão

- **WHEN** um Apoiador em sessão consulta a agenda
- **THEN** o núcleo responde 403

#### Scenario: A agenda distingue a aula pendente de lastro

- **WHEN** a agenda traz uma aula pendente de lastro e outra confirmada
- **THEN** cada uma sai com a sua situação, e nenhuma delas muda por ter sido lida

#### Scenario: Filtro de período recorta a agenda

- **WHEN** a consulta declara um período
- **THEN** vêm apenas as aulas cujo horário inicial cai dentro dele

#### Scenario: A cancelada fica fora da agenda por padrão

- **WHEN** a comunidade tem aula cancelada e aula prevista, e a consulta não declara
  `incluir_canceladas`
- **THEN** vem só a aula prevista

#### Scenario: A cancelada vem quando pedida

- **WHEN** a consulta declara `incluir_canceladas=true`
- **THEN** a aula cancelada vem junto das demais, com o motivo do cancelamento

#### Scenario: Valor inválido no filtro de canceladas é recusado

- **WHEN** a consulta declara `incluir_canceladas=talvez`
- **THEN** o núcleo responde 422 apontando o campo `incluir_canceladas`

#### Scenario: Muitas canceladas antigas não escondem a próxima aula

- **WHEN** a comunidade tem mais aulas canceladas antigas do que cabem numa página e uma aula
  prevista para depois delas, e a consulta não declara `incluir_canceladas`
- **THEN** a primeira página traz a aula prevista

#### Scenario: As próximas aulas vêm antes das já terminadas

- **WHEN** a comunidade tem duas aulas por vir e duas já terminadas
- **THEN** vêm primeiro as duas por vir, da mais próxima à mais distante, e depois as terminadas,
  da mais recente à mais antiga

#### Scenario: A paginação atravessa os dois grupos sem repetir nem pular

- **WHEN** a leitura segue o cursor até o fim, com aulas por vir e terminadas que não cabem numa
  página
- **THEN** cada aula vem uma vez só, na ordem das próximas aulas
