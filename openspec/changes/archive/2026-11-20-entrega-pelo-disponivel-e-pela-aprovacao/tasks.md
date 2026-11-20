# Tasks

## 1. Núcleo

- [x] 1.1 `aulas/regra.py`: `aula_de_referencia_da_comunidade` — a aula de início mais recente
      até o momento, não cancelada (`RF-09-76`, `RF-07-13`).
- [x] 1.2 `recompensas_de_marco/regra.py`: `_validar_entrega` confere o disponível;
      `registrar_entrega` sem `ponto_de_apoio`, derivando-o da aula declarada ou da aula de
      referência, com 422 sem vínculo ou sem aula; `entregar_na_aprovacao` com `SAVEPOINT` por
      recompensa (`RF-07-13`, `RN-07-01`, `RN-07-42`, `RF-09-146`, `RN-09-63`, `RN-07-44`).
- [x] 1.3 `recompensas_de_marco/rotas.py`: a entrada da entrega recusa `ponto_de_apoio_id` e
      aceita `aula_id` opcional (`RF-09-76`).
- [x] 1.4 `trilhas/rotas.py`: o julgamento lê o percurso antes, chama `entregar_na_aprovacao`
      no "cumpriu" e devolve `recompensas_entregues` (`RF-09-146`).

## 2. Núcleo — testes

- [x] 2.1 `tests/test_entrega_pelo_disponivel_e_pela_aprovacao.py`: reservado não lastreia;
      ponto da aula anterior; ponto declarado recusado; comunidade sem aula recusada; aprovação
      que entrega; aprovação sem lastro; julgador sem vínculo (`RF-07-13`, `RN-07-42`,
      `RF-09-76`, `RF-09-146`, `RN-09-63`).
- [x] 2.2 Ajuste dos testes de entrega que escolhiam o ponto de apoio (`RF-09-76`).

## 3. App 09

- [x] 3.1 `recompensas/FilaDeEntregasPendentes.tsx` e `recompensas/api.ts`: sem seletor de ponto
      de apoio, com teste (`RF-09-76`).
- [x] 3.2 `turmas/TelaDeDesbloqueiosPendentes.tsx` e a API do julgamento: aviso da recompensa
      entregue, com teste (`RF-09-146`).

## 4. Documentação

- [x] 4.1 Fatia 13 do PRD-07 como implementada em `openspec/cronograma-de-fatias.md`, com o slug.
      No documento 09, a linha "Consumo do encontro e recompensa de marco" recebe que a aula
      imediatamente anterior é a de início mais recente até o momento, não cancelada, e que
      comunidade sem aula anterior não recebe entrega. Os PRDs não mudam.
