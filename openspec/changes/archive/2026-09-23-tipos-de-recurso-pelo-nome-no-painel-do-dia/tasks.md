## 1. Núcleo

- [x] 1.1 Em `backend/src/nucleo/painel_do_dia/regra.py`, acrescentar `tipo_de_recurso_nome` e
      `tipo_de_recurso_unidade` a `RecursoProvidoSaida` e a `SaldoDoTipoSaida`, preenchidos
      por uma consulta única a `TipoDeRecurso` em `_recursos_providos` e em
      `_saldo_do_ponto_de_apoio` (`RF-02-44`, `RF-02-45`)

## 2. App 03

- [x] 2.1 Em `apps/app-03-gestao/src/painel-do-dia/api.ts`, acrescentar os dois campos a
      `RecursoProvido` e a `SaldoDoTipo` (`RF-02-44`, `RF-02-45`)
- [x] 2.2 Em `TelaDoPainelDoDia.tsx`, exibir recursos providos e saldo como
      `nome: quantidade unidade`, sem o identificador (`RF-02-44`, `RF-02-45`)

## 3. Testes

- [x] 3.1 Em `backend/tests/test_painel_do_dia.py`, conferir nome e unidade na reserva e no
      saldo (cenários "O previsto e o provido saem juntos", "O saldo é o do ponto de apoio da
      aula" e "O tipo de recurso aparece pelo nome e pela unidade")
- [x] 3.2 Em `painel-do-dia.test.tsx`, conferir que a tela mostra nome, quantidade e unidade e
      não mostra o identificador (cenário "O tipo de recurso aparece pelo nome e pela
      unidade")

## 4. Documentação

- [x] 4.1 Marcar a fatia 21 do PRD-02 como `implementado` em `openspec/cronograma-de-fatias.md`,
      com o slug da change. `docs/` não muda: o PRD-02 §5.5.3 já pede o nome e a unidade, e
      não há decisão nova
