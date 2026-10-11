# Proposal

**PRD de origem:** PRD-02 — Frontend de gestão (App 03).
**Fatia:** 25 do bloco do PRD-02 em `openspec/cronograma-de-fatias.md`.
**Identificadores atendidos:** `RF-02-112`, `RN-02-32`, `RN-02-33` (novos), `RF-02-29`
(alterado), alcançando `RF-02-33` e `RF-02-34`.

A revisão do PRD-02 que cria esses identificadores está no **mesmo PR**, no commit `21b64dc`
deste branch — decisão do fundador de 2026-10-11. A fatia não depende de PR algum.

## Why

A atividade avulsa é hoje **cadastro sem destino**: o Admin a grava na área Atividades da
App 03 e, a partir dali, nenhuma tela lança o resultado dela. O seletor de atividade da área
Lançamentos vem de `atividades_previstas`, que exige missão e portanto a exclui; nenhum app a
apresenta a quem a realizaria. Resultado: `RF-02-29` está entregue pela metade — a avulsa
existe no banco, não rende ponto a ninguém e não serve ao encontro.

As quatro decisões do fundador de 2026-10-11 (documento 09 §1) fecham o caminho: a avulsa
declara a aula, e o Admin lança o resultado por aluno ou por equipe da aula.

## What Changes

- **Cadastro da avulsa passa a exigir a aula** do encontro (`RF-02-29` alterado). A
  **comunidade** é passo do formulário, que estreita a lista de aulas, e **não** dado gravado —
  a aula já a declara. O **formato fica fixo em presencial**: a regra vigente da capacidade
  `atividade-de-trilha` recusa com 422 a atividade on-line que declare aula.
- **`GET /v1/atividades` ganha filtro por aula.** A rota já existe e já é restrita a Admin; é
  por ela que a App 03 monta a lista da avulsa, sem passar pela programação do encontro.
- **`POST /v1/atividades/{id}/lancamentos` ganha a guarda do nulo.** O ato por atividade já
  existe e já atende o Admin, mas `lancar_resultados_da_atividade` lê a missão da atividade sem
  conferir nulo e devolve **500** na avulsa. É o ato certo para a avulsa justamente porque não
  consome reserva nem passa a aula a realizada — então roda quantas vezes o encontro exigir.
- **Lançamento por equipe da aula** (`RF-02-112`, `RN-02-32`), que o `RF-02-33` já previa
  ("Guerreiros, Guerreiras e equipes") e nunca foi entregue: desfecho e produção são da
  equipe e valem igualmente a cada Guerreiro(a) integrante **presente**; quem não tem presença
  é pulado, e o familiar da modalidade em equipe com familiar não recebe Resultado.
- **Três recusas novas** (`RN-02-33`): modalidade incoerente com a forma do lançamento, equipe
  sem nenhum integrante presente e **segundo Resultado do mesmo par (Guerreiro(a), atividade)**
  — sem essa última o ponto dobraria em silêncio, porque o ato roda várias vezes e o Resultado
  não se edita nem se remove.
- **Área Lançamentos da App 03** ganha o bloco da atividade avulsa, ao lado dos três atos que
  já tem. O **painel do dia segue de leitura**, levando à área, como já determina a capacidade
  `aplicacao-de-gestao`.

### Fora do escopo

- **Apps 01 e 05**: a avulsa não entra na programação do encontro nem nos desafios semanais do
  Guerreiro(a) — decisão do fundador de 2026-10-11, no documento 09 §1 e na §13 do PRD-02. Os
  dois `INNER JOIN` em `Missao` que a excluem (`painel_do_dia._atividades_previstas` e
  `equipes.programacao_do_encontro`) **permanecem como estão**: são eles que a mantêm fora da
  tela da criança.
- **Autoria de trilha, missão e atividade de missão**, que é do Mestre na App 09 (PRD-02 §3.2).
- **Lançamento das atividades do próprio Mestre**, que ele faz na App 09 (PRD-02 §3.2).
- **Botão de lançar dentro do painel do dia**: o painel é de leitura por requisito vigente.
- **Atividade avulsa cuja aula é cancelada depois dela** — pendência aberta na §14 do PRD-02 e
  no documento 09 §1. Esta change recusa o cadastro em aula **já** cancelada e não decide o
  cancelamento posterior.

## Capabilities

### New Capabilities

Nenhuma. As três capacidades alcançadas já existem no consolidado.

### Modified Capabilities

- `atividade-avulsa`: o cadastro passa a exigir a **aula** do encontro e o **formato
  presencial**; a comunidade vem da aula, não de campo próprio (`RF-02-29`).
- `resultado-de-atividade`: o lançamento da avulsa é ato do Admin **por aluno ou por equipe da
  aula**, com desfecho e produção da equipe valendo igualmente a cada integrante presente, e com
  as três recusas do `RN-02-33` (`RF-02-112`, `RN-02-32`, `RN-02-33`).
- `aplicacao-de-gestao`: o cadastro da avulsa ganha a escolha de comunidade e aula; a área
  **Lançamentos** ganha o bloco da avulsa, por aluno ou por equipe, e o painel do dia segue
  em leitura (`RF-02-29`, `RF-02-112`).

## Impact

**Núcleo (`backend/src/nucleo/`)**

- `atividades/regra.py` e `atividades/rotas.py`: `aula_id` obrigatório e conferido no cadastro,
  formato restrito a presencial, recusa de aula cancelada e inexistente; filtro por aula na
  listagem.
- `resultados/regra.py`: guarda do nulo em `lancar_resultados_da_atividade`; lançamento por
  equipe, com o recorte dos integrantes presentes; as três recusas.
- `resultados/rotas.py`: a entrada do ato por atividade passa a aceitar a **equipe** como
  alternativa à lista de participantes.
- Migração do esquema: `atividade.aula_id` segue existindo e anulável (a de trilha não a
  declara), então a obrigatoriedade da avulsa é regra, não coluna nova.

**App 03 (`apps/app-03-gestao/src/`)**

- `atividades/`: formulário com comunidade e aula; `api.ts` com o filtro.
- `lancamentos/`: bloco da atividade avulsa, com as duas formas de lançar.

**Sem impacto**: Apps 01, 04, 05, 06, 07, 08 e 09; `painel_do_dia`; `equipes`; livro-razão,
reservas e situação da aula, que o ato por atividade não toca.
