# Proposal

Origem: **PRD-09 — Área do Mestre (App 09)**, **fatia 33** do `openspec/cronograma-de-fatias.md`,
com alcance no PRD-01, no PRD-02 e no PRD-05.

Atende os identificadores **novos** `RF-01-88`, `RF-01-89`, `RF-01-90`, `RN-01-67`, `RN-01-68`,
`RF-09-143`, `RF-09-144`, `RF-02-116` e `RF-05-104`, criados por esta change na revisão dos
quatro PRDs. Aplica a decisão do fundador de **2026-11-13**, tomada no `/opsx:propose` que abriu
a change (documento 11 §5; linha "Histórico de pontuação do Guerreiro(a)" do documento 09).

## Why

O núcleo guarda só o **total** de ponto regular por trilha ou poder e as duas contas de ponto
extra: nem o Mestre, nem o Admin, nem o próprio Guerreiro(a) conseguem saber **como e quando**
se chegou a um número. Quando um saldo surpreende — uma conduta que debitou, uma presença
anulada, uma troca —, não há onde conferir.

## What Changes

- **Documentos-fonte**: documento 11 §5 ganha o parágrafo do histórico de pontuação; documento
  15 §9 inclui o histórico entre as telas que mostram o saldo disponível; documento 09 registra
  a decisão em "Já decididos"; documento 99 §§3 e 5 ganham a linha do conceito.
- **PRDs**: nascem `RF-01-88` a `RF-01-90`, `RN-01-67`, `RN-01-68`, `RF-09-143`, `RF-09-144`,
  `RF-02-116` e `RF-05-104`, com §9, §13 e §15 de cada PRD acompanhando.
- **Núcleo**: nasce o **lançamento de pontuação**, somente inserção, gravado na mesma transação
  de cada crédito e débito de ponto regular e extra (`RF-01-88`, `RN-01-67`); a migração abre
  cada conta existente com a linha de **saldo anterior** (`RF-01-90`); duas rotas de leitura —
  `GET /v1/eu/historico-de-pontuacao` e `GET /v1/guerreiros/{id}/historico-de-pontuacao` —
  servem o histórico com os saldos (`RF-01-89`, `RN-01-68`).
- **Regra que muda**: o saldo disponível de ponto extra deixa de ser lido só pelo Guerreiro(a);
  o Mestre do vínculo e o Admin passam a lê-lo **pelo histórico** (`RN-01-68`). A rota
  `GET /v1/eu/pontos-extras` continua só do Guerreiro(a), e o contrato dos jogos continua sem o
  saldo (`RN-01-41`).
- **App 09**: nasce a lista dos Guerreiros e Guerreiras da comunidade do vínculo e a ficha de
  cada um, com o histórico (`RF-09-143`, `RF-09-144`).
- **App 03**: a lista de Guerreiros e Guerreiras abre a ficha com o histórico (`RF-02-116`).
- **App 05**: a carteira ganha o histórico do próprio (`RF-05-104`).

## Capabilities

### New Capabilities

- `historico-de-pontuacao`: o lançamento de cada movimento de ponto, a linha de saldo anterior
  e a leitura do histórico com os saldos, com quem pode ler.

### Modified Capabilities

- `ponto-extra`: o saldo disponível passa a ser lido também pelo Mestre do vínculo e pelo Admin,
  pelo histórico; a rota própria do Guerreiro(a) segue como está.
- `area-do-mestre`: lista e ficha do Guerreiro(a) da comunidade do vínculo, com o histórico.
- `aplicacao-de-gestao`: ficha do Guerreiro(a) com o histórico, aberta da lista.
- `area-do-guerreiro`: o próprio histórico de pontuação na carteira.

## Fora do escopo

- Reconstruir os lançamentos anteriores à implantação a partir dos fatos já gravados: o passado
  entra pela linha de saldo anterior, por decisão do fundador.
- Histórico na Área dos pais e responsáveis (App 07), na vitrine (App 06) e no contrato dos jogos.
- Filtro, busca e exportação do histórico; correção de lançamento (não há edição — `RN-01-67`).
- Pontos da batalha, que ainda não existem no núcleo (PRD-10).
- O que os §3.2 do PRD-01, PRD-02, PRD-05 e PRD-09 já excluem.

## Impact

- **Núcleo**: módulo novo `backend/src/nucleo/historico_de_pontuacao/` (modelo, regra, rotas);
  `pontuacao/regra.py` e `ponto_extra/regra.py` passam a receber a origem e gravar o
  lançamento; chamadores em `resultados`, `coletas`, `quiz`, `criacoes_originais`, `trilhas`,
  `ocorrencias_de_conduta`, `aulas`, `cuidado_do_bem`, `fila` e `trocas` passam a origem; uma
  migração Alembic cria a tabela e a linha de saldo anterior.
- **Apps**: `app-09-mestre` (tela nova de Guerreiros e ficha), `app-03-gestao` (`personas/`),
  `app-05-guerreiro` (`carteira/`); componente de lista do histórico em `comum/pontuacao/`, que as três
  apps compartilham.
- **Documentos**: 09, 11, 15, 99 e PRD-01, 02, 05, 09; cronograma de fatias.
