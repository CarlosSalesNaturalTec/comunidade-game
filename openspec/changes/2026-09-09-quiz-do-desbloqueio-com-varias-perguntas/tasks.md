## 1. Núcleo — modelo e migração

- [ ] 1.1 Em `backend/src/nucleo/trilhas/modelo.py`, criar `PerguntaDoDesbloqueio` (missão,
      ordem, enunciado, quatro alternativas, correta, com unicidade de ordem por missão),
      `SubmissaoDoDesbloqueio` (guerreiro, missão, instante, acertos, total) e
      `RespostaDaSubmissao` (submissão, pergunta, alternativa escolhida, se acertou), e retirar
      da `Missao` as seis colunas do desafio, mantendo `tipo_do_desafio_de_desbloqueio` e o
      `enunciado` do prático (`RF-09-118`, `RN-05-47`, design — decisões 1 e 2). Verificar que
      `uv run pytest tests/test_desbloqueio_da_missao.py -x` carrega o modelo sem erro de
      mapeamento.
- [ ] 1.2 Escrever a revisão do Alembic que cria as três tabelas, transporta cada quiz de
      pergunta única existente como a primeira pergunta da sua missão e só então derruba as
      seis colunas; o `downgrade` refaz o inverso pela pergunta de menor ordem (design —
      Migration). Verificar com `alembic upgrade head` seguido de `alembic downgrade -1` sobre
      banco com desafio de quiz e de prático semeados.

## 2. Núcleo — regra

- [ ] 2.1 `declarar_desafio_de_desbloqueio` passa a receber a lista de perguntas do quiz,
      substituir por inteiro as perguntas anteriores ao redeclarar e recusar com 422 o quiz sem
      nenhuma pergunta; o prático segue pelo `enunciado` (`RF-09-118`, `RN-09-43`). Verificar
      pelos cenários de declaração em `test_desbloqueio_da_missao.py`.
- [ ] 2.2 `submeter_desafio_de_desbloqueio` passa a receber a resposta de todas as perguntas,
      aferir por `acertos * 10 >= total * 6` e devolver `acertos` e `total`; na missão de
      sondagem desbloqueia ao submeter, sem aferir (`RF-05-89`, `RN-05-45`, `RN-05-46`, design
      — decisões 3 e 4). Verificar pelos cenários de aferição e de sondagem.
- [ ] 2.3 Gravar `SubmissaoDoDesbloqueio` e as `RespostaDaSubmissao` em **toda** tentativa — a
      que passa, a que não passa e a da sondagem —, sem apagar nem sobrescrever as anteriores,
      e sem creditar ponto (`RN-05-47`). Verificar que duas tentativas na mesma missão deixam
      duas submissões.
- [ ] 2.4 `duplicar_trilha` passa a copiar as perguntas do quiz de cada missão, na ordem da
      origem, e segue sem copiar submissão nem desbloqueio (`RF-09-13`). Verificar por
      `test_duplicacao_de_trilha.py`.

## 3. Núcleo — rotas

- [ ] 3.1 `POST /v1/missoes/{id}/desbloqueio` passa a receber `perguntas`; a leitura da missão
      no percurso e a da trilha do Mestre passam a servir as perguntas **sem** a alternativa
      correta (`RF-09-118`, design — decisão 6). Verificar que a saída do percurso não traz a
      correta em nenhum caminho.
- [ ] 3.2 `POST /v1/eu/missoes/{id}/desbloqueio` passa a receber `respostas`
      (`pergunta_id`, `alternativa_escolhida`) e a devolver `acertos` e `total` ao lado de
      `aprovado` e `aguardando_mestre`; resposta faltando, repetida ou de pergunta de outra
      missão é 422 (`RF-05-89`). Verificar pelos cenários de contrato da submissão.

## 4. App 09 — bancada do Mestre

- [ ] 4.1 Em `apps/app-09-mestre/src/trilhas/`, `api.ts` e `DesafioDeDesbloqueio.tsx` passam a
      montar o quiz com quantas perguntas o Mestre quiser: acrescentar, remover, preservar a
      ordem, impedir a gravação sem nenhuma pergunta e dizer que passa quem acerta ao menos 60%
      (`RF-09-118`, `RN-09-43`).
- [ ] 4.2 O resumo do bloco recolhível do desafio, em `ListaDeMissoes.tsx`, passa a dizer
      quantas perguntas o quiz tem (`RF-09-118`).

## 5. App 05 — área do Guerreiro(a)

- [ ] 5.1 Em `apps/app-05-guerreiro/src/`, `api/trilha.ts` e
      `trilha/DesafioDeDesbloqueio.tsx` passam a apresentar todas as perguntas numa tela, a
      submeter as respostas de uma vez, a sinalizar pergunta sem resposta antes do envio, a
      dizer quantas ele acertou ao não passar e a não falar em aprovação na sondagem
      (`RF-05-89`, `RN-05-45`, `RN-05-46`).

## 6. Testes

- [ ] 6.1 `backend/tests/test_desbloqueio_da_missao.py` cobre os cenários da spec
      `desbloqueio-da-missao`: quiz com N perguntas, quiz sem pergunta recusado, redeclarar
      substituindo, corte de 60% para os dois lados, sondagem que abre ao ser respondida, toda
      tentativa gravada e registro de terceiro recusado.
- [ ] 6.2 `backend/tests/test_percurso_da_trilha.py` e `test_duplicacao_de_trilha.py` cobrem a
      regressão do percurso com o modelo novo e a cópia das perguntas na duplicação.
- [ ] 6.3 Os testes da App 09 cobrem acrescentar e remover pergunta, a recusa do quiz vazio e o
      resumo com a contagem de perguntas.
- [ ] 6.4 Os testes da App 05 cobrem a submissão única com todas as respostas, a pergunta sem
      resposta sinalizada, a devolutiva com os acertos e a sondagem sem linguagem de aprovação.

## 7. Documentação

- [ ] 7.1 Marcar a fatia 18 do PRD-09 como implementada em
      `openspec/cronograma-de-fatias.md`, com o slug desta change, e devolver o PRD-05 a
      **implementado** na tabela de `docs/prds/index.md`, já que os requisitos que o tiraram de
      lá são os desta fatia. Os documentos 11 §2.2, 03 §11 e 09 §1, os PRDs e o documento 99 já
      foram atualizados antes da change e não mudam de novo.
