## Context

Ver `proposal.md` — Why. O que o núcleo já tem e condiciona o desenho:

- `RegistroDeColeta` já grava **`pontos_creditados`**, `a_conferir` e `situacao`, e é
  **particionada por RANGE em `momento_do_fato`**, com chave primária composta
  `(id, momento_do_fato)`. Quem apontar para o registro aponta para o par.
- `SituacaoDoRegistro` hoje só tem `valida`. O docstring dela já anota que `invalidada`, com o
  estorno, é a entrega desta fatia.
- `PontoRegular` é **um total somado por par (Guerreiro(a), trilha **ou** poder)**, sem detalhe
  por evento. O docstring dele já anota: "o detalhe por evento fica para quando o crédito
  precisar de estorno".
- Duas travas recusam hoje qualquer redução: o listener `_recusar_debito_de_ponto_regular` no
  ORM e o gatilho `trg_ponto_regular_nunca_debita` no PostgreSQL, que também recusa `DELETE`.
- `EstadoDaSerie` já distingue `ativa`, `interrompida` e `encerrada`, derivados da última
  medição válida.

## Goals / Non-Goals

**Goals:**

- Debitar ponto regular sem perder as duas garantias que a fonte impõe: piso em zero e nível e
  badge que não regridem.
- Estornar **o valor exato** que o registro creditou, sem depender de recalcular a régua de
  pontuação meses depois.
- Compor a amostra sem que o Mestre veja registro que já auditou, para que a auditoria termine.

**Non-Goals:**

- A **ocorrência de conduta** (`RF-02-38`): é do PRD-02. Esta fatia entrega a capacidade de
  debitar de que ela vai precisar, não a superfície dela.
- **Livro-razão de pontos** por evento: ver a decisão 1.
- Recalcular nível para baixo: a fonte proíbe, e não há caminho de código que o faça.

## Decisions

### 1. O estorno lê `pontos_creditados` do próprio registro, e não um livro-razão de pontos

O campo já existe, já é gravado no crédito e é imutável como o resto do registro. Ele diz
exatamente quanto aquele registro creditou — inclusive **zero**, no excedente da quantidade do
período e no "a conferir" ainda não confirmado —, que é precisamente o que o estorno precisa
devolver.

_Alternativa considerada:_ criar um lançamento por evento de pontuação, como o docstring de
`PontoRegular` antecipava. Rejeitada por ora: resolveria o mesmo problema com uma entidade
nova e uma migração maior, e o `RF-08-13` só pede o estorno **daquele registro**. Quando a
ocorrência de conduta do PRD-02 chegar, ela traz o seu próprio lastro; se aí um livro-razão de
pontos se justificar, ele nasce lá, com dois casos reais para desenhá-lo em vez de um.

### 2. A trava do PostgreSQL é estreitada, não removida

A função `recusar_debito_de_ponto_regular` e o gatilho passam a recusar **só** o que a fonte
segue proibindo:

```text
antes                             depois
─────────────────────────────     ─────────────────────────────
NEW.total < OLD.total  → erro     NEW.total < 0          → erro
TG_OP = 'DELETE'       → erro     TG_OP = 'DELETE'       → erro
```

O piso em zero é regra do documento 11 §5, não detalhe de implementação, e por isso continua
no banco — mesmo padrão de `RN-01-12` e do que a fatia anterior já fazia. O listener do ORM
acompanha: deixa de recusar a redução e passa a recusar o negativo, mantendo a recusa de
remoção.

_Alternativa considerada:_ derrubar a trava inteira e confiar no `CheckConstraint("total >= 0")`
que já existe. Rejeitada: o `CheckConstraint` cobre o piso, mas perderíamos a recusa de `DELETE`,
que nenhuma regra revogou.

### 3. A auditoria mora no próprio registro, sem entidade nova

O registro ganha `auditado_em`, `auditado_por_id` e `motivo_da_invalidacao`, e a `situacao`
ganha `invalidada`. É o mesmo julgamento que a fatia da credencial de dispositivo fez — "a
credencial é o próprio registro do aparelho" —, e o PRD-08 §8 já declara a situação como o único
campo que evolui.

`auditado_em` é o que tira o registro da amostra seguinte: sem ele, o "a conferir" voltaria
toda semana e a auditoria nunca terminaria.

