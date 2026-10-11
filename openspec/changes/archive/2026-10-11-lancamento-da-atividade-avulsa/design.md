# Design

## Context

Ver `proposal.md` — Why. O que molda o desenho é o que **já existe** e não precisa nascer:

- `POST /v1/atividades/{id}/lancamentos` (`resultados.regra.lancar_resultados_da_atividade`) é
  o ato **por atividade**, que grava Resultados sem consumir reserva nem alterar a situação da
  aula. A matriz de permissões dá `Operacao.tudo` ao Admin, então ele já alcança a rota.
- `Atividade.aula_id` já é coluna, anulável, e `Equipe.atividade_corrente_id` já liga a equipe
  da aula a uma atividade sem passar por missão.
- `registrar_resultado` já restringe ao Admin a atividade sem missão e já credita o ponto
  regular no poder declarado.
- `Presenca` já é única por (aula, guerreiro) entre as não anuladas, com índice parcial.

O que falta é pequeno e está nas specs do delta.

## Goals / Non-Goals

**Goals:**

- Fechar o caminho da avulsa reaproveitando o ato por atividade, sem rota nova.
- Pôr no **núcleo**, não na tela, as regras do documento 11 §4 sobre o lançamento por equipe.

**Non-Goals:**

- Tocar `painel_do_dia._atividades_previstas` e `equipes.programacao_do_encontro`.
- Mexer no ato **por aula**, nas reservas, na baixa e na situação da aula.
- Rota nova no núcleo.

## Decisions

**1. Reaproveitar `POST /v1/atividades/{id}/lancamentos`, sem rota nova.** É o mesmo ato, com a
mesma semântica — grava Resultados e nada mais — e o Admin já o alcança. Descartada rota
própria para a avulsa: duplicaria a regra de gravação por uma diferença que é de dado, não de
ato.

**2. A entrada aceita `equipe_id` **ou** a lista `resultados`, nunca as duas.** O 422 da
ausência e o da presença simultânea ficam na regra, como em `Equipe`, que já usa esse par
exclusivo com `CheckConstraint`. Descartado expandir a equipe no frontend: a regra "igual a cada
integrante presente" e o pulo de quem faltou são do documento 11 §4, e na tela ficariam fora do
alcance dos testes do núcleo e invisíveis a qualquer outro consumidor da API.

**3. O recorte dos presentes é consulta a `Presenca` com `anulada_em IS NULL`.** Mesma condição
do índice parcial que já existe, para que "presente" signifique no lançamento o que significa na
conferência de presença.

**4. A unicidade de (Guerreiro(a), atividade) nasce em dois lugares: regra e índice.** A regra
devolve o 422 com a mensagem legível; o **índice único** em `resultado (guerreiro_id,
atividade_id)` trava a corrida entre dois envios simultâneos. Sem o índice, dois cliques
rápidos dobrariam o ponto, e o Resultado não se edita nem se remove (405) — não haveria
conserto. Índice **total**, não parcial: diferente da presença, o Resultado não tem anulação.

**5. A obrigatoriedade da aula na avulsa fica na regra, não no esquema.** Um
`CheckConstraint` condicional (`poder_id IS NULL OR aula_id IS NOT NULL`) seria possível, mas
`atividade.aula_id` precisa seguir anulável para a atividade de trilha, e a conferência de aula
existente, não cancelada e da comunidade escolhida já é consulta — não cabe em constraint. Não
há ganho em dividir a mesma regra entre dois lugares.

**6. A comunidade não vira coluna.** É passo do formulário da App 03, que estreita a lista de
aulas; o núcleo a deriva da aula. Decisão do fundador de 2026-10-11, documento 09 §1.
Descartado guardá-la na `Atividade`: dois lugares para a mesma verdade, e um 422 de
conferência que só existiria para proteger a duplicidade.

## Risks / Trade-offs

**A migração do índice único pode falhar sobre dado já gravado** — se existir Resultado
duplicado para o mesmo par, a criação do índice é recusada → a tarefa de migração **confere
antes** e, havendo duplicata, **para e leva ao fundador**. Resultado não se apaga (`RF-09-47`),
então a limpeza nunca é decisão da change.

**Atividade avulsa já cadastrada sem aula** fica inválida pela regra nova e não se consegue
lançar → a tarefa de migração as **conta e relata**; atribuir aula a elas é decisão do fundador,
não suposição do artefato.

**O lançamento por equipe falha inteiro se um integrante tropeça** — é o comportamento que o ato
por atividade já tem ("um participante inválido recusa o lançamento inteiro") e se mantém:
meia equipe lançada seria pior, porque não há como desfazer a metade gravada.

**A tela precisa saber a modalidade para escolher a forma de lançar.** `GET /v1/atividades` já
devolve `modalidade`, então não há leitura nova — mas a recusa do núcleo (`RN-02-33`) continua
sendo a autoridade, e a tela apenas evita o erro previsível.
