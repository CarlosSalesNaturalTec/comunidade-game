## ADDED Requirements

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
