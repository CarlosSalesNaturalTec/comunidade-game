# aplicacao-de-gestao Specification

## Purpose

A App 03 é a mesa de comando do projeto: é nela que o Admin cadastra, aprova, lança e confere,
e é dela que sai a Comunidade Virtual, raiz de todo vínculo da plataforma. Esta capacidade
cobre como o adulto entra na aplicação, como a sessão e o papel governam o que ele alcança, e
o cadastro de Comunidade Virtual de ponta a ponta.

## Requirements

### Requirement: A aplicação é inteiramente autenticada e se identifica por chave

A App 03 SHALL apresentar a chave de aplicação dela em toda chamada ao núcleo e NEVER SHALL
expor tela de dados a quem não tem sessão aberta. Visitante não alcança tela alguma.
(`RF-01-02`, `RN-01-32`, PRD-02 §4)

#### Scenario: Quem não tem sessão vê a entrada

- **WHEN** alguém abre qualquer endereço da aplicação sem sessão aberta
- **THEN** a aplicação apresenta a tela de entrada, e nenhum dado de gestão aparece

#### Scenario: A chave acompanha toda chamada

- **WHEN** a aplicação chama qualquer rota de dados do núcleo
- **THEN** a chamada leva a chave de aplicação da App 03 do ambiente em que ela roda

### Requirement: O adulto entra por login social

A App 03 SHALL abrir sessão para o adulto que autentica pela conta social e SHALL guardar o
papel que o núcleo devolveu, que é o que governa o que ele alcança dali em diante.
(`RF-01-09`, documento 03 §1.1)

#### Scenario: Admin com cadastro entra

- **WHEN** um Admin autentica pela conta social associada ao cadastro dele
- **THEN** a aplicação abre a sessão e apresenta as telas de gestão do papel de Admin

#### Scenario: O papel vem do núcleo, não da tela

- **WHEN** a sessão é aberta
- **THEN** o papel que governa a aplicação é o que o núcleo devolveu, e nenhuma escolha na
  tela o altera

### Requirement: Conta sem cadastro é recusada com o caminho da solicitação

A App 03 SHALL apresentar a recusa de quem autentica com conta social sem cadastro
correspondente, orientando a pedir participação pela vitrine, e NEVER SHALL sugerir que o
acesso se resolve tentando de novo. (`RF-01-10`, `RN-01-04`)

#### Scenario: Conta social sem cadastro lê a orientação

- **WHEN** um adulto autentica com conta social que não corresponde a persona cadastrada
- **THEN** a aplicação apresenta a recusa com a orientação de solicitar participação pela
  vitrine, e nenhuma sessão é aberta

### Requirement: Sessão encerrada ou expirada devolve à entrada

A App 03 SHALL devolver o adulto à tela de entrada quando a sessão dele expira ou é
encerrada, e SHALL distinguir essa recusa da recusa da chave — são credenciais independentes.
(`RF-01-09`, `RN-01-34`)

#### Scenario: Sessão expirada durante o uso

- **WHEN** o adulto aciona uma tela de gestão e o núcleo recusa a sessão por expirada
- **THEN** a aplicação o devolve à tela de entrada, informando que a sessão terminou

#### Scenario: O adulto encerra a própria sessão

- **WHEN** o adulto aciona a saída
- **THEN** a sessão é encerrada no núcleo e a aplicação volta à tela de entrada

### Requirement: O Admin cria a Comunidade Virtual, que nasce vazia

A App 03 SHALL permitir ao Admin criar a Comunidade Virtual informando nome, localização e
granularidade máxima, e a comunidade criada SHALL nascer sem Guerreiro(a), sem local e sem
aula. (`RF-02-11`, `RN-02-04`, invariante 4)

#### Scenario: Admin cria a comunidade

- **WHEN** um Admin em sessão informa nome, localização e granularidade máxima e confirma
- **THEN** a comunidade passa a existir, vazia, e a aplicação a apresenta entre as existentes

#### Scenario: Campo obrigatório em falta

- **WHEN** o Admin confirma a criação com nome, localização ou granularidade máxima vazios
- **THEN** a aplicação aponta o campo em falta e nenhuma comunidade passa a existir

### Requirement: Quem não é Admin lê a recusa, não um erro cru

A App 03 SHALL apresentar em linguagem simples a recusa do núcleo a quem tenta criar
Comunidade Virtual sem ser Admin, e NEVER SHALL oferecer o caminho de criação a quem não pode
percorrê-lo. (`RN-02-04`, `RN-08-01`, PRD-02 §4)

#### Scenario: Mestre não alcança a criação

- **WHEN** um Mestre em sessão abre a aplicação
- **THEN** o caminho de criação de comunidade não lhe é oferecido

#### Scenario: Recusa do núcleo é explicada

- **WHEN** o núcleo recusa a criação por papel
- **THEN** a aplicação apresenta que só o Admin cria Comunidade Virtual, sem jargão de TI e
  sem código de erro cru

### Requirement: A aplicação apresenta as comunidades já criadas

A App 03 SHALL apresentar ao adulto em sessão as Comunidades Virtuais existentes, para que
ele saiba o que já há antes de criar. Comunidade abaixo do piso de coletores SHALL aparecer
sem os indicadores do território, e a ausência deles NEVER SHALL ser apresentada como falha.
A apresentação SHALL ser lista densa, no temperamento Operação, e NEVER SHALL usar a carta do
documento 15 §8.1 enquanto a lista não devolver o que o documento 11 §8.2 exige dela.
(`RF-08-30`, `RF-08-31`, `RN-08-28`, documento 15 §6)

#### Scenario: Comunidade recém-criada aparece sem indicadores

- **WHEN** o adulto abre a lista logo após criar uma comunidade
- **THEN** a comunidade nova aparece nela, sem os indicadores do território e sem mensagem de
  erro

#### Scenario: A ausência de indicadores se distingue do erro

- **WHEN** uma comunidade aparece sem os indicadores do território
- **THEN** o que a lista informa é a ausência de indicadores, apresentada como informação, e
  não como aviso de erro

### Requirement: O Admin cadastra o ponto de apoio da comunidade

A App 03 SHALL permitir ao Admin cadastrar o ponto de apoio informando **nome** e a
**comunidade** a que ele pertence, e SHALL apresentar os pontos de apoio já cadastrados antes
de oferecer o cadastro, para que ele saiba o que já há. A apresentação SHALL ser **lista
densa**, no temperamento Operação, como a das comunidades.

O ponto de apoio SHALL nascer **sem responsável pelo acervo**, e a aplicação NEVER SHALL
apresentar essa ausência como falha: a designação é ato posterior, oferecido na própria área.
(`RF-07-47`, `RF-07-49`, `RN-07-34`, documento 15 §6)

#### Scenario: Admin cadastra o ponto de apoio

- **WHEN** um Admin em sessão informa nome e comunidade e confirma
- **THEN** o ponto de apoio passa a existir e a aplicação o apresenta entre os existentes

#### Scenario: Campo obrigatório em falta

- **WHEN** o Admin confirma o cadastro com nome ou comunidade vazios
- **THEN** a aplicação aponta o campo em falta, no próprio campo, e nenhum ponto de apoio
  passa a existir

#### Scenario: Ponto de apoio sem responsável não é apresentado como pendência

- **WHEN** a lista apresenta um ponto de apoio ainda sem responsável pelo acervo
- **THEN** a ausência aparece como informação, e não como aviso de erro

#### Scenario: Quem não é Admin não alcança o cadastro

- **WHEN** um Mestre em sessão abre a área de pontos de apoio
- **THEN** o caminho de cadastro não lhe é oferecido, e a recusa do núcleo, se ocorrer, é
  apresentada em linguagem simples

### Requirement: O Admin desativa e reativa o ponto de apoio pela aplicação

A App 03 SHALL oferecer ao Admin, no ponto de apoio já cadastrado, as ações de **desativar** e
**reativar**, cada uma exigindo motivo antes de confirmar. A lista de pontos de apoio SHALL
distinguir o ativo do inativo, e o inativo SHALL continuar visível — é histórico, não some. As
ações NEVER SHALL ser oferecidas a quem não é Admin. (`RF-07-47`, `RN-07-33`, `RN-02-21`,
PRD-02 §4)

#### Scenario: Admin desativa um ponto de apoio

- **WHEN** um Admin em sessão desativa um ponto de apoio informando o motivo
- **THEN** o ponto passa a aparecer como inativo na lista, e o motivo fica registrado

#### Scenario: Inativo continua na lista

- **WHEN** um Admin abre a lista de pontos de apoio de uma comunidade que tem um inativo
- **THEN** o inativo aparece, distinguido do ativo

#### Scenario: Mestre não vê a ação

- **WHEN** um Mestre em sessão abre um ponto de apoio
- **THEN** as ações de desativar e reativar não lhe são oferecidas

#### Scenario: Sem motivo não confirma

- **WHEN** o Admin tenta confirmar a desativação com o motivo vazio
- **THEN** a aplicação aponta o campo em falta e nada é enviado ao núcleo

### Requirement: A recusa da desativação diz o que está prendendo o espaço

A App 03 SHALL apresentar em linguagem simples por que a desativação foi recusada: **quantas
aulas futuras** prendem o ponto de apoio, ou **quais tipos de recurso** ainda têm saldo nele. A
aplicação SHALL oferecer, na recusa por saldo, o caminho da **transferência**, e NEVER SHALL
apresentar código de erro cru. (`RF-07-47`, `RN-07-01`, `RN-07-15`, PRD-02 §10)

#### Scenario: Recusa por aula futura é explicada

- **WHEN** o núcleo recusa a desativação porque há aulas futuras no ponto de apoio
- **THEN** a aplicação diz quantas aulas o prendem, sem jargão de TI

#### Scenario: Recusa por saldo oferece a transferência

- **WHEN** o núcleo recusa a desativação porque ainda há saldo no ponto de apoio
- **THEN** a aplicação diz quais tipos têm saldo e oferece o caminho de transferi-los

### Requirement: O Admin transfere o saldo de um ponto de apoio para outro

A App 03 SHALL oferecer ao Admin a **transferência** de um tipo de recurso de um ponto de apoio
para outro, informando tipo, quantidade, destino e motivo. A aplicação SHALL apresentar o saldo
disponível na origem antes de confirmar, NEVER SHALL oferecer como destino um ponto de apoio
inativo nem o próprio ponto de origem, e SHALL apresentar a transferência confirmada como **um
fato só**, não como dois lançamentos soltos. (`RF-07-19`, `RN-07-15`, `RN-07-33`)

#### Scenario: Admin transfere um tipo de recurso

