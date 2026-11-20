# Proposal

**PRD-07, fatia 13** do `openspec/cronograma-de-fatias.md` — entrega pelo disponível e pela
aprovação do prático. Atende `RF-07-13`, `RN-07-01`, `RN-07-42`, `RN-07-44` (PRD-07 v12),
`RF-09-76`, `RF-09-146` e `RN-09-63` (PRD-09 v8). Decisão do fundador de 2026-11-20, linha
"Consumo do encontro e recompensa de marco" do documento 09. Depende da fatia 11, implementada.

## Why

A entrega da recompensa de marco confere o **saldo**, não o disponível: em 2026-11-07 e
2026-11-14 ela entregou kits que estavam reservados para a aula, e o disponível ficou negativo.
Fora do encontro, o Mestre escolhe de que ponto de apoio o kit sai, e a aprovação do desafio
prático — que é onde o Mestre de fato entrega o kit — não registra entrega nenhuma.

## What Changes

- A entrega confere o **disponível** — saldo menos o reservado — do ponto de apoio de onde o
  recurso sai (`RF-07-13`, `RN-07-01`, `RN-07-42`).
- **Fora do encontro**, o recurso sai do ponto de apoio da **aula imediatamente anterior** da
  comunidade do Guerreiro(a) — a de início mais recente até agora, não cancelada, o que cobre a
  aula em andamento —; o Mestre não escolhe mais o ponto (`RF-09-76`, `RF-07-13`).
  **BREAKING:** `POST /recompensas-de-marco/{id}/entrega` deixa de aceitar `ponto_de_apoio_id`;
  sem `aula_id`, o núcleo deriva o ponto.
- **A aprovação do prático entrega**: julgado "cumpriu", cada recompensa cujo marco aquele
  julgamento alcançou é entregue no mesmo ato, com baixa, quando quem julga é vinculado à
  comunidade do Guerreiro(a) e há lastro. Senão, a aprovação vale — a missão seguinte abre — e a
  entrega fica na fila de entregas pendentes do Mestre vinculado (`RF-09-146`, `RN-09-63`,
  `RN-07-44`). A resposta do julgamento diz quais recompensas foram entregues.
- App 09: a fila de entregas pendentes deixa de pedir o ponto de apoio, e a bancada de
  julgamento diz quando a aprovação entregou a recompensa.

## Capabilities

### New Capabilities

Nenhuma.

### Modified Capabilities

- `recompensa-de-marco`: lastro contra o disponível; ponto de apoio da aula anterior fora do
  encontro; entrega pela aprovação do prático.
- `area-do-mestre`: fila sem escolha de ponto; aviso da entrega na aprovação.

## Impact

- Núcleo: `recompensas_de_marco` (regra e rota), `aulas/regra.py` (aula de referência da
  comunidade), `trilhas/rotas.py` (julgamento).
- App 09: `recompensas/FilaDeEntregasPendentes.tsx`, `turmas/TelaDeDesbloqueiosPendentes.tsx`.
- Fora do escopo: necessidade da recompensa de marco (fatia 14). A App 01 já entrega pela aula
  do encontro e não muda.
