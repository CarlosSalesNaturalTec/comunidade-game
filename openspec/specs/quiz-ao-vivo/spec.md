## Purpose

A partida do Quiz ao Vivo no encontro presencial — a pergunta de múltipla escolha do Mestre
curador, a disputa entre as equipes de uma mesma trilha e a resposta de cada equipe com o
momento em que chegou ao servidor, que é o critério de desempate do bônus.

## Requirements

### Requirement: A pergunta de quiz é de múltipla escolha com quatro alternativas

O núcleo SHALL manter a **pergunta de quiz**, de autoria de um **Mestre**, com enunciado,
**exatamente quatro alternativas**, a indicação de qual delas é a correta e o **vínculo com a
missão a que ela se refere**, de onde a trilha decorre. A pergunta SHALL recusar número de
alternativas diferente de quatro, SHALL recusar o cadastro sem alternativa correta declarada e
SHALL recusar o cadastro sem a missão declarada. O núcleo NÃO SHALL guardar tempo-limite de
resposta: o ritmo é de quem conduz a partida. A pergunta NÃO SHALL ter situação: ela nasce
disponível e assim permanece — a anulação é da partida, nunca dela, e a mesma pergunta serve a
partidas diferentes. (`RF-09-36`, `RF-09-37`, `RF-09-38`, `RF-09-39`, `RF-01-36`, `RF-01-03`,
documento 05 §5, documento 09)

#### Scenario: Pergunta com quatro alternativas e uma correta é aceita

- **WHEN** um Mestre cadastra uma pergunta com enunciado, quatro alternativas, a correta
  indicada e a missão a que ela se refere
- **THEN** o núcleo grava a pergunta com a autoria, a data e a hora do cadastro, e com a
  trilha decorrente da missão

#### Scenario: Pergunta com três alternativas é recusada

- **WHEN** um Mestre tenta cadastrar uma pergunta com três alternativas
- **THEN** o núcleo responde 422 e nenhuma pergunta é gravada

#### Scenario: Pergunta sem alternativa correta é recusada

- **WHEN** um Mestre tenta cadastrar uma pergunta sem indicar qual alternativa é a correta
- **THEN** o núcleo responde 422 e nenhuma pergunta é gravada

#### Scenario: Pergunta sem missão declarada é recusada

- **WHEN** um Mestre tenta cadastrar uma pergunta sem declarar a missão a que ela se refere
- **THEN** o núcleo responde 422 e nenhuma pergunta é gravada

### Requirement: O Mestre lê o próprio banco de perguntas, filtrado por trilha e missão

O núcleo SHALL servir ao **Mestre em sessão** as perguntas de que ele é autor, e SHALL aceitar
o filtro por **trilha** e por **missão** para que ele monte o banco de uma aula. A leitura SHALL
devolver somente as perguntas do próprio Mestre: o banco de um Mestre NÃO SHALL aparecer para
outro. A leitura SHALL ser paginada pelas convenções do núcleo. (`RF-09-40`, `RF-09-41`,
`RF-01-16`)

#### Scenario: Mestre lê o próprio banco

- **WHEN** um Mestre consulta o seu banco de perguntas
- **THEN** o núcleo devolve, paginadas, as perguntas de que ele é autor, com enunciado,
  alternativas, alternativa correta, missão e trilha

#### Scenario: Filtro por missão devolve só as perguntas daquela missão

- **WHEN** um Mestre consulta o seu banco filtrando por uma missão
- **THEN** o núcleo devolve apenas as perguntas vinculadas àquela missão

#### Scenario: Filtro por trilha devolve as perguntas de todas as missões dela

- **WHEN** um Mestre consulta o seu banco filtrando por uma trilha
- **THEN** o núcleo devolve as perguntas vinculadas a qualquer missão daquela trilha

#### Scenario: O banco de um Mestre não aparece para outro

- **WHEN** um Mestre consulta o seu banco e existem perguntas cadastradas por outro Mestre
- **THEN** o núcleo devolve apenas as perguntas do Mestre em sessão

#### Scenario: Guerreiro(a) não alcança o banco de perguntas

