# Tasks

## 1. Núcleo — correção da missão

- [ ] 1.1 Extrair de `criar_missao` (`backend/src/nucleo/trilhas/regra.py`) as conferências de
      título, obrigatoriedade, etapa e sondagem, com a da sondagem desconsiderando a própria
      missão; a criação passa a chamá-las sem mudar mensagem nem campo (`RF-09-136`,
      `RN-09-57`). Verificação: `uv run pytest tests/test_missao.py -x` segue verde.
- [ ] 1.2 `corrigir_missao` em `trilhas/regra.py`: autoria estrita, campos ausentes intocados,
      as conferências de 1.1 e, na transição da sondagem de verdadeiro para falso em trilha
      publicada, a despublicação com o Mestre como autor da situação e o motivo gerado a partir
      de `_travas_de_publicacao_pendentes` (`RF-09-136`, `RN-09-56`, `RN-09-57`, `RN-09-59`).
- [ ] 1.3 `PATCH /v1/missoes/{id}` em `trilhas/rotas.py`, com `CorrigirMissaoEntrada`
      (`extra="forbid"`, sem `posicao`) e resposta `{missao, situacao_da_trilha,
      motivo_da_situacao}` (`RF-09-136`, `RN-09-59`).
- [ ] 1.4 Testes em `backend/tests/test_missao_corrigida.py`:
      - correção de título, dificuldade, obrigatoriedade e etapa, em rascunho e em publicada;
      - desbloqueio e nível preservados;
      - recusas 422 de título vazio, etapa inválida, sondagem fora da primeira posição,
        segunda sondagem e `posicao` no corpo;
      - 403 para outro Mestre e para Admin;
      - sondagem desmarcada em publicada despublica com Mestre autor e motivo que nomeia a
        missão; em rascunho não despublica; correção de título em publicada não despublica;
        republicação depois de remarcar
      (`RF-09-136`, `RN-09-56`, `RN-09-57`, `RN-09-59`).
      Verificação: `uv run pytest tests/test_missao_corrigida.py -x`.

## 2. Núcleo — movimento da missão

- [ ] 2.1 `mover_missao` em `trilhas/regra.py`: autoria estrita, `DirecaoDoMovimento` reusada
      de `conteudos.regra`, vizinha pela sequência inteira da trilha, recusa da primeira para
      cima, da última para baixo, da sondagem para baixo e da que está logo depois da sondagem
      para cima; troca dos dois valores sob `SET CONSTRAINTS uq_missao_trilha_id_posicao
      DEFERRED` (`RF-09-137`, `RN-09-56`, `RN-09-57`).
- [ ] 2.2 `POST /v1/missoes/{id}/ordem` em `trilhas/rotas.py`, com resposta `{missoes: [a, b]}`
      (`RF-09-137`).
- [ ] 2.3 Testes em `backend/tests/test_missao_movida.py`:
      - subir e descer trocam só as duas posições, inclusive com lacuna na sequência e em
        trilha publicada;
      - as recusas 422 da primeira, da última, da sondagem e da vizinha da sondagem, e da
        direção inválida;
      - 403 para outro Mestre e para Admin;
      - desbloqueio preservado e próxima missão de `derivar_percurso` recalculada pela nova
        ordem
      (`RF-09-137`, `RN-09-56`, `RN-09-57`).
      Verificação: `uv run pytest tests/test_missao_movida.py -x`.

## 3. App 09

- [ ] 3.1 `corrigirMissao` e `moverMissao` em `apps/app-09-mestre/src/trilhas/api.ts`, com os
      tipos das duas respostas (`RF-09-136`, `RF-09-137`).
- [ ] 3.2 `FormularioDeMissao.tsx` serve criação e correção pela prop opcional `missao`: campos
      preenchidos, posição escondida, recusa do núcleo com o motivo; e, em trilha publicada com
      a sondagem desmarcada, a confirmação em linha de que a trilha sai do ar e de que falta a
      sondagem, antes de gravar (`RF-09-136`, `RF-09-139`, `RN-09-59`).
- [ ] 3.3 `ListaDeMissoes.tsx` e `TelaDaTrilha.tsx`: corrigir, subir e descer na linha de cada
      missão; os campos escalares da resposta sobrepostos à missão sem descartar os blocos; a
      situação e o motivo da trilha atualizados pela resposta do `PATCH`; a recusa do movimento
      sob a linha (`RF-09-136`, `RF-09-137`, `RF-09-139`).
- [ ] 3.4 `ListaDeTrilhas.tsx` e a tela da trilha deixam de atribuir ao Admin o motivo da
      despublicação (`RN-09-59`, `RF-09-10`).
- [ ] 3.5 Testes em `apps/app-09-mestre/src/trilhas/trilhas.test.tsx`:
      - correção de título;
      - mudança de etapa leva a missão de página;
      - subir reordena a lista;
      - a recusa do movimento aparece com o motivo;
      - o aviso de despublicação aparece antes de gravar, e desistir não grava;
      - confirmar apresenta a trilha despublicada com o motivo;
      - correção comum não pede confirmação
      (`RF-09-136`, `RF-09-137`, `RF-09-139`).
      Verificação: `vitest run src/trilhas/trilhas.test.tsx`.

## 4. Documentação

- [ ] 4.1 PRD-09 §9: a rota do movimento passa de `/v1/missoes/{id}/movimento` a
      `/v1/missoes/{id}/ordem` (design — decisão 3); `openspec/cronograma-de-fatias.md`: a
      fatia 28 vira `implementado`, com o slug da change. Nenhuma decisão nova, nenhum arquivo
      novo em `docs/` e nenhuma relação entre documentos muda.
