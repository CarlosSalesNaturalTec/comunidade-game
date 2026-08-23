## 1. Regra — autoria estrita e substituição do conjunto

- [x] 1.1 Em `backend/src/nucleo/ods/regra.py`, trocar `conferir_posse_da_trilha` por
      `conferir_autoria_estrita_da_trilha` dentro de `criar_etiqueta_ods` (`RF-09-92`,
      `RF-09-98`, `RF-01-16`). Verificar: Admin que não é autor da trilha recebe
      `PermissaoNegada` ao etiquetar trilha e ao etiquetar missão.
- [x] 1.2 Em `backend/src/nucleo/ods/regra.py`, criar `substituir_etiquetas_da_trilha` e
      `substituir_etiquetas_da_missao`, que conferem a autoria e **validam todos** os
      objetivos recebidos antes de apagar as etiquetas do alvo e gravar as novas, na mesma
      transação (`RF-09-92`, `RF-09-98`, design — decisões 1 e 4). Verificar: lista com um
      objetivo inválido deixa o conjunto anterior intacto e não grava nada.
- [x] 1.3 Garantir na mesma função que a substituição é **escopada ao alvo** — a da trilha não
      alcança etiquetas de missão e vice-versa (`RF-01-45`). Verificar: substituir na trilha
      preserva a etiqueta própria de uma missão dela.

## 2. Porta HTTP

- [x] 2.1 Criar `backend/src/nucleo/ods/rotas.py` com `POST /trilhas/{id}/ods` e
      `POST /missoes/{id}/ods`, recebendo a lista completa de etiquetas — objetivo obrigatório
      e meta opcional — e devolvendo o conjunto resultante (`RF-09-92`, `RF-09-98`, PRD-09 §9,
      design — decisão 3). Verificar: as duas rotas respondem 200 e o corpo traz o conjunto
      gravado.
- [x] 2.2 Registrar o roteador em `backend/src/nucleo/principal.py` por
      `incluir_roteador_de_dados`. Verificar: as duas rotas aparecem em `/openapi.json` sob
      `/v1` e exigem chave de aplicação.
- [x] 2.3 Mapear as recusas para os códigos do PRD-09 §9 — 403 para quem não é o Mestre autor
      (outro Mestre ou Admin) e 422 para objetivo fora de 1 a 18 (`RF-09-92`, `RF-09-98`).
      Verificar: os dois códigos saem no formato de erro único do PRD-01.

## 3. Leitura das etiquetas e da cobertura

- [x] 3.1 Em `backend/src/nucleo/trilhas/rotas.py`, acrescentar as etiquetas declaradas a
      `TrilhaSaida`, `TrilhaComMissoesSaida` e `MissaoSaida`, com a etiqueta da missão sendo a
      **própria dela**, sem cair para a da trilha na saída (`RF-09-92`, `RF-09-98`).
      Verificar: `GET /trilhas/minhas` e `GET /trilhas/{id}` trazem as etiquetas de trilha e
      de cada missão.
- [x] 3.2 Acrescentar às mesmas saídas a **cobertura da trilha**, por `cobertura_por_trilha`,
      acompanhada de `configuracao.ciclo_rotulo` (`RF-09-94`, `RF-01-42`, `RN-01-24`, design —
      decisão 5). Verificar: a cobertura reúne trilha e missões sem repetir objetivo e vem com
      o rótulo do ciclo.

## 4. Testes do núcleo

- [x] 4.1 Em `backend/tests/test_ods.py`, inverter
      `test_admin_etiqueta_trilha_de_qualquer_mestre` para afirmar que o Admin é **recusado**,
      mantendo o cenário do outro Mestre recusado (`RF-09-92`, design — decisão 2). Verificar:
      o arquivo passa inteiro e nenhum outro chamador de `criar_etiqueta_ods` quebra.
- [x] 4.2 Criar os testes da substituição cobrindo os cenários da spec `etiqueta-ods` —
      conjunto substituído, lista vazia, idempotência, escopo por alvo nos dois sentidos,
      etiqueta inválida que recusa a operação inteira, e substituição que não reprocessa
      pontuação (`RF-09-92`, `RF-09-98`, `RF-09-93`, `RN-01-23`).
- [x] 4.3 Criar os testes de contrato das duas rotas — 200 com o conjunto resultante, 403 para
      outro Mestre e para Admin, 422 para objetivo fora da faixa (`RF-09-92`, `RF-09-98`).
- [x] 4.4 Criar os testes de leitura — etiquetas e cobertura em `GET /trilhas/minhas` e no
      `GET /trilhas/{id}` público, missão sem etiqueta própria saindo sem etiqueta, trilha sem
      etiqueta com cobertura vazia, e o rótulo do ciclo presente (`RF-09-92`, `RF-09-98`,
      `RF-09-94`).
- [x] 4.5 Travar a regressão do `RF-09-93`: trilha sem etiqueta ODS **publica** no Ciclo 01.
      Verificar: a publicação de trilha que atende às três travas e não tem etiqueta segue
      respondendo publicada.
- [x] 4.6 Travar o cenário vigente que a porta torna exercitável de ponta a ponta: substituir a
      etiqueta da missão **muda a etiqueta resolvida do desafio de coleta** dela, sem alterar o
      desafio (`RF-08-25`, `RN-08-21`).

## 5. App 09

- [x] 5.1 Em `apps/app-09-mestre/src/trilhas/api.ts`, expor as duas chamadas de substituição e
      passar a ler etiquetas e cobertura das saídas de trilha (`RF-09-92`, `RF-09-98`,
      `RF-09-94`). Verificar: os tipos refletem o contrato das rotas.
- [x] 5.2 Criar a tela de ODS da trilha, dentro de `TelaDaTrilha.tsx` — lista corrente
      carregada para edição, escolha do objetivo de 1 a 18, meta opcional em texto livre, e
      acrescentar, alterar e remover antes de confirmar em uma gravação só (`RF-09-92`,
      `RF-09-12`). Verificar: confirmar com a lista esvaziada deixa a trilha sem etiqueta.
- [x] 5.3 Criar a etiquetagem da missão pelo mesmo caminho, deixando claro que ela só é
      necessária quando a missão toca objetivo diferente do da trilha e que a missão sem
      etiqueta responde pela da trilha (`RF-09-98`, `RF-09-12`). Verificar: confirmar na missão
      não altera o que a trilha apresenta.
- [x] 5.4 Apresentar na trilha a **cobertura resultante**, atualizada após cada confirmação, e
      nunca por Guerreiro(a) (`RF-09-94`, `RN-01-24`). Verificar: acrescentar um objetivo novo
      passa a apresentá-lo na cobertura.
- [x] 5.5 Em `apps/app-09-mestre/src/trilhas/trilhas.test.tsx`, cobrir os cenários da spec
      `area-do-mestre` desta fatia — etiquetar com e sem meta, mais de um objetivo, remover um,
      remover todos, ação ausente em trilha alheia, e a cobertura acompanhando a confirmação.

## 6. Documentação

- [x] 6.1 Acrescentar a `docs/prds/index.md` o parágrafo da **terceira fatia do PRD-09**, que
      fecha o §6.1 e mantém o PRD-09 em **aprovado**, nomeando o que segue pendente. Não há
      decisão nova: a autoria estrita é o código alcançando o documento 11, já vigente — sem
      linha no documento 09, sem alteração de documento-fonte, sem mudança no documento 99 e
      sem arquivo novo em `docs/`, logo sem mexer na `nav` do `mkdocs.yml`.
