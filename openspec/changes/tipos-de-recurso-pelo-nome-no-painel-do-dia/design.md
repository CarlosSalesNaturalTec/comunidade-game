## Context

A leitura do painel já está consolidada em `openspec/specs/painel-do-dia/spec.md`. O núcleo
monta tudo numa leitura só (`montar_painel_do_dia`), que a App 03 consulta a cada 10 segundos.
Hoje `RecursoProvidoSaida` e `SaldoDoTipoSaida` levam só `tipo_de_recurso_id`, e a tela o
imprime como está.

## Decisions

- **O nome e a unidade vêm do núcleo, na própria resposta do painel.** É o padrão de
  `AtividadePrevistaSaida.missao_titulo` e da rota `GET /v1/pontos-de-apoio/{id}/saldos`, que
  já devolve o `nome` do tipo. Os campos novos são `tipo_de_recurso_nome` e
  `tipo_de_recurso_unidade`, ao lado do `tipo_de_recurso_id`, que continua na resposta. A
  leitura é uma consulta a `TipoDeRecurso` pelos identificadores do conjunto, sem um acesso
  por item.
  - Descartado: a tela cruzar o painel com `GET /v1/tipos-de-recurso`. Seriam duas leituras
    por sondagem, e a tela ficaria sem nome se o catálogo falhasse.
- **Exibição:** `nome: quantidade unidade`, por exemplo "Kit MDF: 10.00 kits". O número fica
  como o núcleo o serve, sem formatação nova.

## Risks / Trade-offs

- Nenhuma migração e nenhuma rota nova. Um cliente antigo ignora os campos a mais.
