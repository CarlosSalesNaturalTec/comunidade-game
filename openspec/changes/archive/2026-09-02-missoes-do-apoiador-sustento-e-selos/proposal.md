## Why

Fatia 5 do **PRD-14 — Área do Apoiador**, no `openspec/cronograma-de-fatias.md`. Atende
`RF-14-60` a `RF-14-73` e `RN-14-29` a `RN-14-38`, mais a opção "missão aberta" do `RF-14-02`
que a fatia 2 deixou de fora por faltar a entidade, e `RF-02-102` a `RF-02-105` e `RN-02-31`
do PRD-02 — a publicação da missão pela gestão.

Hoje o Apoiador tem aporte, necessidade e Poder Sustentador (fatia 4), mas nada que o convide
a cobrir uma frente e nada que reconheça quem cobriu: a progressão dele em moedas, selos e
níveis de sustento (`RN-14-29`) não existe ainda. Quem publica a `MissaoDoApoiador` era a trava
anotada na fatia; o fundador decidiu em 2026-09-01 que é a gestão, por ato de Admin na App 03,
e a decisão foi gravada no documento 14 §§5 e 11 antes desta proposta.

## What Changes

- Entidade `MissaoDoApoiador` no núcleo, com o nível de necessidade, o que se pede, o prazo, o
  selo que rende e a necessidade de recurso de origem (`RN-14-31`). O **quanto falta** é
  derivado dos aportes homologados daquela necessidade, nunca armazenado.
- Entidade `SeloDoApoiador`, somente inserção, creditada no ato da homologação que conclui a
  missão (`RF-14-66`, `RN-14-33`).
- **Nível de sustento derivado** dos níveis de necessidade das missões concluídas, que só
  cresce (`RF-14-67`, `RF-14-69`, `RN-14-35`, `RN-14-36`).
- Publicação, listagem e despublicação da missão na App 03, por Admin (`RF-02-102` a
  `RF-02-105`, `RN-02-31`).
- Rota pública das missões abertas, agrupadas por nível de necessidade, com o coberto em
  quantidade e sem identificar quem cobriu (`RF-14-60` a `RF-14-62`, `RF-14-71`, `RF-14-72`).
- Declaração de aporte a partir de uma missão: a origem `missao` que a fatia 4 deixou anotada
  como futura, com abatimento e conclusão só na homologação (`RF-14-63` a `RF-14-65`,
  `RN-14-32`, `RN-14-34`).
- Telas de **Missões**, **sustento** e **selos** na App 08, e a opção "missão aberta" na porta
  pública de pré-cadastro (`RF-14-02`, `RF-14-68`, `RF-14-70`, `RF-14-73`).

Fora do escopo, como o PRD-14 §3.2 já exclui: o **catálogo de missões instanciado para o
Ciclo 01** — a aplicação exibe o que a gestão publicar, não define missão —, o **ranking de
apoiadores por valor**, o relatório fechado de prestação de contas, a notificação por e-mail e
qualquer canal de mensagem. A fila da gestão separada por modalidade (documento 14 §11) também
não entra: não há requisito de PRD para ela.

## Capabilities

### New Capabilities

- `missao-do-apoiador`: a missão publicada pela gestão a partir de uma necessidade, o que ela
  pede e o que falta, a cobertura parcial e coletiva, o vencimento e a conclusão por
  homologação.
- `selo-e-nivel-de-sustento`: o selo creditado na conclusão, as quatro famílias, o nível de
  sustento derivado das frentes cobertas e a garantia de que nenhum dos dois regride.

### Modified Capabilities

- `area-do-apoiador`: as telas de missões, sustento e selos na App 08, e a opção "missão
  aberta" na porta pública.
- `aplicacao-de-gestao`: a publicação, a listagem e a despublicação da missão pelo Admin.
- `aporte`: a declaração de aporte com origem `missao` e a homologação que, além de creditar
  moedas, conclui a missão e credita os selos.

## Impact

- `backend/src/nucleo/missoes_do_apoiador/` (novo), `backend/src/nucleo/selos_do_apoiador/`
  (novo), `backend/src/nucleo/aportes/` (origem `missao` e gancho da homologação), migração
  Alembic com as duas tabelas.
- `apps/app-08-apoiador/src/missoes/` e `.../sustento/` (novos), `.../preCadastro/`
  (opção "missão aberta").
- `apps/app-03-gestao/src/missoes-do-apoiador/` (novo).
- Rotas: `POST`, `GET` e `POST .../despublicacao` em `/v1/missoes-do-apoiador` (Admin), `GET`
  público de `/v1/missoes-do-apoiador` e `GET /v1/eu/apoiador/sustento` (Apoiador).
- Documentação já ajustada nesta change: documento 14 §§5 e 11, documento 09, PRD-02 (§§3.1,
  6.5, 7, 8, 9, 13, 15), PRD-14 §9, documento 99 §8 e o cronograma.
