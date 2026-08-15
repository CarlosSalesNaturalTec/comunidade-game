## Context

Ver `proposal.md` — Why. O que o desenho precisa levar em conta:

- `SerieDeColeta.estado` existe como `VARCHAR(16)`, com domínio de um único valor, `ativa`.
  O `sa.Enum(..., native_enum=False)` do projeto **não cria CHECK constraint** — a migração
  que criou a tabela confirma —, de modo que ampliar o domínio é mudança só de Python.
- `SerieDeColeta.ultima_medicao_valida_em` é gravado a cada registro válido e **não tem
  nenhum leitor** até esta fatia.
- `periodo_de_cadencia(momento, cadencia)` já delimita o período civil — dia, semana de
  segunda a domingo, mês — no fuso do projeto. A docstring dela declara, desde a fatia
  anterior, que "a entrega seguinte conta períodos seguidos sem registro com a mesma régua".
- O Ciclo 01 roda **sem agendador**: um contêiner no Cloud Run, sem tarefa periódica onde
  pendurar uma varredura de séries.

## Goals / Non-Goals

**Goals:**

- Um único ponto de apuração do estado, que toda leitura e toda escrita consultem.
- Estado correto sem agendador e sem varredura.
- Tornar o crédito do registro **estruturalmente** independente do estado, e não dependente
  de alguém lembrar de não escrever a condicional.

**Non-Goals:**

- Recontar ou recompor pontos de período parado — a retomada não recupera nada.
- Notificar o Guerreiro(a) do primeiro período vazio: o documento 09 fecha o Ciclo 01 sem
  notificação por e-mail, e o aviso do PRD-08 §5.4 é leitura na aplicação, não envio.
- Filtrar séries por estado em SQL: quem precisa disso é a amostra da auditoria
  (`RN-08-20`), de outra fatia.

## Decisions

### O estado é derivado; a coluna é espelho, gravado só quando diverge

A fonte da verdade é `f(ultima_medicao_valida_em, aberta_em, cadencia, vigencia_fim, agora)`.
Toda leitura deriva antes de responder e, **quando o derivado diverge do gravado**, persiste a
transição no mesmo ato. Quando não diverge, a leitura não escreve nada.

```text
   gravação de registro            leitura das séries
   (o coletor registra)            (o Guerreiro abre a App 05)
            │                                 │
            └──────────► mesma função ◄───────┘
                  derivado ≠ gravado → persiste
                  derivado = gravado → leitura pura
```

É o precedente da change `ciclo-de-vida-da-chave-de-terceiro` — transição por decurso decidida
na leitura e persistida no mesmo ato — com uma guarda que aquela não precisava. Lá a transição
era **monótona** (vigente → revogada); aqui é **reversível** (ativa ⇄ interrompida), e sem a
guarda toda consulta viraria escrita. Com ela, uma série transita no máximo uma vez por período.

A coluna permanece porque o PRD-08 §8 a declara atributo da série e porque a amostra da
auditoria, o painel público e a consulta do Guerreiro(a) vão querer filtrar por ela em SQL. Ela
é espelho: **nunca é lida como fonte**.

_Alternativas descartadas:_ derivação pura sem coluna — perderia o filtro em SQL de que
`RN-08-20`, `RF-08-16` e `RF-08-17` precisam. Persistir em toda leitura, sem a guarda — faria
cada `GET` escrever mesmo sem transição. Tarefa periódica — não há agendador no Ciclo 01.

### A régua dos períodos é a de `periodo_de_cadencia`, e a âncora é a última medição válida

Seja `P(t)` o período civil que contém `t`, e a **âncora** a `ultima_medicao_valida_em` ou,
quando ela for nula, a `aberta_em`. A série está **interrompida** quando `P(agora)` é ao menos
o **terceiro** período contado a partir de `P(âncora)` — o que equivale a **dois períodos
completos sem registro** entre um e outro.

```text
cadência semanal, registro na semana 1

 sem 1      sem 2      sem 3      sem 4
 [reg]      [ vazia ]  [ vazia ]  ← agora
   │            1º         2º
   └── âncora   período    período      → interrompida
                completo   completo
                vazio      vazio

agora na semana 3 → só um período completo vazio → ativa
                    ("uma falha isolada não interrompe", documento 02 §1)
```