- **WHEN** um Admin informa tipo, quantidade, ponto de apoio de destino e motivo, e confirma
- **THEN** a transferência acontece e os saldos dos dois pontos de apoio aparecem atualizados

#### Scenario: O destino inativo não é oferecido

- **WHEN** o Admin escolhe o destino da transferência
- **THEN** os pontos de apoio inativos e o próprio ponto de origem não aparecem entre as
  opções

#### Scenario: Quantidade acima do saldo é barrada antes de enviar

- **WHEN** o Admin informa quantidade maior que o saldo disponível na origem
- **THEN** a aplicação aponta o limite e nada é enviado ao núcleo

### Requirement: A área Pontos de Apoio apresenta o extrato e corrige por ajuste

A área **Pontos de Apoio** SHALL apresentar, para o ponto de apoio escolhido, o **extrato do
livro-razão** — natureza, tipo de recurso, quantidade, moedas e data de cada lançamento, com
filtro por período e por tipo de recurso. Sobre cada lançamento a tela SHALL oferecer o
**ajuste**, com quantidade, moedas e **motivo**.

A tela NEVER SHALL oferecer caminho de edição nem de remoção de lançamento: a correção é
sempre um lançamento novo, que referencia o original e o deixa intacto (`RN-02-12`). Gravado o
ajuste, o extrato SHALL apresentá-lo referenciando o lançamento corrigido, com o motivo e o
autor. Ajuste sem motivo SHALL impedir o envio. (`RF-02-40`, `RN-02-12`, `RN-02-21`, PRD-02
§§6.3, 12)

#### Scenario: O extrato apresenta os lançamentos do ponto de apoio

- **WHEN** o Admin abre o extrato de um ponto de apoio
- **THEN** a tela lista os lançamentos daquele ponto de apoio, com natureza, tipo de recurso,
  quantidade, moedas e data

#### Scenario: A correção se faz por ajuste

- **WHEN** o Admin lança um ajuste sobre um lançamento errado, com motivo
- **THEN** a aplicação grava o ajuste, o extrato o apresenta referenciando o original, e o
  lançamento original permanece como estava

#### Scenario: A tela não oferece edição de lançamento

- **WHEN** o Admin procura corrigir um lançamento no extrato
- **THEN** a tela só oferece o ajuste, e nenhum caminho de edição ou de remoção

#### Scenario: Ajuste sem motivo não é enviado

- **WHEN** o Admin tenta lançar um ajuste sem escrever o motivo
- **THEN** a aplicação não envia e diz que o motivo é obrigatório

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

### Requirement: A aplicação apresenta a agenda das aulas

A App 03 SHALL apresentar as aulas com **comunidade**, **ponto de apoio**, **data**, **horários**
e **situação**, em lista densa, filtráveis por comunidade e por período. A aula **pendente de
lastro** SHALL se distinguir da **confirmada** na apresentação, e a aula **cancelada** SHALL
exibir o **motivo** registrado.

O **Mestre** SHALL ler a agenda das comunidades a que está vinculado; a aplicação NEVER SHALL
lhe apresentar aula de comunidade a que não pertence. (`RF-02-12`, `RF-01-18`, `RN-02-09`,
`RN-02-20`, documento 15 §6)

#### Scenario: A agenda distingue as situações

- **WHEN** a agenda apresenta uma aula confirmada e uma pendente de lastro
- **THEN** cada uma aparece com a sua situação, distinguíveis sem depender só de cor

#### Scenario: Aula cancelada mostra o motivo

- **WHEN** a agenda apresenta uma aula cancelada
- **THEN** o motivo registrado no cancelamento aparece junto dela

#### Scenario: Mestre lê só a agenda das suas comunidades

- **WHEN** um Mestre vinculado a uma comunidade abre a agenda
- **THEN** só aparecem as aulas daquela comunidade

### Requirement: A aula agendada é cancelada com motivo

A App 03 SHALL permitir o cancelamento da aula agendada ao **Admin** e ao **Mestre da comunidade
da aula**, exigindo o **motivo** e NEVER SHALL aceitar o cancelamento sem ele. A aplicação SHALL
apresentar, antes de confirmar, que o cancelamento **libera os recursos reservados** e que ele
não se desfaz.

Cancelada a aula, a aplicação SHALL apresentá-la com a situação cancelada e o motivo, e NEVER
SHALL oferecer o cancelamento de aula que já teve desfecho. (`RF-02-95`, `RF-01-72`,
`RN-02-20`, PRD-02 §5.4)

#### Scenario: Admin cancela a aula com motivo

- **WHEN** um Admin em sessão confirma o cancelamento informando o motivo
- **THEN** a aula passa a cancelada, com o motivo, e a agenda a apresenta assim

#### Scenario: Cancelamento sem motivo é recusado no campo

- **WHEN** quem cancela confirma sem informar o motivo
- **THEN** a aplicação aponta o campo em falta e a aula segue como estava

#### Scenario: Mestre da comunidade da aula cancela

- **WHEN** um Mestre vinculado à comunidade da aula confirma o cancelamento com motivo
- **THEN** a aula passa a cancelada, e a aplicação não lhe oferece nenhuma outra escrita da
  agenda

#### Scenario: Aula com desfecho não oferece cancelamento

- **WHEN** a agenda apresenta uma aula já cancelada ou já realizada
- **THEN** o caminho de cancelamento não é oferecido para ela

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

### Requirement: A aplicação cumpre o piso de acessibilidade das oito aplicações

A App 03 SHALL ser Web App responsivo projetado primeiro para o celular e SHALL cumprir o
piso do documento 15 §5: contraste, alvo de toque de 48 px, foco sempre visível, nenhum
significado por cor sozinha, ícone acionável nunca sem rótulo e `prefers-reduced-motion`
respeitado. A linguagem das telas e dos erros SHALL ser simples, sem jargão de TI.
As telas SHALL cumprir esse piso consumindo a camada visual comum, e NEVER SHALL
reimplementar por conta própria o alvo de toque, o foco, a associação do erro ao campo nem a
tipografia. (PRD-02 §10, documento 15 §5, invariante 1)

#### Scenario: Operação pelo teclado

- **WHEN** o adulto percorre a aplicação apenas pelo teclado
- **THEN** todo elemento acionável recebe foco visível e a ordem de foco acompanha a leitura
  da tela

#### Scenario: Quem pediu menos movimento

- **WHEN** o aparelho declara `prefers-reduced-motion`
- **THEN** a aplicação não anima transição alguma, e nenhum conteúdo depende do movimento
  para ser lido

#### Scenario: Operação em pé, no celular

- **WHEN** a aplicação é aberta na largura de um celular
- **THEN** as telas desta fatia são operáveis sem rolagem horizontal, com alvos de toque de
  ao menos 48 px

#### Scenario: Erro de campo anunciado no próprio campo

- **WHEN** o Admin confirma a criação com um campo obrigatório vazio e depois alcança esse
  campo pelo teclado ou por leitor de tela
- **THEN** a mensagem que aponta o campo em falta é anunciada junto com o rótulo dele, e o
  campo é anunciado como inválido

#### Scenario: As telas usam a tipografia do documento 15

- **WHEN** qualquer tela da aplicação é apresentada
- **THEN** o texto é desenhado por Atkinson Hyperlegible Next e o título por Archivo, ambas
  servidas pelo próprio domínio da aplicação

### Requirement: A dependência externa de identidade só é acionada quando configurada

A App 03 SHALL acionar o provedor externo de identidade apenas quando o client ID do ambiente
em que ela roda estiver configurado, e NEVER SHALL carregar o script dele em ambiente que não
o tenha — conferência à mão, execução de teste ou demonstração. A tela de entrada SHALL
continuar apresentável nesse ambiente, sem apresentar a ausência do provedor como falha.
(documento 03 §1 princípio 2, PRD-02 §10)

#### Scenario: Ambiente sem client ID configurado

- **WHEN** a tela de entrada é apresentada num ambiente cujo client ID não está configurado
- **THEN** nenhum script do provedor externo de identidade é carregado, e a tela continua
  apresentável, sem mensagem de erro

#### Scenario: Ambiente com client ID configurado

- **WHEN** a tela de entrada é apresentada num ambiente cujo client ID está configurado
- **THEN** o caminho de entrada pela conta social é oferecido ao adulto

### Requirement: O Admin cadastra e edita o Guerreiro(a) pela aplicação

A App 03 SHALL oferecer ao Admin o cadastro de Guerreiro(a) com nome, data de nascimento, nick
e características do avatar, e a edição do que já foi cadastrado. A aplicação SHALL apontar o
campo em falta antes de chamar o núcleo e SHALL apresentar em linguagem simples a recusa por
nick em uso, **sem dizer de quem é o nick**. A aplicação NEVER SHALL exibir a imagem do
Guerreiro(a): a representação é o avatar. (`RF-02-01`, `RN-02-22`, invariante 12 do documento
99 §6, PRD-02 §11)

#### Scenario: Admin cadastra o Guerreiro(a)

- **WHEN** um Admin em sessão informa nome, nascimento, nick e avatar e confirma
- **THEN** o Guerreiro(a) passa a existir e a aplicação o apresenta entre os cadastrados

#### Scenario: Nick em uso é explicado sem revelar o dono

- **WHEN** o núcleo recusa o cadastro porque o nick já está em uso
- **THEN** a aplicação pede outro nick, sem informar quem o usa nem de que papel

#### Scenario: A gestão não vê a imagem da criança

- **WHEN** um Admin abre o cadastro de um Guerreiro(a)
- **THEN** a tela mostra avatar e nick, e nenhuma imagem real aparece

### Requirement: O Admin cadastra Mestre e Apoiador declarando os artefatos

A App 03 SHALL oferecer ao Admin o cadastro de Mestre e de Apoiador com nome, e-mail, WhatsApp
opcional e os artefatos comprobatórios, cada um com endereço e rótulo. A aplicação SHALL
impedir a confirmação sem ao menos um artefato e SHALL explicar por quê. A tela NEVER SHALL
oferecer anexo de arquivo como artefato, nem exigir nick. (`RF-02-02`, `RF-02-03`, `RF-02-04`,
`RN-02-01`, documento 02 §1)

#### Scenario: Admin cadastra Mestre com um link

- **WHEN** um Admin informa nome, e-mail e um link de currículo com rótulo e confirma
- **THEN** o Mestre passa a existir e a aplicação o apresenta entre os cadastrados

#### Scenario: Sem artefato a aplicação não deixa confirmar

- **WHEN** o Admin tenta confirmar o cadastro de um Apoiador sem artefato algum
- **THEN** a aplicação explica que ao menos um é obrigatório e nada é enviado ao núcleo

#### Scenario: A tela de adulto não pede nick ao Admin

