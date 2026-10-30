# Tasks

## 1. Núcleo — recorte por aula na fila

- [x] 1.1 Em `recompensas_de_marco/regra.py`, aceitar a aula em `listar_entregas_pendentes`:
      com ela, alcançar só quem tem **presença registrada e não anulada** naquela aula; sem
      ela, seguir alcançando as comunidades do Mestre; aula de comunidade a que o Mestre não
      está vinculado recusa com **403** (`RF-09-75`, spec `recompensa-de-marco`).
- [x] 1.2 Em `recompensas_de_marco/rotas.py`, receber `aula_id` como parâmetro opcional de
      `GET /v1/recompensas-de-marco/pendentes` e verificar o contrato pelo OpenAPI
      (design — decisão 1).
- [x] 1.3 Cobrir em `backend/tests/test_entregas_pendentes.py` os cenários do delta: a fila da
      aula só com quem registrou presença, presença anulada que tira a pendência, a fila sem
      recorte que segue sendo das comunidades, e a aula de outra comunidade recusada com 403.

## 2. Núcleo — entrega pelo ponto de apoio da aula

- [x] 2.1 Em `recompensas_de_marco/regra.py`, aceitar a aula em `registrar_entrega`: o ponto de
      apoio passa a ser o **declarado na aula**, o lastro é reverificado contra o saldo dele e a
      entrega exige **presença registrada e não anulada** do Guerreiro(a) naquela aula
      (`RF-09-76`, `RF-07-13`, spec `recompensa-de-marco`).
- [x] 2.2 Em `recompensas_de_marco/rotas.py`, tornar `ponto_de_apoio_id` e `aula_id`
      **mutuamente exclusivos** no corpo da entrega — 422 quando vierem os dois e 422 quando
      não vier nenhum — e verificar o contrato pelo OpenAPI (design — decisão 2).
- [x] 2.3 Cobrir em `backend/tests/test_entrega_de_recompensa.py`: a baixa contra o ponto de
      apoio da aula, a recusa por falta de lastro nele, a recusa a quem não tem presença, a
      recusa à presença anulada, a recusa ao Admin e os dois desvios da exclusividade.

## 3. App 01 — a fila do encontro

- [x] 3.1 Criar, em `apps/app-01-aula-presencial/src/entregas/`, o cliente de API e a tela da
      fila do encontro: lista com nick, avatar, trilha, marco, tipo de recurso e quantidade,
      **sem seletor de ponto de apoio** e sem valor em moedas ou reais; confirma sob o
      `tokenDeTrabalho` declarando a aula, relê a fila e apresenta a recusa do núcleo como ela
      vem (`RF-09-75`, `RF-09-76`, spec `aplicacao-da-aula-presencial`).
- [x] 3.2 Acrescentar o caminho na `TelaInicial`, no grupo "Para quem opera o aparelho", entre
      a chave do momento de troca e o encerramento, visível **apenas quando quem abriu a sessão
      de trabalho é Mestre** — mesmo molde de `podeAbrirMomentoDeTroca` (`RF-04-71`,
      `RF-04-49`, `RN-02-17`, design — decisão 4).
- [x] 3.3 Cobrir nos testes da App 01 os cenários do delta: o cartão visível ao Mestre e
      ausente ao Admin, com o encerramento seguindo por último; quem chegou e conquistou
      aparecendo na fila; quem não registrou presença ausente dela; o encontro sem pendência
      alguma; e a ausência do seletor de ponto de apoio.

## 4. Documentação

- [x] 4.1 No mesmo PR: marcar a **fatia 31** como implementada, com o slug, em
      `openspec/cronograma-de-fatias.md`; alterar a tabela do **documento 02 §8.1**, que manda o
      Mestre escolher o ponto de apoio, para distinguir a App 09 — onde ele escolhe — do
      encontro, onde o ponto de apoio é o da aula; acrescentar o fluxo ao **PRD-04 §5** e
      registrar a distinção no **PRD-07** (`RF-07-13`) e no **PRD-09** (`RF-09-76`).
      `docs/prds/index.md` **não muda** — nenhum PRD muda de situação —, e a decisão já está
      gravada no `docs/09` §1, linha "Entrega da recompensa de marco no encontro".

## Workflow follow-up

- Arquivar as duas changes depois da aprovação do fundador, começando pela do vínculo do
  Mestre, de que esta depende. Merge commit — nunca squash.