Contar períodos, e não subtrair datas, é o que faz a régua valer igual para a cadência mensal,
cujo período não tem duração fixa.

O período da âncora **não conta como vazio**, e é por isso que a série aberta no meio de um
período não é punida pelo resto dele. Trata a abertura como trata a medição: uma e outra são o
marco a partir do qual se começa a contar.

_Alternativa descartada:_ contar o período da abertura como vazio — interromperia mais cedo a
série aberta perto do fim de um período, sem que o PRD peça essa distinção.

### `encerrada` prevalece, e é terminal

A ordem de apuração é `encerrada` → `interrompida` → `ativa`. Vigência terminada decide
primeiro, e não se reavalia: no Ciclo 01 não há requisito de edição de desafio, logo
`vigencia_fim` não se move e o estado não volta.

Não é preciso barrar o registro em série encerrada: a gravação já recusa com **422** medição
fora da vigência do desafio, desde a fatia anterior. As duas regras se encontram no mesmo
`vigencia_fim`.

### O crédito não consulta o estado — é a ordem do caminho de escrita que garante

A decisão fechada com o fundador é que o registro que retoma **credita normalmente**. Em vez
de escrevê-la como condicional, o desenho a torna estrutural:

```text
grava o registro  →  credita (RN-08-05, RN-08-06)  →  atualiza a âncora
                            │
                            └── nunca lê `estado`
```

O crédito segue condicionado apenas a registro válido e à quantidade que o desafio declara
pontuar — como a spec de `pontos-niveis-e-badges` já diz. Não há ponto no caminho de escrita
onde o estado seja consultado, então não há onde a condição indevida nascer. A retomada é
consequência de a âncora ter avançado, não um ato à parte.

### `ultima_medicao_valida_em` recebe o máximo, não a última gravação

Hoje o campo é atribuído sem comparação, e uma medição antiga enviada depois de uma recente o
move para o passado — o que faria a série aparecer interrompida sem motivo. Passa a receber o
**maior** entre o valor gravado e a data da medição. É conserto contra a definição do campo em
PRD-08 §8 ("data da **última** medição válida"), não regra nova.

### Sem migração do Alembic

O domínio do enum vive só em Python: a coluna é `VARCHAR(16)` sem CHECK. Acrescentar
`interrompida` e `encerrada` não muda o schema, e nenhuma linha existente precisa de
retroajuste — toda série gravada até aqui está `ativa`, e a primeira leitura de cada uma
apura o estado que lhe cabe.

## Risks / Trade-offs

- **Espelho defasado numa série que ninguém lê** → o espelho nunca é fonte: toda leitura
  deriva antes de responder, então nenhuma resposta da API sai errada. O que fica defasado é
  só a linha no banco, até alguém tocá-la. A fatia da auditoria, que vai filtrar por SQL,
  precisa saber disso — está anotado aqui para ela.
- **A leitura escreve no instante da transição** → limitado pela guarda de divergência: no
  máximo uma escrita por série por período, e nenhuma quando nada mudou.
- **Duas requisições simultâneas persistindo a mesma transição** → escrevem o mesmo valor
  derivado da mesma âncora; a última a gravar não altera o resultado.
- **A consulta soma os pontos de cada série** → é agregação sobre `registro_de_coleta`, que é
  particionada por tempo e cresce sem limite. No Ciclo 01 o volume por Guerreiro(a) é pequeno;
  se crescer, a saída é totalizar na série, não mudar a regra.

## Migration Plan

Não há passo de banco: a mudança é de código. O deploy é o de sempre, e o rollback é voltar a
imagem anterior — o espelho gravado com `interrompida` ou `encerrada` seria lido pela versão
antiga como valor fora do domínio dela, então o rollback pede a mesma janela de atenção de
qualquer ampliação de enum. Nenhum dado se perde nos dois sentidos.

## Open Questions

Nenhuma. As três decisões que travavam o recorte foram fechadas com o fundador antes da
abertura da change, e estão registradas acima: o registro que retoma credita, o estado é
derivado com espelho gravado só quando diverge, e ambas são interpretação do que já está
escrito — sem regra nova a gravar em `docs/`.