- **WHEN** um Admin abre o cadastro de Mestre
- **THEN** a tela não exige nick, porque o Mestre o define no primeiro acesso

### Requirement: A aplicação oferece ao Admin gravar o nick do adulto na colisão

A App 03 SHALL oferecer ao Admin, na ficha de um Mestre ou de um Apoiador, o caminho de gravar
ou trocar o nick daquela persona, e SHALL sinalizar na lista quem está **sem nick**. A
aplicação SHALL apresentar em linguagem simples que o adulto sem nick não aparece em superfície
pública, e NEVER SHALL sugerir ao Admin um nick nem revelar de quem é o nick recusado.
(`RF-02-01`, `RN-01-30`, `RN-14-10`)

#### Scenario: Adulto sem nick é sinalizado na lista

- **WHEN** um Admin abre a lista de Mestres e Apoiadores
- **THEN** quem está sem nick aparece sinalizado, com o caminho de gravá-lo

#### Scenario: Admin grava o nick que recebeu por fora

- **WHEN** o Admin grava um nick disponível na ficha de um Apoiador sem nick
- **THEN** o nick passa a valer e a sinalização de ausência some

#### Scenario: A aplicação não sugere nick ao Admin

- **WHEN** o Admin abre o caminho de gravar nick
- **THEN** a tela não oferece sugestão alguma, e o nick é o que a pessoa lhe passou

### Requirement: O Admin inclui outro Admin e cadastra o responsável com o vínculo

A App 03 SHALL oferecer ao Admin a inclusão manual de outro Admin (`RF-02-05`) e o cadastro de
responsável com o **vínculo** a Guerreiros e Guerreiras já cadastrados, declarando o **grau de
parentesco** em texto livre (`RF-02-06`). A aplicação SHALL impedir o quarto vínculo de um
mesmo Guerreiro(a), respeitando o teto de três responsáveis, e SHALL oferecer a criação de
**credencial de usuário e senha provisória** para o adulto sem conta social (`RF-02-07`).
(`RN-02-02`, `RN-02-08`, invariante 3 do documento 99 §6)

#### Scenario: Admin inclui outro Admin

- **WHEN** um Admin em sessão informa nome e e-mail de um novo Admin e confirma
- **THEN** o Admin novo passa a existir, sem nenhum caminho de autocadastro envolvido

#### Scenario: Responsável é vinculado com grau de parentesco

- **WHEN** o Admin cadastra um responsável e o vincula a um Guerreiro(a) declarando o
  parentesco
- **THEN** o vínculo passa a existir com o parentesco declarado

#### Scenario: Quarto responsável é barrado

- **WHEN** o Admin tenta vincular um quarto responsável ao mesmo Guerreiro(a)
- **THEN** a aplicação explica o teto de três e o vínculo não é criado

#### Scenario: Adulto sem conta social recebe senha provisória

- **WHEN** o Admin cria credencial de usuário e senha provisória para um adulto cadastrado
- **THEN** a aplicação exibe a senha provisória uma vez, para entrega, e não a recupera depois

### Requirement: A aplicação reúne as filas numa lista só, com filtro por natureza

A App 03 SHALL apresentar as solicitações numa **área Filas** única, com **filtro por
natureza**, e NEVER SHALL abrir uma área separada por natureza. Cada item SHALL mostrar a
natureza a que pertence, quem enviou, a situação e o prazo, e SHALL distinguir visualmente o
que está **em atraso** — por rótulo e não apenas por cor. (`RF-02-18`, `RF-02-65`,
`RF-02-25`, PRD-02 §10, documento 15 §5)

A área SHALL ser aberta apenas por **Admin**; para os demais papéis a aplicação SHALL
apresentar a recusa em linguagem simples, e não um erro cru. (`RN-02-01`, `RF-01-16`)

Nesta fatia a área SHALL servir a natureza **participação**; as demais SHALL entrar sem que a
lista, o filtro ou a apresentação do atraso mudem de forma. (PRD-02 §6.2)

#### Scenario: Admin abre a área Filas

- **WHEN** um Admin em sessão abre a área Filas
- **THEN** vê as solicitações numa lista só, com o filtro por natureza e, em cada item, a
  natureza, quem enviou, a situação e o prazo

#### Scenario: O atraso é anunciado por rótulo, não só por cor

- **WHEN** a lista traz uma solicitação em atraso
- **THEN** ela vem com um rótulo textual que diz isso, legível também sem distinguir cores

#### Scenario: Quem não é Admin lê a recusa, não um erro

- **WHEN** um Mestre em sessão abre a área Filas
- **THEN** a aplicação explica em linguagem simples que a área é do Admin, sem exibir código
  nem mensagem técnica

### Requirement: O Admin avalia a solicitação de participação pela aplicação

A App 03 SHALL oferecer ao Admin o desfecho da solicitação de participação — **aceitar** ou
**recusar** — com o **parecer** informado na própria tela, e SHALL apresentar, depois do
desfecho, a situação final, o parecer, quem avaliou e a data. A recusa SHALL exigir o motivo
no parecer antes de chamar o núcleo. (`RF-02-19`, `RF-02-86`)

A tela SHALL apresentar a identificação, a pretensão, a apresentação, a instituição, os links
declarados e, no pré-cadastro de Apoiador, o **aporte declarado** e o **nick pretendido**.
(`RF-02-18`, `RF-02-83`)

A aplicação SHALL apresentar em linguagem simples a recusa do núcleo por solicitação já
avaliada, e NEVER SHALL oferecer reavaliação de solicitação com desfecho gravado.

#### Scenario: Admin aceita e vê o desfecho registrado

- **WHEN** um Admin aceita uma solicitação informando o parecer
- **THEN** a tela passa a mostrar a situação aceita, o parecer, quem avaliou e a data

#### Scenario: Recusa sem motivo é apontada antes de chamar o núcleo

- **WHEN** um Admin escolhe recusar e confirma com o parecer vazio
- **THEN** a aplicação aponta o campo em falta junto do rótulo dele, e nada é enviado ao núcleo

#### Scenario: Solicitação já avaliada não oferece desfecho

- **WHEN** o Admin abre uma solicitação que já tem desfecho gravado
- **THEN** a tela mostra o desfecho e não oferece aceitar nem recusar

### Requirement: A solicitação aceita abre o cadastro pré-preenchido, sem criar acesso

A App 03 SHALL oferecer, a partir de uma solicitação **aceita**, a abertura do cadastro de
**Mestre** ou de **Apoiador** conforme a pretensão declarada, com os campos **pré-preenchidos**
pelo que a solicitação trouxe. O cadastro SHALL continuar sendo ato explícito do Admin: aceitar
a solicitação NEVER SHALL criar persona, credencial ou acesso por si só. (`RF-02-20`,
`RN-02-03`, `RN-01-28`)

O pré-preenchimento SHALL ser editável pelo Admin antes da confirmação, e o cadastro SHALL
passar pelas mesmas exigências de sempre — entre elas ao menos um artefato comprobatório de
Mestre ou Apoiador. (`RF-02-04`, `RN-02-01`)

#### Scenario: Aceitar não cadastra ninguém

- **WHEN** um Admin aceita uma solicitação de participação
- **THEN** nenhuma persona passa a existir, e a aplicação apenas oferece abrir o cadastro

#### Scenario: O cadastro abre com o que a solicitação trouxe

- **WHEN** o Admin abre o cadastro a partir de uma solicitação aceita com pretensão de Apoiador
- **THEN** o formulário de Apoiador aparece com os dados da solicitação já preenchidos e
  editáveis

#### Scenario: O cadastro pré-preenchido cumpre as mesmas exigências

- **WHEN** o Admin confirma o cadastro pré-preenchido sem nenhum artefato comprobatório
- **THEN** a aplicação aponta a falta e o cadastro não é criado

### Requirement: O Admin homologa pela aplicação o aporte declarado no pré-cadastro

A App 03 SHALL oferecer ao Admin, sobre uma solicitação de participação com **aporte
declarado**, o registro do aporte apontando a solicitação de origem, e SHALL apresentar depois
o valor **em moedas** creditado. A tela NEVER SHALL apresentar o aporte em reais.
(`RF-02-84`, `RF-07-30`, `RN-02-19`, `RN-07-21`, invariante 16 do documento 99 §6)

A aplicação SHALL apresentar em linguagem simples a recusa do núcleo por solicitação **já
homologada**, e SHALL deixar de oferecer a homologação depois que ela ocorreu.

#### Scenario: Admin homologa o aporte declarado

- **WHEN** um Admin registra o aporte apontando a solicitação de participação de origem
- **THEN** a tela passa a mostrar o aporte homologado, com o valor em moedas

#### Scenario: A homologação não se repete

- **WHEN** o Admin abre uma solicitação cujo aporte declarado já foi homologado
- **THEN** a tela mostra a homologação registrada e não oferece homologar de novo

#### Scenario: O aporte aparece em moedas, nunca em reais

- **WHEN** a tela apresenta um aporte homologado
- **THEN** o valor aparece em moedas da plataforma, e nenhum valor em reais é exibido

### Requirement: A área Filas serve as quatro naturezas sob o mesmo filtro

A App 03 SHALL apresentar, na área Filas já existente, também as solicitações de **dados**, as
de **chave** e as **sugestões e propostas**, sob o mesmo filtro por natureza e com a mesma
apresentação do atraso. A aplicação NEVER SHALL abrir área separada para nenhuma delas.
(`RF-02-25`, `RF-02-77`, `RF-02-87`, PRD-02 §6.2)

Cada natureza SHALL mostrar o que lhe é próprio: a de dados, o solicitante, a instituição, a
finalidade declarada e o recorte pedido; a de chave, quem pediu e o que pretende construir; a
sugestão, o autor, a persona dele e o teor. (`RF-02-77`, `RF-02-87`, `RF-02-25`)

#### Scenario: O filtro alcança as quatro naturezas

- **WHEN** um Admin em sessão abre a área Filas e percorre o filtro por natureza
- **THEN** pode ver participação, dados, chave e sugestões, cada uma com os seus campos

#### Scenario: Cada natureza mostra o que lhe é próprio

- **WHEN** o Admin filtra pela natureza dados
- **THEN** cada item traz solicitante, instituição, finalidade declarada e recorte pedido

### Requirement: A tela da solicitação de dados apresenta ao Admin os três critérios

A App 03 SHALL apresentar, na avaliação da solicitação de dados, os **três critérios de
aprovação** — solicitante identificado, finalidade compatível e não reidentificação — e SHALL
exigir do Admin a afirmação do **compromisso de não reidentificação** antes de aprovar. O
parecer SHALL ser obrigatório na aprovação e na recusa, apontado no próprio campo antes de
chamar o núcleo. (`RF-02-93`, `RF-02-78`, `RN-02-26`)

