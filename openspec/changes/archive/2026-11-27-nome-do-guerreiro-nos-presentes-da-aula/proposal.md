# Proposal

PRD-09 — Área do Mestre (App 09), **fatia 38** do `openspec/cronograma-de-fatias.md`. Alcança
`RF-09-145` (reescrito) e `RN-09-18`, sem identificador novo: é decisão de exibição do
fundador de 2026-11-27 sobre requisito já entregue pela fatia 36.

## Why

Na tela da aula (Minhas turmas → Presença e ocorrência), cada presente aparece só por nick e
avatar. O nick nem sempre diz quem é a criança, e o Mestre precisa reconhecê-la pelo nome para
conferir a presença e lançar a ocorrência no Guerreiro(a) certo — o mesmo motivo da fatia 37,
que pôs o nome ao lado do nick na lista de responsáveis.

## What Changes

- **Núcleo:** cada presença de `GET /v1/aulas/{id}/presencas` passa a trazer o **nome** do
  Guerreiro(a), ao lado de nick, avatar, momento do fato e modo. Escopo do Mestre (`RN-09-08`),
  permissão e exclusão da presença anulada não mudam.
- **App 09:** a lista "Presentes nesta aula" passa a mostrar, de cada presente, **avatar, nick
  e nome**, com a hora e o modo.
- Continuam proibidos imagem real e descritor facial do Guerreiro(a) (`RN-09-18`); a tela não é
  superfície pública (invariante 12 do documento 99 §6).
- **Documentação:** a linha "Presentes da aula em Minhas turmas" do documento 09 §1 e o
  enunciado do `RF-09-145` no PRD-09 passam a dizer "por nick, nome e avatar" (decisão de
  2026-11-27).

Fora do escopo: os formulários de confirmação de presença e de ocorrência, que seguem pedindo
o nick; as demais leituras de presença (`/presencas/eu`, painel do dia); a App 01 e a App 03.

## Capabilities

### New Capabilities

Nenhuma.

### Modified Capabilities

- `aula-e-presenca`: "O Mestre lê as presenças registradas na aula" passa a exigir o nome do
  Guerreiro(a) em cada presença.
- `area-do-mestre`: "O Mestre confirma a presença e lança a ocorrência de conduta" passa a
  exibir o nome de cada presente.

## Impact

- `backend/src/nucleo/aulas/rotas.py` (`PresencaDaAulaSaida`, `listar_presencas_da_aula_rota`);
  `backend/tests/test_presenca_do_mestre.py`.
- `apps/app-09-mestre/src/turmas/api.ts`, `TelaDaAula.tsx`, `turmas.test.tsx`.
- `docs/09-topicos-em-aberto-e-sugestoes.md` §1, `docs/prds/prd-09-area-do-mestre.md` e
  `openspec/cronograma-de-fatias.md`.
- Sem migração, sem rota nova, sem `Operacao` nova. Campo **acrescentado** à resposta: cliente
  que o ignora segue funcionando.
