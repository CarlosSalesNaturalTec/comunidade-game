## ADDED Requirements

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
no ar, se o resultado dela já foi liberado e as equipes disputantes. A leitura SHALL ser
alcançável a qualquer momento da partida aberta e SHALL devolver sempre o estado corrente,
de modo que o aparelho que ficou fora do ar durante uma pergunta **volte na pergunta
corrente**, sem travar a partida nem recuperar a que perdeu. A sincronização em tempo real do
Ciclo 01 é **sondagem periódica**, e não conexão longa (documento 03 §1). (`RF-02-60`,
`RF-04-41`, PRD-02 §12)

#### Scenario: A leitura devolve o estado corrente

- **WHEN** quem conduz ou o aparelho de uma equipe disputante lê a partida
- **THEN** o núcleo devolve a situação, a pergunta no ar, se o resultado está liberado e as
  equipes disputantes

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
