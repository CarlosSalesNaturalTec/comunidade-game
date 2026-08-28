# aula-e-presenca Specification

## Purpose
A aula agendada é o que faz o App 01 existir num momento e num lugar: dela saem a comunidade do
cadastro novo e a habilitação do onboarding, e nela se registra quem esteve presente — por
reconhecimento na chegada ou por confirmação de quem estava na sala.
## Requirements
### Requirement: Aula é agendada com comunidade, data e horários

O núcleo SHALL manter a **aula** com **comunidade**, **ponto de apoio**, **data**, **horário
inicial**, **horário final**, os **recursos que ela consome** e a **situação**. Agendar aula
SHALL ser operação de **Admin**; qualquer outro papel SHALL receber **403**. Aula sem
comunidade, **sem ponto de apoio**, sem data ou sem um dos horários SHALL ser recusada com
**422**, indicando o campo em falta, e aula cujo horário final não seja posterior ao inicial
SHALL ser recusada com **422**.

O **ponto de apoio** declarado SHALL pertencer à **mesma comunidade** da aula; aula cujo ponto de
apoio seja de outra comunidade SHALL ser recusada com **422**. É o ponto de apoio que liga a
aula ao saldo de recursos guardado naquele espaço.

O ponto de apoio declarado SHALL estar **ativo**; aula que declare ponto de apoio **inativo**
SHALL ser recusada com **422**. Espaço que saiu de operação não recebe aula nova, e aula já
agendada antes da desativação NEVER SHALL perder o vínculo com ele — a desativação é bloqueada
justamente enquanto houver aula futura ali.

Os **recursos que a aula consome** SHALL ser declarados no agendamento, como pares de tipo de
recurso e quantidade, e NÃO SHALL ser derivados da atividade prevista. A lista SHALL poder ser
vazia — aula que não consome recurso algum é agendada e nasce **confirmada**. Quantidade menor
ou igual a zero, ou tipo de recurso inexistente, SHALL ser recusada com **422**.

O agendamento SHALL ser exposto em rota de **Admin**, e é ele que dispara a reserva.
(`RF-01-20`, `RF-01-71`, `RF-01-16`, `RF-01-03`, `RF-07-08`, `RF-07-47`, `RF-02-31`,
`RN-07-33`, `RN-07-01`, invariante 4 do documento 99 §6, PRD-01 §8, documento 04 §1,
documento 05 §2)

#### Scenario: Admin agenda a aula

- **WHEN** um Admin agenda uma aula com comunidade, ponto de apoio, data, horário inicial e
  horário final
- **THEN** o núcleo grava a aula com a autoria de quem a agendou

#### Scenario: Mestre não agenda aula

- **WHEN** um Mestre tenta agendar uma aula
- **THEN** o núcleo responde 403 e nada é gravado

#### Scenario: Aula sem comunidade é recusada

- **WHEN** chega uma aula sem comunidade declarada
- **THEN** o núcleo responde 422 indicando o campo em falta e nada é gravado

#### Scenario: Aula sem ponto de apoio é recusada

- **WHEN** chega uma aula sem ponto de apoio declarado
- **THEN** o núcleo responde 422 indicando o campo em falta e nada é gravado

#### Scenario: Ponto de apoio de outra comunidade é recusado

- **WHEN** chega uma aula cujo ponto de apoio pertence a comunidade diferente da comunidade da
  aula
- **THEN** o núcleo responde 422 e nada é gravado

#### Scenario: Ponto de apoio inativo é recusado

- **WHEN** chega uma aula cujo ponto de apoio está inativo
- **THEN** o núcleo responde 422 e nenhuma aula passa a existir

#### Scenario: Horário final anterior ao inicial é recusado

- **WHEN** chega uma aula cujo horário final é anterior ou igual ao inicial
- **THEN** o núcleo responde 422 e nada é gravado

#### Scenario: Aula com recurso de quantidade zero é recusada

- **WHEN** chega uma aula declarando um recurso com quantidade zero ou negativa
- **THEN** o núcleo responde 422 indicando o campo e nada é gravado

#### Scenario: Aula sem recursos declarados nasce confirmada

- **WHEN** um Admin agenda uma aula sem declarar recurso algum
- **THEN** o núcleo grava a aula na situação confirmada, sem reserva alguma

