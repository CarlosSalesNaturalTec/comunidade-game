# Design

## Context

Ver `proposal.md` — _Why_. A fatia aplica à missão o padrão que as fatias 24 e 25 já
consolidaram para o conteúdo e a atividade (`openspec/specs/conteudo-da-missao`,
`openspec/specs/atividade-de-trilha`): autoria estrita, correção na linha com os campos
opcionais e `extra="forbid"`, e movimento que troca de lugar com a vizinha
(`conteudos.regra.mover_conteudo`). Três diferenças moldam o que é novo aqui:

- A posição da missão tem **unicidade** — `uq_missao_trilha_id_posicao`, criada adiável e
  `INITIALLY IMMEDIATE` justamente para a troca. O conteúdo não tem unicidade na `ordem`.
- A posição **é o percurso**: `derivar_percurso` escolhe a próxima missão pela ordem da posição.
- A sondagem é trava de publicação (`_travas_de_publicacao_pendentes`), e a correção pode
  tirá-la.

## Goals / Non-Goals

**Goals:** as conferências de campo da criação valem iguais na correção, sem cópia; a troca de
posição acontece numa transação, sem estado intermediário inválido.

**Non-Goals:** exclusão da missão (fatia 29); despublicação por qualquer outra correção — nesta
fatia só a sondagem quebra trava.

## Decisions

1. **As conferências saem de `criar_missao` para funções próprias** — título, obrigatoriedade,
   etapa e sondagem —, chamadas pela criação e pela correção, como a fatia 25 fez com
   `_conferir_titulo_da_atividade`. A da sondagem recebe a missão corrigida, para não se
   contar como "segunda sondagem" da trilha. _Descartado:_ chamar `criar_missao` em modo de
   correção — mistura duas portas com recusas diferentes (a posição).
2. **`CorrigirMissaoEntrada` com os cinco campos opcionais e `extra="forbid"`**: a `posicao`
   mandada responde 422 pelo próprio Pydantic, como a `natureza` na atividade.
3. **A rota do movimento é `POST /v1/missoes/{id}/ordem`, com `{"direcao": "cima" | "baixo"}`**,
   reusando `DirecaoDoMovimento`. O PRD-09 §9 dizia `/movimento`; passa a `/ordem` no mesmo PR,
   porque a decisão do fundador foi reaproveitar o padrão, e o padrão é `/conteudos/{id}/ordem`.
4. **A vizinha é a da sequência inteira da trilha, não a da etapa.** O percurso é um só e
   ordenado pela posição; trocar dentro da etapa pularia missões de outras etapas e mudaria o
   percurso mais do que o ato pedido. Posições com lacuna são aceitas: a vizinha é a próxima na
   ordem, e as duas trocam os valores que tinham. _Descartado:_ renumerar a trilha a cada
   movimento — altera missões que o ato não tocou.
5. **A troca roda com `SET CONSTRAINTS uq_missao_trilha_id_posicao DEFERRED`** na transação
   da rota; a unicidade é conferida no `COMMIT`. _Descartado:_ posição temporária negativa —
   três escritas e um valor inválido visível a quem ler no meio.
6. **A despublicação só dispara na transição da sondagem** — `e_sondagem` de verdadeiro para
   falso em trilha publicada —, não pela releitura geral das travas depois de toda correção.
   Trilha publicada antes de uma trava existir não sai do ar por uma correção de título. O
   motivo reusa `_travas_de_publicacao_pendentes` e `_unir_em_portugues`:
   `A correção da missão "<título>" deixou a trilha sem <travas>. Corrija e publique de novo.`
   Autor da situação é o Mestre, com o papel e o momento, nos campos que a despublicação do
   Admin já grava. A fatia 29 reusa a mesma função para a exclusão.
7. **Respostas.** O `PATCH` devolve `{missao, situacao_da_trilha, motivo_da_situacao}`; o
   movimento devolve `{missoes: [a, b]}`, as duas que trocaram. As duas trazem a missão sem os
   aninhados (conteúdo, bibliografia, desafio), como o `POST` da criação: a App 09 **sobrepõe
   os campos escalares** à missão que já tem, sem descartar os blocos. _Descartado:_ devolver a
   trilha inteira — repete `GET /v1/trilhas/minhas` a cada clique.
8. **Na App 09, `FormularioDeMissao` ganha a prop opcional `missao`**, no molde de
   `FormularioDeAtividade`: preenche os campos, esconde a posição e troca a chamada. O aviso de
   despublicação (`RF-09-139`) é decidido no cliente — trilha publicada e sondagem de verdadeiro
   para falso — e usa a confirmação em linha `role="alert"` que `BlocoDeAtividades` já usa,
   nunca `window.confirm`. Subir e descer ficam na linha da missão, e a recusa aparece sob ela.

## Risks / Trade-offs

- [Reordenar trilha publicada muda a próxima missão de quem está no meio dela] → nenhum
  desbloqueio é tocado (cenário na spec); o efeito é o que a decisão do fundador aceitou.
- [Duas abas do mesmo Mestre movendo ao mesmo tempo] → a unicidade adiada recusa no `COMMIT`; a
  tela apresenta a recusa e a ordem gravada vale.

## Migration Plan

Sem migração: nenhuma coluna nova, e a unicidade já é adiável desde a fatia 1.
