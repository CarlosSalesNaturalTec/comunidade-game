## Context

Ver `proposal.md` — Why. O padrão de formulário atrás de toggle já existe em
`TelaDoAcervo` e `TelaDaAgenda` (`mostrarFormulario`, botão "Tombar exemplar" / "Nova aula").
O saldo por tipo de recurso já existe como `listarSaldosDoPontoDeApoio` em
`pontos-de-apoio/api.ts`, consumido hoje só por `TransferenciaDeSaldo`. `TelaDeRecursos` já
carrega `comunidades` e, a partir delas, os `pontosDeApoio` de todas — usado hoje para
rotular `ListaDeNecessidades`.

## Goals / Non-Goals

**Goals:**
- Aplicar o padrão de toggle já consolidado aos dois formulários de Recursos.
- Mostrar o saldo disponível por ponto de apoio em Recursos, sem nova rota.
- Esconder aula cancelada por padrão na Agenda, com opção de reexibir.

**Non-Goals:**
- Somar saldo entre pontos de apoio ou entre tipos — a rota do núcleo já apura por par
  ponto/tipo, e a spec (`aplicacao-de-gestao`) proíbe recalcular.
- Mudar a rota `/v1/aulas` ou `/v1/pontos-de-apoio/{id}/saldos` no backend.

## Decisions

- **Saldo em Recursos reaproveita a função existente**: `TelaDeRecursos` importa
  `listarSaldosDoPontoDeApoio` de `../pontos-de-apoio/api` em vez de duplicar a chamada em
  `recursos/api.ts` — mesma dependência cruzada que a tela já tem hoje para
  `listarPontosDeApoio`. Chama uma vez por ponto de apoio das comunidades carregadas
  (`Promise.all`), no mesmo molde que já monta `pontosDeApoio` para rotular necessidades.
  Alternativa descartada: criar rota agregada nova no núcleo — rejeitada por não ser
  necessária (poucos pontos de apoio por comunidade) e por exigir mudança de backend fora do
  recorte.
- **Dois estados de toggle independentes em `TelaDeRecursos`**: `mostrarFormularioDeAporte` e
  `mostrarFormularioDeMissao`, cada um controlando seu próprio formulário — os dois podem
  ficar abertos ao mesmo tempo, sem exclusão mútua, pois não compartilham dado nem ordem de
  preenchimento.
- **Filtro de canceladas é local ao componente, não parâmetro de API**: `TelaDaAgenda` guarda
  `exibirCanceladas` (padrão `false`) e filtra o array `aulas` antes de repassá-lo a
  `ListaDaAgenda` — a busca ao núcleo continua trazendo todas as situações do período/comunidade
  filtrados, como hoje.

## Risks / Trade-offs

- [N+1 chamadas de saldo, uma por ponto de apoio] → aceitável: mesmo padrão que a tela já usa
  para pontos de apoio, e o Ciclo 01 opera com poucas comunidades e poucos pontos cada.
- [Cancelada ainda trafega da API mesmo oculta] → aceito: manter a busca completa evita
  divergência entre o filtro local e o que o Admin decide reexibir, sem round-trip extra ao
  marcar o controle.
