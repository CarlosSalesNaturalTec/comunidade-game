# Design

## Context

A tela da aula (`TelaDaAula.tsx`) segue o requisito "O Mestre confirma a presença e lança a
ocorrência de conduta" de `openspec/specs/area-do-mestre/spec.md`. `GET
/v1/guerreiros/vinculaveis` já devolve ao Mestre, paginado, nick e avatar dos Guerreiros e
Guerreiras ativos das comunidades dele. O nick é único sem distinção de maiúsculas
(`uq_nick_valor`, sobre `lower(valor)`).

## Goals / Non-Goals

**Goals:** o Mestre digita o nick em campo simples; a tela nunca manda ao núcleo texto que não
seja o `id` de um Guerreiro(a) encontrado.

**Non-Goals:** rota nova no núcleo; filtro pela comunidade da aula (o núcleo já recusa o
Guerreiro(a) fora do escopo da aula); sugestão ou autocompletar.

## Decisions

- **Campo de texto "Nick do Guerreiro(a)"** nos dois formulários, por decisão do fundador de
  2026-11-26. Descartado: seletor com a lista, que o fundador recusou.
- **Conversão nick → `id` na tela**: ao abrir, carrega todas as páginas de
  `/v1/guerreiros/vinculaveis` seguindo o `proximo_cursor`, como `TelaDeGuerreiros.tsx`, e monta
  um mapa `nick.trim().toLocaleLowerCase("pt-BR") → id`. No envio, o nick digitado passa pela
  mesma normalização. Descartado: rota de busca por nick no núcleo — seria contrato novo para o
  que a rota existente já resolve.
- Leitura da lista falhou: o envio diz em linguagem simples que não foi possível conferir o
  nick e pede para tentar de novo; a tela segue de pé.

## Risks / Trade-offs

- Nick digitado errado não sugere alternativa → a mensagem pede para conferir a grafia.
