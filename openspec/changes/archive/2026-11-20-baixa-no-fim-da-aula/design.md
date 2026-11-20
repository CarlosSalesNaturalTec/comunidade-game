# Design

## Context

A reserva da aula vive em `openspec/specs/reserva-de-recurso` e hoje sai pela baixa de
`consumir_reservas_da_aula`, chamada só por `lancar_atividade_realizada`. O núcleo já tem um
comando periódico, `python -m nucleo.manutencao` (documento 03 §12.2), cujo agendamento é da
implantação e não está no repositório. Esta fatia tira a baixa do ato humano.

## Goals / Non-Goals

**Goals:** varredura das aulas vencidas, nos dois disparos; situação `realizada_sem_lastro`;
lançamento por aula sem baixa; painel sem a pendência; transição na migração; rótulos.

**Non-Goals:** entrega pelo disponível (fatia 13), necessidade da recompensa (fatia 14), tela
para lançar resultado depois do fim da aula na App 03.

## Decisions

1. **`encerrar_aulas_vencidas(sessao, momento)` em `reservas/regra.py`**, ao lado de
   `consumir_reservas_da_aula`. Seleciona as aulas com `fim_em <= momento` em prevista, confirmada
   ou pendente de lastro, com `FOR UPDATE SKIP LOCKED`: duas varreduras simultâneas nunca pegam a
   mesma aula. Confirmada e prevista: baixa das reservas e `realizada`; pendente:
   `realizada_sem_lastro`, sem baixa.
2. **Autoria do sistema:** o débito leva `autor_id` do Admin que agendou a aula e
   `papel_do_autor = "sistema"`, no precedente da migração do piso, que gravou `"migracao"` com o
   autor da vigência anterior. `lancar_debito` e `consumir_reservas_da_aula` passam a aceitar a
   autoria explícita. Descartada: persona técnica "sistema" — criaria papel novo fora do
   documento 02.
3. **Valoração pela vigência no dia do fim da aula**, não pela de hoje: a baixa é do fato daquele
   dia. Sem vigência, a aula é pulada nesta varredura e o erro vai ao log; a operação que
   disparou a varredura segue.
4. **Disparo sob demanda por `varrer_aulas_vencidas(sessao)`**, que roda a varredura e faz
   `commit`, chamada no começo de: `GET /aulas`, `GET /vitrine/necessidades`,
   `GET /necessidades/minhas`, `GET /pontos-de-apoio/{id}/saldos`, `agendar_aula`,
   `cancelar_aula` e `tentar_reservar_aula_pendente`. O painel do dia fica de fora: a spec dele
   proíbe escrita por causa da consulta, e ele lê a aula em andamento, que não venceu.
   `executar_manutencao` ganha a mesma chamada como primeira etapa.
5. **`lancar_atividade_realizada`** só grava os Resultados: sai a baixa e a mudança de
   situação; recusa só a aula cancelada. O nome da função e a rota ficam, para não quebrar a App
   03.
6. **Cancelamento** recusa também `realizada_sem_lastro` e a aula com `fim_em` passado.
7. **Migração `e5a7c9b1d3f4`, transição** (`RF-07-56`): em SQL, para as aulas com
   `fim_em < now()` em prevista, confirmada ou pendente — reservas `reservada` → `liberada`;
   pendente → `realizada_sem_lastro`; as demais → `realizada`. Roda no Job de migração, antes da
   revisão nova do serviço, e por isso nenhuma varredura alcança essas aulas antes dela.

## Risks / Trade-offs

- **Escrita em rota de leitura**: as quatro leituras passam a poder gravar a baixa. É o custo da
  decisão de manter a situação certa sem depender do agendamento; a varredura é curta, indexável
  por `fim_em` e não trava quem já está varrendo.
- O comando de manutenção precisa ser agendado na implantação; até isso, a varredura sob demanda
  cobre.
- Lançar resultado depois do fim da aula continua possível pela rota, mas a área Lançamentos da
  App 03 só abre na aula vigente — limitação que segue como está.
