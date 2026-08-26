# solicitacao-de-local Specification

## Purpose

TBD - created by archiving change solicitacao-de-local. Update Purpose after archive.

## Requirements

### Requirement: A solicitação de local nasce presa à comunidade do Guerreiro(a) e a um desafio

O núcleo SHALL registrar a solicitação de novo local com **solicitante**, **comunidade**,
**desafio de origem**, **nível pretendido**, **rótulo**, **justificativa**, **situação**,
**avaliador** e **motivo da recusa**. Solicitar SHALL ser ato do **Guerreiro(a)**; persona de
qualquer outro papel SHALL receber **403**. A comunidade da solicitação SHALL ser a
**comunidade vigente do solicitante**, e a solicitação apontada para outra comunidade SHALL ser
recusada com **403**. O nível pretendido SHALL ser um dos seis níveis da hierarquia, e o rótulo
e a justificativa SHALL ser exigidos. (`RF-08-22`, `RN-08-02`, `RN-08-18`, PRD-08 §§5.3, 8)

#### Scenario: Guerreiro(a) solicita local faltante na própria comunidade

- **WHEN** um Guerreiro(a) solicita a inclusão de um local para um desafio de coleta,
  informando nível, rótulo e justificativa
- **THEN** o núcleo grava a solicitação na situação **recebida**, com a comunidade vigente do
  solicitante e o desafio de origem

#### Scenario: Solicitação para comunidade que não é a do solicitante é recusada

- **WHEN** um Guerreiro(a) solicita local apontando comunidade diferente da sua comunidade
  vigente
- **THEN** o núcleo recusa com **403**, e nenhuma solicitação é gravada

#### Scenario: Persona que não é Guerreiro(a) não solicita local

- **WHEN** um Mestre, um Admin, um responsável ou um Apoiador tenta solicitar novo local
- **THEN** o núcleo recusa com **403**, e nenhuma solicitação é gravada

#### Scenario: Solicitação sem rótulo ou sem justificativa é recusada

- **WHEN** a solicitação chega sem rótulo, sem justificativa ou com nível fora dos seis da
  hierarquia
- **THEN** o núcleo recusa com **422**, indicando o campo em falta

### Requirement: O pedido não cria local, em nenhuma situação

O núcleo SHALL gravar a solicitação **sem criar local**, e o envio SHALL devolver apenas o
registro da solicitação e a sua situação. O local SHALL nascer **somente** do cadastro direto
por Admin ou da **aprovação** da solicitação. A série de coleta que depende do local pedido
SHALL continuar impedida de abrir enquanto a solicitação não for aprovada. (`RN-08-18`,
`RF-08-07`, PRD-08 §§5.3, 12)

#### Scenario: Envio da solicitação não cria local

- **WHEN** um Guerreiro(a) envia a solicitação de novo local
- **THEN** o núcleo devolve a solicitação registrada, e **nenhum local** passa a existir na
  hierarquia da comunidade

#### Scenario: Série não abre no local ainda pedido

- **WHEN** o Guerreiro(a) tenta abrir série apontando um local que só existe como solicitação
  em aberto
- **THEN** o núcleo recusa a abertura, porque o local não existe

### Requirement: Avalia o Admin ou o Mestre autor da trilha do desafio de origem

O núcleo SHALL permitir a avaliação da solicitação por um **Admin** ou pelo **Mestre autor da
trilha** do desafio de origem, alcançada pelo desafio até a missão e desta até a trilha. Mestre
que não é o autor daquela trilha SHALL receber **403**, ainda que o papel dele permita escrever
trilhas em geral. Guerreiro(a), responsável e Apoiador SHALL receber **403**. O desfecho SHALL
gravar **quem avaliou** e **quando**. (`RF-08-23`, `RN-08-18`, PRD-08 §§5.3, 9)

#### Scenario: Mestre autor da trilha avalia a solicitação

- **WHEN** o Mestre autor da trilha do desafio de origem avalia a solicitação
- **THEN** o núcleo aceita a avaliação e grava o avaliador e a data e hora do desfecho

#### Scenario: Admin avalia qualquer solicitação

- **WHEN** um Admin avalia a solicitação, seja qual for a trilha do desafio de origem
- **THEN** o núcleo aceita a avaliação e grava o avaliador e a data e hora do desfecho

#### Scenario: Mestre de outra trilha é recusado

