## 1. Documentos-fonte da decisão nova

- [x] 1.1 Em `docs/04-modelo-economico-e-sustentabilidade.md` §3, gravar na tabela de definições
      vigentes o que **encerra** um desafio extra: **ato de Admin na gestão**, que devolve ao
      ponto de apoio a recompensa ainda não entregue; a vigência declarada não encerra sozinha
      (decisão do fundador, 2026-09-02)
- [x] 1.2 Em `docs/09-topicos-em-aberto-e-sugestoes.md` §1, acrescentar a linha da decisão em
      "Já decididos", apontando o documento 04 §3 como fonte
- [x] 1.3 Em `docs/prds/prd-02-frontend-de-gestao.md`, acrescentar `RF-02-106` (o Admin encerra o
      desafio extra publicado, liberando a reserva da recompensa não entregue) na §6, as rotas
      `GET /v1/desafios-extras/publicados` e `POST /v1/desafios-extras/{id}/encerramento` na §9
      com os erros previstos (encerramento de desafio não publicado ou já encerrado, 409), o
      critério de aceite na §12 e a origem na §15

## 2. A reserva passa a servir aula ou desafio extra

- [x] 2.1 Em `backend/src/nucleo/reservas/modelo.py`, tornar `aula_id` opcional, acrescentar
      `desafio_extra_id` com FK para `desafio_extra`, o `CheckConstraint` que exige exatamente
      um dos dois e o índice de `desafio_extra_id` (`RF-07-39`, PRD-07 §8, design — decisão 2)
- [x] 2.2 Em `backend/src/nucleo/reservas/regra.py`, acrescentar `reservar_recompensa_do_desafio`
      — bloqueia o par, confere a natureza do tipo (422 no durável), confere a disponível e grava
      a `Reserva` do desafio — e `liberar_reservas_do_desafio`, que leva a `liberada` toda
      reserva ainda `reservada` daquele desafio (`RF-07-39`, `RF-07-40`, `RN-07-01`, `RN-07-07`,
      design — decisões 3, 4 e 5)
- [x] 2.3 Criar a migração Alembic que afrouxa `reserva.aula_id`, cria `reserva.desafio_extra_id`
      com a FK, o `CHECK` de exclusividade e o índice

## 3. Fila, aprovação, recusa e encerramento no núcleo

- [x] 3.1 Em `backend/src/nucleo/desafios_extras/modelo.py`, acrescentar `encerrado_em` e
      `admin_encerrador_id` ao `DesafioExtra`, e criar a migração Alembic das duas colunas
      (`RF-02-106`, `RF-07-40`, design — decisão 1)
- [x] 3.2 Em `backend/src/nucleo/desafios_extras/regra.py`, acrescentar
      `listar_desafios_em_aprovacao_do_admin` e `listar_desafios_publicados`, que devolvem só a
      situação de cada uma, da mais antiga para a mais recente (`RF-02-27`, `RN-02-10`)
- [x] 3.3 Em `backend/src/nucleo/desafios_extras/regra.py`, acrescentar `aprovar_desafio_extra`,
      na ordem de guardas situação → natureza → lastro → disponível: 409 fora de
      `em_aprovacao_do_admin`, 422 do durável, `conferir_publicacao_com_lastro` e a reserva pela
      `reservar_recompensa_do_desafio`; grava `admin_aprovador_id` e `publicado` no mesmo ato
      (`RF-02-28`, `RN-02-10`, `RN-02-11`, `RF-07-15`, `RF-07-39`, design — decisões 3 e 4)
- [x] 3.4 Em `backend/src/nucleo/desafios_extras/regra.py`, acrescentar `recusar_desafio_extra`,
      que exige o motivo (422 sem ele), recusa 409 fora de `em_aprovacao_do_admin` e não grava
      reserva alguma (`RF-02-28`, `RF-14-36`, `RN-14-13`)
- [x] 3.5 Em `backend/src/nucleo/desafios_extras/regra.py`, acrescentar `encerrar_desafio_extra`
      — 409 fora de `publicado` e 409 no já encerrado, grava quem encerrou e quando e chama
      `liberar_reservas_do_desafio` — e acrescentar a `registrar_conclusao_de_desafio_extra` a
      guarda que recusa conclusão de desafio encerrado (`RF-02-106`, `RF-07-40`, design —
      decisões 1 e 8)
- [x] 3.6 Em `backend/src/nucleo/desafios_extras/rotas.py`, acrescentar as quatro rotas sob
      `Operacao.tudo` — `GET /v1/desafios-extras/pendentes`, `POST
      /v1/desafios-extras/{id}/aprovacao` com entrada `{situacao, motivo}`, `GET
      /v1/desafios-extras/publicados` com a quantidade restante e `POST
      /v1/desafios-extras/{id}/encerramento` —, reusando `DesafioExtraSaida` acrescida do
      encerramento, sem identificar Guerreiro(a) algum, e verificar as quatro no OpenAPI
      (`RF-02-27`, `RF-02-28`, `RF-02-106`, `RF-14-39`, `RN-14-20`, design — decisão 6)

