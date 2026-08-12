## Context

Ver `proposal.md` — Why. Da quinta fatia já existem `Poder`, `Trilha`, `Missao` e `Atividade`,
com `ComAutoria` e a matriz de posse do Mestre autor (`trilhas/regra.py`). Não existe ainda
nenhum registro de que um Guerreiro(a) realizou algo — é a lacuna que `Resultado` fecha.

O documento 11 §5 é a fonte única da tabela de pontuação; §6, dos critérios de nível; §7, dos
tipos de badge. Esta fatia aplica esses três, sem reabrir nenhum número.

## Goals / Non-Goals

**Goals**

- Fechar `RF-01-20` com o objeto que faltava (`Resultado`), sem inventar rota para lançá-lo.
- Tornar a régua de pontuação, nível e badge testável por unidade, sem depender de PRD-07, 08 ou
  09 para os critérios que não precisam deles.
- Deixar explícito, no esquema, o que esta fatia não certifica — nível 3/5, badge de território,
  de autoria e Guardião do Acervo —, para a próxima fatia encontrar o gancho, não reconstruir.

**Non-Goals**

- Rota de lançamento de Resultado: é do PRD-09 (Mestre) e do PRD-02 (gestão).
- Débito do saldo disponível por troca: precisa da `Troca` do PRD-07 (`RF-01-60`).
- Nível 3 (série de coleta), nível 5 (culminância), badge de território, badge de autoria,
  Guardião do Acervo: dependem de PRD-08, PRD-09 ou de `Aula/Agenda`.
- Leitura pública ou para jogos (`RF-01-22`, `RF-01-59`): a rota é a mesma da vitrine, travada
  pela pendência de números do documento 09.
- Pontuação negativa: pendência de prazo de guarda no PRD-01 §14.

## Decisions

### `Resultado` referencia `Atividade`, não `Missao` nem `Trilha`

O Resultado carrega `atividade_id`; trilha e missão são alcançadas pela relação já existente
(`Atividade.missao_id` → `Missao.trilha_id`). Guardar `trilha_id` ou `missao_id` direto no
Resultado duplicaria dado que já é navegável e abriria a possibilidade de inconsistência entre a
atividade e a trilha declaradas.

Alternativa descartada: desnormalizar `trilha_id` no Resultado para facilitar a consulta de
"pontos por trilha" — adiado até a consulta real (vitrine) mostrar que o `JOIN` pesa.

### O desfecho é enumeração fechada de três valores

`realizada`, `realizada_com_merito`, `merito_extra_por_auxilio` — os três que o documento 11 §4
declara. Fechada, e não `String` como a natureza da atividade: aqui o documento não anuncia lista
aberta, ao contrário da natureza (que já firmou o padrão na quinta fatia).

### O valor-base de pontos vem da combinação de modalidade, sem tabela nova

A tabela do documento 11 §5 ("Desafio semanal") resolve para uma regra única a partir da
`modalidade` já gravada na atividade: **20** se `em_equipe_com_familiar`, **10** nos outros três
valores (`individual`, `em_equipe`, e qualquer `formato`). O `formato` não muda o valor-base — a
tabela lista "atividade on-line" e "atividade presencial" com o mesmo número. `realizada_com_
merito` soma **+5** regular e **+5** extra ao valor-base; `merito_extra_por_auxilio` soma **+10**
regular e **+10** extra. Nenhum número é novo: os quatro vêm literalmente do documento 11 §5.

Alternativa descartada: tabela de pontos por natureza da atividade — o documento 11 §5 não
tabela por natureza para as fontes desta fatia; forçaria uma correspondência que o texto não
declara.

### Nível e badge são derivados, não persistidos como fato isolado

`Nivel` e `Badge` guardam o que foi **certificado** (trilha ou poder, o valor do nível ou o tipo
do badge, quando), mas a certificação em si é resultado de uma consulta sobre `Resultado` e
`Missao.obrigatoria` — não um contador incrementado a cada Resultado. Persistir o fato certificado
(e não recalcular a cada leitura) é o que permite "nível conquistado nunca regride" sem lógica
extra: uma vez gravado, o registro não é apagado nem quando o critério deixa de valer.

Alternativa descartada: calcular nível e badge sempre em tempo de leitura, sem persistir — falha
o requisito de não regressão assim que uma missão obrigatória for despublicada ou um Resultado
for estornado por auditoria (fatias futuras).

### As duas contas do ponto extra são colunas do mesmo registro, não tabelas separadas

Uma linha por Guerreiro(a) com `acumulado` e `saldo_disponivel`, e todo crédito soma nas duas na
mesma transação. Guardar o extra como *ledger* de lançamentos (um registro por evento) fica para
quando o débito por troca existir e a auditoria precisar do histórico linha a linha — esta fatia
só credita, e a soma direta nas duas colunas é suficiente e mais barata de consultar.

Alternativa descartada: *ledger* de lançamentos desde já — antecipa uma necessidade que só chega
com a troca (PRD-07), na linha do princípio de não desenhar para requisito hipotético.

## Risks / Trade-offs

- **Recalcular nível e badge em cada Resultado é caro se a trilha crescer muito** → nesta fatia o
  volume por Guerreiro(a) é pequeno (poucas trilhas, poucas missões); reavaliar índice quando a
  consulta real da vitrine existir.
- **Sem rota nesta fatia, a regra de crédito fica sem exercício de ponta a ponta** → coberta por
  teste de unidade sobre a função de regra, como a posse da trilha na quinta fatia; o PRD-09
  pendura a chamada quando a rota de lançamento nascer.
- **Guardar acumulado/saldo como soma direta perde o detalhe por evento** → aceitável enquanto só
  há crédito; a migração para *ledger*, se vier, é aditiva e não quebra o que já foi somado.

## Open Questions

Nenhuma. As duas lacunas que apareceram ao desenhar esta fatia — se Guardião do Acervo nasceria
aqui e se `RF-01-22` teria rota própria — já foram resolvidas na proposta: nenhuma delas é desta
fatia.
