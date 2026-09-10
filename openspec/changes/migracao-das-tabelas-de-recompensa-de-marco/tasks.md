# Tarefas — migração das tabelas de recompensa de marco

Recorte em `proposal.md`; decisões em `design.md`. Nenhum requisito muda: as tarefas fazem
existir em produção o schema que `RF-09-71`, `RF-09-72`, `RF-09-76`, `RN-09-27` e `RF-07-13` já
supõem.

## 1. Migração

- [ ] 1.1 Criar a revisão em `backend/alembic/versions/`, a partir do head corrente, com
  `recompensa_de_marco` (FKs para `trilha`, `missao` e `tipo_de_recurso`, `quantidade` em
  `Numeric(12, 2)`, o índice `ix_recompensa_de_marco_trilha_id` e as colunas de `ComAutoria`)
  e, depois dela, `entrega_de_recompensa` (FKs para `recompensa_de_marco`, `persona`,
  `ponto_de_apoio` e `lancamento`, mais `ComAutoria`). Conferir o resultado contra
  `--autogenerate` e contra `recompensas_de_marco/modelo.py`, coluna a coluna; `downgrade`
  derruba as duas na ordem inversa (design — decisão 1).

## 2. Guarda contra a repetição

- [ ] 2.1 Em `backend/tests/test_migracoes.py` (novo), aplicar `alembic upgrade head` num banco
  vazio e comparar o schema resultante com `Base.metadata`: nenhuma tabela e nenhuma coluna do
  modelo pode faltar no banco migrado. A falha nomeia o que diverge, para que a mensagem baste
  sem depurar. Cobre também que a revisão nova sobe e desce sem erro (design — decisões 2 e 3).

## 3. Documentação

- [ ] 3.1 Registrar a change em `openspec/cronograma-de-fatias.md`: linha sem número no bloco
  do PRD-09, com o slug. Nada muda em `docs/`, em `docs/prds/index.md`, no documento 99 nem na
  `nav` do `mkdocs.yml` — a change não toma decisão nova, não altera requisito e não cria
  arquivo em `docs/`.
