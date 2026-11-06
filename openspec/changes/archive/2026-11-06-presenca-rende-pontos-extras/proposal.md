# Proposal

Origem: **PRD-01** (núcleo) e **PRD-07** (economia), fatia sem número do bloco PRD-01 do
`openspec/cronograma-de-fatias.md` — "Presença rende 5 pontos extras, e o piso do catálogo sobe
a 25". Identificadores **novos**, criados na revisão dos PRDs feita por esta change:
`RF-01-82`, `RF-01-83`, `RN-01-64`, `RN-01-65` e `RF-07-50`. Alterados: `RF-01-56`,
`RN-01-39`, `RF-07-44` e `RN-07-30`. Preservados: `RF-01-20`, `RF-02-36`, `RN-02-12`,
`RN-01-40`.

## Why

A decisão do fundador de 2026-11-06 (documento 09 §1, "A presença na aula presencial rende 5
pontos extras") torna a presença registrada uma fonte de ponto extra (documento 11 §5) e a
anulação da presença o único fato que reduz o acumulado (invariante 23). Como o encontro
exemplar passa a render 23 extras, o piso do catálogo avulso sobe de 20 para 25 (documento 02
§8.2). Hoje o núcleo não credita nada na presença, recusa por gatilho toda redução do
acumulado e recusa só preço abaixo de 20.

## What Changes

- **A presença registrada credita 5 pontos extras** ao Guerreiro(a), no acumulado e no saldo
  disponível, na mesma operação que grava a presença, nos dois modos de comprovação. O
  reenvio idempotente do App 01 não credita de novo.
- **A anulação da presença estorna os 5 extras** nas duas contas, na mesma operação que grava a
  anulação. O saldo disponível para em zero quando já foi trocado. **BREAKING** na regra
  vigente de `ponto-extra`: o acumulado deixa de ser "só crédito", e o gatilho do banco passa
  a admitir esta única redução.
- **Sem crédito retroativo**: presença gravada antes da entrega não rende e, anulada depois,
  não estorna.
- **O piso do preço de referência sobe de 20 para 25** pontos extras, na regra e no `CHECK` do
  banco.
- **A migração eleva a 25 todo preço de referência vigente abaixo do piso**, abrindo vigência
  nova na data da entrega; a vigência anterior fica no histórico.
- **A carteira da App 05** deixa de dizer que o acumulado "só cresce": passa a dizer que a
  troca não o diminui.
- Migração Alembic: coluna do crédito da presença, gatilho do ponto extra, piso e preços.

**Fora desta fatia**: aviso do estorno na tela de anulação da App 03 e exibição do "+5" na
confirmação de presença do App 01 — o PRD não os pede.

## Capabilities

### New Capabilities

Nenhuma.

### Modified Capabilities

- `ponto-extra`: a presença vira fonte só extra; o acumulado passa a admitir uma única
  redução, o estorno da presença anulada; o saldo disponível ganha um segundo débito, que para
  em zero.
- `aula-e-presenca`: registrar presença credita os extras, e anular a presença os estorna.
- `catalogo-de-tipos-de-recurso`: o piso do preço de referência passa a 25, e os preços
  vigentes abaixo dele são elevados na entrega.

## Impact

- **Núcleo**: `aulas/` (modelo e regra da presença), `ponto_extra/` (modelo, gatilho e
  regra do estorno), `recursos/` (piso).
- **Contratos**: nenhuma rota nova nem campo novo de resposta. Preço de referência entre 20 e
  24 passa a ser recusado com 422.
- **Dados**: migração Alembic — coluna em `presenca`, função e gatilho de `ponto_extra`,
  `CHECK` do piso e vigências novas de preço.
- **App 05**: uma frase da carteira (`MinhaCarteira.tsx`) e o teste dela.
- **Documentação**: a decisão já está gravada nos documentos 11 §§1 e 5, 02 §§1 e 8.2, 99 §6 e
  09 §1. Esta change revisa o **PRD-01**, o **PRD-07** e as menções ao piso e ao acumulado nos
  PRDs 04, 05, 09 e 14, e fecha a linha do cronograma.
