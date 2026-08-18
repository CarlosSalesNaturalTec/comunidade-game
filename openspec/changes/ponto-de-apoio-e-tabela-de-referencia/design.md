## Context

Ver `proposal.md` — Why. O que o desenho precisa saber do estado atual:

- A `Aula` existe desde a fatia `aula-presenca-e-equipe` e **não tem rota HTTP**: nasce por
  `aulas.regra.agendar_aula`, chamada hoje só pelos testes. A rota de agendamento é do PRD-02.
  Acrescentar campo obrigatório à aula, portanto, mexe em **modelo, regra e migration**, e em
  nenhum contrato HTTP publicado.
- O banco é **PostgreSQL** em produção e nos testes (`tests/conftest.py`), o que torna
  `NUMERIC(p, s)` exato — não há o problema de ponto flutuante que o SQLite traria.
- `ComAutoria` e `ComMomentoDoFato` (`src/nucleo/autoria.py`, `tempo.py`) são os _mixins_ que
  todas as entidades de escrita já usam para autor, papel do autor e momento com fuso.
- A matriz de papéis vive em `permissoes.py`, e o padrão de rota de Admin já está em
  `locais/rotas.py` e `coletas/rotas.py` — é dele que estas rotas herdam a forma.

## Goals / Non-Goals

**Goals:**

- Duas entidades de cadastro que o resto do PRD-07 possa pendurar sem retrabalho: a dimensão do
  saldo (ponto de apoio) e a régua de valor (tipo de recurso e sua tabela).
- Uma tabela de referência cuja consulta **por data** seja barata e correta, porque todo aporte
  passará por ela.
- Fechar o `RF-01-71` sem tocar em contrato HTTP algum.

**Non-Goals:**

- Nada de livro-razão: sem `Lancamento`, sem saldo, sem reserva. O desenho **não antecipa** o
  formato deles — só evita fechar portas.
- Sem rota de leitura, pelo motivo da `proposal` — Fora do escopo.

## Decisions

### 1. Moeda em `Numeric(12, 2)`, nunca float

`RN-07-04` fixa duas casas decimais. Em Postgres, `NUMERIC(12, 2)` é decimal exato e o driver
devolve `Decimal`, de modo que soma e comparação não derivam. O teto de 12 dígitos comporta
`9_999_999_999.99` moedas — dez ordens de grandeza acima do Ciclo 01, e barato de alargar depois.

**Alternativas consideradas.** _Inteiro de centésimos_ (como `ponto_extra` faz com pontos)
funcionaria, mas obrigaria toda leitura a dividir por 100 e abriria espaço para o erro clássico
de esquecer a divisão em um lugar só; `Numeric` carrega a escala no próprio tipo. _`Float`_ está
fora: `RN-07-04` pede exatidão, e dinheiro em binário não a tem.

A recusa de valor com mais de duas casas é **explícita na regra**, antes do banco: `NUMERIC(12,2)`
arredondaria em silêncio, e a spec exige 422.

### 2. Vigência como intervalo semiaberto, encerrada por escrita

`ValorDeReferencia` guarda `vigencia_inicio` e `vigencia_fim` (`date`, `fim` anulável), com o
intervalo **semiaberto**: `inicio <= data < fim`. Abrir vigência nova grava `vigencia_fim` da
anterior **igual ao início da nova** — nunca "a véspera".

A diferença importa numa borda real: com "véspera", dois valores registrados no mesmo dia
produziriam `fim < inicio` na anterior, um intervalo inválido. Com o semiaberto, o caso degenera
para um intervalo vazio, que a consulta simplesmente nunca seleciona. O desempate entre vigências
do mesmo dia é a **ordem de registro**, e é por isso que a consulta ordena por
`vigencia_inicio DESC, criado_em DESC` e toma a primeira.