- **WHEN** um Mestre que não é o autor da trilha do desafio de origem tenta avaliar
- **THEN** o núcleo recusa com **403**, e a solicitação continua em aberto

#### Scenario: Guerreiro(a) não avalia a própria solicitação

- **WHEN** o Guerreiro(a) solicitante tenta aprovar a própria solicitação
- **THEN** o núcleo recusa com **403**

### Requirement: A aprovação cria o local, e a recusa exige motivo

O núcleo SHALL criar o local ao aprovar a solicitação, com o **nível pretendido** e o **rótulo**
da solicitação, na **comunidade** dela, e com o **local pai informado pelo avaliador no ato da
avaliação**. O local criado SHALL obedecer às mesmas regras de hierarquia do local cadastrado
diretamente por Admin — pai do **nível imediatamente acima**, da **mesma comunidade**, e apenas
o nível `comunidade` sem pai. Hierarquia inválida SHALL ser recusada com **422**, e a
solicitação SHALL permanecer em aberto, sem desfecho gravado. A recusa SHALL exigir **motivo**;
recusa sem motivo SHALL ser recusada com **422**. (`RF-08-23`, `RF-08-04`, `RN-08-18`,
PRD-08 §§8, 12)

#### Scenario: Aprovação cria o local e libera a abertura da série

- **WHEN** o Mestre autor da trilha aprova a solicitação informando o local pai
- **THEN** o núcleo cria o local na hierarquia da comunidade, grava a situação **aprovada** com
  o avaliador e a data, e a série passa a poder abrir naquele local

#### Scenario: Recusa devolve o motivo e não cria local

- **WHEN** o avaliador recusa a solicitação com motivo
- **THEN** o núcleo grava a situação **recusada** com o motivo, o avaliador e a data, e
  **nenhum local** é criado

#### Scenario: Recusa sem motivo é recusada

- **WHEN** o avaliador recusa a solicitação sem informar motivo
- **THEN** o núcleo recusa com **422**, e a solicitação continua em aberto

#### Scenario: Pai de nível ou comunidade inválidos não consome a solicitação

- **WHEN** o avaliador aprova informando local pai de nível que não é o imediatamente acima, de
  outra comunidade ou inexistente
- **THEN** o núcleo recusa com **422**, nenhum local é criado, e a solicitação continua em
  aberto, sem avaliador nem data de desfecho gravados

### Requirement: A solicitação avaliada não se reavalia

O núcleo SHALL aceitar **um único desfecho** por solicitação. Solicitação já aprovada ou já
recusada SHALL recusar nova avaliação com **422**, e o desfecho gravado — situação, avaliador,
data e motivo — NEVER SHALL ser alterado. (`RF-08-23`, PRD-08 §8)

#### Scenario: Segunda avaliação da mesma solicitação é recusada

- **WHEN** um avaliador tenta avaliar solicitação que já está aprovada ou recusada
- **THEN** o núcleo recusa com **422**, e o desfecho gravado permanece como estava

#### Scenario: Aprovação não cria um segundo local

- **WHEN** a mesma solicitação aprovada recebe nova tentativa de aprovação
- **THEN** o núcleo recusa com **422**, e nenhum segundo local é criado

### Requirement: A lista de solicitações em aberto alimenta o alerta, com o recorte de cada papel

O núcleo SHALL devolver as solicitações **em aberto**, para que as Apps 03 e 09 mostrem o alerta
enquanto houver alguma sem desfecho. A consulta SHALL exigir o **filtro por comunidade**, como
toda consulta de dado de comunidade, e SHALL ser recusada com **422** quando ele faltar. O
**Admin** SHALL ver todas as solicitações em aberto da comunidade filtrada, de qualquer trilha e
de qualquer Mestre; o **Mestre** SHALL ver apenas as dos desafios das **suas** trilhas naquela
comunidade. Solicitação já avaliada NEVER SHALL aparecer na lista. Persona de outro papel SHALL
receber **403**. (`RF-08-24`, `RF-08-23`, `RF-01-18`, PRD-08 §9)

#### Scenario: Admin vê todas as solicitações em aberto da comunidade filtrada

- **WHEN** um Admin consulta as solicitações em aberto com o filtro de uma comunidade
- **THEN** o núcleo devolve todas as solicitações em aberto daquela comunidade, inclusive as de
  trilhas de outros Mestres

