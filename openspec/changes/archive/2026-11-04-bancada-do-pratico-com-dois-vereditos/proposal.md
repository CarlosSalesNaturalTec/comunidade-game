# Proposal

## Why

É a **fatia 27 do PRD-09** (`openspec/cronograma-de-fatias.md`), e ela atende identificadores
**novos** — `RF-09-132` a `RF-09-135`, `RN-09-52` a `RN-09-55` e `RF-05-94` —, criados na
revisão do PRD-09 e do PRD-05 que entra nesta change, aplicando a decisão do fundador de
2026-11-03 (documento 09 §1, documentos 02 §4 e 11 §§2.2 e 5).

A bancada de "Desafios práticos a julgar" mostra hoje **nick, missão e hora** e mais nada: o
Mestre julga às cegas o que não vê. A fatia 13 do PRD-05 já pôs a comprovação e o critério de
aceite na resposta de `GET /v1/missoes/desbloqueios-pendentes`, e nenhuma tela os desenha.

E o julgamento é um **booleano**: `JulgarDesafioPraticoEntrada` tem só `aprovado`. Com o
portfólio passando a ser o acervo, um campo só obriga o Mestre a escolher entre dois erros —
reprovar quem cumpriu mas enquadrou mal, ou publicar o rosto da criança. Falta ainda o crédito
que o documento 11 §5 já declara ("Comprovação do desafio prático de desbloqueio — 5 —
Regular — Mestre autor, ao julgar") e que nenhuma via do núcleo executa.

## What Changes

- **A bancada exibe a produção entregue** e o **critério de aceite** que o próprio Mestre
  declarou, ao lado do Guerreiro(a), da missão e do momento, abrindo a mídia pela rota de bytes
  que a fatia 13 criou. (`RF-09-132`)
- **O julgamento passa a ter dois vereditos** — **cumpriu**, que abre a missão seguinte, e
  **publicável**, que leva ou não a entrega à vitrine. (`RF-09-133`)
- **Publicável só é aceito sobre entrega cumprida e com comprovação gravada**: na entrega
  presencial e na reprovação é recusado com **422** (decisão do fundador de 2026-11-04).
  (`RN-09-52`)
- **O julgamento registra o motivo em linguagem simples**, **exigido em todo veredito
  negativo** — não cumpriu, ou cumpriu e não publicável —, pelo precedente da devolução da
  criação original (decisão do fundador de 2026-11-04). (`RF-09-134`, `RN-09-53`)
- **BREAKING — a reprovação deixa de apagar a declaração**: ela fica gravada com o veredito e o
  motivo, e entregar de novo **reabre a mesma linha** para julgamento, substituindo a
  comprovação. Sem isso o motivo seria apagado no mesmo ato em que nasce, e a criança nunca o
  leria (decisão do fundador de 2026-11-04). **Reverte** o `RN-05-52` e o requisito do
  apagamento em `desbloqueio-da-missao`. (`RN-09-54`)
- **Julgar que cumpriu credita 5 pontos regulares** à trilha da missão, uma vez por par
  Guerreiro(a)–missão. **Reverte** o `NEVER SHALL` de `desbloqueio-da-missao` — "o desbloqueio
  NEVER SHALL creditar pontos por si" — e abre a **segunda via de crédito** ao lado do Resultado
  lançado pelo Mestre. Sem retroatividade: o já julgado antes desta regra não recebe crédito
  (decisão do fundador de 2026-11-04). (`RF-09-135`, `RN-09-55`)
- **O veredito e o motivo chegam ao Guerreiro(a)**: o percurso passa a devolvê-los e a tela do
  prático os apresenta, com o convite a entregar de novo em linguagem acolhedora — nada sai
  *write-only*, a lição das quatro linhas de conserto do bloco do PRD-09 (decisão do fundador
  de 2026-11-04). (`RF-05-94`)
- Migração Alembic: `aprovado` vira os dois vereditos e nascem o motivo e o momento do
  julgamento em `desbloqueio_da_missao`, em colunas **anuláveis** e sem *backfill*.
- Revisão do **PRD-09** (§§6.4, 7, 9, 15) com os oito identificadores novos, e do **PRD-05**
  com o `RF-05-94` e o enunciado do `RN-05-52`, que a decisão reverte.

**Fora do escopo** — é fatia de outras, e está nomeado para não ser suposto: a **linha do
portfólio** com nick + título e a **vitrine** abrindo a produção aprovada (fatia 12 do PRD-03),
que é quem lê o `publicavel` daqui; a **conclusão do desafio extra** (fatia 23); o **badge de
autoria**, que o documento 02 §4 mantém só na culminância; e o **nível**, que é percurso e não
se move por ponto (documento 09 §1). Segue valendo o que o PRD-09 §3.2 já exclui.

## Capabilities

### New Capabilities

Nenhuma. A fatia amplia capacidades existentes.

### Modified Capabilities

- `desbloqueio-da-missao`: o julgamento do prático deixa de ser um booleano e passa a dois
  vereditos com motivo; a reprovação para de apagar a declaração; e o desbloqueio passa a
  creditar ponto, o que o requisito de hoje proíbe.
- `area-do-mestre`: a bancada passa a exibir a produção entregue e o critério, e a julgar pelos
  dois vereditos com o motivo.
- `area-do-guerreiro`: a tela do prático passa a apresentar o veredito do Mestre e o motivo, e
  a entrega deixa de se encerrar na reprovação.
- `pontos-niveis-e-badges`: o ponto regular ganha a **quinta fonte** — o desafio prático julgado
  como cumprido —, ao lado do Resultado, da criação original, da partida de quiz e do registro
  de coleta.

**`livro-razao` não entra**, embora a linha 27 do cronograma o preveja: a capacidade é o
registro contábil de **recursos e moedas** e não trata de ponto regular, que é inteiramente de
`pontos-niveis-e-badges`. Era estimativa de planejamento, e esta change corrige a linha
(decisão do fundador de 2026-11-04).

## Impact

- **Núcleo**: `trilhas/` — `modelo.py` (`DesbloqueioDaMissao`), `regra.py`
  (`julgar_desafio_pratico`, `listar_desbloqueios_praticos_pendentes`, `derivar_percurso`,
  `declarar_cumprimento_do_pratico`), `rotas.py` (entrada do julgamento e as saídas da bancada e
  do percurso); `pontuacao/regra.py` (a via de crédito nova).
- **Contratos**: `POST /v1/missoes/{id}/desbloqueios/{id}/julgamento` troca `aprovado` por
  `cumpriu`, `publicavel` e `motivo` — **BREAKING** sob `extra="forbid"`, e o único cliente é a
  App 09, que entra na mesma change. `GET /v1/missoes/desbloqueios-pendentes` e o percurso
  passam a devolver o veredito, o motivo e o momento do julgamento.
- **Dados**: migração Alembic em `desbloqueio_da_missao`, com as colunas anuláveis e sem
  *backfill*; nenhum saldo de ponto muda pela migração.
- **Aplicações**: **App 09** (a bancada) e **App 05** (a tela do prático, em `comum/trilha/`,
  que a App 05 consome).
- **PRDs**: identificadores novos a partir de `RF-09-132`, `RN-09-52` e `RF-05-94`, livres hoje;
  o `RN-05-52` muda de enunciado. A §14 dos dois PRDs não tem pendência que trave esta fatia.
- **Documentação**: a decisão já está nos documentos 02 §4, 11 §§2.2 e 5, 99 §6 e 09 §1 — esta
  change não a reescreve. Acrescenta ao documento 09 §1 a **quarta reversão**, que o entry de
  lá ainda conta como três, e fecha a linha 27 do cronograma.
