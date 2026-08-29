## Why

Fatia 14 do **PRD-02** (`openspec/cronograma-de-fatias.md`, bloco PRD-02), mais a linha sem
número **Entregas confirmadas**, do mesmo bloco. A App 03 é o único lugar onde a solicitação de
direitos do responsável é tratada — com protocolo, prazo de 7 dias e desfecho registrado —, e
hoje não existe nem a fila nem a entidade que a sustenta: das cinco solicitações do PRD-01 §8, o
núcleo tem quatro, e a `SolicitacaoDoResponsavel` nunca foi implementada. Sem ela, o direito que
o documento 03 §9 promete à família não tem onde ser exercido. Na mesma entrega vai a leitura das
entregas confirmadas pelo Mestre, que fecha o acervo da gestão: o núcleo já grava a entrega com a
baixa definitiva, e a gestão não tem tela que a mostre.

Identificadores atendidos: `RF-02-23`, `RF-02-24`, `RF-02-66`, `RF-02-50`, `RF-02-51`,
`RN-02-17`. No núcleo, o mesmo recorte atende `RF-13-22`, `RF-13-24`, `RF-13-25`, `RF-13-26`,
`RN-13-13` e `RN-13-14`.

**A fatia deixa de entrar junto da fatia 4 do PRD-13** (decisão do fundador, 2026-08-29): o
núcleo da solicitação — entidade, abertura pelo responsável e leitura das próprias — vem aqui,
para que a fila nasça alimentável e verificável de ponta a ponta; a fatia 4 do PRD-13 fica com as
telas da App 07 e com o que só ela decide — o limite da despersonalização antes do aceite
(`RF-13-23`, `RN-13-12`), a recusa da imagem (`RF-13-27`, `RF-13-28`) e o apagamento do
_template_ biométrico (`RF-13-43`, `RF-13-44`, `RN-13-22`).

## What Changes

- O núcleo ganha a **quinta solicitação** do PRD-01 §8, `SolicitacaoDoResponsavel`, com
  protocolo, responsável, Guerreiro(a), tipo, texto, situação, prazo, quem tratou, desfecho e
  data, sobre o mesmo ciclo de prazo e atraso das outras quatro (`RN-13-14`).
- O responsável passa a **abrir a solicitação** por `POST /v1/solicitacoes`, nos quatro tipos —
  acesso, correção, exclusão e esclarecimento —, recebendo protocolo e prazo de 7 dias, e a **ler
  as próprias** por `GET /v1/eu/solicitacoes`, com protocolo, tipo, situação, prazo e atraso
  (`RF-13-22`, `RF-13-24`, `RF-13-25`, `RF-13-26`). Segunda solicitação idêntica em aberto é
  recusada com 409, como o PRD-13 §9 prevê.
- O Admin passa a ler a fila por `GET /v1/solicitacoes-do-responsavel` e a registrar o desfecho
  por `POST /v1/solicitacoes-do-responsavel/{id}/tratamento`, que grava quem tratou e quando
  (`RF-02-23`, `RF-02-24`).
- A App 03 ganha, na área **Filas**, a fila das solicitações do responsável: protocolo, tipo,
  situação e prazo de 7 dias na lista, o tratamento com desfecho na tela de avaliação, e o
  destaque **em atraso** para a solicitação sem desfecho vencido o prazo (`RF-02-23`, `RF-02-24`,
  `RF-02-66`).
- A App 03 ganha, na área **Acervo**, a leitura das **entregas confirmadas pelo Mestre** — o
  exemplar da linha Alpha e a camisa —, com o Guerreiro(a), o Mestre que entregou, o ponto de
  apoio, a data e a **baixa definitiva** no livro-razão (`RF-02-50`, `RF-02-51`, `RN-02-17`). A
  área segue sem oferecer saída de exemplar: a confirmação da entrega é ato do Mestre.
- `GET /v1/entregas` passa a devolver, além do que já devolve, o **tipo de recurso**, a
  **quantidade** e o **lançamento** da baixa, sem o que a gestão não distingue o exemplar Alpha
  da camisa nem mostra a baixa.

## Capabilities

### New Capabilities

- `solicitacao-do-responsavel`: a solicitação de direitos aberta pelo responsável — os quatro
  tipos, o protocolo, o prazo de 7 dias, o atraso derivado, a leitura pela família, a fila do
  Admin e o desfecho com quem tratou e quando.

### Modified Capabilities

- `aplicacao-de-gestao`: ganha a fila das solicitações do responsável na área Filas
  (`RF-02-23`, `RF-02-24`, `RF-02-66`) e a leitura das entregas confirmadas na área Acervo
  (`RF-02-50`, `RF-02-51`, `RN-02-17`).
- `recompensa-de-marco`: a leitura de `GET /v1/entregas` passa a devolver o tipo de recurso, a
  quantidade e o lançamento da baixa, para que a gestão mostre a entrega com a baixa definitiva
  (`RF-02-50`, `RF-02-51`, `RN-02-17`).

## Impact

- `backend/src/nucleo/solicitacoes_do_responsavel/` — módulo novo: modelo, regra e rotas.
- `backend/src/nucleo/recompensas_de_marco/rotas.py` — a saída da entrega ganha três campos.
- `backend/alembic/` — migração da tabela nova.
- `apps/app-03-gestao/src/filas/` e `apps/app-03-gestao/src/acervo/` — a fila nova e a lista de
  entregas.
- `openspec/cronograma-de-fatias.md` — a fatia 14 do PRD-02 e a linha Entregas confirmadas mudam
  de situação; a fatia 4 do PRD-13 perde o núcleo da solicitação e mantém as telas da App 07.
- `docs/` — a decisão do fundador sobre a separação das duas fatias entra no documento 09 §1;
  o PRD-02 §9 perde a rota `POST /v1/entregas`, resíduo da decisão de 2026-08-19 que já passou
  `RF-02-50` e `RF-02-51` de escrita para leitura e que a §6.5 do PRD-02 já reflete; o PRD-13 §9
  registra que a abertura da solicitação já está no núcleo. Nenhum arquivo novo em `docs/`.

## Fora do escopo

O que o PRD-02 §3.2 já exclui e esta fatia toca de perto: a **Área dos pais e responsáveis** em
si — a App 07 é do PRD-13 —, e a **saída do exemplar do acervo permanente** pela gestão, que
segue sendo ato do Mestre. Fora do escopo por serem da fatia 4 do PRD-13: o aviso do limite da
despersonalização antes do aceite do pedido de exclusão (`RF-13-23`, `RN-13-12`), a recusa da
imagem captada no onboarding (`RF-13-27`, `RF-13-28`) e o apagamento do _template_ biométrico
(`RF-13-43`, `RF-13-44`, `RN-13-22`) — nenhum deles é efeito automático do desfecho gravado
nesta fatia. `RF-02-56` (conferência de inventário) segue travado pela pendência do `RF-07-20`,
no documento 09.
