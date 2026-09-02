## Why

Fatia 15 do PRD-02 (`openspec/cronograma-de-fatias.md`, bloco "PRD-02 — Frontend de gestão"),
atendendo `RF-02-27`, `RF-02-28`, `RN-02-10` e `RN-02-11`, e — porque a publicação é o ato que
compromete a recompensa — também `RF-07-39` e `RF-07-40` do PRD-07.

A trava anotada na linha da fatia caiu: a entidade `DesafioExtra` entrou com a fatia 1 do
PRD-14, já com as guardas de lastro (`conferir_publicacao_com_lastro`), a imutabilidade do
publicado e a quantidade restante derivada. Falta a outra ponta: hoje toda proposta nasce em
`em_validacao_do_mestre` e **nenhum ato a tira de lá** — não há fila do Admin, não há aprovação,
e nenhum desafio chega a `publicado`. Sem a publicação, `RF-07-39` e `RF-07-40` — reserva e
liberação da recompensa — também não têm onde acontecer.

Duas decisões do fundador de 2026-09-02 orientam o recorte:

1. **O que encerra um desafio extra é um ato de Admin na gestão**, não o decurso da vigência. A
   regra vigente da `reserva-de-recurso` — nenhuma reserva muda de estado por decurso de prazo —
   fica intacta, e a reserva do desafio continua saindo só por ato humano. Como o PRD-02 §9 não
   declarava esse ato, o PRD ganha na mesma entrega o requisito e as rotas dele.
2. **A validação do Mestre não vem nesta fatia.** Ela é a fatia 15 do PRD-09; aqui a fila do
   Admin apenas filtra por quem já passou por ela, e nenhuma rota do PRD-09 é antecipada.

## What Changes

- **Fila do Admin** no núcleo: rota que devolve só os desafios em **aprovação do Admin** — os já
  validados pelo Mestre da trilha. Proposta ainda em validação do Mestre NUNCA aparece
  (`RF-02-27`, `RN-02-10`).
- **Aprovação e recusa** pelo Admin: a aprovação publica o desafio e é recusada com **422** sem o
  lastro da recompensa registrado e com **409** sobre desafio que não passou pela validação do
  Mestre; a recusa grava o motivo, que a leitura do proponente já devolve (`RF-02-28`,
  `RN-02-10`, `RN-02-11`).
- **A publicação reserva a recompensa** — a quantidade disponível do tipo de recurso no ponto de
  apoio declarado —, e sem disponível a publicação é recusada, mesmo com o lastro apurado
  (`RF-07-39`).
- **Encerramento pelo Admin**: ato novo que fecha o desafio publicado e leva a reserva ainda
  `reservada` a `liberada`, devolvendo o saldo. Desafio encerrado não recebe conclusão nova
  (`RF-07-40`).
- **A reserva passa a servir aula ou desafio extra**, como o PRD-07 §8 já descreve a entidade:
  `aula_id` e `desafio_extra_id` mutuamente exclusivos, com migração.
- **Natureza "desafios extras" na área Filas da App 03** — não uma área nova, como a própria
  spec da gestão exige: a fila dos pendentes com o que cada proposta oferece e o que falta de
  lastro, a aprovação e a recusa com motivo, a lista dos publicados e o encerramento.
- **O PRD-02 ganha `RF-02-106`** (o Admin encerra o desafio extra publicado, liberando a reserva
  da recompensa não entregue) e as duas rotas dele na §9, por decisão do fundador de 2026-09-02
  — gravada antes no documento 04 §3, que é a fonte das regras do desafio extra, e no
  documento 09 §1.

**Fora do escopo**, como o PRD e o cronograma já excluem: a **validação do Mestre da trilha**
(`RF-09-51`, `RF-09-52`, fatia 15 do PRD-09); o **ato de registrar a conclusão** de um desafio —
atribuir a recompensa, baixar a reserva e creditar os pontos extras —, que o cronograma deixa
para uma fatia do PRD-09 ainda sem número; a **tela do Apoiador** para acompanhar o desfecho,
já entregue pela fatia 1 do PRD-14; e a **trilha de auditoria** desta aplicação, adiada ao
Ciclo 02.

## Capabilities

### New Capabilities

Nenhuma.

### Modified Capabilities

- `desafio-extra`: ganha a fila do Admin, a aprovação e a recusa com motivo, a publicação que
  reserva a recompensa e o encerramento que a libera.
- `reserva-de-recurso`: a reserva passa a vincular **aula ou desafio extra**, e ganha a saída
  por encerramento do desafio — sem afrouxar a regra de que nenhuma reserva sai por prazo.
- `aplicacao-de-gestao`: ganha a área Desafios extras da App 03.

## Impact

- `backend/src/nucleo/desafios_extras/`: `modelo.py` (encerramento), `regra.py` (fila,
  aprovação, recusa, publicação com reserva, encerramento) e `rotas.py` (três rotas novas).
- `backend/src/nucleo/reservas/`: `modelo.py` (`aula_id` opcional e `desafio_extra_id`) e
  `regra.py` (reservar e liberar pelo desafio).
- `backend/alembic/versions/`: uma migração para a reserva e uma para o desafio.
- `backend/tests/`: testes de regra e de rota.
- `apps/app-03-gestao/src/filas/`: a natureza nova no filtro, a tela do desafio e o cliente
  dela. Nenhuma área nova na navegação, e `App.tsx` não muda.
- Documentação: documento 04 §3 e documento 09 §1 (a decisão nova), PRD-02 §§6, 9, 12 e 15
  (`RF-02-106` e as rotas), PRD-07 §14 (a nota que remetia `RF-07-39` e `RF-07-40` a outro PRD),
  documento 99 §8 (a mesma remissão) e a linha da fatia 15 no
  `openspec/cronograma-de-fatias.md`.
