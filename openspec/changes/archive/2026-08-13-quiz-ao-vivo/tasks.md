## 1. Modelo de dados e migração

- [x] 1.1 Criar o modelo `PerguntaDeQuiz` em `backend/src/nucleo/quiz/modelo.py`, com autoria
      (`ComAutoria`), enunciado, as quatro alternativas e a indicação da correta, e
      `CheckConstraint` que prende a correta ao intervalo das quatro (`RF-01-36`, `RF-01-03`).
- [x] 1.2 Criar o modelo `PartidaDeQuiz` com `aula_id`, `atividade_id`, situação fechada em
      `aberta`/`encerrada` e a autoria da abertura e do encerramento. **Sem `trilha_id`**: a
      trilha é derivada de `atividade → missao → trilha` (design — decisão 3).
- [x] 1.3 Criar o modelo `EquipeNaPartida`, a lista de equipes disputantes fixada na abertura,
      com `UniqueConstraint` por `(partida, equipe)` (`RF-01-39`, design — decisão 4).
- [x] 1.4 Criar o modelo `PerguntaAnuladaNaPartida`, o par (partida, pergunta) com autoria e
      `UniqueConstraint` por `(partida, pergunta)` — é ele que impede a pergunta anulada de
      creditar quando a resposta chega depois da anulação (`RN-01-38`, design — decisão 6).
- [x] 1.5 Criar o modelo `RespostaDeQuiz` com partida, pergunta, equipe, alternativa escolhida,
      `momento_de_chegada` carimbado pelo servidor e `anulada_em`, a projeção consultável da
      anulação, com `UniqueConstraint` por `(partida, pergunta, equipe)` — é ela que torna o
      reenvio inofensivo (`RF-01-36`, design — Migration Plan).
- [x] 1.6 Escrever a décima migração Alembic na ordem do design — Migration Plan: criar
      `pergunta_de_quiz`, `partida_de_quiz`, `equipe_na_partida`,
      `pergunta_anulada_na_partida` e `resposta_de_quiz`, com o `downgrade` derrubando as
      cinco. Nenhuma tabela existente é alterada.

## 2. Pergunta de quiz

- [x] 2.1 Implementar o cadastro da pergunta restrito ao Mestre e ao Admin pela matriz de
      permissões, gravando autoria, data e hora (`RF-01-36`, `RF-01-03`, `RF-01-16`).
- [x] 2.2 Implementar a recusa com 422, indicando o campo em falta, da pergunta com número de
      alternativas diferente de quatro e da pergunta sem alternativa correta declarada
      (`RF-01-36`, `RF-01-27`).
- [x] 2.3 Verificar: pergunta com quatro alternativas e uma correta grava com autoria; pergunta
      com três alternativas recebe 422; pergunta sem correta recebe 422; nenhum campo de
      tempo-limite existe no modelo (`RF-01-36`, specs — pergunta de múltipla escolha).

## 3. Abertura da partida

- [x] 3.1 Implementar a abertura da partida restrita à operação
      `conducao_do_quiz_ao_vivo_das_suas_aulas` do Mestre que ministra aquela aula e à operação
      `tudo` do Admin, recusando com 403 o Mestre de outra aula (`RF-01-17`, `RF-01-16`,
      `RF-01-03`).
- [x] 3.2 Implementar a recusa com 422 da partida sem atividade declarada e da partida cuja
      atividade não tenha natureza de competição ao vivo (`RF-01-21`, specs — partida sobre
      atividade da trilha).
- [x] 3.3 Implementar a materialização das equipes disputantes na abertura, recusando com 422
      quando a interseção de integrantes entre quaisquer duas delas não for vazia (`RF-01-39`,
      design — decisão 4).
- [x] 3.4 Implementar a recusa com 422 da equipe da trilha como disputante: só equipe da aula,
      e da aula da partida (`RF-01-37`, `RF-01-39`, `RF-01-18`).
- [x] 3.5 Verificar: Mestre da aula abre com autoria gravada; Mestre de outra aula recebe 403;
      Admin abre em qualquer aula; partida sem atividade recebe 422; duas partidas de trilhas
      diferentes convivem na mesma aula; equipes com integrante em comum recebem 422; equipe da
      trilha recebe 422 (`RF-01-17`, `RF-01-21`, `RF-01-39`).

## 4. Resposta da equipe

- [x] 4.1 Implementar o registro da resposta pela operação `resposta_de_quiz_da_equipe` do
      Guerreiro(a), gravando a equipe, a alternativa e a autoria de quem enviou (`RF-01-36`,
      `RF-01-03`, `RF-01-16`).
- [x] 4.2 Implementar o carimbo de `momento_de_chegada` **pelo núcleo**, ignorando qualquer
      instante declarado pelo chamador (`RF-01-36`, design — decisão 2).
