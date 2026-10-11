# Tasks

## 1. Cadastro da atividade avulsa com a aula (núcleo)

- [x] 1.1 Em `backend/src/nucleo/atividades/regra.py`, exigir a **aula** no cadastro da avulsa,
      conferir que existe e não está cancelada, e restringir o **formato** a presencial —
      recusando com 422 e nomeando o campo em falta (`RF-02-29`)
- [x] 1.2 Em `backend/src/nucleo/atividades/rotas.py`, acrescentar `aula_id` à entrada do
      cadastro, recusar campo de comunidade pelo `extra="forbid"` que o modelo já aplica, e
      devolver a aula na saída (`RF-02-29`)
- [x] 1.3 Em `atividades/regra.py` e `atividades/rotas.py`, dar à listagem o filtro opcional
      por aula, mantendo a exigência de Admin, e devolver lista vazia para aula sem avulsa
      (`RF-02-29`, `RF-02-112`)
- [x] 1.4 Cobrir o grupo em `backend/tests/test_atividade_avulsa.py` e
      `test_atividade_avulsa_rota.py`: cadastro com aula, recusa sem aula, aula cancelada,
      aula inexistente, formato on-line, campo de comunidade recusado, e os quatro cenários do
      filtro por aula — incluindo o 403 de quem não é Admin (`RF-02-29`, `RF-02-112`)

## 2. Lançamento da avulsa pelo ato por atividade (núcleo)

- [x] 2.1 Em `backend/src/nucleo/resultados/regra.py`, guardar o nulo de `missao_id` em
      `lancar_resultados_da_atividade`: sem missão, conferir Admin em vez de posse de trilha,
      no mesmo molde que `registrar_resultado` já usa — o 500 vira 403 para Mestre e segue para
      Admin (`RF-02-112`)
- [x] 2.2 Na mesma regra, aceitar a **equipe da aula** como alternativa à lista de
      participantes, recusando com 422 a ausência das duas e a presença simultânea; expandir a
      equipe em um Resultado por integrante, com o desfecho e a produção da equipe
      (`RF-02-112`, `RN-02-32`)
- [x] 2.3 Na expansão da equipe, pular integrante sem `Presenca` não anulada naquela aula e
      integrante que não é Guerreiro(a), e devolver quem ficou de fora; recusar com 422 a
      equipe sem nenhum presente (`RN-02-32`, `RN-02-33`)
- [x] 2.4 Na mesma regra, recusar com 422 a forma incoerente com a modalidade — por equipe na
      individual, por participante na em equipe e na em equipe com familiar (`RN-02-33`)
- [x] 2.5 Em `resultados/regra.py`, recusar com 422 o segundo Resultado do mesmo par
      (Guerreiro(a), atividade), antes de gravar qualquer um da lista (`RN-02-33`)
- [x] 2.6 Em `backend/src/nucleo/resultados/modelo.py`, acrescentar índice único de
      `(guerreiro_id, atividade_id)` e gerar a migração Alembic; a migração **confere
      duplicatas antes** e, havendo, para sem apagar Resultado — relatar ao fundador, como o
      `design.md` prevê (`RN-02-33`)
- [x] 2.7 Em `resultados/rotas.py`, acrescentar `equipe_id` à entrada do ato por atividade e
      devolver na resposta quem ficou de fora por falta de presença (`RF-02-112`, `RN-02-32`)
- [x] 2.8 Cobrir o grupo em `backend/tests/test_lancamento_por_atividade.py`: avulsa lançada
      por Admin sem tocar reserva nem situação da aula, dois lançamentos na mesma aula, 403 do
      Mestre, lançamento por equipe com valor integral a cada presente, presença anulada,
      familiar fora, equipe vazia, as duas incoerências de modalidade e o Resultado repetido
      (`RF-02-112`, `RN-02-32`, `RN-02-33`)

## 3. App 03 — cadastro e área Lançamentos

- [x] 3.1 Em `apps/app-03-gestao/src/atividades/`, pôr no formulário a escolha de **comunidade**
      — que estreita a lista de aulas e não é enviada ao núcleo — e a de **aula**, sem as
      canceladas, fixar o formato em presencial com a linha que explica, e enviar `aula_id`
      (`RF-02-29`)
- [x] 3.2 Em `apps/app-03-gestao/src/atividades/api.ts`, acrescentar o filtro por aula e o
      `aula_id` à entrada e à saída do cadastro (`RF-02-29`, `RF-02-112`)
- [x] 3.3 Em `apps/app-03-gestao/src/lancamentos/`, acrescentar o bloco das atividades avulsas
      da aula vigente, com a frase de que esse lançamento não dá baixa nem passa a aula a
      realizada, e a ausência dita em uma frase quando a aula não tem avulsa (`RF-02-112`)
- [x] 3.4 No mesmo bloco, oferecer a forma de lançamento que a modalidade admite — por aluno ou
      por equipe da aula, nunca as duas —, apresentar as equipes pelo nome, dizer quem ficou de
      fora antes de enviar, impedir o envio sem desfecho e traduzir as recusas do núcleo em
      linguagem simples (`RF-02-112`, `RN-02-32`, `RN-02-33`)
- [x] 3.5 Cobrir o grupo em `apps/app-03-gestao/src/atividades/atividades.test.tsx` e
      `src/lancamentos/lancamentos.test.tsx`: comunidade estreitando as aulas, falta de aula
      apontada no campo, ausência de escolha de formato, as avulsas listadas na área, a forma
      por modalidade, o aviso de quem ficou de fora e a recusa do Resultado repetido em
      linguagem simples (`RF-02-29`, `RF-02-112`, `RN-02-32`, `RN-02-33`)

## 4. Documentação

- [x] 4.1 Marcar a fatia 25 do PRD-02 como `implementado` em
      `openspec/cronograma-de-fatias.md`, com o slug desta change na coluna Recorte. O
      documento-fonte (11 §4), o documento 09, o PRD-02 e o documento 99 §8 **já foram
      atualizados** no commit `21b64dc` deste mesmo PR; `docs/prds/index.md` não muda, porque a
      situação do PRD-02 é a mesma, e a `nav` do `mkdocs.yml` não muda, porque nenhum arquivo
      nasceu em `docs/`
