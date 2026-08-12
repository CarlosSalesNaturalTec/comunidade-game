## Purpose

A aula agendada é o que faz o App 01 existir num momento e num lugar: dela saem a comunidade do
cadastro novo e a habilitação do onboarding, e nela se registra quem esteve presente — por
reconhecimento na chegada ou por confirmação de quem estava na sala.

## ADDED Requirements

### Requirement: Aula é agendada com comunidade, data e horários

O núcleo SHALL manter a **aula** com **comunidade**, **data**, **horário inicial** e **horário
final**. Agendar aula SHALL ser operação de **Admin**; qualquer outro papel SHALL receber
**403**. Aula sem comunidade, sem data ou sem um dos horários SHALL ser recusada com **422**,
indicando o campo em falta, e aula cujo horário final não seja posterior ao inicial SHALL ser
recusada com **422**. (`RF-01-20`, `RF-01-16`, `RF-01-03`, PRD-01 §8)

#### Scenario: Admin agenda a aula

- **WHEN** um Admin agenda uma aula com comunidade, data, horário inicial e horário final
- **THEN** o núcleo grava a aula com a autoria de quem a agendou

#### Scenario: Mestre não agenda aula

- **WHEN** um Mestre tenta agendar uma aula
- **THEN** o núcleo responde 403 e nada é gravado

#### Scenario: Aula sem comunidade é recusada

- **WHEN** chega uma aula sem comunidade declarada
- **THEN** o núcleo responde 422 indicando o campo em falta e nada é gravado

#### Scenario: Horário final anterior ao inicial é recusado

- **WHEN** chega uma aula cujo horário final é anterior ou igual ao inicial
- **THEN** o núcleo responde 422 e nada é gravado

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
