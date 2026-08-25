## Context

O motor da partida está em `backend/src/nucleo/quiz/regra.py` e a spec consolidada em
`openspec/specs/quiz-ao-vivo/spec.md` — `abrir_partida`, `registrar_resposta`,
`anular_pergunta` e `encerrar_partida`, todos testados e sem rota. O que falta desenhar é o
**estado da pergunta no ar**, que não existe no modelo, e o contrato de leitura que a sondagem
consome. Ver `proposal.md` — Why.

## Goals / Non-Goals

**Goals:**

- Dar porta HTTP às quatro operações sem tocar na regra já testada de nenhuma delas.
- Gravar a pergunta no ar de modo que a partida fique legível depois: qual caiu, em que ordem
  e quando.
- Servir a leitura da partida barata o bastante para ser sondada a cada 2 segundos.

**Non-Goals:**

- A tela do aparelho da equipe na App 01 — é a fatia B; aqui as duas rotas dela saem testadas
  por contrato.
- O painel do dia, que herda a mesma decisão de sondagem mas é outro recorte do PRD-02.

## Decisions

**1. A pergunta no ar é tabela própria, não coluna na partida.** Nasce `PerguntaNaPartida`
com partida, pergunta, ordem, momento de entrada e momento da liberação do resultado. A
pergunta no ar é a de maior ordem. _Alternativa descartada:_ duas colunas anuláveis na
`PartidaDeQuiz` — perde o histórico que a spec exige ("preservando a ordem e o momento") e
não teria onde marcar a liberação de cada pergunta.

**2. A resposta que chega depois da virada continua aceita.** `registrar_resposta` não ganha
recusa por pergunta fora do ar: a decisão 6 já arquivada mantém a pergunta anulada recebendo
resposta enquanto a partida está aberta, e o PRD não declara essa recusa. Quem garante que a
equipe responde à pergunta certa é a App 01, que só exibe a que está no ar. _Alternativa
descartada:_ recusar a resposta de pergunta que saiu do ar — seria regra nova, fora do PRD.

**3. Duas leituras, públicos diferentes.** `GET /v1/partidas-de-quiz/{id}` serve quem conduz,
com a contagem de quem já respondeu; `GET /v1/partidas-de-quiz/{id}/pergunta` serve o aparelho
da equipe. Nenhuma das duas devolve a **alternativa correta** enquanto o resultado não é
liberado — o esquema de saída da partida é próprio, não reaproveita `PerguntaDeQuizSaida`, que
é do banco do Mestre e traz a correta por ser tela de autoria. _Alternativa descartada:_ uma
leitura só com o conteúdo variando por papel — esconde o vazamento dentro de um `if`.

**4. A leitura usa a mesma operação da escrita.** `conducao_do_quiz_ao_vivo_das_suas_aulas`
entra no conjunto `le` do Mestre, e `resposta_de_quiz_da_equipe` no do Guerreiro(a). Não
nasce operação nova: é a mesma, do lado da leitura. A matriz do PRD-01 §4 registra as duas
leituras. _Alternativa descartada:_ reaproveitar `painel_do_dia_na_app_03` e
`equipes_da_aula_em_andamento` — a partida não é o painel nem a equipe.

**5. As rotas seguem o PRD-02 §9 e o PRD-04 §9, e o §9 do PRD-02 ganha as três que faltam.**
Abertura, _start_ e encerramento já estão declarados lá com esses nomes; anulação
(`RF-02-72`), liberação do resultado (`RF-04-44`) e leitura do estado não estavam, embora os
requisitos existam. É correção de tabela de rotas, não requisito novo — mesmo precedente da
rota de desfecho da chave, na quarta fatia.

**6. A App 03 monta a abertura com o que já existe.** `GET /v1/minhas-turmas` dá as aulas e as
atividades do Mestre em sessão, `GET /v1/aulas/{id}/equipes` dá as equipes formadas na App 01
e `GET /v1/perguntas/minhas`, filtrado por trilha e missão, dá o banco. Nenhuma rota de
leitura nova para a tela de abertura.

**7. A sondagem é inteira do cliente.** Nada no servidor guarda assinante, sessão longa ou
fila. O intervalo — 2 segundos na partida — é constante da App 03 e da App 01, e o núcleo não
sabe que está sendo sondado.

## Risks / Trade-offs

- **Sondagem a 2s com o Cloud Run em um contêiner só** → a leitura é uma consulta por
  identificador, sem `N+1`: partida, pergunta no ar e contagem de respostas em consultas
  diretas. Com ~6 aparelhos por turma, são ~3 requisições por segundo, e o contêiner já está
  quente pela própria aula.
- **A alternativa correta trafega na tela do Mestre antes da liberação** → é a tela de quem
  conduz, e ela já alcança o banco inteiro por `GET /v1/perguntas/minhas`; o que a fatia
  garante é que a rota do aparelho da equipe nunca a devolva antes da liberação.
- **Virar a pergunta enquanto uma equipe responde** → a resposta atrasada é gravada para a
  pergunta anterior (decisão 2) e entra na apuração dela; quem conduz vê a contagem subir
  depois da virada, o que a tela precisa tolerar sem parecer erro.

## Migration Plan

Uma migração Alembic cria `pergunta_na_partida`, com unicidade em (partida, pergunta) e em
(partida, ordem). A tabela nasce vazia e nenhuma partida anterior existe fora de teste, então
não há retrocompatibilidade a manter. As colunas e as quatro operações já existentes não são
alteradas.