## 4. Testes do núcleo

- [x] 4.1 Em `backend/tests/test_desafio_extra_regra.py`, cobrir a aprovação e a recusa: desafio
      em validação do Mestre não aparece na fila e a aprovação dele dá 409; aprovação sem lastro
      dá 422 informando o que falta e o desafio segue na fila; aprovação com lastro publica e
      grava o aprovador; recusa sem motivo dá 422; recusa grava o motivo e não deixa reserva
      (`RF-02-27`, `RF-02-28`, `RN-02-10`, `RN-02-11`)
- [x] 4.2 Em `backend/tests/test_desafio_extra_regra.py`, cobrir a reserva e o encerramento: a
      publicação grava a reserva e reduz a disponível sem mexer no saldo derivado; recompensa que
      não cabe na disponível dá 422 sem gravar reserva e sem publicar; recompensa de tipo durável
      dá 422; o encerramento libera a reserva e devolve a disponível; encerrar fora de
      `publicado` ou duas vezes dá 409; vigência vencida sem encerramento mantém a reserva
      (`RF-07-39`, `RF-07-40`, `RN-07-01`, `RN-07-07`)
- [x] 4.3 Em `backend/tests/test_conclusao_de_desafio_extra.py`, acrescentar o cenário da
      conclusão recusada em desafio encerrado (`RF-07-40`, `RF-14-42`)
- [x] 4.4 Em `backend/tests/test_desafio_extra_rota.py`, cobrir as quatro rotas: a fila só traz
      `em_aprovacao_do_admin`; persona de outro papel recebe 403 nas quatro; a aprovação e o
      encerramento devolvem o desafio atualizado; nenhuma resposta traz dado de Guerreiro(a) além
      do nick digitado no direcionado (`RF-02-27`, `RF-02-28`, `RF-02-106`, `RF-14-39`,
      `RN-14-20`)

## 5. A natureza dos desafios extras na área Filas da App 03

- [x] 5.1 Em `apps/app-03-gestao/src/filas/api.ts`, acrescentar `listarDesafiosExtrasPendentes`,
      `listarDesafiosExtrasPublicados`, `avaliarDesafioExtra` e `encerrarDesafioExtra`, com os
      tipos do desafio (`RF-02-27`, `RF-02-28`, `RF-02-106`)
- [x] 5.2 Em `apps/app-03-gestao/src/filas/TelaDeFilas.tsx`, acrescentar a natureza "Desafios
      extras" ao filtro e a mensagem de fila vazia dela, sem abrir área nova e sem oferecê-la ao
      Mestre (`RF-02-27`, `RN-02-10`, design — decisão 7)
- [x] 5.3 Criar `apps/app-03-gestao/src/filas/AvaliacaoDoDesafioExtra.tsx` com o que a proposta
      oferece — trilha, missão, modalidade, recompensa, quantidade, ponto de apoio, critério,
      pontos extras, formato, custeio e vigência —, a aprovação oferecida só com lastro provido,
      o que falta prover no lugar dela, a recusa com motivo obrigatório apontado no próprio campo
      e o motivo devolvido pelo núcleo apresentado na tela (`RF-02-28`, `RN-02-11`, `RF-07-39`)
- [x] 5.4 Na mesma tela, acrescentar a lista dos publicados com a quantidade restante e a
      vigência, e o encerramento com o aviso prévio de que a recompensa não entregue volta ao
      ponto de apoio e o desafio deixa de receber conclusão, mostrando depois quem encerrou e
      quando, sem oferecer novo encerramento nem edição do publicado (`RF-02-106`, `RF-07-40`,
      `RF-14-38`)
- [x] 5.5 Em `apps/app-03-gestao/src/filas/filas.test.tsx`, cobrir a natureza nova: o filtro
      alcança os desafios extras; a fila vazia é informação, não falha; sem lastro a aprovação
      não é oferecida e o que falta aparece; recusa sem motivo é apontada sem chamar o núcleo; a
      recusa do núcleo por falta de disponível aparece na tela; o encerramento avisa antes e
      mostra quem encerrou depois; nenhuma tela traz nome, avatar ou contato de Guerreiro(a)
      (`RF-02-27`, `RF-02-28`, `RF-02-106`, `RF-14-39`, `RN-14-20`)

## 6. Documentação

- [x] 6.1 Marcar a fatia 15 do PRD-02 como implementada no
      `openspec/cronograma-de-fatias.md`, com o slug desta change no lugar do recorte previsto e
      sem a trava, que caiu; ajustar a nota do PRD-07 §14 e o parágrafo do documento 99 §8 que
      remetiam `RF-07-39` e `RF-07-40` a uma fatia do PRD-09 ou do PRD-14. `docs/prds/index.md`
      não muda: a situação do PRD-02 segue a mesma enquanto a fatia 16 estiver em aberto, e
      nenhum arquivo novo entrou em `docs/`, de modo que a `nav` do `mkdocs.yml` também não muda
