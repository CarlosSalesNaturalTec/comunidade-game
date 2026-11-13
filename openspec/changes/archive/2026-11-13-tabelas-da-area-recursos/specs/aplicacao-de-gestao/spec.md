## MODIFIED Requirements

### Requirement: A App 03 abre a área Recursos, com o registro do aporte e as necessidades

A App 03 SHALL oferecer ao **Admin** uma área **Recursos**, alcançável pela navegação da gestão,
que reúne o **registro do aporte**, a **lista das necessidades de recurso em aberto** e o
**saldo disponível por tipo de recurso**, apurado por ponto de apoio como a rota do núcleo já o
devolve — a área NEVER SHALL somar ou recalcular o saldo entre pontos de apoio por conta
própria. As necessidades e o saldo SHALL aparecer cada um sob o **próprio título de seção**.
O saldo SHALL aparecer em **uma tabela por ponto de apoio**, sob o nome do ponto e da sua
comunidade, com o **recurso** e o **saldo acompanhado da unidade** do catálogo de tipos de
recurso, no formato numérico pt-BR, sem zeros decimais supérfluos. Persona que não é Admin
SHALL ler a recusa do núcleo em texto, no mesmo padrão das demais áreas, e NEVER SHALL ver
dado de gestão antes da sessão aberta. (`RF-02-57`, `RF-02-58`, `RF-02-45`, `RF-02-97`,
`RF-01-02`, PRD-02 §4)

#### Scenario: O Admin alcança a área Recursos

- **WHEN** um Admin em sessão escolhe Recursos na navegação
- **THEN** a área apresenta o registro do aporte e, cada um sob o próprio título, as
  necessidades em aberto e o saldo disponível por tipo de recurso

#### Scenario: Quem não é Admin lê a recusa

- **WHEN** um Mestre em sessão alcança a área Recursos
- **THEN** a aplicação apresenta a recusa em texto simples, sem dado de gestão

#### Scenario: O saldo disponível aparece por ponto de apoio

- **WHEN** a área Recursos carrega o saldo dos pontos de apoio das comunidades cadastradas
- **THEN** cada ponto de apoio aparece com o seu nome e o da comunidade, sobre uma tabela com
  o saldo de cada tipo de recurso que o núcleo devolveu para ele, sem soma entre pontos

#### Scenario: O saldo aparece com a unidade e sem decimal cru

- **WHEN** o núcleo devolve o saldo `17.00` de um tipo de recurso cuja unidade é `un`
- **THEN** a tabela apresenta `17 un`

#### Scenario: Sem saldo disponível a área diz isso

- **WHEN** nenhum ponto de apoio tem saldo de nenhum tipo de recurso
- **THEN** a área apresenta que não há saldo disponível, sem tratar como erro

### Requirement: A área Recursos lista as necessidades de recurso em aberto

A App 03 SHALL apresentar as **necessidades de recurso em aberto** numa **tabela única**, uma
linha por par **aula + tipo de recurso**, com as colunas **aula** (data e horário),
**comunidade**, **ponto de apoio**, **recurso**, **falta** e **valor**, na ordem em que o núcleo
as devolve. A falta SHALL vir com a **unidade** do catálogo de tipos de recurso e o valor
**em moedas**, ambos no formato numérico pt-BR, sem zeros decimais supérfluos, cada um na sua
célula. Necessidade de tipo sem valor de referência vigente SHALL aparecer **sem valor em
moedas**, e NEVER com valor arbitrado pela aplicação.

A lista SHALL vir do núcleo já derivada; a aplicação NEVER SHALL somar, ordenar por saldo nem
recalcular a falta, e só formata o número que o núcleo devolveu. Não havendo necessidade em
aberto, a aplicação SHALL dizê-lo em texto, e NEVER SHALL apresentar tabela vazia sem
explicação. (`RF-02-58`, `RF-02-32`, `RN-02-19`, documento 04 §1)

#### Scenario: A necessidade aparece com o recurso, a aula e o lugar

- **WHEN** existe uma aula pendente de lastro com falta de um tipo de recurso
- **THEN** a tabela traz, numa linha e cada um na sua coluna, a data e o horário daquela aula,
  a comunidade, o ponto de apoio, o tipo, a quantidade que falta e o valor em moedas

#### Scenario: Falta e valor não se confundem

- **WHEN** o núcleo devolve a falta `1.00` de um tipo cuja unidade é `un` e o valor `5.00`
- **THEN** a célula da falta apresenta `1 un` e a do valor, `5 moedas`

#### Scenario: Tipo sem vigência aparece sem valor

- **WHEN** a necessidade é de um tipo sem valor de referência vigente na data da leitura
- **THEN** a aplicação apresenta a quantidade que falta e nenhum valor em moedas

#### Scenario: Sem necessidade em aberto a área diz isso

- **WHEN** nenhuma aula está pendente de lastro
- **THEN** a área apresenta em texto que não há necessidade em aberto
