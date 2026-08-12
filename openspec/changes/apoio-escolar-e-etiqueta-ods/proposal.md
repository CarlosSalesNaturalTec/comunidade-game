## Why

**PRD de origem:** PRD-01 — Backend API (núcleo). Oitava fatia, na ordem do documento 99 §9.

**Requisitos atendidos:** `RF-01-35` (parcial — disciplina e conteúdo do corpus), `RF-01-40`,
`RF-01-42`, `RF-01-45`, `RN-01-23`, `RN-01-24`.

Duas frentes independentes do que resta do PRD-01, ambas livres das pendências que travam o
resto da esteira (território, culminância, `Aula/Agenda`, rota pública).

**Apoio escolar** (documento 03 §7): o núcleo guarda o corpus fechado que o assistente de voz
vai consultar — disciplina e conteúdo, cadastrados pelos Mestres. O PRD-01 §4 já concede essa
escrita: "Mestre: suas trilhas **e conteúdos**" é a mesma operação que a trilha usa.

**Etiqueta ODS** (documento 11 §2.1): o Mestre autor declara quais Objetivos de Desenvolvimento
Sustentável a trilha toca, opcionalmente por missão, e o núcleo agrega a cobertura. É rótulo
descritivo — `RN-01-23` — que não pesa no motor de pontuação que a sexta e a sétima fatias já
entregaram.

## What Changes

### Apoio escolar

- Nasce a **Disciplina**: catálogo aberto, cadastrado por qualquer Mestre, único por nome
  normalizado — no padrão da natureza da atividade (quarta fatia), para não duplicar "Matemática"
  e "matemática" como disciplinas diferentes (`RF-01-35`, `RF-01-03`).
- Nasce o **Conteúdo do corpus**: pertence a exatamente uma disciplina, com o material e a
  autoria do Mestre que o escreveu. Só o **Mestre autor** altera o próprio conteúdo — a mesma
  posse que já vale para trilha, missão e atividade —, e o **Admin** alcança qualquer um para
  **despublicar com motivo**, como já faz com a trilha (`RF-01-35`, `RF-01-16`, `RF-01-03`,
  03 §7).
- Escrita de Disciplina e Conteúdo usa a operação `suas_trilhas_e_conteudos`, já concedida ao
  Mestre desde a fundação — nenhuma entrada nova na matriz.

### Etiqueta ODS

- Nasce a **Etiqueta ODS**: objetivo de 1 a 18, com meta opcional em texto (`4.7`, `13.3`), presa
  a uma trilha **ou** a uma missão — nunca as duas —, declarada pelo Mestre autor. Uma trilha
  aceita mais de uma etiqueta; a mesma vale para missão (`RF-01-40`, `RF-01-45`, 11 §2.1).
- A etiqueta de missão **prevalece sobre a da trilha** nos vínculos dela — regra que a próxima
  fatia a usar (desafio de coleta, desafio extra) aplica; aqui nasce o dado (`RF-01-45`).
- A etiqueta **não pontua e não é poder**: nenhum caminho do núcleo a liga a ponto, nível ou
  badge (`RN-01-23`).
- Nasce a **agregação de cobertura**: por trilha, por poder e por comunidade — a soma dos
  objetivos distintos que as etiquetas declaram, sem lançamento manual (`RF-01-42`, `RN-01-24`).
  A dimensão **ciclo** não entra ainda: o núcleo não modela mais de um ciclo hoje, e agregar por
  um ciclo único é agregar por tudo — a dimensão fica pronta para quando o Ciclo 02 exigir o
  corte.

### O que esta fatia não tem, e não é omissão

**A Consulta** — a terceira entidade de `RF-01-35` — fica de fora. Ela registra pergunta,
resposta e o desfecho do assistente de voz, mas **nada a produz ainda**: o assistente em si
(App 05/01, chamada ao Gemini) não está construído, e o custo dele depende do livro-razão
(PRD-07). Mais que isso, o prazo de guarda dela é ativo, não só de saída — "7 dias vinculada ao
Guerreiro(a), depois só disciplina e data" (documento 03 §12.2) apaga o vínculo e a transcrição,
não apenas anonimiza na leitura. O núcleo não tem hoje nenhum mecanismo de expurgo automático por
prazo — nem a chave de terceiro, que precisaria do mesmo tipo de rotina (`RF-01-52`), o tem — e
inventar esse mecanismo agora, sem produtor para testá-lo, seria desenhar para requisito
hipotético. Fica para quando o assistente nascer.

