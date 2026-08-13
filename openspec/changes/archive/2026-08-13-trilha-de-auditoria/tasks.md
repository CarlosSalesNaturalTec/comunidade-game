## 1. Entidade e migração

- [x] 1.1 Modelar `Auditoria` em `backend/src/nucleo/auditoria/modelo.py` com autor, papel do
      autor, ação, entidade afetada, data e hora com fuso e origem (`RF-01-29`, PRD-01 §8).
      Verificável: o modelo espelha as colunas do §8, sem coluna a mais
- [x] 1.2 Aplicar o par _listener_ de mapeador + trigger Postgres que recusa `UPDATE` e
      `DELETE`, no mesmo padrão de `Consentimento` e `acesso_ao_template` (PRD-01 §8,
      "Imutabilidade"). Verificável: teste que tenta alterar e apagar um registro e recebe
      recusa nas duas tentativas
- [x] 1.3 Escrever a migração Alembic da tabela `auditoria`, indexada por autor e por momento.
      Verificável: a migração sobe e desce, e o banco volta a vazio
- [x] 1.4 Adicionar `AuditoriaImutavel` ao catálogo de `erros.py`, no mesmo formato de
      `ConsentimentoImutavel` e `AcessoAoTemplateImutavel`. Verificável: a tentativa de
      alteração devolve o corpo único de erro

## 2. Contexto compartilhado

- [x] 2.1 Gravar o `ContextoDaSessao` resolvido em `request.state` dentro de `exigir_persona`
      (`backend/src/nucleo/autenticacao.py`), além de continuar devolvendo-o como hoje.
      Verificável: nenhuma rota que usa `exigir_persona` muda de comportamento
- [x] 2.2 Gravar o `ContextoDaChave` resolvido em `request.state` dentro de
      `exigir_chave_de_aplicacao` (`backend/src/nucleo/chaves/conferencia.py`), pelo mesmo
      padrão. Verificável: nenhuma rota que usa a dependência muda de comportamento

## 3. Middleware de gravação

- [x] 3.1 Implementar o middleware ASGI em `backend/src/nucleo/auditoria/middleware.py`, que
      roda para toda chamada sob `/v1` com método `POST`/`PUT`/`PATCH`/`DELETE` (`RF-01-29`,
      PRD-01 §12). Verificável: chamada de leitura nunca aciona o middleware
- [x] 3.2 Gravar o registro só quando a resposta final tiver `status_code < 400`, lendo persona,
      papel e origem de `request.state` (`RF-01-29`). Verificável: chamada de escrita recusada
      não gera registro
- [x] 3.3 Derivar `ação` do método HTTP mais o nome da rota (`request.scope["route"].name`) e
      `entidade afetada` do mesmo nome, conforme `design.md`. Verificável: duas rotas
      diferentes produzem rótulos de ação diferentes e estáveis
- [x] 3.4 Abrir uma sessão de banco própria do middleware, independente da sessão já fechada da
      rota, e fechá-la ao final (`design.md`). Verificável: teste que confirma a gravação
      mesmo quando a sessão da rota já terminou
- [x] 3.5 Tornar a gravação _best-effort_: falha ao gravar o registro é registrada em log e não
      altera a resposta já pronta (`design.md`, Risks). Verificável: teste que simula falha na
      gravação e confirma que a resposta original chega inalterada ao cliente
- [x] 3.6 Registrar o middleware em `principal.py`, para toda a aplicação. Verificável: uma
      escrita aceita em qualquer roteador já existente gera um registro de auditoria

## 4. Rota de consulta

- [x] 4.1 Implementar `GET /v1/auditoria` em `backend/src/nucleo/auditoria/rotas.py`, exigindo o
      papel Admin pela dependência única de permissão (`RF-01-29`, PRD-01 §9). Verificável:
      persona autenticada sem papel Admin recebe recusa por permissão
- [x] 4.2 Paginar e filtrar a consulta pelo `contrato_de_listagem`, com os filtros universais de
      período e persona mais os filtros de domínio ação e entidade afetada (`RF-01-28`).
      Verificável: parâmetro não declarado é recusado com 422, nomeando o parâmetro
- [x] 4.3 Incluir o roteador de auditoria em `principal.py` via `incluir_roteador_de_dados`.
      Verificável: a rota exige chave de aplicação como as demais

## 5. Verificação contra os critérios de aceite

- [x] 5.1 Testar que toda escrita bem-sucedida em uma rota já existente (por exemplo,
      `POST /v1/responsaveis`) gera um registro de auditoria com autor, papel, ação, entidade
      afetada, data e hora e origem (`RF-01-29`, critério do PRD-01 §12)
- [x] 5.2 Testar que uma chamada de leitura e uma chamada de escrita recusada não geram
      registro algum (`RF-01-29`)
- [x] 5.3 Testar que Admin consulta a trilha paginada e filtrada, e que persona de outro papel
      recebe recusa por permissão (`RF-01-29`, PRD-01 §9)
- [x] 5.4 Testar que a trilha não traz nenhuma escrita anterior à existência do middleware —
      confirmando por ausência, não reconstruindo nada (`design.md`, Non-Goals)
- [x] 5.5 Testar que uma tentativa de alterar ou apagar um registro de auditoria já gravado é
      recusada, preservando o original (PRD-01 §8, "Imutabilidade")

## 6. Documentação

- [x] 6.1 Conferir que a interpretação de `RF-01-29` registrada em `proposal.md` — a trilha
      audita toda escrita, de qualquer persona, e "das ações de Admin"/"de gestão" descreve
      quem lê — não exige mudança de texto no PRD-01: as duas frases já estão lá, e esta fatia
      só declara qual prevalece. Verificável: nenhum documento-fonte muda por causa desta
      decisão
- [x] 6.2 Conferir que `docs/prds/index.md` e o documento 99 seguem corretos: o PRD-01 continua
      "aprovado", fatiado em changes, e nenhuma relação entre documentos mudou. Verificável: os
      dois seguem sem alteração, e isso é a conclusão
- [x] 6.3 Conferir que nenhum arquivo novo entrou em `docs/`. Verificável: a `nav` do
      `mkdocs.yml` não precisa de entrada nova
- [x] 6.4 Rodar `npm run fix`, `npm run lint` e `mkdocs build --strict` antes de abrir o PR.
      Verificável: os três passam
