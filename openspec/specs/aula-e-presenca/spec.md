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

Os **recursos que a aula consome** SHALL ser declarados no agendamento, como pares de tipo de
recurso e quantidade, e NÃO SHALL ser derivados da atividade prevista. A lista SHALL poder ser
vazia — aula que não consome recurso algum é agendada e nasce **confirmada**. Quantidade menor
ou igual a zero, ou tipo de recurso inexistente, SHALL ser recusada com **422**.

O agendamento SHALL ser exposto em rota de **Admin**, e é ele que dispara a reserva.
(`RF-01-20`, `RF-01-71`, `RF-01-16`, `RF-01-03`, `RF-07-08`, `RF-02-31`, `RN-07-33`,
`RN-07-01`, invariante 4 do documento 99 §6, PRD-01 §8, documento 04 §1, documento 05 §2)

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

### Requirement: A presença é única por aula e Guerreiro(a)

O núcleo SHALL manter **no máximo uma** presença por aula e Guerreiro(a). O reenvio da mesma
presença — o caso do App 01 que operou com a rede fora e sincroniza depois — SHALL deixar o
registro existente inalterado, sem duplicar e sem erro. (`RF-01-20`, PRD-01 §10, documento 09,
"App 01 com a rede fora")

#### Scenario: Reenvio da mesma presença não duplica

- **WHEN** a presença de um Guerreiro(a) já registrada naquela aula é enviada de novo
- **THEN** o núcleo mantém um único registro e não responde erro

#### Scenario: Sincronização depois da rede voltar preserva o primeiro registro

- **WHEN** uma presença confirmada na fila local chega depois de a mesma presença já ter sido
  gravada
- **THEN** o núcleo mantém o registro existente, com o confirmador e o momento originais

