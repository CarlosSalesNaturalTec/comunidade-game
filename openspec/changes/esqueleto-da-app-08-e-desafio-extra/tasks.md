## 1. Núcleo — a entidade `DesafioExtra`

- [ ] 1.1 Criar `backend/src/nucleo/desafios_extras/modelo.py` com `DesafioExtra` e os atributos
      do PRD-14 §8: proponente, trilha, missão opcional, modalidade, nick do destinatário e
      justificativa do vínculo, recompensa, quantidade disponível, critério de atribuição,
      pontos extras, formato, custeio, vigência, Mestre validador, Admin aprovador, aporte de
      lastro, situação, motivo da recusa e etiquetas ODS herdadas; `ComAutoria` grava quem
      propôs. O **nick do destinatário é coluna de texto, sem `ForeignKey`** (`RF-14-29` a
      `RF-14-32`, `RF-14-74` a `RF-14-76`, `RN-14-17`, `RN-14-18`)
- [ ] 1.2 Declarar os dois `StrEnum` da entidade — `Modalidade` (aberto, direcionado) e
      `SituacaoDoDesafioExtra` (em validação do Mestre, em aprovação do Admin, publicado,
      recusado) — e a restrição de banco que exige nick e justificativa **somente** no
      direcionado (`RF-14-31`, `RF-14-32`, `RF-14-35`, `RN-14-13`)
- [ ] 1.3 Escrever a migração Alembic da tabela, com o teto de 10 pontos extras como
      `CheckConstraint` (`RF-14-74`, `RN-14-41`)

## 2. Núcleo — a regra da proposta

- [ ] 2.1 Implementar em `desafios_extras/regra.py` o registro da proposta: exigir trilha em
      **andamento** (422 quando não for), recompensa, quantidade, critério de atribuição,
      vigência, formato e custeio, sem teto de propostas simultâneas (`RF-14-29`, `RF-14-30`,
      `RF-14-75`, `RN-14-15`, `RN-14-16`)
- [ ] 2.2 Recusar com 422 os pontos extras acima de 10 e registrar a proposta sempre em
      `em_validacao_do_mestre`, mantendo os pontos do desafio isolados da pontuação regular
      (`RF-14-74`, `RN-14-41`, `RN-14-19`, `RN-14-13`)
- [ ] 2.3 Aceitar a proposta direcionada **sem consultar a existência do nick** e recusar com
      422 a que não traga nick ou justificativa do vínculo (`RF-14-32`, `RF-14-33`, `RN-14-17`,
      `RN-14-18`)
- [ ] 2.4 Derivar `lastro_provido` do custeio declarado — aporte do proponente **homologado**
      ou saldo de recurso disponível — e implementar a guarda da publicação, que recusa publicar
      o desafio sem lastro informando o que falta prover, sem rota que a chame nesta fatia
      (`RF-14-34`, `RF-14-76`, `RF-07-15`, `RF-07-41`, `RN-14-14`)
- [ ] 2.5 Recusar com 405 toda alteração de desafio **publicado**, preservando a proposta
      anterior com o desfecho que teve (`RF-14-38`)

## 3. Núcleo — as rotas do proponente

- [ ] 3.1 Expor `POST /v1/desafios-extras` sob a operação `propostas_de_desafio_extra`, restrita
      ao Apoiador em sessão, e registrar o roteador na aplicação (`RF-14-29` a `RF-14-34`,
      `RF-14-74` a `RF-14-76`)
- [ ] 3.2 Expor `GET /v1/eu/desafios-extras` com a situação de cada desafio do proponente, o
      motivo da recusa, o que falta de lastro e a **quantidade restante** no publicado, sem
      nome real, contato ou dado de identificação de Guerreiro(a) e sem dado algum do
      destinatário (`RF-14-35` a `RF-14-37`, `RF-14-39`, `RN-14-18`, `RN-14-20`)

## 4. Testes do núcleo

- [ ] 4.1 Em `tests/test_desafio_extra_regra.py`, cobrir a proposta: trilha fora de andamento
      recusada, ausência de formato ou custeio recusada, teto de 10 pontos, situação inicial,
      direcionado sem justificativa recusado, nick inexistente **aceito** — critério de aceite
      do PRD-14 §12 —, `lastro_provido` derivado nos dois custeios, publicação sem lastro
      recusada e alteração de publicado recusada com 405 (`RF-14-29` a `RF-14-34`, `RF-14-38`,
      `RF-14-74` a `RF-14-76`, `RF-07-15`, `RN-14-13` a `RN-14-18`, `RN-14-41`)
