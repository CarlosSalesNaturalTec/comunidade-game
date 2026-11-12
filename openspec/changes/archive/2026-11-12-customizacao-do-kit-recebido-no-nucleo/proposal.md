# Proposal

Origem: **PRD-01** (núcleo), fatia sem número do bloco PRD-01 do
`openspec/cronograma-de-fatias.md` — "Customização do kit recebido no núcleo". Identificadores
atendidos: `RF-01-84`, `RF-01-85`, `RF-01-86`, `RF-01-87` e `RN-01-66`, mais o lado do núcleo de
`RF-09-141`, `RN-09-62`, `RF-09-113` e `RF-03-88` — a gravação do kit declarado no prático, a
exclusão entre as duas fontes, o crédito da conservação e a terceira fonte do acervo, que as
fatias de aplicação consomem.

## Why

As decisões do fundador de 2026-11-12 (documento 09 §1, "Customização do kit recebido" e
"Conservação do bem recebido") criam uma fonte de ponto extra — a nova customização do kit
recebido, julgada ao vivo pelo Mestre da aula — e levam a validação da conservação para a fila do
encontro, com uma só pontuação por bem e por encontro (documento 11 §§2.2 e 5). Hoje o núcleo não
sabe que kit um prático apresenta, não guarda registro de customização, e a conservação
(`RF-09-113`) nunca foi implementada: não há crédito algum pelo cuidado com o bem recebido. Todas
as fatias de aplicação da customização (PRD-09 fatia 31, PRD-04 fatias 34 e 35, PRD-05 fatia 18,
PRD-03 fatia 14) dependem desta.

## What Changes

- **O prático declara o kit que apresenta** (`RF-09-141`): campo opcional na declaração do
  desafio prático, apontando uma recompensa de marco da mesma trilha. O núcleo não distingue kit
  de camisa ou livro — vale a declaração do Mestre autor.
- **A customização abre** para o Guerreiro(a) que recebeu aquela recompensa e teve aprovado o
  prático que a declara; a comprovação aprovada é o primeiro registro do kit (`RF-01-84`).
- **Registro de customização**: descrição em texto (a fala chega transcrita) e foto ou vídeo
  pela sessão de envio, feito pelo próprio Guerreiro(a) ou capturado pelo Mestre da aula; um
  pendente por kit; o Guerreiro(a) acompanha e cancela o pendente (`RF-01-84`, `RF-01-86`).
- **Julgamento pelo Mestre da aula**, com a aula do encontro e presença registrada: aprovado
  credita **1 ponto extra** e leva o registro ao acervo; reprovado exige motivo e permite novo
  registro (`RF-01-85`).
- **Validação da conservação** de uma recompensa de marco entregue, na aula, creditando **1 ponto
  extra** (`RF-01-87`, `RF-09-113`).
- **Uma pontuação por bem e por encontro** — conservação ou customização, nunca as duas —
  garantida também no banco (`RN-01-66`, `RN-09-62`).
- **Fila do encontro**: leitura, para o Mestre da aula, dos bens recebidos de quem tem presença
  registrada, com o registro pendente, o último aprovado e o que já pontuou naquela aula.
- **O encerramento do ciclo expira** os registros de customização pendentes (`RF-01-86`).
- **Terceira fonte do acervo público**: o registro aprovado, de Guerreiro(a) com autorização
  vigente, sai com a descrição como título e a trilha da recompensa; a mídia pública segue o
  mesmo portão (`RF-03-88`).
- Migração Alembic: coluna do kit na missão e as tabelas do registro e da pontuação do bem.

**Fora desta fatia**: todas as telas — declaração do kit na App 09, fila e registro no App 01,
registro em casa na App 05 e exibição na vitrine (App 06) —, que são as fatias de aplicação do
cronograma; o PRD-01 §3.2 exclui interface do núcleo.

## Capabilities

### New Capabilities

- `customizacao-do-kit`: abertura, registro, mídia, cancelamento, expiração e julgamento da
  customização do kit recebido, e o crédito que ela rende.
- `conservacao-do-bem-recebido`: validação da conservação da recompensa de marco entregue, a
  fila do encontro e a regra de uma pontuação por bem e por encontro.

### Modified Capabilities

- `desbloqueio-da-missao`: a declaração do prático passa a aceitar, opcional, o kit que ele
  apresenta.
- `ponto-extra`: a conservação e a customização entram como fontes só extra.
- `fim-de-ciclo`: o encerramento passa a expirar os registros de customização pendentes.
- `leitura-publica-da-vitrine`: o acervo público ganha a terceira fonte e a rota pública da
  mídia dela.

## Impact

- **Núcleo**: `trilhas/` (declaração do prático), módulo novo do cuidado com o bem recebido
  (modelo, regra e rotas), `ponto_extra/` (crédito), `ciclo/` (expiração), `vitrine/` (acervo
  e mídia pública).
- **Contratos**: campo opcional novo na declaração do desafio de desbloqueio e na leitura dele;
  rotas novas do registro, do envio, do julgamento, da conservação e da fila; valor novo de
  `fonte` no item do acervo público. Nenhuma rota existente muda de comportamento.
- **Dados**: migração Alembic, sem _backfill_ — prático já declarado segue sem kit.
- **Documentação**: as decisões já estão nos documentos 11, 02, 09 e 99 e nos PRDs; esta change
  fecha a linha do cronograma.
