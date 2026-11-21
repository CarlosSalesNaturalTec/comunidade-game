# Proposal

**PRD-07, fatia 14** do `openspec/cronograma-de-fatias.md` — necessidade da recompensa de
marco, a última das quatro da decisão "Consumo do encontro e recompensa de marco" do documento
09. Atende `RF-07-54`, `RF-07-18`, `RF-07-27`, `RF-07-28` (PRD-07), `RF-09-56`, `RF-09-57`
(PRD-09), `RF-02-58`, `RF-02-102` (PRD-02), `RF-14-24`, `RF-14-25`, `RF-14-02` (PRD-14) e
`RF-03-47` (PRD-03). Depende da fatia 13, implementada.

Decisões do fundador de 2026-11-21, tomadas ao abrir a fatia e gravadas no documento 04 §1 e na
linha da decisão no documento 09: o disponível de um tipo num ponto de apoio é contado pelas
trilhas em **ordem fixa** — a de atividade em aula da comunidade mais antiga primeiro —; conta
a atividade em **qualquer aula não cancelada** da comunidade; **comunidade sem aula anterior
não gera necessidade** de recompensa; e a **declaração do Apoiador** por necessidade aceita
também a nova espécie, o que acrescentou `RF-14-25` e `RF-14-02` ao recorte.

## Why

Desde a fatia 11 a recompensa de marco não passa pela aula: ela não reserva e sai do saldo na
entrega. A falta dela, então, não aparece em lugar nenhum — a necessidade só nasce de aula
pendente de lastro —, e o kit que vai faltar na próxima aprovação não vira pedido ao Apoiador,
nem missão, nem absorção do Mestre.

## What Changes

- **Segunda espécie de necessidade** (`RF-07-54`, `RF-07-18`): por comunidade, ponto de apoio,
  tipo e trilha — Guerreiros(as) com vínculo vigente na comunidade que ainda não receberam cada
  recompensa da trilha, vezes a quantidade dela, menos o disponível no ponto de apoio da aula
  imediatamente anterior da comunidade. Contam as trilhas com atividade em aula não cancelada da
  comunidade.
- As rotas `GET /vitrine/necessidades` e `GET /necessidades/minhas` passam a servir as duas
  espécies (`RF-07-27`, `RF-03-47`, `RF-09-56`). Cada item ganha `especie`, `trilha_id` e
  `trilha_nome`; **BREAKING:** `aula_id`, `inicio_em` e `fim_em` passam a nulos na necessidade
  da recompensa.
- **Absorção** (`RF-07-28`, `RF-09-57`), **missão do Apoiador** (`RF-02-102`) e **declaração
  por necessidade** (`RF-14-25`) aceitam a necessidade da recompensa, declarando comunidade e
  trilha no lugar da aula.
- Telas: a lista de necessidades da App 03, da App 08, da vitrine e da App 09 mostra a trilha no
  lugar da data da aula (`RF-02-58`, `RF-14-24`, `RF-03-47`, `RF-09-56`); a publicação da missão
  na App 03, a absorção na App 09 e a declaração e o pré-cadastro na App 08 aceitam a nova
  espécie (`RF-14-02`).
- Documento 04 §1 e documento 09: as três regras de contagem decididas ao abrir a fatia.

## Capabilities

### New Capabilities

Nenhuma.

### Modified Capabilities

- `necessidade-de-recurso`: segunda espécie, ordem de contagem entre trilhas, identificação e
  campos publicados; absorção que declara comunidade e trilha.
- `aporte`: absorção e declaração do Apoiador apontam a necessidade da recompensa.
- `missao-do-apoiador`: a missão nasce também da necessidade da recompensa.
- `aplicacao-de-gestao`: lista de necessidades e publicação da missão com a nova espécie.
- `area-do-apoiador`: lista, declaração e pré-cadastro com a nova espécie.
- `aplicacao-da-vitrine`: a vitrine publica a necessidade da recompensa com a trilha.
- `area-do-mestre`: lista de necessidades e absorção com a nova espécie.

## Impact

- Núcleo: `necessidades` (regra e rotas), `aportes` (modelo, regra e rotas),
  `missoes_do_apoiador` (modelo, regra e rotas); migração Alembic que acrescenta
  `comunidade_virtual_id` e `trilha_id` a `aporte`, `aporte_declarado` e `missao_do_apoiador`
  e torna `missao_do_apoiador.aula_id` anulável.
- App 03: `recursos/ListaDeNecessidades.tsx`, `recursos/TelaDeRecursos.tsx`,
  `missoes-do-apoiador/PublicacaoDeMissao.tsx`.
- App 06: `necessidades/ListaDeNecessidades.tsx` (a porta do convite a reaproveita).
- App 08: `aportes/TelaDeNecessidadesEmAberto.tsx`, `aportes/TelaDeDeclaracaoDeAporte.tsx`,
  `preCadastro/TelaDePreCadastro.tsx`.
- App 09: `recursos/ListaDeNecessidades.tsx`, `recursos/AbsorcaoDaNecessidade.tsx`.
- Documentos 04 §1 e 09; cronograma ao fechar.
- Fora do escopo, como o PRD-07 §3.2 e o cronograma registram: conferência de inventário
  (`RF-07-20`), desafio extra, empréstimo de bancada e reposição solidária.
