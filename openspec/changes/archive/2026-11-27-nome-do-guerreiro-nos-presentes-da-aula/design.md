# Design

## Context

Aplica o padrão da fatia 37 (`2026-11-26-nome-do-guerreiro-na-lista-de-responsaveis`) à leitura
dos presentes da fatia 36: `GET /v1/aulas/{id}/presencas` já junta `Presenca`, `Persona` e
`Nick`, e `Persona.nome` é anulável. Contrato vigente em `openspec/specs/aula-e-presenca` e
`openspec/specs/area-do-mestre`.

## Goals / Non-Goals

**Goals:** o nome do Guerreiro(a) chega à lista de presentes da App 09.

**Non-Goals:** trocar o nick pelo nome nos formulários de presença e ocorrência; alterar
ordenação, escopo ou permissão da leitura.

## Decisions

1. **Campo `nome: str | None` em `PresencaDaAulaSaida`**, lido de `Persona.nome` na mesma
   consulta, sem junção nova. Descartado: rota própria para o nome — duas chamadas para o que a
   consulta já tem.
2. **Exibição `nick — nome`** ao lado do avatar, com "sem nome" quando o nome é nulo ou vazio,
   como a lista de responsáveis da App 09 (fatia 37). Descartado: omitir o nome ausente — a
   marca diz ao Mestre que o cadastro está incompleto.

## Risks / Trade-offs

- [Nome civil de criança numa leitura a mais] → a rota é só do Mestre das comunidades da aula e
  do Admin (`RN-09-08`), nunca superfície pública (invariante 12); imagem real segue proibida
  (`RN-09-18`).
