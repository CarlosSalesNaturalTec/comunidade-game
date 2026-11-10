# Spec Delta

## ADDED Requirements

### Requirement: Cada resposta da sondagem tem retorno por 2 segundos e avança sozinha

Respondida uma pergunta da sondagem, por toque ou por voz, a tela SHALL mostrar por **2
segundos** o símbolo de **acerto**, verde, ou de **erro**, vermelho, com formas distintas e
texto acessível, e SHALL avançar sozinha à pergunta seguinte. Durante o retorno as alternativas
SHALL ficar travadas; a resposta dada NEVER SHALL ser trocada, e a sondagem NEVER SHALL
oferecer voltar à pergunta anterior nem botão de envio. (`RF-05-99`)

#### Scenario: Acertar mostra o símbolo verde

- **WHEN** o Guerreiro(a) toca a alternativa correta de uma pergunta da sondagem
- **THEN** a tela mostra o símbolo verde de acerto por 2 segundos e apresenta a pergunta seguinte

#### Scenario: Errar mostra o símbolo vermelho

- **WHEN** o Guerreiro(a) toca uma alternativa que não é a correta
- **THEN** a tela mostra o símbolo vermelho de erro por 2 segundos e apresenta a pergunta
  seguinte

#### Scenario: A resposta não se troca

- **WHEN** o retorno de uma pergunta está na tela
- **THEN** as alternativas estão travadas, e não há caminho para voltar à pergunta anterior

#### Scenario: O retorno não depende só da cor

- **WHEN** o símbolo de acerto ou de erro está na tela
- **THEN** acerto e erro têm formas diferentes e um texto que o leitor de tela anuncia

### Requirement: Com a narração ligada, o retorno da sondagem é falado

Com a narração ligada, o retorno de acerto ou de erro de cada pergunta da sondagem SHALL ser
**falado** enquanto o símbolo está na tela; desligada, NEVER SHALL falar. (`RF-05-99`, decisão
do fundador de 2026-11-10)

#### Scenario: Com o áudio ligado, o retorno é falado

- **WHEN** a narração está ligada e o Guerreiro(a) responde uma pergunta da sondagem
- **THEN** o retorno de acerto ou de erro é falado enquanto o símbolo está na tela

#### Scenario: Com o áudio desligado, o retorno não fala

- **WHEN** a narração está desligada e o Guerreiro(a) responde uma pergunta da sondagem
- **THEN** o símbolo aparece e nada é falado

### Requirement: A sondagem termina na tela de acertos e erros, com Refazer e Concluir

Depois do retorno da **última** pergunta, a sondagem SHALL ser submetida sem toque, e a tela
SHALL mostrar o **total de acertos e de erros** que o núcleo devolveu, com os botões
**Refazer** e **Concluir**. Refazer SHALL recomeçar da primeira pergunta, sem resposta marcada;
Concluir SHALL seguir o percurso, que só então recarrega. Falhando o envio, a tela SHALL dizer
em linguagem simples e oferecer tentar de novo sem refazer. (`RF-05-100`, `RN-05-56`)

#### Scenario: A tela final traz o total

- **WHEN** o Guerreiro(a) responde a última pergunta de uma sondagem de cinco, acertando três
- **THEN** depois do retorno a tela diz que ele acertou três e errou duas, com Refazer e Concluir

#### Scenario: Concluir segue o percurso

- **WHEN** o Guerreiro(a) toca Concluir
- **THEN** a trilha recarrega e apresenta a missão seguinte do percurso, que a sondagem abriu

#### Scenario: Refazer recomeça a sondagem

- **WHEN** o Guerreiro(a) toca Refazer
- **THEN** a primeira pergunta volta sem resposta marcada, e a nova realização é gravada ao fim

#### Scenario: Resposta falada sem alternativa conta como erro

- **WHEN** uma resposta falada da sondagem não se ligou a alternativa alguma
- **THEN** o retorno daquela pergunta é o de erro, e ela entra no total de erros