### 4. A quantidade que pontua no período é reapurada na confirmação

Um "a conferir" não consome vaga do período enquanto não credita, porque a regra vigente conta
"quantos registros **válidos já pontuaram**". Na confirmação, a contagem é refeita: se o período
já se esgotou nesse meio-tempo, o registro é confirmado e credita **zero**.

A consequência é assimétrica de propósito: gravado segunda-feira um "a conferir" e terça um
registro dentro da faixa, num desafio em que só um pontua, quem leva os pontos é o de terça. É o
preço de não reservar vaga para medição que ainda não se sabe verdadeira, e o inverso —
reservar — daria ao valor suspeito precedência sobre o normal.

A invalidação **não** devolve a vaga a ninguém: recreditar registro alheio depois do fato não
está em requisito algum, e o spec o proíbe explicitamente.

### 5. A amostra é determinística, não sorteada

Dentro do contrato do spec — 10% por série, mínimo de um, todo "a conferir" —, a seleção dos
10% segue a **ordem de `momento_do_fato`** entre os ainda não auditados. Sorteio faria a amostra
mudar a cada chamada, e o Mestre nunca teria a mesma lista duas vezes; determinismo também torna
o teste possível sem semente.

O percentual arredonda **para baixo**, e é o mínimo de um que sustenta a série pequena — a
própria existência do piso na fonte mostra que o arredondamento previsto é esse.

### 6. "Semana" são os 7 dias anteriores ao pedido, pela hora da medição

A fonte diz "registros da semana" sem fixar a borda. A amostra é pedida sob demanda, então
janela móvel de 7 dias serve melhor que semana de calendário, e a apuração usa **`momento_do_fato`**,
como `RF-08-15` já manda para toda regra dependente de tempo.

## Risks / Trade-offs

- **Derrubar a trava de débito é o passo mais arriscado da fatia** → ela é estreitada no mesmo
  commit em que o piso em zero entra, e o teste que hoje prova "ponto regular não decresce" é
  reescrito para provar "não fica negativo" em vez de ser apagado.
- **`pontos_creditados` é a única fonte do estorno** → se um caminho de crédito futuro esquecer
  de preenchê-lo, o estorno vira silenciosamente zero. Mitigação: teste que credita e afirma que
  o campo e o saldo concordam, para cada caminho de crédito da coleta.
- **`ALTER TABLE` em tabela particionada** → as colunas novas entram pelo pai e descem às
  partições; a restrição de `CHECK` do enum `situacao`, que `native_enum=False` cria, precisa ser
  derrubada e recriada com o valor novo.
- **A assimetria da decisão 4 pode surpreender o Mestre** → é comportamento visível, coberto por
  cenário próprio no spec; se incomodar no encontro real, volta como decisão de produto, não como
  correção de código.
- **Nível não regride, mas o saldo cai** → um Guerreiro(a) pode ficar com nível acima do que o
  saldo corrente sugere. É o que a fonte manda, e a vitrine lê nível, não saldo.

## Migration Plan

1. Migração do Alembic, numa revisão só:
   - `ALTER TABLE registro_de_coleta` com `auditado_em`, `auditado_por_id` e
     `motivo_da_invalidacao`, todos nulos — registro já gravado nasce não auditado.
   - Derruba e recria a restrição de `CHECK` de `situacao`, agora com `invalidada`.
   - `CREATE OR REPLACE FUNCTION recusar_debito_de_ponto_regular` com a trava estreita; o gatilho
     não precisa ser recriado, porque aponta para a função pelo nome.
2. Sem retrocompatibilidade a preservar: nenhuma aplicação consome as rotas de coleta no Ciclo
   01, e não há registro invalidado em base alguma.
3. Rollback: a revisão `down` recria a função anterior e derruba as colunas. Registro invalidado
   entre a subida e o rollback perderia a marca — aceitável enquanto não há dado de produção.

## Open Questions

Nenhuma que trave a fatia. As bordas que a fonte não fixou — arredondamento do percentual e
janela da semana — estão resolvidas nas decisões 5 e 6, dentro do que o spec contrata; se o
encontro real pedir outra coisa, viram decisão de produto pelo fluxo normal.
