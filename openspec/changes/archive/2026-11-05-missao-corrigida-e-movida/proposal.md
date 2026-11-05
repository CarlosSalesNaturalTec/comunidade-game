# Proposal

## Why

Fatia **28 do PRD-09** (`openspec/cronograma-de-fatias.md`). Atende `RF-09-136`, `RF-09-137`,
`RF-09-139`, `RN-09-56`, `RN-09-57` e `RN-09-59`, criados pela decisão do fundador de
2026-11-05 (documento 09 §1, documento 03 §11, PRD-09 §§6.1, 7 e 9).

A missão é a última peça da trilha que ainda é rua de mão única: o conteúdo (fatia 24) e a
atividade (fatia 25) já se corrigem, a missão só nasce (`POST /v1/trilhas/{id}/missoes`). Não
há `PATCH` de `/v1/missoes/{id}`, e a linha da missão em "Minhas trilhas" só exibe posição,
título, etapa e obrigatoriedade. Título com erro de digitação, dificuldade mal declarada,
missão posta na etapa errada ou na posição errada são permanentes — e a posição é o que
`derivar_percurso` usa para dizer ao Guerreiro(a) qual é a próxima missão.

## What Changes

- **Nasce `PATCH /v1/missoes/{id}`** (`RF-09-136`), que corrige **título**, **nível de
  dificuldade**, **obrigatoriedade**, **etapa do ciclo** e **sondagem**, em qualquer situação
  da trilha. Valem as recusas da criação: título vazio, etapa fora dos quatro valores,
  obrigatoriedade nula, sondagem fora da primeira posição e segunda sondagem respondem **422**.
  A posição **não** é campo do `PATCH`: ela muda só pelo movimento.
- **Nasce `POST /v1/missoes/{id}/ordem`** (`RF-09-137`), no molde de `POST
  /v1/conteudos/{id}/ordem`: recebe `cima` ou `baixo` e troca a posição com a missão vizinha
  na sequência da trilha. Primeira para cima e última para baixo respondem 422 sem alterar
  nada. A sondagem não desce, e nenhuma missão sobe para o lugar dela (`RN-09-57`).
- **Autoria estrita** nas duas rotas (`RN-09-56`): só o Mestre autor da trilha; o Admin recebe
  **403**, como já acontece na correção do conteúdo e da atividade.
- **Desmarcar a sondagem de trilha publicada despublica a trilha** no mesmo ato (`RN-09-59`):
  é a única correção desta fatia que pode quebrar uma trava de publicação. A situação passa a
  despublicada, com o **Mestre autor** como autor dela e um motivo gerado pelo núcleo que
  nomeia a missão e a trava. É exceção à regra de que só o Admin despublica, e vale **somente**
  para esse efeito: o Mestre continua sem rota para despublicar a trilha por pedido.
- **A App 09 corrige e move a missão** na linha dela em "Minhas trilhas": o formulário da
  missão passa a servir criação e correção, e cada linha ganha subir e descer. Antes de
  confirmar a correção que despublica, a tela diz que a trilha sai do ar e que falta a
  sondagem (`RF-09-139`). O motivo da despublicação deixa de ser apresentado como "registrado
  pelo Admin", porque agora pode ser do próprio Mestre.

**Fora do escopo.** A **exclusão** da missão (`RF-09-138`, `RN-09-58`, `RN-09-60`) é a fatia 29.
O PRD-09 §3.2 já exclui a trilha de auditoria das escritas do Mestre (`RF-09-48`, Ciclo 02).
Reordenar a trilha publicada muda a próxima missão que `derivar_percurso` calcula, mas não
toca nenhum desbloqueio gravado — não há regra nova para isso, e nenhuma é criada aqui.

## Capabilities

### New Capabilities

Nenhuma.

### Modified Capabilities

- `trilha-e-missao`: a missão passa a se corrigir e a se mover, com as recusas da criação; a
  correção e o movimento ficam com autoria estrita, sem o Admin; a sondagem não sai da
  primeira posição; e a correção que tira a sondagem de trilha publicada a despublica, com o
  Mestre como autor da situação — exceção à despublicação só de Admin.
- `area-do-mestre`: a linha da missão corrige e move a missão, avisa antes da correção que
  despublica, e o motivo da despublicação deixa de ser atribuído sempre ao Admin.

## Impact

- `backend/src/nucleo/trilhas/regra.py` — `corrigir_missao` e `mover_missao`; as conferências
  de título, etapa, obrigatoriedade e sondagem extraídas de `criar_missao` para as duas usarem;
  e `_despublicar_por_trava`, que reusa `_travas_de_publicacao_pendentes`.
- `backend/src/nucleo/trilhas/rotas.py` — `PATCH /missoes/{id}` e `POST /missoes/{id}/ordem`.
- Sem migração: a unicidade `uq_missao_trilha_id_posicao` já é adiável.
- `apps/app-09-mestre/src/trilhas/api.ts` — `corrigirMissao` e `moverMissao`.
- `apps/app-09-mestre/src/trilhas/FormularioDeMissao.tsx` — criação e correção.
- `apps/app-09-mestre/src/trilhas/ListaDeMissoes.tsx` e `TelaDaTrilha.tsx` — corrigir, subir,
  descer, o aviso de despublicação e a situação da trilha atualizada pela resposta.
- `apps/app-09-mestre/src/trilhas/ListaDeTrilhas.tsx` — o texto do motivo.
- Documentação, no mesmo PR: PRD-09 §9, onde a rota de movimento passa de `/movimento` a
  `/ordem` para seguir o padrão do conteúdo (decisão 4 do fundador), e a situação da fatia 28
  no cronograma.
