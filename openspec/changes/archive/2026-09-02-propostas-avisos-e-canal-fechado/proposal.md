## Why

Fatia 8 do PRD-14 (`openspec/cronograma-de-fatias.md`, bloco "PRD-14 — Área do Apoiador"),
atendendo `RF-14-56` a `RF-14-59`, `RN-14-26` e `RN-14-27`.

A App 08 já coleta dado em oito telas — pré-cadastro, troca da senha provisória, identidade
pública, comprobatórios, declaração de aporte, cobertura de missão, proposta de desafio extra e
favorito — e não avisa o que coleta nem oferece a área detalhada. E o Apoiador ainda não tem por
onde propor evolução da plataforma: a fila única da gestão já recebe o Guerreiro(a), o
responsável e o Mestre, e o núcleo já aceita o Apoiador nela.

## What Changes

- Área **Propostas** na App 08: registro da proposta de evolução em texto na fila única da
  gestão e acompanhamento do status até o retorno, com o motivo em linguagem simples quando não
  adotada (`RF-14-56`, `RF-14-57`, `RN-14-26`, `RN-14-27`).
- Área **Direitos e dados** na App 08 — a área detalhada do aviso —, de leitura, com o que a
  aplicação coleta, para quê, com que base legal, por quanto tempo e quem acessa (PRD-14 §11).
- **Aviso discreto de coleta** em toda tela da App 08 que grava dado, nomeando o dado daquela
  tela e levando à área detalhada, sem bloquear a tela nem exigir confirmação (`RF-14-58`).
- Garantia declarada de **canal fechado**: nenhuma tela da App 08 oferece mensagem, contato ou
  resposta a Guerreiro(a), família ou Mestre (`RF-14-59`).
- Sem mudança no núcleo: as rotas `POST /v1/sugestoes` e `GET /v1/sugestoes/minhas` e a
  operação `propostas_de_evolucao` do Apoiador já existem.

## Capabilities

### New Capabilities

Nenhuma.

### Modified Capabilities

- `area-do-apoiador`: ganha os requisitos da área de propostas, da área de direitos e dados, do
  aviso de coleta em toda tela que grava dado e do canal fechado em toda a aplicação.

## Impact

- `apps/app-08-apoiador/src/propostas/` (novo): tela e cliente da fila única.
- `apps/app-08-apoiador/src/direitos/` (novo): contexto, aviso e a tela da área detalhada.
- `apps/app-08-apoiador/src/App.tsx`: duas áreas novas na navegação e o provedor do aviso.
- As oito telas da App 08 que gravam dado passam a exibir o aviso.
- `apps/app-08-apoiador/src/index.css`: classes do aviso e da tabela de direitos.
- Backend, banco e contratos de API: nada muda.
- Documentação: a linha da fatia 8 no `openspec/cronograma-de-fatias.md`.
