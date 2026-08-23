## Context

Ver `proposal.md` — Why. Três das quatro peças do núcleo são **regra pronta sem porta**:
`resultados.regra.registrar_resultado`, `aulas.regra.registrar_presenca` e a leitura das aulas
já existente em `aulas/rotas.py`. As specs `resultado-de-atividade` e `aula-e-presenca` já
descrevem o comportamento delas; esta fatia não o reescreve.

O que a fatia decide de novo é a **ocorrência de conduta** — entidade que não existe — e o
recorte de permissão de duas rotas cujo alcance os PRDs descrevem de formas diferentes.

## Goals / Non-Goals

**Goals:**

- Abrir as três portas sem reescrever nenhuma recusa que já existe no núcleo.
- Dar à ocorrência de conduta casa própria, com o motivo separável do lançamento.

**Non-Goals:**

- Unificar os dois lançamentos (por aula e por atividade) numa rota só.
- Qualquer caminho de edição, ajuste ou expurgo — ver Decisão 5.

## Decisions

### 1. Dois lançamentos, duas rotas, um `registrar_resultado`

`POST /v1/atividades/{id}/lancamentos` (Mestre autor) e `POST /v1/aulas/{id}/lancamentos`
(Admin) chamam o **mesmo** `registrar_resultado` por participante. O que difere é o que vem
depois: só o ato por aula chama `consumir_reservas_da_aula` e leva a aula a realizada.

A rota nova NÃO reaproveita `lancar_atividade_realizada`, que é `Papel.admin` por dentro e
carrega a baixa das reservas. Ela itera `registrar_resultado` dentro de uma transação e para
inteira no primeiro erro.

_Alternativa descartada:_ um parâmetro em `lancar_atividade_realizada` distinguindo os dois
atos — mistura duas autorizações e dois efeitos numa função só.

### 2. A presença do Mestre é confirmação, não escrita de gestão

`registrar_presenca` não confere papel algum — foi escrita para o App 01. A rota nova exige
`Operacao.confirmacao_de_identidade_do_guerreiro` e **recusa o modo reconhecimento** vindo do
Mestre, antes de chamar a regra. A guarda fica na rota porque é dela o recorte; a regra
continua servindo o App 01 sem alteração.

_Alternativa descartada:_ acrescentar `Operacao` nova de presença à matriz — mudaria o PRD-01
§4, e o `RF-01-17` fecha a lista de escritas do Mestre.

### 3. `OcorrenciaDeConduta` é entidade, e o valor não trafega

Módulo novo `nucleo/ocorrencias_de_conduta/`, no padrão de `livro_razao`: somente inserção,
sem caminho de alteração no ORM.

Colunas: `guerreiro_id`, `aula_id`, `atividade_id`, `valor` (gravado, não recebido),
`motivo` (`Text`, **anulável**), `momento_do_fato`, mais `ComAutoria`.

O `valor` é gravado a partir da constante do documento 11 §5 e **entra na coluna** em vez de
ser derivado na leitura: o `RN-01-52` exige que o lançamento sobreviva com valor, data e autor
depois de o motivo sumir, e uma tabela de valores que mude de vigência não pode reescrever o
passado. É o mesmo motivo por que a `Troca` grava o preço cobrado.

`motivo` nasce anulável para que o expurgo seja um `UPDATE` para `NULL`, sem tocar o
lançamento.

_Alternativa descartada:_ um campo de motivo em `PontoRegular` — ele é `total` corrente, sem
histórico, e não comporta duas ocorrências nem autoria.

### 4. A trilha do débito vem da atividade; o teto vem da aula

`debitar_ponto_regular` exige exatamente uma referência — trilha **ou** poder — e a aula não
tem trilha. A ocorrência declara a **atividade**, e a trilha sai de atividade → missão →
trilha, pela mesma travessia que `registrar_resultado` já faz.

O **teto de 10 por Guerreiro(a) e por aula presencial** é conferido por contagem das
ocorrências já gravadas daquele par (aula, Guerreiro(a)) antes de qualquer escrita — duas
ocorrências de 5 esgotam o teto, e a terceira é 422. A conferência não olha o saldo: teto é do
encontro, não do Guerreiro(a).

`conferir_posse_da_trilha` sobre a trilha derivada é a recusa de atividade alheia, reusada sem
reescrever.

### 5. O expurgo do motivo não entra

Nem rota, nem tarefa agendada, nem gatilho. O ciclo é rótulo de configuração
(`configuracao.ciclo_rotulo`), não entidade, e nada no núcleo sabe que um ciclo terminou —
pendência que a fatia devolve ao documento 09, junto com a saída do ranking ao fim do ciclo,
que depende do mesmo gatilho.

O que a fatia entrega é a **preparação**: `motivo` anulável e as saídas montadas para omitir o
campo quando ele é nulo, de modo que o expurgo, quando vier, seja só o `UPDATE`.

### 6. `GET /v1/minhas-turmas` é leitura derivada, sem entidade nova

Aulas das comunidades do Mestre em sessão, com as atividades de que ele é autor, agrupadas por
`FormatoDeAtividade`. Reusa `escopo_de_comunidade_da_leitura` de `aulas/regra.py` e a posse de
trilha para filtrar as atividades. Paginada no padrão de `PaginaDeResultado`, como a agenda.

## Risks / Trade-offs

- **A rota nova de lançamento duplica a montagem de `ResultadoDeclarado` que `aulas/rotas.py`
  já faz** → o trecho comum sai para uma função de `resultados/regra.py`, consumida pelas duas
  rotas, em vez de copiada.
- **O teto conferido por contagem corre risco de escrita concorrente** → a conferência e a
  inserção ficam na mesma transação, como a reverificação de lastro da troca já faz.
- **`motivo` anulável pode ser lido como "motivo opcional"** → a regra exige o motivo na
  criação e o modelo documenta que a nulidade existe para o expurgo, não para a entrada.
- **A fatia deixa `RN-01-52` sem executor** → o Ciclo 01 termina em dezembro de 2026; a
  pendência precisa de decisão antes disso, e a proposal a registra no documento 09.

## Migration Plan

Migração de banco criando `ocorrencia_de_conduta`. Sem alteração de tabela existente e sem
retrocompatibilidade a preservar: nenhuma linha existe hoje. Rollback é derrubar a tabela — as
três outras rotas não dependem dela.
