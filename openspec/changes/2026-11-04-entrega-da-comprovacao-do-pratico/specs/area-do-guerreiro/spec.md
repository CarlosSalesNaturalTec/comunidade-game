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

## MODIFIED Requirements

### Requirement: O Guerreiro(a) faz o desafio de desbloqueio e repete sem ser punido

A aplicação SHALL permitir ao Guerreiro(a) **realizar o desafio de desbloqueio** da missão. No
**quiz**, a tela SHALL apresentar **uma pergunta por vez**, na ordem declarada pelo Mestre
autor, com um controle de **avançar** para a seguinte, e SHALL submeter as respostas **de uma
vez só** ao fim, nunca uma pergunta por submissão: o critério de aprovação é do conjunto
(`RN-05-45`), e submeter por pergunta o tornaria incalculável. A resposta já dada SHALL ser
guardada **no aparelho** enquanto o Guerreiro(a) percorre as demais, e ele SHALL poder
**voltar** a uma pergunta anterior para trocá-la antes de submeter. A tela NEVER SHALL declarar
a **posição na sequência** de perguntas, nem escrita nem anunciada a leitor de tela.
(documento 15 §6.4, decisão do fundador de 2026-09-26, revista em 2026-10-16)

O controle de **enviar as respostas** SHALL ficar **indisponível enquanto houver pergunta sem
resposta**, e SHALL ficar disponível quando todas estiverem respondidas: o inválido se impede
antes do toque, não se explica depois dele. Esta condição SHALL valer **só para o quiz** — o
desafio que se cumpre por **declaração** tem a **comprovação** por condição própria: o controle
dele SHALL ficar indisponível enquanto a comprovação na forma aceita não estiver preenchida, e
SHALL seguir sempre disponível no prático que **não declarou** forma de comprovação, que não tem
o que preencher. O controle de enviar SHALL ser apresentado **junto** dos controles de
avançar e voltar, e NEVER SHALL desaparecer no quiz de **uma única** pergunta, que não pagina.
(`RF-05-89`, `RN-05-45`, decisão do fundador de 2026-10-16)

Com a narração ligada, cada pergunta alcançada SHALL ser **falada** — enunciado e alternativas
—, ao avançar e ao voltar, como a camada de narração determina. (documento 15 §5.1, decisão do
fundador de 2026-10-16)

**Passando**, a missão seguinte SHALL abrir **na hora**, sem recarregar a aplicação nem esperar
ato de terceiro. **Não passando**, a tela SHALL dizer **quantas perguntas ele acertou** e de
quantas, e SHALL oferecer **tentar de novo** em linguagem acolhedora, sem contagem de
fracassos, sem punição e sem qualquer mensagem que elimine ou classifique a criança. Na
**missão de sondagem**, a tela NEVER SHALL apresentar o resultado como aprovação ou reprovação:
respondida, a trilha segue. (`RF-05-13`, `RF-05-14`, `RF-05-89`, `RN-05-20`, `RN-05-45`,
`RN-05-46`)

A pergunta que tem **imagem** SHALL exibi-la junto do enunciado, antes das alternativas, com
**texto alternativo** que a nomeie para quem usa leitor de tela. A imagem que não carrega NEVER
SHALL impedir de responder: a pergunta SHALL continuar respondível, com aviso de que a imagem
não abriu. A tela NEVER SHALL exigir a imagem para submeter o quiz. (`RF-09-119`)

#### Scenario: O quiz apresenta uma pergunta por vez

- **WHEN** o Guerreiro(a) abre um quiz de seis perguntas
- **THEN** a primeira pergunta aparece sozinha, com o controle de avançar para a seguinte

#### Scenario: A posição entre as perguntas não é declarada

- **WHEN** o Guerreiro(a) percorre as perguntas do quiz, com ou sem leitor de tela
- **THEN** nenhuma contagem de posição é apresentada nem anunciada

#### Scenario: Voltar a uma pergunta anterior troca a resposta

- **WHEN** o Guerreiro(a) na quarta pergunta volta à segunda
- **THEN** a resposta que ele deu à segunda está lá, e ele pode trocá-la antes de submeter

#### Scenario: A submissão leva todas as respostas de uma vez

- **WHEN** o Guerreiro(a) percorre as seis perguntas do quiz e conclui
- **THEN** as seis respostas vão numa única submissão, ao fim, nunca uma por pergunta

#### Scenario: Pergunta sem resposta é sinalizada

- **WHEN** o Guerreiro(a) respondeu cinco das seis perguntas do quiz
- **THEN** o controle de enviar as respostas permanece indisponível, nada é submetido, e é essa
  indisponibilidade que sinaliza a pendência

#### Scenario: Respondidas todas, enviar fica disponível

- **WHEN** o Guerreiro(a) responde a última pergunta que faltava
- **THEN** o controle de enviar as respostas fica disponível

#### Scenario: Enviar aparece junto de avançar e voltar

- **WHEN** o Guerreiro(a) percorre as perguntas do quiz
- **THEN** o controle de enviar as respostas é apresentado junto dos de avançar e voltar

#### Scenario: Quiz de uma pergunta oferece enviar

- **WHEN** o quiz do desbloqueio tem uma única pergunta, e ela foi respondida
- **THEN** o controle de enviar as respostas é apresentado, embora não haja o que paginar

#### Scenario: O desafio por declaração não espera resposta

- **WHEN** o Guerreiro(a) abre um desafio de desbloqueio que se cumpre por declaração
- **THEN** o controle de declarar que cumpriu está disponível, sem pergunta alguma a responder

#### Scenario: A pergunta alcançada é falada com as alternativas

- **WHEN** a narração está ligada e o Guerreiro(a) avança para a pergunta seguinte do quiz
- **THEN** o enunciado dela e as alternativas são falados

#### Scenario: Passar abre a seguinte na hora

- **WHEN** o Guerreiro(a) responde a todas as perguntas do quiz, submete e passa
- **THEN** a missão seguinte aparece aberta imediatamente no percurso dele

#### Scenario: A pergunta com imagem a exibe junto do enunciado

- **WHEN** o Guerreiro(a) alcança, no quiz, a pergunta que tem imagem
- **THEN** a imagem aparece com o enunciado daquela pergunta, antes das alternativas, com texto
  alternativo

#### Scenario: Imagem que não carrega não tranca a pergunta

- **WHEN** a imagem de uma pergunta não carrega
- **THEN** a tela avisa que a imagem não abriu e o Guerreiro(a) segue podendo responder e
  submeter

#### Scenario: Não passar convida a tentar de novo

- **WHEN** o Guerreiro(a) submete o quiz e não passa
- **THEN** a tela diz quantas perguntas ele acertou, de quantas, e o convida a tentar de novo,
  sem punição e sem exibir contagem de fracassos

#### Scenario: A sondagem não fala em aprovação

- **WHEN** o Guerreiro(a) responde a missão de sondagem
- **THEN** a tela agradece e segue para a trilha, sem dizer que ele passou ou não passou

#### Scenario: O controle do prático fica indisponível sem a comprovação

- **WHEN** o Guerreiro(a) abre um prático cuja forma aceita é vídeo e ainda não escolheu o
  arquivo
- **THEN** o controle de declarar que cumpriu fica indisponível

#### Scenario: O prático sem forma declarada segue com o controle disponível

- **WHEN** o Guerreiro(a) abre um prático declarado antes de a forma de comprovação existir
- **THEN** o controle de declarar que cumpriu está disponível, e não há campo algum a preencher
