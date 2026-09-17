## 1. Saldo disponível em Recursos

- [ ] 1.1 Em `recursos/TelaDeRecursos.tsx`, importar `listarSaldosDoPontoDeApoio` de
      `../pontos-de-apoio/api` e carregar o saldo de cada ponto de apoio das comunidades já
      listadas (`Promise.all`, mesmo molde do carregamento de `pontosDeApoio` existente)
      (`RF-02-45`, `RF-02-97`).
- [ ] 1.2 Criar `recursos/ListaDeSaldosDisponiveis.tsx`, que recebe o saldo por ponto de apoio
      e apresenta sem somar entre pontos; estado vazio explícito quando não há saldo (`RF-02-45`,
      `RF-02-58`).
- [ ] 1.3 Encaixar `ListaDeSaldosDisponiveis` em `TelaDeRecursos.tsx`, ao lado de
      `ListaDeNecessidades`.

## 2. Toggle dos formulários em Recursos

- [ ] 2.1 Em `TelaDeRecursos.tsx`, envolver `RegistroDeAporte` num toggle próprio
      (`mostrarFormularioDeAporte`, botão "Registrar aporte"), no mesmo padrão de
      `TelaDoAcervo`/`TelaDaAgenda`.
- [ ] 2.2 Envolver `PublicacaoDeMissao` num segundo toggle independente
      (`mostrarFormularioDeMissao`, botão "Publicar missão").
- [ ] 2.3 Fechar o formulário correspondente ao concluir o registro do aporte ou a publicação
      da missão (reaproveitar `onRegistrado`/`onPublicada` já existentes).

## 3. Toggle do formulário e saldo em Agenda

- [ ] 3.1 Em `agenda/TelaDaAgenda.tsx`, envolver `FormularioDeAgendamento` num toggle
      (`mostrarFormulario`, botão "Nova aula"), mantendo o filtro de comunidade e período
      sempre visível (`RF-02-12`, `RF-02-30`).

## 4. Filtro de canceladas em Agenda

- [ ] 4.1 Em `TelaDaAgenda.tsx`, adicionar estado `exibirCanceladas` (padrão `false`) e um
      checkbox "Exibir canceladas"; filtrar `aulas` (excluindo `situacao === "cancelada"`
      quando desmarcado) antes de passar a `ListaDaAgenda` (`RN-02-09`, `RN-02-20`).
- [ ] 4.2 Confirmar que a busca ao núcleo (`listarAgenda`) continua trazendo todas as
      situações do período/comunidade filtrados — o filtro de canceladas é só de
      apresentação, sem parâmetro novo na chamada.

## 5. Testes

- [ ] 5.1 Em `recursos/recursos.test.tsx`, cobrir: saldo disponível aparece por ponto de apoio
      sem somar entre pontos; estado vazio sem saldo; os formulários de aporte e de missão
      abrem e fecham pelo próprio toggle, independentes um do outro (cenários da requirement
      "A App 03 abre a área Recursos" em `specs/aplicacao-de-gestao/spec.md`).
- [ ] 5.2 Em `agenda/agenda.test.tsx`, cobrir: aula cancelada não aparece por padrão; aparece
      com o motivo ao marcar "Exibir canceladas"; filtro de comunidade e período continua
      visível com o formulário fechado; formulário de nova aula abre e fecha pelo toggle
      (cenários da requirement "A aplicação apresenta a agenda das aulas").

## 6. Documentação

- [ ] 6.1 Marcar a fatia 20 como `implementado` em `openspec/cronograma-de-fatias.md`, com o
      slug desta change na coluna Recorte. Nenhum outro documento muda: a change não altera
      RF, RN, documento-fonte nem a situação do PRD-02 em `docs/prds/index.md`.