A aplicação SHALL apresentar, depois do desfecho, **o que foi entregue e a quem**, e SHALL
deixar claro que a entrega é **gratuita e anonimizada**. (`RF-02-79`)

#### Scenario: Os critérios aparecem antes da decisão

- **WHEN** um Admin abre uma solicitação de dados para avaliar
- **THEN** a tela apresenta os três critérios de aprovação antes de oferecer aprovar ou recusar

#### Scenario: Aprovar exige afirmar o compromisso

- **WHEN** o Admin escolhe aprovar sem marcar o compromisso de não reidentificação
- **THEN** a aplicação aponta a falta junto do rótulo e nada é enviado ao núcleo

#### Scenario: A entrega registrada aparece na tela

- **WHEN** o Admin abre uma solicitação de dados já aprovada e entregue
- **THEN** a tela mostra o que foi entregue e a quem, e diz que a entrega foi gratuita e
  anonimizada

### Requirement: A aprovação do pedido de chave e a emissão são dois atos na tela

A App 03 SHALL oferecer ao Admin, sobre a solicitação de chave, primeiro o **desfecho** —
aprovar ou recusar, com parecer — e só depois, sobre a solicitação aprovada, a **emissão**. A
aplicação NEVER SHALL emitir a chave no mesmo ato da aprovação. (`RF-02-88`, `RF-02-89`)

A emissão SHALL apresentar o **identificador** e o **segredo**, com o aviso de que o segredo
aparece **uma única vez** e não é recuperável depois. A aplicação NEVER SHALL guardar o segredo
nem reapresentá-lo em consulta posterior. (`RF-02-89`, `RN-02-28`)

A solicitação que já rendeu chave NEVER SHALL oferecer emissão de novo.

#### Scenario: Aprovar não emite

- **WHEN** um Admin aprova uma solicitação de chave
- **THEN** a tela mostra o desfecho gravado e passa a oferecer a emissão como ato seguinte

#### Scenario: O segredo é mostrado uma vez, com o aviso

- **WHEN** o Admin emite a chave
- **THEN** a tela apresenta o identificador e o segredo, avisando que o segredo não será
  mostrado de novo

#### Scenario: O segredo não volta numa consulta posterior

- **WHEN** o Admin volta à mesma solicitação depois de sair da tela de emissão
- **THEN** o segredo não aparece, e a tela mostra apenas que a chave foi emitida

#### Scenario: Solicitação que já rendeu chave não emite outra

- **WHEN** o Admin abre uma solicitação aprovada cuja chave já foi emitida
- **THEN** a tela não oferece emitir de novo

### Requirement: A aplicação apresenta o painel das chaves emitidas

A App 03 SHALL apresentar ao Admin as chaves emitidas com **prazo de apresentação**, **URL
apresentada** quando houver e **situação**, e SHALL **destacar** as que estão com o prazo a
vencer e as **revogadas automaticamente por prazo vencido**. O destaque SHALL ser legível sem
distinguir cores. (`RF-02-90`, `RF-02-91`, `RN-02-29`, documento 15 §5)

A App 03 SHALL oferecer ao Admin a **revogação a qualquer tempo, com motivo**, exigido antes de
chamar o núcleo. (`RF-02-92`)

O painel NEVER SHALL apresentar o segredo nem o seu resumo criptográfico. (`RN-02-28`)

#### Scenario: O painel mostra o ciclo de vida de cada chave

- **WHEN** um Admin em sessão abre o painel de chaves
- **THEN** cada chave aparece com prazo, URL apresentada quando houver e situação

#### Scenario: Prazo a vencer e revogação por decurso são destacados por rótulo

- **WHEN** o painel traz uma chave com prazo a vencer e outra revogada por prazo vencido
- **THEN** as duas vêm com rótulo textual que diz isso, legível também sem distinguir cores

#### Scenario: Revogar exige o motivo

- **WHEN** o Admin escolhe revogar uma chave e confirma sem informar o motivo
- **THEN** a aplicação aponta o campo em falta e nada é enviado ao núcleo

#### Scenario: O painel nunca mostra o segredo

- **WHEN** o painel apresenta qualquer chave
- **THEN** o segredo não aparece em campo algum

### Requirement: O Admin avalia a sugestão e a tela mostra o retorno a quem propôs

A App 03 SHALL oferecer ao Admin o desfecho da sugestão — **adotada** ou **não adotada** —, com
o **motivo do retorno** exigido na não adotada, em linguagem simples, apontado antes de chamar
o núcleo. A tela SHALL apresentar, depois do desfecho, o retorno que chegará a quem propôs.
(`RF-02-26`, `RN-02-25`)

A aplicação SHALL apresentar, na sugestão adotada, que **20 pontos extras e o badge de
protagonismo** foram creditados a quem propôs. (`RF-01-56`, `RN-01-50`)

Todo o retorno SHALL acontecer **dentro da plataforma**: a aplicação NEVER SHALL oferecer envio
por e-mail. (`RN-02-25`)

#### Scenario: Não adotada exige o motivo do retorno

- **WHEN** o Admin escolhe não adotar e confirma sem o motivo do retorno
- **THEN** a aplicação aponta o campo em falta e nada é enviado ao núcleo

#### Scenario: Adotada mostra o que foi creditado

- **WHEN** o Admin adota uma sugestão
- **THEN** a tela mostra que 20 pontos extras e o badge de protagonismo foram creditados a quem
  propôs

#### Scenario: O retorno não sai por e-mail

- **WHEN** o Admin conclui a avaliação de uma sugestão
- **THEN** a aplicação não oferece envio por e-mail, e o retorno fica dentro da plataforma

### Requirement: A área Filas apresenta a fila das solicitações do responsável

A aplicação SHALL apresentar, na área **Filas**, a fila das solicitações vindas da App 07, com
**protocolo**, **tipo**, **situação** e o **prazo de 7 dias** de cada uma, da mais antiga para a
mais recente, e SHALL identificar o Guerreiro(a) a que a solicitação se refere e o responsável
que a abriu. A lista é da gestão: NEVER SHALL ser alcançada por Mestre. (`RF-02-23`, PRD-02 §5.8)

#### Scenario: A fila mostra o que o Admin precisa para triar

- **WHEN** o Admin abre a fila das solicitações do responsável
- **THEN** cada item traz protocolo, tipo, situação e o prazo de 7 dias

#### Scenario: O Mestre não alcança a fila

- **WHEN** um Mestre abre a área Filas
- **THEN** a fila das solicitações do responsável não lhe é oferecida

### Requirement: O Admin registra o desfecho da solicitação do responsável

A aplicação SHALL oferecer, sobre a solicitação escolhida, a tela de tratamento com o texto do
pedido e o registro do **desfecho** — aceita ou recusada —, com o texto do que foi tratado. Feito
o registro, a tela SHALL mostrar **quem tratou** e **quando**, e a solicitação tratada NEVER
SHALL oferecer novo tratamento. (`RF-02-24`)

#### Scenario: Desfecho registrado mostra o autor e a data

- **WHEN** o Admin registra o desfecho de uma solicitação
- **THEN** a solicitação passa a exibir o desfecho, quem tratou e a data e hora

#### Scenario: Solicitação tratada não reabre o tratamento

- **WHEN** o Admin abre uma solicitação que já tem desfecho
- **THEN** a tela a apresenta em leitura, sem caminho para novo desfecho

### Requirement: A solicitação sem desfecho em 7 dias aparece em atraso na fila

A aplicação SHALL destacar na fila, como **em atraso**, a solicitação sem desfecho cujo prazo já
venceu, e o item em atraso SHALL continuar tratável como qualquer outro — o atraso NEVER SHALL
retirá-lo da fila nem bloquear o tratamento. (`RF-02-66`)

#### Scenario: Vencido o prazo, a fila destaca o atraso

- **WHEN** a fila traz uma solicitação sem desfecho com o prazo vencido
- **THEN** ela aparece destacada como em atraso

#### Scenario: O atraso não impede o tratamento

- **WHEN** o Admin abre uma solicitação em atraso
- **THEN** trata e registra o desfecho normalmente

### Requirement: A App 03 abre a partida sobre a atividade e as equipes da aula

A aplicação SHALL oferecer ao Mestre que conduz — e ao Admin — a abertura da partida de Quiz
ao Vivo a partir da aula em andamento, escolhendo a **atividade de competição ao vivo** sobre
a qual ela corre e as **equipes formadas na App 01** naquele encontro. A tela SHALL apresentar
as equipes por **avatar e nick**, sem dado pessoal algum, e NEVER SHALL exibir imagem real de
Guerreiro(a). Não havendo equipe formada na aula, a aplicação SHALL dizê-lo em uma frase, sem
oferecer a abertura. (`RF-02-59`, `RF-02-61`, PRD-02 §§11, 12)

#### Scenario: O Mestre abre a partida escolhendo atividade e equipes

- **WHEN** o Mestre que conduz escolhe a atividade de competição ao vivo e marca as equipes
  disputantes
- **THEN** a aplicação abre a partida e passa à tela de condução

#### Scenario: As equipes aparecem por avatar e nick

- **WHEN** a tela de abertura lista as equipes da aula
- **THEN** cada integrante aparece por avatar e nick, sem nome, idade ou imagem real

#### Scenario: Aula sem equipe formada não abre partida

- **WHEN** a aula em andamento não tem equipe formada
- **THEN** a aplicação informa em uma frase que não há equipe e não oferece a abertura

### Requirement: A tela de condução governa o ritmo da partida

A aplicação SHALL oferecer a quem conduz, na partida aberta, quatro atos: **pôr uma pergunta
no ar**, escolhida do banco da missão daquela atividade; **liberar o resultado** da pergunta
no ar; **anular** a pergunta contestada; e **encerrar** a partida. Não há tempo por pergunta —
o ritmo é de quem conduz. A tela SHALL mostrar, enquanto o resultado não está liberado,
quantas equipes já responderam, sem revelar o que responderam; liberado, SHALL mostrar a
alternativa correta, as equipes que acertaram e a primeira delas. O encerramento SHALL avisar
que a pontuação será lançada automaticamente às equipes. (`RF-02-60`, `RF-02-62`, `RF-02-72`,
`RF-02-73`, documento 05 §5)

#### Scenario: Quem conduz põe a pergunta no ar

- **WHEN** quem conduz escolhe uma pergunta do banco da missão e dá o _start_
- **THEN** a tela passa a mostrar a pergunta no ar e quantas equipes já responderam

#### Scenario: Antes de liberar, a tela não revela as respostas

