# Proposal

**PRD-07, fatia 11** do `openspec/cronograma-de-fatias.md` — finalidade do tipo de recurso.
Atende `RF-07-53`, `RF-07-01`, `RF-07-51`, `RN-07-41` (PRD-07 v12), `RF-02-31`, `RF-02-107`,
`RF-02-113` (PRD-02 v13), `RF-09-71` e `RF-09-84` (PRD-09 v8). Decisão do fundador de
2026-11-20, linha "Consumo do encontro e recompensa de marco" do documento 09.

## Why

Nas aulas de 2026-11-07 e 2026-11-14 o kit que era recompensa de marco foi declarado na aula: a
aula reservou o saldo inteiro, cada entrega debitou de novo, e a aula seguinte ficou pendente de
lastro com falta de 17 kits. Nada no núcleo distingue o que a aula consome do que sai na entrega
de uma recompensa. Esta fatia cria essa distinção; é o piso das fatias 12 a 14.

## What Changes

- O tipo de recurso não durável ganha a **finalidade** — consumo do encontro ou recompensa —,
  declarada no cadastro e corrigível pelo Admin; o durável não tem finalidade (`RF-07-53`,
  `RF-07-01`, `RF-07-51`, `RN-07-41`).
- A aula aceita declarar só tipo de **consumo do encontro**; a recompensa de marco, o item do
  catálogo avulso e a recompensa do desafio extra aceitam só tipo de **recompensa** — escolha
  nova de tipo da finalidade errada é recusada com 422 (`RF-07-53`, `RF-02-31`, `RF-09-71`,
  `RF-09-84`).
- A leitura do catálogo traz a finalidade (`RF-07-01`).
- **Migração:** os tipos não duráveis já cadastrados recebem **recompensa**; o Admin corrige para
  consumo do encontro os que forem, depois da implantação (decisão do fundador de 2026-11-20). O
  que já foi gravado com o tipo — aula, reserva, recompensa, item, desafio — segue intacto: a
  trava vale só para escolha nova, como a do tipo desativado (`RF-07-52`).
- App 03: o catálogo cadastra, lista e corrige a finalidade (`RF-02-107`, `RF-02-113`), e o
  seletor de recursos da aula oferece só consumo do encontro (`RF-02-31`).
- App 09: o seletor da recompensa de marco oferece só recompensa (`RF-09-71`, `RF-09-84`).

## Capabilities

### New Capabilities

Nenhuma.

### Modified Capabilities

- `catalogo-de-tipos-de-recurso`: finalidade no cadastro, na correção e na leitura; migração dos
  tipos existentes.
- `aula-e-presenca`: a aula declara só tipo de consumo do encontro.
- `recompensa-de-marco`: a declaração aceita só tipo de recompensa.
- `catalogo-avulso`: o item aceita só tipo de recompensa.
- `desafio-extra`: a recompensa aceita só tipo de recompensa.
- `aplicacao-de-gestao`: finalidade no catálogo da App 03 e seletor da aula filtrado.
- `area-do-mestre`: seletor da recompensa de marco da App 09 filtrado.

## Impact

- Núcleo: `recursos` (modelo, regra, rotas), `aulas`, `recompensas_de_marco`, `catalogo_avulso`,
  `desafios_extras`; uma migração Alembic.
- App 03: `catalogos/TelaDeCatalogos.tsx`, `agenda/FormularioDeAgendamento.tsx`.
- App 09: `trilhas/DeclaracaoDeRecompensa.tsx`.
- Fora do escopo (fatias 12 a 14 do PRD-07): baixa no fim da aula e fim do fechamento, entrega
  pelo disponível e pela aprovação do prático, e necessidade da recompensa de marco. As telas da
  App 08 que informam o tipo pelo identificador não ganham seletor; a recusa do núcleo as cobre.
