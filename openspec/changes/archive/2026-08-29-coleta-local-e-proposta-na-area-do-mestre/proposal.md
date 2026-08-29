## Why

Origem: **PRD-09 — Área do Mestre**, fatias **7** e **8** do
`openspec/cronograma-de-fatias.md`. Recorte: `RF-09-27`, `RF-09-28` (fatia 7) e `RF-09-53` a
`RF-09-55` (fatia 8).

A trilha do Mestre **não publica**. A trava de `RN-08-14` — ao menos um desafio de coleta na
trilha — já está de pé desde a fatia 2, e a App 09 não tem por onde criar um: o núcleo expõe
`POST /v1/desafios-de-coleta` desde o PRD-08, mas nenhuma tela do Mestre o chama, e o catálogo
de tipos de coleta, entre os quais `RF-09-27` manda escolher, **não tem leitura alguma** no
núcleo. Sem esta fatia a autoria da trilha morre no último passo.

As duas outras portas da mesma superfície estão igualmente fechadas. A solicitação de novo
local que o Guerreiro(a) abre na App 05 fica parada até que um Admin a veja, embora o núcleo já
autorize o **Mestre autor da trilha do desafio de origem** a avaliá-la (`RF-08-23`). E a
proposta de evolução, que o PRD-09 §9 declara como `POST /v1/sugestoes`, não tem porta na App
09 nem forma de acompanhar o status.

As duas fatias entram numa change só porque partilham a mesma superfície nova da App 09 — o
território da trilha — e a mesma junção desafio → missão → trilha que define a posse do Mestre.

## What Changes

Fatia 7 — desafio de coleta:

- A App 09 ganha a declaração do **desafio de coleta** dentro da missão: tipo escolhido no
  catálogo, cadência, vigência, granularidade exigida e quantos registros do período pontuam
  (`RF-09-27`, `RF-09-28`). A escrita é a rota do PRD-08 já existente — nenhuma regra de coleta
  nasce aqui.
- O núcleo passa a **servir o catálogo de tipos de coleta em leitura**: hoje só há escrita de
  Admin, e sem a lista o Mestre não tem entre o que escolher.
- `GET /v1/trilhas/minhas` passa a trazer os desafios de coleta **aninhados em cada missão**,
  como já traz as atividades e as etiquetas ODS, para que o Mestre veja o que já declarou e o
  que ainda falta para publicar.

Fatia 8 — solicitação de local e proposta:

- A App 09 ganha a área de **território**: as solicitações de novo local em aberto dos desafios
  das trilhas do próprio Mestre, com aprovação — informando o local pai — ou recusa com motivo
  (`RF-09-53`), sobre as rotas de avaliação e de listagem que o PRD-08 já entregou.
- A área exibe **alerta enquanto houver solicitação sem desfecho** (`RF-09-54`).
- A App 09 ganha a **proposta de evolução da plataforma**, registrada na fila única e
  acompanhada pelo Mestre até o desfecho (`RF-09-55`). O núcleo passa a devolver ao autor as
  próprias sugestões: hoje só o Admin lê a fila.

Fora do escopo, como o PRD-09 §3.2 já exclui: **cadastro direto de local e criação de
Comunidade Virtual**, que seguem de Admin — o Mestre só avalia o pedido; e a **avaliação da
proposta**, que é da App 03. A auditoria por amostragem da coleta (`RF-09-35`, `RN-09-21`) foi
ao Ciclo 02 por decisão do fundador de 2026-08-28 e não entra aqui.

## Capabilities

### New Capabilities

Nenhuma. As quatro capacidades tocadas já existem: a coleta e o território nasceram no PRD-08 e
a fila única no PRD-01. Esta change abre as portas do Mestre para elas.

### Modified Capabilities

- `area-do-mestre`: a App 09 ganha a declaração do desafio de coleta na missão, a área de
  território com a avaliação das solicitações de local e o alerta das que estão em aberto, e a
  proposta de evolução com acompanhamento do status (`RF-09-27`, `RF-09-28`, `RF-09-53` a
  `RF-09-55`).
- `catalogo-de-tipos-de-coleta`: o catálogo, hoje só de escrita, passa a ser **legível** por
  quem escolhe entre os tipos — sem isso `RF-09-27` não tem como ser cumprido.
- `desafio-de-coleta`: o **Mestre autor** passa a ler os desafios das suas missões, pela leitura
  da trilha própria que já existe. A rota de Admin e a do Guerreiro(a) não mudam.
- `fila-de-avaliacao`: quem propôs passa a **ler as próprias sugestões e propostas**, com a
  situação, o prazo, o desfecho e o motivo do retorno — a leitura de Admin não muda.

## Impact

- **Núcleo (`backend/`)**: `coletas/` ganha a leitura do catálogo de tipos; `trilhas/` aninha os
  desafios na saída de `/trilhas/minhas`; `fila/` ganha a leitura das próprias sugestões.
  **Nenhuma migração**: não nasce entidade nem coluna — as três tabelas envolvidas
  (`tipo_de_coleta`, `desafio_de_coleta`, `sugestao_ou_proposta`) já existem.
- **`locais/` não é tocado**: a avaliação da solicitação e a listagem das em aberto com o
  recorte do Mestre já estão implementadas e testadas desde o PRD-08.
- **App 09 (`apps/app-09-mestre/`)**: módulo novo `territorio/`, o formulário do desafio de
  coleta dentro de `trilhas/` e o módulo novo `propostas/`. A navegação de áreas ganha duas
  entradas, uma delas com o contador do alerta.
- **Documentação**: as linhas das fatias 7 e 8 no `openspec/cronograma-de-fatias.md`. Nenhuma
  decisão nova de produto, logo nada muda nos documentos 01–15 nem no 99.
