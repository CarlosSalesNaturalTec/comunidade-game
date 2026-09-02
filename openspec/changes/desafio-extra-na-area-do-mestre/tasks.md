## 1. Núcleo — modelo e migração

- [ ] 1.1 Acrescentar `parecer_do_mestre` (texto, nulo) a `DesafioExtra` em
      `backend/src/nucleo/desafios_extras/modelo.py`, com a revisão do Alembic que cria e
      derruba a coluna (design — decisão 1, Migration Plan). Verificar por
      `alembic upgrade head` e `alembic downgrade -1` no banco de teste.

## 2. Núcleo — regra

- [ ] 2.1 `propor_desafio_extra` passa a aceitar **Mestre** além de Apoiador e decide a situação
      de nascimento pelo proponente: Mestre autor da trilha nasce em `em_aprovacao_do_admin`,
      qualquer outro em `em_validacao_do_mestre`; papel que não seja um dos dois recebe 403
      (`RF-09-105`, `RF-09-107`, `RF-09-108`, `RF-09-109`, `RN-09-41`, design — decisão 4).
- [ ] 2.2 Exigir a justificativa do direcionado também do Mestre, no campo
      `justificativa_do_vinculo`, mantendo as guardas do nick (`RF-09-111`, design — decisão 5).
- [ ] 2.3 `validar_desafio_extra`: só o Mestre autor da trilha, sobre desafio em
      `em_validacao_do_mestre`; exige o parecer (422 sem ele), grava `mestre_validador_id` e
      leva a `em_aprovacao_do_admin`; 403 para qualquer outra persona e 409 para desafio em
      outra situação (`RF-09-51`, `RN-09-11`, design — decisões 2 e 3).
- [ ] 2.4 `recusar_desafio_extra_pelo_mestre`: mesmas guardas de posse e situação, exige o
      motivo (422 sem ele), grava em `motivo_da_recusa` e leva a `recusado`, sem gravar reserva
      (`RF-09-51`, `RF-09-52`, design — decisão 1).
- [ ] 2.5 `listar_desafios_a_validar_do_mestre`: os `em_validacao_do_mestre` das trilhas de que
      a persona é autora, nunca de trilha alheia nem em outra situação (`RF-09-51`, `RN-09-11`).

## 3. Núcleo — rotas e permissões

- [ ] 3.1 `POST /v1/desafios-extras/{id}/validacao` com `situacao` mais `parecer` ou `motivo`,
      guardada só por persona em sessão — a posse fica na regra (`RF-09-51`, `RF-09-52`,
      design — decisões 2 e 3).
- [ ] 3.2 `GET /v1/desafios-extras/a-validar`, restrita ao Mestre, devolvendo a fila sem
      identificar Guerreiro(a): do direcionado só o nick como o proponente o digitou
      (`RF-09-51`, `RN-09-11`, `RN-14-20`).
- [ ] 3.3 Ampliar `POST /v1/desafios-extras` ao Mestre — o papel Mestre ganha
      `propostas_de_desafio_extra` em escrita na matriz de `permissoes.py` — e
      `GET /v1/eu/desafios-extras` a qualquer proponente, filtrando por `proponente_id` em vez
      de recusar por papel (`RF-09-105`, design — decisão 6).

## 4. App 09 — área Desafios extras

- [ ] 4.1 `apps/app-09-mestre/src/desafiosExtras/api.ts` com as quatro chamadas — fila a
      validar, validação, proposta e os próprios desafios (`RF-09-51`, `RF-09-105`).
- [ ] 4.2 Tela da fila e do ato de validar: a lista do que há por validar com o que cada
      proposta oferece, o parecer exigido na validação e o motivo na recusa, dizendo que o
      validado segue ao Admin e o recusado não chega a ele; o tratado sai da lista
      (`RF-09-51`, `RF-09-52`).
- [ ] 4.3 Formulário da proposta do Mestre: trilha em andamento, recompensa, quantidade,
      critério, pontos extras com o teto de 10, formato, custeio, vigência e, no direcionado,
      nick e justificativa pedagógica; a tela anuncia a dispensa na trilha própria e a
      validação do autor na trilha alheia, sem sugerir dispensa do Admin (`RF-09-105` a
      `RF-09-108`, `RF-09-110`, `RF-09-111`, `RN-09-40`, `RN-09-41`).
- [ ] 4.4 Lista dos desafios que o Mestre propôs, com a situação, o motivo da recusa e a
      quantidade restante do publicado, sem identificar Guerreiro(a) (`RF-09-105`,
      `RF-09-112`, `RN-14-20`).
- [ ] 4.5 Ligar a área no `App.tsx`, no molde das demais.

## 5. Testes

- [ ] 5.1 `backend/tests/test_desafio_extra_regra.py`: proposta do Mestre autor nascendo em
      aprovação do Admin e a de outro Mestre em validação; papel sem direito recusado;
      direcionado do Mestre sem justificativa recusado e com nick inexistente aceito; validação
      com e sem parecer; recusa com e sem motivo; validação por quem não é o autor e sobre
      desafio em outra situação; a fila trazendo só as trilhas do próprio Mestre
      (`RF-09-51`, `RF-09-52`, `RF-09-105` a `RF-09-109`, `RF-09-111`, `RN-09-11`,
      `RN-09-40`, `RN-09-41`).
- [ ] 5.2 `backend/tests/test_desafio_extra_rota.py`: as rotas `/validacao` e `/a-validar` com
      403 para papel alheio; `POST /desafios-extras` aceitando Mestre e `GET /eu/desafios-extras`
      servindo cada proponente só o que propôs; e o critério de aceite do PRD-09 §12 — desafio
      recusado pelo Mestre não aparece na fila de aprovação do Admin (`RF-09-51`, `RF-09-52`,
      `RF-09-105`).
- [ ] 5.3 `apps/app-09-mestre/src/desafiosExtras/desafiosExtras.test.tsx`: a fila listando só o
      que há por validar, a validação exigindo parecer e a recusa exigindo motivo, o teto de 10
      recusado no formulário, a justificativa pedagógica exigida no direcionado, o aviso da
      dispensa na trilha própria e a lista do que o Mestre propôs com situação e motivo
      (`RF-09-51`, `RF-09-52`, `RF-09-105`, `RF-09-106`, `RF-09-108`, `RF-09-111`, `RN-09-40`).

## 6. Documentação

- [ ] 6.1 Marcar a fatia 15 do PRD-09 como implementada em
      `openspec/cronograma-de-fatias.md`, com o slug desta change e o recorte corrigido
      (`RF-09-105` a `RF-09-112` acrescidos, por decisão do fundador de 2026-09-02).
- [ ] 6.2 PRD-09 §9: as duas rotas novas — `POST /v1/desafios-extras` pelo Mestre e
      `GET /v1/desafios-extras/a-validar` —, com a §15 conferida; PRD-01 §4: o papel Mestre
      passa a listar propostas de desafio extra, como o documento 04 §3 já define; e
      `docs/09-topicos-em-aberto-e-sugestoes.md` §1: as decisões do fundador de 2026-09-02
      (o recorte da fatia e as duas rotas). Nenhum arquivo novo em `docs/`, logo nada muda na
      `nav` do `mkdocs.yml`; `docs/prds/index.md` só muda se a situação do PRD-09 mudar.
