# Culminância e publicação da trilha

Origem: **PRD-09 — Área do Mestre**, §6.1 e §6.4 (parcial). Segunda fatia do PRD-09.

Atende `RF-09-05` a `RF-09-11`, `RF-09-29`, `RF-09-30` e `RF-09-82`, sob `RN-09-01`,
`RN-09-02`, `RN-09-03`, `RN-09-05` e `RN-09-29`.

## Why

A primeira fatia abriu a porta da autoria e o Mestre escreve trilha, missão e atividade — mas
a trilha **nunca sai do rascunho**. Não existe `POST /v1/trilhas/{id}/publicacao`, e
`SituacaoDaTrilha` só conhece `rascunho` e `publicada`. Tudo a jusante espera: o
`GET /v1/trilhas/{id}` público do §9, a App 05, a App 01. O que a App 09 escreve hoje é
invisível para o resto da plataforma.

Publicar exige três travas (`RF-09-06`, `RF-09-07`, `RF-09-82`) — que são a forma executável
do invariante 5 do documento 99 §6. Duas já têm com o que conferir: `Missao.e_sondagem` e
`DesafioDeColeta.missao_id`. A terceira não: a `Culminancia` é uma das cinco entidades que o
PRD-09 §8 declara e **nenhuma fatia criou**. Sem ela, a trava do `RF-09-07` só teria duas
saídas — recusar toda publicação para sempre, ou não implementar a trava. Culminância e
publicação são, por isso, uma fatia só.

## Decisões novas do fundador — 2026-08-22

Ambas gravadas no documento 03 §11 (fonte única da publicação e curadoria da trilha) e
movidas no documento 09 antes do código.

1. **A situação da trilha tem três valores** — `rascunho`, `publicada`, `despublicada` —,
   confirmando o PRD-09 §8 e fechando a pendência levantada pela fatia anterior. O
   `RF-09-11` recebe correção de redação: a trilha despublicada **volta a ser editável, como
   rascunho**, sem que o estado vire `rascunho`.
2. **A republicação é do Mestre autor**, pela mesma rota e pelas mesmas três travas. O motivo
   que o Admin registra existe para o Mestre corrigir e voltar ao ar; laço de correção sem
   saída contrariaria `RN-09-01` e o `RF-09-05`.

## What Changes

### A culminância da trilha (PRD-09 §6.4, §8)

Entidade nova `Culminancia` — trilha, descrição da criação original esperada, modalidade
(individual ou em equipe) e critério de validação —, **uma por trilha**, declarada pelo Mestre
autor em `POST /v1/trilhas/{id}/culminancia` (`RF-09-29`, `RF-09-30`).

A `CriacaoOriginal` continua apontando para `trilha_id`, sem coluna nova: com uma culminância
por trilha, a referência do PRD-09 §8 já se resolve pela trilha.

### O ciclo de publicação (PRD-09 §6.1)

| Rota                                    | Persona     | Atende                                     |
| --------------------------------------- | ----------- | ------------------------------------------ |
| `POST /v1/trilhas/{id}/culminancia`     | Mestre autor| `RF-09-29`, `RF-09-30`                     |
| `POST /v1/trilhas/{id}/publicacao`      | Mestre autor| `RF-09-05` a `RF-09-09`, `RF-09-82`        |
| `POST /v1/trilhas/{id}/despublicacao`   | Admin       | `RF-09-10`, `RF-09-11`                     |
| `GET /v1/trilhas/{id}`                  | pública     | `RF-09-09`                                 |

`SituacaoDaTrilha` ganha `despublicada`, e a `Trilha` os quatro campos de procedência do
padrão que a change `desativacao-do-ponto-de-apoio` firmou no `PontoDeApoio` — motivo, autor,
papel do autor e momento. `GET /v1/trilhas/minhas` passa a devolver o motivo, que é o caminho
pelo qual o Mestre autor o lê (`RF-09-10`).

A publicação aceita `rascunho` **e** `despublicada`, confere as três travas e recusa dizendo
em linguagem simples exatamente o que falta (`RF-09-08`). Não confere lastro de recompensa de
marco: `RN-09-27` o exige na entrega, nunca na publicação.

