## 1. Modelo da reserva e do recurso declarado

- [x] 1.1 Criar `backend/src/nucleo/reservas/modelo.py` com `EstadoDaReserva` (reservada,
      consumida, liberada) e `Reserva` — aula, tipo de recurso, quantidade em `NUMERIC(12, 2)`,
      ponto de apoio, estado, autor e momento (`RF-07-08`, `RN-07-04`, `RF-01-03`,
      design — Decisions 1, 3)
- [x] 1.2 Criar `RecursoDeclaradoDaAula` em `backend/src/nucleo/aulas/modelo.py` — aula, tipo de
      recurso e quantidade —, separado da `Reserva` porque a aula pendente de lastro precisa
      lembrar o que lhe falta (`RF-07-08`, design — Decisions 1)
- [x] 1.3 Acrescentar `SituacaoDaAula` (prevista, pendente de lastro, confirmada, realizada,
      cancelada) e a coluna `situacao` a `Aula`, com o motivo do cancelamento (`RF-01-72`,
      `RF-07-09`, PRD-01 §8, design — Decisions 9)
- [x] 1.4 Acrescentar `aula_id` obrigatório a `Resultado` em `resultados/modelo.py`
      (`RF-07-09`, `RF-02-35`, design — Decisions 8)
- [x] 1.5 Gerar a migration Alembic com as duas tabelas novas, o índice composto
      `(tipo_de_recurso_id, ponto_de_apoio_id, estado)`, as colunas de `aula` e o `aula_id` de
      `resultado` (design — Migration Plan)

## 2. Saldo disponível

- [x] 2.1 Escrever `quantidade_reservada(sessao, tipo, ponto_de_apoio)` em
      `reservas/regra.py`, por agregação sobre as reservas no estado reservada, sem tabela de
      saldo (`RF-07-07`, design — Decisions 2)
- [x] 2.2 Escrever `disponivel_de(sessao, tipo, ponto_de_apoio)` — o saldo derivado dos
      lançamentos menos o reservado (`RF-07-07`, `RF-07-08`, design — Decisions 2)
- [x] 2.3 Verificar que a reserva não altera o saldo derivado e que a disponível cai por ela
      (`RF-07-07`, spec `reserva-de-recurso` e `livro-razao`)

## 3. Reserva no agendamento

- [x] 3.1 Estender `agendar_aula(...)` em `aulas/regra.py` para receber os recursos declarados,
      recusando quantidade menor ou igual a zero e tipo inexistente com 422 (`RF-07-08`,
      `RF-01-27`)
- [x] 3.2 Avaliar a disponível de cada tipo declarado dentro da transação, com
      `SELECT ... FOR UPDATE` sobre o par tipo/ponto de apoio (`RF-07-08`, design — Decisions 4)
- [x] 3.3 Havendo disponível para todos, gravar uma `Reserva` por recurso e a aula como
      **confirmada**; faltando qualquer parcela, gravar a aula como **pendente de lastro** sem
      reserva alguma (`RF-07-08`, `RN-07-01`, design — Decisions 4)
- [x] 3.4 Aula sem recurso declarado nasce **confirmada**, sem reserva (`RF-07-08`, spec
      `aula-e-presenca`)
- [x] 3.5 Verificar os três desfechos do agendamento e a ausência de reserva parcial
      (`RF-07-08`, `RN-07-01`, PRD-07 §12)

## 4. Confirmação pelo aporte

- [x] 4.1 Escrever `confirmar_aulas_pendentes(sessao, tipo, ponto_de_apoio, operador)` em
      `reservas/regra.py`: varre as aulas pendentes de lastro daquele ponto de apoio, ordenadas
      pelo horário inicial, e confirma as que couberem (`RN-07-37`, design — Decisions 5)
- [x] 4.2 Chamar a confirmação em `aportes/regra.py` logo depois de `lancar_credito`, nas três
      formas que creditam — registro da gestão, absorção e homologação do pré-cadastro
      (`RN-07-37`, `RN-07-35`, design — Decisions 5)
