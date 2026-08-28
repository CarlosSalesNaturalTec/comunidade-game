## 1. Núcleo — anulação da presença

- [x] 1.1 Acrescentar a `Presenca`, em `backend/src/nucleo/aulas/modelo.py`, as colunas
      `anulada_em`, `anulada_por_id` (FK de `persona`) e `motivo_da_anulacao`, todas anuláveis, e
      trocar a `UniqueConstraint (aula_id, guerreiro_id)` por **índice único parcial** sobre as
      não anuladas (`postgresql_where=anulada_em IS NULL`), com a migração Alembic
      correspondente (`RF-02-36`, `RF-01-20`, design — decisão 4)
- [x] 1.2 Implementar `anular_presenca` em `backend/src/nucleo/aulas/regra.py`: exige motivo
      (422 sem ele), recusa a presença já anulada (409), restringe ao Admin (403 para os demais)
      e grava motivo, autor e momento sem alterar modo, confirmador nem momento do fato
      (`RF-02-36`, `RN-02-12`, design — decisão 5)
- [x] 1.3 Passar `registrar_presenca` a ignorar a presença anulada na idempotência, de modo que
      o par aula e Guerreiro(a) volte a aceitar o registro correto, e filtrar as anuladas em
      `painel_do_dia/regra.py` — presenças, aguardando aparelho e pendências (`RF-02-36`,
      `RF-01-20`, design — decisão 6)
- [x] 1.4 Expor `POST /v1/aulas/{id_da_aula}/presencas/{id_da_presenca}/anulacao` em
      `aulas/rotas.py`, com o corpo `motivo`, devolvendo a presença anulada e registrando a
      escrita na trilha de auditoria como as demais (`RF-02-36`, `RN-02-21`)

## 2. Núcleo — leitura dos lançamentos

- [x] 2.1 Implementar em `backend/src/nucleo/livro_razao/regra.py` a paginação dos lançamentos
      de um ponto de apoio, com filtro obrigatório de ponto de apoio, opcionais de período e de
      tipo de recurso, ordenação estável por data e cursor, e 403 para quem não é Admin
      (`RF-02-40`, `RF-01-18`, `RF-01-28`, design — decisão 3)
- [x] 2.2 Expor `GET /v1/lancamentos` em `livro_razao/rotas.py` pelo `contrato_de_listagem`,
      devolvendo natureza, tipo de recurso, quantidade, moedas, data e, no ajuste, o lançamento
      original e o motivo — sem abrir caminho de edição ou remoção (`RF-02-40`, `RF-07-19`,
      `RN-02-12`)

## 3. Testes do núcleo

- [x] 3.1 Em `backend/tests/test_presenca_do_mestre.py` (ou arquivo novo de presença, se couber
      melhor), cobrir a anulação: gravação com motivo, autor e momento; 422 sem motivo; 409 na
      já anulada; 403 para Mestre, Guerreiro(a) e responsável; registro correto aceito depois da
      anulação; anulada fora do painel do dia e fora do lançamento; e o reenvio do App 01 que
      não ressuscita a anulada (`RF-02-36`, `RN-02-12`)
- [x] 3.2 Em `backend/tests/test_lancamento_rota.py`, cobrir a listagem: lançamentos do ponto de
      apoio informado e só dele, 422 sem o filtro de ponto de apoio, filtros de período e de
      tipo de recurso, ajuste com original e motivo na saída, paginação por cursor e 403 para
      quem não é Admin (`RF-02-40`, `RF-01-18`, `RF-01-28`)

## 4. App 03 — porta de API dos lançamentos

- [x] 4.1 Criar `apps/app-03-gestao/src/lancamentos/api.ts` com as chamadas da área: lançar a
      atividade realizada da aula com a lista de participantes e o desfecho de cada um, confirmar
      presença, anular presença com motivo e registrar a ocorrência de conduta — reusando
      `obterPainelDoDia` para a aula vigente, sem duplicar a leitura (`RF-02-34`, `RF-02-36`,
      `RF-02-37`, `RF-02-39`, design — decisão 1)
- [x] 4.2 Acrescentar a `apps/app-03-gestao/src/pontos-de-apoio/api.ts` a listagem de lançamentos
      do ponto de apoio, com período e tipo de recurso, e o lançamento de ajuste com quantidade,
      moedas e motivo (`RF-02-40`)

## 5. App 03 — área Lançamentos

- [x] 5.1 Criar `TelaDeLancamentos.tsx` com a área ancorada na aula vigente do painel do dia,
      registrada em `App.tsx` como área nova, dizendo em uma frase que não há encontro em
      andamento quando for o caso, e alcançável pela pendência de lançamento listada no painel
      (`RF-02-34`, `RF-02-46`, `RF-02-47`, design — decisões 1 e 2)