### Requirement: O agendamento reserva, e a falta de saldo deixa a aula pendente de lastro

O núcleo SHALL avaliar, no agendamento, a **quantidade disponível** de cada tipo de recurso
declarado no ponto de apoio da aula. Havendo disponível para **todos** os recursos declarados,
o núcleo SHALL reservar cada quantidade e gravar a aula na situação **confirmada**. Faltando
disponível para **qualquer** parcela, o núcleo SHALL gravar a aula na situação **pendente de
lastro** e NÃO SHALL reservar quantidade alguma — nem a dos tipos que tinham saldo. A aula
pendente de lastro SHALL ser agendada assim mesmo, não recusada. (`RF-07-08`, `RN-07-01`,
`RF-02-31`, `RF-02-32`, invariante 9 do documento 99 §6, PRD-07 §5.3)

#### Scenario: Saldo suficiente confirma a aula

- **WHEN** um Admin agenda uma aula cujos recursos declarados têm todos disponível bastante
- **THEN** o núcleo reserva cada quantidade e grava a aula como confirmada

#### Scenario: Falta em um tipo deixa a aula pendente de lastro

- **WHEN** um Admin agenda uma aula com dois recursos declarados e apenas um deles tem
  disponível bastante
- **THEN** o núcleo grava a aula como pendente de lastro e não reserva nenhum dos dois

#### Scenario: Aula pendente de lastro não é recusada

- **WHEN** um Admin agenda uma aula sem disponível para o que ela consome
- **THEN** o núcleo grava a aula e responde com sucesso, indicando o que falta

### Requirement: A situação da aula tem cinco valores e o desfecho não se repete

O núcleo SHALL manter a **situação** da aula entre exatamente cinco valores: **prevista**,
**pendente de lastro**, **confirmada**, **realizada** e **cancelada**. A aula SHALL passar a
**realizada** pelo lançamento da atividade e a **cancelada** por ato de cancelamento. Aula já
**realizada** ou já **cancelada** SHALL recusar com **422** tanto um novo lançamento quanto um
novo cancelamento: o desfecho é único. (`RF-01-72`, `RF-07-09`, PRD-01 §8)

#### Scenario: Lançamento leva a aula a realizada

- **WHEN** a atividade realizada é lançada numa aula confirmada
- **THEN** a aula passa à situação realizada

#### Scenario: Aula realizada recusa novo lançamento

- **WHEN** chega um segundo lançamento de atividade para uma aula já realizada
- **THEN** o núcleo responde 422 e nada muda

#### Scenario: Aula cancelada recusa lançamento

- **WHEN** chega o lançamento de atividade de uma aula já cancelada
- **THEN** o núcleo responde 422 e nada muda

### Requirement: O cancelamento é de Admin ou de Mestre da comunidade da aula

O núcleo SHALL aceitar o cancelamento de aula agendada de um **Admin** ou de um **Mestre
vinculado à comunidade da aula**, sempre com **motivo** registrado. Mestre de outra comunidade
SHALL receber **403**, e qualquer outro papel SHALL receber **403**. Cancelamento sem motivo
SHALL ser recusado com **422**. O cancelamento SHALL **liberar** todas as reservas da aula,
devolvendo as quantidades à disponível, e SHALL ser gravado com autoria, data e hora. Esta é a
única escrita de gestão do Mestre, pela exceção do `RF-01-17`. (`RF-01-72`, `RF-01-17`,
`RF-02-95`, `RF-07-09`, `RF-01-03`, documento 05 §4)

#### Scenario: Mestre da comunidade cancela a aula

- **WHEN** um Mestre vinculado à comunidade da aula a cancela com motivo
- **THEN** o núcleo grava o cancelamento com a autoria dele e libera as reservas da aula

#### Scenario: Mestre de outra comunidade é recusado

- **WHEN** um Mestre não vinculado à comunidade da aula tenta cancelá-la
- **THEN** o núcleo responde 403 e nada é gravado

#### Scenario: Cancelamento sem motivo é recusado

- **WHEN** chega um cancelamento de aula sem motivo declarado
- **THEN** o núcleo responde 422 e nada é gravado

#### Scenario: Guerreiro(a) não cancela aula

- **WHEN** um Guerreiro(a) tenta cancelar uma aula
- **THEN** o núcleo responde 403 e nada é gravado

