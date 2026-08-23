## Why

Origem: **PRD-09 — Área do Mestre**, §6.5, quinta fatia. Atende `RF-09-36`, `RF-09-37`,
`RF-09-38`, `RF-09-39` e `RF-09-40`.

O módulo `quiz` do núcleo está escrito e testado desde a change `quiz-ao-vivo` — 40 testes
cobrindo cadastro de pergunta, abertura de partida, resposta, anulação e encerramento com
crédito — e **não tem uma única rota**. O banco de perguntas do Mestre curador é hoje
inalcançável por HTTP: a App 09 não tem por onde cadastrar nem por onde listar. É a mesma
figura da change `etiqueta-ods-da-trilha-e-da-missao`, que abriu a porta de um módulo pronto
sem reescrever recusa alguma.

Além da porta, a fatia fecha duas lacunas do modelo. `PerguntaDeQuiz` não guarda o vínculo com
trilha e missão que o `RF-09-39` exige e de que o filtro do `RF-09-40` depende, embora o
PRD-09 §8 já os declare. E o §8 lista uma **situação** que nenhum requisito define — lacuna
levada ao fundador e decidida por ele em 2026-08-23.

## What Changes

- **`PerguntaDeQuiz` ganha `trilha_id` e `missao_id`** (`RF-09-39`, PRD-09 §8), com migração
  Alembic. A tabela está vazia: não há _backfill_.
- **`cadastrar_pergunta` passa a exigir e gravar o vínculo**, sem tocar nas recusas que já
  existem — quatro alternativas e alternativa correta declarada seguem como estão
  (`RF-09-36`, `RF-09-37`).
- **Leitura nova `perguntas_do_mestre`**, do banco do próprio Mestre, filtrável por trilha e
  por missão (`RF-09-40`), paginada pelas convenções do PRD-01.
- **Rotas novas**: `POST /v1/perguntas` e `GET /v1/perguntas/minhas` (PRD-09 §9).
- **A App 09 ganha a área "Banco do Quiz"** — cadastro com as quatro alternativas e a correta,
  e lista filtrável por trilha e missão.
- **Decisão nova do fundador, 2026-08-23: a `PerguntaDeQuiz` não tem situação.** A palavra sai
  da linha do PRD-09 §8. O documento 05 §5 nunca a previu, e a única transição concebível — a
  anulação — foi deliberadamente posta na partida (`PerguntaAnuladaNaPartida`), nunca na
  pergunta do banco, que serve a partidas diferentes. Não é regra nova: é o PRD voltando a
  aplicar a fonte, como já ocorreu com o responsável do `ItemPatrimonial` e com o ponto de
  apoio da `RecompensaDeMarco`.

## Capabilities

### New Capabilities

Nenhuma. O assunto já tem capacidade consolidada.

### Modified Capabilities

- `quiz-ao-vivo`: o requisito da pergunta de múltipla escolha passa a exigir o **vínculo com
  a missão e a trilha** a que ela se refere (`RF-09-39`) e ganha o requisito da **leitura do
  banco do Mestre**, filtrável por trilha e missão (`RF-09-40`). Fica explícito que a pergunta
  **não tem situação** e que a anulação segue sendo da partida.

## Impact

- **Núcleo**: `backend/src/nucleo/quiz/` — `modelo.py` (duas colunas), `regra.py`
  (`cadastrar_pergunta` e `perguntas_do_mestre`) e `rotas.py` (arquivo novo, registrado em
  `principal.py`). Uma migração Alembic.
- **App 09**: `apps/app-09-mestre/` — área "Banco do Quiz" e o cliente das duas rotas.
- **Documentação**: PRD-09 §8 (risca "situação"), documento 09 (linha nova em "Já
  decididos"), `docs/prds/index.md` (narrativa da quinta fatia).
- **Não toca** a partida: `abrir_partida`, `registrar_resposta`, `anular_pergunta` e
  `encerrar_partida` ficam como estão, sem rota.

## Fora do escopo

Reproduz o que o PRD-09 §3.2 já exclui, mais o limite desta fatia:

- **Condução da partida** — é da App 03 (PRD-02 §6.5), com o banco cadastrado aqui.
- **Responder ao quiz** — é tela do Guerreiro(a), na App 05 (PRD-05) e no App 01 (PRD-04).
- **`RF-09-41`** — "banco cadastrado fica disponível para a partida conduzida na App 03" só se
  verifica quando a condução tiver porta. A abertura de partida exige equipe **da aula**, e
  `criar_equipe` é restrita ao Guerreiro(a) (invariante 15): sem a App 01, não há quem forme
  equipe nem quem responda. O requisito segue nomeado como pendente, sem entrega fingida.