#### Scenario: Sondagem largada no meio recomeça

- **WHEN** o Guerreiro(a) sai da sondagem antes da última pergunta e volta a ela
- **THEN** ela recomeça da primeira pergunta, e nada da realização largada foi gravado

### Requirement: A sondagem respondida se refaz pelo rodapé da trilha

Com a sondagem da trilha já respondida, o rodapé da trilha SHALL oferecer **Refazer a
sondagem**, a qualquer tempo e sem limite, que a apresenta com o mesmo retorno por pergunta e a
mesma tela final; Concluir SHALL voltar à missão em que o percurso está. Sem submissão ligada,
o caminho NEVER SHALL aparecer. (`RF-05-101`, `RN-05-56`)

#### Scenario: O rodapé oferece refazer

- **WHEN** o Guerreiro(a) abre uma trilha cuja sondagem ele já respondeu
- **THEN** o rodapé oferece Refazer a sondagem

#### Scenario: Antes de responder não há o caminho

- **WHEN** o Guerreiro(a) abre uma trilha cuja sondagem ainda é a próxima missão
- **THEN** o rodapé não oferece Refazer a sondagem, porque ela já está na tela

#### Scenario: Refazer pelo rodapé e concluir volta ao percurso

- **WHEN** o Guerreiro(a) refaz a sondagem pelo rodapé e toca Concluir
- **THEN** a tela volta à missão em que o percurso dele está

## MODIFIED Requirements

### Requirement: O Guerreiro(a) responde à sondagem que abre a trilha

A aplicação SHALL apresentar a **missão de sondagem** como o primeiro passo da trilha recém
inscrita, e a tela SHALL dizer, em linguagem simples, que ela serve para **o Mestre ajustar** o
que vem pela frente e que o resultado dela **não muda o nível** de ninguém. NEVER SHALL
apresentar a sondagem como prova nem exibir acerto e erro como nota: o retorno por pergunta e
o total de acertos e erros da tela final dizem o que a criança acertou, sem nota, sem palavra
de aprovação ou reprovação e sem trancar nada. (`RF-05-72`, `RF-05-73`, `RF-05-99`,
`RF-05-100`, `RN-05-34`)

#### Scenario: A sondagem abre a trilha

- **WHEN** o Guerreiro(a) abre uma trilha em que acabou de se inscrever
- **THEN** a missão de sondagem é o primeiro passo apresentado

#### Scenario: A tela explica para que serve a sondagem

- **WHEN** o Guerreiro(a) está respondendo a sondagem
- **THEN** a tela diz que ela serve para o Mestre ajustar e que não muda o nível dele

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

Na **missão de sondagem**, o voltar à pergunta anterior e o controle de enviar as respostas
NEVER SHALL ser apresentados: a resposta tem retorno por pergunta, a sondagem avança e se
submete sozinha e termina na tela de acertos e erros, como o requisito do retorno por pergunta
determina. As demais regras deste requisito seguem valendo para ela. (`RF-05-99`, `RF-05-100`)

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
- **THEN** a tela mostra o total de acertos e de erros, sem dizer que ele passou ou não passou

#### Scenario: A sondagem não volta nem tem botão de enviar

- **WHEN** o Guerreiro(a) percorre as perguntas da sondagem
- **THEN** não há controle de voltar à pergunta anterior nem de enviar as respostas

#### Scenario: O controle do prático fica indisponível sem a comprovação

- **WHEN** o Guerreiro(a) abre um prático cuja forma aceita é vídeo e ainda não escolheu o
  arquivo
- **THEN** o controle de declarar que cumpriu fica indisponível

#### Scenario: O prático sem forma declarada segue com o controle disponível

- **WHEN** o Guerreiro(a) abre um prático declarado antes de a forma de comprovação existir
- **THEN** o controle de declarar que cumpriu está disponível, e não há campo algum a preencher
