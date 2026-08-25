## 1. Estado da pergunta no ar

- [x] 1.1 Criar `PerguntaNaPartida` em `backend/src/nucleo/quiz/modelo.py` — partida,
      pergunta, ordem, momento de entrada e momento da liberação —, com unicidade em
      (partida, pergunta) e em (partida, ordem), e a migração Alembic correspondente
      (`RF-02-60`, `RF-04-44`; design — decisão 1). Verificar pelo `alembic upgrade head` em
      banco limpo e pela criação do registro num teste de modelo.
- [x] 1.2 Implementar `por_pergunta_no_ar` em `backend/src/nucleo/quiz/regra.py`: exige quem
      conduz, partida aberta e pergunta do banco da missão da atividade; substitui a anterior
      preservando ordem e momento (`RF-02-60`, `RF-09-41`). Verificar pelos cenários da spec
      `quiz-ao-vivo` — primeira pergunta, substituição, missão errada, partida encerrada e
      403 de quem não conduz.
- [x] 1.3 Implementar `liberar_resultado` na mesma regra: marca a liberação da pergunta no ar,
      é idempotente e não credita pontuação alguma (`RF-04-44`, `RF-02-62`). Verificar pelos
      cenários de liberação, reliberação e ausência de crédito.
- [x] 1.4 Implementar a leitura do estado da partida na regra — situação, pergunta no ar,
      liberação, equipes disputantes e contagem de respostas —, sem devolver a alternativa
      correta antes da liberação (`RF-02-60`, `RF-02-62`; design — decisão 3). Verificar pelos
      dois cenários de leitura da spec.

## 2. Portas HTTP da partida

- [x] 2.1 Acrescentar `conducao_do_quiz_ao_vivo_das_suas_aulas` ao conjunto `le` do Mestre e
      `resposta_de_quiz_da_equipe` ao do Guerreiro(a) em
      `backend/src/nucleo/permissoes.py` (design — decisão 4). Verificar pelo teste da matriz,
      que passa a aceitar as duas leituras e segue recusando os demais papéis.
- [x] 2.2 Escrever em `backend/src/nucleo/quiz/rotas.py` as rotas de escrita da condução —
      `POST /v1/partidas-de-quiz`, `POST /v1/partidas-de-quiz/{id}/perguntas`, `POST
      /v1/partidas-de-quiz/{id}/resultado`, `POST /v1/partidas-de-quiz/{id}/anulacoes` e `POST
      /v1/partidas-de-quiz/{id}/encerramento` —, cada uma sobre a operação já implementada da
      regra (`RF-02-59`, `RF-02-60`, `RF-02-72`, `RF-02-73`, `RF-04-44`). Verificar pelo teste
      de rota de cada uma, incluindo o 403 do Mestre que não conduz.
- [x] 2.3 Escrever as rotas de leitura — `GET /v1/partidas-de-quiz/{id}` para quem conduz e
      `GET /v1/partidas-de-quiz/{id}/pergunta` para o aparelho da equipe —, com esquemas de
      saída próprios que nunca trazem a alternativa correta antes da liberação (`RF-02-60`,
      `RF-04-41`; design — decisão 3). Verificar que a correta não aparece antes e aparece
      depois da liberação.
- [x] 2.4 Escrever `POST /v1/partidas-de-quiz/{id}/respostas` sobre `registrar_resposta`, sem
      alterar a regra (`RF-04-43`, `RF-04-41`). Verificar pelos cenários de resposta única,
      segunda alternativa recusada e reenvio idempotente.

## 3. Testes do núcleo

- [x] 3.1 Cobrir em `backend/tests/test_quiz.py` os cenários de regra do estado novo: pergunta
      no ar e substituição, pergunta de outra missão, partida encerrada, liberação idempotente
      e ausência de crédito na liberação (`RF-02-60`, `RF-04-44`).
- [x] 3.2 Cobrir em `backend/tests/test_quiz_rota.py` o percurso completo pelas rotas — abrir,
      pôr pergunta no ar, responder por duas equipes, liberar o resultado, anular, encerrar e
      conferir o crédito —, mais o 403 do Mestre que não conduz e o aparelho que volta na
      pergunta corrente (`RF-02-59`, `RF-02-62`, `RF-02-72`, `RF-02-73`, PRD-02 §12).

## 4. Tela de condução na App 03

- [x] 4.1 Criar `apps/app-03-gestao/src/quiz/` com o cliente das rotas da partida em
      `src/api/`, seguindo o padrão das áreas já existentes (`RF-02-59` a `RF-02-62`).
      Verificar pelos testes de cliente do módulo.
- [x] 4.2 Implementar a tela de abertura — aula e atividade vindas de `GET /v1/minhas-turmas`,
      equipes de `GET /v1/aulas/{id}/equipes` por avatar e nick, e a frase única quando não há
      equipe formada (`RF-02-59`, `RF-02-61`; design — decisão 6). Verificar pelos três
      cenários de abertura da spec `aplicacao-de-gestao`.
- [x] 4.3 Implementar a tela de condução com os quatro atos — pôr pergunta no ar do banco de
      `GET /v1/perguntas/minhas`, liberar o resultado, anular e encerrar —, mostrando só a
      contagem de quem respondeu antes da liberação (`RF-02-60`, `RF-02-62`, `RF-02-72`,
      `RF-02-73`). Verificar pelos cinco cenários de condução da spec.
- [x] 4.4 Implementar a sondagem a cada 2 segundos, com o aviso de perda de contato que
      preserva o que já está na tela e retoma o estado corrente na sondagem seguinte
      (`RF-02-60`, documento 03 §1; design — decisão 7). Verificar pelos dois cenários de
      sondagem da spec.
- [x] 4.5 Ligar a área ao roteamento e ao menu da App 03 sob a permissão do Mestre, com a
      recusa dita em uma frase para a aula que não é dele (`RF-02-49`, `RN-02-20`). Verificar
      pelos dois cenários de alcance da spec.

## 5. Documentação

- [x] 5.1 Gravar no documento 03 §1 a decisão do fundador de 2026-08-25 — a sincronização em
      tempo real do Ciclo 01 é sondagem periódica, a 2 segundos na partida e 10 segundos no
      painel do dia — e mover a linha correspondente no documento 09 §1 para "Já decididos".
- [x] 5.2 Corrigir os PRDs ao que já está decidido e ao que esta fatia entregou: no PRD-02, o
      `RF-02-61` sem "aparelho vinculado", as três rotas que faltam na §9 e a §10 falando em
      sondagem; no PRD-04, a `RespostaDeQuiz` da §8 sem o aparelho e a §9 com a rota de
      respostas ajustada; e no PRD-01, a matriz da §4 com as duas leituras da partida.
      Registrar a fatia em `docs/prds/index.md`. O documento 99 não muda: nenhuma relação
      entre documentos foi alterada.
