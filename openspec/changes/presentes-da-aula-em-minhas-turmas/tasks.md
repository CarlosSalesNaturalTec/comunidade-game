# Tarefas — Presentes da aula em Minhas turmas

## 1. Núcleo

- [ ] 1.1 `backend/src/nucleo/aulas/rotas.py` — `listar_minhas_turmas_rota` filtra
      `Aula.situacao != cancelada` na consulta, antes do cursor e do `limit` (`RF-09-42`,
      design — decisão 1).
- [ ] 1.2 `backend/src/nucleo/aulas/rotas.py` — nasce `GET /v1/aulas/{id_da_aula}/presencas`
      com `PresencaDaAulaSaida` (`id`, `guerreiro_id`, `nick`, `avatar`, `momento_do_fato`,
      `modo`): só presenças não anuladas, por `momento_do_fato`; Mestre fora das comunidades
      dele e aula inexistente → 404 com a mesma mensagem; operação `suas_turmas` (`RF-09-145`,
      `RF-09-42`, `RN-09-08`, `RN-09-18`, design — decisões 2 a 4).

## 2. App 09

- [ ] 2.1 `apps/app-09-mestre/src/turmas/api.ts` — tipo `PresencaDaAula` e
      `listarPresencasDaAula(idDaAula, token)` (`RF-09-145`).
- [ ] 2.2 `TelaDaAula.tsx` — seção "Presentes nesta aula": `Avatar` de `comum/avatar` com nick,
      hora e modo ("Reconhecimento"/"Confirmação"); mensagem de lista vazia; `Aviso` de erro só
      na seção; recarga após confirmação de presença bem sucedida (`RF-09-145`, `RF-09-45`,
      `RN-09-18`, design — decisão 5).
- [ ] 2.3 `TelaDeMinhasTurmas.tsx` — sai a seção "Atividades presenciais" e o filtro de
      cancelada da carga; `atividadesPresenciais` segue indo para `TelaDaAula`; comentário do
      componente atualizado (`RF-09-73`, `RF-09-42`, design — decisão 6).

## 3. Testes

- [ ] 3.1 `backend/tests/test_presenca_do_mestre.py` — minhas turmas: cancelada não devolvida;
      página cheia e cursor coerente com canceladas intercaladas (`RF-09-42`).
- [ ] 3.2 `backend/tests/test_presenca_do_mestre.py` — presenças da aula: Mestre lê nick,
      avatar, momento e modo; anulada some; aula sem presença dá lista vazia; aula de outra
      comunidade e aula inexistente dão 404 iguais; Admin lê; papel sem `suas_turmas` dá 403
      (`RF-09-145`, `RN-09-08`, `RN-09-18`).
- [ ] 3.3 `apps/app-09-mestre/src/turmas/turmas.test.tsx` — sem seção de atividades
      presenciais e com atalho de lançamento ainda na tela da aula; presentes listados por
      avatar e nick com hora e modo; lista vazia; falha da leitura com formulários ativos;
      confirmação recarrega a lista. Ajusta os testes da fatia 34 que dependiam do filtro na
      tela (`RF-09-145`, `RF-09-73`, `RF-09-45`, `RN-09-18`).

## 4. Documentação

- [ ] 4.1 PRD-09: `RF-09-73` reescrito (presenciais só dentro da aula), `RF-09-145` novo em
      §6.6, `GET /v1/aulas/{id}/presencas` em §9, passo 1 da jornada §5.5 ajustado e
      "Decisões de 2026-11-20" em §13 (`RF-09-73`, `RF-09-145`).
- [ ] 4.2 Documento 09 §1, "Já decididos": linha "Presentes da aula em Minhas turmas", com a
      decisão do fundador de 2026-11-20 (documento 03 §11).
- [ ] 4.3 `openspec/cronograma-de-fatias.md`: fatia 36 do PRD-09 `implementado` com o slug ao
      arquivar. `docs/prds/index.md`, documento 99 e `mkdocs.yml` não mudam.
