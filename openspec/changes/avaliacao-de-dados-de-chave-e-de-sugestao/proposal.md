## Why

**Origem: PRD-02**, com `RF-02-25`, `RF-02-26`, `RF-02-77`, `RF-02-78`, `RF-02-79`, `RF-02-87`,
`RF-02-88`, `RF-02-89`, `RF-02-93` (o de §6.2) e, em leitura, `RF-02-90` a `RF-02-92`. Do
núcleo, atende `RF-01-25`, `RF-01-46`, `RF-01-47`, `RF-01-49`, `RN-01-48`, `RN-01-49` e
`RN-01-50`.

Completa a fila de avaliação nas três naturezas que a fatia
`avaliacao-da-participacao-e-do-pre-cadastro` deixou: **dados**, **chave** e **sugestão**. Como
lá, a regra está escrita e testada em `backend/src/nucleo/fila/regra.py` — `avaliar_
solicitacao_de_dados`, `avaliar_solicitacao_de_chave`, `avaliar_sugestao` e
`liberar_conjunto_de_dados` — e nenhum chamador em produção a alcança.

Duas consequências passam despercebidas até se olhar o encadeamento:

**O ciclo de vida inteiro da chave de terceiro está morto.** `POST /chaves` recusa emitir se a
solicitação não estiver **aceita** (`emitir_chave_de_terceiro`, `RF-01-50`, `RN-01-51`), e
nenhuma rota consegue gravar essa situação. A change `ciclo-de-vida-da-chave-de-terceiro`
entregou emissão, prazo de apresentação, revogação por decurso e revogação por Admin — tudo
inalcançável, porque falta o degrau anterior. Esta fatia é o degrau.

**A sugestão adotada credita 20 pontos extras e o badge de protagonismo** na mesma operação,
idempotente pela marca `creditado_em` (`RF-01-56`, `RN-01-50`). Hoje nenhuma persona das Apps
05, 07, 08 e 09 recebe retorno de nada que proponha.

## What Changes

- **`GET /solicitacoes-de-dados`** e **`POST /solicitacoes-de-dados/{id}/avaliacao`**: fila com
  solicitante, instituição, finalidade declarada e recorte pedido; desfecho de Admin com
  parecer obrigatório e o **compromisso de não reidentificação** afirmado no ato, que a regra
  já exige na aprovação (`RF-02-77`, `RF-02-78`, `RF-02-93`, `RN-01-48`).
- **Registro do que foi entregue e a quem** (`RF-02-79`), pela guarda `liberar_conjunto_de_
  dados`: nenhum conjunto sai sem aprovação de Admin registrada. A **geração do arquivo** é do
  PRD-08 e não entra aqui.
- **`GET /solicitacoes-de-chave`** e o **desfecho da solicitação de chave**, que destrava
  `POST /chaves` (`RF-02-87`, `RF-02-88`, `RF-02-89`).
- **`GET /sugestoes`** e **`POST /sugestoes/{id}/avaliacao`**: fila única das Apps 05, 07, 08 e
  09, com autor e persona; adotada credita os 20 extras e o badge, não adotada exige o motivo
  do retorno em linguagem simples e marca a data de descarte da transcrição (`RF-02-25`,
  `RF-02-26`).
- **As três naturezas na área "Filas" da App 03**, sob o filtro por natureza que a fatia
  anterior criou, com o **atraso de 7 dias** derivado em todas (`RF-02-65` já entregue,
  `RN-01-49`).
- **Painel das chaves emitidas** na App 03, sobre o `GET /chaves` que já existe: prazo de
  apresentação, URL apresentada, situação, destaque das que estão a vencer e das revogadas por
  decurso, e a revogação com motivo (`RF-02-90`, `RF-02-91`, `RF-02-92`). O segredo aparece
  **uma única vez**, na emissão (`RN-02-28`).

Nenhuma rota de escrita existente muda. `POST /chaves`, `DELETE /chaves/{id}`, `GET /chaves`,
`POST /solicitacoes-de-dados`, `POST /solicitacoes-de-chave` e `POST /sugestoes` ficam como
estão.

### O que fica para depois — e por quê

Nada disto é exclusão nova: o PRD-02 §3.1 mantém tudo em escopo, e a fatia apenas não alcança.

| Adiado                                          | Trava                                                       |
| ----------------------------------------------- | ----------------------------------------------------------- |
| Geração do conjunto de dados entregue           | é do PRD-08; aqui fica só a guarda e o registro da entrega  |
| Solicitações do responsável (`RF-02-23`, `-24`) | não existe entidade no núcleo — é PRD-13, App 07           |
| Solicitação de novo local (`RF-02-21`, `-22`)   | núcleo pronto e roteado; falta só tela — fatia própria     |
| Desafios extras (`RF-02-27`, `RF-02-28`)        | espera a entidade `DesafioExtra`, do PRD-09 ou do PRD-14   |
| Conteúdo institucional da vitrine (`RF-02-80`)  | é superfície de PRD-03, não da fila                        |

### Perguntas ao fundador, antes do `/opsx:apply`

1. **O PRD-02 §9 não declara a rota de desfecho da solicitação de chave.** A tabela traz
   `GET /v1/solicitacoes-de-chave` e `POST /v1/chaves`, mas o `RF-02-88` exige *aprovar ou
   recusar, com parecer e autoria* — e a recusa não tem para onde ir, já que `POST /v1/chaves`
   só emite. As outras três naturezas têm `POST .../{id}/avaliacao`. A leitura simétrica é
   acrescentar `POST /v1/solicitacoes-de-chave/{id}/avaliacao` à §9; a alternativa é a
   aprovação ser o próprio `POST /v1/chaves` e a recusa entrar por rota separada. **É correção
   de PRD, não decisão de artefato** — precisa da sua palavra antes de virar código.

2. **`RF-02-93` está duplicado** (§6.2 linha 222 e §6.5 linha 304, enunciados diferentes; a §15
   rastreia só o primeiro). Esta fatia implementa o de §6.2 — o critério de aprovação da
   solicitação de dados. O de §6.5, sobre a amostra semanal de coleta, precisa de identificador
   próprio.

## Capabilities

### New Capabilities

Nenhuma.

### Modified Capabilities

- `fila-de-avaliacao`: as naturezas **dados**, **chave** e **sugestão** ganham **superfície de
  leitura e de desfecho**, fechando o que a fatia anterior abriu para participação.
- `chave-de-aplicacao`: o desfecho da solicitação passa a ter porta, e com ele a emissão da
  chave de terceiro deixa de ser inalcançável. Requisito de leitura e revogação pela gestão,
  hoje especificado e sem consumidor.
- `aplicacao-de-gestao`: a área Filas passa a servir as quatro naturezas, e a App 03 ganha o
  **painel das chaves emitidas**.

## Impact

**Backend** — só adição, nenhuma migração:

- `backend/src/nucleo/fila/rotas.py` — as três rotas de leitura e as três de desfecho
- `backend/src/nucleo/fila/regra.py` — `avaliar_solicitacao_de_dados`,
  `avaliar_solicitacao_de_chave`, `avaliar_sugestao` e `liberar_conjunto_de_dados` passam a ser
  consumidas, não alteradas
- `backend/src/nucleo/chaves/rotas.py` — nenhuma alteração; `POST /chaves` passa a ser
  alcançável

**App 03** — `apps/app-03-gestao/`: três naturezas na área Filas e o painel de chaves.

**Documentação** — o PRD-02 §9 e o `RF-02-93` mudam conforme as respostas às duas perguntas
acima; enquanto não houver resposta, as pendências ficam no documento 09 §1.