- **WHEN** equipes respondem e o resultado ainda não foi liberado
- **THEN** a tela mostra apenas a contagem de quem respondeu, sem a alternativa de ninguém

#### Scenario: Liberado o resultado, a tela mostra quem acertou

- **WHEN** quem conduz libera o resultado da pergunta no ar
- **THEN** a tela mostra a alternativa correta, as equipes que acertaram e qual chegou
  primeiro

#### Scenario: A pergunta contestada é anulada

- **WHEN** quem conduz anula a pergunta contestada
- **THEN** a tela marca a pergunta como anulada e informa que ela não credita ninguém

#### Scenario: O encerramento avisa do lançamento

- **WHEN** quem conduz encerra a partida
- **THEN** a aplicação confirma o encerramento e informa que a pontuação foi lançada às
  equipes

### Requirement: A tela de condução acompanha a partida por sondagem a cada 2 segundos

A aplicação SHALL manter a tela de condução atualizada **sondando o núcleo a cada 2
segundos**, sem recarga manual e sem conexão longa (documento 03 §1, decisão do fundador de
2026-08-25). Sondagem que falha por rede NEVER SHALL derrubar a partida nem apagar o que já
está na tela: a aplicação SHALL avisar que perdeu contato e SHALL retomar o estado corrente na
sondagem seguinte. (`RF-02-60`, PRD-02 §§10, 12)

#### Scenario: A tela acompanha sem recarga

- **WHEN** a partida está aberta e equipes vão respondendo
- **THEN** a contagem na tela avança sozinha, sem que quem conduz recarregue

#### Scenario: A queda de rede não derruba a partida

- **WHEN** uma sondagem falha por rede
- **THEN** a tela avisa que perdeu contato, mantém o que já exibia e volta ao estado corrente
  na sondagem seguinte

### Requirement: O Mestre alcança a condução da partida e nada mais da gestão

A aplicação SHALL permitir ao Mestre autenticado ler o painel, conduzir a partida de quiz da
aula dele e **registrar a infração ocorrida na aula, sobre atividade de trilha que ele autora**
— e SHALL apresentar a recusa do núcleo em qualquer outra escrita de gestão. Mestre que tenta
conduzir a partida de uma aula que não é dele, ou registrar infração sobre atividade de trilha
que não é dele, SHALL receber a recusa, dita em uma frase, sem que a tela ofereça caminho
alternativo.

O Mestre NEVER SHALL alcançar o lançamento da atividade realizada por aula, que é do Admin, nem
o ajuste das presenças. (`RF-02-49`, `RN-02-20`, `RF-02-37`, `RN-02-13`, PRD-02 §§4, 12)

#### Scenario: Mestre conduz a partida da sua aula

- **WHEN** o Mestre autenticado abre a condução da partida da aula dele
- **THEN** a aplicação oferece os quatro atos da condução

#### Scenario: Mestre de outra aula é recusado

- **WHEN** o Mestre tenta conduzir a partida de uma aula que não é dele
- **THEN** a aplicação apresenta a recusa em uma frase e não oferece caminho alternativo

#### Scenario: Mestre registra a infração da atividade que autora

- **WHEN** o Mestre autor da trilha registra a infração ocorrida na aula sobre uma atividade
  dela
- **THEN** a aplicação a grava e informa que ela valeu no ato

#### Scenario: Mestre que não é o autor é recusado

- **WHEN** o Mestre tenta registrar infração sobre atividade de trilha que não é dele
- **THEN** a aplicação apresenta a recusa em uma frase e não oferece caminho alternativo

#### Scenario: O Mestre não alcança o lançamento nem o ajuste de presença

- **WHEN** o Mestre abre a área Lançamentos
- **THEN** a tela lhe oferece apenas o registro da infração, e nem o lançamento da atividade
  realizada nem o ajuste das presenças

### Requirement: A App 03 abre a área Painel do dia, em leitura

A App 03 SHALL apresentar a área **Painel do dia**, que mostra o encontro em andamento numa tela
só: quem chegou, quem aguarda aparelho, as equipes com a missão de cada uma, a atividade prevista
e os recursos providos, o saldo dos tipos de recurso do ponto de apoio e os lançamentos
pendentes do encontro (`RF-02-41` a `RF-02-47`, `RF-02-69`).

A área SHALL ser de **leitura**: ela NEVER SHALL oferecer botão que lance, que edite equipe ou
que altere presença. Cada pendência listada SHALL levar o operador à tela que já a resolve, e é
lá que a escrita acontece.

Fora da janela de toda aula agendada, a área SHALL dizer em uma frase que não há encontro em
andamento, sem apresentar tela vazia nem erro cru. (`RF-02-41` a `RF-02-47`, `RF-02-69`,
`RN-02-12`, PRD-02 §§6.4, 12)

#### Scenario: A área mostra o encontro em andamento

- **WHEN** um Admin abre o Painel do dia durante a janela de uma aula
- **THEN** a tela apresenta presenças, espera, equipes com missão, previsto e provido, saldo e
  lançamentos pendentes

#### Scenario: Sem encontro, a área explica em uma frase

- **WHEN** o Painel do dia é aberto fora da janela de toda aula agendada
- **THEN** a tela diz que não há encontro em andamento, sem erro cru

#### Scenario: A área não oferece escrita

- **WHEN** o operador procura lançar ou alterar algo pela tela do painel
- **THEN** a tela não oferece caminho de escrita, e leva à tela que resolve aquela pendência

#### Scenario: A tela não exibe imagem real de criança

- **WHEN** o painel apresenta presenças e equipes
- **THEN** cada Guerreiro(a) aparece por nick e avatar, e nenhuma imagem real é exibida

### Requirement: O painel se atualiza sozinho durante o encontro

A App 03 SHALL manter o Painel do dia atualizado **por sondagem**, sem recarga manual, no mesmo
padrão já usado na condução da partida de quiz. O operador NEVER SHALL precisar recarregar a
página para ver quem acabou de chegar ou a equipe que acabou de trocar de missão.

Caindo a rede, a tela SHALL manter legível o que já carregou e SHALL dizer que parou de
atualizar, retomando sozinha quando a rede voltar. (`RF-02-48`, PRD-02 §6.4)

#### Scenario: A chegada aparece sem recarga

- **WHEN** um Guerreiro(a) tem a presença registrada pela App 01 com o painel aberto
- **THEN** ele passa a aparecer no painel sem que ninguém recarregue a página

#### Scenario: A troca de missão aparece sem recarga

- **WHEN** uma equipe declara outra atividade da programação com o painel aberto
- **THEN** o painel passa a mostrá-la na missão nova sem recarga

#### Scenario: Sem rede, a tela avisa e não apaga o que carregou

- **WHEN** a rede cai com o painel aberto
- **THEN** a tela segue legível, diz que parou de atualizar e retoma sozinha quando a rede volta

### Requirement: A gestão anexa a digitalização do termo pela tela do painel

A App 03 SHALL oferecer ao **Admin**, a partir da lista de termos que aguardam digitalização, o
caminho para **anexar a digitalização** do termo de biometria assinado no encontro, em PDF, JPG
ou PNG (`RF-02-68`).

A tela SHALL dizer em linguagem simples a recusa de formato fora dos três e a recusa do termo
que já tem digitalização. O Mestre NEVER SHALL receber o caminho de anexar: ele lê o painel e
não escreve nele (`RN-02-20`). (`RF-02-68`, `RF-02-69`, `RN-02-20`, PRD-02 §§6.3, 6.4)

#### Scenario: O Admin anexa a digitalização a partir da pendência

- **WHEN** um Admin escolhe um termo pendente e envia a digitalização em PDF
- **THEN** a aplicação a anexa e a pendência sai da lista na atualização seguinte

#### Scenario: Formato recusado é explicado

- **WHEN** o Admin envia um arquivo que não é PDF, JPG nem PNG
- **THEN** a tela diz em linguagem simples quais formatos valem, e nada é enviado

#### Scenario: O Mestre não recebe o caminho de anexar

- **WHEN** um Mestre abre o painel com termos aguardando digitalização
- **THEN** a tela lista a pendência e não oferece a ele o caminho de anexar

### Requirement: A App 03 abre a área Lançamentos sobre a aula vigente

A App 03 SHALL apresentar a área **Lançamentos**, que opera sobre a **aula vigente** — a mesma
que o painel do dia mostra — e reúne os três atos que fecham o encontro antes de ele acabar:
lançar a atividade realizada, conferir e ajustar as presenças e registrar a infração ocorrida
na aula (`RF-02-46`, `RF-02-47`, PRD-02 §5.6).

A pendência `lancamento_da_atividade_realizada`, listada no painel do dia, SHALL levar o
operador a esta área — é aqui que a escrita acontece, e o painel permanece em leitura.

Fora da janela de toda aula agendada, a área SHALL dizer em uma frase que não há encontro em
andamento, sem apresentar tela vazia nem erro cru. (`RF-02-34`, `RF-02-36`, `RF-02-37`,
`RF-02-39`, PRD-02 §§5.6, 6.3, 12)

#### Scenario: A área abre sobre a aula vigente

- **WHEN** um Admin abre a área Lançamentos durante a janela de uma aula
- **THEN** a tela apresenta os participantes, as presenças e a atividade prevista daquela aula

#### Scenario: Sem encontro, a área explica em uma frase

- **WHEN** a área Lançamentos é aberta fora da janela de toda aula agendada
- **THEN** a tela diz que não há encontro em andamento, sem erro cru

#### Scenario: A pendência do painel leva à área

- **WHEN** o Admin escolhe a pendência de lançamento da atividade realizada no painel do dia
- **THEN** a aplicação o leva à área Lançamentos daquela aula

### Requirement: O lançamento atribui o desfecho de cada participante num ato só

A área Lançamentos SHALL apresentar, para a atividade prevista da aula, a lista dos
participantes e SHALL exigir de cada um o **desfecho** entre os três valores fechados —
**realizada**, **realizada com mérito** e **mérito extra por auxílio aos colegas** —, além do
momento do fato e da produção. É o terceiro valor que credita o ponto extra a quem ajudou o
colega, e a tela NEVER SHALL oferecer campo de valor: o número vem da tabela do documento 11
§5 (`RF-02-39`).

O lançamento SHALL ser enviado como **um único ato por aula**, com todos os participantes
juntos, e a tela SHALL informar que ele converteu as reservas em baixa e passou a aula a
realizada. Participante sem desfecho SHALL impedir o envio, com a falta dita na tela.
(`RF-02-34`, `RF-02-39`, `RN-02-21`, PRD-02 §§6.3, 12)

#### Scenario: O Admin lança os participantes com o desfecho de cada um

