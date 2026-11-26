# Design

## Context

A tela da aula (`TelaDaAula.tsx`) segue o requisito "O Mestre confirma a presença e lança a
ocorrência de conduta" de `openspec/specs/area-do-mestre/spec.md`. O seletor de Guerreiro(a)
por nick já existe no vínculo do responsável (`FormularioDeResponsavel.tsx`), sobre
`GET /v1/guerreiros/vinculaveis` — paginada, restrita ao Mestre, só nick e avatar.

## Goals / Non-Goals

**Goals:** trocar o campo de identificador pelo seletor nos dois formulários; nunca mais
mandar ao núcleo texto que não seja o `id` de um Guerreiro(a) listado.

**Non-Goals:** rota nova no núcleo; filtro pela comunidade da aula (a rota não devolve a
comunidade, e o núcleo já recusa o Guerreiro(a) fora do escopo da aula).

## Decisions

- **Carregar todas as páginas** de `/v1/guerreiros/vinculaveis` ao abrir a tela, seguindo o
  `proximo_cursor`, como `TelaDeGuerreiros.tsx` — a primeira página sozinha esconderia parte da
  turma. Falha da leitura: aviso em linguagem simples, formulários seguem na tela.
- **Rótulo da opção**: só o nick, ordenado alfabeticamente (`localeCompare` pt-BR) — o Mestre
  procura pelo nome que a criança usa. Descartado: `nick — avatar`, do formulário do
  responsável, porque o nome do avatar não ajuda a achar ninguém.
- **Presença exclui os presentes** pelo `guerreiro_id` da lista já carregada; a ocorrência
  oferece todos, porque o motivo de conduta não depende de presença registrada na tela.
- `<select>` nativo com `<label>`, no molde do seletor de atividade da mesma tela.

## Risks / Trade-offs

- Comunidade com muitos Guerreiros(as) gera lista longa → aceitável no Ciclo 01; busca por
  digitação fica para quando o volume exigir.
