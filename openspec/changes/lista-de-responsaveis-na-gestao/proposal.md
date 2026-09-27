# Proposal

Fatia 24 do **PRD-02 — Frontend de gestão (App 03)**, conforme
`openspec/cronograma-de-fatias.md`. Atende `RF-02-111` (novo) e reaproveita `RF-02-06`,
`RF-02-07` e `RN-02-08`. Decisão nova do fundador, 2026-09-26.

## Why

A sub-área **Responsáveis** da App 03 tem só o botão de cadastrar. Não há lista, e nenhuma
rota do núcleo devolve os responsáveis cadastrados — só existem `GET /v1/guerreiros/{id}/responsaveis`
(por criança) e `GET /v1/eu/guerreiros` (o próprio responsável).

A consequência é operacional, não cosmética: uma vez que o Admin clica em "Concluir",
aquele responsável fica **inalcançável pela gestão**. Cadastro interrompido antes do
vínculo não aparece em lugar nenhum, e não há como vincular mais um Guerreiro(a) a um
responsável já cadastrado. Relatado pelo fundador em 2026-09-26.

## What Changes

- **Núcleo:** nasce `GET /v1/responsaveis`, paginada, com o **nome** do responsável e os
  Guerreiros e Guerreiras vinculados por **nick** e **grau de parentesco**.
  - **Admin** alcança todos os responsáveis.
  - **Mestre** alcança os responsáveis com vínculo vigente a Guerreiros e Guerreiras das
    comunidades em que atua, **e os que ele próprio cadastrou** — sem a segunda parte, o
    cadastro que ele interrompeu antes do vínculo sumiria justamente de quem precisa
    retomá-lo.
  - Responsável **sem vínculo** aparece na lista.
  - A resposta NEVER traz credencial, senha ou contato.
- **App 03:** a sub-área Responsáveis passa a apresentar a lista, e a partir dela o Admin
  **retoma um responsável já cadastrado** para vincular outro Guerreiro(a), pela rota de
  vínculo que já existe.
- **Documentação:** o documento 02 §1 ganha uma frase sobre quem consulta os responsáveis
  cadastrados; o documento 09 §1 recebe a decisão em "Já decididos"; o PRD-02 recebe
  `RF-02-111`; o PRD-09 recebe `RF-09-122` **declarado**, sem tela.

## Capabilities

### New Capabilities

Nenhuma.

### Modified Capabilities

- `responsavel-e-vinculo`: requisito novo — o núcleo responde a Admin e a Mestre os
  responsáveis cadastrados, com os vinculados de cada um, em recortes distintos por papel.
- `aplicacao-de-gestao`: requisito novo — a App 03 apresenta os responsáveis cadastrados e
  retoma o vínculo de um deles.

## Impact

- `backend/src/nucleo/responsaveis/regra.py` — a consulta e os dois recortes.
- `backend/src/nucleo/responsaveis/rotas.py` — `GET /v1/responsaveis`.
- `backend/tests/` — cobertura da rota e dos recortes.
- `apps/app-03-gestao/src/personas/api.ts`, `TelaDePersonas.tsx`,
  `FormularioDeResponsavel.tsx` e uma lista nova; `personas.test.tsx`.
- Migrações: **nenhuma** — a consulta usa `Persona.criada_por` e `VinculoResponsavel`, que
  já existem.
- Permissões: **nenhuma `Operacao` nova** — reaproveita a de vínculo, como `RF-13-35` já faz.
- `docs/02-*.md` §1, `docs/09-*.md` §1, `docs/prds/prd-02-frontend-de-gestao.md` (§§6, 9 e
  a rastreabilidade), `docs/prds/prd-09-area-do-mestre.md` (declaração de `RF-09-122`) e
  `openspec/cronograma-de-fatias.md`.

## Fora do escopo

- **A tela do Mestre** para essa lista: é a fatia 22 do PRD-09 (`RF-09-122`), que depende
  desta. Aqui a rota já sai autorizada ao Mestre, mas a App 09 não ganha tela.
- **Sinalizar se o responsável tem credencial criada**: superfície nova de dado de
  autenticação, sem requisito no PRD — decisão do fundador de deixar de fora, 2026-09-26.
- **Editar, encerrar vínculo ou descadastrar responsável**: não há requisito no PRD-02 nem
  rota no núcleo; segue fora, como já estava.
- Listar Admins, que sofre da mesma falta na sub-área vizinha: sem requisito, não entra por
  conveniência.
