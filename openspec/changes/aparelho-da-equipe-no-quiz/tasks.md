## 1. Núcleo — descoberta da partida

- [x] 1.1 Em `backend/src/nucleo/quiz/regra.py`, escrever `partidas_da_aula`, que exige
      `resposta_de_quiz_da_equipe` em leitura, lista as partidas da aula com a situação e cruza
      as equipes disputantes com as que o Guerreiro(a) em sessão integra, devolvendo a única que
      resta ou nula (`RF-04-41`, `RF-04-42`; design — decisão 1). Verificar por
      `uv run pytest tests/test_quiz.py -x`.
- [x] 1.2 Em `backend/src/nucleo/quiz/rotas.py`, expor `GET /aulas/{id}/partidas` sobre
      `partidas_da_aula`, sem tocar na matriz de permissões (`RF-04-41`, `RF-04-42`). Verificar
      por `uv run pytest tests/test_quiz_rota.py -x`.

## 2. Núcleo — resultado para o aparelho

- [x] 2.1 Ampliar `pergunta_para_equipe` e `PerguntaParaEquipeSaida` para, quando a pergunta no
      ar estiver com o resultado liberado, devolver a alternativa correta, se a equipe daquele
      Guerreiro(a) acertou e qual equipe chegou primeiro por ordem de chegada no servidor; antes
      da liberação, nenhum dos três sai, e a leitura nunca credita (`RF-04-44`; design —
      decisão 2). Verificar por `uv run pytest tests/test_quiz.py -x`.
- [x] 2.2 Corrigir a spec consolidada de `quiz-ao-vivo` onde ela promete que o aparelho da equipe
      lê o estado da partida: `estado_da_partida` segue restrita a quem conduz, e o aparelho
      acompanha pela pergunta no ar (`RF-02-60`, `RF-04-41`; design — decisão 3). Verificar que
      o cenário da recusa do Guerreiro(a) em `estado_da_partida` passa em
      `tests/test_quiz_rota.py`.

## 3. Núcleo — testes

- [x] 3.1 Em `backend/tests/test_quiz.py`, cobrir a descoberta e o resultado: equipe derivada com
      o Guerreiro(a) em mais de uma equipe do encontro, quem não disputa recebendo equipe nula,
      aula sem partida devolvendo lista vazia, resultado oculto antes da liberação e completo
      depois, e liberação que não credita (`RF-04-41`, `RF-04-42`, `RF-04-44`).
- [x] 3.2 Em `backend/tests/test_quiz_rota.py`, cobrir as duas portas: `GET /aulas/{id}/partidas`
      pelo Guerreiro(a) e o 403 de Mestre nela (Admin bypassa por `Operacao.tudo`, como em toda
      a matriz — a spec da change foi corrigida), e o 403 do Guerreiro(a) em
      `GET /partidas-de-quiz/{id}` (`RF-04-41`, `RF-04-42`).

## 4. App 01 — cliente e caminho

- [x] 4.1 Em `apps/app-01-aula-presencial/src/api/`, escrever o cliente do quiz — partidas da
      aula, pergunta no ar e envio da resposta —, no padrão dos clientes já existentes
      (`RF-04-41`, `RF-04-43`). Verificar pelos testes do módulo em 5.1.
- [x] 4.2 Em `src/inicio/TelaInicial.tsx`, acrescentar o caminho do quiz, sempre presente na
      sessão de trabalho e independente do momento de troca, levando à entrada do Guerreiro(a)
      quando não houver sessão dele aberta (`RF-04-01`, `RF-04-41`; design — decisão 5).
      Verificar por `vitest run src/inicio`.

## 5. App 01 — a tela da partida

- [x] 5.1 Criar `src/quiz/TelaDaPartida.tsx`: abertura relendo as partidas da aula, equipe vinda
      do núcleo sem escolha em tela, vínculo partida–equipe guardado em `sessionStorage` sob
      `app-01:quiz:partida` e apagado ao voltar ao início, e a frase de saída quando não há
      partida ou o Guerreiro(a) não disputa (`RF-04-41`, `RF-04-42`; design — decisões 1 e 4).
- [x] 5.2 Implementar a sondagem a cada 2 segundos da pergunta no ar, com a espera entre
      perguntas, o aviso de perda de contato que mantém a tela e a volta à pergunta corrente
      (`RF-04-41`, `RF-04-58`; design — decisão 7).
- [x] 5.3 Implementar o envio da resposta — uma por equipe e pergunta, segunda tentativa recusada
      antes de enviar, recusa do núcleo por outro aparelho da equipe apresentada com a mesma
      mensagem, e a alternativa escolhida mantida em tela até a pergunta seguinte (`RF-04-43`).
- [x] 5.4 Implementar a exibição do resultado liberado — alternativa correta, se a equipe acertou
      e qual chegou primeiro —, oculto antes da liberação e sem pontuação da partida em tela
      alguma (`RF-04-44`).
- [x] 5.5 Implementar o comportamento sem rede: pergunta carregada segue legível, resposta
      apresentada como indisponível e nada enfileirado para envio posterior (`RF-04-58`;
      design — decisão 6).

## 6. App 01 — testes

- [x] 6.1 Em `src/quiz/quiz.test.tsx`, cobrir a abertura e a partida: entrada sem sessão levando
      ao nick e imagem, equipe nunca escolhida em tela, ausência de partida explicada, atendimento
      seguinte sem herdar equipe, pergunta aparecendo por sondagem e rede caída no meio da
      pergunta que não tira a equipe da partida (`RF-04-41`, `RF-04-42`, `RF-04-58`).
- [x] 6.2 No mesmo arquivo, cobrir resposta e resultado: escolha mantida em tela, segunda
      tentativa recusada antes de enviar, recusa do núcleo por outro aparelho tratada como "a
      equipe já respondeu", resultado oculto antes da liberação e completo depois, nenhuma
      pontuação em tela, e resposta indisponível sem rede sem enfileirar (`RF-04-43`, `RF-04-44`,
      `RF-04-58`).
- [x] 6.3 Em `src/inicio/inicio.test.tsx`, cobrir o quarto caminho: presente com o momento de
      troca fechado e levando à entrada do Guerreiro(a) sem sessão aberta (`RF-04-01`,
      `RF-04-41`).

## 7. Documentação

- [x] 7.1 Corrigir no `docs/prds/prd-04-aula-presencial.md` o que contraria o documento 05 §5: a
      §3.2 deixa de excluir o vínculo aparelho–equipe como sendo da App 03, a jornada 5.9 item 1
      deixa de atribuir o vínculo ao Mestre na App 03 e o `RF-04-41` (a tarefa citava `RF-04-42`
      por engano — é o `RF-04-41` que fala em "aparelho vinculado") deixa de falar em aparelho
      vinculado — o vínculo é estado do próprio aparelho. Registrar a resolução do conflito em
      `docs/09-topicos-em-aberto-e-sugestoes.md` §1 (fundador, 2026-08-25) e a fatia em
      `docs/prds/index.md`. O documento 05, o documento 99 e a `nav` do `mkdocs.yml` não mudam —
      nenhum arquivo nasce em `docs/` e nenhuma relação entre documentos muda.
