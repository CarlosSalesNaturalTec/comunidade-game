## Why

A suíte do backend leva **4 min 18 s** para 962 testes, e a maior parte disso é espera de
banco: o tempo de CPU do processo é de 1 min 05 s. A causa está no isolamento entre testes —
a fixture `sessao` termina cada teste com `TRUNCATE` das 48 tabelas do `Base.metadata`.

Medido nesta máquina, contra o mesmo PostgreSQL 16 que a esteira usa:

| Medida                                          | Valor                       |
| ----------------------------------------------- | --------------------------- |
| Suíte completa hoje                             | 258 s (962 testes)          |
| `TRUNCATE` das 48 tabelas, por teste            | 174 ms                      |
| Projeção do `TRUNCATE` sobre a suíte            | **167 s — 65% do total**    |
| Protótipo com isolamento por transação          | 72 s (3,6× mais rápido)     |

O custo não para de crescer: ele é o número de tabelas vezes o número de testes, e as duas
coisas aumentam a cada fatia. O ritmo de verificação que o `CLAUDE.md` acaba de fixar — suíte
inteira uma vez ao fechar as tarefas — só se sustenta se essa execução for barata.

**Esta change não tem `RF-XX-nn` nem `RN-XX-nn`, e não é de um PRD.** Ela é infraestrutura
de teste do backend: não altera comportamento de produto, não tem delta de spec e declara
`skip_specs: true`. A fixture `sessao` é usada por toda a suíte — hoje pelo que já entrou do
PRD-01 e do PRD-07, daqui em diante por toda fatia, de qualquer PRD. O que ela muda é o custo
de rodar a verificação, e esse custo é pago em toda change do ciclo.

A esteira do backend que ela respeita — Ruff, pytest e cobertura medida sem limiar no Ciclo
01 — está no `CLAUDE.md`, sobre a stack Python 3.12 do documento 03 §1.13 e registrada no
PRD-01 §13. Change sem identificador é exceção à regra de rastreabilidade, e por isso precisa
do aval explícito do fundador antes do `/opsx:apply`.

## What Changes

- A fixture `sessao` deixa de limpar o banco por `TRUNCATE` e passa a rodar cada teste dentro
  de uma transação desfeita no fim, sobre uma única conexão por teste.
- Nasce a fixture `conexao`, que expõe essa conexão. Os 21 usos de `engine.connect()` e
  `engine.begin()` espalhados por 12 arquivos de teste passam a usá-la, para que o SQL cru
  enxergue o que o teste gravou e seja desfeito junto.
- O middleware de auditoria, que abre a própria sessão pela fábrica de `nucleo.banco`, passa
  a entrar na transação do teste por uma fixture que substitui essa fábrica.
- Os poucos testes que precisam mesmo de dado gravado — concorrência real entre duas conexões
  — passam a declarar isso por marcador, e só eles pagam a limpeza por `TRUNCATE`.
- Nenhuma mudança em `backend/src/`, nas migrações ou nos workflows.

## Capabilities

### New Capabilities

Nenhuma.

### Modified Capabilities

Nenhuma. A change não altera comportamento observável: `.openspec.yaml` declara
`skip_specs: true`.

## Impact

- `backend/tests/conftest.py` — fixtures `engine`, `conexao`, `sessao` e a nova fixture da
  fábrica de sessão do middleware.
- Doze arquivos de `backend/tests/` que hoje usam a fixture `engine`: `test_auditoria.py`,
  `test_auditoria_middleware.py`, `test_autoria.py`, `test_autorizacao_vigente.py`,
  `test_biometria.py`, `test_cli.py`, `test_consentimento.py`, `test_convencoes.py`,
  `test_desafio_de_coleta.py`, `test_lancamento.py`, `test_ponto_extra.py`,
  `test_pontuacao.py`, `test_quiz.py` e `test_responsavel.py`.
- `backend/pyproject.toml` — registro do marcador do banco compartilhado.
- Sem impacto em rota, contrato de API, modelo de dados, migração ou documentação de `docs/`.
