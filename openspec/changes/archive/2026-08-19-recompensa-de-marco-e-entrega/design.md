## Context

Ver `proposal.md` — Why. A fatia aplica um padrão já consolidado: `ItemDeCatalogoAvulso 1─N
Troca ─1 Lancamento` é a mesma anatomia de `RecompensaDeMarco 1─N EntregaDeRecompensa ─1
Lancamento`, e `openspec/specs/troca-de-recompensa-avulsa/spec.md` já traz a forma —
recusas antes de qualquer escrita, operação atômica, valoração pela vigência corrente.

O que **não** é padrão consolidado, e por isso está aqui: a recompensa de marco é a primeira
entidade do núcleo que pende da **trilha**, e a trilha é bem comum — `openspec/specs/
trilha-e-missao/spec.md` proíbe vinculá-la a comunidade. Toda decisão abaixo decorre disso.

## Goals / Non-Goals

**Goals:**

- Emitir a baixa definitiva da recompensa conquistada, com as cinco recusas do delta.
- Reusar a derivação de percurso que `pontuacao` já faz, sem duplicar a consulta.

**Non-Goals:**

- Fila ou painel de entregas pendentes do Mestre (PRD-09 §5, item 5) — é da App 09.
- Reposição do estoque esgotado como necessidade de recurso: a necessidade hoje é derivada da
  aula, e ampliá-la é fatia própria.

## Decisions

### O marco aceito é só a missão

Das quatro espécies do documento 02 §8.1, só a **missão** existe no núcleo: não há
`Culminancia` (PRD-09), não há `Batalha` (PRD-10) e a etapa do ciclo ainda não é atributo da
`Missao` implementada. Aceitar as outras três criaria marco cuja conquista o núcleo não sabe
verificar — e a quinta recusa ficaria inexequível, o mesmo defeito que a decisão do lastro
acabou de corrigir. O documento 02 §8.1 chama a missão de "marco de uso corrente" e diz que é
por ela que saem a camisa, o livro e o kit, então o recorte não perde nada do Ciclo 01.

_Alternativa descartada:_ aceitar as quatro e verificar só a missão — deixaria três espécies
entregáveis sem conferência alguma.

### O percurso é lido de `pontuacao`, não reconsultado

`pontuacao/regra.py` já tem `_missoes_concluidas_pelo_guerreiro`, que deriva as missões
concluídas dos `Resultado`s. A quinta recusa promove essa função a pública e a chama; não
duplica a consulta nem cria tabela de percurso.

_Alternativa descartada:_ consultar `Resultado` direto do módulo novo — duplicaria a regra de
o que conta como missão concluída, que é da capacidade `pontos-niveis-e-badges`.

### A comunidade conferida é a do Guerreiro(a)

A trilha não tem comunidade, e a entrega não tem aula. Sobra o vínculo que já existe: o Mestre
precisa estar vinculado à Comunidade Virtual do Guerreiro(a). É o mesmo precedente do
cancelamento de aula e do filtro da lista de necessidades — conferir contra o vínculo que já
existe, sem campo novo.

### O ponto de apoio é escolhido no ato da entrega

Como a trilha alcança todas as comunidades, o ponto de apoio não pode vir da declaração do
marco. Ele é informado na entrega, e é contra o saldo dele que a segunda recusa confere o
lastro. Não há verificação de que o ponto de apoio pertença à comunidade do Guerreiro(a) além
do que a própria leitura de saldo impõe: o PRD não a exige.

### A quantidade é contada, não decrementada

`RecompensaDeMarco.quantidade` é o teto declarado; a terceira recusa compara com a **contagem
de entregas** daquela recompensa. Diferente do `ItemDeCatalogoAvulso`, cujo estoque é
decrementado, aqui o saldo derivado é a forma que o livro-razão já usa — e evita um número
editável, que `RN-07-15` recusa em toda a economia.

_Alternativa descartada:_ decrementar um campo `entregues` — seria estado guardado à parte,
recontável divergindo do fato.

### Módulo novo em `backend/src/nucleo/recompensas_de_marco/`

Segue o desenho de `trocas/` — `modelo.py`, `regra.py`, `rotas.py`. Não entra em `trilhas/`,
que hoje só tem `modelo.py` e `regra.py` e é autoria, nem em `livro_razao/`, que é o ledger.

## Risks / Trade-offs

- **A entrega não confere presença nem aula** → é deliberado, e repete a decisão da troca: o
  núcleo registra o ato, o Mestre julga o momento. A quinta recusa já garante que a conquista
  aconteceu.
- **Trilha publicada pode prometer o que nenhum ponto de apoio tem** → a promessa passa a ser
  guardada na entrega, não na publicação. O risco real é o Guerreiro(a) alcançar o marco e não
  receber; a mitigação é operacional no Ciclo 01 (o Mestre vê a recusa e aporta ou absorve),
  e a mitigação em produto é a necessidade de recurso, deixada fora desta fatia.
- **Promover uma função privada de `pontuacao`** → amplia a superfície pública daquele módulo;
  o ganho é não ter duas definições de missão concluída.

## Migration Plan

Somente inserção de tabelas novas — `recompensa_de_marco` e `entrega_de_recompensa`. Nenhum
lançamento existente é alterado: `Lancamento` já aceita débito sem aula, do caminho da troca,
e nenhuma coluna nova é exigida dele. Rollback é a remoção das duas tabelas.
