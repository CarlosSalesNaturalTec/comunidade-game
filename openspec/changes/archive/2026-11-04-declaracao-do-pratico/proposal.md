# Proposal

## Why

É a **fatia 26 do PRD-09** (`openspec/cronograma-de-fatias.md`), e ela atende
identificadores **novos** — `RF-09-129` a `RF-09-131`, `RN-09-50` e `RN-09-51` —, criados na
revisão do PRD-09 que entra nesta change, aplicando a decisão do fundador de 2026-11-03
(documento 09 §1, documentos 02 §4 e 11 §2.2).

O desafio prático é hoje **só um enunciado em texto livre**: `Missao` guarda
`tipo_do_desafio_de_desbloqueio` e `desafio_de_desbloqueio_enunciado`, e nada mais. Com o
portfólio passando a ser o acervo, falta no prático tudo o que o acervo precisa — **que forma
de comprovação** o Mestre aceita, **sob que critério** ele vai julgar e **que título** a
vitrine exibe ao lado do nick. Sem esta fatia, a entrega da comprovação (fatia 13 do PRD-05)
não tem contra o que validar, a bancada do julgamento (fatia 27) não tem critério a exibir e a
linha do portfólio (fatia 12 do PRD-03) não tem título — as três dependem dela.

## What Changes

- **O desafio prático passa a declarar a forma de comprovação aceita** — **uma** entre as
  seis formas de entrega do Guerreiro(a): texto, imagem, áudio, vídeo, arquivo e link externo
  (documento 02 §4). (`RF-09-129`)
- **Passa a declarar o critério de aceite**, em texto livre, que diz ao Guerreiro(a) o que
  precisa aparecer na comprovação e o que não pode. (`RF-09-130`)
- **Passa a declarar um título curto**, campo **próprio** e distinto do enunciado, com no
  máximo **60 caracteres**. (`RF-09-131`, `RN-09-51`)
- **Declarar prático passa a exigir os três campos**, com recusa por campo que falta; o quiz
  NEVER SHALL recebê-los. (`RN-09-50`)
- **A App 09 ganha os três campos no bloco do desafio de desbloqueio**, apresentados só
  quando o tipo escolhido é prático, e os reabre ao Mestre autor pela leitura que já existe.
- Migração Alembic: três colunas **anuláveis** em `missao`. O prático declarado antes desta
  change segue valendo e fica incompleto até o Mestre autor redeclará-lo (decisão do fundador
  de 2026-11-04).
- Revisão do **PRD-09** com os cinco identificadores novos, nas §§6.4, 7, 8, 9 e 15.

**Fora do escopo** — é fatia das outras, e está nomeado para não ser suposto: a **entrega da
comprovação** pelo Guerreiro(a) e o aviso da mídia guardada (fatia 13 do PRD-05); os **dois
vereditos**, o motivo e os **5 pontos** (fatia 27 do PRD-09); a **linha do portfólio** com
nick e título (fatia 12 do PRD-03). Segue valendo o que o PRD-09 §3.2 já exclui, em especial
as **telas do Guerreiro(a)**, que são da App 05.

## Capabilities

### New Capabilities

Nenhuma. A fatia amplia capacidades existentes.

### Modified Capabilities

- `desbloqueio-da-missao`: a declaração do desafio prático deixa de ser só o enunciado e passa
  a exigir a forma de comprovação aceita, o critério de aceite e o título curto, com as
  recusas de cada um.
- `area-do-mestre`: o bloco do desafio de desbloqueio na App 09 passa a pedir, apresentar e
  reabrir os três campos do prático.

## Impact

- **Núcleo**: `trilhas/` — `modelo.py` (três colunas em `Missao`), `regra.py`
  (`declarar_desafio_de_desbloqueio`), `rotas.py` (entrada e saídas que já carregam o
  enunciado do prático).
- **Contratos**: `POST /v1/missoes/{id}/desbloqueio` passa a exigir três campos no prático —
  **BREAKING** para quem declara prático com o corpo de hoje, e o único cliente é a App 09,
  que entra na mesma change. `GET /v1/trilhas/minhas`, a leitura pública da trilha e a do
  percurso passam a devolvê-los.
- **Dados**: migração Alembic, três colunas anuláveis em `missao`.
- **Aplicações**: só a **App 09**. A App 05 e a App 01 leem os campos novos nas fatias delas.
- **PRD-09**: identificadores novos a partir de `RF-09-129` e `RN-09-50`, livres hoje. A §14
  não tem pendência que trave esta fatia.
- **Documentação**: a decisão já está nos documentos 02 §4, 11 §§2.2, 5 e 8.2, 99 §6 e 09 §1 —
  esta change não a reescreve. Revisa o **PRD-09** e fecha a linha 26 do cronograma.
