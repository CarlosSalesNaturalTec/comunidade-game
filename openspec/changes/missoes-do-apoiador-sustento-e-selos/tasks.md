## 1. Núcleo — entidades e migração

- [x] 1.1 Criar `backend/src/nucleo/missoes_do_apoiador/modelo.py` com `MissaoDoApoiador` — par
      `aula_id` + `tipo_de_recurso_id` da necessidade de origem, `nivel_de_necessidade`,
      título, o que se pede, quantidade, prazo, selo e família do selo, `situacao` e Admin que
      publicou — e a enum dos quatro níveis (`RF-14-71`, `RN-14-31`, `RF-02-102`, design —
      Decisions 1, 4, 8). Verifica-se importando o modelo no `modelos.py` sem erro de mapeamento.
- [x] 1.2 Criar `backend/src/nucleo/selos_do_apoiador/modelo.py` com `SeloDoApoiador` —
      Apoiador, família, selo, missão de origem e data —, somente inserção, com índice único
      por (Apoiador, missão, selo) (`RF-14-66`, `RN-14-36`, design — Decisions 6).
- [x] 1.3 Acrescentar `missao` a `OrigemDaEscolhaDoAporte` e a coluna
      `missao_do_apoiador_id` em `AporteDeclarado` (`RF-14-63`, `RF-14-25`, design — Migration).
- [x] 1.4 Gerar a migração Alembic com as duas tabelas e a coluna nova, e verificar que
      `alembic upgrade head` e `downgrade` correm limpos no banco de teste.

## 2. Núcleo — regra da missão

- [x] 2.1 `missoes_do_apoiador/regra.py`: `publicar_missao()` — só Admin, conferindo o par
      contra as necessidades derivadas e recusando com 422 sem necessidade por trás
      (`RF-02-102`, `RF-02-103`, `RN-02-31`, `RN-14-31`, design — Decisions 1).
- [x] 2.2 `despublicar_missao()` — só Admin, 409 na missão já concluída, sem estorno de aporte
      homologado (`RF-02-105`, `RN-14-34`).
- [x] 2.3 `derivar_missoes()` — o coberto e o quanto falta a partir dos aportes homologados que
      vieram pela missão, o filtro de abertas (situação, prazo e necessidade ainda existente) e
      o agrupamento por nível (`RF-14-60` a `RF-14-62`, `RF-14-64`, `RF-14-71`, `RF-14-72`,
      `RF-02-104`, design — Decisions 2, 3, 4).
- [x] 2.4 `concluir_se_fechou()` — chamada de `registrar_aporte()` na homologação de declaração
      com origem `missao`: recalcula, grava `concluida` e insere o selo de cada participante,
      mais o de mutirão quando houver mais de um, na mesma transação (`RF-14-65`, `RF-14-66`,
      `RN-14-32`, `RN-14-33`, `RN-14-34`, design — Decisions 5, 8).
- [x] 2.5 Estender `declarar_aporte()` com a origem `missao`, recusando com 409 a missão
      concluída, vencida ou inexistente, e mantendo a declaração pendente sem abater nada
      (`RF-14-63`, `RF-14-64`, `RN-14-07`, `RN-14-32`).

## 3. Núcleo — sustento e selos

- [x] 3.1 `selos_do_apoiador/regra.py`: `derivar_sustento()` — nível 1 pelo primeiro aporte
      homologado e níveis 2 a 4 pelos níveis de necessidade das missões concluídas, com a
      frente que falta; a escada para no nível 4 (`RF-14-67`, `RF-14-69`, `RN-14-35`,
      `RN-14-36`, design — Decisions 7).
- [x] 3.2 `listar_selos()` agrupando por família, somente leitura do próprio Apoiador
      (`RF-14-68`, `RF-14-70`, `RN-14-38`).

## 4. Núcleo — rotas

- [x] 4.1 `missoes_do_apoiador/rotas.py`: `POST /v1/missoes-do-apoiador`,
      `GET /v1/missoes-do-apoiador` — pública nas abertas, com filtro de situação e coberto para
      Admin — e `POST /v1/missoes-do-apoiador/{id}/despublicacao` (`RF-14-60` a `RF-14-62`,
      `RF-02-102`, `RF-02-104`, `RF-02-105`, design — Decisions 9).
- [x] 4.2 `GET /v1/eu/apoiador/sustento`, do Apoiador em sessão, com 403 para o sustento de
      outro (`RF-14-67`, `RF-14-68`).
