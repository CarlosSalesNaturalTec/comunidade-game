## ADDED Requirements

### Requirement: O Guerreiro(a) descobre a partida da sua aula, com a equipe dele já derivada

O núcleo SHALL servir ao Guerreiro(a) em sessão as partidas de uma aula em **`GET
/v1/aulas/{id}/partidas`**, cada uma com a situação e com **a equipe pela qual ele disputa,
derivada pelo núcleo**. O aparelho NEVER SHALL escolher a equipe nem informá-la: a garantia de
que é uma só é da abertura da partida, que recusa a equipe com integrante já disputante por
outra. Guerreiro(a) que não disputa nenhuma equipe daquela partida SHALL recebê-la com a equipe
nula, e aula sem partida SHALL devolver lista vazia, sem erro. A leitura SHALL exigir a mesma
operação da resposta da equipe, e papel que não a tem SHALL receber 403. (`RF-04-41`,
`RF-04-42`, PRD-04 §9, documento 05 §5)

#### Scenario: O Guerreiro(a) descobre a partida em que a sua equipe disputa

- **WHEN** o Guerreiro(a) em sessão lê as partidas da aula em que a equipe dele disputa
- **THEN** o núcleo devolve a partida, a situação dela e o identificador da equipe pela qual
  ele disputa

#### Scenario: A equipe vem derivada, e o aparelho não a escolhe

- **WHEN** o Guerreiro(a) integra mais de uma equipe do encontro e só uma disputa a partida
- **THEN** o núcleo devolve a equipe disputante, e nenhuma escolha é pedida ao aparelho

#### Scenario: Quem não disputa recebe a partida sem equipe

- **WHEN** um Guerreiro(a) da aula que não integra equipe disputante lê as partidas
- **THEN** o núcleo devolve a partida com a equipe nula, e o aparelho não tem por onde responder

#### Scenario: Aula sem partida devolve lista vazia

- **WHEN** a aula ainda não teve partida aberta
- **THEN** o núcleo devolve lista vazia, sem erro

#### Scenario: Papel sem a operação é recusado

- **WHEN** um Mestre ou um Admin lê as partidas da aula por esta rota
- **THEN** o núcleo recusa com 403, e a condução segue pelas rotas próprias dela

## MODIFIED Requirements

### Requirement: A partida é lida por sondagem periódica

O núcleo SHALL expor a **leitura do estado da partida**, que devolve a situação, a pergunta
no ar, se o resultado dela já foi liberado e as equipes disputantes, **restrita a quem
conduz**. O aparelho da equipe SHALL acompanhar a partida pela leitura que é dele — a pergunta
no ar —, e NEVER SHALL alcançar a leitura do estado. Ambas SHALL ser alcançáveis a qualquer
momento da partida aberta e SHALL devolver sempre o estado corrente, de modo que o aparelho que
ficou fora do ar durante uma pergunta **volte na pergunta corrente**, sem travar a partida nem
recuperar a que perdeu. A sincronização em tempo real do Ciclo 01 é **sondagem periódica**, e
não conexão longa (documento 03 §1). (`RF-02-60`, `RF-04-41`, PRD-02 §12)

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

### Requirement: O aparelho da equipe recebe a pergunta e envia a resposta

O núcleo SHALL servir ao aparelho da equipe a pergunta no ar em **`GET
/v1/partidas-de-quiz/{id}/pergunta`** e a resposta da equipe em **`POST
/v1/partidas-de-quiz/{id}/respostas`**. A resposta é **da equipe**, e uma só por equipe e
pergunta: o reenvio devolve o registro já gravado, e alternativa diferente da já gravada é
recusada. A plataforma NEVER SHALL controlar aparelhos no Ciclo 01 — a resposta não guarda de
que aparelho veio (documento 05 §5).

Liberado o resultado por quem conduz, a leitura da pergunta SHALL devolver também a
**alternativa correta**, **se a equipe do Guerreiro(a) em sessão acertou** e **qual equipe
chegou primeiro**, por ordem de chegada no servidor. Enquanto o resultado não for liberado,
NEVER SHALL devolver qualquer um dos três. A leitura NEVER SHALL creditar pontuação: o crédito
segue sendo do encerramento da partida. (`RF-04-41`, `RF-04-43`, `RF-04-44`, PRD-04 §9)

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

#### Scenario: Antes da liberação o aparelho não recebe a correta

- **WHEN** o aparelho lê a pergunta cujo resultado ainda não foi liberado
- **THEN** o núcleo devolve o enunciado e as alternativas, sem a correta, sem dizer se a equipe
  acertou e sem quem chegou primeiro

#### Scenario: Liberado, o aparelho recebe o resultado da sua equipe

- **WHEN** quem conduz libera o resultado e o aparelho lê a pergunta na sondagem seguinte
- **THEN** o núcleo devolve a alternativa correta, se a equipe daquele Guerreiro(a) acertou e
  qual equipe chegou primeiro

#### Scenario: A leitura do resultado não credita

- **WHEN** o aparelho lê o resultado liberado de uma pergunta numa partida ainda aberta
- **THEN** nenhuma pontuação é lançada às equipes