#### Scenario: Mestre vê só as das suas trilhas

- **WHEN** um Mestre consulta as solicitações em aberto com o filtro de uma comunidade em que há
  solicitações de trilhas dele e de trilhas de outro Mestre
- **THEN** o núcleo devolve apenas as dos desafios das trilhas dele

#### Scenario: Consulta sem o filtro de comunidade é recusada

- **WHEN** a consulta de solicitações em aberto chega sem o filtro de comunidade
- **THEN** o núcleo responde **422**, indicando o campo em falta

#### Scenario: Solicitação avaliada sai da lista

- **WHEN** uma solicitação em aberto é aprovada ou recusada e a lista é consultada em seguida
- **THEN** ela não aparece mais entre as em aberto

### Requirement: A solicitação de local não herda o ciclo da fila única de avaliação

O núcleo SHALL tratar a solicitação de local **fora** da fila única de avaliação das quatro
naturezas, porque a aprovação dela **cria cadastro** — o que aquela fila proíbe em toda
situação — e porque o avaliador pode ser o Mestre da trilha, e não só um Admin. A solicitação de
local NEVER SHALL receber o **prazo de 7 dias** das quatro naturezas, e NEVER SHALL ser
identificada como em atraso: enquanto não tem desfecho, ela está **em aberto**. (`RF-08-24`,
`RN-08-18`)

#### Scenario: Solicitação de local não recebe prazo

- **WHEN** um Guerreiro(a) registra a solicitação de novo local
- **THEN** o núcleo grava a situação recebida **sem prazo de resposta**, e a solicitação nunca é
  marcada como em atraso, por mais tempo que passe

#### Scenario: A fila das quatro naturezas não devolve solicitação de local

- **WHEN** a fila única de avaliação é consultada
- **THEN** as solicitações de local não aparecem nela, porque não são uma das suas quatro
  naturezas

### Requirement: O Guerreiro(a) acompanha as próprias solicitações de local

O núcleo SHALL devolver ao **Guerreiro(a) em sessão** as solicitações de local que **ele
mesmo** abriu, em qualquer situação — `recebida`, `aprovada` ou `recusada` —, cada uma com o
**rótulo pretendido**, o **nível pretendido**, a **justificativa**, o **desafio de coleta** de
origem e a **situação**. A solicitação **recusada** SHALL sair com o **motivo** que o avaliador
declarou; a **aprovada** SHALL sair com o **local que a aprovação criou**, para que a criança
o encontre na hora de abrir a série. (`RF-05-32`, `RN-05-11`, PRD-05 §§5.4, 6.4)

A consulta NEVER SHALL devolver solicitação de outro solicitante, e SHALL recusar com **403**
a persona de outro papel — Admin e Mestre acompanham pela listagem das solicitações em aberto,
que é outra porta e outro recorte. A consulta SHALL ser paginada como toda listagem do núcleo
e NEVER SHALL exigir o filtro de comunidade: a sessão do Guerreiro(a) já recorta mais estreito
que ele. (`RN-05-21`, `RF-01-28`)

#### Scenario: O Guerreiro(a) vê as próprias solicitações em qualquer situação

- **WHEN** um Guerreiro(a) em sessão consulta as suas solicitações de local
- **THEN** o núcleo devolve as que ele abriu, recebidas, aprovadas e recusadas, cada uma com
  rótulo, nível pretendido, justificativa, desafio de origem e situação

#### Scenario: A recusa exibe o motivo

- **WHEN** a lista inclui uma solicitação recusada
- **THEN** ela sai com a situação `recusada` e com o motivo que o avaliador declarou

#### Scenario: A aprovação aponta o local criado

- **WHEN** a lista inclui uma solicitação aprovada
- **THEN** ela sai com a situação `aprovada` e com o local que a aprovação criou

#### Scenario: A consulta não alcança solicitação de outro Guerreiro(a)

- **WHEN** um Guerreiro(a) consulta as suas solicitações e há solicitações de outros
  Guerreiros e Guerreiras da mesma comunidade
- **THEN** o núcleo devolve apenas as do Guerreiro(a) da sessão

#### Scenario: Outro papel não lê pela porta do Guerreiro(a)

- **WHEN** um Mestre ou um Admin chama a consulta das próprias solicitações do Guerreiro(a)
- **THEN** o núcleo responde 403
