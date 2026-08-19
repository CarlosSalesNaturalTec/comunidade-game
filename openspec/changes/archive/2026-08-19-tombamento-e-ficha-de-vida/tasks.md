## 1. Modelo e migração

- [x] 1.1 Criar `backend/src/nucleo/patrimonio/modelo.py` com `ItemPatrimonial` — aporte de
      origem opcional, título, número de tombo, ponto de apoio, estado de conservação corrente —
      e `AnotacaoDaFichaDeVida` — item, teor (cuidado, perda ou dano), estado de conservação
      apurado —, ambos com `ComAutoria` (`RF-07-11`, `RF-07-48`, design — Decisions 2, 3).
- [x] 1.2 Migração Alembic das duas tabelas, com `UNIQUE (ponto_de_apoio_id,
      numero_de_tombo)`, índice por ponto de apoio e a trava de **somente inserção** da
      `anotacao_da_ficha_de_vida`, nos mesmos moldes da de `acesso_ao_template` e `auditoria`
      (`RF-07-11`, design — Decisions 2, 5, Migration Plan).

## 2. Regras do patrimônio

- [x] 2.1 `patrimonio/regra.py`: `tombar_item` — exige Admin, valida título, tombo, ponto de
      apoio e estado de conservação, recusa aporte de origem de natureza não durável e recusa
      tombo repetido no mesmo ponto de apoio (`RF-07-11`, `RN-07-07`).
- [x] 2.2 Conferência do **teto do aporte** dentro de `tombar_item`, com `SELECT ... FOR UPDATE`
      sobre o aporte à imagem de `_bloquear_par`; item sem aporte de origem não conta e não tem
      teto (`RN-07-07`, `RN-07-01`, design — Decisions 6).
- [x] 2.3 `anotar_ficha_de_vida` — exige Admin ou Mestre, grava a anotação e reescreve o estado
      de conservação corrente do item. Não recebe Guerreiro(a), não chama `livro_razao` nem
      `ponto_extra` (`RF-07-48`, `RN-07-09`, design — Decisions 3, 7).
- [x] 2.4 `listar_acervo` — itens com responsável **derivado** por junção com
      `PontoDeApoio.responsavel_id` e a ficha de vida em ordem cronológica, filtrados por
      comunidade; Admin lê todas, Mestre só as vinculadas (`RF-07-11`, `RN-07-10`, `RF-01-16`,
      design — Decisions 4).

## 3. As duas recusas da natureza durável

- [x] 3.1 `aulas/regra.py`: recusar com 422 o recurso declarado de tipo de natureza durável, no
      laço de validação que já existe, **antes** de a `Aula` ser criada — de modo que a aula não
      nasça pendente de lastro nem publique necessidade (`RN-07-07`, `RF-07-08`, design —
      Decisions 1).
- [x] 3.2 `catalogo_avulso/regra.py`: recusar com 422 em `cadastrar_item` o item cujo tipo é de
      natureza durável, preservando intacta a regra do item sem lastro, que segue aceito e
      inativo (`RF-07-34`, `RN-07-07`, `RN-07-26`).

## 4. Rotas

- [x] 4.1 `patrimonio/rotas.py` com `POST /v1/itens-patrimoniais` (Admin),
      `GET /v1/itens-patrimoniais` (gestão, filtrada por comunidade) e
      `POST /v1/itens-patrimoniais/{id}/ficha-de-vida` (Admin ou Mestre), registradas em
      `principal.py`. Nenhuma saída traz valor em reais (`RF-07-11`, `RF-07-48`, `RN-07-05`,
      design — Decisions 8).

## 5. Testes

- [x] 5.1 `tests/test_patrimonio_tombamento.py`: tombamento por Admin com e sem aporte de
      origem, 403 do Mestre, 422 do aporte de natureza não durável, tombo repetido no mesmo
      ponto de apoio recusado e mesmo tombo aceito em pontos de apoio diferentes; teto do aporte
      no limite e além dele (`RF-07-11`, `RN-07-07`).
- [x] 5.2 `tests/test_patrimonio_ficha_de_vida.py`: anotação gravada com autoria, 403 do
      Guerreiro(a), ficha lida na ordem do tempo, `UPDATE` e `DELETE` recusados também fora do
      ORM, e o critério de aceite do PRD-07 §12 — **exemplar dado como perdido não gera débito
      algum**: nenhum `Lancamento` novo, nenhum `PontoExtra` alterado, nenhuma cobrança, e a
      anotação de dano aceita sem identificar culpado (`RF-07-48`, `RN-07-09`).
- [x] 5.3 `tests/test_patrimonio_rota.py`: leitura do acervo por Admin e por Mestre vinculado,
      403 do Apoiador, responsável derivado presente na resposta, troca do responsável do ponto
      de apoio refletida em todos os exemplares sem escrita neles, e nenhum campo em reais
      (`RF-07-11`, `RN-07-10`, `RN-07-05`).
- [x] 5.4 `tests/test_saldo_duravel_inerte.py`: aporte durável credita Poder Sustentador;
      agendamento que declara tipo durável responde 422 mesmo com saldo de sobra e **não** deixa
      aula pendente de lastro nem necessidade publicada; cadastro de item de catálogo de tipo
      durável responde 422 enquanto o item consumível sem lastro segue aceito e inativo
      (`RN-07-07`, `RF-07-08`, `RF-07-34`, `RN-07-26`).

## 6. Documentação

- [x] 6.1 Gravar as quatro decisões novas no documento-fonte de cada uma — documento 04 §1
      (saldo durável inerte), documento 05 §3 (tombo digitado e único por ponto de apoio;
      responsável do exemplar derivado do ponto de apoio) e documento 02 §8.2 (ressalva da
      recusa por natureza na frase "nunca é recusado") — e em "Já decididos" do documento 09.
- [x] 6.2 Aplicar as decisões ao PRD-07: §8 (atributos do `ItemPatrimonial`, sem responsável
      próprio; saldo durável), §9 (as três rotas de patrimônio) e §13 (tabela de decisões).
      Atualizar `docs/prds/index.md` com a nona fatia. O documento 99 só muda se alguma relação
      entre documentos mudar; nenhum arquivo novo em `docs/`, logo a `nav` do `mkdocs.yml` fica
      como está.