- [x] 4.3 Verificar que aporte que fecha a falta confirma a aula, que aporte insuficiente não
      confirma nada, que aporte em outro ponto de apoio não alcança a aula e que a aula de
      horário mais próximo é atendida primeiro (`RN-07-37`, spec `aporte`)

## 5. Baixa pelo lançamento da atividade

- [x] 5.1 Escrever `lancar_debito(...)` em `livro_razao/regra.py`, no ponto de apoio da aula que
      consumiu (`RF-07-09`, `RN-07-36`)
- [x] 5.2 Escrever `lancar_atividade_realizada(sessao, aula, resultados, operador)` em
      `resultados/regra.py`: grava os `Resultado` de todos os participantes, converte cada
      reserva em débito, leva as reservas a **consumida** e a aula a **realizada**, tudo na mesma
      transação (`RF-07-09`, `RF-02-35`, `RF-01-16`, design — Decisions 7)
- [x] 5.3 Recusar com 422 o lançamento em aula já realizada ou já cancelada (`RF-07-09`,
      spec `aula-e-presenca`)
- [x] 5.4 Verificar que a baixa gera um débito por reserva, que o saldo cai pelo débito e que
      aula sem reserva apenas registra os resultados (`RF-07-09`, PRD-07 §12)

## 6. Cancelamento e liberação

- [x] 6.1 Escrever `cancelar_aula(sessao, aula, operador, motivo)` em `aulas/regra.py`: aceita
      Admin ou Mestre com vínculo na comunidade da aula, exige motivo e recusa os demais com 403
      (`RF-01-72`, `RF-01-17`, `RF-02-95`, design — Decisions 10)
- [x] 6.2 Levar as reservas da aula a **liberada**, devolvendo as quantidades à disponível
      (`RF-07-09`, spec `reserva-de-recurso`)
- [x] 6.3 Recusar com 422 o cancelamento de aula já realizada ou já cancelada (`RF-01-72`,
      spec `aula-e-presenca`)
- [x] 6.4 Verificar que a reserva **não expira**: aula cuja data passou sem lançamento nem
      cancelamento mantém as reservas no estado reservada (`RF-07-09`, PRD-07 §5.3)

## 7. Rotas

- [x] 7.1 Criar `backend/src/nucleo/aulas/rotas.py` com `POST /aulas`, de Admin, que agenda e
      dispara a reserva, devolvendo a situação e o que falta (`RF-07-08`, `RF-02-31`,
      `RF-01-16`)
- [x] 7.2 Acrescentar `POST /aulas/{id}/reservas`, de gestão, idempotente: tenta a reserva de
      aula pendente de lastro e devolve o estado corrente quando já confirmada (PRD-07 §9,
      design — Decisions 6)
- [x] 7.3 Acrescentar `POST /aulas/{id}/lancamentos`, de Admin, com os resultados dos
      participantes (`RF-07-09`, `RF-02-35`)
- [x] 7.4 Acrescentar `POST /aulas/{id}/cancelamento`, de Admin ou Mestre da comunidade, com
      motivo (`RF-01-72`, `RF-02-95`)
- [x] 7.5 Registrar o roteador em `principal.py`, sob `/v1` e a chave de aplicação (`RF-01-02`)
- [x] 7.6 Verificar a matriz de permissões das quatro rotas e o formato único de erro
      (`RF-01-16`, `RF-01-27`)

## 8. Esteira e documentação

- [x] 8.1 Ajustar os testes existentes que criam `Resultado` sem aula (`test_resultado.py` e os
      de pontuação) e os que agendam aula sem recursos declarados (design — Risks)
- [x] 8.2 Rodar `ruff format --check .`, `ruff check .` e `pytest` no `backend/`
- [x] 8.3 Atualizar a narrativa da fatia entregue em `docs/prds/index.md` — o PRD-07 segue **em
      implementação** e o PRD-01 fecha o `RF-01-72`
- [x] 8.4 Rodar `npm run fix`, `npm run lint` e `mkdocs build --strict` antes de abrir o PR
