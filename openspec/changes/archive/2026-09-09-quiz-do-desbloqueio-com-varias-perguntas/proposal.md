## Why

Fatia **18 do PRD-09** (`openspec/cronograma-de-fatias.md`). Atende `RF-09-118`, `RN-09-43`,
`RF-05-89` e `RN-05-45` a `RN-05-47`, e muda o alcance de `RF-09-26`, `RF-05-13` e `RF-05-14`,
já implementados.

O quiz do desbloqueio nasceu com **uma pergunta só** — seis colunas achatadas na `Missao` —,
escolha de implementação que nenhum documento fixava. O fundador decidiu em 2026-09-09
(documento 09 §1, documento 11 §2.2) que o quiz tem quantas perguntas o Mestre quiser, que
passa quem acerta ao menos 60% delas, que a sondagem abre a trilha ao ser respondida e que toda
tentativa fica gravada com a resposta de cada pergunta.

## What Changes

- O desafio de desbloqueio em forma de **quiz** passa a ter **N perguntas**, sem limite, cada
  uma com quatro alternativas e uma correta (`RF-09-118`). O desafio **prático** não muda.
- Declarar um quiz **sem nenhuma pergunta** passa a ser recusado (`RN-09-43`).
- **BREAKING** — a submissão do desbloqueio deixa de levar **uma** alternativa e passa a levar
  a resposta de **todas** as perguntas de uma vez; a devolutiva diz quantas o Guerreiro(a)
  acertou (`RF-05-89`).
- Passa quem acerta **ao menos 60%** das perguntas (`RN-05-45`), contra o "acertou a única" de
  hoje. A **sondagem é exceção**: abre a trilha ao ser respondida, nunca ao ser acertada
  (`RN-05-46`).
- **Toda tentativa** passa a ser gravada, com a resposta de cada pergunta e se ela acertou
  (`RN-05-47`) — hoje a tentativa que não passa não deixa rastro.
- **BREAKING** — as seis colunas do desafio saem da `Missao`; o desafio de pergunta única que
  já existe é migrado para a estrutura nova sem perda.
- A duplicação da trilha passa a copiar as **perguntas** do desafio, que deixam de vir de
  carona nas colunas da `Missao` (`RF-09-75`, sem mudança de regra).

Fora do escopo, pelo recorte da fatia: a **imagem** opcional por pergunta (`RF-09-119`), que é
a fatia 19; a **marcação item a item** da hipótese H5, pendência aberta no documento 09 §1; e
a leitura agregada dessas submissões para medir a H5, que o PRD não pede no Ciclo 01.

## Capabilities

### New Capabilities

Nenhuma. A fatia altera o comportamento de capacidades que já existem.

### Modified Capabilities

- `desbloqueio-da-missao`: o quiz passa a ter N perguntas; a aferição passa a ser por
  proporção de acertos, com corte em 60%; a sondagem abre ao ser respondida; toda tentativa
  fica registrada com a resposta de cada pergunta.
- `area-do-mestre`: a App 09 monta o quiz com quantas perguntas o Mestre quiser, acrescentando
  e removendo perguntas, em vez de um enunciado único com quatro alternativas.
- `area-do-guerreiro`: a App 05 apresenta todas as perguntas e submete as respostas de uma vez,
  e o convite a tentar de novo passa a dizer quantas ele acertou.
- `trilha-e-missao`: a cópia da trilha leva o desafio de desbloqueio **com todas as suas
  perguntas**.

## Impact

- `backend/src/nucleo/trilhas/modelo.py` — entidade das perguntas e das submissões; as seis
  colunas do desafio saem da `Missao`.
- `backend/src/nucleo/trilhas/regra.py` — `declarar_desafio_de_desbloqueio`,
  `submeter_desafio_de_desbloqueio` e `duplicar_trilha`.
- `backend/src/nucleo/trilhas/rotas.py` — corpo e devolutiva de
  `POST /v1/missoes/{id}/desbloqueio` e da submissão; leitura da missão no percurso.
- `backend/alembic/versions/` — migração que cria as tabelas novas, transporta o desafio de
  pergunta única e derruba as seis colunas.
- `apps/app-09-mestre/src/trilhas/` — `DesafioDeDesbloqueio.tsx` e `api.ts`.
- `apps/app-05-guerreiro/src/trilha/` — `DesafioDeDesbloqueio.tsx` e `api/trilha.ts`.
- Testes: `backend/tests/test_desbloqueio_da_missao.py`, `test_percurso_da_trilha.py`,
  `test_duplicacao_de_trilha.py` e os testes das duas telas.