**A trava de publicação sem etiqueta a partir do Ciclo 02** (`RF-01-44`) fica de fora: publicar é
rota do PRD-09, como a sondagem e a culminância já são (quinta e sétima fatias); o núcleo hoje
só tem uma trilha em rascunho e publicada, sem versão de ciclo por trilha, e o Ciclo 01 corrente
não a exige.

**A propagação da etiqueta para desafio de coleta e desafio extra** (`RF-01-41`) fica de fora:
os dois alvos são entidades do PRD-08 e do PRD-14/PRD-02, que ainda não existem.

**A rota pública de cobertura** (`RF-01-43`) fica de fora, pela mesma pendência "Números da
proteção das rotas públicas" do documento 09 que já travava `RF-01-33`/`RF-01-34` desde a quarta
fatia — a agregação nasce como função de consulta, sem rota.

**Resposta de quiz, equipe e quiz ao vivo** (`RF-01-36` a `RF-01-39`) seguem fora: dependem de
`Aula/Agenda`, que nenhuma fatia construiu ainda.

### Fora do escopo

O que o PRD-01 §3.2 já exclui: interface de qualquer aplicação; a chamada ao modelo Gemini e os
filtros de segurança do assistente; captura da imagem, conversa de cadastro e geração do
descritor no aparelho; exclusão do _template_; telemetria da Batalha de Laser e personalização
por IA.

O que é do PRD-01 mas de outra fatia, por dependência declarada ou por pendência aberta:

| Fica para                              | Porque                                                          |
| --------------------------------------- | ---------------------------------------------------------------- |
| `Consulta` (resto de `RF-01-35`)        | sem produtor ainda; prazo de guarda ativo sem mecanismo de expurgo automático no núcleo |
| `RF-01-36` a `RF-01-39`                 | pendem de `Aula/Agenda`, da fatia da operação da aula            |
| `RF-01-41`                               | os alvos (desafio de coleta, desafio extra) são do PRD-08/PRD-14 |
| `RF-01-43`                               | documento 09, "Números da proteção das rotas públicas"           |
| `RF-01-44`                               | trava de publicação, rota do PRD-09, e o Ciclo 01 não a exige    |
| `RF-01-23` a `RF-01-26` (exceto 26, já entregue), `RF-01-29`, `RF-01-46`, `RF-01-47` | território, ledger, fila de avaliação e auditoria |
| `RF-01-49` a `RF-01-53`, `RF-01-55`     | documento 09, "Números da proteção das rotas públicas"           |

## Capabilities

### New Capabilities

- `apoio-escolar`: a disciplina como catálogo aberto cadastrado por qualquer Mestre e o conteúdo
  do corpus, autorado por um Mestre e sujeito à despublicação por Admin.
- `etiqueta-ods`: a etiqueta ODS presa a uma trilha ou a uma missão, opcional e sem peso no motor
  de pontuação, e a agregação de cobertura por trilha, poder e comunidade.

### Modified Capabilities

Nenhuma. `trilha-e-missao` não muda de requisito: a etiqueta é entidade própria que referencia
trilha ou missão por chave estrangeira, sem alterar o comportamento delas.

## Impact

- `backend/src/nucleo/`: módulos novos `apoio_escolar/` (Disciplina, Conteúdo e regra de posse) e
  `ods/` (Etiqueta e a agregação de cobertura), lendo `trilha`, `missao`, `poder`, `resultado` e
  `persona` já existentes.
- `backend/alembic/`: migração para `disciplina`, `conteudo_do_corpus` e `etiqueta_ods`.
- Nenhuma rota nova sob `/v1`: como as fatias 5 a 7, entidade e regra, sem rota de gestão — as
  rotas de cadastro do corpus são do PRD-09/PRD-05, e a rota de cobertura pública é da fatia da
  vitrine.
- `docs/`: nenhuma decisão nova nesta fatia — a régua de ODS já está no documento 11 §2.1 e a do
  apoio escolar no documento 03 §7. `docs/prds/index.md` recebe a situação atualizada se ela
  mudar ao fim da implementação.
