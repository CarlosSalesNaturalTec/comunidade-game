## 1. Núcleo — porta da equipe da trilha (fatia 8)

- [ ] 1.1 `equipes/rotas.py`: `POST /v1/trilhas/{id}/equipes`, sob
      `Operacao.equipe_que_forma_na_aula`, chamando `criar_equipe` com a trilha e devolvendo
      201 com a equipe e o autor como primeiro integrante; trilha inexistente responde 404
      (`RF-04-61`, design — decisão 6). Verificar pela rota nova em
      `tests/test_equipe_da_trilha_rota.py`.
- [ ] 1.2 `equipes/rotas.py`: `POST /v1/equipes/{id}/homologacao`, sob
      `Operacao.homologacao_da_equipe_da_trilha`, chamando `homologar_equipe_da_trilha` e
      devolvendo quem homologou e quando; equipe da aula responde 422 e Guerreiro(a) responde
      403 (`RF-04-62`). Verificar no mesmo arquivo de teste.
- [ ] 1.3 `equipes/rotas.py` e `trilhas/`: `ItemDaProgramacaoSaida` ganha `trilha_id` e
      `trilha_titulo`, alimentados pela missão de cada item (`RF-04-35`, `RF-04-61`, design —
      decisão 7). Verificar em `tests/test_programacao_do_encontro.py`, no cenário "Cada item
      traz a trilha da missão".

## 2. Núcleo — entidade e porta da produção (fatia 9)

- [ ] 2.1 `producoes/modelo.py`: `ProducaoDaMissao` com equipe, Guerreiro(a), missão,
      atividade, forma de entrega (texto, áudio, foto), transcrição, devolutiva e momento, com
      a restrição de **exatamente um** entre equipe e Guerreiro(a); sem coluna de foto, de
      áudio nem de custo (`RF-04-45`, `RF-04-46`, design — decisão 2).
- [ ] 2.2 `backend/alembic/`: uma migração criando `producao_da_missao`, com a restrição da
      2.1. Verificar que `alembic upgrade head` e `downgrade` correm limpos no banco de teste.
- [ ] 2.3 `producoes/porta.py`, `local.py`, `nuvem.py` e `fabrica.py`: `LeituraDaProducao`
      (transcrição e devolutiva) e `PortaDaProducaoDaMissao.ler(...)`, com `None` como
      indisponibilidade; adaptador local fora de produção e Gemini em produção, escolhido pelo
      ambiente, sem medir consumo nem lançar custo (`RF-04-46`, `RF-04-47`, `RF-09-90`, design
      — decisão 4). Verificar em `tests/test_producao_da_missao_porta.py`.
- [ ] 2.4 `producoes/regra.py`: `registrar_producao` — integrância na equipe (403 a quem não a
      integra e a Mestre e Admin), atividade corrente obrigatória (422), aula encerrada (422),
      forma única entre as três (422), missão derivada da atividade, e o desfecho da
      indisponibilidade por forma: texto grava com devolutiva em branco, áudio e foto respondem
      503 sem gravar (`RF-04-45` a `RF-04-47`, design — decisão 5). Verificar em
      `tests/test_producao_da_missao.py`.
- [ ] 2.5 `producoes/regra.py`: a gravação **não** emite `Resultado`, lançamento, ponto, nível
      nem badge, e **não** consulta chave de personalização de integrante algum (`RF-04-47`,
      `RN-04-31`). Verificar no mesmo arquivo, com o percurso de cada integrante inalterado
      depois de várias entregas.
- [ ] 2.6 `permissoes.py`: `Operacao.producao_da_equipe`, no Guerreiro(a), em escreve e lê
      (`RF-04-45`, design — decisão 6). Verificar em `tests/test_permissoes.py`.
- [ ] 2.7 `producoes/rotas.py`: `POST /v1/equipes/{id}/producao` em `multipart/form-data` —
      `forma` e `texto` por `Form`, `arquivo` por `UploadFile` —, lendo o byte em memória,
      passando-o à porta e deixando-o sair de escopo sem tocar `armazenamento`, disco ou log; a
      resposta traz transcrição e devolutiva, e nenhum campo de foto, áudio, custo ou cota
      (`RF-04-45`, `RF-04-46`, design — decisão 3). Registrar o roteador em `app.py`.

