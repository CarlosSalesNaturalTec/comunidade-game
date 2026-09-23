# Tasks

## 1. Núcleo — a presença própria se lê

- [ ] 1.1 `RF-04-68`, `RN-04-40`: criar `GET /v1/aulas/{id}/presencas/eu` em
      `backend/src/nucleo/aulas/rotas.py`, sob a sessão do Guerreiro(a) e a operação
      `seus_dados`, devolvendo 200 com a presença **não anulada** daquela aula — momento do
      fato e modo de comprovação — ou 200 dizendo que não há; aula inexistente responde 404.
      O Guerreiro(a) vem do contexto da sessão, nunca do cliente (invariante 15).
      Verificação: a rota aparece no OpenAPI e os testes da tarefa 3.1 passam.

## 2. Núcleo — formar equipe da aula exige presença

- [ ] 2.1 `RF-04-68`, `RN-04-40`: acrescentar em `backend/src/nucleo/erros.py` a recusa 422 com
      código próprio para a falta de presença do encontro, no padrão de
      `NickDeGuerreiroEmUsoNoEncontro`. Verificação: o código aparece no corpo único da recusa
      nos testes da tarefa 3.2.
- [ ] 2.2 `RF-04-68`, `RN-04-40`: em `backend/src/nucleo/equipes/regra.py`, `criar_equipe` (com
      aula) e `entrar_na_equipe` (equipe cujo vínculo é aula) recusam quem não tem presença não
      anulada naquela aula; sair da equipe e renomear seguem sem exigir presença, e a equipe da
      trilha segue sem a guarda (design — decisão 4). Verificação: os testes da tarefa 3.2
      passam.

## 3. Testes do núcleo

- [ ] 3.1 `RF-04-68`: testes da leitura da presença própria — tem presença, não tem, presença
      anulada lida como ausência, leitura sempre da própria persona e aula inexistente em 404
      (cenários da spec `aula-e-presenca`).
- [ ] 3.2 `RF-04-68`, `RN-04-40`: testes da guarda em `backend/tests/test_equipe_rota.py` e
      `test_equipe.py` — sem presença recusa criar e entrar com 422 e código próprio, com
      presença corre como antes, presença anulada barra, sair e renomear passam sem presença e
      a equipe da trilha não é barrada (cenários da spec `equipe`).

## 4. App 01 — a entrada sabe por qual caminho veio

- [ ] 4.1 `RF-04-68`: em `apps/app-01-aula-presencial/src/api/presencas.ts`, a leitura da
      presença do Guerreiro(a) em sessão na aula em curso. Verificação: usada em 4.3 e coberta
      pelos testes da tarefa 5.
- [ ] 4.2 `RF-04-67`, `RF-04-18`, `RF-04-21`: `TelaDeEntradaDoGuerreiro` passa a receber o
      caminho que a chamou e **só registra presença** no caminho `presenca` — no reconhecimento
      e na confirmação por PIN. Fora dele, abre a sessão e devolve o controle sem tocar em
      presença, e a fila local segue exclusiva do caminho `presenca`. Verificação: os testes da
      tarefa 5.1 passam.
- [ ] 4.3 `RF-04-01`, `RF-04-67`, `RF-04-68`, `RN-04-40`: `TelaInicial` passa a oferecer
      Onboarding, Presença e Equipes — o estado `Caminho` troca `"trilhas"` por `"presenca"` e
      `"equipes"` —, termina o caminho Presença na volta ao início e, nos caminhos Equipes,
      Quiz e Troca, confere a presença assim que a sessão abre: sem ela, encerra a sessão, diz
      em linguagem simples o que falta e oferece o caminho Presença. A recusa do núcleo por
      falta de presença aparece como o que é, nunca como recusa do rosto (`RN-04-36`).
      Verificação: os testes da tarefa 5.2 passam.

## 5. Testes do App 01

- [ ] 5.1 `RF-04-67`, `RF-04-18`, `RF-04-21`: em `entrada/entrada.test.tsx`, o caminho
      `presenca` registra a presença por reconhecimento e por confirmação, e os demais caminhos
      abrem a sessão **sem** nenhuma requisição de presença (cenários "Nick e imagem conferem",
      "Nos demais caminhos a entrada não registra presença" e "A confirmação fora do caminho da
      presença não registra presença").
- [ ] 5.2 `RF-04-01`, `RF-04-67`, `RF-04-68`: em `inicio/inicio.test.tsx`, os três caminhos na
      tela, Equipes sem sessão levando à entrada, o caminho da presença terminando na volta ao
      início, a recusa por falta de presença em Equipes, Quiz e Troca com a oferta do caminho
      Presença, e a volta às equipes passando para quem já tem presença (cenários dos dois
      requisitos novos da spec `aplicacao-da-aula-presencial`).
- [ ] 5.3 Ajustar os testes que hoje entram pelas equipes pelo caminho antigo —
      `equipes/equipes.test.tsx`, `quiz/quiz.test.tsx`, `troca/troca.test.tsx` e
      `trilhas/trilhas.test.tsx` — para o caminho novo, sem afrouxar asserção alguma.
      Verificação: `vitest run` do App 01 verde.

## 6. Documentação

- [ ] 6.1 Decisão nova do fundador de 2026-09-23 (quiz e troca também exigem presença):
      acrescentar a frase ao documento 03 §§3 e 4, ampliar a linha da decisão no documento 09
      §1 e ampliar o enunciado de `RN-04-40` no PRD-04 §7, com a linha correspondente nas
      jornadas §§5.9 e 5.10. Verificação: `npm run lint` e `mkdocs build --strict`.
- [ ] 6.2 Marcar a fatia 18 do PRD-04 como implementada em
      `openspec/cronograma-de-fatias.md`, trocando o recorte previsto pelo slug da change.
      `docs/prds/index.md`, o documento 99 e a `nav` do `mkdocs.yml` não mudam: nenhum arquivo
      novo nasce em `docs/`, nenhuma relação entre documentos muda e a situação do PRD-04
      segue a mesma.
