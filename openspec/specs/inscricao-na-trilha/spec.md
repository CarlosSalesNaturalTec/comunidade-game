# inscricao-na-trilha Specification

## Purpose

A inscrição na trilha é o que põe o Guerreiro(a) no percurso — ato dele, nunca lançamento de
terceiro. É o vínculo que faltava para o nível 1 ter as duas condições que o documento 11 §6
exige, e é ela que responde "quais são as minhas trilhas".

## Requirements

### Requirement: O Guerreiro(a) inscreve-se na trilha publicada

O núcleo SHALL registrar a **inscrição** de um Guerreiro(a) numa trilha, com o momento do ato.
A inscrição SHALL ser ato do **próprio Guerreiro(a) em sessão** — nenhuma outra persona a grava
por ele. A trilha SHALL estar **publicada**: inscrição em trilha em rascunho ou despublicada
SHALL ser recusada com **422**. O núcleo SHALL admitir **várias trilhas ao mesmo tempo**, sem
teto, e **uma única inscrição por Guerreiro(a) e trilha** — inscrever-se de novo na mesma
trilha SHALL devolver a inscrição existente, sem criar vínculo novo e sem erro.
(`RF-05-09`, `RN-05-43`)

#### Scenario: Inscrição em trilha publicada é gravada

- **WHEN** o Guerreiro(a) em sessão inscreve-se numa trilha publicada
- **THEN** o núcleo grava a inscrição com o momento do ato, vinculada a ele e àquela trilha

#### Scenario: Inscrição em trilha em rascunho é recusada

- **WHEN** o Guerreiro(a) tenta inscrever-se numa trilha em rascunho ou despublicada
- **THEN** o núcleo responde 422 e nada é gravado

#### Scenario: Segunda inscrição na mesma trilha não cria vínculo novo

- **WHEN** o Guerreiro(a) já inscrito inscreve-se de novo na mesma trilha
- **THEN** o núcleo devolve a inscrição que já existe, sem gravar uma segunda

#### Scenario: Várias trilhas ao mesmo tempo

- **WHEN** o Guerreiro(a) já inscrito numa trilha inscreve-se em outra trilha publicada
- **THEN** o núcleo grava a segunda inscrição, e as duas permanecem vigentes

#### Scenario: Ninguém inscreve o Guerreiro(a) em lugar dele

- **WHEN** uma persona que não é o Guerreiro(a) da inscrição tenta gravá-la
- **THEN** o núcleo responde 403 e nada é gravado

### Requirement: A inscrição não se desfaz e não obriga a concluir

O núcleo NEVER SHALL expor forma de desfazer uma inscrição: ela é **fato com data**, não
máquina de estados. Concluir a trilha NEVER SHALL ser obrigatório — o Guerreiro(a) que para no
meio SHALL manter a evolução limitada às etapas realizadas, e o nível já certificado SHALL
permanecer. (`RN-05-44`)

#### Scenario: Não há desinscrição

- **WHEN** se procura no núcleo uma forma de remover ou cancelar uma inscrição gravada
- **THEN** nenhuma existe, e a inscrição permanece

#### Scenario: Parar no meio não derruba o que foi conquistado

- **WHEN** um Guerreiro(a) inscrito deixa de avançar na trilha
- **THEN** a inscrição permanece e o nível já certificado naquela trilha não regride

### Requirement: O Guerreiro(a) lê as próprias trilhas e nunca as de terceiro

O núcleo SHALL servir ao Guerreiro(a) em sessão as trilhas em que ele está **inscrito**, cada
uma com a **próxima missão** do percurso dele. A leitura SHALL alcançar **apenas as próprias
inscrições**: inscrição de outro Guerreiro(a) NEVER SHALL ser servida por esta leitura.
(`RF-05-08`, `RF-05-17`, `RN-05-21`)

#### Scenario: A lista traz as trilhas inscritas com a próxima missão

- **WHEN** o Guerreiro(a) em sessão lê as próprias trilhas
- **THEN** o núcleo devolve cada trilha em que ele está inscrito, com a próxima missão do
  percurso dele em cada uma

#### Scenario: Inscrição de terceiro não sai

- **WHEN** o Guerreiro(a) em sessão lê as próprias trilhas
- **THEN** nenhuma inscrição de outro Guerreiro(a) aparece na resposta

#### Scenario: Sem inscrição, a lista sai vazia

- **WHEN** um Guerreiro(a) sem nenhuma inscrição lê as próprias trilhas
- **THEN** o núcleo devolve lista vazia, sem erro