- **WHEN** o Admin atribui o desfecho de cada participante e envia o lançamento
- **THEN** a aplicação envia um único lançamento com todos eles e informa que a aula passou a
  realizada e que as reservas viraram baixa

#### Scenario: O mérito extra por auxílio é um dos três desfechos

- **WHEN** o Admin marca "mérito extra por auxílio aos colegas" para o Guerreiro(a) que ajudou
- **THEN** a aplicação envia esse desfecho, sem que a tela peça ou aceite o valor da pontuação

#### Scenario: Participante sem desfecho impede o envio

- **WHEN** o Admin tenta enviar o lançamento com um participante sem desfecho
- **THEN** a aplicação não envia e diz qual participante está sem desfecho

#### Scenario: O lançamento gravado não se edita

- **WHEN** o Admin volta à área depois de a aula ter sido lançada
- **THEN** a tela apresenta o lançamento em leitura e não oferece caminho de edição nem de
  remoção

### Requirement: A área confere as presenças e registra o ajuste

A área Lançamentos SHALL apresentar as presenças daquela aula vindas do App 01, cada uma com o
**modo de comprovação** e, quando houver, quem confirmou. A tela SHALL oferecer dois ajustes:
**registrar por confirmação** a presença que faltou, gravando quem confirmou, e **anular** a
presença registrada por engano, exigindo o **motivo**. Anulada uma presença, a tela SHALL
permitir registrar em seguida a presença correta do mesmo Guerreiro(a) naquela aula.

A presença anulada SHALL permanecer visível, marcada como anulada e com o motivo — a correção
nunca apaga o registro (`RN-02-12`). A tela SHALL apresentar a recusa do núcleo em uma frase, e
NEVER SHALL exibir imagem real do Guerreiro(a): a representação é o avatar e o nick
(`RN-02-22`). (`RF-02-36`, `RN-02-12`, `RN-02-21`, `RN-02-22`, PRD-02 §§6.3, 12)

#### Scenario: O Admin registra a presença que faltou

- **WHEN** o Admin confirma a presença de um Guerreiro(a) que chegou e não foi reconhecido
- **THEN** a aplicação grava a presença por confirmação, com ele como confirmador, e a lista
  passa a mostrá-la

#### Scenario: O Admin anula a presença registrada por engano

- **WHEN** o Admin anula, com motivo, uma presença registrada por engano
- **THEN** a aplicação grava a anulação e a lista mostra a presença marcada como anulada, com
  o motivo

#### Scenario: Anulação sem motivo não é enviada

- **WHEN** o Admin tenta anular uma presença sem escrever o motivo
- **THEN** a aplicação não envia e diz que o motivo é obrigatório

#### Scenario: A lista de presenças mostra avatar e nick

- **WHEN** a área apresenta as presenças do encontro
- **THEN** cada Guerreiro(a) aparece por nick e avatar, e nenhuma imagem real é exibida

### Requirement: A área registra a infração ocorrida na aula, sem revisão de terceiro

A área Lançamentos SHALL oferecer o registro da **infração** ocorrida na aula, vinculada ao
**encontro**, à **atividade** e ao **Guerreiro(a)**, com o **motivo** em texto livre. O
registro SHALL valer **no ato**, sem fila de revisão e sem intervenção de outro adulto
(`RN-02-13`). A tela NEVER SHALL oferecer campo de valor da pontuação negativa: o número vem da
tabela do documento 11 §5.

A tela SHALL declarar, junto ao campo do motivo, que **descuido acidental com material comum
não é infração e não gera pontuação negativa** (`RN-02-14`). Infração sem motivo SHALL impedir
o envio, e a recusa do núcleo — entre elas o teto da aula já alcançado e a atividade que não é
daquela aula — SHALL ser apresentada em uma frase. (`RF-02-37`, `RN-02-13`, `RN-02-14`,
`RN-02-21`, PRD-02 §§6.3, 12)

#### Scenario: O registro vale no ato

- **WHEN** o operador registra a infração de um Guerreiro(a) declarando a atividade e o motivo
- **THEN** a aplicação a grava e informa que ela valeu no ato, sem fila de revisão

#### Scenario: A tela não pede o valor

- **WHEN** o operador preenche o registro da infração
- **THEN** a tela não apresenta campo de valor da pontuação negativa

#### Scenario: A tela avisa que descuido acidental não é infração

- **WHEN** o operador abre o registro da infração
- **THEN** a tela declara que descuido acidental com material comum não é infração e não gera
  pontuação negativa

#### Scenario: Infração sem motivo não é enviada

- **WHEN** o operador tenta registrar a infração sem escrever o motivo
- **THEN** a aplicação não envia e diz que o motivo é obrigatório

#### Scenario: O teto da aula é dito em uma frase

- **WHEN** o núcleo recusa a infração porque o teto daquele Guerreiro(a) na aula foi alcançado
- **THEN** a tela apresenta a recusa em uma frase, sem erro cru

### Requirement: O Admin encerra o ciclo por uma tela da gestão

A App 03 SHALL oferecer ao Admin a tela do **encerramento do ciclo**, e SHALL exigir
confirmação explícita antes de executá-lo, porque o expurgo do motivo das ocorrências de
conduta não se desfaz. A tela SHALL dizer, antes da confirmação, os dois efeitos do ato — o
expurgo dos motivos guardados e a saída das ocorrências do ranking público — e SHALL deixar
claro que o ciclo seguinte **não** é declarado ali. (`RF-02-99`, `RF-02-100`, `RN-02-30`)

#### Scenario: O ato pede confirmação antes de executar

- **WHEN** o Admin aciona o encerramento do ciclo na App 03
- **THEN** a tela apresenta os dois efeitos do ato e pede confirmação explícita, sem executar
  nada ainda

#### Scenario: Confirmado, o ato é executado e o resultado é exibido

- **WHEN** o Admin confirma o encerramento
- **THEN** a App 03 executa o ato no núcleo e exibe o resultado dele

#### Scenario: Desistir não executa nada

- **WHEN** o Admin desiste diante da confirmação
- **THEN** nenhum motivo é expurgado e nada muda

#### Scenario: A tela não oferece declarar o ciclo seguinte

- **WHEN** a tela do encerramento do ciclo é apresentada
- **THEN** ela não oferece campo, opção nem etapa para declarar o ciclo seguinte

### Requirement: A App 03 abre a área Território sob a comunidade escolhida

A App 03 SHALL abrir a área **Território** ao adulto em sessão, com a **comunidade escolhida
no seletor** que as áreas Pontos de Apoio e Filas já usam, e SHALL apresentar os locais já
cadastrados naquela comunidade **na hierarquia de seis níveis**, cada local sob o seu pai, para
que o Admin saiba o que já há antes de cadastrar. A apresentação SHALL ser **lista densa**, no
temperamento Operação, como a das comunidades e a dos pontos de apoio.

Comunidade **sem local algum** SHALL ser apresentada como comunidade vazia — o estado normal de
quem acabou de nascer (`RN-08-01`) —, e a ausência NEVER SHALL ser apresentada como falha.
(`RF-02-16`, `RF-08-04`, `RF-01-18`, documento 15 §6)

#### Scenario: A área abre com os locais da comunidade escolhida

- **WHEN** o adulto em sessão abre a área Território e escolhe uma comunidade que já tem locais
- **THEN** a aplicação apresenta os locais daquela comunidade, cada um sob o local pai dele

#### Scenario: Trocar a comunidade troca a hierarquia apresentada

- **WHEN** o adulto troca a comunidade no seletor
- **THEN** a aplicação passa a apresentar os locais da comunidade escolhida, e nenhum local de
  outra comunidade aparece na lista

#### Scenario: Comunidade sem local não é apresentada como falha

- **WHEN** a comunidade escolhida ainda não tem local algum cadastrado
- **THEN** a aplicação informa que a comunidade está sem locais, como informação, e não como
  aviso de erro

### Requirement: O Admin cadastra o local do território pela aplicação

A App 03 SHALL permitir ao **Admin** cadastrar local informando **nível**, **rótulo** e **local
pai**, dentro da comunidade escolhida. O nível SHALL ser escolhido entre os seis da hierarquia,
e o local pai SHALL ser escolhido **entre os locais já cadastrados** daquela comunidade — a
aplicação NEVER SHALL pedir que o Admin digite um identificador. O nível `comunidade` SHALL ser
o único que dispensa o pai.

A recusa do núcleo — pai de nível que não é o imediatamente acima, pai de outra comunidade, ou
nível fora dos seis — SHALL ser apresentada **em linguagem simples**, no campo que a originou,
e o caminho de cadastro NEVER SHALL ser oferecido a quem não é Admin. (`RF-02-16`, `RF-08-04`,
`RN-08-18`, documento 15 §6)

#### Scenario: Admin cadastra o local sob o pai escolhido

- **WHEN** um Admin em sessão informa nível `rua`, um rótulo e um local pai de nível `bairro`
  da mesma comunidade, e confirma
- **THEN** o local passa a existir e a aplicação o apresenta na hierarquia, sob aquele pai

#### Scenario: O nível `comunidade` é o único oferecido sem pai

- **WHEN** o Admin escolhe o nível `comunidade` no formulário
- **THEN** a aplicação não exige local pai; escolhido qualquer outro nível, ela o exige antes
  de deixar confirmar

#### Scenario: A recusa da hierarquia é apresentada no campo

- **WHEN** o núcleo recusa o cadastro por hierarquia inválida
- **THEN** a aplicação apresenta a recusa em linguagem simples, no campo que a originou, e
  nenhum local passa a existir

#### Scenario: Quem não é Admin não alcança o cadastro

- **WHEN** um Mestre em sessão abre a área Território
- **THEN** o caminho de cadastro de local não lhe é oferecido

### Requirement: A área Território alerta enquanto houver solicitação de local em aberto

A App 03 SHALL apresentar as **solicitações de novo local em aberto** da comunidade escolhida, e
SHALL **alertar enquanto houver ao menos uma sem desfecho**, para que a fila não fique
esquecida. Cada solicitação SHALL aparecer com **quem pediu**, o **nível pretendido**, o
**rótulo**, a **justificativa** e o **desafio de coleta de origem**.

O alerta SHALL desaparecer quando a última solicitação da comunidade receber desfecho, e a
solicitação já avaliada NEVER SHALL continuar na fila. A solicitação de local NEVER SHALL
aparecer na área Filas: ela não é uma das quatro naturezas daquela fila e não tem prazo de 7
dias. Quem pediu SHALL ser apresentado por **nick e avatar**, nunca por imagem real.
(`RF-02-21`, `RF-08-24`, `RN-02-22`, documento 99 §6 invariante 12)

