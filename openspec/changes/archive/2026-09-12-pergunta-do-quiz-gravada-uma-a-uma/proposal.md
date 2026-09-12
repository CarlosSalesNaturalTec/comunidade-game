## Why

Fatia **20 do PRD-09** (`openspec/cronograma-de-fatias.md`, bloco do PRD-09). Atende
`RF-09-120` e `RN-09-44`, novos, e alcança `RF-09-26`, `RF-09-118`, `RF-09-119`, `RF-09-81`,
`RN-09-43` e `RN-05-47`, já existentes.

**O quiz só se grava inteiro.** `POST /v1/missoes/{id}/desbloqueio` recebe a lista completa e
substitui o conjunto: corrigir a vírgula de uma pergunta reescreve as doze, e cada gravação
carimba as vigentes e insere uma geração nova. O Mestre autor paga três preços por isso. O
primeiro é o risco — a gravação é tudo ou nada, e uma recusa em qualquer pergunta derruba o
trabalho das outras. O segundo é a imagem: a referência do arquivo nasce do **id** da pergunta,
e como a gravação do todo troca os ids, conservar a imagem depende de o cliente devolver a
referência certa em cada posição, mecanismo que a fatia 19 precisou inventar só para que
corrigir texto não custasse reenviar arquivo. O terceiro é a ordem dos gestos: a imagem só pode
ser anexada depois que a pergunta existe, e como só existe quem gravou o quiz inteiro, o Mestre
que acrescenta uma pergunta precisa gravar tudo antes de poder anexar a imagem dela.

Vale igual para a **sondagem**, que é quiz pelo `RF-09-81` e usa o mesmo bloco da tela: quem
monta a sondagem que abre a trilha enfrenta exatamente os mesmos três preços.

Duas falhas da fatia anterior, já corrigidas no branch (commit `2d487c7`), vêm registradas
nesta fatia porque travavam o mesmo ato: a tela mandava o `id` da pergunta num corpo que recusa
campo fora do contrato, de modo que **toda** regravação de quiz já declarado respondia 422; e o
CORS do núcleo não permitia o `Content-Range` do protocolo de envio, de modo que o navegador
barrava o envio de **qualquer** arquivo — imagem da pergunta, conteúdo da missão e criação
original — antes de o núcleo ser chamado.

## What Changes

- O núcleo passa a gravar, corrigir e remover **cada pergunta do quiz isoladamente**, sem
  tocar nas demais (`RF-09-120`). A pergunta ganha endereço próprio de escrita, na sondagem
  como no desbloqueio, e a **ordem** declarada pelo Mestre segue sendo dele.
- Gravar uma pergunta isolada **exige que ela esteja completa** — enunciado, as quatro
  alternativas e a indicação da correta (`RN-09-44`). É a mesma exigência que `RN-09-43` já faz
  do quiz inteiro, aplicada à unidade menor: a pergunta nasce válida ou não nasce (decisão do
  fundador, 2026-09-12).
- `POST /v1/missoes/{id}/desbloqueio` **continua** como está, declarando o tipo do desafio e o
  enunciado do prático, e segue substituindo o quiz quando recebe a lista. As rotas por
  pergunta entram **ao lado** dela, não no lugar (decisão do fundador, 2026-09-12). Nada muda
  para a App 05 nem para o percurso do Guerreiro(a).
- A edição de uma pergunta honra `RN-05-47` como a substituição do todo já honra: pergunta que
  alguma submissão já respondeu NEVER é apagada nem alterada — sai da leitura e permanece
  guardada, para que o registro da tentativa siga apontando o que o Guerreiro(a) respondeu.
- A App 09 passa a gravar pergunta a pergunta, com marca de gravação própria de cada uma, e o
  erro de uma pergunta deixa de apagar o que foi escrito nas outras. Anexar imagem numa
  pergunta ainda não gravada passa a ser **um gesto só**: a tela grava a pergunta e emenda o
  envio; incompleta, diz o que falta (decisão do fundador, 2026-09-12).
- Entram os dois consertos já commitados: o corpo da declaração deixa de levar o `id` da
  pergunta, a recusa do núcleo passa a chegar ao Mestre com o motivo, e o CORS passa a permitir
  o `Content-Range` e a expor o `Range` da retomada.

Fora do escopo, pelo que o PRD-09 §3.2 já exclui: nada muda na **submissão** do quiz pelo
Guerreiro(a), na aferição dos 60%, no julgamento do prático nem na leitura do percurso. A
pergunta segue com **quatro** alternativas e **uma** imagem, e o teto de 1 MB não se reabre.

## Capabilities

### New Capabilities

Nenhuma. A change amplia capacidades que já existem.

### Modified Capabilities

- `desbloqueio-da-missao`: a pergunta do quiz passa a ter escrita própria — criar, corrigir e
  remover uma pergunta sem tocar nas demais —, com a exigência de pergunta completa e com o
  mesmo cuidado da substituição do todo quanto à pergunta já respondida. A declaração do
  desafio inteiro permanece, e a rota de imagem passa a valer também para pergunta criada
  isoladamente.
- `area-do-mestre`: a tela do desafio passa a gravar pergunta a pergunta, com marca e erro por
  pergunta, e a anexar imagem em pergunta nova sem exigir do Mestre que grave o quiz antes.

## Impact

- `backend/src/nucleo/trilhas/regra.py` — regras de criar, corrigir e remover pergunta do
  quiz; reaproveita `_conferir_perguntas_do_quiz`, `conferir_posse_da_trilha` e o carimbo de
  `substituida_em` que a substituição do todo já usa.
- `backend/src/nucleo/trilhas/rotas.py` — as rotas por pergunta, ao lado da declaração do
  desafio, que não muda.
- `apps/app-09-mestre/src/trilhas/api.ts` e `DesafioDeDesbloqueio.tsx` — gravação por pergunta,
  marca e erro por pergunta, e o anexo da imagem num gesto só.
- `backend/src/nucleo/principal.py` — `Content-Range` permitido e `Range` exposto no CORS (já
  commitado).
- Testes: `backend/tests/test_desbloqueio_da_missao.py`, `backend/tests/test_convencoes.py` e
  `apps/app-09-mestre/src/trilhas/trilhas.test.tsx`.
- Documentação: `docs/03-plataforma-e-arquitetura.md` §11 (documento-fonte da decisão nova),
  `docs/09-topicos-em-aberto-e-sugestoes.md` §1, `docs/prds/prd-09-area-do-mestre.md`
  (`RF-09-120`, `RN-09-44` e a rastreabilidade §15) e a linha da fatia 20 no cronograma.
- Migração: nenhuma coluna nova prevista; o índice parcial de (missão, ordem) das perguntas
  vigentes é o ponto a confirmar no `design`.