## 3. Testes do núcleo

- [ ] 3.1 `tests/test_equipe_da_trilha_rota.py`: os cenários das duas rotas novas de `equipe` —
      criação com primeiro integrante, tetos de composição, segunda equipe da mesma trilha,
      Admin e Mestre recusados, trilha inexistente, homologação pelo Mestre, composição fixa
      depois dela, Guerreiro(a) recusado e equipe da aula recusada.
- [ ] 3.2 `tests/test_producao_da_missao.py`: os cenários de `producao-da-missao` — as três
      formas de entrega, entrega sem conteúdo e com duas formas, equipe sem atividade corrente,
      um registro por equipe com Guerreiro(a) em branco, produção visível a todos os
      integrantes, devolutiva sem crédito, integrante com chave desligada, quem não integra,
      Mestre e Admin, aula encerrada e sem sessão.
- [ ] 3.3 `tests/test_producao_da_missao_porta.py`: descarte de foto e áudio (nada persistido,
      nada em log, nada na resposta), devolutiva em branco no texto, 503 na foto e no áudio, e
      ausência de lançamento no livro-razão e de contador de consumo.

## 4. App 01

- [ ] 4.1 `src/api/equipes.ts` e `src/api/producao.ts`: as três chamadas novas — criar equipe
      da trilha, homologar e entregar a produção em `multipart` — e o `trilha_id` que a
      programação passa a trazer (`RF-04-61`, `RF-04-62`, `RF-04-45`).
- [ ] 4.2 `src/trilhas/TelaDaProgramacao.tsx`: na atividade corrente, formar ou entrar na
      equipe da trilha com o papel declarado, recusas em linguagem simples, e nenhuma ação de
      entrar ou sair depois de homologada (`RF-04-61`, `RN-01-44`).
- [ ] 4.3 `src/trilhas/`: a homologação oferecida só ao Mestre em sessão de trabalho, com a
      composição — avatar, nick e papel — e o aviso de que a composição fica fixa; nunca
      oferecida ao Guerreiro(a), e a aplicação segue sem oferecer formar equipe à gestão
      (`RF-04-62`, `RN-04-18`).
- [ ] 4.4 `src/trilhas/`: a entrega da produção nas três formas, com a produção esperada em
      tela, o microfone abrindo por ação e fechando ao fim da fala, nada de foto ou áudio
      guardado no aparelho, a devolutiva apresentada com o aviso de que não vale ponto, o
      retorno que não veio no texto e o pedido de reenvio na fala e na foto (`RF-04-45` a
      `RF-04-47`, `RN-04-20`, `RN-04-12`).
- [ ] 4.5 `src/trilhas/trilhas.test.tsx`: os cenários de `aplicacao-da-aula-presencial` desta
      change — formação a partir da atividade escolhida, segunda equipe recusada, equipe
      homologada sem entrar nem sair, homologação só para o Mestre, as três entregas, a tela
      dizendo que a devolutiva não vale ponto, o reenvio pedido e a entrega por texto sempre
      oferecida em aparelho sem câmera nem microfone (`RF-04-45`, `RN-04-09`).

## 5. Documentação

- [ ] 5.1 Gravar a decisão nova de 2026-08-30 — a produção entregue no App 01 é da equipe, num
      registro só válido para todos os integrantes — no **documento 03 §4.2** (documento-fonte)
      em uma frase, e como linha nova no **documento 09 §1**.
- [ ] 5.2 PRD-04: a `ProducaoDaMissao` na §8, a rota `POST /v1/equipes/{id}/producao` na §9 com
      o erro de leitura indisponível, e as duas linhas de decisão na §13. PRD-05 §8: a entidade
      passa a admitir o vínculo com a equipe.
- [ ] 5.3 `openspec/cronograma-de-fatias.md`: corrigir o recorte da fatia 8 para `RF-04-61` e
      `RF-04-62` — `RN-04-17` e `RN-04-22` são regras da partida, atendidas nas fatias 6 e 7 —
      e marcar as fatias 8 e 9 como implementadas, com o slug desta change nas duas linhas.
      `docs/prds/index.md`, o documento 99 e a `nav` do `mkdocs.yml` **não mudam**: o PRD-04
      segue "aprovado", nenhuma relação entre documentos se altera e nenhum arquivo nasce em
      `docs/`.
