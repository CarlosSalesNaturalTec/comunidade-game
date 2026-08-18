Sem `RF-XX-nn` nem `RN-XX-nn`: a change é infraestrutura de teste do backend, usada por
toda a suíte e por toda fatia de qualquer PRD, e não altera comportamento de produto. Cada
tarefa cita a decisão do `design.md` que a origina.

## 1. Isolamento por transação

- [x] 1.1 Criar a fixture `conexao` em `backend/tests/conftest.py`: abre uma conexão do
      `engine`, inicia a transação e a desfaz no teardown (design — Decisions 1)
- [x] 1.2 Reescrever a fixture `sessao` para `bind=conexao` com
      `join_transaction_mode="create_savepoint"`, sem `TRUNCATE` e sem `RESTART IDENTITY`
      (design — Decisions 1, 5)
- [x] 1.3 Criar a fixture que substitui `obter_fabrica_de_sessao` de `nucleo.banco` por uma
      fábrica presa à `conexao`, aplicada onde o middleware de auditoria grava
      (design — Decisions 3)
- [x] 1.4 Registrar o marcador `banco_compartilhado` em `backend/pyproject.toml` e dar a ele
      uma `sessao` presa ao `engine`, com o `TRUNCATE` no teardown (design — Decisions 4)
- [x] 1.5 Na fixture `engine`, depois do `create_all`, trocar o `DEFAULT` das colunas com
      `server_default=func.now()` por `clock_timestamp()` via `ALTER TABLE`, só no banco de
      teste (design — Decisions 6)

## 2. Conversão dos testes que abrem segunda conexão

Trocar `engine` por `conexao` — `engine.connect()` vira o uso direto da `conexao`, e
`engine.begin()` vira `conexao.begin_nested()`. Cada arquivo termina verde antes do próximo
(design — Decisions 2).

- [x] 2.1 `test_autoria.py`, `test_convencoes.py` e `test_cli.py` — este último passa a montar
      a `sessionmaker` sobre a `conexao`
- [x] 2.2 Testes de gatilho de imutabilidade: `test_auditoria.py`, `test_consentimento.py`,
      `test_lancamento.py`, `test_ponto_extra.py` e `test_pontuacao.py`
- [x] 2.3 `test_biometria.py`, `test_quiz.py`, `test_desafio_de_coleta.py` e
      `test_autorizacao_vigente.py`
- [x] 2.4 `test_auditoria_middleware.py`, com a fixture da tarefa 1.3
- [x] 2.5 `test_responsavel.py`: a criação simultânea do terceiro vínculo recebe
      `@pytest.mark.banco_compartilhado`, por precisar de duas conexões sobre dado gravado

## 3. Verificação

- [x] 3.1 Suíte inteira verde, com o mesmo número de testes de antes (962) e nenhum
      `xfail`, `skip` ou cenário removido
- [x] 3.2 Registrar no `design.md`, em uma linha, o tempo medido depois da conversão, ao lado
      dos 258 s de antes — a meta declarada na proposta é ficar abaixo de 90 s

## 4. Documentação

- [x] 4.1 Nada a atualizar em `docs/`: a change não toma decisão nova, não muda requisito de
      PRD, não muda a situação de nenhum PRD nem a relação entre documentos, e não cria
      arquivo. Conferir que segue assim ao fechar