- [ ] 4.2 Em `tests/test_desafio_extra_rota.py`, cobrir as duas rotas: papel que não é Apoiador
      recusado, proposta registrada com o proponente da sessão, leitura devolvendo situação,
      motivo, lastro que falta e quantidade restante, e a conferência de que **nenhuma resposta
      traz identificação de Guerreiro(a) nem indica se o nick existe** (`RF-14-35` a `RF-14-37`,
      `RF-14-39`, `RN-14-18`, `RN-14-20`)

## 5. App 08 — a aplicação e a entrada do Apoiador

- [ ] 5.1 Criar `apps/app-08-apoiador/` no molde de `apps/app-09-mestre/` — Vite, React, TS,
      `index.html`, `vite.config.ts`, `tsconfig*`, `.env.example` com a chave `app-08-apoiador`,
      `README.md` e favicon — e registrar a pasta no _workspace_ do `package.json` da raiz; o
      `frontend-ci.yml` já a alcança por `apps/**`, e nenhum workflow novo nasce (`RF-01-02`,
      `RN-01-32`)
- [ ] 5.2 Implementar `src/autenticacao/` sobre `comum/`: entrada por login social e por usuário
      e senha, sessão guardada como nas demais aplicações e nenhuma tela do Apoiador acessível
      sem sessão (`RF-14-08`)
- [ ] 5.3 Trancar todas as demais telas até a troca da senha provisória, sem caminho de
      contorno, e apresentar a recusa do login sem cadastro com a orientação de usar o
      pré-cadastro (`RF-14-09`, `RF-14-10`, `RN-14-02`)
- [ ] 5.4 Conferir que nenhuma tela oferece convite, delegação ou segundo acesso ao mesmo
      cadastro (`RF-14-11`, `RN-14-04`)

## 6. App 08 — as telas do desafio extra

- [ ] 6.1 Implementar `src/desafiosExtras/` com a proposição: trilha em andamento, recompensa,
      quantidade, critério de atribuição, vigência, modalidade, pontos extras com o teto de 10
      recusado na tela, formato e custeio; no direcionado, nick e justificativa do vínculo, sem
      confirmar existência e sem exibir dado do destinatário (`RF-14-29` a `RF-14-33`,
      `RF-14-74` a `RF-14-76`)
- [ ] 6.2 Implementar o acompanhamento: estado no fluxo, motivo da recusa em linguagem simples,
      o que falta de lastro, quantidade restante no publicado e **nenhuma edição** de desafio
      publicado, com a indicação de que a correção é propor de novo (`RF-14-34` a `RF-14-38`)
- [ ] 6.3 Conferir que nenhuma tela de desafio exibe nome real ou contato de Guerreiro(a), nem
      oferece campo de mensagem, telefone ou e-mail (`RF-14-39`, `RN-14-20`)

## 7. Testes da App 08

- [ ] 7.1 Em `apps/app-08-apoiador/src/testes/`, cobrir a entrada: sem sessão só a entrada
      aparece, senha provisória tranca as demais telas, login sem cadastro recusado com a
      orientação do pré-cadastro e ausência de convite ou segundo acesso — critérios de aceite
      do PRD-14 §12 (`RF-14-08` a `RF-14-11`, `RN-14-02`, `RN-14-04`)
- [ ] 7.2 Cobrir as telas do desafio: teto de pontos recusado na tela, direcionado com nick
      desconhecido aceito sem revelar nada, lastro que falta exibido, publicado sem edição com a
      quantidade restante e nenhuma tela com campo de mensagem (`RF-14-29` a `RF-14-39`,
      `RF-14-74` a `RF-14-76`)

## 8. Documentação

- [ ] 8.1 Marcar a fatia 1 do PRD-14 como `implementado` em `openspec/cronograma-de-fatias.md`,
      trocando o recorte previsto pelo slug da change. Não há decisão nova a gravar em `docs/`:
      a fatia aplica o PRD-14 como está, `docs/prds/index.md` só muda quando o PRD inteiro
      estiver implementado, e nenhum arquivo novo entra em `docs/` nem na `nav`
