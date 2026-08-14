## Context

Ver `proposal.md` — Why. O que importa para o desenho é o estado do código:

- `ComunidadeVirtual` mora hoje em `backend/src/nucleo/personas/modelo.py`, como entidade sem
  rota, criada pela segunda fatia só para o vínculo e o filtro terem a que apontar.
- O vínculo é a coluna `Persona.comunidade_virtual_id`, com o `CheckConstraint`
  `ck_persona_guerreiro_tem_comunidade` garantindo `RN-01-05` na própria tabela.
- Essa coluna é lida em **seis pontos** fora de `personas/`: `vitrine/publico.py`,
  `vitrine/rotas.py`, `aulas/regra.py` e três lugares de `ods/regra.py`. Todos filtram por
  comunidade.
- O banco é PostgreSQL em produção **e nos testes** (`backend/tests/conftest.py`), então
  recurso próprio do Postgres está disponível sem penalizar a esteira.
- As migrações são Alembic, em `backend/alembic/versions/`.

## Goals / Non-Goals

**Goals:**

- Trocar a coluna pelo `VinculoJogador` sem que exista, em nenhum momento da migração, uma
  janela em que `RN-01-05` não valha.
- Manter o custo dos seis pontos de leitura em uma mudança de forma só, não em seis
  invenções diferentes de junção.
- Garantir a hierarquia de locais o mais perto possível do banco, porque ela é a estrutura
  sobre a qual a série de coleta vai se apoiar.

**Non-Goals:**

- Rota de transferência entre comunidades — `RF-08-03`, fora do Ciclo 01.
- Qualquer superfície pública de comunidade: `GET /comunidades` e `/series` são `RF-08-16` e
  seguintes, e dependem de série.
- Lançamento no livro-razão: esta fatia não tem operação com custo. Série temporal com
  coletor identificado também não se aplica — não há medição aqui.

## Decisions

### O `VinculoJogador` substitui a coluna, e não convive com ela

A coluna sai. A alternativa — manter `Persona.comunidade_virtual_id` como cache do vínculo
vigente e o `VinculoJogador` só como histórico — é tentadora, porque no Ciclo 01 não há
transferência e as duas fontes nunca divergiriam na prática. Foi descartada: a spec diz que o
vínculo NEVER SHALL ser atributo da persona, e duas fontes de verdade para a mesma pergunta é
exatamente o que o invariante 4 não deve depender.

"Exatamente um vigente" passa a ser **índice parcial único** no Postgres:

```text
UNIQUE INDEX uq_vinculo_jogador_vigente ON vinculo_jogador (guerreiro_id)
WHERE data_fim IS NULL
```

O banco garante a unicidade; a regra de aplicação continua devolvendo o erro em linguagem
simples, porque o `IntegrityError` cru não serve de resposta. Alternativa descartada:
garantir só na aplicação, que perde a garantia sob concorrência.

A obrigatoriedade — Guerreiro(a) **sem** vínculo não existe — não tem equivalente declarativo,
porque é uma asserção entre duas tabelas. Fica na criação da persona, que já é o único
caminho por onde Guerreiro(a) nasce (`personas/regra.py`), e ganha teste próprio.

### Os seis pontos de leitura passam por um helper só

Nasce `comunidades/regra.py::filtrar_personas_por_comunidade(consulta, comunidade_id)`, que
aplica a junção com o vínculo vigente. Os seis pontos passam a chamá-lo em vez de comparar a
coluna. A `Persona` ganha também uma `relationship` para o vínculo vigente
(`primaryjoin` com `data_fim IS NULL`), para o acesso a partir de uma persona já carregada —
é o que `aulas/regra.py:80` faz ao conferir se o Guerreiro(a) é da comunidade da aula.

Alternativa descartada: `column_property` com subconsulta escalar, que preservaria a escrita
`Persona.comunidade_virtual_id == x` sem tocar nos seis pontos. Esconde uma subconsulta por
linha em toda listagem paginada, e o ganho é só de diff.

