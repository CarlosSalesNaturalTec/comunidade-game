# Proposal

Fatia **18 do PRD-04** (`openspec/cronograma-de-fatias.md`), decisão do fundador de
2026-09-23 (documento 09 §1). Atende `RF-04-67`, `RF-04-68` e `RN-04-40` (novos), alterando
`RF-04-01` e `RF-04-29`.

## Why

A App 01 registra a presença e, no mesmo atendimento, leva a criança às equipes. Quem volta ao
aparelho para trocar de equipe, retomar a missão ou responder ao quiz esbarra no aviso de
presença já registrada e **não passa** — o único caminho de volta às equipes é o mesmo que
registra a presença. Separar os dois caminhos atende `RF-04-67` e `RF-04-68` e desfaz esse beco
sem saída.

## What Changes

- Tela inicial passa a oferecer **Onboarding**, **Presença** e **Equipes**: o botão Trilhas
  vira **Presença** (`RF-04-01`). Quiz ao Vivo, medição do limiar e troca por recompensa
  avulsa seguem como estão na tela.
- **Caminho Presença**: entrada por nick e imagem, ou confirmação do adulto com PIN, registra a
  presença e **termina ali**, voltando à tela inicial — não leva às equipes (`RF-04-67`).
- **Caminhos Equipes, Quiz e Troca**: abrem a sessão do Guerreiro(a) pelos mesmos dois meios e
  **não registram presença**; recusam quem não a tem no encontro e o mandam ao caminho
  Presença (`RF-04-68`, `RN-04-40`). Quiz e Troca entram nessa regra por decisão do fundador de
  2026-09-23, que estende `RN-04-40` — sem ela, os dois continuariam no beco sem saída.
- **BREAKING (comportamento)**: entrar pelo caminho das equipes deixa de registrar presença. A
  criança que chega ao encontro passa **obrigatoriamente** pelo caminho Presença.
- **Núcleo**: `GET /v1/aulas/{id}/presencas/eu` devolve ao Guerreiro(a) em sessão se ele tem
  presença não anulada naquela aula, e as rotas de formação da **equipe da aula** recusam quem
  não a tem (`RF-04-68`, `RN-04-40`).
- Trabalhar a trilha — programação, missão, produção e assistente — fica **dentro** de Equipes,
  depois de escolher a equipe, como já acontece no aparelho.
- Documentação: uma frase no documento 03 §§3 e 4 estendendo a exigência a quiz e troca, a
  linha do documento 09 §1 ajustada, `RN-04-40` ampliada no PRD-04 e as jornadas §§5.9 e 5.10.

## Capabilities

### New Capabilities

Nenhuma.

### Modified Capabilities

- `aplicacao-da-aula-presencial`: a tela inicial passa a três caminhos; a entrada por nick e
  imagem deixa de registrar presença fora do caminho Presença; os caminhos Equipes, Quiz e
  Troca recusam quem não tem presença no encontro.
- `aula-e-presenca`: o Guerreiro(a) em sessão lê se tem presença registrada na aula.
- `equipe`: criar equipe da aula e entrar em equipe da aula exigem presença registrada naquela
  aula.

## Impact

- `apps/app-01-aula-presencial/`: `inicio/TelaInicial.tsx`, `entrada/TelaDeEntradaDoGuerreiro.tsx`,
  `api/presencas.ts` e os testes de `inicio`, `entrada` e `equipes`.
- `backend/src/nucleo/aulas/rotas.py` (leitura nova), `backend/src/nucleo/equipes/regra.py` e
  `rotas.py` (recusa sem presença), e os testes de `test_equipe_rota.py`, `test_presenca*`.
- Documentação: documento 03 §§3 e 4, documento 09 §1, PRD-04 §§5.9, 5.10 e 7, e
  `openspec/cronograma-de-fatias.md`.
- Fora do escopo: a guarda de presença no núcleo para a **equipe da trilha** (a rota não
  carrega a aula do encontro; o aparelho só a oferece dentro do caminho Equipes, já atrás da
  guarda) e para as rotas de quiz e de troca (a troca é operação do Mestre). Também fica fora
  o que o PRD-04 §3.2 já exclui.
