## Context

Ver `proposal.md` — Why. Da quinta e sexta fatias já existem `Trilha` (com `ComAutoria` e
`conferir_posse_da_trilha`) e o motor de `pontuacao/` — `creditar_ponto_regular`,
`avaliar_niveis` (níveis 1, 2, 4) e os badges de nível e de valores/causas. O comentário de
`avaliar_niveis` já registrava a lacuna do nível 5 como dependente de "entidade de outro PRD"; a
leitura do PRD-09 §8 mostra que a entidade que falta é `CriacaoOriginal`, do próprio PRD-01.

O documento 11 §5 é a fonte única do valor de pontos (50, integrais), §6 do critério do nível 5
e §7 do badge de autoria. Esta fatia aplica os três, sem reabrir nenhum número.

## Goals / Non-Goals

**Goals**

- Fechar `RF-01-26` com a entidade `CriacaoOriginal` e o fluxo mínimo de entrega e validação.
- Fechar o nível 5 e o badge de autoria que `avaliar_niveis` e o catálogo de badges já
  anunciavam como pendentes, reaproveitando o motor de pontuação existente.
- Manter a trava antifraude do documento 11 §5.1: uma validação nunca credita duas vezes.

**Non-Goals**

- `Culminancia` e `RecompensaDeMarco` — atributos do PRD-09 (proposal.md já registra).
- Crédito em equipe — depende de `Equipe` (RF-01-37 a RF-01-39).
- Reenvio de uma criação devolvida ("para ajuste"). O modelo de dados comporta a transição de
  volta a "entregue" no futuro, mas nenhuma regra desta fatia a implementa — é fluxo do PRD-09
  (`RF-09-34`), que decide se reaproveita o mesmo registro ou abre um novo.
- Rota HTTP: como a quinta e a sexta fatias, esta entrega entidade e regra, sem rota de gestão.
- Motivo estruturado de devolução: não é exigido por `RF-01-26`; fica para o PRD-09.

## Decisions

### `CriacaoOriginal` referencia `Trilha` direto, não `Atividade`

Ao contrário de `Resultado`, que nasce de uma atividade específica, a criação original é o
fechamento da trilha inteira (documento 11 §2, "Culminância: encerramento de toda trilha") — não
há uma atividade a que ela pertença. `trilha_id` direto, como `PontoRegular` e `Nivel` já fazem.

### Um registro por Guerreiro(a) e trilha, com restrição de unicidade

`UniqueConstraint(guerreiro_id, trilha_id)`, no mesmo padrão de `PontoRegular` e `Nivel`. Evita
crédito duplicado de pontos e do badge de autoria a cada nova tentativa de validação, e mantém a
trava antifraude do documento 11 §5.1 sem lógica extra: só existe um registro para validar.

Alternativa descartada: sem unicidade, permitindo várias entregas por trilha — abriria brecha
para revalidar e creditar pontos repetidas vezes, e o documento não descreve múltiplas criações
originais por trilha.

### Autoria (`ComAutoria`) é sempre do Guerreiro(a) que entrega; validação usa campos próprios

`ComAutoria.autor_id` grava o Guerreiro(a) na entrega — a mesma permissão que o PRD-01 §4 já
lista ("Guerreiro(a) escreve... suas criações") — e nunca muda depois (`RN-01-13`). A validação
ou devolução, feita pelo Mestre autor da trilha ou por um Admin, grava em campos próprios
(`validado_por_id`, `validado_em`), preenchidos só na transição. Reaproveitar `ComAutoria` para o
validador sobrescreveria a autoria da criação, violando `RN-01-13`.

Alternativa descartada: um segundo mixin de autoria genérico para "quem validou" — desnecessário
para dois campos; `ComAutoria` já resolve o caso de uma autoria única por registro.

### Situação é enumeração fechada de três valores, mutável

`entregue`, `validada`, `devolvida` — mesmo padrão de `SituacaoDaTrilha`. A regra só aceita a
transição partindo de "entregue"; validar ou devolver um registro que não está "entregue" é
recusado, o que também impede crédito duplo por chamada repetida.

### Crédito de pontos, nível 5 e badge de autoria vivem em `pontuacao/regra.py`

Mesmo padrão de `creditar_pontuacao_do_resultado`: um ponto de entrada único
(`creditar_pontuacao_da_criacao_original`), chamado pela regra de validação de
`criacoes_originais/regra.py`, que credita os 50 pontos regulares, certifica o nível 5 (função
nova, separada de `avaliar_niveis`, já que o gatilho não é `Resultado`) e concede o badge de
autoria (mesmo padrão de `conceder_badge_de_valores_e_causas`, sem guarda extra de duplicidade
porque a unicidade do registro já impede revalidação).

Alternativa descartada: colocar o crédito dentro de `criacoes_originais/regra.py` — duplicaria a
localização da régua de pontuação, hoje centralizada em `pontuacao/`, e quebraria o padrão que a
sexta fatia já fixou para `Resultado`.

## Risks / Trade-offs

- **Sem reenvio nesta fatia, uma criação devolvida fica sem caminho de ajuste até o PRD-09** →
  aceitável: o PRD-01 entrega entidade e regra, não o fluxo de autoria completo; o modelo já
  comporta a transição de volta quando aquela fatia chegar.
- **Sem rota nesta fatia, a regra de crédito fica sem exercício de ponta a ponta** → coberta por
  teste de unidade sobre a função de regra, como já vale para trilha, missão, atividade e
  resultado.
- **Unicidade por (guerreiro_id, trilha_id) impede múltiplas tentativas dentro desta fatia** →
  intencional, pela trava antifraude; se o PRD-09 precisar de reenvio, ele atualiza o mesmo
  registro, não cria um segundo.

## Open Questions

Nenhuma. As duas dúvidas que apareceram ao desenhar esta fatia — se a validação deveria
sobrescrever a autoria e se caberia reenvio após devolução — já foram resolvidas acima: a
autoria nunca muda (`RN-01-13`), e o reenvio fica para o PRD-09.
