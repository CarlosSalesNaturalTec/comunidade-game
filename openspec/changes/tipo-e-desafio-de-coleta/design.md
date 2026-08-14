## Context

Ver `proposal.md` — Why. O que importa para o desenho é o estado do código:

- `Trilha` e `Missao` existem em `backend/src/nucleo/trilhas/modelo.py`, ambas com o mixin
  `ComAutoria`; `trilhas/regra.py::conferir_posse_da_trilha` já implementa "só o Mestre autor
  escreve na própria trilha, e o Admin passa".
- `ods/regra.py::resolver_etiquetas_da_missao` já implementa, palavra por palavra, a resolução
  que `RF-08-25` pede: a etiqueta própria da missão prevalece, e na falta dela cai para a
  trilha. `criar_etiqueta_ods` é o precedente de como chegar à trilha a partir de uma missão
  para conferir posse.
- `locais/modelo.py` traz `NivelDoLocal` com os seis níveis e `ORDEM_DOS_NIVEIS` com a ordem de
  contenção — a mesma hierarquia que a granularidade exigida do desafio usa.
- `permissoes.py` traz `Operacao.suas_trilhas_e_conteudos` para o Mestre, e o precedente do
  `catalogo_de_poderes`: operação de catálogo que **não** entra na matriz de papel algum, e que
  o Admin alcança por `Operacao.tudo`.
- O banco é PostgreSQL em produção e nos testes; as migrações são Alembic.

## Goals / Non-Goals

**Goals:**

- Fazer a propagação da etiqueta (`RF-01-41`, `RF-08-25`) sem inventar caminho novo: a
  resolução já existe e o desafio deve consumi-la, não copiá-la.
- Deixar a pasta pronta para a série e o registro da fatia seguinte, sem antecipar nada deles.
- Garantir no banco o que o banco garante melhor, e na aplicação o que exige mensagem em
  linguagem simples.

**Non-Goals:**

- Série, registro, invalidação e a credencial do sensor — fatia seguinte.
- Conferir a granularidade contra a comunidade: `RN-08-25` põe isso na abertura da série.
- Lançamento no livro-razão: esta fatia não tem operação com custo. Série temporal com coletor
  identificado também não se aplica — não há medição aqui.

## Decisions

### O módulo novo é `coletas/`

`TipoDeColeta` e `DesafioDeColeta` nascem em `backend/src/nucleo/coletas/`, com `modelo.py`,
`regra.py` e `rotas.py`, como os módulos vizinhos. É a casa que a série e o registro encontram
pronta na fatia seguinte.

Alternativa descartada: pendurar o desafio em `trilhas/`, já que ele se prende a uma missão.
Ficaria certo hoje e errado na fatia seguinte, quando série e registro — que não são da trilha —
tivessem de morar junto ou se separar do desafio.

### A etiqueta do desafio é derivada, nunca coluna

`DesafioDeColeta` **não** ganha `etiqueta_ods_id`. Nasce
`coletas/regra.py::resolver_etiquetas_do_desafio(sessao, desafio)`, que carrega a missão e
delega a `ods/regra.py::resolver_etiquetas_da_missao`.

É o que faz os cenários da spec valerem sem código próprio: "mudar a etiqueta da missão muda a
do desafio" é consequência de não haver cópia, e "trocar a etiqueta não reprocessa pontuação" é
consequência de não haver nada a reprocessar. `RN-08-21` — a etiqueta é descritiva — deixa de
ser regra a vigiar e passa a ser propriedade da forma.

Alternativa descartada: gravar a etiqueta no desafio no momento da criação. Exigiria propagar
toda alteração de etiqueta de missão ou trilha para os desafios já criados, e é justamente o
reprocessamento que `RN-08-21` proíbe.

Consequência aceita: a etiqueta do desafio custa uma consulta a cada leitura. Nesta fatia não
há listagem de desafios por etiqueta, então o custo não aparece; quando a cobertura por
comunidade precisar dele em massa (`RF-08-26`, outra fatia), a agregação entra por consulta
própria, como `cobertura_por_trilha` já faz.

