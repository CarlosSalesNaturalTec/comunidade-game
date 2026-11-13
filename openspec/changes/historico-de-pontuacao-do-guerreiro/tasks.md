# Tasks

## 1. Núcleo — lançamento de pontuação

- [ ] 1.1 Criar `backend/src/nucleo/historico_de_pontuacao/modelo.py` com `LancamentoDePontuacao`
      e o enum `OrigemDoLancamento` (design, decisões 1 e 3), `CheckConstraint` de trilha ou
      poder só na conta regular, índice `(guerreiro_id, registrado_em DESC, id)` e recusa de
      alteração e remoção no ORM e por gatilho no banco (`RF-01-88`, `RN-01-67`)
- [ ] 1.2 Migração Alembic: cria a tabela e o gatilho e insere a linha de saldo anterior de cada
      `ponto_regular` e de cada `ponto_extra` existentes, contas zeradas inclusive; `downgrade`
      derruba a tabela (`RF-01-90`, design, decisão 5)
- [ ] 1.3 `pontuacao/regra.py` e `ponto_extra/regra.py`: as cinco funções de movimento recebem
      `origem`, `referencia_id` e `detalhe` obrigatórios e gravam o lançamento com o valor
      efetivamente movido — no extra, saldo e acumulado separados (`RF-01-88`, `RN-01-67`)
- [ ] 1.4 Passar a origem em todos os chamadores: `resultados`, `creditar_ponto_extra_do_resultado`,
      `coletas` (crédito e estorno), `quiz`, `criacoes_originais`, `trilhas` (desafio prático),
      `ocorrencias_de_conduta`, `aulas` (presença e estorno), `cuidado_do_bem`, `fila`
      (proposta adotada) e `trocas` (`RF-01-88`)

## 2. Núcleo — leitura do histórico

- [ ] 2.1 `historico_de_pontuacao/regra.py`: leitura paginada do mais recente ao mais antigo, com
      nome da trilha ou do poder, motivo da conduta por `LEFT JOIN` na ocorrência (nunca
      copiado) e os saldos regular e extra (`RF-01-89`, design, decisões 4 e 6)
- [ ] 2.2 `historico_de_pontuacao/rotas.py`: `GET /v1/eu/historico-de-pontuacao` só para o
      Guerreiro(a) e `GET /v1/guerreiros/{id}/historico-de-pontuacao` para Admin e para o Mestre
      com vínculo vigente na comunidade do Guerreiro(a); demais, 403; registrar o roteador
      (`RF-01-89`, `RN-01-68`, `RN-01-41`)

## 3. Apps

- [ ] 3.1 `comum/pontuacao/`: componente `HistoricoDePontuacao` — saldos regular e extra
      rotulados, lista com data, origem em linguagem simples, valor com sinal, trilha ou poder e
      motivo da conduta, "carregar mais", estado vazio e erro declarado pelo núcleo; tipos do
      contrato (`RF-09-144`, `RF-02-116`, `RF-05-104`, invariantes 24 e 25)
- [ ] 3.2 App 09: caminho "Guerreiros e Guerreiras", lista por `GET /v1/guerreiros/vinculaveis`
      (nick e avatar) e ficha com o histórico (`RF-09-143`, `RF-09-144`, `RN-09-18`)
- [ ] 3.3 App 03: ação "Ficha" em `ListaDeGuerreiros` abrindo `FichaDoGuerreiro` com o histórico
      (`RF-02-116`)
- [ ] 3.4 App 05: entrada "Como cheguei aqui" em `MinhaCarteira`, abrindo o histórico do
      próprio pela rota sem identificador (`RF-05-104`)

## 4. Testes

- [ ] 4.1 `backend/tests/test_lancamento_de_pontuacao.py`: lançamento de cada origem nos fluxos
      de resultado (com e sem mérito), coleta e estorno, quiz, criação original, desafio
      prático, conduta (com piso em zero), presença e estorno (saldo parando em zero),
      cuidado do bem, proposta adotada e troca (só saldo); troca recusada sem lançamento;
      alteração e remoção recusadas no ORM e no banco; soma dos lançamentos = total da conta
      (`RF-01-88`, `RN-01-67`)
- [ ] 4.2 `backend/tests/test_historico_de_pontuacao.py`: ordem do mais recente ao mais
      antigo, paginação, saldos, histórico vazio, motivo presente e motivo apagado, linha de
      saldo anterior da migração; autorização — Guerreiro(a) próprio, Mestre do vínculo,
      Mestre de outra comunidade (403), Admin, Guerreiro(a) na rota com id (403), responsável
      e Apoiador (403); `/v1/eu/pontos-extras` segue 403 para Mestre e Admin (`RF-01-89`,
      `RF-01-90`, `RN-01-68`)
- [ ] 4.3 Vitest do componente comum e das três telas: saldos e lançamentos, conduta com
      motivo, troca e estorno negativos, estado vazio, 403 mostrado como recusa, "carregar
      mais" (`RF-09-143`, `RF-09-144`, `RF-02-116`, `RF-05-104`)

## 5. Documentação

- [ ] 5.1 Já feito na abertura da change: documentos 11 §5, 15 §9, 09 §1 e 99 §§3 e 5; PRD-01,
      PRD-02, PRD-05 e PRD-09 (§6, §7, §9, §13, §15); fatia 33 no cronograma. Ao fechar: marcar
      a fatia 33 como `implementado` com o slug arquivado, e conferir que o PRD-01 §9 e os
      contratos dos PRDs batem com as rotas entregues; `docs/prds/index.md` não muda