- **WHEN** um Guerreiro(a) tenta ler o banco de perguntas
- **THEN** o núcleo responde 403 e nenhuma pergunta é devolvida

### Requirement: A partida corre sobre uma atividade da trilha, dentro de uma aula

O núcleo SHALL manter a **partida de quiz** vinculada a **uma aula** e a **uma atividade** de
natureza competição ao vivo, e SHALL derivar dessa atividade a **missão e a trilha** da
partida. A aula NÃO SHALL ganhar vínculo com trilha: o encontro é assíncrono e cada equipe
avança na sua. (`RF-01-21`, `RN-01-42`, documento 05 §§4, 5, documento 11 §4)

#### Scenario: Partida herda a trilha da atividade

- **WHEN** uma partida é aberta sobre uma atividade de uma missão da trilha 1
- **THEN** o núcleo registra a partida com a trilha 1 derivada da atividade, sem que a aula
  seja alterada

#### Scenario: Partida sem atividade é recusada

- **WHEN** alguém tenta abrir uma partida sem declarar a atividade sobre a qual ela corre
- **THEN** o núcleo responde 422 e nenhuma partida é aberta

#### Scenario: Duas partidas de trilhas diferentes convivem na mesma aula

- **WHEN** duas partidas são abertas na mesma aula, cada uma sobre uma atividade de uma trilha
  diferente
- **THEN** o núcleo registra as duas, cada qual com a sua trilha

### Requirement: A partida é conduzida pelo Mestre que ministra a aula ou por um Admin

O núcleo SHALL aceitar a abertura, a condução e o encerramento da partida apenas do **Mestre
que ministra aquela aula** ou de um **Admin**, conforme a matriz de permissões do PRD-01 §4, e
SHALL registrar autoria, data e hora de cada uma dessas escritas. Mestre que não ministra a
aula SHALL receber **403**. (`RF-01-17`, `RF-01-16`, `RF-01-03`, `RF-01-18`)

#### Scenario: Mestre da aula abre a partida

- **WHEN** o Mestre que ministra a aula abre uma partida nela
- **THEN** o núcleo grava a partida com a autoria dele, a data e a hora

#### Scenario: Mestre de outra aula é recusado

- **WHEN** um Mestre que não ministra aquela aula tenta abrir uma partida nela
- **THEN** o núcleo responde 403 e nenhuma partida é aberta

#### Scenario: Admin conduz a partida de qualquer aula

- **WHEN** um Admin abre uma partida numa aula que não ministra
- **THEN** o núcleo grava a partida com a autoria dele

### Requirement: O Guerreiro(a) disputa a partida por uma única equipe

O núcleo SHALL recusar, com **422**, a abertura de partida em que o mesmo Guerreiro(a) integre
**duas ou mais** das equipes disputantes. As equipes disputantes SHALL ser **equipes da aula**
daquela aula, nunca equipes da trilha. (`RF-01-39`, documento 03 §4.1, documento 02 §5)

#### Scenario: Guerreiro(a) em duas equipes disputantes recusa a partida

- **WHEN** alguém tenta abrir uma partida entre duas equipes da aula que têm um integrante em
  comum
- **THEN** o núcleo responde 422 e nenhuma partida é aberta

#### Scenario: Equipes sem integrante em comum abrem a partida

- **WHEN** uma partida é aberta entre três equipes da aula sem nenhum integrante em comum
- **THEN** o núcleo grava a partida com as três equipes disputantes

#### Scenario: Equipe da trilha não disputa partida

- **WHEN** alguém tenta abrir uma partida declarando uma equipe da trilha como disputante
- **THEN** o núcleo responde 422 e nenhuma partida é aberta

### Requirement: A resposta é da equipe e guarda o momento em que chegou ao servidor

O núcleo SHALL registrar a **resposta de quiz** por **equipe e pergunta** da partida, com a
alternativa escolhida e o **momento de chegada**. O momento SHALL ser carimbado **pelo núcleo,
na chegada** — nenhum momento declarado pela aplicação chamadora SHALL ser aceito como
critério de ordem. A resposta SHALL ser da **equipe**, não do aparelho de onde veio nem do
integrante que a enviou. (`RF-01-36`, `RF-01-03`, documento 05 §5)