**Alternativa considerada.** Guardar **só** `vigencia_inicio` e derivar o fim ("a maior vigência
que começou até a data") elimina de vez a possibilidade de sobreposição e seria mais enxuto. Foi
descartada porque o PRD-07 §8 declara `vigência inicial e final` como atributos da entidade, e
artefato do OpenSpec não retira atributo que o PRD declara. O `fim` é, na prática, derivado — mas
fica **materializado**, como o PRD pede.

### 3. `ponto_de_apoio_id` entra `NOT NULL` direto

A coluna nasce obrigatória, sem passo intermediário anulável. Não há retrocompatibilidade a
preservar — a plataforma não está implantada, nenhuma aula real existe, e **não há valor de
backfill defensável**: inventar um ponto de apoio para preencher linhas antigas seria criar dado
que ninguém cadastrou.

A migration falha alto se a tabela `aula` tiver linhas, e isso é o comportamento desejado: num
ambiente com aulas gravadas, quem opera precisa cadastrar o ponto de apoio e decidir a qual delas
cada aula pertence — decisão de gestão, não de migration.

**Alternativa considerada.** Anulável agora e obrigatória depois adiaria o `RF-01-71` para uma
segunda change sem entregar nada em troca, já que o requisito é justamente a obrigatoriedade.

### 4. A conferência de comunidade fica na regra, não no banco

Que o ponto de apoio seja da mesma comunidade da aula (`proposal` — decisão 4) é conferido em
`aulas.regra.agendar_aula`, com 422. Uma restrição declarativa equivalente exigiria chave
composta `(id, comunidade_virtual_id)` em `ponto_de_apoio` e uma _foreign key_ composta a partir
de `aula` — solução correta, porém desproporcional: acopla o esquema de duas tabelas para uma
regra que só tem um ponto de entrada, e esse ponto já é o único caminho de criação de aula.

### 5. Duas pastas, não uma

`pontos_de_apoio/` e `recursos/`, cada uma com `modelo.py`, `regra.py` e `rotas.py`, no padrão
das demais. Não viram uma pasta `economia/` comum porque o ponto de apoio é **cadastro da
gestão** consumido também pela aula e, adiante, pelo patrimônio, enquanto o catálogo de tipos é
peça do livro-razão. Juntá-las agora criaria uma dependência da aula sobre o módulo do ledger.

### 6. O responsável é coluna anulável, não tabela de histórico

`ponto_de_apoio.responsavel_id` anulável, trocável por escrita direta. O histórico de quem foi
designado quando **já existe**: a trilha de auditoria (`RF-01-29`) grava toda escrita de gestão,
e a spec só exige que a designação anterior permaneça auditável — não que seja consultável como
série. Uma tabela `DesignacaoDeResponsavel` seria a escolha se houvesse requisito de ler o
histórico, e não há.

O papel do designado é conferido na regra contra `Papel.admin`, `Papel.mestre` e
`Papel.apoiador`.

## Risks / Trade-offs

- **A migration falha em base com aulas gravadas** → é intencional (decisão 3), mas precisa estar
  escrito no docstring da revisão, para quem a rodar entender que o remédio é cadastrar o ponto de
  apoio antes, não afrouxar a coluna.
- **`Numeric` volta como `Decimal` e contamina comparações com `float` nos testes** → os testes
  comparam com `Decimal("10.00")`, nunca com literal float.
- **A tabela de referência nasce sem consumidor** e só será exercitada de verdade na fatia do
  aporte → mitigado por teste que consulta o valor **por data** em três pontos: dentro da vigência
  encerrada, no dia da virada e depois da última abertura.
- **Um `ativo` sem operação que o mude** pode ser lido como esquecimento → o campo carrega
  comentário apontando a pendência do documento 09, e nenhuma regra o consulta.
- **Duas pastas novas** aumentam a superfície do núcleo → aceito: é o mesmo padrão das outras
  quinze, e a esteira de CI do `backend/` já existe e cobre ambas sem alteração.

## Migration Plan

Uma revisão do Alembic, encadeada na última (`a7b8c9d0e1f2`):

1. `ponto_de_apoio` — `id`, `nome`, `comunidade_virtual_id` (FK, `NOT NULL`), `responsavel_id`
   (FK, anulável), `ativo` (`NOT NULL`, _default_ verdadeiro) e as colunas de `ComAutoria`.
2. `tipo_de_recurso` — `id`, `nome`, `natureza`, `unidade` e as colunas de `ComAutoria`.
3. `valor_de_referencia` — `id`, `tipo_de_recurso_id` (FK, `NOT NULL`), `valor_em_moedas`
   (`NUMERIC(12, 2)`, `NOT NULL`), `vigencia_inicio` (`NOT NULL`), `vigencia_fim` (anulável) e as
   colunas de `ComAutoria`, com `CHECK` de valor não negativo e de `vigencia_fim >= vigencia_inicio`.
4. `aula.ponto_de_apoio_id` — FK `NOT NULL`.

`downgrade` derruba na ordem inversa. Sem passo de dados: não há o que migrar.

## Open Questions

Nenhuma que altere spec, desenho ou tarefas. A desativação de ponto de apoio é pendência **de
produto**, aberta no documento 09, e o desenho a acomoda sem se comprometer: o `ativo` existe e
nenhuma regra o lê.
