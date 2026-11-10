# Spec Delta

## ADDED Requirements

### Requirement: A sondagem respondida se refaz, e vale a última tentativa

A submissão de **sondagem já respondida** pelo Guerreiro(a) SHALL ser aceita: o núcleo SHALL
gravá-la como **tentativa nova**, com o instante e a resposta de cada pergunta, e devolver o
placar dela — acertos e total. NEVER SHALL criar segundo desbloqueio, creditar ponto nem
definir nível. O resultado vigente da sondagem SHALL ser o da tentativa **mais recente**.
(`RF-05-101`, `RN-05-56`, `RN-05-47`, `RN-05-46`)

#### Scenario: Refazer a sondagem grava tentativa nova

- **WHEN** o Guerreiro(a) que já respondeu a sondagem a submete de novo
- **THEN** o núcleo grava uma submissão nova, com os acertos e a resposta de cada pergunta, e
  as anteriores seguem gravadas

#### Scenario: Refazer devolve o placar da nova tentativa

- **WHEN** o Guerreiro(a) refaz a sondagem de cinco perguntas e acerta três
- **THEN** a resposta diz que ele acertou três de cinco, e a missão segue desbloqueada

#### Scenario: Refazer não cria segundo desbloqueio nem credita

- **WHEN** o Guerreiro(a) refaz a sondagem
- **THEN** o desbloqueio dele na sondagem segue um só, e o saldo e o nível dele não mudam

#### Scenario: Vale a tentativa mais recente

- **WHEN** o Guerreiro(a) respondeu a sondagem acertando duas e a refez acertando quatro
- **THEN** o resultado vigente da sondagem dele é quatro acertos, o da tentativa mais recente

#### Scenario: O desafio de desbloqueio já cumprido não muda

- **WHEN** o Guerreiro(a) submete de novo o quiz de uma missão comum que ele já desbloqueou
- **THEN** o núcleo responde com a situação do desbloqueio, como antes desta change

### Requirement: A leitura do percurso traz o gabarito só da sondagem

A leitura da missão no percurso do Guerreiro(a) SHALL trazer, em cada pergunta da **missão de
sondagem**, qual alternativa é a **correta**, para a tela dar o retorno por pergunta. Na missão
que não é sondagem, a pergunta NEVER SHALL trazer a alternativa correta. (`RN-05-57`,
`RF-05-99`)

#### Scenario: A pergunta da sondagem traz a correta

- **WHEN** o Guerreiro(a) inscrito lê a missão de sondagem no percurso
- **THEN** cada pergunta vem com o enunciado, as quatro alternativas e qual delas é a correta

#### Scenario: A pergunta do desafio de desbloqueio não traz a correta

- **WHEN** o Guerreiro(a) inscrito lê no percurso uma missão comum com quiz de desbloqueio
- **THEN** as perguntas vêm sem a alternativa correta

## MODIFIED Requirements

### Requirement: A imagem da pergunta é servida a quem pode ver a pergunta

O núcleo SHALL servir os **bytes** da imagem de uma pergunta do quiz ao **Mestre autor da
trilha** e ao **Guerreiro(a) inscrito** nela — os mesmos que já leem a pergunta —, com o tipo
declarado no envio. A quem não é um dos dois SHALL responder **403**, e NEVER SHALL servir a
imagem de trilha em que o Guerreiro(a) não está inscrito. Pergunta **sem imagem** SHALL
responder **404**. A leitura NEVER SHALL revelar a alternativa correta, que segue fora de toda
saída ao Guerreiro(a) — salvo a da **sondagem**, que a leitura da missão no percurso traz.
(`RF-09-119`, `RF-05-89`, `RN-05-57`, decisão do fundador de 2026-09-11)

#### Scenario: O Guerreiro(a) inscrito vê a imagem da pergunta

- **WHEN** o Guerreiro(a) inscrito na trilha pede a imagem de uma pergunta do quiz de uma
  missão dela
- **THEN** o núcleo devolve os bytes da imagem, com o tipo declarado no envio

#### Scenario: O Mestre autor vê a imagem que anexou

- **WHEN** o Mestre autor pede a imagem de uma pergunta da sua trilha
- **THEN** o núcleo devolve os bytes da imagem

#### Scenario: Quem não é inscrito nem autor é recusado

- **WHEN** um Guerreiro(a) não inscrito na trilha pede a imagem de uma pergunta dela
- **THEN** o núcleo responde **403** e nenhum byte é servido

#### Scenario: Pergunta sem imagem responde 404

- **WHEN** alguém que pode ver a pergunta pede a imagem de uma pergunta que não tem imagem
- **THEN** o núcleo responde **404**