### A granularidade exigida reusa `NivelDoLocal`

A coluna `granularidade_exigida` usa o enum `NivelDoLocal` de `locais/modelo.py`, não um enum
novo. São os mesmos seis níveis, e duplicá-los criaria duas listas para manter.

A criação do desafio **não** consulta `ComunidadeVirtual` — é o que `RN-08-25` decide e o que a
spec exige ao afirmar que nenhuma comunidade é lida. O teto entra na fatia da série.

Alternativa descartada: enum próprio de granularidade em `coletas/`, sob o argumento de que o
desafio não é do território. Perde a fonte única da hierarquia sem ganhar nada.

### Unidade e faixa esperada valem só para o tipo que se mede por número

`unidade`, `faixa_minima` e `faixa_maxima` são colunas anuláveis, com `CheckConstraint` de
tabela garantindo que estão **presentes** quando `forma_de_registro = 'numero'`, **ausentes**
quando é `foto` ou `video`, e que o mínimo não passa do máximo.

Esta é uma **leitura** do PRD, não uma regra dele: o PRD-08 §8 lista os quatro atributos do
`TipoDeColeta` sem dizer que algum é opcional. A leitura vem de `RF-08-12`, que manda marcar
para auditoria o registro **fora da faixa esperada** — comparação que pressupõe valor numérico
e não existe para o tipo cujo registro é a própria mídia (`RF-08-21`). Exigir unidade de um
tipo "buraco na via" seria pedir um campo sem significado.

Alternativa descartada: as quatro colunas obrigatórias sempre, com valores de fachada para foto
e vídeo. Enche o catálogo de dado morto e faz `RF-08-12` comparar contra faixa inventada.

### Posse e permissão reusam o que existe

O desafio de coleta é conteúdo da trilha: a rota exige `Operacao.suas_trilhas_e_conteudos`, que
o PRD-01 §4 já dá ao Mestre, e depois chama `conferir_posse_da_trilha` com a trilha alcançada
por `missao.trilha_id` — exatamente o caminho de `criar_etiqueta_ods`. Nenhuma operação nova
para o desafio.

O catálogo segue o precedente do `catalogo_de_poderes`: nasce `Operacao.catalogo_de_tipos_de_coleta`,
sem entrada na matriz de papel algum, de modo que o Admin a alcança por `Operacao.tudo` e a
negativa por padrão recusa todos os demais — inclusive o Mestre, como `RF-08-05` agora exige.

### O tipo desativado é recusado na aplicação

Que o desafio só escolha tipo ativo é conferido em `coletas/regra.py`, não no banco: a
alternativa declarativa exigiria replicar `ativo` na tabela do desafio para caber numa chave
estrangeira composta, o que criaria dado derivado e faria a desativação reescrever desafios —
o oposto do que a spec pede.

## Risks / Trade-offs

- **A condicionalidade de unidade e faixa é leitura minha do PRD, não texto dele.** → Está
  isolada num `CheckConstraint` e em um requisito só da spec; se o fundador decidir que os
  quatro atributos são sempre obrigatórios, cai uma migração e um cenário, sem tocar no resto.
- **A etiqueta derivada custa uma consulta por leitura.** → Aceito nesta fatia, que não lista
  desafios por etiqueta; a agregação em massa entra por consulta própria quando `RF-08-26`
  chegar.
- **`RN-08-14` fica declarada e não conferida.** → É decisão registrada no `proposal`, com o
  precedente da sondagem; a spec afirma explicitamente que a trilha sem desafio não é recusada
  aqui, de modo que a ausência é testada e não esquecida.

## Migration Plan

Uma revisão do Alembic, com duas tabelas novas — `tipo_de_coleta` e `desafio_de_coleta` — e
nenhuma migração de dado: as duas nascem vazias. O `downgrade` derruba as duas na ordem
inversa. Nada de outra fatia depende delas ainda, então o rollback é a própria queda.
