# Design

## Context

O catálogo de tipos de recurso está em `openspec/specs/catalogo-de-tipos-de-recurso` e já tem
uma trava de **escolha nova**: o tipo desativado é recusado só quando alguém o escolhe, por
`exigir_tipo_de_recurso_ativo` (`RF-07-52`). A recusa do durável na aula, no item avulso e no
desafio extra também já existe, cada uma no seu `regra.py`. A finalidade segue os dois padrões.

## Goals / Non-Goals

**Goals:** finalidade no tipo, nas três escritas do catálogo e na leitura; recusa da finalidade
errada nas quatro escolhas novas; migração dos tipos existentes; seletores das Apps 03 e 09.

**Non-Goals:** baixa no fim da aula, entrega pelo disponível e necessidade da recompensa
(fatias 12 a 14); seletor nas telas da App 08, que informam o tipo pelo identificador.

## Decisions

1. **Coluna `finalidade` anulável em `tipo_de_recurso`**, com enum `FinalidadeDoRecurso`
   (`consumo_do_encontro`, `recompensa`) e `CheckConstraint`: nula se, e só se, a natureza é
   durável. A trava de banco garante o `RN-07-41` mesmo fora da regra. Descartada: marca
   booleana `eh_recompensa` — deixaria o durável com um valor sem sentido.
2. **Guarda única `exigir_finalidade(tipo, esperada, campo)`** em `recursos/regra.py`, ao lado
   de `exigir_tipo_de_recurso_ativo`, chamada só nas escolhas novas: `agendar_aula`
   (consumo do encontro), `declarar_recompensa_de_marco`, cadastro do item do catálogo avulso e
   proposta do desafio extra (recompensa). Ela recusa toda finalidade diferente da esperada,
   inclusive a nula do durável: a recompensa de marco e a proposta do desafio extra, que hoje só
   recusam o durável na entrega e na aprovação, passam a recusá-lo na escolha. Na aula e no item
   avulso, a guarda de natureza que já existe roda antes e mantém a mensagem. Entrega, troca,
   publicação do desafio, reserva e aporte NEVER a chamam: seguem fato já gravado.
3. **Escritas do catálogo:** `POST /tipos-de-recurso` exige a finalidade no não durável e a
   recusa no durável; `PATCH /tipos-de-recurso/{id}` aceita a finalidade, que só o Admin
   corrige, com a mesma recusa no durável; `GET /tipos-de-recurso` devolve `finalidade`.
4. **Migração Alembic** em três passos: cria a coluna anulável, grava `recompensa` em todo tipo
   não durável, cria a `CheckConstraint`. Nenhuma outra tabela é tocada.
5. **Filtro nas aplicações pelo campo da leitura**, sem rota nova: o formulário de agendamento
   da App 03 filtra `consumo_do_encontro`, a declaração de recompensa da App 09 filtra
   `recompensa`, os dois somando ao filtro de ativo que já existe.

## Risks / Trade-offs

- **Logo após a implantação, a aula não aceita lanche nem material** até o Admin corrigir esses
  tipos para consumo do encontro: é a consequência da migração decidida pelo fundador. A
  entrega da change avisa quais tipos corrigir.
- Aula já agendada com tipo que a migração marca como recompensa — as de 2026-11-07 e
  2026-11-14 — segue com a reserva. A liberação dela é da fatia 12 (`RF-07-56`).