#### Scenario: A fila alerta enquanto há solicitação sem desfecho

- **WHEN** o adulto abre a área Território de uma comunidade com solicitações em aberto
- **THEN** a aplicação alerta que há solicitação aguardando e apresenta cada uma com
  solicitante, nível pretendido, rótulo, justificativa e desafio de origem

#### Scenario: O alerta cessa quando a fila esvazia

- **WHEN** a última solicitação em aberto da comunidade recebe desfecho
- **THEN** o alerta deixa de aparecer e a fila é apresentada vazia

#### Scenario: A solicitação de local não aparece na área Filas

- **WHEN** o adulto abre a área Filas com solicitações de local em aberto
- **THEN** nenhuma delas aparece ali, e nenhuma é apresentada como em atraso

#### Scenario: O solicitante aparece por nick e avatar

- **WHEN** a fila apresenta uma solicitação
- **THEN** o Guerreiro(a) que a abriu aparece por nick e avatar, e nenhuma imagem real dele é
  exibida

### Requirement: O Admin aprova a solicitação informando o local pai, ou recusa com motivo

A App 03 SHALL permitir ao **Admin** dar o desfecho da solicitação de novo local em dois
caminhos: **aprovar**, informando o **local pai** escolhido entre os locais já cadastrados da
comunidade, o que **cria o local**; ou **recusar**, informando o **motivo**, sem criar local
algum. A aplicação NEVER SHALL deixar confirmar a recusa sem motivo.

A recusa do núcleo por hierarquia inválida SHALL ser apresentada em linguagem simples, e a
solicitação SHALL continuar na fila, em aberto. Solicitação já avaliada NEVER SHALL receber
segundo desfecho pela aplicação. Aprovada, o local criado SHALL aparecer na hierarquia da área
sem que o adulto precise recarregar a tela. (`RF-02-22`, `RF-08-23`, `RF-08-04`, `RN-08-18`)

#### Scenario: A aprovação cria o local e ele aparece na hierarquia

- **WHEN** um Admin aprova a solicitação informando o local pai
- **THEN** o local passa a existir, a solicitação sai da fila e o local aparece na hierarquia
  apresentada

#### Scenario: A recusa exige motivo

- **WHEN** o Admin tenta confirmar a recusa sem escrever o motivo
- **THEN** a aplicação aponta o motivo em falta e nenhum desfecho é registrado

#### Scenario: Recusa com motivo não cria local

- **WHEN** o Admin recusa a solicitação com motivo
- **THEN** a solicitação sai da fila como recusada e nenhum local passa a existir

#### Scenario: A hierarquia inválida devolve a solicitação à fila

- **WHEN** o núcleo recusa a aprovação por local pai de nível ou comunidade inválidos
- **THEN** a aplicação apresenta a recusa em linguagem simples e a solicitação continua na
  fila, em aberto

### Requirement: A área Território apresenta os desafios de coleta publicados, em leitura

A App 03 SHALL apresentar ao adulto em sessão os **desafios de coleta de trilha publicada**,
cada um com o **tipo de coleta**, a **cadência**, a **vigência** e a **quantidade de séries
ativas**. A apresentação SHALL ser **em leitura**: a aplicação NEVER SHALL oferecer caminho de
criar, editar ou apagar desafio de coleta, que é autoria do Mestre na App 09 (PRD-02 §3.2).

Desafio de trilha ainda em rascunho NEVER SHALL aparecer, e desafio sem série aberta SHALL
aparecer com zero séries ativas, como informação e não como falha. (`RF-02-17`, `RF-08-06`,
documento 15 §6)

#### Scenario: O adulto lê os desafios publicados com o que a fatia exige

- **WHEN** o adulto abre a área Território
- **THEN** a aplicação apresenta os desafios de coleta de trilha publicada, cada um com tipo,
  cadência, vigência e quantidade de séries ativas

#### Scenario: Desafio de trilha em rascunho não aparece

- **WHEN** há desafio de coleta numa missão de trilha ainda em rascunho
- **THEN** ele não aparece na lista

#### Scenario: A leitura não oferece escrita

- **WHEN** o adulto abre a lista dos desafios de coleta
- **THEN** nenhum caminho de criar, editar ou apagar desafio lhe é oferecido

#### Scenario: Desafio sem série não é apresentado como falha

- **WHEN** um desafio publicado ainda não tem série aberta
- **THEN** ele aparece com zero séries ativas, como informação, e não como aviso de erro

### Requirement: A lista de Guerreiros e Guerreiras mostra o vínculo, sem caminho de troca

A App 03 SHALL apresentar, na lista de Guerreiros e Guerreiras da área Personas, a **comunidade
do vínculo vigente** de cada um e a **data de início** desse vínculo, para que o Admin **confira**
o que a aula agendada atribuiu. A apresentação SHALL ser em **leitura**.

A aplicação NEVER SHALL oferecer caminho de mudar a comunidade do Guerreiro(a): no Ciclo 01 não
há transferência, e o histórico existe apenas no modelo. Guerreiro(a) ainda **sem vínculo
vigente** SHALL aparecer com a ausência informada em linguagem simples, e a lista NEVER SHALL
exibir imagem real de Guerreiro(a). (`RF-02-15`, `RN-02-06`, `RN-02-22`, `RF-08-02`, `RF-08-03`,
documento 99 §6 invariantes 4 e 12)

#### Scenario: A lista apresenta a comunidade herdada da aula

- **WHEN** o Admin abre a lista de Guerreiros e Guerreiras
- **THEN** cada um aparece com a comunidade do vínculo vigente e a data de início dele

#### Scenario: Não existe tela de transferência de comunidade

- **WHEN** o Admin procura, na lista ou na edição do Guerreiro(a), um caminho para mudar a
  comunidade dele
- **THEN** nenhum lhe é oferecido em lugar algum da aplicação

#### Scenario: Guerreiro(a) sem vínculo vigente é informado, não acusado

- **WHEN** a lista alcança um Guerreiro(a) sem vínculo vigente
- **THEN** a ausência aparece em linguagem simples, como informação, e não como aviso de erro

### Requirement: A App 03 abre a área Acervo sob a comunidade escolhida

A App 03 SHALL abrir a área **Acervo** com a escolha da comunidade, e SHALL apresentar os
exemplares permanentes ali tombados em **lista densa**, cada um com **título**, **número de
tombo**, **ponto de apoio**, **estado de conservação corrente** e o **responsável designado**
pelo acervo daquele ponto de apoio, com o **nome** e não com o identificador. O exemplar de
ponto de apoio ainda sem responsável SHALL aparecer assim mesmo, com a ausência apresentada como
informação e nunca como falha. A área NEVER SHALL apresentar valor em reais. Sem exemplar
tombado, a área SHALL dizê-lo em texto próprio, e NEVER SHALL apresentar lista vazia sem
explicação. (`RF-02-52`, `RF-02-53`, `RN-02-19`, PRD-02 §6.5)

#### Scenario: A área apresenta os exemplares da comunidade

- **WHEN** um Admin em sessão escolhe uma comunidade na área Acervo
- **THEN** vêm os exemplares tombados nos pontos de apoio daquela comunidade, cada um com
  título, número de tombo, ponto de apoio, estado de conservação e o nome do responsável

#### Scenario: Exemplar sem responsável designado aparece assim mesmo

- **WHEN** a lista traz exemplar de ponto de apoio ainda sem responsável pelo acervo
- **THEN** ele aparece, a ausência é apresentada como informação e nada é sinalizado como erro

#### Scenario: Comunidade sem acervo tem texto próprio

- **WHEN** a comunidade escolhida não tem exemplar tombado
- **THEN** a área diz que não há acervo tombado ali, sem apresentar lista vazia

#### Scenario: O Mestre lê o acervo das suas comunidades

- **WHEN** um Mestre em sessão abre a área Acervo
- **THEN** ele lê o acervo, e a recusa do núcleo às comunidades a que não está vinculado é
  apresentada em linguagem simples

### Requirement: O Admin tomba o exemplar permanente pela aplicação

A App 03 SHALL oferecer ao Admin o **tombamento** do exemplar permanente, informando **título**,
**número de tombo**, **ponto de apoio** e **estado de conservação**. A aplicação SHALL apontar o
campo em falta no próprio campo, sem enviar nada ao núcleo, e SHALL apresentar em linguagem
simples a recusa do núcleo ao **número de tombo já usado naquele ponto de apoio**, nunca como
código de erro cru. O caminho do tombamento NEVER SHALL ser oferecido a quem não é Admin.
(`RF-02-52`, `RN-02-21`, PRD-02 §6.5)

#### Scenario: Admin tomba um exemplar

- **WHEN** um Admin informa título, número de tombo, ponto de apoio e estado de conservação e
  confirma
- **THEN** o exemplar passa a existir e aparece na lista do acervo daquela comunidade

#### Scenario: Campo obrigatório em falta

- **WHEN** o Admin confirma o tombamento com um dos quatro campos vazio
- **THEN** a aplicação aponta o campo em falta e nada é enviado ao núcleo

#### Scenario: Tombo repetido é explicado

- **WHEN** o núcleo recusa o tombamento porque o número de tombo já existe naquele ponto de
  apoio
- **THEN** a aplicação diz isso em linguagem simples, e o que foi digitado permanece na tela

#### Scenario: Mestre não tomba

- **WHEN** um Mestre em sessão abre a área Acervo
- **THEN** o caminho do tombamento não lhe é oferecido

### Requirement: A ficha de vida do exemplar é lida na ordem do tempo

A App 03 SHALL apresentar, em cada exemplar, a sua **ficha de vida** completa, da anotação mais
antiga à mais recente, cada anotação com o **teor** — cuidado, perda ou dano —, o **estado de
conservação apurado**, **quem anotou** e **quando**. A aplicação NEVER SHALL oferecer caminho de
editar nem de remover anotação já gravada. Exemplar sem anotação SHALL dizê-lo em texto próprio.
(`RF-02-53`, `RN-02-21`, PRD-02 §6.5)

#### Scenario: A ficha vem completa e em ordem

- **WHEN** o Admin abre um exemplar com várias anotações
- **THEN** todas aparecem, da mais antiga à mais recente, com teor, estado de conservação, autor
  e data e hora

#### Scenario: Não há como editar nem apagar anotação

- **WHEN** a ficha de vida de um exemplar é apresentada
- **THEN** nenhuma anotação oferece caminho de edição ou de remoção

#### Scenario: Exemplar sem anotação

- **WHEN** o Admin abre um exemplar recém-tombado
- **THEN** a ficha diz que ainda não há anotação, sem apresentar lista vazia