### O pai do local se prende por chave composta

"Local pai da mesma comunidade" é declarável, e por isso é declarado. `local` ganha
`UNIQUE (id, comunidade_id)` e a chave estrangeira do pai é composta:

```text
FOREIGN KEY (local_pai_id, comunidade_id) REFERENCES local (id, comunidade_id)
```

Com isso o banco recusa pai de outra comunidade sem que nenhuma regra precise conferir.
Alternativa descartada: conferir na aplicação, que deixa o convite aberto para escrita por
outro caminho.

O **nível do pai** — imediatamente acima — não cabe em chave estrangeira e fica na regra de
aplicação, sobre um enum ordenado (`comunidade`, `bairro`, `rua`, `condominio`, `bloco`,
`quadra`). O caso "só o nível `comunidade` não tem pai" é `CheckConstraint` de tabela, porque
envolve só as duas colunas da mesma linha.

### A granularidade máxima é guardada, não aplicada nesta fatia

`RF-08-01` manda a comunidade declarar granularidade máxima, e nenhum requisito manda o
cadastro de local conferi-la. Quem exige granularidade é o desafio de coleta (`RF-08-06`),
que não entra aqui. O atributo é gravado e não filtra nada nesta entrega.

Aplicar um teto que o PRD não escreveu seria criar regra dentro de um artefato do OpenSpec.
Ver Riscos, e a pergunta ao fundador no relatório desta change.

### `ComunidadeVirtual` muda de módulo

Sai de `personas/modelo.py` para `comunidades/modelo.py`, junto do `VinculoJogador`. Os
módulos novos seguem a forma dos existentes: `modelo.py`, `regra.py` e `rotas.py` onde há
superfície — `comunidades/` tem rota de criação por Admin, `locais/` tem cadastro e consulta.

## Risks / Trade-offs

- **A migração mexe em tabela com dado já gravado** → A migração faz, numa transação:
  criar `vinculo_jogador`; copiar cada `Persona.comunidade_virtual_id` não nulo como vínculo
  vigente, com `data_inicio` igual a `Persona.criada_em`; criar o índice parcial; só então
  derrubar a coluna e o `CheckConstraint`. O `downgrade` reconstrói a coluna a partir do
  vínculo vigente. Como a cópia precede a queda, não há janela sem a invariante.
- **Seis pontos de leitura mudam de forma ao mesmo tempo** → Todos passam pelo mesmo helper,
  e os testes de vitrine, ODS e aula já existentes são a rede: eles cobrem o filtro por
  comunidade e devem passar sem alteração de expectativa, só de montagem.
- **A junção encarece o filtro por comunidade**, que antes era coluna na própria linha → É
  junção por chave primária indexada, e as listagens já são paginadas. Se aparecer custo, o
  lugar de resolver é índice, não desnormalizar de volta.
- **A granularidade máxima guardada e não aplicada pode deixar local cadastrado abaixo do
  teto**, se a intenção do PRD for que ela limite a profundidade → Enquanto não houver
  decisão, o dado fica declarado e conferível; se a regra vier, ela alcança o cadastro sem
  precisar reescrever a hierarquia. Levado ao fundador como pergunta.

## Migration Plan

1. Migração do Alembic: cria `comunidade_virtual` no lugar novo — a tabela não muda de nome,
   só de módulo, então não há DDL de renomeação —, cria `local` com a chave composta e cria
   `vinculo_jogador`.
2. Copia os vínculos existentes de `Persona.comunidade_virtual_id`.
3. Cria o índice parcial único.
4. Derruba `Persona.comunidade_virtual_id` e o `CheckConstraint`
   `ck_persona_guerreiro_tem_comunidade`.
5. `downgrade` percorre o caminho inverso, reconstruindo a coluna a partir do vínculo
   vigente.
