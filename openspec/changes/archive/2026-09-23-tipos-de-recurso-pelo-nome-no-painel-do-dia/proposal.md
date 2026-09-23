PRD-02 (Frontend de gestão, App 03), fatia 21 do `openspec/cronograma-de-fatias.md`. Atende
`RF-02-44` e `RF-02-45`, já entregues pela fatia 7 e corrigidos aqui. É correção de defeito:
não cria requisito, regra, rota nem entidade nova.

## Why

No painel do dia, as listas "Previsto e provido" e "Saldo do ponto de apoio" mostram o
**identificador interno** do tipo de recurso (`e2fd9f23-…: 10.00`), e não o nome dele. Quem
conduz o encontro, em pé e no celular, não sabe o que foi reservado nem o que tem no ponto de
apoio. O `RF-02-45` pede o saldo "pelo catálogo configurável da gestão", e o PRD-02 §5.5.3
pede cada tipo pelo nome e pela unidade, nunca pelo identificador.

## What Changes

- `GET /v1/painel-do-dia` passa a devolver, em cada item de `recursos_providos` e de
  `saldo_do_ponto_de_apoio`, o `nome` e a `unidade` do tipo de recurso, lidos do catálogo. A
  mudança é **aditiva**: os campos atuais continuam iguais.
- A tela do painel do dia (App 03) mostra cada item como nome, quantidade e unidade, e deixa
  de exibir o identificador.

## Capabilities

### New Capabilities

Nenhuma.

### Modified Capabilities

- `painel-do-dia`: o requisito "O painel mostra o previsto, o provido e o saldo do ponto de
  apoio" passa a exigir que cada tipo de recurso apareça pelo nome e pela unidade do catálogo,
  nunca pelo identificador interno (`RF-02-44`, `RF-02-45`).

## Impact

- Núcleo: `backend/src/nucleo/painel_do_dia/regra.py`, com saída aditiva e sem migração.
- App 03: `apps/app-03-gestao/src/painel-do-dia/api.ts` e `TelaDoPainelDoDia.tsx`.
- Testes: `backend/tests/test_painel_do_dia.py` e `painel-do-dia.test.tsx`.
- Fora do escopo: o nome da equipe e o papel dos integrantes no painel, que são da fatia 17 do
  PRD-04, e tudo o que o PRD-02 §3.2 já exclui.
