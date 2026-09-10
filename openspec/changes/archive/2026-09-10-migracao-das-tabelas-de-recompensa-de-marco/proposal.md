# Migração das tabelas de recompensa de marco

Origem: **PRD-09** (fatia 13, `Recompensa por desbloqueio e duplicação de trilha` — `RF-09-71`,
`RF-09-72`, `RF-09-75`, `RF-09-76`, `RN-09-27`) e **PRD-07** (`RF-07-13`). A fatia está
`implementado` no cronograma e **não está no ar**: subiu com modelo e sem migração. Esta change
não abre fatia nova — conserta a entrega daquela. Entra no cronograma como linha sem número no
bloco do PRD-09.

## Why

`recompensa_de_marco` e `entrega_de_recompensa` existem como modelo em
`recompensas_de_marco/modelo.py` e **não existem em migração nenhuma**. Em produção, toda
chamada à listagem de recompensas de marco responde 500:

```text
psycopg.errors.UndefinedTable: relation "recompensa_de_marco" does not exist
```

Comparando os 85 `__tablename__` do núcleo com os `create_table` das 67 migrações, faltam
exatamente estas duas. As demais 83 estão cobertas.

A suíte não pega porque `tests/conftest.py` monta o schema com `Base.metadata.create_all`, que
nunca executa o Alembic: o teste roda contra um schema que produção não tem. O Job de migração
do deploy também "passa" — não há revisão pendente a aplicar. Nada no caminho entre o commit e
o Cloud Run compara as duas coisas, e por isso a fatia foi dada por entregue.

## What Changes

- Migração nova que cria `recompensa_de_marco` e `entrega_de_recompensa`, com as chaves
  estrangeiras, o índice e as colunas de `ComAutoria` que o modelo declara.
- **Guarda contra a repetição:** teste que aplica as migrações num banco vazio e compara o
  schema resultante com `Base.metadata`. Divergência quebra a esteira — é o que teria pego esta
  fatia antes do merge, e pega a próxima.
- Nenhuma mudança de comportamento, rota, regra ou modelo: as tabelas passam a existir onde o
  código sempre supôs que existissem.

## Capabilities

### New Capabilities

Nenhuma.

### Modified Capabilities

Nenhuma. `recompensa-de-marco` já especifica o comportamento e segue valendo palavra por
palavra — a change entrega o schema que a implementação daquela fatia deixou de entregar.
Comportamento não muda, logo spec não muda: `skip_specs: true`.

## Impact

| Área | O que muda |
| --- | --- |
| `backend/alembic/versions/` | uma revisão nova, no head corrente |
| `backend/tests/` | o teste de paridade entre migrações e `Base.metadata` |
| `openspec/cronograma-de-fatias.md` | linha sem número no bloco do PRD-09 |

Sem dependência de outra change. Não toca `docs/`: não há decisão nova — a fatia 13 já foi
decidida e aprovada, e esta change apenas a faz existir no banco.

**Risco de dado:** nenhum. As tabelas não existem, logo não há linha a preservar nem a migrar.
