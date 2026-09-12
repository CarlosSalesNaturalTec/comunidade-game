## Why

Conserto das fatias **18 e 19 do PRD-09** (`openspec/cronograma-de-fatias.md`, linha sem
número no bloco do PRD-09). Atende `RF-09-26`, `RF-09-118`, `RF-09-119`, `RF-09-81` e
`RN-09-30`, e alcança `RN-05-46`, que o núcleo já cumpre.

**Nenhuma rota devolve o desafio de desbloqueio ao Mestre autor.** Só a resposta do próprio
`POST /v1/missoes/{id}/desbloqueio` o traz; `MissaoSaida`, de que a leitura das trilhas
próprias deriva, não carrega campo algum do desafio. Em produção, o Mestre declara o quiz, vê
a marca de gravação, sai e volta: o formulário está vazio, e a linha da missão diz que a
missão não tem desafio. O dado está no banco — o que falta é a leitura de volta.

O efeito é pior que a invisibilidade. Redeclarar **substitui**; como o formulário volta
vazio, gravar de novo carimba as perguntas vigentes e órfã as imagens, porque o cliente não
tem como devolver a referência que nunca recebeu. `desbloqueio-da-missao` já prescreve essa
leitura ao autor, incluindo a referência da imagem — a decisão 4 da fatia 18 protegeu a
alternativa correta de vazar em `MissaoSaida`, mas a contrapartida, uma leitura só do autor,
nunca foi escrita.

Duas sequelas da mesma origem vêm junto: a App 09 nunca desenha a imagem da pergunta, que só
o Guerreiro(a) vê, e a tela trata a **sondagem** como um desbloqueio comum, anunciando um
corte de 60% que `RN-05-46` não lhe aplica.

## What Changes

- A leitura das trilhas próprias do Mestre passa a trazer, em cada missão, o **desafio de
  desbloqueio** declarado — tipo, enunciado do prático e, no quiz, as perguntas com
  identificador, alternativa correta e referência da imagem (`RF-09-26`, `RF-09-118`,
  `RF-09-119`). É a rota que já é exclusiva do Mestre autor e já aninha o desafio de coleta,
  de modo que a alternativa correta não sai do alcance de quem pode vê-la.
- A App 09 passa a **reabrir** o desafio já declarado: o formulário nasce preenchido, com a
  alternativa correta marcada e o identificador de cada pergunta, e o resumo da linha da
  missão passa a refletir o que existe. Corrigir texto deixa de trocar o quiz inteiro, e
  anexar imagem a pergunta antiga passa a funcionar entre sessões.
- A App 09 passa a **mostrar a imagem** da pergunta ao Mestre autor, hoje reduzida à frase de
  que a pergunta tem imagem (`RF-09-119`). Só tela: a rota que serve os bytes ao autor já
  existe.
- A missão de **sondagem** passa a se chamar pelo nome na App 09: rótulo, abertura, aviso de
  vazio e resumo próprios, o corte de 60% substituído pelo que de fato vale — a trilha abre
  quando o Guerreiro(a) responde —, e a escolha entre quiz e prático deixa de ser oferecida,
  porque `RF-09-81` fixa a sondagem na forma de quiz (`RN-09-30`, `RN-05-46`).

Fora do escopo, além do que o PRD-09 §3.2 já exclui:

- A trava de publicação de `RF-09-82` e `RN-09-29` confere apenas que a missão de sondagem
  **existe**, de modo que sondagem sem nenhuma pergunta publica. A change **não** altera a
  trava; registra a pendência no documento 09 §1 para o fundador decidir.
- Nenhuma imagem órfã a recuperar: o fundador confirmou que nenhuma chegou a ser salva em
  produção.
- O corte de 60% e a exceção da sondagem no núcleo não mudam — já estão corretos.

## Capabilities

### New Capabilities

Nenhuma. A change conserta o alcance de capacidades que já existem.

### Modified Capabilities

- `trilha-e-missao`: a leitura das trilhas próprias do Mestre passa a trazer o desafio de
  desbloqueio de cada missão, com a alternativa correta e a referência da imagem de cada
  pergunta — hoje a leitura devolve a missão sem nenhum campo do desafio.
- `area-do-mestre`: a tela do desafio passa a reabrir o que já foi declarado em vez de nascer
  vazia; a imagem da pergunta passa a ser exibida ao Mestre autor; e a missão de sondagem
  passa a ser apresentada como sondagem, sem o corte de 60% e sem a escolha de desafio
  prático.

## Impact

- `backend/src/nucleo/trilhas/rotas.py` — a saída da missão do Mestre em `GET
  /v1/trilhas/minhas` passa a aninhar o desafio; reaproveita `_saida_das_perguntas` e a saída
  ao autor que a declaração já usa.
- `apps/app-09-mestre/src/trilhas/api.ts` — o tipo da missão passa a receber o desafio pela
  leitura, e o comentário que descreve a ausência como intencional sai.
- `apps/app-09-mestre/src/trilhas/DesafioDeDesbloqueio.tsx` — exibição da imagem pela função
  cliente que já existe e nunca foi chamada, e os textos da sondagem.
- `apps/app-09-mestre/src/trilhas/ListaDeMissoes.tsx` — rótulo e resumo do bloco na sondagem.
- Testes: `backend/tests/test_trilha_rota.py`, `backend/tests/test_desbloqueio_da_missao.py` e
  `apps/app-09-mestre/src/trilhas/trilhas.test.tsx`.
- Documentação: `openspec/cronograma-de-fatias.md` (a linha desta change) e
  `docs/09-topicos-em-aberto-e-sugestoes.md` §1 (a pendência da sondagem sem pergunta).
