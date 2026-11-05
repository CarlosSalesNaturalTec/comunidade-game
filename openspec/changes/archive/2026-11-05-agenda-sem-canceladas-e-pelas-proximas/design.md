# Design

## Context

A leitura da agenda está em `openspec/specs/aula-e-presenca/spec.md` ("A gestão lê a agenda") e
a tela em `openspec/specs/aplicacao-de-gestao/spec.md` ("A aplicação apresenta a agenda").
`listar_agenda_rota` (`backend/src/nucleo/aulas/rotas.py`) pagina por cursor de conjunto
`(inicio_em, id)` crescente, 25 por página (`paginacao_tamanho_padrao`). `TelaDaAgenda.tsx` lê
só a primeira página e esconde a cancelada localmente.

## Goals / Non-Goals

**Goals:** a cancelada fora da leitura por padrão; a próxima aula na primeira página.

**Non-Goals:** "carregar mais" na App 03 — com a ordem nova, o que passa da primeira página são
as aulas terminadas mais antigas; filtro genérico por situação; mexer em
`GET /v1/aulas/vigentes`.

## Decisions

1. **Filtro `incluir_canceladas`**, declarado em `contrato_de_listagem(frozenset(...))` da rota.
   Ausente ou `false` acrescenta `Aula.situacao != cancelada`; `true` não filtra; outro valor →
   `ErroDeValidacao` com `campo="incluir_canceladas"` (422). Descartado: `situacao=` genérico —
   cobre caso que ninguém pediu.
2. **Dois grupos, duas consultas.** Momento de referência `ref` = `agora()` na primeira página.
   Grupo `por_vir`: `fim_em > ref`, ordem `(inicio_em, id)` crescente. Grupo `terminadas`:
   `fim_em <= ref`, ordem `(inicio_em, id)` decrescente. A página consulta o grupo do cursor com
   `limit(tamanho + 1)`; se o grupo `por_vir` acaba antes de encher a página, completa com o
   início de `terminadas`. A aula em curso fica no topo, por não ter terminado. Descartado: uma
   consulta só com `ORDER BY CASE` — o cursor de conjunto não comporta direção mista.
3. **Cursor** passa a `{"grupo", "ref", "inicio_em", "id"}`, codificado por `codificar_cursor`.
   `ref` viaja no cursor para a divisão não mudar entre páginas. Cursor sem esses campos →
   422 "Cursor de paginação inválido", como hoje.
4. **Filtros de comunidade e período** continuam aplicados antes da divisão, nos dois grupos.
5. **App 03**: `FiltroDeAgenda` ganha `incluirCanceladas`; `api.ts` envia
   `incluir_canceladas=true` só quando marcado; `exibirCanceladas` entra nas dependências de
   `carregar`, e `aulasApresentadas` sai — `ListaDaAgenda` recebe `aulas` direto.

## Risks / Trade-offs

- [Comunidade com mais de 25 aulas por vir esconde as mais distantes] → aceito: o filtro de
  período alcança; paginação na tela fica para quando houver o caso.
- [Marcar o controle refaz a consulta] → aceito: é uma ida ao núcleo, contra trazer sempre todas.
