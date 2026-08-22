# Tarefas — Culminância e publicação da trilha

## Núcleo — modelo e migração

- [x] 1. Criar `backend/src/nucleo/culminancias/modelo.py` com `Culminancia` — `trilha_id`,
      `descricao`, `modalidade` (`individual`, `em_equipe`) e `criterio_de_validacao` —, com
      índice único em `trilha_id` e `ComAutoria`. (`RF-09-29`, `RF-09-30`)
- [x] 2. Acrescentar `despublicada` a `SituacaoDaTrilha` e as quatro colunas de procedência à
      `Trilha` — `motivo_da_situacao`, `autor_da_situacao_id`, `papel_do_autor_da_situacao`,
      `situacao_alterada_em` —, anuláveis, no padrão do `PontoDeApoio`. (`RF-09-10`,
      `RF-09-11`, design 3)
- [x] 3. Gerar a migração Alembic das duas tarefas acima: tabela nova e alteração da restrição
      de verificação da situação, sem retroalimentar trilha existente. (design 3)

## Núcleo — regra

- [x] 4. Escrever `culminancias/regra.py`: declarar a culminância com posse do Mestre autor
      (403 para outro Mestre), recusar modalidade fora dos dois valores e critério em falta
      (422), e substituir a existente em vez de criar segunda. (`RF-09-29`, `RF-09-30`)
- [x] 5. Acrescentar a `trilhas/regra.py` a conferência das três travas — sondagem declarada,
      `EXISTS` de desafio de coleta nas missões da trilha, culminância declarada — devolvendo
      **todas** as pendentes de uma vez, não a primeira. (`RF-09-06`, `RF-09-07`, `RF-09-08`,
      `RF-09-82`, `RN-09-02`, `RN-09-03`, `RN-09-29`, design 5, 6)
- [x] 6. Acrescentar a `trilhas/regra.py` a publicação pelo Mestre autor a partir de
      `rascunho` ou `despublicada`, recusando de trilha já publicada (422) e de quem não é o
      autor (403), gravando a procedência e limpando o motivo. Sem conferência de lastro de
      recompensa. (`RF-09-05`, `RF-09-11`, `RN-09-01`, `RN-09-27`, design 4, 7)
- [x] 7. Acrescentar a `trilhas/regra.py` a despublicação privativa de Admin, com motivo
      obrigatório (422 sem motivo, 403 para Mestre, 422 sobre rascunho), gravando situação,
      motivo, autor, papel e momento, sem tocar missão, atividade, resultado, presença ou
      ponto. (`RF-09-10`, `RF-09-11`)

## Núcleo — porta HTTP

- [x] 8. Criar `culminancias/rotas.py` com `POST /v1/trilhas/{id}/culminancia` e registrar o
      roteador em `principal.py`. (`RF-09-29`, `RF-09-30`)
- [x] 9. Acrescentar a `trilhas/rotas.py` `POST /v1/trilhas/{id}/publicacao`,
      `POST /v1/trilhas/{id}/despublicacao` e o `GET /v1/trilhas/{id}` público que serve só
      trilha publicada — 404 para rascunho e despublicada —, com a licença CC BY-SA e o
      crédito ao Mestre autor. (`RF-09-05`, `RF-09-09`, `RF-09-10`, `RN-09-05`, design 8)
- [x] 10. Fazer `GET /v1/trilhas/minhas` devolver o motivo da despublicação junto da situação,
      que é como o Mestre autor o lê. (`RF-09-10`)

## Testes do núcleo

- [x] 11. `backend/tests/test_culminancia.py` — cenários da spec `culminancia`: declaração
      pelo autor, modalidade inválida, critério em falta, Mestre não autor recusado,
      substituição da anterior, e a criação original resolvida pela trilha sem coluna nova.
      (`RF-09-29`, `RF-09-30`)
- [x] 12. Acrescentar a `backend/tests/test_trilha.py` os cenários de situação e travas da
      spec `trilha-e-missao`: despublicada invisível em consulta pública, trilha despublicada
      editável pelo autor, as três travas isoladas e as três juntas, recompensa sem lastro que
      publica, e o percurso preservado na despublicação. (`RF-09-06` a `RF-09-08`, `RF-09-11`,
      `RF-09-82`, `RN-09-27`)
- [x] 13. Acrescentar a `backend/tests/test_trilha_rota.py` os cenários de porta: publicação
      pelo autor, 403 de outro Mestre, despublicação por Admin com e sem motivo, 403 de Mestre
      despublicando, 422 sobre rascunho, republicação pelo autor com as travas reconferidas,
      `GET` público servindo só publicada, e o motivo em `minhas`. (`RF-09-05`, `RF-09-09`,
      `RF-09-10`, `RF-09-11`)

## App 09

- [x] 14. Criar a tela da culminância dentro de `apps/app-09-mestre/src/trilhas/` —
      descrição, modalidade e critério —, apresentando a já declarada e permitindo
      substituí-la, e estender `trilhas/api.ts` com a chamada. (`RF-09-29`, `RF-09-30`)
- [x] 15. Acrescentar a ação de publicar em `TelaDaTrilha.tsx`, com a recusa apresentada em
      linguagem simples nomeando todas as travas que faltam, sem código de erro nem jargão.
      (`RF-09-05`, `RF-09-08`, `RF-09-12`, `RF-09-82`)
- [x] 16. Apresentar em `ListaDeTrilhas.tsx` as três situações e, na despublicada, o motivo
      registrado pelo Admin; não oferecer a publicação em trilha de outro Mestre. (`RF-09-04`,
      `RF-09-10`)
- [x] 17. Acrescentar a `apps/app-09-mestre/src/trilhas/trilhas.test.tsx` os cenários da spec
      `area-do-mestre`: culminância declarada e substituída, campo obrigatório em falta,
      publicação bem-sucedida, recusa com uma e com três travas, republicação, motivo visível
      e ação ausente em trilha alheia. (`RF-09-08`, `RF-09-10`, `RF-09-29`)

## Documentação

- [x] 18. Gravar as decisões novas e o que elas mudam: as duas decisões de 2026-08-22 no
      documento 03 §11 (fonte única da publicação e curadoria da trilha); a pendência das
      situações movida para "Já decididos" no documento 09, junto da linha nova da
      republicação e da consequência conhecida da trilha publicada imutável; no PRD-09, o
      `RF-09-11` reescrito para "volta a ser editável, como rascunho", o `RF-09-05` estendido
      à trilha despublicada e a §14 sem a pendência resolvida; a segunda fatia do PRD-09 em
      `docs/prds/index.md`. Nenhum arquivo novo em `docs/`, logo a `nav` do `mkdocs.yml` não
      muda; o documento 99 também não, porque nenhuma relação entre documentos mudou.