### Requirement: A anotação de perda ou dano não cobra de ninguém

A App 03 SHALL oferecer ao **Admin** e ao **Mestre** a anotação na ficha de vida, com o **teor**
— cuidado, perda ou dano — e o **estado de conservação apurado**. A tela da anotação de **perda**
ou **dano** SHALL dizer que o fato não gera débito ao Guerreiro(a) nem à família, e NEVER SHALL
oferecer campo para identificar um Guerreiro(a) responsável pelo fato nem caminho algum de
cobrança. O caminho NEVER SHALL ser oferecido a Apoiador, Guerreiro(a) ou responsável.
(`RF-02-55`, `RN-02-14`, `RN-02-15`, `RN-02-16`, PRD-02 §7, documento 05 §3.6)

#### Scenario: Mestre anota o cuidado do exemplar

- **WHEN** um Mestre em sessão anota o cuidado de um exemplar com o estado de conservação
  apurado
- **THEN** a anotação passa a existir e aparece na ficha de vida, com o nome dele

#### Scenario: A perda não pede culpado

- **WHEN** o Admin escolhe o teor perda ou dano
- **THEN** a tela diz que nada é debitado ao Guerreiro(a) nem à família, e nenhum campo pede um
  Guerreiro(a) responsável pelo fato

#### Scenario: Estado de conservação em falta

- **WHEN** a anotação é confirmada sem o estado de conservação apurado
- **THEN** a aplicação aponta o campo em falta e nada é enviado ao núcleo

### Requirement: A área Acervo não oferece saída do exemplar

A área Acervo NEVER SHALL oferecer **retirada**, **empréstimo**, **devolução** nem
**transferência** de exemplar entre pontos de apoio: no Ciclo 01 o exemplar permanece onde foi
tombado. (`RN-02-18`, PRD-02 §3.2, documento 05 §3.2)

#### Scenario: Nenhum caminho tira o exemplar do lugar

- **WHEN** um Admin abre um exemplar na área Acervo
- **THEN** nenhuma ação de retirada, empréstimo, devolução ou transferência lhe é oferecida

### Requirement: A área Acervo mostra as entregas confirmadas pelo Mestre

A aplicação SHALL apresentar, na área **Acervo**, a leitura das entregas de recompensa de marco
já confirmadas pelo Mestre — entre elas o **exemplar da linha Alpha** e a **camisa** —, com o
Guerreiro(a), o **tipo de recurso** entregue, o **Mestre que entregou**, o ponto de apoio de onde
o recurso saiu e a data. A lista SHALL mostrar que a entrega deu **baixa definitiva** no
livro-razão, e NEVER SHALL exibir valor em moedas nem em reais. (`RF-02-50`, `RF-02-51`,
`RN-02-17`)

#### Scenario: A entrega do exemplar Alpha aparece com a baixa

- **WHEN** o Admin abre a lista de entregas na área Acervo
- **THEN** vê a entrega do exemplar Alpha com o Guerreiro(a), o Mestre que entregou, o ponto de
  apoio, a data e a baixa definitiva registrada

#### Scenario: A entrega da camisa aparece com o Guerreiro(a) inscrito

- **WHEN** o Admin abre a lista de entregas na área Acervo
- **THEN** vê a entrega da camisa ao Guerreiro(a) inscrito, com a mesma baixa definitiva

#### Scenario: A lista não mostra custo

- **WHEN** o Admin lê a lista de entregas
- **THEN** nenhum campo traz valor em moedas nem em reais

### Requirement: A gestão não confirma a entrega, apenas a mostra

A área Acervo SHALL apresentar as entregas em **leitura**, e NEVER SHALL oferecer à gestão o
caminho de confirmar, corrigir ou desfazer uma entrega: quem confirma é o Mestre que estava no
encontro. (`RF-02-50`, `RF-02-51`)

#### Scenario: Nenhuma tela da gestão confirma entrega

- **WHEN** o Admin percorre a área Acervo
- **THEN** encontra a lista de entregas em leitura e nenhum caminho para registrar entrega

### Requirement: O Admin designa o responsável pelo acervo do ponto de apoio

A App 03 SHALL oferecer ao Admin **designar e trocar** o responsável pelo acervo de um ponto de
apoio, escolhendo entre os **Mestres** e **Apoiadores** cadastrados, e a lista de pontos de apoio
SHALL passar a apresentar o **nome** do designado. A troca SHALL substituir o anterior. O caminho
NEVER SHALL ser oferecido a quem não é Admin, e a recusa do núcleo SHALL ser apresentada em
linguagem simples. (`RF-02-52`, `RF-07-49`, `RN-07-34`, PRD-02 §6.5)

#### Scenario: Admin designa um Mestre

- **WHEN** um Admin escolhe um Mestre como responsável pelo acervo de um ponto de apoio e
  confirma
- **THEN** a lista passa a apresentar o nome dele, e o acervo daquele ponto de apoio também

#### Scenario: A troca substitui o anterior

- **WHEN** o Admin designa outro responsável para ponto de apoio que já tinha um
- **THEN** a lista passa a apresentar o novo, e o anterior não aparece mais como designado

#### Scenario: Mestre não designa

- **WHEN** um Mestre em sessão abre a área Pontos de Apoio
- **THEN** o caminho da designação não lhe é oferecido

### Requirement: Toda tela que grava dado pessoal avisa o que ali se coleta

A aplicação SHALL exibir um **aviso discreto** do que está sendo coletado em toda tela em que a
gestão grava dado pessoal — o cadastro de Guerreiro(a), de Mestre, de Apoiador, de Admin e de
responsável; a conferência de presença; o lançamento do desfecho da atividade; o registro de
infração; o anexo da digitalização do termo; e a avaliação da solicitação de participação e da
solicitação de dados. Cada aviso SHALL nomear o dado daquela tela, na linha correspondente da
tabela do PRD-02 §11, e SHALL oferecer o acesso à área detalhada de direitos. O aviso NEVER
SHALL bloquear a tela, NEVER SHALL exigir confirmação para continuar e NEVER SHALL impedir o
envio do formulário. (`RF-02-64`, PRD-02 §11, documento 03 §12)

#### Scenario: A tela de cadastro traz o aviso

- **WHEN** o Admin abre o cadastro de Guerreiro(a)
- **THEN** um aviso discreto informa o que aquela tela coleta e dá acesso à área detalhada de
  direitos

#### Scenario: A tela de lançamento traz o aviso do dado dela

- **WHEN** o Admin abre o lançamento do desfecho da atividade ou o registro de infração
- **THEN** o aviso nomeia o dado daquela tela, e não o de outra

#### Scenario: O aviso não atrapalha o uso

- **WHEN** o aviso está exibido numa tela de cadastro ou de lançamento
- **THEN** a gestão preenche e envia o formulário sem confirmar o aviso, e nada na tela fica
  bloqueado por ele

### Requirement: A App 03 abre a área Direitos e dados, em leitura

A aplicação SHALL oferecer uma área **Direitos e dados**, alcançável pelo menu e por todo aviso
de coleta, que apresenta, para cada dado que a gestão coleta, a **finalidade**, a **base legal**,
o **prazo de retenção** e **quem acessa**, conforme a tabela do PRD-02 §11. A área SHALL
declarar também que a gestão não vê a imagem do Guerreiro(a), que o responsável exerce os
direitos pela App 07, que o registro de dado do território é **despersonalizado e não apagado**,
e que a infração fica restrita à gestão e ao responsável daquele Guerreiro(a). A área é de
**leitura**: NEVER SHALL oferecer escrita, exclusão ou exportação de dado. (`RF-02-64`,
PRD-02 §11)

#### Scenario: A área apresenta o destino de cada dado

- **WHEN** o Admin abre a área Direitos e dados
- **THEN** vê, para cada dado coletado, a finalidade, a base legal, o prazo de retenção e quem
  acessa

#### Scenario: O aviso leva à área

- **WHEN** a gestão aciona o acesso à área detalhada a partir do aviso de uma tela que coleta
- **THEN** chega à área Direitos e dados

#### Scenario: A área diz que o dado do território não se apaga

- **WHEN** o Admin lê a área Direitos e dados
- **THEN** encontra declarado que o registro de dado do território é despersonalizado, não
  apagado

### Requirement: Consentimento recusado não retira o Guerreiro(a) do lançamento

A aplicação NEVER SHALL usar a recusa ou a revogação de um consentimento para deixar um
Guerreiro(a) de fora do lançamento, da conferência de presença ou do registro de infração. A
lista dessas telas SHALL ser a do encontro inteiro, sem filtro por consentimento, e a aplicação
NEVER SHALL oferecer caminho que exclua alguém da atividade por causa da decisão do
responsável. (`RN-02-23`, PRD-01 `RN-01-21`, invariante 11 do documento 99 §6)

#### Scenario: Quem não tem autorização aparece no lançamento

- **WHEN** o Admin abre o lançamento de um encontro em que há Guerreiro(a) cujo responsável
  recusou a autorização
- **THEN** esse Guerreiro(a) aparece na lista como qualquer outro, e o desfecho dele é lançado
  normalmente

#### Scenario: A tela não oferece excluir por consentimento

- **WHEN** a gestão percorre o lançamento, a conferência de presença e o registro de infração
- **THEN** nenhuma delas oferece filtro, marcação ou ação que retire alguém por causa do
  consentimento

### Requirement: A autoria da trilha é do Mestre, e a gestão não oferece caminho para ela

A aplicação NEVER SHALL oferecer ao Admin cadastrar ou editar trilha, missão, conteúdo da
missão, atividade de missão, recompensa de marco ou desafio de coleta — a autoria é do Mestre,
na App 09. A área Atividades SHALL cadastrar **apenas atividade avulsa, fora de trilha**, e a
área Território SHALL apresentar os desafios de coleta publicados **em leitura**. Onde a
fronteira se confunde, a tela SHALL dizer, em uma linha, que aquilo se faz na App 09.
(`RN-02-24`, PRD-02 §§3.2, 4)

#### Scenario: A gestão não cadastra trilha nem missão

- **WHEN** o Admin percorre as áreas da App 03
- **THEN** não encontra caminho para criar ou editar trilha, missão, conteúdo, atividade de
  missão, recompensa de marco ou desafio de coleta

#### Scenario: A área Atividades diz o que cadastra e o que não cadastra

- **WHEN** o Admin abre a área Atividades
- **THEN** a tela cadastra atividade avulsa e diz, em uma linha, que a atividade de missão é
  autoria do Mestre, na App 09

#### Scenario: O desafio de coleta é só leitura

- **WHEN** o Admin abre os desafios de coleta publicados na área Território
- **THEN** os lê sem qualquer caminho de criação ou edição