- [x] 4.3 Implementar a idempotência do reenvio: achando resposta já gravada para
      `(partida, pergunta, equipe)`, devolver a existente sem duplicar nem alterar o momento;
      recusar com 422 a segunda alternativa diferente (`RF-01-36`, PRD-01 §10).
- [x] 4.4 Implementar a recusa com 422 da resposta a pergunta de partida já encerrada e da
      resposta de equipe que não disputa aquela partida (`RF-01-36`, `RF-01-39`).
- [x] 4.5 Verificar: resposta grava equipe, alternativa e momento carimbado; momento declarado
      pelo chamador é ignorado; reenvio mantém um registro e o momento da primeira; segunda
      alternativa recebe 422; resposta a partida encerrada recebe 422 (`RF-01-36`).

## 5. Anulação de pergunta

- [x] 5.1 Implementar a anulação de pergunta pelo Mestre que conduz a partida ou por um Admin,
      gravando `PerguntaAnuladaNaPartida` com autoria, data e hora (`RF-01-03`, `RF-01-16`,
      documento 05 §5, design — decisão 6).
- [x] 5.2 Implementar a recusa com 422 da anulação em partida já encerrada — é o que mantém
      `RN-01-38`, já que a partida encerrada creditou (`RN-01-38`, design — decisão 1).
- [x] 5.3 Implementar a marca de pergunta anulada nas respostas já gravadas e na resposta que
      chegar depois da anulação, que seguem consultáveis (`RF-01-36`, design — decisão 6).
- [x] 5.4 Verificar: pergunta anulada não credita a nenhuma equipe, inclusive quando a resposta
      chega depois da anulação; nenhum saldo de ponto regular diminui em consequência da
      anulação; respostas seguem consultáveis marcadas; anulação depois do encerramento recebe
      422 (`RN-01-38`).

## 6. Apuração e crédito no encerramento

- [x] 6.1 Implementar o encerramento da partida aceito apenas na transição `aberta → encerrada`,
      recusando com 422 a segunda chamada sem tocar em `PontoRegular` (design — decisão 7).
- [x] 6.2 Implementar a apuração por equipe sobre as perguntas **não anuladas**: 1 por acerto e
      1 de bônus à primeira a acertar cada pergunta, pela ordenação
      `(momento_de_chegada, id)` (`RF-01-36`, `RF-01-21`, design — decisões 1 e 2).
- [x] 6.3 Implementar o teto de 10 pontos por partida, aplicado **antes** do crédito
      (`RF-01-21`, documento 11 §5).
- [x] 6.4 Implementar o crédito do valor apurado **integral a cada integrante** da equipe, na
      trilha derivada da atividade, chamando `creditar_ponto_regular` — o mesmo ponto de entrada
      que `creditar_pontuacao_da_criacao_original` usa (`RF-01-21`, `RN-01-42`, design —
      decisão 5).
- [x] 6.5 Implementar a apuração parcial como **leitura**, para o placar ao vivo da App 03, sem
      creditar nada (`RF-01-21`, design — Risks).
- [x] 6.6 Verificar: acerto credita 1 por integrante; a primeira a acertar recebe 2 e a outra 1;
      apuração de 13 credita 10; equipes de tamanhos diferentes recebem o mesmo total por
      integrante, sem rateio; erro não credita nem reduz saldo; pergunta anulada fica fora da
      apuração; partida de trilha 1 credita à trilha 1 (`RF-01-21`, `RF-01-36`, `RN-01-38`).
- [x] 6.7 Verificar que o gatilho de `PontoRegular` continua recusando débito com o quiz no
      caminho, no ORM e fora dele (`RN-01-38`, `RF-01-57`).

## 7. Esteira do backend

- [x] 7.1 Rodar `ruff format --check`, `ruff check` e `pytest` com a cobertura publicada no log,
      sem limiar que bloqueie. A fatia não cria pasta de topo, então não nasce workflow novo:
      `backend-ci.yml` já cobre `backend/**`.

## 8. Documentação

- [x] 8.1 Conferir que as duas decisões seguem registradas onde foram gravadas antes desta
      change — a plataforma não controla aparelhos (documentos 03 §4, 05 §5, 09, 11 §5.1 e 99
      §3) e o Quiz ao Vivo é uma atividade da trilha (documentos 05 §5 e 09) — e que a
      implementação não divergiu de nenhum desses textos.
- [x] 8.2 Atualizar `docs/prds/index.md` se a situação do PRD-01 mudar ao fim desta fatia.
      Nenhum arquivo novo em `docs/`, e portanto nenhuma entrada nova na `nav` do `mkdocs.yml`.
- [x] 8.3 Rodar `npm run fix`, `npm run lint` e `mkdocs build --strict` antes de abrir o PR.
