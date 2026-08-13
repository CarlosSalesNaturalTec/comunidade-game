## Context

Ver `proposal.md` — Why. O núcleo já tem quatro peças que esta fatia reaproveita: o mixin
`ComAutoria` (autor, papel, momento em toda entidade de negócio), o padrão de tabela somente
inserção com _listener_ de mapeador + trigger Postgres (`Consentimento`, `acesso_ao_template`),
o contrato único de listagem (`contrato_de_listagem` em `paginacao.py`) e as duas dependências
que resolvem contexto por chamada — `exigir_persona` (`ContextoDaSessao`) e
`exigir_chave_de_aplicacao` (`ContextoDaChave`). Erro é sempre exceção, convertida em corpo
único pelos manipuladores registrados em `principal.py`; uma chamada sem exceção é, por
definição, sucesso.

`obter_sessao` é uma dependência de escopo de requisição: a sessão de banco fecha no
_teardown_ da chamada, antes de `call_next` devolver o controle a um middleware ASGI. Um
middleware não herda a sessão da rota.

## Goals / Non-Goals

**Goals:**

- Gravar auditoria de toda escrita aceita sob `/v1`, sem que nenhuma rota — presente ou
  futura — declare nada.
- Expor a trilha, paginada e filtrável, só para Admin.
- Preservar a imutabilidade que o projeto já usa para registro de guarda permanente.

**Non-Goals:**

- Reconstruir `origem` ou qualquer campo retroativo das dez fatias já entregues.
- Garantir que a auditoria nunca falhe silenciosamente sob falha de infraestrutura — é
  best-effort quanto à própria gravação (Risks).
- Correlacionar várias linhas da trilha numa mesma "sessão de uso" — cada linha é
  independente.

## Decisions

### Middleware ASGI, não dependência por rota

Um middleware roda para toda chamada, sem que a rota declare `Depends`. É a mesma lógica que
levou a matriz de permissões a virar uma dependência única em vez de checagem espalhada: o que
não depende de disciplina não se esquece. Alternativa descartada: dependência de auditoria
que cada roteador novo declara — funciona para rotas futuras, mas não é transversal, e uma
fatia nova poderia esquecê-la.

### O middleware lê o contexto de `request.state`, gravado pelas próprias dependências

`exigir_persona` e `exigir_chave_de_aplicacao` passam a gravar o `ContextoDaSessao` e o
`ContextoDaChave` que já resolvem em `request.state`, além de devolvê-los como hoje. É uma
adição de uma linha em cada uma — nenhuma rota muda, porque as duas já são dependências
compartilhadas por todo o núcleo, não código por rota. O middleware lê os dois de
`request.state` depois de `call_next`, sem recalcular nada.

Alternativa descartada: o middleware resolve sessão e chave por conta própria, a partir dos
cabeçalhos. Duplicaria a consulta ao banco e a comparação em tempo constante que
`exigir_chave_de_aplicacao` já faz — sem ganhar nada, porque a chamada já passou por ali.

### "Ação" e "entidade afetada" vêm do nome da rota FastAPI, não do caminho bruto

Cada rota declarada com `@roteador.post(...)` etc. tem um nome estável no roteamento do
Starlette (`request.scope["route"].name`, por padrão o nome da função Python). O middleware
grava `ação = método HTTP + nome da rota` e deriva `entidade afetada` do mesmo nome — sem
tocar em nenhuma rota para declará-lo explicitamente, porque o nome já existe. O caminho bruto
fica de fora do campo `ação`: ele carrega valor de parâmetro (`/v1/responsaveis/{id}/vinculos`
vira `/v1/responsaveis/3f2.../vinculos`), que é dado de negócio, não rótulo de operação — o
`id` afetado entra à parte, como referência da entidade, não como texto livre dentro de
`ação`.

Alternativa descartada: mapa explícito caminho → nome de entidade, mantido por fatia. Mais um
lugar para lembrar de atualizar a cada rota nova, quando o nome da função já é único e
legível.

### Sucesso é resposta com status abaixo de 400

Todo erro do núcleo é exceção convertida em `CorpoDeErro` pelos manipuladores de
`principal.py`; nenhuma rota devolve corpo de erro com status de sucesso. O middleware grava
o registro quando a resposta final tem `status_code < 400` e o método é
`POST`/`PUT`/`PATCH`/`DELETE` — mesma regra para toda rota, sem exceção por domínio.

### O middleware abre sua própria sessão de banco

Como a sessão de `obter_sessao` já fechou quando o middleware recebe a resposta, a gravação
do registro de auditoria abre uma sessão própria, pela mesma fábrica de `banco.py`, e a fecha
ao final — nunca reaproveita nem estende a sessão da rota, que já fez seu commit e terminou.

## Risks / Trade-offs

- **Falha ao gravar o registro de auditoria não pode derrubar uma escrita já aceita** → a
  gravação do registro é _best-effort_: falha nela é registrada em log e não altera a
  resposta já pronta, que o cliente já recebe como sucesso. A escrita de negócio não espera
  pela auditoria nem é desfeita por ela.
- **Duas sessões de banco por chamada de escrita (a da rota, a do middleware)** → é o custo
  aceito de o middleware não herdar uma sessão já fechada; volume de escrita do Ciclo 01 não
  justifica _pooling_ dedicado além do que `banco.py` já oferece.
- **Nome de rota como identificador de "ação" muda se a função Python for renomeada** → é
  reconhecido: renomear a função de uma rota já entregue muda o rótulo de `ação` dali em
  diante nos registros novos; registros antigos preservam o nome de quando foram gravados,
  porque a trilha é somente inserção.

## Migration Plan

Uma migração Alembic cria a tabela `auditoria` com o mesmo par _listener_ de mapeador +
trigger Postgres que `Consentimento` e `acesso_ao_template` já usam para recusar `UPDATE` e
`DELETE`. Não há dado a migrar: a trilha nasce vazia e passa a crescer a partir do _deploy_
desta fatia — não há passo de _rollback_ além do padrão (`alembic downgrade`), porque nenhuma
tabela existente muda.
