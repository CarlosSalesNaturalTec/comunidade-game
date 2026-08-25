## Why

O motor do Quiz ao Vivo está escrito e testado no núcleo desde a change
`quiz-ao-vivo` — `abrir_partida`, `registrar_resposta`, `anular_pergunta` e
`encerrar_partida` —, e o banco de perguntas do Mestre curador está no ar desde
`banco-do-quiz-ao-vivo`. Falta a **porta**: nenhuma das quatro operações tem rota HTTP, e
por isso não há como conduzir uma partida. É a mesma dívida que `equipes/regra.py` tinha
antes da primeira fatia do PRD-04.

Esta é a **fatia A** do recorte de Quiz ao Vivo do PRD-02 (`RF-02-59` a `RF-02-62`,
`RF-02-72`, `RF-02-73`), e fecha o `RF-09-41` do PRD-09 — o banco cadastrado só fica
disponível para a partida quando a condução tiver porta. A formação de equipe da aula, de
que a partida depende, chegou na primeira fatia do PRD-04.

## What Changes

- **Portas HTTP das quatro operações já implementadas**: abertura da partida
  (`RF-02-59`), _start_ da pergunta corrente (`RF-02-60`), anulação da pergunta contestada
  (`RF-02-72`) e encerramento com lançamento automático da pontuação (`RF-02-73`).
- **Estado novo da partida**: qual pergunta está no ar e se o resultado dela já foi
  liberado. A `PartidaDeQuiz` hoje não guarda nem uma coisa nem outra, e as duas são
  exigidas pelo `RF-02-60`, pelo `RF-04-44` e pela leitura da §5.7 item 6 do PRD-02 —
  dispositivo que caiu volta na pergunta corrente.
- **Leitura do estado da partida** para quem conduz e para o aparelho da equipe, por
  **sondagem periódica** a cada 2 segundos. Decisão do fundador de 2026-08-25: a
  sincronização em tempo real do Ciclo 01 é sondagem, e não conexão longa — vai ao
  documento 03 §1 e ao documento 09, com o painel do dia a 10 segundos.
- **Tela de condução na App 03**: abrir a partida sobre a atividade e as equipes da aula,
  pôr pergunta no ar, apurar e liberar o resultado, anular e encerrar (`RF-02-61`,
  `RF-02-62`, `RN-02-20`).
- **Rotas da App 01 entregues testadas por contrato, sem tela**: `GET
  /v1/partidas-de-quiz/{id}/pergunta` e `POST /v1/partidas-de-quiz/{id}/respostas` do
  PRD-04 §9 (`RF-04-41`, `RF-04-43`, `RF-04-44`). São a leitura e a escrita do mesmo estado
  que esta fatia cria; a tela do aparelho da equipe é a fatia B.
- **O PRD-02 §9 recebe as rotas que faltam**: anulação, liberação do resultado e leitura do
  estado da partida — os requisitos existem, as rotas não estavam declaradas.
- **Correção de PRD ao documento 05 §5, sem decisão nova**: o `RF-02-61` e o PRD-04 §8
  perdem o "aparelho vinculado". O documento 05 §5 item 5 já decide que **a plataforma não
  controla aparelhos no Ciclo 01** e que a resposta é registrada pela equipe, nunca pelo
  aparelho de onde veio — é o que `registrar_resposta` já implementa, por idempotência em
  (partida, pergunta, equipe). A hierarquia resolve pelo nível de cima.

Fora do escopo, pelo PRD-02 §3.2 e pelo recorte: a autoria do banco de perguntas, que é da
App 09 e já está entregue; e a tela do aparelho da equipe na App 01, que é a fatia B.

## Capabilities

### New Capabilities

Nenhuma. A fatia opera sobre capacidades existentes.

### Modified Capabilities

- `quiz-ao-vivo`: a partida passa a ter **pergunta corrente** e **resultado liberado**, e as
  quatro operações do motor ganham porta HTTP, com a leitura do estado para quem conduz e
  para o aparelho da equipe.
- `aplicacao-de-gestao`: a App 03 ganha a **tela de condução da partida**, com a sondagem a
  cada 2 segundos e a recusa de escrita a Mestre que não conduz aquela aula.

## Impact

- **Núcleo** — `backend/src/nucleo/quiz/`: `rotas.py` ganha as rotas da partida; `modelo.py`
  ganha o estado da pergunta corrente e da liberação do resultado, com migração Alembic;
  `regra.py` ganha as operações do estado novo, sem alterar as quatro já testadas.
- **App 03** — `apps/app-03-gestao/src/`: área nova da condução da partida, consumindo as
  rotas por sondagem.
- **Documentação no mesmo PR**: documento 03 §1 (a sondagem e os dois intervalos), documento
  09 §1 (a linha movida para "Já decididos"), PRD-02 (`RF-02-61`, §9 e §10), PRD-04 (§8 e
  §10) e `docs/prds/index.md`.
- **Esteiras**: backend e App 03 já têm a delas; nenhuma pasta nova.