### Requirement: A gestão lê a agenda, filtrada por comunidade e por período

O núcleo SHALL devolver as aulas com **comunidade**, **ponto de apoio**, **data**, **horário
inicial**, **horário final**, **situação** e, quando cancelada, o **motivo do cancelamento**. A
leitura SHALL ser paginada e SHALL aceitar filtro por **comunidade** e por **período**.

A leitura SHALL exigir persona de gestão em sessão: o **Admin** SHALL ler todas as comunidades e
o **Mestre**, apenas as comunidades a que está vinculado. **Apoiador**, **Guerreiro(a)** e
**responsável** SHALL receber **403**.

A aula **pendente de lastro** SHALL sair com a situação que a distingue da confirmada, sem que a
leitura altere situação alguma. (`RF-02-12`, `RF-01-28`, `RF-01-18`, `RF-01-16`, `RN-02-09`,
PRD-02 §9)

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

### Requirement: A disponibilidade do App 01 é derivada da aula vigente no momento

O núcleo SHALL derivar as **aulas vigentes** como aquelas cuja data e cuja faixa entre o horário
inicial e o final **contêm o momento corrente**, sem nenhum parâmetro de liberação separado.
Havendo aulas vigentes em comunidades diferentes no mesmo momento, o núcleo SHALL devolver
**todas** — a escolha é da aplicação que abre, nunca do Guerreiro(a). Não havendo aula vigente, o
núcleo SHALL devolver conjunto vazio. (`RF-01-32`, `RF-01-18`, documento 09, "Comunidade do
onboarding")

#### Scenario: Aula em curso é devolvida como vigente

- **WHEN** o momento corrente está entre o horário inicial e o final de uma aula daquela data
- **THEN** o núcleo devolve aquela aula entre as vigentes

#### Scenario: Aula fora do horário não é vigente

- **WHEN** o momento corrente é anterior ao horário inicial ou posterior ao final da aula
- **THEN** o núcleo não devolve aquela aula entre as vigentes

#### Scenario: Duas comunidades no mesmo horário devolvem duas aulas

- **WHEN** duas aulas de comunidades diferentes estão vigentes no mesmo momento
- **THEN** o núcleo devolve as duas, sem escolher uma delas

#### Scenario: Sem aula agendada não há operação

- **WHEN** nenhuma aula está vigente no momento corrente
- **THEN** o núcleo devolve conjunto vazio

### Requirement: As aulas vigentes são lidas pela aplicação que abre, sem persona em sessão

O núcleo SHALL expor as **aulas vigentes** — as já derivadas pela capacidade, sem parâmetro de
liberação separado — em rota que exige **chave de aplicação** e NEVER SHALL exigir credencial de
persona: a consulta acontece antes de qualquer pessoa se identificar. A saída SHALL trazer, de
cada aula vigente, ao menos a **comunidade**, para que a aplicação que abre saiba em qual está
operando.

Não havendo aula vigente, o núcleo SHALL responder **200 com conjunto vazio** — é o que faz o
App 01 não abrir, e NEVER SHALL ser tratado como erro. (`RF-02-14`, `RF-02-13`, `RF-01-32`,
`RF-01-02`, `RN-02-05`, PRD-02 §§9, 12)

#### Scenario: Aplicação sem persona lê as vigentes

- **WHEN** uma aplicação com chave válida e sem nenhuma persona em sessão consulta as aulas
  vigentes
- **THEN** o núcleo responde com as aulas vigentes daquele momento

#### Scenario: Fora de qualquer janela a lista volta vazia

- **WHEN** o momento corrente não está dentro da janela de nenhuma aula agendada
- **THEN** o núcleo responde 200 com conjunto vazio, e não um erro

#### Scenario: Duas comunidades no mesmo horário chegam ambas a quem abre

- **WHEN** duas aulas de comunidades diferentes estão vigentes no mesmo momento
- **THEN** as duas saem na consulta, cada uma com a sua comunidade, sem que o núcleo escolha

#### Scenario: Consulta sem chave é recusada

- **WHEN** a consulta das aulas vigentes chega sem chave de aplicação válida
- **THEN** o núcleo recusa a chamada, como em qualquer rota de dados

### Requirement: Presença registra o modo de comprovação e quem confirmou

O núcleo SHALL registrar a **presença** de um Guerreiro(a) numa aula com o **modo de
comprovação** — **reconhecimento** do próprio Guerreiro(a) ou **confirmação** de Mestre ou Admin
— e, no modo confirmação, **quem confirmou**. Presença por confirmação sem o registro de quem
confirmou SHALL ser recusada com **422**. Presença de Guerreiro(a) em aula de comunidade
diferente da dele SHALL ser recusada com **422**. (`RF-01-20`, `RF-01-03`, `RN-01-05`, documento
09, "App 01 com a rede fora")

#### Scenario: Presença por reconhecimento dispensa confirmador

- **WHEN** o Guerreiro(a) é reconhecido na chegada e a presença é registrada
- **THEN** o núcleo grava a presença com modo "reconhecimento" e sem confirmador

#### Scenario: Presença por confirmação grava quem confirmou

- **WHEN** um Mestre confirma pelo nick a presença de um Guerreiro(a) na aula
- **THEN** o núcleo grava a presença com modo "confirmação" e o Mestre como confirmador

#### Scenario: Confirmação sem confirmador é recusada

- **WHEN** chega uma presença com modo "confirmação" e sem quem confirmou
- **THEN** o núcleo responde 422 indicando o campo em falta e nada é gravado

#### Scenario: Presença em comunidade alheia é recusada

- **WHEN** chega a presença de um Guerreiro(a) numa aula de outra comunidade
- **THEN** o núcleo responde 422 e nada é gravado

### Requirement: A presença registrada por engano é anulada, sem apagar o registro

O núcleo SHALL oferecer ao **Admin** a **anulação** de uma presença já registrada — o caso do
reconhecimento que apontou a pessoa errada —, guardando **motivo**, **autor** e **momento da
anulação**. A anulação NEVER SHALL apagar o registro: a presença anulada permanece consultável
com o modo, o confirmador e o momento do fato originais, e é assim que o ajuste manual do
`RF-02-36` fica registrado, como manda a `RN-02-12`.

Anulação sem motivo SHALL ser recusada com **422**. Anulação de presença já anulada SHALL ser
recusada com **409**. Quem não é Admin SHALL receber **403** — o Mestre confirma presença, não
a desfaz. A presença anulada NEVER SHALL contar como presença: ela sai do painel do dia e não
alcança o lançamento da atividade realizada. (`RF-02-36`, `RF-01-20`, `RN-02-12`, `RN-02-21`,
documento 03 §5)

#### Scenario: O Admin anula a presença registrada por engano

- **WHEN** um Admin anula, com motivo, a presença de um Guerreiro(a) reconhecido por engano
- **THEN** o núcleo grava a anulação com motivo, autor e momento, e a presença permanece
  consultável com o modo e o momento do fato originais

#### Scenario: Anulação sem motivo é recusada

- **WHEN** chega uma anulação sem motivo, ou com motivo em branco
- **THEN** o núcleo responde 422 indicando o campo em falta e nada é gravado

#### Scenario: A mesma presença não se anula duas vezes

- **WHEN** chega a anulação de uma presença já anulada
- **THEN** o núcleo responde 409 e a anulação original permanece como está

#### Scenario: O Mestre não anula presença

- **WHEN** um Mestre em sessão tenta anular a presença de um Guerreiro(a)
- **THEN** o núcleo responde 403 e nada é gravado

#### Scenario: A presença anulada sai do painel do dia

- **WHEN** o painel do dia é lido depois de uma presença daquela aula ter sido anulada
- **THEN** o Guerreiro(a) não aparece entre quem chegou

### Requirement: A presença é única por aula e Guerreiro(a)

O núcleo SHALL manter **no máximo uma** presença **não anulada** por aula e Guerreiro(a). O
reenvio da mesma presença — o caso do App 01 que operou com a rede fora e sincroniza depois —
SHALL deixar o registro existente inalterado, sem duplicar e sem erro. Anulada a presença
daquele par, o núcleo SHALL aceitar o **registro correto** da presença do mesmo Guerreiro(a)
naquela aula, sem que a anulada seja tocada: é o que fecha o ajuste manual do `RF-02-36`.
(`RF-01-20`, `RF-02-36`, PRD-01 §10, documento 09, "App 01 com a rede fora")

#### Scenario: Reenvio da mesma presença não duplica

- **WHEN** a presença de um Guerreiro(a) já registrada naquela aula é enviada de novo
- **THEN** o núcleo mantém um único registro e não responde erro

#### Scenario: Sincronização depois da rede voltar preserva o primeiro registro

- **WHEN** uma presença confirmada na fila local chega depois de a mesma presença já ter sido
  gravada
- **THEN** o núcleo mantém o registro existente, com o confirmador e o momento originais

#### Scenario: Anulada a presença, a correta é registrada

- **WHEN** a presença de um Guerreiro(a) numa aula é anulada e, em seguida, a presença correta
  dele naquela mesma aula é registrada por confirmação
- **THEN** o núcleo grava a presença nova e a anulada permanece gravada, sem ser alterada

### Requirement: A App 01 registra a presença por reconhecimento sob a sessão de trabalho

O núcleo SHALL aceitar o registro de presença no modo **reconhecimento** quando a chave de
aplicação declarar a **App 01** e quem estiver em sessão for o **Mestre ou o Admin da sessão de
trabalho do aparelho**. A presença assim gravada SHALL ficar **sem confirmador**: a sessão de
trabalho autentica a escrita e NEVER SHALL constar como quem confirmou, pela mesma distinção que
o autocadastro do encontro já observa. O Guerreiro(a) NEVER SHALL ganhar operação de escrita de
presença na matriz de permissões — a presença é fato do encontro, não ato dele.

A mesma rota SHALL continuar aceitando o modo **confirmação** pela App 01, gravando quem
confirmou. Permanecem valendo, sem alteração, a unicidade por aula e Guerreiro(a) e a recusa de
presença em comunidade alheia. (`RF-04-18`, `RF-04-21`, `RF-01-20`, `RF-01-03`, PRD-04 §9,
documento 09, 2026-08-24)

#### Scenario: A entrada por reconhecimento grava a presença sem confirmador

- **WHEN** a App 01, na sessão de trabalho do aparelho, registra a presença de um Guerreiro(a)
  reconhecido na chegada
- **THEN** o núcleo grava a presença com modo reconhecimento e sem confirmador

#### Scenario: A confirmação humana pela App 01 grava quem confirmou

- **WHEN** a App 01 registra, no modo confirmação, a presença de um Guerreiro(a) cuja
  identificação falhou
- **THEN** o núcleo grava a presença com modo confirmação e o adulto da sessão de trabalho como
  confirmador

#### Scenario: A sessão de trabalho não vira autora da presença

- **WHEN** se lê uma presença gravada por reconhecimento pela App 01
- **THEN** ela não aponta confirmador algum, ainda que a escrita tenha sido autenticada por um
  Mestre ou Admin

#### Scenario: O Guerreiro(a) não alcança a rota por conta própria

- **WHEN** um Guerreiro(a) em sessão tenta registrar a própria presença
- **THEN** o núcleo recusa, porque nenhuma operação de presença lhe é concedida na matriz

### Requirement: A presença já registrada é devolvida, e é a aplicação que avisa

O núcleo SHALL responder ao reenvio da presença de um par aula e Guerreiro(a) já registrado
**devolvendo o registro existente**, sem duplicar, sem alterá-lo e **sem erro** — tanto para a
criança que volta à porta no mesmo encontro quanto para o reenvio da fila local. O núcleo NEVER
SHALL distinguir os dois casos por código de resposta: a resposta SHALL permitir que o cliente
reconheça o registro anterior pelo **momento do fato** já gravado.

Avisar a criança de que a presença dela já constava é comportamento da **aplicação**, não do
núcleo. (`RF-04-19`, `RF-01-20`, PRD-01 §10, PRD-04 §§5.4, 9, documento 09, 2026-08-24)

#### Scenario: A criança que volta à porta no mesmo encontro

- **WHEN** chega a presença de um Guerreiro(a) que já a tem naquela aula
- **THEN** o núcleo devolve o registro existente, com o modo e o momento do fato originais, e
  nada é gravado

#### Scenario: O momento do fato original é preservado

- **WHEN** o reenvio traz um momento do fato diferente do gravado
- **THEN** o núcleo mantém o momento original e o devolve, sem sobrescrevê-lo

### Requirement: O Mestre lê as suas turmas, separadas pelo formato da atividade

O núcleo SHALL servir ao **Mestre em sessão** as aulas das comunidades a que ele é vinculado e
as atividades **de que ele é autor**, e nada além: turma de outra comunidade e atividade de
outro Mestre NEVER SHALL aparecer na leitura (`RN-09-08`).

A leitura SHALL separar as atividades pelo **formato** — **presencial** do encontro e
**on-line** entre encontros —, para que o Mestre distinga o que conduz na sala do que corre
entre os encontros. Em cada atividade presencial, a leitura SHALL trazer a **aula que ela
declarou**, quando houver: é como o Mestre confere a programação que montou e reconhece a
atividade que ainda não foi vinculada a encontro algum. Atividade sem aula declarada SHALL
aparecer na mesma lista, com o vínculo em branco.

A leitura exige a operação **suas turmas** da matriz de permissões: papel sem ela SHALL receber
**403**. (`RF-09-42`, `RF-09-73`, `RN-09-08`, `RF-01-16`, documento 05 §4)

#### Scenario: O Mestre vê as próprias turmas e atividades

- **WHEN** o Mestre em sessão lê as suas turmas
- **THEN** o núcleo devolve as aulas das comunidades dele com as atividades de que ele é autor

#### Scenario: Atividade de outro Mestre não aparece

- **WHEN** existe atividade autorada por outro Mestre numa aula da mesma comunidade
- **THEN** ela não aparece na leitura das turmas do Mestre em sessão

#### Scenario: As atividades saem separadas por formato

- **WHEN** a turma do Mestre tem atividades presenciais e on-line
- **THEN** a saída distingue as presenciais das on-line pelo formato de cada atividade

#### Scenario: A atividade presencial sai com a aula que declarou

- **WHEN** o Mestre lê as suas turmas e uma atividade presencial dele declarou uma aula
- **THEN** a saída traz aquela aula junto da atividade

#### Scenario: Atividade ainda sem encontro sai com o vínculo em branco

- **WHEN** o Mestre lê as suas turmas e uma atividade presencial dele não declarou aula alguma
- **THEN** ela aparece na lista com o vínculo em branco

#### Scenario: Papel sem a operação é recusado

- **WHEN** uma persona cujo papel não tem a operação de suas turmas pede a leitura
- **THEN** o núcleo responde 403 e nada é devolvido

### Requirement: O Mestre registra presença apenas por confirmação

O núcleo SHALL aceitar do **Mestre** o registro de presença de um Guerreiro(a) na aula
**somente no modo confirmação**, gravando-o como quem confirmou. O modo **reconhecimento** é da
**App 01**, e a recusa SHALL ser decidida pela **aplicação declarada na chave**, não pela rota
inteira nem pelo papel de quem está em sessão: chegando o modo reconhecimento por qualquer
aplicação que não seja a App 01, a tentativa SHALL receber **403**.

A distinção pela chave é o que permite ao mesmo Mestre registrar presença por confirmação na
App 09 e, na App 01, autenticar a presença por reconhecimento da criança reconhecida na porta —
sem que nenhuma das duas aplicações alcance o que é da outra.

O recorte é o que concilia o `RF-09-45`, que dá a presença ao Mestre, com o PRD-01 §4, que não
a lista entre as escritas de gestão dele (`RF-01-17`): o Mestre a alcança pela **confirmação de
identidade do Guerreiro(a)**, operação que a matriz já lhe concede, e não por escrita de gestão
nova.

Permanecem valendo, sem alteração, a unicidade por aula e Guerreiro(a) e a recusa de presença
em comunidade alheia. (`RF-09-45`, `RF-01-20`, `RF-01-17`, `RF-01-03`, `RF-04-18`)

#### Scenario: O Mestre confirma a presença que faltou

- **WHEN** o Mestre registra, no modo confirmação, a presença de um Guerreiro(a) da comunidade
  dele numa aula
- **THEN** o núcleo grava a presença com modo confirmação e o Mestre como confirmador

#### Scenario: O Mestre não registra presença por reconhecimento

- **WHEN** o Mestre tenta registrar presença no modo reconhecimento por uma chave que não é a
  da App 01
- **THEN** o núcleo responde 403 e nada é gravado

#### Scenario: O reenvio da mesma presença não duplica

- **WHEN** o Mestre confirma novamente a presença de um Guerreiro(a) que já a tem naquela aula
- **THEN** o núcleo devolve a presença já gravada, sem duplicar e sem erro

