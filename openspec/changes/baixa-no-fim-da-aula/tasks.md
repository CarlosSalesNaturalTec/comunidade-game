# Tasks

## 1. Núcleo — situação, varredura e baixa do sistema

- [ ] 1.1 `aulas/modelo.py`: `SituacaoDaAula.realizada_sem_lastro` (`RF-07-55`, `RN-02-09`).
- [ ] 1.2 `livro_razao/regra.py` e `reservas/regra.py`: autoria explícita no débito e em
      `consumir_reservas_da_aula`, valoração pelo dia do fim da aula, e
      `encerrar_aulas_vencidas` com `FOR UPDATE SKIP LOCKED` e `varrer_aulas_vencidas`
      (`RF-07-09`, `RF-07-55`, `RN-07-43`, `RF-01-91`).
- [ ] 1.3 Disparos: `manutencao.py`, agenda (`aulas/rotas.py`), necessidades pública e do
      Mestre, saldos do ponto de apoio, `agendar_aula`, `cancelar_aula` e
      `tentar_reservar_aula_pendente` (`RF-01-91`).
- [ ] 1.4 `aulas/regra.py` (`cancelar_aula`), `pontos_de_apoio/regra.py` e
      `painel_do_dia/regra.py`: a situação nova não se cancela nem bloqueia a desativação, e o
      cancelamento recusa a aula que já terminou; o painel não lista mais a atividade realizada
      (`RF-07-55`, `RF-02-46`, `RF-02-47`).
- [ ] 1.5 `resultados/regra.py` (`lancar_atividade_realizada`): grava só os Resultados, sem
      baixa nem mudança de situação; recusa só a aula cancelada (`RF-02-33`, `RF-02-35`).
- [ ] 1.6 Migração Alembic com a transição das aulas já terminadas (`RF-07-56`).

## 2. Núcleo — testes

- [ ] 2.1 `tests/test_baixa_no_fim_da_aula.py`: varredura da confirmada, da pendente e da sem
      recurso; débito com papel sistema e vigência do dia do fim; repetição sem segundo débito;
      aula sem vigência pulada; disparo pela agenda e pela necessidade (`RF-07-09`, `RF-07-55`,
      `RN-07-43`, `RF-01-91`).
- [ ] 2.2 Ajuste dos testes de lançamento, cancelamento, painel e reserva ao comportamento novo
      (`RF-02-33`, `RF-02-35`, `RF-02-46`, `RF-02-47`, `RF-07-09`).
- [ ] 2.3 `tests/test_migracoes.py`: a aula terminada tem a reserva liberada, sem débito, e a
      pendente vira realizada sem lastro (`RF-07-56`).

## 3. Aplicações

- [ ] 3.1 App 03, `lancamentos/`: a mensagem e os rótulos deixam de falar em fechamento e baixa,
      com teste (`RF-02-33`, `RF-02-35`).
- [ ] 3.2 App 03, `agenda/ListaDaAgenda.tsx`, e App 09, `turmas/TelaDeMinhasTurmas.tsx`: rótulo
      "Realizada sem lastro", com teste (`RN-02-09`, `RF-07-55`).

## 4. Documentação

- [ ] 4.1 Fatia 12 do PRD-07 como implementada em `openspec/cronograma-de-fatias.md`, com o slug.
      No documento 09, a linha "Consumo do encontro e recompensa de marco" recebe o disparo
      decidido — comando periódico e varredura sob demanda — e o autor da baixa gravado com o
      papel sistema. Os PRDs não mudam.
