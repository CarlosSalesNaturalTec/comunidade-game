## 1. Núcleo — a declaração e o seu desfecho

- [x] 1.1 Criar `AporteDeclarado` em `backend/src/nucleo/aportes/modelo.py` — provedor, valor
      declarado da transferência, modalidade (`necessidade`, `valor_sugerido`, `valor_livre`),
      par aula + tipo de recurso da necessidade escolhida, comprovante, situação (`pendente`,
      `homologada`, `recusada`), motivo da recusa, Admin que a resolveu e data —, acrescentar
      `app_08` a `OrigemDoRegistro` e `aporte_declarado_id` único e anulável a `Aporte`
      (`RF-14-25` a `RF-14-27`, `RN-14-07`, design — decisões 1 a 3). Verificar pela migração
      Alembic aplicando e revertendo sem perda (tarefa 1.2).
- [x] 1.2 Escrever a migração Alembic da tabela, da coluna e do valor novo do enum, com
      `downgrade` que derruba as duas adições (design — Migration Plan). Verificar com `alembic
      upgrade head` e `alembic downgrade -1` no banco de teste.
- [x] 1.3 Implementar em `backend/src/nucleo/aportes/regra.py` a declaração do Apoiador: exige
      comprovante em PDF, JPG ou PNG pela porta de armazenamento já usada, recusa forma que não
      seja dinheiro com a orientação de procurar a gestão, e grava a declaração pendente sem
      gerar lançamento (`RF-14-25`, `RF-14-26`, `RF-14-28`, `RN-14-05` a `RN-14-07`, design —
      decisão 7). Verificar pelos testes da tarefa 4.1.
- [x] 1.4 Implementar a resolução da declaração: `registrar_aporte` passa a aceitar a
      declaração de origem, grava o aporte com `origem_do_registro = app_08`, marca a
      declaração como homologada e recusa com 422 a segunda tentativa sobre a mesma; e nasce a
      recusa por Admin, com motivo obrigatório, 409 sobre declaração já resolvida e sem
      lançamento algum (`RF-14-26`, `RF-14-27`, `RN-14-07`, `RN-14-08`, design — decisões 2 e
      5). Verificar pelos testes da tarefa 4.2.
- [x] 1.5 Publicar as rotas em `backend/src/nucleo/aportes/rotas.py` e registrá-las em
      `principal.py`: `POST /v1/aportes/declarados` e `GET /v1/eu/aportes/declarados` para o
      Apoiador em sessão, `POST /v1/aportes/declarados/{id}/recusa` para Admin, e
      `aporte_declarado_id` no `POST /v1/aportes` já existente (`RF-14-25` a `RF-14-27`, PRD-14
      §9). Verificar pelos testes de rota da tarefa 4.3.

## 2. Núcleo — as leituras que a App 08 precisa

- [x] 2.1 Acrescentar o nome do tipo de recurso, da comunidade e do ponto de apoio à saída de
      `GET /v1/vitrine/necessidades` e `GET /v1/necessidades/minhas`, ao lado dos
      identificadores já publicados (`RF-14-24`, `RF-07-27`, design — decisão 6). Verificar
      pelos testes da tarefa 4.4.
- [x] 2.2 Acrescentar o nome do tipo de recurso e o destino à saída de `GET /v1/meus-aportes`,
      mantendo o Poder Sustentador em moedas e o valor de origem em reais fora da resposta
      (`RF-14-21`, `RF-14-22`, `RF-14-23`, `RN-14-09`). Verificar pelos testes da tarefa 4.4.

## 3. App 08 — as telas do aporte

- [x] 3.1 Mover a escada de valores sugeridos de `src/preCadastro/escada.ts` para um módulo
      compartilhado da aplicação e apontar a porta pública para ele, sem mudar valor nem escala
      (`RF-14-25`, design — decisão 4). Verificar que os testes do pré-cadastro seguem verdes.
- [x] 3.2 Criar `src/aportes/api.ts` com as chamadas de "Meus aportes", necessidades em aberto,
      declaração e situação das declarações (`RF-14-21`, `RF-14-24`, `RF-14-25`, `RF-14-27`).
- [x] 3.3 Criar a tela "Meus aportes": os aportes homologados com data, tipo e destino, o Poder
      Sustentador como total acumulado em moedas e o vazio explicado (`RF-14-21`, `RF-14-22`).
      Verificar pelos testes da tarefa 4.5.
