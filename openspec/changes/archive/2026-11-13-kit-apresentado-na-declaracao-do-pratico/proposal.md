# Proposal

Origem: **PRD-09** (Área do Mestre, App 09), **fatia 31** do `openspec/cronograma-de-fatias.md`
— "Kit apresentado na declaração do prático". Identificador atendido: `RF-09-141`, no lado da
aplicação. O lado do núcleo — a gravação, a validação e a leitura do kit — já entrou pela fatia
"Customização do kit recebido no núcleo" do PRD-01
(`2026-11-12-customizacao-do-kit-recebido-no-nucleo`), da qual esta depende.

## Why

O núcleo já aceita, na declaração do desafio prático, a recompensa de marco da trilha que o
prático apresenta como kit, e devolve o kit nas leituras do Mestre autor. A App 09, porém, não
oferece a escolha e não manda o campo: nenhum prático ganha kit, a customização do kit recebido
nunca abre, e as fatias de aplicação da customização (PRD-04 fatia 34, PRD-05 fatia 18) ficam
sem ter o que julgar ou registrar. Pior: como declarar de novo **substitui** o kit, inclusive
por nenhum, uma tela que não reenvia o campo apagaria o kit a cada correção do critério.

## What Changes

- No bloco do desafio de desbloqueio, escolhido o **prático**, a App 09 oferece a escolha
  **opcional** do kit apresentado entre as **recompensas de marco já declaradas na trilha**,
  pelo nome do tipo de recurso e pela missão do marco, com a opção "nenhum" (`RF-09-141`).
- A tela diz ao Mestre, em linguagem dele, o que a escolha faz: a comprovação aprovada vira o
  primeiro registro daquele kit e abre a customização dele, e cabe ao Mestre dizer o que é kit
  — camisa e livro não são (`RF-09-141`).
- A tela **reabre** o kit declarado e o **reenvia** a cada nova declaração do prático, para
  que corrigir o critério nunca apague o kit; no **quiz** o campo não aparece nem vai ao núcleo.
- Trilha sem recompensa de marco declarada mostra a escolha vazia com o caminho: declarar a
  recompensa no bloco "Recompensa pelo desbloqueio".
- A recusa do núcleo pelo campo (`kit_apresentado_id`) chega no bloco, com o motivo.
- O resumo recolhido do desafio prático diz o kit declarado, quando houver.

**Fora desta fatia**, como o PRD-09 e o cronograma já recortam: o julgamento da customização e
a validação da conservação, que são do Mestre da aula no App 01 (PRD-04 fatias 34 e 35); o
registro em casa (PRD-05 fatia 18); a exibição na vitrine (PRD-03 fatia 14). Nenhuma mudança de
núcleo.

## Capabilities

### New Capabilities

Nenhuma.

### Modified Capabilities

- `area-do-mestre`: o bloco do desafio prático passa a declarar, reabrir e reenviar o kit
  apresentado.

## Impact

- **App 09**: `src/trilhas/api.ts` (o campo na entrada e na leitura da missão),
  `src/trilhas/DesafioDeDesbloqueio.tsx` (a escolha, a reabertura e o reenvio),
  `src/trilhas/ListaDeMissoes.tsx` (repassa as recompensas e os tipos de recurso, e o resumo),
  e os testes de `src/trilhas/`.
- **Contratos**: nenhum novo — consome `kit_apresentado_id` de `POST
  /v1/missoes/{id}/desbloqueio` e `desafio_pratico_kit_apresentado` de `GET /v1/trilhas/minhas`
  e da resposta da declaração, já existentes.
- **Dados**: sem migração.
- **Documentação**: a decisão já está nos documentos 11, 09 e 99 e no PRD-09; esta change fecha
  a linha do cronograma.