#### Scenario: Resposta registra a equipe e o momento de chegada

- **WHEN** uma equipe responde a uma pergunta da partida
- **THEN** o núcleo grava a resposta com a equipe, a alternativa, o momento carimbado na
  chegada e a autoria de quem enviou

#### Scenario: Momento declarado pelo chamador é ignorado

- **WHEN** a chamada traz um momento de resposta declarado pela aplicação
- **THEN** o núcleo grava o momento que ele próprio carimbou na chegada, e a ordem da partida
  usa apenas esse

### Requirement: A resposta é única por equipe e pergunta

O núcleo SHALL aceitar **uma única** resposta por equipe e pergunta da partida. O reenvio da
mesma resposta, próprio de rede instável, NÃO SHALL duplicar o registro nem alterar o momento
de chegada já gravado. Resposta a pergunta de partida já encerrada SHALL ser recusada com
**422**. (`RF-01-36`, PRD-01 §10)

#### Scenario: Reenvio não duplica nem reordena

- **WHEN** a mesma equipe reenvia a resposta que já chegou, depois de uma queda de rede
- **THEN** o núcleo mantém um único registro, com o momento de chegada da primeira

#### Scenario: Segunda alternativa da mesma equipe é recusada

- **WHEN** uma equipe que já respondeu tenta responder a mesma pergunta com outra alternativa
- **THEN** o núcleo responde 422 e a resposta gravada não muda

#### Scenario: Resposta a partida encerrada é recusada

- **WHEN** uma equipe responde a uma pergunta de partida já encerrada
- **THEN** o núcleo responde 422 e nenhuma resposta é gravada

### Requirement: O Mestre anula a pergunta, e a anulada não credita ponto

O núcleo SHALL permitir ao **Mestre que conduz a partida**, ou a um **Admin**, **anular uma
pergunta** havendo contestação, com autoria, data e hora registradas. A anulação SHALL exigir a
partida **ainda aberta** e SHALL ser recusada com **422** depois do encerramento — é o que
mantém `RN-01-38`, já que a partida encerrada já creditou. A pergunta anulada NÃO SHALL
creditar ponto a nenhuma equipe, e a anulação NÃO SHALL debitar ponto regular de Guerreiro(a)
algum. As respostas já registradas SHALL continuar consultáveis, marcadas como de pergunta
anulada. (`RN-01-38`, `RF-01-03`, documento 05 §5)

#### Scenario: Pergunta anulada não credita ponto

- **WHEN** o Mestre que conduz anula uma pergunta da partida
- **THEN** nenhuma equipe recebe ponto por ela, e o registro guarda quem anulou, a data e a
  hora

#### Scenario: Anulação nunca debita ponto regular

- **WHEN** uma pergunta é anulada numa partida
- **THEN** o saldo de ponto regular de todos os Guerreiros e Guerreiras envolvidos permanece
  igual ou maior, nunca menor

#### Scenario: Resposta de pergunta anulada segue consultável

- **WHEN** uma pergunta com respostas já registradas é anulada
- **THEN** as respostas continuam consultáveis, marcadas como de pergunta anulada

#### Scenario: Anulação depois do encerramento é recusada

- **WHEN** o Mestre tenta anular uma pergunta de partida já encerrada
- **THEN** o núcleo responde 422, a pergunta segue valendo e nenhum ponto é debitado

### Requirement: A partida guarda qual pergunta está no ar

O núcleo SHALL registrar, na partida aberta, a **pergunta no ar** — aquela que quem conduz
deu o _start_ e que os aparelhos das equipes exibem. Pôr uma pergunta no ar SHALL substituir
a anterior, preservando a **ordem** em que cada uma caiu e o **momento** em que entrou, de
modo que a partida seja legível depois. A pergunta SHALL pertencer ao banco da **missão da
atividade** sobre a qual a partida corre; pergunta de outra missão SHALL ser recusada com
**422**. Partida encerrada NEVER SHALL receber pergunta no ar, e a tentativa SHALL receber
**422**. A operação SHALL ser aceita apenas de quem conduz a partida — o Mestre autor da
trilha ou um Admin —, com autoria, data e hora. (`RF-02-60`, `RF-09-41`, `RF-01-03`,
documento 05 §5)

