# Spec Delta

## Purpose

A resposta falada da missão de sondagem: com o áudio ligado, depois que a narração fala a
pergunta e as alternativas, uma janela de escuta curta capta a resposta da criança, a mostra
transcrita e a envia sozinha, nas Apps 01 e 05.

## ADDED Requirements

### Requirement: Com o áudio ligado, a sondagem escuta depois de falar a pergunta

Com a narração ligada e a transcrição disponível, ao **terminar a fala** do enunciado e das
alternativas de uma pergunta da **sondagem**, a tela SHALL abrir o microfone por **5 segundos**,
e só então. Antes do fim da fala NEVER SHALL abrir. (`RF-05-97`, `RF-04-77`)

#### Scenario: Terminada a fala, o microfone abre

- **WHEN** o áudio está ligado e a narração termina de falar uma pergunta da sondagem
- **THEN** o microfone abre e a janela de 5 segundos começa

#### Scenario: Durante a fala, o microfone segue fechado

- **WHEN** a narração ainda fala o enunciado ou as alternativas
- **THEN** o microfone permanece fechado

### Requirement: A janela de escuta é visível e mostra a transcrição

Enquanto a janela dura, a tela SHALL mostrar uma **barra de progresso** de 5 segundos e a
**transcrição obtida até ali**, atualizada conforme a criança fala. A barra SHALL ter rótulo
acessível, e a transcrição SHALL ser texto da tela, alcançável por leitor de tela.
(`RF-05-97`, documento 15 §5)

#### Scenario: A barra corre enquanto escuta

- **WHEN** a janela de escuta está aberta
- **THEN** a barra avança de vazia a cheia em 5 segundos

#### Scenario: O que foi dito aparece na tela

- **WHEN** a criança fala durante a janela
- **THEN** a transcrição aparece na tela antes do envio

### Requirement: Ao fim da janela, a resposta é enviada sozinha

Ao fim dos 5 segundos, o microfone SHALL fechar e a resposta SHALL ser marcada na pergunta, que
SHALL avançar para a seguinte; na **última** pergunta, a sondagem SHALL ser **submetida** sem
toque. A resposta falada SHALL substituir a escolha por toque naquela pergunta. (`RF-05-97`)

#### Scenario: A resposta falada avança a sondagem

- **WHEN** a janela de uma pergunta que não é a última termina
- **THEN** o microfone fecha, a resposta fica marcada e a pergunta seguinte é apresentada e falada

#### Scenario: A última resposta submete a sondagem

- **WHEN** a janela da última pergunta termina
- **THEN** a sondagem é submetida, e segue o que a submissão por toque já faz

### Requirement: A fala é ligada à alternativa aproximada

A transcrição SHALL ser comparada às quatro alternativas da pergunta, sem distinção de caixa,
acento e pontuação, aceitando também a **letra** ou a **posição** da alternativa. Havendo uma
alternativa claramente mais próxima, ela SHALL ser a marcada. (`RF-05-98`)

#### Scenario: Falar o texto da alternativa a marca

- **WHEN** a criança fala, com pequenas diferenças, o texto de uma alternativa
- **THEN** aquela alternativa é a marcada

#### Scenario: Falar a letra a marca

- **WHEN** a criança fala "letra B" ou "a segunda"
- **THEN** a segunda alternativa é a marcada

### Requirement: Silêncio ou fala sem correspondência segue como transcrição literal

Quando a transcrição for vazia, ou nenhuma alternativa for claramente a mais próxima, a resposta
SHALL seguir **sem alternativa**, levando a **transcrição literal** (vazia, no silêncio). A
sondagem SHALL avançar do mesmo jeito: responder abre a trilha, acertar não (`RF-05-98`,
`RN-05-46`, `RN-05-55`).

#### Scenario: Silêncio segue sem alternativa

- **WHEN** a janela termina sem fala alguma
- **THEN** a resposta segue sem alternativa e com transcrição vazia, e a sondagem avança

#### Scenario: Fala que não bate segue literal

- **WHEN** a criança fala algo que não se aproxima de nenhuma alternativa
- **THEN** a resposta segue sem alternativa, com o texto transcrito, e a sondagem avança

### Requirement: Só a sondagem responde por voz

A resposta falada SHALL valer **somente** na missão de sondagem. O desafio de desbloqueio, o Quiz
ao Vivo e os demais quizzes NEVER SHALL abrir o microfone. Com o áudio desligado, ou sem
transcrição no navegador, a sondagem SHALL seguir **por toque**, sem nenhuma diferença.
(`RN-05-54`)

#### Scenario: O desafio de desbloqueio não escuta

- **WHEN** o áudio está ligado e a narração termina de falar uma pergunta do desafio de
  desbloqueio
- **THEN** o microfone não abre

#### Scenario: Áudio desligado, a sondagem é por toque

- **WHEN** o áudio está desligado
- **THEN** a sondagem não abre o microfone e segue respondida por toque, como antes

#### Scenario: Sem transcrição no navegador, a sondagem é por toque

- **WHEN** o navegador não oferece transcrição de fala
- **THEN** a sondagem segue por toque, sem mensagem de erro a cada pergunta

### Requirement: O microfone só capta dentro da janela

O microfone SHALL ficar aberto **apenas** durante a janela de 5 segundos e NEVER SHALL captar
entre uma pergunta e outra nem fora da sondagem. O áudio NEVER SHALL chegar ao núcleo nem ficar no
aparelho; ao núcleo segue só o texto. Tocar uma alternativa durante a janela SHALL fechar o
microfone e valer como resposta. (`RN-05-54`, documento 03 §§1.12, 4)

#### Scenario: Entre perguntas, o microfone fecha

- **WHEN** a resposta de uma pergunta é marcada
- **THEN** o microfone fecha antes de a pergunta seguinte ser falada

#### Scenario: O toque vence a voz

- **WHEN** a criança toca uma alternativa durante a janela
- **THEN** o microfone fecha e a alternativa tocada é a resposta

#### Scenario: Microfone negado, segue por toque

- **WHEN** a permissão do microfone foi negada
- **THEN** a sondagem segue por toque, sem janela de escuta
