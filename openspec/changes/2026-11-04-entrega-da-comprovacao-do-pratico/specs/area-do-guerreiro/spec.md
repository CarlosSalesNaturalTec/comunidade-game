# Spec Delta

## ADDED Requirements

### Requirement: A tela do prático diz o que entregar e sob que critério

A tela do desafio **prático** SHALL apresentar, junto do enunciado, o **critério de aceite**
escrito pelo Mestre autor e **qual forma de comprovação** ele aceita, antes de qualquer controle
de entrega: é deles que o Guerreiro(a) sabe o que entregar e sob que critério será julgado. A
tela NEVER SHALL apresentar o **título curto**, que é da vitrine, nem exigir que a criança
escolha a forma — ela é **uma** e já está declarada. (`RF-05-92`, `RF-09-129`, `RF-09-130`)

#### Scenario: O critério e a forma aparecem antes do controle de entrega

- **WHEN** o Guerreiro(a) abre uma missão cujo desbloqueio é prático
- **THEN** a tela apresenta o enunciado, o critério de aceite e a forma aceita, e só então o
  controle de entrega

#### Scenario: A criança não escolhe a forma

- **WHEN** a forma aceita é vídeo
- **THEN** a tela oferece só a entrega em vídeo, sem seletor de forma

#### Scenario: O prático antigo, sem os três campos, segue realizável

- **WHEN** o Guerreiro(a) abre um prático declarado antes de os três campos existirem
- **THEN** a tela apresenta o enunciado que ele tem, sem critério nem forma, e a entrega segue
  possível

### Requirement: A tela avisa que a mídia fica guardada e pode ir à vitrine

Antes de a criança entregar, a tela do prático SHALL **avisá-la**, em linguagem simples, de que
aquela comprovação **fica guardada** e **pode ir à vitrine pública**, com acesso à área
detalhada sobre destino e uso. O aviso é requisito, não texto de enfeite: é o que dá sentido ao
critério de aceite. Ele NEVER SHALL ser apresentado só depois do envio, nem substituído por
rótulo de controle. (`RF-05-92`, PRD-05 §11, documento 03 §12)

#### Scenario: O aviso aparece antes da entrega

- **WHEN** o Guerreiro(a) abre o prático cuja forma aceita é imagem, áudio, vídeo ou arquivo
- **THEN** a tela avisa, antes do controle de entrega, que a mídia fica guardada e pode ir à
  vitrine, com acesso à área detalhada

#### Scenario: O aviso não vira confirmação depois do envio

- **WHEN** o Guerreiro(a) conclui o envio da comprovação
- **THEN** o aviso já tinha sido apresentado antes, e a tela não o apresenta como novidade
  depois

### Requirement: O Guerreiro(a) entrega a comprovação e acompanha o envio

A tela SHALL receber a comprovação na forma aceita — corpo escrito, endereço ou arquivo — e
SHALL **impedir o envio antes de ela estar preenchida**, em vez de explicá-lo depois do toque.
No envio de arquivo, a tela SHALL apresentar o **progresso** e, caindo a rede, SHALL dizê-lo e
oferecer **retomar**, sem recomeçar do zero nem perder a declaração. (`RF-05-91`, `RF-05-93`)

#### Scenario: O controle de entrega fica indisponível sem a comprovação

- **WHEN** o Guerreiro(a) abre o prático e ainda não preencheu a comprovação
- **THEN** o controle de declarar que cumpriu fica indisponível

#### Scenario: O envio do arquivo mostra o progresso

- **WHEN** o Guerreiro(a) envia a comprovação em vídeo
- **THEN** a tela apresenta o progresso do envio até concluir

#### Scenario: A rede cai no meio do envio

- **WHEN** a conexão cai durante o envio da comprovação
- **THEN** a tela diz o que houve e oferece retomar, sem perder a declaração nem o que já subiu

#### Scenario: O Guerreiro(a) reencontra a comprovação entregue

- **WHEN** o Guerreiro(a) volta à missão depois de entregar e antes do julgamento
- **THEN** a tela apresenta a comprovação que ele entregou, e não um formulário vazio

### Requirement: Quem não pode entregar pelo aparelho entrega ao Mestre no encontro

A tela SHALL oferecer, ao lado da entrega, **entregar ao Mestre no encontro**, para quem recusa
a câmera ou o microfone, não tem aparelho que grave ou não consegue enviar. Escolhida, a
declaração segue adiante **sem mídia**, e a tela SHALL dizer que o Mestre vai conferir no
encontro. A tela NEVER SHALL apresentar essa escolha como falha, desistência ou perda da missão.
(`RN-05-51`, `RF-05-78`, PRD-05 §11)

#### Scenario: A alternativa fica à vista junto da entrega

- **WHEN** o Guerreiro(a) abre o prático cuja forma aceita é mídia
- **THEN** a tela oferece a entrega pelo aparelho e, ao lado, entregar ao Mestre no encontro

#### Scenario: Escolhida a entrega no encontro, a declaração segue

- **WHEN** o Guerreiro(a) escolhe entregar ao Mestre no encontro
- **THEN** a declaração é enviada sem mídia e a tela diz que o Mestre vai conferir no encontro

#### Scenario: A alternativa não é apresentada como falha

- **WHEN** o Guerreiro(a) escolhe a entrega no encontro
- **THEN** nenhuma mensagem a trata como desistência, erro ou perda da missão