#### Scenario: Quem conduz põe a primeira pergunta no ar

- **WHEN** quem conduz dá o _start_ de uma pergunta do banco da missão da atividade
- **THEN** o núcleo grava a pergunta como a que está no ar, com a ordem, o momento e a
  autoria

#### Scenario: A pergunta seguinte substitui a anterior

- **WHEN** quem conduz põe uma segunda pergunta no ar
- **THEN** a segunda passa a ser a pergunta no ar e a primeira segue registrada, com a ordem
  e o momento em que caiu

#### Scenario: Pergunta de outra missão é recusada

- **WHEN** quem conduz tenta pôr no ar uma pergunta de missão diferente da atividade da
  partida
- **THEN** o núcleo responde 422 e a pergunta no ar não muda

#### Scenario: Partida encerrada não recebe pergunta

- **WHEN** alguém tenta pôr uma pergunta no ar numa partida já encerrada
- **THEN** o núcleo responde 422 e nada é gravado

#### Scenario: Quem não conduz é recusado

- **WHEN** um Mestre que não conduz aquela partida tenta pôr uma pergunta no ar
- **THEN** o núcleo responde 403 e nada é gravado

### Requirement: O resultado da pergunta aparece quando quem conduz o libera

O núcleo SHALL manter a pergunta no ar com o **resultado ainda não liberado** até que quem
conduz o libere. Enquanto não liberado, nenhuma leitura SHALL devolver a alternativa correta
nem quem acertou. Liberado, o núcleo SHALL devolver a **alternativa correta**, as **equipes
que acertaram** e qual delas chegou **primeiro**, por ordem de chegada no servidor. Liberar o
resultado já liberado SHALL devolver o mesmo resultado, sem erro. A liberação NEVER SHALL
creditar pontuação: o crédito segue sendo do encerramento da partida. (`RF-04-44`,
`RF-02-62`, `RF-02-73`, documento 05 §5)

#### Scenario: Antes da liberação a alternativa correta não sai

- **WHEN** a pergunta está no ar com o resultado ainda não liberado
- **THEN** a leitura da partida devolve o enunciado e as quatro alternativas, sem a correta e
  sem quem acertou

#### Scenario: Liberado, o resultado sai com quem acertou e quem chegou primeiro

- **WHEN** quem conduz libera o resultado da pergunta no ar
- **THEN** a leitura da partida devolve a alternativa correta, as equipes que acertaram e a
  primeira delas por ordem de chegada no servidor

#### Scenario: Liberar de novo é idempotente

- **WHEN** quem conduz libera o resultado de uma pergunta cujo resultado já estava liberado
- **THEN** o núcleo devolve o mesmo resultado, sem erro e sem alterar o momento da liberação

#### Scenario: A liberação não credita

- **WHEN** o resultado de uma pergunta é liberado numa partida ainda aberta
- **THEN** nenhuma pontuação é lançada às equipes

### Requirement: A partida é lida por sondagem periódica

O núcleo SHALL expor a **leitura do estado da partida**, que devolve a situação, a pergunta
no ar, se o resultado dela já foi liberado e as equipes disputantes, **restrita a quem
conduz**. O aparelho da equipe SHALL acompanhar a partida pela leitura que é dele — a
pergunta no ar —, e NEVER SHALL alcançar a leitura do estado. Ambas SHALL ser alcançáveis a
qualquer momento da partida aberta e SHALL devolver sempre o estado corrente, de modo que o
aparelho que ficou fora do ar durante uma pergunta **volte na pergunta corrente**, sem travar
a partida nem recuperar a que perdeu. A sincronização em tempo real do Ciclo 01 é **sondagem
periódica**, e não conexão longa (documento 03 §1). (`RF-02-60`, `RF-04-41`, PRD-02 §12)

#### Scenario: A leitura devolve o estado corrente

- **WHEN** quem conduz lê o estado da partida
- **THEN** o núcleo devolve a situação, a pergunta no ar, se o resultado está liberado e as
  equipes disputantes

