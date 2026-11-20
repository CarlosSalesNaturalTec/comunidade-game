# Proposal

**PRD-07, fatia 12** do `openspec/cronograma-de-fatias.md` — baixa no fim da aula, sem
fechamento. Atende `RF-07-09`, `RF-07-55`, `RF-07-56`, `RN-07-43` (PRD-07 v12), `RF-01-91`
(PRD-01 v19), `RF-02-33`, `RF-02-35`, `RF-02-46`, `RF-02-47` e `RN-02-09` (PRD-02 v13). Decisão
do fundador de 2026-11-20, linha "Consumo do encontro e recompensa de marco" do documento 09.
Depende da fatia 11, implementada.

## Why

Hoje a reserva da aula só sai pelo lançamento da atividade realizada, que o Admin faz durante o
encontro e que nenhuma tela alcança depois dele. As aulas de 2026-11-07 e 2026-11-14 ficaram
presas — uma segurando 20 robôs e 20 baterias, a outra pendente de lastro —, e lançar agora a
primeira levaria o saldo de robôs a −9. O fundador decidiu que a aula não tem fechamento.

## What Changes

- **Varredura das aulas vencidas**: passado o `fim_em`, a aula confirmada tem as reservas
  baixadas pelo sistema e passa a **realizada**; a pendente de lastro passa a **realizada sem
  lastro**, sem baixa, e sai das necessidades (`RF-07-09`, `RF-07-55`, `RF-01-91`, `RN-07-43`,
  `RN-02-09`).
- **Disparo nos dois caminhos**, por decisão do fundador de 2026-11-20: o comando periódico
  `python -m nucleo.manutencao` e a varredura sob demanda no começo das operações que leem ou
  escrevem aula, saldo e necessidade.
- **Situação nova `realizada_sem_lastro`**, que não se cancela e não bloqueia a desativação do
  ponto de apoio, como a realizada.
- **BREAKING:** `POST /aulas/{id}/lancamentos` deixa de baixar a reserva e de mudar a situação:
  só grava os resultados, inclusive depois do fim da aula; só a aula cancelada o recusa
  (`RF-02-33`, `RF-02-35`).
- O painel do dia deixa de listar a pendência da atividade realizada (`RF-02-46`, `RF-02-47`).
- **Transição** (`RF-07-56`): na migração, a aula que já terminou tem a reserva liberada, sem
  baixa, e passa a realizada — ou a realizada sem lastro, se estava pendente.
- App 03 e App 09 rotulam a situação nova; a área Lançamentos deixa de dizer que fecha a aula.

## Capabilities

### New Capabilities

Nenhuma.

### Modified Capabilities

- `reserva-de-recurso`: a reserva da aula sai pela baixa no fim do horário ou pela liberação.
- `aula-e-presenca`: seis situações; realizada e realizada sem lastro pelo horário; varredura.
- `resultado-de-atividade`: o lançamento por aula só grava resultados.
- `painel-do-dia`: sem a pendência da atividade realizada.
- `aplicacao-de-gestao`: Lançamentos sem fechamento; rótulo da situação nova.
- `area-do-mestre`: rótulo da situação nova em Minhas turmas.

## Impact

- Núcleo: `aulas` (modelo, regra, rotas), `reservas`, `livro_razao` (débito com autoria do
  sistema), `resultados`, `painel_do_dia`, `necessidades`, `pontos_de_apoio`, `manutencao`;
  uma migração Alembic com a transição.
- App 03: `lancamentos/`, `agenda/ListaDaAgenda.tsx`. App 09: `turmas/TelaDeMinhasTurmas.tsx`.
- Fora do escopo: entrega pelo disponível (fatia 13) e necessidade da recompensa (fatia 14). O
  lançamento de resultados depois do fim da aula pela App 03 segue sem tela — a área Lançamentos
  continua sobre a aula vigente (PRD-02 §5.6); o Mestre lança por atividade na App 09.
