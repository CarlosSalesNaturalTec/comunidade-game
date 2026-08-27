# Desenho — inscrição na trilha, guia do percurso e desafio de desbloqueio

## Context

Ver `proposal.md` — Why. O que o desenho precisa levar em conta, e que já existe:

- `Missao` tem `posicao`, `obrigatoria`, `e_sondagem` e `cadencia_de_retomada`
  (`backend/src/nucleo/trilhas/modelo.py`). A autoria do PRD-09 fechou tudo o que o
  Guerreiro(a) precisa **ler**; falta só o desafio de desbloqueio.
- `GET /v1/trilhas/{id}` já serve a trilha publicada com **conteúdo, bibliografia,
  atividades e disponibilidade do exemplar por `ponto_de_apoio_id`** — o docstring da rota
  diz que ela existe para "destravar o consumo pela App 05 e pela App 01".
- `pontuacao.regra.avaliar_niveis` certifica o nível 1 a partir de
  `missoes_concluidas_pelo_guerreiro`, que deriva de `Resultado`.
- A App 05 tem `AreaDoGuerreiro.tsx` com nav de dois blocos (coleta, carteira) e o comentário
  que reserva o terceiro para a trilha.
- **Nada** de bloqueio ou desbloqueio existe no núcleo: `desbloqueio` aparece só num
  comentário do modelo.

## Goals / Non-Goals

**Goals:**

- Duas entidades de fato datado — inscrição e desbloqueio — sem máquina de estados.
- O percurso **derivado na leitura**, não materializado numa tabela de estado por missão.
- Reaproveitar `GET /v1/trilhas/{id}` para conteúdo e bibliografia, sem duplicar pipeline.

**Non-Goals:**

- Não mexer na derivação dos níveis **2 e 4**, que seguem por `Resultado` (proposal —
  Documentação, pendência (b)).
- Não criar trava de publicação por falta de desafio de desbloqueio.
- Não guardar a produção da missão nem devolutiva: é a fatia seguinte.

## Decisions

**1. `InscricaoNaTrilha` e `DesbloqueioDaMissao` são tabelas de fato, não de estado.**
Ambas guardam apenas `guerreiro_id`, o alvo (`trilha_id` / `missao_id`) e o momento, com
unicidade no par. Segue o precedente de `Nivel` e de `CriacaoOriginal`: o que não se desfaz é
fato com data. *Alternativa descartada:* uma tabela `progresso_da_missao` com situação por
missão — cria estado a sincronizar e contradiz `RN-05-44`.

**2. O percurso é derivado na leitura, a partir de `posicao`.** A próxima missão é a de menor
`posicao` sem desbloqueio do Guerreiro(a); as de posição maior vêm bloqueadas, com o motivo
nomeando a anterior. *Alternativa descartada:* materializar "aberta/travada" por
Guerreiro(a) e missão — multiplicaria linhas por inscrição e exigiria recomputar a cada
publicação de missão nova.

**3. A sondagem entra no percurso pela `posicao`, não por regra à parte.** `e_sondagem` já é
única por trilha e a sondagem ocupa a primeira posição; o percurso não precisa de exceção — o
que muda é só que responder a sondagem **não** dispara `avaliar_niveis`.

**4. O desafio de desbloqueio é coluna da `Missao`, não entidade nova.** O PRD-09 §8 o lista
entre os atributos da missão, ao lado da cadência de retomada, e declarar de novo substitui —
o mesmo comportamento de `POST /missoes/{id}/retomada`, que já existe e serve de molde.

**5. Quiz o núcleo afere; prático o Mestre autor julga.** Decisão do fundador em 2026-08-27.
O quiz grava a submissão e o desbloqueio na mesma transação; o prático grava a **declaração**
do Guerreiro(a) e o desbloqueio só nasce no julgamento do Mestre. As duas formas produzem a
**mesma** linha de `DesbloqueioDaMissao` — quem a criou é que muda.

**6. As rotas `/v1/eu/*` carregam só o que é do Guerreiro(a).** Conteúdo, bibliografia e
atividades continuam vindo de `GET /v1/trilhas/{id}`, que a App 05 chama passando o
`ponto_de_apoio_id` dele. `GET /v1/eu/trilhas/{id}/missoes/{ordem}` devolve o **estado da
missão no percurso** — desbloqueada, próxima, bloqueada com motivo, aguardando o Mestre —, não
o conteúdo. Mantém a rota que o PRD-05 §9 declara, sem duplicar o que a capacidade
`conteudo-da-missao` já entrega. *Alternativa descartada:* uma rota `/v1/eu/*` que devolvesse
conteúdo e estado juntos — duplicaria a serialização do conteúdo e a regra da licença.

**7. `GET /v1/eu/progresso` responde por trilha inscrita.** Nível certificado, missões
obrigatórias desbloqueadas, quantas faltam para o próximo nível, e badges e recompensas por
trilha ou poder. Reaproveita `avaliar_niveis` e as consultas de badge que já existem; não
recalcula nada por conta própria.

**8. A segunda condição do nível 1 entra dentro de `avaliar_niveis`.** É uma consulta a mais
antes de certificar o `NIVEL_1`, no mesmo ponto em que a função já roda. Nenhum chamador muda.

**9. A App 05 ganha `src/trilha/`, terceiro item do nav.** Mesmo padrão de `coleta/` e
`carteira/`: um componente raiz `Trilha.tsx` e as telas do bloco, com `src/api/trilha.ts` para
as chamadas. A App 09 ganha a bancada do desafio junto da autoria de missão que já tem.

## Risks / Trade-offs

- **A mudança do nível 1 é retroativa** → Guerreiro(a) que já tem `Resultado` sem inscrição
  perde a certificação do nível 1 na próxima avaliação. No Ciclo 01 ainda não há turma em
  produção, e `avaliar_niveis` nunca regride nível **já certificado** — o risco é de dado de
  desenvolvimento, e a migração não apaga `Nivel` existente.
- **O percurso derivado custa uma consulta por leitura** → é leitura por Guerreiro(a) e por
  trilha, com índice no par; o volume do Ciclo 01 não justifica materializar.
- **Missão reordenada muda o percurso de quem já desbloqueou** → o desbloqueio é da missão,
  não da posição, então reordenar não apaga fato nenhum; a próxima missão pode mudar, e é o
  comportamento correto quando o Mestre reordena.
- **O julgamento do prático é fluxo novo, sem `RF` que o descreva** → nasce da decisão de
  2026-08-27 e é gravado no documento 11 §2.2 e no PRD-09 §9 **antes** de virar código, como
  a hierarquia de autoridade exige.

## Migration Plan

Duas migrações, ambas aditivas e sem backfill:

1. `inscricao_na_trilha` — tabela nova, unicidade em (`guerreiro_id`, `trilha_id`).
2. `desbloqueio_da_missao` — tabela nova, unicidade em (`guerreiro_id`, `missao_id`) — e a
   coluna do desafio de desbloqueio em `missao`, anulável.

Rollback: derrubar as duas tabelas e a coluna devolve o núcleo ao comportamento anterior,
menos a condição de inscrição do nível 1, que volta com o código.
