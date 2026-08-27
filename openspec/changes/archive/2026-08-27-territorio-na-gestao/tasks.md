## 1. Núcleo — o vínculo na listagem de Guerreiros e Guerreiras

- [x] 1.1 Acrescentar à saída de `GET /v1/guerreiros` a **comunidade do vínculo vigente** e a
      **data de início** dele, pelo relacionamento `Persona.vinculo_vigente` já mapeado, com os
      dois campos vazios quando não há vínculo vigente e sem devolver vínculo encerrado; nenhuma
      coluna nova e nenhuma migração (`RF-02-15`, `RF-08-02`)
- [x] 1.2 Conferir que a rota continua restrita a Admin e que nenhuma escrita nasceu deste
      caminho — o núcleo segue sem rota que mova o Guerreiro(a) de comunidade (`RN-02-06`,
      `RF-08-03`)

## 2. Núcleo — leitura dos desafios de coleta publicados

- [x] 2.1 Implementar em `backend/src/nucleo/coletas/regra.py` a consulta de Admin dos desafios
      cuja missão pertence a trilha em situação `publicada`, alcançada por
      `desafio.missao_id → missao.trilha_id`, paginada e sem filtro de comunidade, recusando com
      403 qualquer papel que não seja Admin (`RF-02-17`, `RF-01-28`)
- [x] 2.2 Compor cada item com tipo de coleta, cadência, vigência, granularidade exigida e a
      **quantidade de séries no estado `ativa`**, apurada em agregação única sobre os desafios da
      página — nunca uma consulta por desafio —, com zero para o desafio sem série (`RF-02-17`)
- [x] 2.3 Expor `GET /v1/desafios-de-coleta` como leitura de Admin, verificando pelo OpenAPI que
      a rota nasceu sob `/v1` e que ela não cria, altera nem apaga desafio (`RF-02-17`,
      `RF-01-16`)

## 3. Testes do núcleo

- [x] 3.1 Em `tests/test_persona_rota.py`, cobrir a listagem com o vínculo: comunidade e data de
      início na saída, Guerreiro(a) sem vínculo vigente com os campos vazios, vínculo encerrado
      fora da saída e a recusa de quem não é Admin; e o critério de aceite do PRD-02 §12 —
      Guerreiro(a) do onboarding nasce vinculado à comunidade da aula e não há caminho de
      transferência (`RF-02-15`, `RN-02-06`)
- [x] 3.2 Criar `tests/test_desafio_de_coleta_rota.py` cobrindo a listagem de Admin: desafio de
      trilha publicada na lista e o de trilha em rascunho ou despublicada fora dela, séries
      `ativa` contadas e `interrompida`/`encerrada` não, desafio sem série com zero, paginação e
      403 para Mestre, Guerreiro(a), responsável e Apoiador (`RF-02-17`)

## 4. App 03 — porta de API do território

- [x] 4.1 Criar `apps/app-03-gestao/src/territorio/api.ts` com as chamadas da área: listar locais
      da comunidade **seguindo o `proximo_cursor` até o fim** (a árvore e o seletor de pai exigem
      a listagem inteira), cadastrar local, listar solicitações em aberto, dar desfecho à
      solicitação e listar os desafios publicados (`RF-02-16`, `RF-02-17`, `RF-02-21`,
      `RF-02-22`)

## 5. App 03 — área Território

- [x] 5.1 Criar a tela da área com o seletor de comunidade no padrão de Pontos de Apoio e a
      **hierarquia dos locais** montada no cliente a partir da lista plana, apresentando a
      comunidade sem local como vazia e não como falha (`RF-02-16`, `RF-01-18`)
- [x] 5.2 Oferecer ao Admin o cadastro de local com nível escolhido entre os seis, rótulo e local
      pai escolhido **entre os já cadastrados** da comunidade, exigindo pai em todo nível exceto
      `comunidade`, apresentando a recusa do núcleo no campo que a originou e não oferecendo o
      caminho a quem não é Admin (`RF-02-16`, `RN-08-18`)
- [x] 5.3 Apresentar a fila das solicitações de novo local em aberto — solicitante por nick e
      avatar, nível pretendido, rótulo, justificativa e desafio de origem — com **alerta enquanto
      houver ao menos uma sem desfecho**, e sem levá-las à área Filas (`RF-02-21`, `RN-02-22`)
- [x] 5.4 Oferecer ao Admin os dois desfechos: aprovar informando o local pai, o que cria o local
      e o faz aparecer na hierarquia sem recarregar a tela, ou recusar com motivo, sem deixar
      confirmar a recusa vazia e devolvendo a solicitação à fila quando o núcleo recusa a
      hierarquia (`RF-02-22`, `RF-08-23`)
- [x] 5.5 Apresentar, em leitura, os desafios de coleta publicados com tipo, cadência, vigência e
      séries ativas, sem oferecer caminho algum de escrita sobre eles (`RF-02-17`)
- [x] 5.6 Registrar a área Território em `apps/app-03-gestao/src/App.tsx`, entre as áreas da
      navegação (`RF-02-16`)

## 6. App 03 — o vínculo na lista de Guerreiros e Guerreiras

- [x] 6.1 Apresentar na lista de Guerreiros e Guerreiras a comunidade do vínculo vigente e a data
      de início, em leitura, sem caminho de troca em lugar algum e informando em linguagem
      simples o Guerreiro(a) sem vínculo (`RF-02-15`, `RN-02-06`)

## 7. Testes da App 03

- [x] 7.1 Criar `apps/app-03-gestao/src/territorio/territorio.test.tsx` cobrindo a área:
      hierarquia apresentada e troca de comunidade, comunidade vazia sem aviso de erro, cadastro
      de local com e sem pai, recusa de hierarquia apresentada no campo, ausência do caminho de
      cadastro para quem não é Admin, alerta com fila cheia e alerta ausente com fila vazia,
      aprovação que faz o local aparecer, recusa sem motivo barrada, e a lista de desafios em
      leitura, sem caminho de escrita (`RF-02-16`, `RF-02-17`, `RF-02-21`, `RF-02-22`)
- [x] 7.2 Em `apps/app-03-gestao/src/personas/personas.test.tsx`, cobrir a comunidade e a data na
      lista, a ausência de qualquer caminho de transferência e o Guerreiro(a) sem vínculo
      (`RF-02-15`, `RN-02-06`)

## 8. Documentação

- [x] 8.1 Corrigir a redação do `RF-02-17` na §6.1 do PRD-02 para "desafios de coleta de trilha
      publicada" e gravar na §13 a resposta do fundador de 2026-08-27 que a fixou; marcar a fatia
      9 como implementada em `openspec/cronograma-de-fatias.md`, trocando o recorte previsto pelo
      slug da change. Sem decisão de produto nova e, portanto, sem linha no documento 09; a
      situação do PRD-02 em `docs/prds/index.md` não muda, o documento 99 não muda e nenhum
      arquivo novo entra em `docs/` nem na `nav` do `mkdocs.yml`
