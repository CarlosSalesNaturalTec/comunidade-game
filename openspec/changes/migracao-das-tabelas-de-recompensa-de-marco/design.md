# Design — migração das tabelas de recompensa de marco

## Context

Motivação em `proposal.md` — Why. O que o desenho precisa saber:

- O modelo está escrito e correto (`recompensas_de_marco/modelo.py`): `RecompensaDeMarco` com
  três chaves estrangeiras (`trilha`, `missao`, `tipo_de_recurso`), `quantidade` em
  `Numeric(12, 2)` e um índice por `trilha_id`; `EntregaDeRecompensa` com quatro
  (`recompensa_de_marco`, `persona`, `ponto_de_apoio`, `lancamento`). As duas herdam
  `ComAutoria`.
- `tests/conftest.py:152` usa `Base.metadata.create_all(motor)`. É uma escolha legítima — a
  suíte é rápida e não depende da cadeia de revisões —, mas deixa migração e modelo livres para
  divergir sem que nada acuse.
- O `backend-deploy.yml` roda `alembic upgrade head` como Job antes do serviço. O Job cumpriu o
  que lhe cabia: não havia revisão a aplicar.

## Goals / Non-Goals

**Goals:**

- As duas tabelas passam a existir em produção, exatamente como o modelo as declara.
- A divergência entre migrações e modelo deixa de ser possível sem a esteira reclamar.

**Non-Goals:**

- Não revisar as outras 83 tabelas: a comparação já mostrou que estão cobertas, e o teste novo
  passa a guardá-las continuamente.
- Não trocar o `create_all` do `conftest` por `alembic upgrade` na suíte inteira — encareceria
  todos os testes para resolver o que um teste dedicado resolve.
- Não mexer em regra, rota ou modelo da recompensa de marco.

## Decisions

**1. A migração é escrita à mão, conferida contra `--autogenerate`, não o contrário.** O
`alembic revision --autogenerate` produz o esqueleto, mas o que entra no repositório é revisado
linha a linha contra o modelo: autogenerate erra em `server_default`, em nome de índice e em
ordem de dependência entre tabelas com chave estrangeira mútua — e este projeto já tem um ciclo
conhecido (`chave_de_aplicacao` ↔ `solicitacao_de_chave`, avisado pelo SQLAlchemy na suíte). As
duas tabelas nascem na ordem certa: `recompensa_de_marco` antes de `entrega_de_recompensa`, que
a referencia.

**2. A guarda é um teste de paridade, não uma verificação no deploy.** Um teste aplica `alembic
upgrade head` num banco vazio e compara o schema resultante com `Base.metadata` — tabelas e
colunas. Falha lista o que diverge. _Descartado:_ checar no Job de migração — descobriria
tarde, com o deploy em curso, e o Job não tem como saber o que o modelo espera. _Descartado:_
trocar o `create_all` da suíte inteira por migrações — cada teste pagaria a cadeia de 68
revisões para proteger contra um defeito que um teste isolado pega igual.

**3. A comparação cobre tabelas e colunas, não tipos nem constraints.** Paridade de tipo entre
SQLAlchemy e o catálogo do Postgres tem falso positivo demais (`Numeric(12,2)` × `NUMERIC`,
`Uuid` × `uuid`, colação, `server_default` normalizado). Tabela ou coluna faltando é o defeito
que aconteceu e o que mais dói; tipo divergente é raro e aparece no teste da regra. Começar
exigente demais gera teste que se desliga na primeira semana. _Descartado:_ `alembic check` —
compara metadata contra o banco e serve ao fluxo inverso, o de detectar modelo mudado sem
revisão nova; é complementar e pode entrar depois.

## Risks / Trade-offs

- **O teste novo precisa de banco real e a suíte já depende de um** (`CG_DSN_BANCO_TESTE`). →
  Sem custo novo de ambiente; o teste cria e derruba o schema num banco próprio para não
  colidir com o `create_all` das outras fixtures.
- **Aplicar 68 revisões num banco vazio é lento.** → É um teste só, não uma fixture de sessão.
  Se pesar no CI, marca-se para rodar apenas quando `alembic/versions/` ou um `modelo.py`
  mudar.
- **A migração pode conflitar com outra revisão aberta em paralelo.** → O head é conferido no
  momento de escrever e o Alembic acusa cabeça dupla. Não há outra change tocando migrações.

## Migration Plan

1. Merge. O deploy roda `alembic upgrade head` no Job antes de subir o serviço, e as tabelas
   nascem vazias.
2. Conferir a listagem de recompensas de marco na App 09 — a rota que hoje devolve 500.

Reversão: o `downgrade` derruba as duas tabelas, que nascem vazias. Sem risco de dado.