- [x] 4.3 Registrar os roteadores em `principal.py` e verificar que os caminhos novos aparecem
      no OpenAPI servido fora do `/v1`.

## 5. Testes do núcleo

- [x] 5.1 `tests/test_missao_do_apoiador.py`: publicação com e sem necessidade por trás,
      despublicação sem estorno e recusada na concluída, agrupamento por nível, coberto sem
      identificar quem cobriu, missão vencida fora da lista (`RF-14-60` a `RF-14-62`,
      `RF-14-71`, `RF-14-72`, `RF-02-102` a `RF-02-105`).
- [x] 5.2 `tests/test_missao_do_apoiador_cobertura.py`: declaração pendente não abate,
      homologação parcial abate e não credita selo, homologação que fecha conclui e credita, as
      duas pessoas com as próprias moedas e o selo de mutirão, missão fechada recusando aporte
      com 409 (`RF-14-63` a `RF-14-66`, `RN-14-32`, `RN-14-34`).
- [x] 5.3 `tests/test_sustento_do_apoiador.py`: nível 1 pelo primeiro aporte, frentes diferentes
      valendo mais que volume, escada parando no nível 4, nível que não regride, selos por
      família, 403 no sustento alheio (`RF-14-67` a `RF-14-70`, `RN-14-35`, `RN-14-36`).
- [x] 5.4 `tests/test_missao_do_apoiador_rota.py`: as quatro rotas, com chave de aplicação,
      persona errada em 403 e a leitura pública sem sessão (`RF-14-60`, `RF-02-102`,
      `RF-02-104`, `RF-02-105`).

## 6. App 08 — Área do Apoiador

- [x] 6.1 `src/missoes/TelaDeMissoes.tsx` e `api.ts`: missões abertas agrupadas por nível, com o
      que se pede, o que falta em moedas, prazo, selo e o coberto em quantidade, sem identificar
      quem cobriu (`RF-14-60` a `RF-14-62`, `RF-14-72`).
- [x] 6.2 `src/missoes/DeclaracaoPorMissao.tsx`: cobrir a missão inteira ou parte, com
      comprovante, declarando que o aporte entra pendente e não abate nem conclui (`RF-14-63`,
      `RF-14-64`, `RN-14-32`).
- [x] 6.3 `src/sustento/TelaDeSustento.tsx`: nível alcançado, selos por família e a frente que
      falta, dita uma vez e sem repetição nas demais telas (`RF-14-67` a `RF-14-70`,
      `RF-14-73`).
- [x] 6.4 Acrescentar a opção "missão aberta" à porta pública de pré-cadastro e ao caminho de
      declaração do Apoiador em sessão (`RF-14-02`, `RF-14-25`).
- [x] 6.5 Testes Vitest de `missoes` e `sustento`: agrupamento e coberto anônimo, aviso do
      pendente, cobertura parcial mostrando o restante sem selo, selo novo e nível na conclusão,
      nenhuma tela ordenando por valor (`RF-14-61`, `RF-14-64`, `RF-14-66`, `RF-14-70`).

## 7. App 03 — Gestão

- [x] 7.1 `src/missoes-do-apoiador/PublicacaoDeMissao.tsx` e `ListaDeMissoes.tsx`, na área
      Recursos: publicar a partir de uma necessidade em aberto, listar em qualquer situação com
      coberto, falta e situação, e despublicar declarando que nada é estornado (`RF-02-102` a
      `RF-02-105`).
- [x] 7.2 Testes Vitest: publicação recusada por faltar necessidade apresentada em linguagem
      simples, despublicação da concluída recusada, lista sem nick de quem cobriu, caminho
      ausente para quem não é Admin (`RF-02-103`, `RF-02-105`, `RN-02-31`).

## 8. Documentação

- [x] 8.1 Marcar a fatia 5 do PRD-14 como implementada no `openspec/cronograma-de-fatias.md`.
      As demais mudanças de documentação já foram feitas nesta change, antes dos artefatos:
      documento 14 §§5 e 11 e documento 09 (quem publica a missão e a pendência do nível 5),
      PRD-02 (§§3.1, 6.5, 7, 8, 9, 13, 15), PRD-14 (§§9, 14) e documento 99 §8. `docs/prds/index.md`
      não muda: o PRD-14 segue em implementação, e nenhum arquivo novo entrou em `docs/`.
