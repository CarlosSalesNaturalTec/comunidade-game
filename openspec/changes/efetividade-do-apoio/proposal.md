## Why

O Apoiador que propõe desafio extra e aporta recurso não tem hoje nenhuma tela que responda
_"o que esse apoio produziu"_: a App 08 mostra o estado da proposta (fatia 1) e o que foi
aportado (fatia 4), nunca o que aconteceu por causa disso. A **fatia 6 do PRD-14** —
`openspec/cronograma-de-fatias.md`, bloco do PRD-14 — entrega o painel vivo de efetividade,
que fecha o ciclo entre o apoio e o resultado dele sem abrir um só dado de criança.

PRD de origem: **PRD-14 — Área do Apoiador (App 08)**.
Recorte da fatia: `RF-14-40` a `RF-14-47`, `RN-14-21`, `RN-14-22`, `RN-14-28`.
Depende das fatias 1 (`DesafioExtra`) e 5 (moedas, missões e selos), ambas implementadas.

## What Changes

- Nasce o **registro da conclusão** de um `DesafioExtra` por um Guerreiro(a) — a entidade que o
  painel lê para saber quantos concluíram, em que trilha e em que período. Nesta fatia ela é
  **só de leitura**: o ato de registrar a conclusão e atribuir a recompensa é do PRD-09 e
  entra com a fatia que o cronograma lhe der (decisão do fundador, 2026-09-02). O mesmo
  desenho da fatia 1, que criou as situações do `DesafioExtra` deixando as transições para
  fora dela.
- A **quantidade restante** do desafio publicado passa a descontar as conclusões registradas,
  em vez de repetir sempre a quantidade disponível (`RF-14-37`).
- Nasce a rota `GET /v1/eu/desafios-extras/efetividade` (PRD-14 §9), restrita ao Apoiador em
  sessão, com o painel agregado: desafios propostos, publicados e concluídos; concluintes por
  desafio, com trilha e período; moedas aportadas e o que custearam; cobertura de ODS herdada
  das missões, agregada por comunidade e ciclo (`RF-14-40` a `RF-14-44`).
- O painel identifica concluinte **apenas por avatar e nick**, e só com divulgação autorizada
  vigente; sem ela, a conclusão entra somente na contagem agregada (`RF-14-45`, `RF-14-46`,
  `RN-14-22`). No direcionado, o proponente vê **que houve conclusão e nada além disso**
  (`RF-14-47`).
- O painel é **vivo**: a leitura reflete a última conclusão registrada, sem fechamento nem
  periodicidade, e nenhuma rota devolve relatório fechado (`RF-14-40`, `RN-14-21`).
- A cobertura de ODS sai **descritiva e agregada**, nunca como mérito do apoio nem por
  Guerreiro(a) (`RN-14-28`).
- A App 08 ganha a área **Efetividade**, que consome a rota nova.

Fora do escopo, como o PRD-14 §3.2 já exclui: relatório fechado de prestação de contas,
qualquer canal de mensagem com Guerreiro(a), família ou Mestre, e ranking de apoiadores por
valor. Também ficam de fora, por não serem desta fatia: o ato de registrar a conclusão e
atribuir a recompensa (PRD-09), a baixa da reserva na entrega (`RF-07-39`, `RF-07-40`, fatia 15
do PRD-02) e os favoritos (`RF-14-48` a `RF-14-55`, fatia 7).

## Capabilities

### New Capabilities

- `efetividade-do-apoio`: o painel vivo do Apoiador — o que agrega, com que recorte e sob que
  salvaguardas de identificação (`RF-14-40` a `RF-14-47`, `RN-14-21`, `RN-14-22`, `RN-14-28`).

### Modified Capabilities

- `desafio-extra`: passa a registrar a **conclusão** de um desafio por um Guerreiro(a), e a
  quantidade restante do publicado passa a descontá-la (`RF-14-37`, `RF-14-42`).
- `area-do-apoiador`: a App 08 ganha a tela de efetividade, com as salvaguardas de leitura que
  ela precisa exibir (`RF-14-40` a `RF-14-47`).

## Impact

- **Backend** (`backend/src/nucleo/`): entidade nova de conclusão em `desafios_extras/`, com
  migração Alembic; leitura da efetividade em módulo próprio; rota nova sob `/v1`. Lê
  `consentimentos.regra.autorizacao_de_divulgacao_vigente`, `ods.regra` (cobertura e etiquetas
  da missão), `aportes.modelo.Aporte` e `poder_sustentador.regra` — nenhum deles é alterado.
- **App 08** (`apps/app-08-apoiador/`): área e tela novas, com o cliente da rota.
- **API**: um `GET` novo; nenhum contrato existente muda de forma. A leitura de
  `GET /v1/eu/desafios-extras` muda de **valor** no campo `quantidade_restante`, que passa a
  descontar conclusões — o campo já existe e o formato não muda.
- **Documentação**: a linha da fatia 6 no `openspec/cronograma-de-fatias.md`. Nenhuma decisão
  de produto nova, logo nada muda em `docs/`.
