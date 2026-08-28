## MODIFIED Requirements

### Requirement: O Admin agenda a aula com comunidade, data e horários

A App 03 SHALL permitir ao Admin agendar a aula informando **comunidade**, **data**, **horário
inicial**, **horário final** e o **ponto de apoio** em que ela acontece. A data e os horários
SHALL trafegar com **fuso**, e a aplicação NEVER SHALL enviar horário sem ele.

A aplicação SHALL oferecer, como ponto de apoio, apenas os da **comunidade escolhida**, e SHALL
apresentar no próprio campo a recusa do núcleo a horário final não posterior ao inicial e a
ponto de apoio de outra comunidade. Aula agendada sem recurso declarado SHALL nascer
**confirmada**, e a aplicação SHALL apresentar a situação como ela vem do núcleo, sem
recalculá-la.

O formulário SHALL permitir declarar, no mesmo ato, os **recursos que a aula consome**, como
pares de **tipo de recurso** e **quantidade**, escolhidos no catálogo de tipos da gestão. A
aplicação SHALL aceitar nenhum, um ou vários pares, SHALL permitir remover um par antes de
confirmar e NEVER SHALL enviar par com quantidade menor ou igual a zero, apontando a recusa no
próprio campo. Confirmado o agendamento, é o núcleo que reserva o que a aula consome; a
aplicação NEVER SHALL calcular saldo, reserva ou falta por conta própria. (`RF-02-12`,
`RF-02-30`, `RF-02-31`, `RN-02-09`, PRD-02 §5.1, documento 04 §1)

#### Scenario: Admin agenda a aula

- **WHEN** um Admin em sessão informa comunidade, data, horário inicial, horário final e ponto
  de apoio, e confirma
- **THEN** a aula passa a existir, confirmada, e a aplicação a apresenta na agenda

#### Scenario: Horário final anterior ao inicial é apontado no campo

- **WHEN** o Admin confirma o agendamento com horário final não posterior ao inicial
- **THEN** a aplicação aponta o erro no próprio campo e nenhuma aula passa a existir

#### Scenario: O ponto de apoio oferecido é o da comunidade escolhida

- **WHEN** o Admin escolhe a comunidade no formulário
- **THEN** só os pontos de apoio daquela comunidade lhe são oferecidos

#### Scenario: Quem não é Admin não alcança o agendamento

- **WHEN** um Mestre em sessão abre a agenda
- **THEN** o caminho de agendamento não lhe é oferecido

#### Scenario: O agendamento declara os recursos que a aula consome

- **WHEN** o Admin acrescenta dois pares de tipo de recurso e quantidade e confirma o
  agendamento
- **THEN** a aula passa a existir com os dois recursos declarados, e a aplicação apresenta a
  situação que o núcleo devolveu

#### Scenario: Quantidade não positiva é apontada no campo

- **WHEN** o Admin declara um recurso com quantidade zero
- **THEN** a aplicação aponta o erro no próprio campo e nenhuma aula passa a existir

#### Scenario: Aula sem saldo nasce pendente de lastro

- **WHEN** o Admin agenda a aula declarando mais de um recurso do que há disponível no ponto de
  apoio
- **THEN** a aplicação apresenta a aula como pendente de lastro, tal como o núcleo a devolveu

## ADDED Requirements

### Requirement: A App 03 abre a área Recursos, com o registro do aporte e as necessidades

A App 03 SHALL oferecer ao **Admin** uma área **Recursos**, alcançável pela navegação da gestão,
que reúne o **registro do aporte** e a **lista das necessidades de recurso em aberto**. Persona
que não é Admin SHALL ler a recusa do núcleo em texto, no mesmo padrão das demais áreas, e
NEVER SHALL ver dado de gestão antes da sessão aberta. (`RF-02-57`, `RF-02-58`, `RF-01-02`,
PRD-02 §4)

#### Scenario: O Admin alcança a área Recursos

- **WHEN** um Admin em sessão escolhe Recursos na navegação
- **THEN** a área abre com o registro do aporte e a lista das necessidades em aberto

#### Scenario: Quem não é Admin lê a recusa

- **WHEN** um Mestre em sessão alcança a área Recursos
- **THEN** a aplicação apresenta a recusa em texto, sem dado de gestão

### Requirement: O Admin registra e homologa o aporte pela aplicação

A App 03 SHALL permitir ao Admin registrar o aporte declarando **provedor**, **tipo de recurso**,
**quantidade**, **ponto de apoio de entrada**, **data do aporte**, **forma** — financeira,
material ou serviço — e o **comprovante**. O provedor SHALL ser escolhido entre os adultos já
cadastrados, e o ponto de apoio, entre os da comunidade escolhida.

A aplicação SHALL exigir o comprovante quando o **tipo de recurso o exigir**, e SHALL apresentar
no próprio campo as recusas do núcleo: campo em falta, quantidade não positiva, formato de
comprovante fora de PDF, JPG ou PNG, data sem vigência de valor de referência, tipo inexistente
e o aporte em causa própria, em que o provedor é a própria persona que registra.

Registrado o aporte, a aplicação SHALL apresentar o **valor em moedas** que o núcleo devolveu, e
NEVER SHALL exibir valor em reais nem oferecer campo de chave PIX, banco ou conta. A aplicação
NEVER SHALL converter quantidade em moedas por conta própria. (`RF-02-57`, `RN-02-19`,
invariante 16 do documento 99 §6, PRD-07 §9)

#### Scenario: Admin registra o aporte com comprovante

- **WHEN** um Admin informa provedor, tipo, quantidade, ponto de apoio, data, forma e anexa o
  comprovante, e confirma