### A App 09 (PRD-09 §4, §6.1)

Tela da culminância dentro da trilha, ação de publicar com a recusa detalhada do `RF-09-08`, e
a situação de cada trilha com o motivo da despublicação visível ao autor.

## Capabilities

### New Capabilities

- `culminancia`: o que a criação original de uma trilha precisa ser — descrição esperada,
  modalidade e critério de validação —, uma por trilha, declarada pelo Mestre autor. Irmã de
  `criacao-original`, que trata da entrega e da validação.

### Modified Capabilities

- `trilha-e-missao`: a situação passa de dois para **três** valores; nascem a publicação com
  as três travas, a despublicação motivada de Admin e a republicação pelo Mestre autor; a
  trilha ganha a procedência da mudança de situação.
- `area-do-mestre`: a App 09 ganha a declaração da culminância, a publicação com recusa
  detalhada e a leitura do motivo da despublicação.

## Impact

| Onde                                                | O quê                                        |
| --------------------------------------------------- | -------------------------------------------- |
| `backend/src/nucleo/culminancias/`                  | módulo novo — `modelo.py`, `regra.py`, `rotas.py` |
| `backend/src/nucleo/trilhas/modelo.py`              | `despublicada` e quatro colunas de procedência, com migração Alembic |
| `backend/src/nucleo/trilhas/regra.py`               | publicar, despublicar e as três travas       |
| `backend/src/nucleo/trilhas/rotas.py`               | três rotas novas; `minhas` devolve o motivo  |
| `backend/src/nucleo/principal.py`                   | registro do roteador                         |
| `apps/app-09-mestre/src/`                           | culminância, publicar e situação da trilha   |
| `docs/03-plataforma-e-arquitetura.md` §11           | as duas decisões novas                       |
| `docs/09-topicos-em-aberto-e-sugestoes.md`          | pendência movida para "Já decididos"         |
| `docs/prds/prd-09-area-do-mestre.md`                | `RF-09-11` e `RF-09-05` ajustados às decisões; §14 |
| `docs/prds/index.md`                                | a segunda fatia do PRD-09                    |

Destrava o `GET /v1/trilhas/{id}` público e, com ele, o consumo da trilha pela App 05 e pela
App 01.

## Fora do escopo

O PRD-09 §3.2 já exclui o que não é do Ciclo 01. Esta fatia recorta ainda, dentro do que o
PRD inclui:

| O quê                                        | Por quê                                          |
| -------------------------------------------- | ------------------------------------------------ |
| Etiqueta ODS declarada pelo Mestre           | `RF-09-92` a `-98`; rotas próprias no §9, fatia curta seguinte |
| Edição e versão de trilha publicada          | nenhum `RF` do §6.1 a cobre; decisão do fundador em 2026-08-22 |
| Duplicar trilha (`RF-09-13`)                 | desejável, não essencial                         |
| Desafio de desbloqueio (`RF-09-26`)          | PRD-09 §6.4, entidade própria                    |
| Validação da criação original (`RF-09-31`)   | PRD-09 §6.4; `criacoes_originais/regra.py` já a tem, falta a porta |
| Tela de despublicação na App 03              | pendência abaixo                                 |

## Pendências — decisão do fundador

Não travam esta fatia; a primeira decide quando a despublicação ganha tela.

1. **`RF-02-71` continua sem rota**, e agora trava um segundo item. A despublicação é ato de
   Admin, logo da App 03 — mas a App 03 não tem por onde listar a trilha de um Mestre, porque
   o PRD-02 §9 não declara rota de leitura da autoria e o `GET /v1/trilhas/{id}` do PRD-09 é
   público e serve só trilha publicada. A rota de despublicação entrega testada, sem tela, até
   a pendência ser decidida.
2. **Trilha publicada é imutável até esta fatia ser sucedida.** Com a edição fora do escopo, o
   Mestre que encontrar um erro na própria trilha publicada depende de um Admin despublicá-la.
   Registrado no documento 09 como consequência conhecida, não como defeito.