#### Scenario: O aparelho da equipe não alcança a leitura de quem conduz

- **WHEN** o Guerreiro(a) em sessão lê o estado da partida
- **THEN** o núcleo recusa com 403, e o aparelho acompanha a partida pela pergunta no ar

#### Scenario: O aparelho que caiu volta na pergunta corrente

- **WHEN** um aparelho fica fora do ar durante uma pergunta e volta depois de outra ter
  entrado no ar
- **THEN** a leitura devolve a pergunta corrente, e a partida corre sem ter sido travada

### Requirement: A condução da partida acontece por rotas próprias

O núcleo SHALL servir a condução da partida sob `/v1`, com a chave da aplicação e a
credencial da persona exigidas como em toda escrita: abertura em **`POST
/v1/partidas-de-quiz`**, _start_ da pergunta em **`POST /v1/partidas-de-quiz/{id}/perguntas`**,
liberação do resultado em **`POST /v1/partidas-de-quiz/{id}/resultado`**, anulação em **`POST
/v1/partidas-de-quiz/{id}/anulacoes`**, encerramento em **`POST
/v1/partidas-de-quiz/{id}/encerramento`** e leitura do estado em **`GET
/v1/partidas-de-quiz/{id}`**. Toda escrita SHALL ser aceita apenas de quem conduz a partida,
e SHALL responder **403** a Mestre que não conduz aquela aula. (`RF-02-59`, `RF-02-72`,
`RF-02-73`, `RF-09-41`, PRD-02 §§9, 12)

#### Scenario: Mestre abre a partida com a atividade e as equipes da aula

- **WHEN** o Mestre que conduz abre a partida declarando a aula, a atividade de competição ao
  vivo e as equipes disputantes
- **THEN** o núcleo grava a partida aberta com as equipes fixadas e a autoria dele

#### Scenario: Mestre de outra aula recebe 403

- **WHEN** um Mestre que não conduz aquela aula chama qualquer das escritas da partida
- **THEN** o núcleo responde 403 e nada é gravado

#### Scenario: A anulação da pergunta contestada tem rota

- **WHEN** quem conduz anula a pergunta contestada de uma partida aberta
- **THEN** o núcleo grava a anulação, marca as respostas já dadas e nenhuma delas credita

#### Scenario: O encerramento lança a pontuação

- **WHEN** quem conduz encerra a partida
- **THEN** o núcleo credita a pontuação às equipes na mesma transação da transição

### Requirement: O aparelho da equipe recebe a pergunta e envia a resposta

O núcleo SHALL servir ao aparelho da equipe a pergunta no ar em **`GET
/v1/partidas-de-quiz/{id}/pergunta`** e a resposta da equipe em **`POST
/v1/partidas-de-quiz/{id}/respostas`**. A resposta é **da equipe**, e uma só por equipe e
pergunta: o reenvio devolve o registro já gravado, e alternativa diferente da já gravada é
recusada. A plataforma NEVER SHALL controlar aparelhos no Ciclo 01 — a resposta não guarda de
que aparelho veio (documento 05 §5). (`RF-04-41`, `RF-04-43`, `RF-04-44`, PRD-04 §9)

#### Scenario: O aparelho recebe a pergunta no ar

- **WHEN** o aparelho de uma equipe disputante lê a pergunta da partida
- **THEN** o núcleo devolve o enunciado e as quatro alternativas da pergunta no ar

#### Scenario: A equipe envia a resposta

- **WHEN** o aparelho de uma equipe disputante envia a alternativa escolhida
- **THEN** o núcleo grava a resposta da equipe com o momento de chegada carimbado por ele

#### Scenario: A segunda resposta da mesma equipe é recusada

- **WHEN** a mesma equipe envia uma alternativa diferente para a mesma pergunta
- **THEN** o núcleo recusa com 422 e a resposta já gravada permanece

#### Scenario: O reenvio por rede instável não duplica

- **WHEN** a mesma equipe reenvia a mesma alternativa para a mesma pergunta
- **THEN** o núcleo devolve o registro já gravado, sem duplicar e sem mover o momento
