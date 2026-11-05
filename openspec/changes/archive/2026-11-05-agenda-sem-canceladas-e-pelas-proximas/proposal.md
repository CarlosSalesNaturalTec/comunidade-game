PRD-02 (App 03 — Frontend de gestão), sobre o PRD-01. Linha sem número no
`openspec/cronograma-de-fatias.md` ("Agenda sem canceladas e pelas próximas aulas") — correção
de defeito sobre a agenda já entregue, não requisito novo. Atende `RF-02-12` e `RF-01-28`.
Decisão do fundador de 2026-11-05, registrada no documento 09 §1.

## Why

A agenda da App 03 mostra "Nenhuma aula agendada ainda." com aula prevista na comunidade. A rota
`GET /v1/aulas` devolve a primeira página de 25 da mais antiga para a mais nova, e a tela esconde
a cancelada **depois**, sobre essa página — a escolha da change
`2026-09-17-recursos-disponiveis-e-agenda-filtrada-na-gestao`. Com as aulas da fase de testes
canceladas (documento 09, "Vínculo do Mestre com a comunidade"), a página 1 vem inteira de
canceladas, some no filtro, e a aula válida fica numa página que a tela nunca pede.

## What Changes

- `GET /v1/aulas` deixa de devolver aula `cancelada` por padrão; o filtro de domínio novo
  `incluir_canceladas=true` a devolve junto das demais.
- `GET /v1/aulas` ordena pelas **próximas aulas**: primeiro as que ainda não terminaram, da mais
  próxima à mais distante; depois as já terminadas, da mais recente à mais antiga. O cursor
  passa a carregar o grupo e o momento de referência da primeira página.
- App 03: o controle "Exibir canceladas" passa a ser parâmetro da busca ao núcleo; sai o filtro
  local.
- **BREAKING** (só para consumidor que dependia da ordem cronológica crescente ou da cancelada
  no padrão): a App 03 é o único consumidor de `GET /v1/aulas` e muda no mesmo PR.

## Capabilities

### New Capabilities

Nenhuma.

### Modified Capabilities

- `aula-e-presenca`: "A gestão lê a agenda, filtrada por comunidade e por período" ganha a
  exclusão da cancelada por padrão, o filtro que a inclui e a ordem pelas próximas aulas.
- `aplicacao-de-gestao`: "A aplicação apresenta a agenda das aulas" troca a reexibição local
  pela busca ao núcleo — a regra "NEVER SHALL deixar de buscar a aula cancelada" se inverte — e
  a ordem pelas próximas aulas. O comentário de `TelaDaAgenda.tsx` que ancora o filtro em
  `RN-02-09`/`RN-02-20` sai: nenhum dos dois trata da cancelada.

## Impact

- **Backend**: `backend/src/nucleo/aulas/rotas.py` (`listar_agenda_rota`); testes em
  `backend/tests/test_aula.py`. Nenhuma migração.
- **App 03**: `apps/app-03-gestao/src/agenda/api.ts`, `TelaDaAgenda.tsx`, `agenda.test.tsx` e
  `api.test.ts` (novo).
- **Sem impacto** em `GET /v1/aulas/vigentes` (App 01 e painel do dia), que já exclui a
  cancelada, nem no cancelamento.
- **Docs**: linha nova em "Já decididos" do documento 09 §1; nenhum PRD muda de texto — nenhum
  `RF`/`RN` fixava a ordem nem a presença da cancelada.
