## Purpose

A partida do Quiz ao Vivo no encontro presencial — a pergunta de múltipla escolha do Mestre
curador, a disputa entre as equipes de uma mesma trilha e a resposta de cada equipe com o
momento em que chegou ao servidor, que é o critério de desempate do bônus.

## Requirements

### Requirement: A pergunta de quiz é de múltipla escolha com quatro alternativas

O núcleo SHALL manter a **pergunta de quiz**, de autoria de um **Mestre**, com enunciado,
**exatamente quatro alternativas** e a indicação de qual delas é a correta. A pergunta SHALL
recusar número de alternativas diferente de quatro e SHALL recusar o cadastro sem alternativa
correta declarada. O núcleo NÃO SHALL guardar tempo-limite de resposta: o ritmo é de quem
conduz a partida. (`RF-01-36`, `RF-01-03`, documento 05 §5, documento 09)

#### Scenario: Pergunta com quatro alternativas e uma correta é aceita

- **WHEN** um Mestre cadastra uma pergunta com enunciado, quatro alternativas e a correta
  indicada
- **THEN** o núcleo grava a pergunta com a autoria, a data e a hora do cadastro

#### Scenario: Pergunta com três alternativas é recusada

- **WHEN** um Mestre tenta cadastrar uma pergunta com três alternativas
- **THEN** o núcleo responde 422 e nenhuma pergunta é gravada

#### Scenario: Pergunta sem alternativa correta é recusada

- **WHEN** um Mestre tenta cadastrar uma pergunta sem indicar qual alternativa é a correta
- **THEN** o núcleo responde 422 e nenhuma pergunta é gravada

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