- [x] 5.2 Criar `LancamentoDaAtividade.tsx`: lista dos participantes com o desfecho de cada um
      entre os três valores fechados — incluindo o mérito extra por auxílio —, momento do fato e
      produção, envio em ato único por aula, bloqueio do envio com participante sem desfecho,
      sem campo de valor de pontuação, e a confirmação de que a aula passou a realizada e as
      reservas viraram baixa (`RF-02-34`, `RF-02-39`)
- [x] 5.3 Criar `ConferenciaDePresencas.tsx`: presenças da aula com modo e confirmador, avatar e
      nick e nenhuma imagem real, confirmação da presença que faltou, anulação com motivo
      obrigatório, presença anulada visível e marcada, e registro da presença correta em seguida
      (`RF-02-36`, `RN-02-12`, `RN-02-22`)
- [x] 5.4 Criar `RegistroDeInfracao.tsx`: encontro, atividade, Guerreiro(a) e motivo em texto
      livre, sem campo de valor e sem item de catálogo, aviso de que descuido acidental com
      material comum não é infração, efetivação no ato e recusas do núcleo — teto da aula,
      atividade fora da aula, trilha alheia — ditas em uma frase (`RF-02-37`, `RN-02-13`,
      `RN-02-14`)
- [x] 5.5 Restringir a área ao papel: o Mestre vê apenas o registro da infração, e nem o
      lançamento da atividade realizada nem a conferência de presenças (`RF-02-49`, `RN-02-20`,
      design — decisão 7)

## 6. App 03 — extrato e ajuste em Pontos de Apoio

- [x] 6.1 Criar `ExtratoDoPontoDeApoio.tsx` na área Pontos de Apoio, ao lado dos saldos e da
      transferência: lançamentos com natureza, tipo de recurso, quantidade, moedas e data,
      filtro por período e por tipo de recurso, e o ajuste apresentado referenciando o original
      (`RF-02-40`, design — decisão 8)
- [x] 6.2 Criar `AjusteDeLancamento.tsx` com quantidade, moedas e motivo obrigatório, sem
      caminho de edição nem de remoção, atualizando o extrato depois de gravado (`RF-02-40`,
      `RN-02-12`)

## 7. Testes da App 03

- [x] 7.1 Criar `apps/app-03-gestao/src/lancamentos/lancamentos.test.tsx` cobrindo os cenários da
      área: abertura sobre a aula vigente e a frase sem encontro; desfecho por participante,
      mérito extra por auxílio, bloqueio sem desfecho e ausência de campo de valor; confirmação,
      anulação com motivo e registro correto em seguida; infração no ato, aviso da `RN-02-14`,
      motivo obrigatório e teto da aula em uma frase; e o Mestre com acesso apenas à infração
      (`RF-02-34`, `RF-02-36`, `RF-02-37`, `RF-02-39`, `RF-02-49`, `RN-02-13`, `RN-02-14`,
      `RN-02-20`, `RN-02-22`)
- [x] 7.2 Em `apps/app-03-gestao/src/pontos-de-apoio/pontos-de-apoio.test.tsx`, cobrir o extrato
      e o ajuste: listagem com filtros, ajuste gravado referenciando o original, ausência de
      caminho de edição ou remoção e motivo obrigatório (`RF-02-40`, `RN-02-12`)

## 8. Documentação

- [x] 8.1 Gravar as três decisões novas em `docs/09-topicos-em-aberto-e-sugestoes.md` §1, em "Já
      decididos" — a leitura dos lançamentos, a anulação da presença e a infração registrada pelo
      Mestre na App 03 — e refletir as duas de produto em `docs/03-arquitetura-e-tecnologia.md`
      §5, no "Registro de presença" e no "Lançamento de pontuação negativa"
- [x] 8.2 Atualizar `docs/prds/prd-02-frontend-de-gestao.md`: a §4 e a `RN-02-20` com a infração
      pelo Mestre, o `RF-02-49` com a exceção, a §8 trocando "é `Resultado` de valor negativo"
      pela `OcorrenciaDeConduta` que o núcleo gravou, e a §9 com
      `POST /v1/ocorrencias-de-conduta`, a anulação da presença e `GET /v1/lancamentos`; e
      `docs/prds/prd-07-economia-e-ledger.md` §9 com a linha da listagem
- [x] 8.3 Marcar a fatia 10 como implementada em `openspec/cronograma-de-fatias.md`, trocando o
      recorte pelo slug da change. `docs/prds/index.md` não muda — o PRD-02 segue em
      implementação —, nenhum arquivo novo entra em `docs/` e a `nav` do `mkdocs.yml` fica como
      está
