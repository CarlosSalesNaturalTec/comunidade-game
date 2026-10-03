# Proposal

Origem: **PRD-02 — Frontend de gestão (App 03)**, fatia **16** do
`openspec/cronograma-de-fatias.md`.

Recorte: `RF-02-80` e `RF-02-101`, alcançando `RF-02-99` (auditoria da escrita) e a leitura
pública do `RF-03-45`, que não muda.

## Why

As duas telas de Admin que fecham o institucional e o comprobatório do Apoiador são o que falta
para a App 03 cobrir o que o núcleo já expõe. O núcleo foi entregue pensando nelas: a capacidade
`conteudo-institucional` declara, no próprio texto, que "a tela de edição é da App 03", e o
`POST /v1/apoiadores/{id}/artefatos/{artefato_id}/anexacao` nasceu citando o `RF-02-101`. Hoje o
Admin não tem por onde publicar "Quem somos", "Contatos" e "Como apoiar", nem por onde anexar o
documento que o Apoiador declarou pela App 08 — o documento fica pendente e nunca vai a público.

A fatia também fecha **duas lacunas de contrato** que impedem as telas de existir, ambas
decididas pelo fundador em 2026-10-02:

- **O Admin não consegue ler o que vai editar.** A única leitura do conteúdo institucional é a
  pública, que omite o autor de propósito (`RF-03-45`). Mas o `RF-02-80` exige a tela "com autor
  e data do que publicou", e hoje autor e data só voltam na resposta do `PUT` — recarregar a
  página perde a informação.
- **O Admin não consegue alcançar a rota de anexação.** O `ArtefatoSaida` de
  `GET /v1/apoiadores` leva `endereco` e `rotulo`, mas **não leva o `id` do artefato nem a marca
  de publicado**. Sem o `id` a gestão não tem como chamar a anexação, e sem a marca não há como
  separar o que espera anexação do que já está público.

## What Changes

- **Nasce `GET /v1/conteudo-institucional`, restrito a Admin**, devolvendo as três seções com
  texto, link de vídeo, autor e data. A rota pública segue intacta e segue sem autor
  (`RF-03-45`).
- **O `ArtefatoSaida` de `GET /v1/apoiadores` passa a levar `id` e `publicado`.** Nenhuma rota
  nasce para isto: a fila da gestão se monta filtrando a listagem que já existe.
- **Tela de edição do conteúdo institucional na App 03** (`RF-02-80`): as três seções, o texto, o
  link de vídeo só em "Quem somos", e quem publicou e quando.
- **Fila dos comprobatórios pendentes e ato de anexação na App 03** (`RF-02-101`): o que o
  Apoiador declarou e ainda espera, com a anexação que o publica.

Nada do recorte original da fatia 16 além destes dois identificadores: o `RF-02-85` saiu pela
fatia 3 e a homologação do aporte declarado, pela fatia 11 — o cronograma já foi corrigido.

## Capabilities

### New Capabilities

Nenhuma. As três capacidades que a fatia toca já existem.

### Modified Capabilities

- `conteudo-institucional`: nasce a leitura de Admin, que devolve autor e data — o que a leitura
  pública não pode devolver (`RF-02-80`).
- `prova-do-apoio`: o Admin passa a ler o que espera anexação, com o identificador que a
  anexação exige e a marca de publicado (`RF-02-101`).
- `aplicacao-de-gestao`: as duas telas novas do Admin — a edição do institucional e a fila da
  anexação (`RF-02-80`, `RF-02-101`).

## Impact

| Alvo | O que muda |
| --- | --- |
| `backend/src/nucleo/conteudo_institucional/rotas.py` | rota de leitura restrita a Admin |
| `backend/src/nucleo/personas/rotas.py` | `ArtefatoSaida` ganha `id` e `publicado` |
| `apps/app-03-gestao/src/` | pasta nova do institucional; fila da anexação em `filas/` |
| `docs/prds/prd-02-frontend-de-gestao.md` §9 | a rota nova de leitura entra no contrato |
| `docs/09-topicos-em-aberto-e-sugestoes.md` §1 | as duas decisões de 2026-10-02 |

Sem migração de banco: nenhuma entidade nasce nem muda de forma — `publicado` é derivado, pelo
`artefato_esta_publicado()` que já existe. Nenhuma rota pública muda de contrato, e nenhum
arquivo nasce em `docs/`. A esteira do `backend/` e a da App 03 já existem.