- **THEN** o aporte passa a existir e a aplicação apresenta o valor em moedas devolvido pelo
  núcleo

#### Scenario: Tipo que exige comprovante bloqueia o envio sem ele

- **WHEN** o Admin escolhe um tipo de recurso que exige comprovante e confirma sem anexá-lo
- **THEN** a aplicação aponta a falta no próprio campo e nenhum aporte passa a existir

#### Scenario: Aporte em causa própria é apresentado como recusa

- **WHEN** o Admin registra um aporte cujo provedor é ele próprio
- **THEN** a aplicação apresenta a recusa do núcleo e nenhum aporte passa a existir

#### Scenario: Nenhuma tela do aporte mostra reais

- **WHEN** o aporte registrado é apresentado
- **THEN** o valor aparece em moedas, e nenhum campo da tela traz valor em reais

### Requirement: A área Recursos lista as necessidades de recurso em aberto

A App 03 SHALL apresentar as **necessidades de recurso em aberto** com **tipo de recurso**,
**quantidade que falta**, **valor em moedas**, **comunidade**, **ponto de apoio** e a **data e o
horário** da aula, em lista densa, identificando cada uma pelo par **aula + tipo de recurso**.
Necessidade de tipo sem valor de referência vigente SHALL aparecer **sem valor em moedas**, e
NEVER com valor arbitrado pela aplicação.

A lista SHALL vir do núcleo já derivada; a aplicação NEVER SHALL somar, ordenar por saldo nem
recalcular a falta. Não havendo necessidade em aberto, a aplicação SHALL dizê-lo em texto, e
NEVER SHALL apresentar lista vazia sem explicação. (`RF-02-58`, `RF-02-32`, `RN-02-19`,
documento 04 §1)

#### Scenario: A necessidade aparece com o recurso, a aula e o lugar

- **WHEN** existe uma aula pendente de lastro com falta de um tipo de recurso
- **THEN** a lista traz o tipo, a quantidade que falta, o valor em moedas, a comunidade, o ponto
  de apoio e a data e o horário daquela aula

#### Scenario: Tipo sem vigência aparece sem valor

- **WHEN** a necessidade é de um tipo sem valor de referência vigente na data da leitura
- **THEN** a aplicação apresenta a quantidade que falta e nenhum valor em moedas

#### Scenario: Sem necessidade em aberto a área diz isso

- **WHEN** nenhuma aula está pendente de lastro
- **THEN** a área apresenta em texto que não há necessidade em aberto

### Requirement: O aporte que fecha a falta mostra a aula confirmada e a reserva efetivada

Registrado um aporte que **fecha a falta** de uma aula pendente de lastro, a App 03 SHALL
apresentar, na mesma área, a aula já **confirmada** e a **reserva efetivada**, e a necessidade
correspondente SHALL **sair da lista** — sem oferecer ato humano de confirmação, que não existe.
A aplicação SHALL obter a mudança relendo o núcleo depois do registro, e NEVER SHALL antecipar a
confirmação antes de o núcleo a devolver.

Aporte que cobre **parte** da falta SHALL manter a necessidade na lista, com a falta **abatida**,
e a aula **pendente de lastro**. (`RF-02-67`, `RF-02-32`, `RN-02-09`, documento 04 §1)

#### Scenario: O aporte que fecha a falta confirma a aula

- **WHEN** o Admin registra um aporte que cobre toda a falta de uma aula pendente de lastro
- **THEN** a necessidade some da lista e a aplicação apresenta a aula confirmada, com a reserva
  efetivada

#### Scenario: O aporte parcial abate a falta e a aula segue pendente

- **WHEN** o Admin registra um aporte que cobre parte da falta
- **THEN** a necessidade continua na lista com a falta abatida, e a aula segue pendente de
  lastro

#### Scenario: Não há ato de confirmação a oferecer

- **WHEN** a área apresenta uma aula pendente de lastro
- **THEN** nenhum caminho de confirmação manual da aula é oferecido

### Requirement: A App 03 cadastra a atividade avulsa, fora de trilha

A App 03 SHALL oferecer ao **Admin** o cadastro da **atividade avulsa**, com **título**,
**descrição**, **modalidade**, **formato**, **natureza**, **produção esperada** e o **poder** que
ela desenvolve, escolhido no catálogo de poderes da gestão. Modalidade e formato SHALL ser
oferecidos como escolha fechada nos valores do documento 11 §4.

A aplicação NEVER SHALL oferecer campo de **pontuação** — o valor vem do motor do documento 11
§5 — nem campo de **recurso**, que é declaração da aula. A aplicação NEVER SHALL oferecer ao
Admin o cadastro de atividade **de trilha**, que é autoria do Mestre na App 09, e SHALL
apresentar no próprio campo as recusas do núcleo. (`RF-02-29`, PRD-02 §3.2, documento 11 §§4, 5)

#### Scenario: Admin cadastra a atividade avulsa

- **WHEN** um Admin informa título, modalidade, formato, natureza, produção esperada e o poder,
  e confirma
- **THEN** a atividade avulsa passa a existir e a aplicação a apresenta na lista

#### Scenario: A tela não oferece pontuação nem recurso

- **WHEN** o Admin abre o cadastro da atividade avulsa
- **THEN** não há campo de pontuação nem campo de tipo de recurso no formulário

#### Scenario: Cadastro sem poder é apontado no campo

- **WHEN** o Admin confirma o cadastro sem escolher o poder
- **THEN** a aplicação aponta a falta no próprio campo e nenhuma atividade passa a existir

#### Scenario: Quem não é Admin não alcança o cadastro

- **WHEN** um Mestre em sessão alcança a área
- **THEN** o caminho de cadastro da atividade avulsa não lhe é oferecido
