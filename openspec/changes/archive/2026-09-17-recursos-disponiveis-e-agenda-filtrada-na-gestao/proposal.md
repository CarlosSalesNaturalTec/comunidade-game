PRD-02 (Frontend de gestão, App 03) — fatia 20 do `openspec/cronograma-de-fatias.md`.
Atende `RF-02-57`, `RF-02-58`, `RF-02-102` (área Recursos, já entregues), `RF-02-45`,
`RF-02-97` (conceito de saldo disponível por tipo de recurso, já entregue em Painel do dia e
em Pontos de Apoio) e `RF-02-12`, `RN-02-20` (agenda). Decisão do fundador de 2026-09-17: só
reorganização de tela e reaproveitamento de rota — não cria RF, RN, rota nem entidade nova.

## Why

Na área Recursos, o formulário de registro de aporte e o de publicação da missão do Apoiador
ficam sempre abertos, empilhados na mesma tela, sem o padrão de toggle que Acervo e Agenda já
usam — e a área só mostra o que **falta** (necessidades em aberto), nunca o que **há**
disponível, embora o núcleo já sirva esse saldo (hoje só consumido em Pontos de Apoio). Na
Agenda, a lista sempre traz as aulas canceladas junto das demais, sem filtro para escondê-las,
o que polui a leitura do dia a dia do Admin.

## What Changes

- Recursos: o formulário de registro de aporte (`RegistroDeAporte`) e o de publicação de
  missão do Apoiador (`PublicacaoDeMissao`) passam a ficar atrás de um botão de toggle cada
  ("Registrar aporte" / "Publicar missão"), no padrão já usado em `TelaDoAcervo` e
  `TelaDaAgenda`.
- Recursos: nova lista de saldo disponível por tipo de recurso, reaproveitando a rota que já
  existe (`GET /v1/pontos-de-apoio/{id}/saldos`, hoje só consumida em Pontos de Apoio),
  agregada pelos pontos de apoio das comunidades que a tela já lista.
- Agenda: o formulário de nova aula (`FormularioDeAgendamento`) passa a ficar atrás do toggle
  "Nova aula"; o filtro de comunidade e período permanece sempre visível.
- Agenda: novo checkbox "Exibir canceladas", desmarcado por padrão — a lista esconde as aulas
  com `situacao = cancelada` até o Admin ou Mestre marcá-lo; sem mudar a rota `/v1/aulas`,
  filtro só sobre o que ela já devolve.

Fora do escopo: qualquer cálculo de saldo agregado no frontend (a rota do núcleo já apura por
ponto de apoio), e qualquer filtro de situação na rota `/v1/aulas` do núcleo.

## Capabilities

### New Capabilities

Nenhuma — reorganização de tela e reaproveitamento de rota já normativa.

### Modified Capabilities

- `aplicacao-de-gestao`: a requirement "A App 03 abre a área Recursos, com o registro do
  aporte e as necessidades" passa a incluir o saldo disponível por tipo de recurso entre o que
  a área apresenta; a requirement "A aplicação apresenta a agenda das aulas" passa a esconder
  por padrão a aula cancelada, com opção de reexibir.

## Impact

- `apps/app-03-gestao/src/recursos/TelaDeRecursos.tsx`, `RegistroDeAporte.tsx`,
  `PublicacaoDeMissao.tsx`, `api.ts` (nova função que reaproveita
  `listarSaldosDoPontoDeApoio`, hoje só em `pontos-de-apoio/api.ts`).
- `apps/app-03-gestao/src/agenda/TelaDaAgenda.tsx`, `ListaDaAgenda.tsx`.
- Nenhum código de `backend/` muda — as duas rotas já existem e já respondem o que as telas
  vão consumir.
