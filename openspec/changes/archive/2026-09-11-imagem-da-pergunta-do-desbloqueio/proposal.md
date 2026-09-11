## Why

Fatia **19 do PRD-09** (`openspec/cronograma-de-fatias.md`). Atende `RF-09-119`, e alcança
`RF-09-118` e `RF-05-89`, já implementados na fatia 18.

A pergunta do quiz do desbloqueio só tem texto. Uma pergunta sobre um gráfico, um mapa ou uma
fotografia não se escreve em quatro alternativas — o documento 03 §11 já decidiu que cada
pergunta admite **uma imagem opcional de até 1 MB**, nos formatos de imagem da lista fechada do
upload, com teto menor que o do conteúdo porque o quiz é lido no aparelho do Guerreiro(a),
muitas vezes em rede fraca.

Três decisões do fundador de 2026-09-11 acompanham a fatia, porque o desenho de hoje não as
resolvia:

- **A imagem sobrevive à redeclaração do desafio.** Redeclarar substitui as perguntas
  (`RF-09-26`): sem isso, corrigir uma vírgula no enunciado custaria reenviar todos os
  arquivos do quiz.
- **O núcleo serve os bytes da imagem.** Nenhuma rota devolve arquivo enviado — as telas
  exibem só a referência —, e imagem que não se vê não cumpre o `RF-09-119`.
- **A redeclaração deixa de estourar.** A fatia 18 subiu apagando as perguntas para
  substituí-las, mas a resposta gravada aponta a pergunta: depois que qualquer Guerreiro(a)
  responde o quiz, redeclarar viola a integridade e responde **500**. É a mesma operação que
  esta fatia reescreve para preservar a imagem, e o conserto entra com ela.

## What Changes

- A pergunta do quiz do desbloqueio passa a ter **imagem opcional**, uma por pergunta, enviada
  pelo mesmo padrão do conteúdo da missão: sessão retomável, bytes direto ao armazenamento,
  núcleo guardando só a referência (`RF-09-119`).
- O envio da imagem aceita apenas **JPG, PNG e WebP** — os formatos de imagem da lista fechada
  do `RF-09-115` — e recusa **acima de 1 MB**, na abertura da sessão e de novo na confirmação.
- **Redeclarar o desafio preserva a imagem** de cada pergunta cuja referência volta na
  declaração; a pergunta que a omite fica sem imagem, e é assim que o Mestre a remove.
- O núcleo passa a **servir os bytes** da imagem de uma pergunta a quem já pode vê-la — o
  Mestre autor da trilha e o Guerreiro(a) inscrito nela —, e a ninguém mais.
- A App 09 anexa, troca e remove a imagem de cada pergunta, com o progresso do envio; a App 05
  exibe a imagem junto do enunciado, com texto alternativo.
- A duplicação da trilha leva a **referência** da imagem das perguntas copiadas, sem copiar
  bytes (`RF-09-75`, sem mudança de regra).
- **Conserto da fatia 18** — redeclarar o desafio deixa de **apagar** as perguntas: elas são
  marcadas como substituídas e saem da leitura, o que devolve o 500 ao lugar de nunca ter
  existido e preserva a submissão já gravada, que o `RN-05-47` manda nunca apagar nem
  sobrescrever.

Fora do escopo, pelo recorte da fatia: imagem na **alternativa**, que nenhum requisito pede;
imagem no desafio **prático**, que não tem pergunta; e a leitura de bytes dos demais arquivos
enviados — vídeo, áudio, PDF e imagem do conteúdo da missão —, que é a mesma lacuna mas
alcança todo o `conteudo-da-missao` e não cabe nesta fatia.

## Capabilities

### New Capabilities

Nenhuma. A fatia acrescenta comportamento a capacidades que já existem.

### Modified Capabilities

- `desbloqueio-da-missao`: a pergunta do quiz passa a ter imagem opcional, com envio em sessão
  retomável, teto de 1 MB e formatos de imagem da lista fechada; a redeclaração preserva a
  imagem cuja referência volta; o núcleo serve os bytes a quem pode ver a pergunta.
- `area-do-mestre`: a App 09 anexa, troca e remove a imagem de cada pergunta do quiz, e a
  mantém ao gravar o desafio de novo.
- `area-do-guerreiro`: a App 05 exibe a imagem da pergunta junto do enunciado.
- `trilha-e-missao`: a cópia da trilha leva a imagem das perguntas do desafio, pela referência.

## Impact

- `backend/src/nucleo/trilhas/modelo.py` — a referência, o tipo e o tamanho da imagem e a
  marca de substituição em `PerguntaDoDesbloqueio`.
- `backend/src/nucleo/trilhas/regra.py` — `declarar_desafio_de_desbloqueio` (preservação da
  referência), abertura e confirmação do envio, leitura dos bytes e `duplicar_trilha`.
- `backend/src/nucleo/trilhas/rotas.py` — as três rotas novas da imagem e a saída da pergunta,
  ao Mestre autor e ao Guerreiro(a).
- `backend/alembic/versions/` — revisão que acrescenta as quatro colunas e troca a unicidade
  de (missão, ordem) por unicidade só entre as perguntas vigentes.
- `comum/api/` — leitura de bytes do núcleo, que o cliente compartilhado ainda não faz.
- `docs/03-plataforma-e-arquitetura.md` §11, `docs/09-topicos-em-aberto-e-sugestoes.md` §1 e
  `docs/prds/prd-09-area-do-mestre.md` §§9, 14 — as duas decisões do fundador de 2026-09-11.
- `apps/app-09-mestre/src/trilhas/` — `DesafioDeDesbloqueio.tsx` e `api.ts`.
- `apps/app-05-guerreiro/src/trilha/` — `DesafioDeDesbloqueio.tsx` e `api/trilha.ts`.
- Testes: `backend/tests/test_desbloqueio_da_missao.py`, `test_duplicacao_de_trilha.py`,
  `test_migracoes.py` e os testes das duas telas.