- [x] 3.4 Criar a tela das necessidades em aberto: atividade, comunidade e o que falta em
      moedas, sem somar nem reordenar, com a necessidade sem valor de referência ainda na lista
      e o vazio explicado (`RF-14-24`, `RN-14-09`). Verificar pelos testes da tarefa 4.5.
- [x] 3.5 Criar a tela da declaração do aporte: os três caminhos — necessidade, valor sugerido
      pela escada do perfil escolhido na tela e valor livre com fração de duas casas —, o
      equivalente em moedas ao lado do valor em reais, o comprovante obrigatório com os
      formatos aceitos, a declaração de que o aporte entra pendente e não credita nada, e a
      orientação de procurar a gestão para material, serviço ou divulgação (`RF-14-23`,
      `RF-14-25`, `RF-14-26`, `RF-14-28`, `RN-14-05` a `RN-14-07`, `RN-14-09`). Verificar pelos
      testes da tarefa 4.6.
- [x] 3.6 Criar a tela da situação das declarações — pendente, homologado ou recusado com
      motivo em linguagem simples, com o valor em moedas e sem nenhum ato sobre a situação — e
      ligar as quatro telas novas à navegação de `App.tsx` (`RF-14-23`, `RF-14-27`). Verificar
      pelos testes da tarefa 4.6.

## 4. Testes

- [x] 4.1 `backend/tests/test_aporte_declarado.py` — a declaração nasce pendente e não gera
      lançamento nem move o Poder Sustentador; a declaração por necessidade não abate o que
      falta; sem comprovante ou em formato não aceito responde 422 com os formatos; material,
      serviço ou divulgação responde 422 com a orientação de procurar a gestão (`RF-14-25`,
      `RF-14-26`, `RF-14-28`, `RN-14-05` a `RN-14-07`).
- [x] 4.2 No mesmo arquivo, o desfecho: a homologação grava o aporte com origem "App 08",
      converte pela vigência da data e credita; a segunda homologação da mesma declaração é
      422; o provedor homologando a própria é 403; a recusa grava o motivo sem creditar, a
      declaração já resolvida é 409 e a recusa sem motivo é 422 (`RF-14-26`, `RF-14-27`,
      `RN-14-07`, `RN-14-08`).
- [x] 4.3 `backend/tests/test_aporte_declarado_rota.py` — as rotas do Apoiador alcançam só as
      declarações dele, exigem a credencial da persona e a recusa é restrita a Admin
      (`RF-14-25`, `RF-14-27`, `RN-14-08`).
- [x] 4.4 Estender `backend/tests/test_necessidade_rota.py` e o teste de "Meus aportes" com os
      nomes na saída, o valor em moedas e a ausência de reais e de dado de pessoa (`RF-14-21` a
      `RF-14-24`, `RN-14-09`).
- [x] 4.5 `apps/app-08-apoiador/src/aportes/meusAportes.test.tsx` — "Meus aportes" com total e
      vazio explicado; necessidades com atividade, comunidade, moedas, a sem valor de
      referência e o vazio (`RF-14-21`, `RF-14-22`, `RF-14-24`).
- [x] 4.6 `apps/app-08-apoiador/src/aportes/declaracao.test.tsx` — os três caminhos da
      declaração, o equivalente em moedas, a recusa por falta de comprovante, a orientação
      sobre material e serviço, a declaração de que entra pendente, e a situação com as três
      marcas e o motivo da recusa (`RF-14-23`, `RF-14-25` a `RF-14-28`).

## 5. Documentação

- [x] 5.1 Gravar a decisão nova do fundador de 2026-09-01 — o Admin recusa com motivo a
      declaração de aporte vinda da App 08, e a rota nasce no núcleo antes da tela da gestão —
      no documento 04 §2, que hoje diz que a homologação vale para o registro da gestão e para
      o do pré-cadastro, e na tabela "Já decididos" do documento 09 §1, com os identificadores
      `RF-14-27`, `RN-14-07` e `RN-14-08`.
- [x] 5.2 Marcar a fatia 4 do PRD-14 como implementada em `openspec/cronograma-de-fatias.md`,
      com o slug desta change, e anotar na fatia 16 do PRD-02 que a tela da gestão para a fila
      das declarações entra com ela — o requisito daquela tela é do fundador, não desta change.
      Nada muda em `docs/prds/index.md` (a situação do PRD-14 não muda), no documento 99 nem na
      `nav` do `mkdocs.yml`: nenhum arquivo nasce em `docs/`.
