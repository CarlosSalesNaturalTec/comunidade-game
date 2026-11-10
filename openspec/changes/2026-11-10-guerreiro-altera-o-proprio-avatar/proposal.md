# Proposal

**PRD de origem:** PRD-05 — Área do Guerreiro(a) (App 05). **Fatia 16** do bloco do PRD-05 no
`openspec/cronograma-de-fatias.md`, aberta nesta change por decisão do fundador de 2026-11-10.
**Atende:** `RF-05-51` e a rota `PATCH /v1/eu/avatar` da §9 do PRD-05; alcança `RF-05-50`,
`RN-05-15` e `RN-05-21`, e na App 01 o `RF-04-07`, sem mudar comportamento dela.

## Why

O `RF-05-51` manda o Guerreiro(a) **escolher e alterar** as características do próprio avatar, e
a §9 do PRD-05 declara a rota `PATCH /v1/eu/avatar` — nenhuma das duas existe. Hoje o avatar só
nasce no onboarding da App 01 e só muda pela edição do Admin na App 03 (`RF-02-01`): a criança
que quis outro cabelo, ou que cresceu, fica com o retrato que montou no primeiro encontro, e o
avatar é o **único retrato público** dela (documento 15 §7).

O pedido do fundador de 2026-11-10 trouxe também **regravar a facial** pela App 05. Ficou **fora
desta change**: contradiz o `RF-01-08` e a spec `template-biometrico`, que reservam o recadastro
ao Mestre ou Admin e recusam com 403 o próprio Guerreiro(a). Mudar isso é decisão nova e vira
pendência no documento 09 §1 (decisão do fundador de 2026-11-10).

## What Changes

- **Núcleo:** nasce `PATCH /v1/eu/avatar`, restrita ao Guerreiro(a) em sessão e sobre a própria
  persona; outro papel recebe 403. O núcleo segue tratando o avatar como **texto opaco**, como
  nas rotas do Apoiador e do Mestre. Sem migração.
- **Camada comum:** a montagem do avatar por camada do catálogo fechado, hoje dentro da
  `TelaDeCadastro` da App 01, **sobe a `comum/avatar`** como componente, e a App 01 passa a
  consumi-lo sem mudar comportamento.
- **App 05:** a carteira, onde a carta do Guerreiro(a) mora, ganha o caminho **"Mudar o meu
  avatar"**, que abre a montagem já com o avatar vigente, grava pela rota nova e devolve à
  carteira com a carta redesenhada. Todas as nove camadas, a qualquer tempo e sem limite de
  vezes (decisão do fundador de 2026-11-10). A **forma de tratamento** que viaja ao lado do
  objeto do documento 15 §7.2 é preservada, nunca apagada pela troca.
- **Documentação:** a linha da fatia 16 no cronograma e a pendência nova da regravação da
  facial pelo próprio Guerreiro(a) no documento 09 §1.

## Capabilities

### New Capabilities

Nenhuma.

### Modified Capabilities

- `persona-e-credencial`: o Guerreiro(a) em sessão altera o próprio avatar pela rota do PRD-05,
  que a spec já anuncia e não descreve.
- `camada-visual-comum`: a camada comum passa a entregar a montagem do avatar por camada, que
  hoje é só da App 01.
- `area-do-guerreiro`: a App 05 oferece ao Guerreiro(a) a alteração do próprio avatar, a partir
  da carteira, preservando a forma de tratamento.

## Impact

- `backend/src/nucleo/personas/` — regra e rota novas; testes em `backend/tests/`.
- `comum/avatar/` — componente de montagem e seus testes.
- `apps/app-01-aula-presencial/src/onboarding/TelaDeCadastro.tsx` — passa a consumir o
  componente comum; os testes do onboarding seguem sem edição de asserção.
- `apps/app-05-guerreiro/src/carteira/` e `src/api/` — tela de montagem, cliente da rota e testes.
- `openspec/cronograma-de-fatias.md` e `docs/09-topicos-em-aberto-e-sugestoes.md` §1.
- Fora do escopo: o cadastro do Guerreiro(a) e a captura da imagem, que o PRD-05 §3.2 deixa no
  onboarding da App 01, e a regravação da facial pelo próprio Guerreiro(a), pela decisão de
  2026-11-10.
