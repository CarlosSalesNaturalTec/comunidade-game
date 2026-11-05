# Tasks

## 1. Núcleo — leitura da agenda

- [ ] 1.1 `listar_agenda_rota` declara o filtro de domínio `incluir_canceladas`, exclui a
      cancelada quando ausente ou `false` e recusa com 422 outro valor (`RF-02-12`, `RF-01-28`)
- [ ] 1.2 `listar_agenda_rota` ordena pelas próximas aulas em dois grupos, com `ref` fixado na
      primeira página e o cursor `{grupo, ref, inicio_em, id}`, mantendo os filtros de comunidade
      e período e o escopo do Mestre (`RF-01-28`, `RF-02-12`, `RF-01-18`)

## 2. App 03 — agenda

- [ ] 2.1 `api.ts`: `FiltroDeAgenda.incluirCanceladas` envia `incluir_canceladas=true` só quando
      marcado (`RF-02-12`)
- [ ] 2.2 `TelaDaAgenda.tsx`: o controle "Exibir canceladas" passa à busca, o filtro local
      `aulasApresentadas` e o comentário que o ancorava em `RN-02-09`/`RN-02-20` saem
      (`RF-02-12`)

## 3. Testes

- [ ] 3.1 `backend/tests/test_aula_rota.py`: cenários "A cancelada fica fora da agenda por
      padrão", "A cancelada vem quando pedida", "Valor inválido no filtro de canceladas é
      recusado", "Muitas canceladas antigas não escondem a próxima aula", "As próximas aulas vêm
      antes das já terminadas" e "A paginação atravessa os dois grupos sem repetir nem pular";
      ajustar os testes existentes que supunham ordem crescente ou cancelada no padrão
      (`RF-02-12`, `RF-01-28`)
- [ ] 3.2 `apps/app-03-gestao/src/agenda/agenda.test.tsx`: cenários "Aula cancelada some da
      lista por padrão", "Marcar o controle busca as canceladas", "Aula cancelada mostra o
      motivo" e "Aula prevista aparece mesmo com muitas canceladas" (`RF-02-12`)

## 4. Documentação

- [ ] 4.1 `openspec/cronograma-de-fatias.md`: a linha sem número "Agenda sem canceladas e pelas
      próximas aulas" do PRD-02 vira `implementado` com o slug da change; o documento 09 §1 já
      recebeu a decisão ao abrir a change; nenhum PRD, `docs/prds/index.md`, documento 99 nem
      `nav` muda
