## Context

Ver `proposal.md` — Why. O que o desenho precisa saber do que já existe:

- `Atividade` pertence a uma `Missao`, que pertence a uma `Trilha`, e a matriz de posse é do
  **Mestre autor** da trilha (capacidade `atividade-de-trilha`).
- A `Aula` é agendada por Admin e não conhece trilha, missão nem atividade (`aula-e-presenca`).
- `Equipe` tem dois tempos de vida; a **da aula** aponta para a aula e encerra com ela
  (`equipe`).
- O conteúdo e a bibliografia da missão já são servidos, mas só pela leitura da **trilha
  publicada** (`conteudo-da-missao`, `bibliografia-da-missao`).
- A App 01 já abre a sessão de trabalho pela aula vigente, entra o Guerreiro(a) por nick e
  imagem e forma equipe (`aplicacao-da-aula-presencial`).

O vínculo que falta é um só: **atividade → aula**. Todo o resto desta fatia é derivação.

## Goals / Non-Goals

**Goals:**

- Um vínculo declarado, anulável, sem tabela nova.
- A programação do encontro derivada por consulta, nunca materializada.
- A App 01 lendo por uma rota só, para não somar chamadas em rede instável.

**Non-Goals:**

- Estado de progressão de qualquer espécie — ver `proposal.md` — Fora do escopo.
- Reordenar ou paginar a programação: um encontro tem poucas atividades.

## Decisions

**A coluna vai na `Atividade`, não numa tabela de ligação.** Uma atividade acontece em um
encontro; um encontro tem várias atividades. É 1–N, e `aula_id` anulável em `atividade`
resolve. _Alternativa descartada:_ tabela `programacao_do_encontro`, que traria cardinalidade
N–N que ninguém pediu.

**O formato presencial é a trava do vínculo.** Recusar `aula_id` em atividade on-line ou
assíncrona mantém a separação que o `RF-09-73` já exigia e evita que a programação do encontro
traga o que corre entre encontros. _Alternativa descartada:_ aceitar em qualquer formato e
filtrar só na leitura, que deixaria o dado incoerente no banco.

**A programação sai numa rota só, `GET /v1/equipes/{id}/missao`.** É a rota que o PRD-04 §9 já
declara. Ela resolve equipe → aula → atividades presenciais → missão → conteúdo e bibliografia,
e devolve tudo montado. _Alternativa descartada:_ a App 01 encadear
`equipe → aula → atividades → trilha` em quatro chamadas, o que multiplica a exposição à queda
de rede que o `RF-04-58` cobra.

**A trava de publicação é reusada, não reescrita.** A leitura filtra por trilha **publicada**,
mesma condição que `conteudo-da-missao` já aplica na leitura pública. `trilhas/regra.py` não é
tocado — as três travas de publicação continuam sendo as únicas.

**A guarda da rota é a integrância na equipe.** Menor privilégio, coerente com as rotas
`eu`-escopadas que o núcleo já tem, e o fluxo da App 01 sempre passa pela equipe escolhida. Não
é regra de produto: é a porta certa para uma rota chaveada por equipe.

**A escolha entre atividades é estado do aparelho.** Mesmo desenho da fatia
`aparelho-da-equipe-no-quiz`, em que o vínculo aparelho–equipe ficou no aparelho: a equipe da
aula morre com a aula (documento 02 §5) e não guarda percurso.

## Risks / Trade-offs

- **Atividade vinculada a aula já realizada ou cancelada** → sem risco na App 01, que só opera
  dentro da janela da aula vigente (`RF-04-02`) e nunca alcança encontro encerrado. Não se cria
  guarda que o PRD não pede.
- **Encontro sem programação declarada** → o Mestre esquecer de vincular deixaria a equipe sem
  o que fazer. Mitigado no aviso em linguagem simples da App 01 e na leitura de turmas do
  Mestre, que passa a mostrar a atividade ainda sem encontro.
- **Peso do conteúdo da missão em rede instável** → a rota devolve conteúdo, não bytes de
  vídeo e arquivo, que seguem no armazenamento; o que já carregou permanece legível.

## Migration Plan

Uma migração Alembic: `aula_id` anulável em `atividade`, com chave estrangeira para `aula` e
índice. Nenhum registro existente é preenchido — atividade anterior à fatia fica sem encontro,
como o `RF-09-73` já a trataria. Reversão é o `drop` da coluna, sem perda de dado de outra
natureza.
