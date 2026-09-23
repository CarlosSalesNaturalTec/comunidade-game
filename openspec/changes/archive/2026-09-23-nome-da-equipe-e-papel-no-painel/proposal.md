# Proposal

**PRD de origem:** PRD-04 — Aula presencial (App 01), **fatia 17** do
`openspec/cronograma-de-fatias.md`. Alcança o PRD-02 pelo painel do dia.

**Identificadores:** `RF-04-69`, `RF-04-70` e `RN-04-39` (novos); `RF-04-34` e `RF-02-08`
(alterados).

## Why

A equipe não tem nome: o App 01 a mostra pelos nicks dos integrantes, e o painel do dia da
App 03 a chama pelos nicks juntados por vírgula, sem o papel de ninguém. O Mestre não consegue
dizer "a equipe Leões" em sala, e o painel não mostra quem constrói, registra, apresenta ou
media. O nome já constava do PRD-04 §§5.7 e 8 e do documento 02 §5, mas sem requisito na §6 —
nenhuma fatia o entregou. A decisão do fundador de 2026-09-23 (documento 09, linha "Presença e
equipes em caminhos separados, e a equipe com nome") fixa o tamanho, a unicidade e a troca.

## What Changes

- **Nome da equipe** no núcleo: obrigatório, até 20 caracteres, único entre as equipes da
  mesma aula — ou da mesma trilha. Vale tanto na criação da equipe da aula quanto na da
  trilha (`RF-04-69`, `RN-04-39`).
- **Renomear:** `PATCH /v1/equipes/{id}`, só para quem integra a equipe, com a mesma regra
  do nome (`RF-04-70`).
- **Três pontos que o fundador decidiu na elicitação desta change, em 2026-09-23:**
  - a comparação de unicidade ignora maiúsculas e espaços nas pontas;
  - a troca do nome trava junto com a composição (aula encerrada ou equipe da trilha
    homologada);
  - as equipes que já existem ganham "Equipe N" na migração, por ordem de criação dentro de
    cada aula ou trilha.

  As duas primeiras são regra de negócio, então entram no documento 02 §5, no documento 09 e
  no PRD-04 no mesmo PR.
- **App 01:** pede o nome ao criar a equipe da aula e a da trilha, mostra cada equipe pelo
  nome junto do avatar e do nick dos integrantes e oferece renomear a quem a integra
  (`RF-04-34`, `RF-04-69`, `RF-04-70`).
- **Painel do dia:** o núcleo devolve o nome da equipe e o papel de cada integrante, e a App 03
  mostra os dois no lugar dos nicks juntados (`RF-02-08`).
- **BREAKING:** `POST /v1/aulas/{id}/equipes` e `POST /v1/trilhas/{id}/equipes` passam a exigir
  `nome` no corpo. Só o App 01 chama essas rotas, e ele muda no mesmo PR.

## Capabilities

### New Capabilities

Nenhuma.

### Modified Capabilities

- `equipe`: a equipe nasce com nome válido e único na aula ou na trilha; quem a integra a
  renomeia, com a trava da composição; as leituras devolvem o nome (`RF-04-69`, `RF-04-70`,
  `RN-04-39`, `RF-04-34`).
- `aplicacao-da-aula-presencial`: a formação da equipe da aula e a da trilha pedem o nome; a
  tela das equipes mostra o nome e oferece renomear (`RF-04-34`, `RF-04-69`, `RF-04-70`).
- `painel-do-dia`: cada equipe sai com o nome e com o papel de cada integrante (`RF-02-08`).
- `aplicacao-de-gestao`: o Painel do dia apresenta a equipe pelo nome e cada integrante com o
  papel (`RF-02-08`).

## Fora do escopo

- **Presença e equipes em caminhos separados** (`RF-04-67`, `RF-04-68`, `RN-04-40`): é a
  fatia 18. Esta change não muda a tela inicial nem exige presença para formar equipe.
- Criar, editar ou desfazer equipe pela gestão: a App 03 só lê (`RF-02-09`).
- Nome da equipe na condução da partida de quiz e na App 05: o recorte desta fatia não tem
  requisito que os peça. O nome vai no payload, mas essas telas não mudam.

## Impact

- **Núcleo:** `backend/src/nucleo/equipes/` (modelo, regra e rotas), a migração Alembic da
  coluna `nome` com o preenchimento das equipes existentes, e
  `backend/src/nucleo/painel_do_dia/regra.py`. Testes em `backend/tests/`.
- **App 01:** `src/api/equipes.ts`, `src/equipes/TelaDeEquipes.tsx`,
  `src/trilhas/EquipeDaTrilha.tsx` e os testes delas.
- **App 03:** `src/painel-do-dia/api.ts`, `TelaDoPainelDoDia.tsx` e o teste.
- **Documentação:** documento 02 §5, documento 09 (a linha já decidida), PRD-04 (`RF-04-70`,
  `RN-04-39`) e a linha 17 do cronograma.
