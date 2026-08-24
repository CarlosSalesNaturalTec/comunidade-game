## 1. Modelo e migração

- [x] 1.1 Acrescentar `missao_id` e `trilha_id` a `PerguntaDeQuiz` em
      `backend/src/nucleo/quiz/modelo.py`, ambas `NOT NULL` com chave estrangeira, e retirar
      qualquer menção a situação — a entidade não a tem (`RF-09-39`, design decisões 1 a 3).
      Verificar: `PerguntaDeQuiz` importa e os testes existentes de `test_quiz.py` seguem
      passando depois de ajustados ao vínculo obrigatório.
- [x] 1.2 Criar a revisão Alembic que acrescenta as duas colunas com índice em cada uma, sem
      _backfill_, e o `downgrade` que as remove (design — Migration Plan). Verificar:
      `alembic upgrade head` e `alembic downgrade -1` correm limpos sobre o banco de teste.

## 2. Regra

- [x] 2.1 Fazer `cadastrar_pergunta` receber a missão, recusar cadastro sem ela com
      `ErroDeValidacao`, derivar a trilha da missão e gravar as duas — sem tocar nas recusas de
      alternativa que já existem (`RF-09-36`, `RF-09-37`, `RF-09-39`, design decisão 1).
      Verificar: cenários "Pergunta com quatro alternativas e uma correta é aceita" e "Pergunta
      sem missão declarada é recusada" da spec.
- [x] 2.2 Escrever `perguntas_do_mestre` em `backend/src/nucleo/quiz/regra.py` — perguntas do
      Mestre em sessão, com filtros opcionais por trilha e por missão, paginada pelas
      convenções de `paginacao.py` (`RF-09-40`, `RF-01-16`, design decisão 4). Verificar: os
      cenários de filtro e de isolamento por autoria da spec.

## 3. Porta HTTP

- [x] 3.1 Criar `backend/src/nucleo/quiz/rotas.py` com `POST /v1/perguntas` e
      `GET /v1/perguntas/minhas`, delegando à regra sem conferência própria de permissão, e
      registrar o roteador em `principal.py` (PRD-09 §9, `RF-09-36`, `RF-09-40`, design decisão
      5). Verificar: as duas rotas aparecem no OpenAPI e respondem 201 e 200 no caminho feliz.

## 4. Testes do núcleo

- [x] 4.1 Estender `backend/tests/test_quiz.py` com o vínculo obrigatório: os quatro cenários do
      requisito modificado — aceite com missão e trilha derivada, três alternativas recusadas,
      sem alternativa correta recusada, sem missão recusada (`RF-09-36`, `RF-09-37`,
      `RF-09-39`). Cobre o critério de aceite do PRD-09 §12 "pergunta com três alternativas é
      recusada; pergunta com quatro e uma correta entra no banco".
- [x] 4.2 Cobrir a leitura do banco: Mestre lê o próprio, filtro por missão, filtro por trilha
      alcançando todas as missões dela, banco de um Mestre invisível para outro, e 403 para
      Guerreiro(a) (`RF-09-40`, `RF-01-16`) — os cinco cenários do requisito acrescentado.

## 5. App 09 — área "Banco do Quiz"

- [x] 5.1 Criar `apps/app-09-mestre/src/quiz/api.ts` com o cliente das duas rotas, no padrão de
      `trilhas/api.ts` e `turmas/api.ts` (`RF-09-36`, `RF-09-40`). Verificar: tipos compilam e
      o `vitest` do módulo passa.
- [x] 5.2 Criar o formulário de cadastro — enunciado, as quatro alternativas, a indicação da
      correta e o seletor de missão dentro de uma trilha do Mestre —, recusando o envio
      incompleto com mensagem sem jargão (`RF-09-36`, `RF-09-37`, `RF-09-39`, PRD-09 §10).
- [x] 5.3 Criar a lista do banco com os filtros por trilha e por missão (`RF-09-40`).
- [x] 5.4 Ligar a área "Banco do Quiz" à navegação da App 09, ao lado de Minhas turmas e
      Autoria. Verificar: `apps/app-09-mestre/src/quiz/quiz.test.tsx` cobre cadastro com as
      quatro alternativas, recusa do incompleto e filtro da lista.

## 6. Documentação

- [x] 6.1 Gravar a decisão do fundador de 2026-08-23 e o que a fatia entregou: riscar
      **situação** da linha `PerguntaDeQuiz` no PRD-09 §8 e confirmar ali trilha e missão;
      acrescentar a linha "Situação da pergunta de quiz" aos **já decididos** do documento 09;
      narrar a quinta fatia do PRD-09 em `docs/prds/index.md`, registrando que o `RF-09-41`
      segue pendente até a condução da partida ter porta. O documento 05 §5 não muda — nunca
      previu situação —, nenhum arquivo nasce em `docs/`, e por isso `mkdocs.yml` e o documento
      99 ficam como estão.
