## 1. Núcleo — a lista dos vinculados

- [ ] 1.1 Expor `GET /v1/eu/guerreiros` em `responsaveis/rotas.py`, restrita ao responsável em
      sessão (403 para outro papel), devolvendo os vinculados por vínculo **vigente** com nick,
      avatar e o **grau de parentesco** daquele vínculo; estender `guerreiros_vinculados` para
      trazer o vínculo, e não só o `id` (`RF-13-04`, `RF-13-05`, `RN-13-04`, `RF-01-15`)

## 2. Núcleo — a evolução do vinculado

- [ ] 2.1 Criar `backend/src/nucleo/evolucao/regra.py`, sem `modelo.py`, com a montagem do
      payload: presença não anulada, atividades realizadas com desfecho e data, badges, nível e
      percurso vindos de `trilhas.regra.consultar_progresso` e pontos por poder vindos de
      `PontoRegular` (`RF-13-07`, `RF-13-08`)
- [ ] 2.2 Acrescentar à regra as **criações originais validadas**, com título, trilha e data da
      validação, e omitir as que ainda não foram validadas (`RF-13-10`)
- [ ] 2.3 Garantir na montagem que nenhum dado identificável de outra criança entra no payload —
      atividade em equipe e criação coletiva expõem terceiro no máximo por avatar e nick — e que
      nada de `assistente/` ou `apoio_escolar/` é consultado (`RF-13-11`, `RF-13-12`, `RN-13-20`)
- [ ] 2.4 Implementar em `evolucao/regra.py` a leitura das ocorrências de conduta do vinculado,
      com motivo e momento do fato, devolvendo a ocorrência **sem motivo** quando o expurgo do
      ciclo já o anulou (`RF-13-09`, `RN-13-21`, `RN-01-52`)
- [ ] 2.5 Expor em `evolucao/rotas.py` as duas rotas — `GET /v1/eu/guerreiros/{id}/evolucao` e
      `GET /v1/eu/guerreiros/{id}/ocorrencias` —, cada uma recusando antes o papel que não é
      responsável e exigindo depois o vínculo por `exigir_vinculo_do_responsavel`, e registrar o
      roteador na aplicação (`RF-13-07` a `RF-13-12`, `RN-13-04`)

## 3. Testes do núcleo

- [ ] 3.1 Em `tests/test_evolucao_regra.py`, cobrir a montagem: Guerreiro(a) com histórico traz
      presença, atividades, pontos, poderes, badges e nível; recém-cadastrado traz tudo vazio sem
      falhar; o percurso da trilha vem em missões concluídas e faltantes, nunca como saldo;
      criação validada aparece e a não validada não; ocorrência com motivo e ocorrência já
      expurgada (`RF-13-07` a `RF-13-10`, `RN-13-21`, `RN-01-52`)
- [ ] 3.2 Em `tests/test_evolucao_rota.py`, cobrir as três rotas com os critérios de aceite do
      PRD-13 §12: responsável com dois vinculados vê os dois com o parentesco e um terceiro não
      vinculado não aparece; papel que não é responsável recebe 403; evolução e ocorrências de
      criança sem vínculo recebem 403 sem vazar dado; e a resposta inteira **não traz** consulta
      ao assistente, transcrição de apoio escolar nem dado identificável de outra criança
      (`RF-13-04`, `RF-13-05`, `RF-13-11`, `RF-13-12`, `RN-13-04`, `RN-13-20`)

## 4. App 07 — a aplicação e a entrada do responsável

- [ ] 4.1 Criar `apps/app-07-responsaveis/` no molde de `apps/app-08-apoiador/` — Vite, React,
      TS, `index.html`, `vite.config.ts`, `tsconfig*`, `.env.example` com a chave
      `app-07-responsaveis`, `README.md` e favicon — e registrar a pasta no _workspace_ do
      `package.json` da raiz; `frontend-ci.yml` já alcança `apps/**` e nenhum workflow novo nasce
      (`RF-01-02`, `RN-01-32`)
- [ ] 4.2 Implementar `src/entrada/` sobre `comum/`: login social e usuário e senha, troca
      obrigatória da senha provisória trancando todas as demais telas sem contorno, e recusa do
      login sem cadastro com a orientação de **procurar a gestão no encontro** (`RF-13-01` a
      `RF-13-03`, `RN-13-01`, `RN-13-02`)
- [ ] 4.3 Conferir que nenhuma tela oferece autocadastro, cadastro de responsável, criação,
      edição ou remoção de vínculo, nem mudança do grau de parentesco (`RF-13-06`, `RN-13-01`)

## 5. App 07 — os vinculados e a evolução

- [ ] 5.1 Implementar `src/vinculados/` com a lista dos vinculados, cada um com o grau de
      parentesco, e a alternância entre eles como estado da aplicação, sem nova entrada e sem
      encerrar a sessão; busca por criança não vinculada não a apresenta (`RF-13-04`, `RF-13-05`,
      `RN-13-04`)
- [ ] 5.2 Implementar `src/evolucao/` com o painel do vinculado: presença, atividades realizadas,
      pontos, poderes, badges, nível, progresso de cada trilha como percurso e criações validadas
      com título, trilha e data — o nível nunca como saldo de pontos (`RF-13-07`, `RF-13-08`,
      `RF-13-10`)
- [ ] 5.3 Apresentar as ocorrências de conduta com motivo e data, em linguagem simples e sem
      código de erro, e a ocorrência de ciclo anterior com a data e **sem texto substituto** no
      lugar do motivo apagado (`RF-13-09`, `RN-13-21`)
- [ ] 5.4 Conferir que nenhuma tela apresenta consulta ao assistente, transcrição de apoio
      escolar ou dado identificável de outra criança, e que o fim do vínculo é dito em texto, não
      em erro cru (`RF-13-11`, `RF-13-12`, `RN-13-20`, design — riscos)

## 6. Testes da App 07

- [ ] 6.1 Em `apps/app-07-responsaveis/src/testes/`, cobrir a entrada e a lista: sem sessão só a
      entrada aparece, senha provisória tranca as demais telas, login sem cadastro recusado com a
      orientação de procurar a gestão, ausência de cadastro e de vínculo em toda a aplicação, dois
      vinculados com o parentesco e alternância entre eles sem sair — critérios de aceite do
      PRD-13 §12 (`RF-13-01` a `RF-13-06`, `RN-13-01`, `RN-13-02`, `RN-13-04`)
- [ ] 6.2 Cobrir o painel: evolução com presença, atividades, pontos, poderes, badges e nível;
      percurso da trilha em missões, não em saldo; criação validada com título, trilha e data;
      ocorrência com motivo e ocorrência de ciclo anterior sem motivo; e nenhuma tela com consulta
      ao assistente, transcrição ou dado de outra criança (`RF-13-07` a `RF-13-12`, `RN-13-20`,
      `RN-13-21`)

## 7. Documentação

- [ ] 7.1 Marcar as fatias 1 e 2 do PRD-13 como `implementado` em
      `openspec/cronograma-de-fatias.md`, trocando o recorte previsto pelo slug da change, e
      anotar na linha da fatia 2 que `RF-13-09` saiu sem o estado da reparação
- [ ] 7.2 Registrar a lacuna do **estado da reparação** na §14 do PRD-13 e na tabela de decisões
      pendentes do documento 09 §1 — falta o requisito que crie o registro da reparação (quem o
      lança e se devolve os pontos), decisão do fundador de 2026-08-31 —, e passar o PRD-13 a em
      implementação na tabela de `docs/prds/index.md`. Nenhum arquivo novo entra em `docs/` nem na
      `nav` do `mkdocs.yml`
