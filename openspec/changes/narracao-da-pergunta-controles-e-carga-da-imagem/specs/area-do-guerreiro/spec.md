# Spec Delta

## MODIFIED Requirements

### Requirement: O Guerreiro(a) percorre o conteúdo e a bibliografia da missão

A aplicação SHALL exibir o **conteúdo da missão** — texto, imagens, vídeo e arquivos — na ordem
em que o Mestre autor o dispôs, **um conteúdo por vez**, com um controle de **avançar** que
leva ao seguinte; avançar SHALL apenas percorrer, e NEVER SHALL gravar nem submeter coisa
alguma. A tela NEVER SHALL declarar a **posição na sequência** — nem escrita, nem anunciada a
quem usa leitor de tela: numa Arena de uma decisão por tela a contagem é ruído, e o que orienta
é o próprio conteúdo da vez. No último conteúdo NEVER SHALL oferecer avançar para lugar nenhum.
Missão com **um único** conteúdo NEVER SHALL apresentar controle de avançar. (`RF-05-11`,
documento 15 §6.4, decisão do fundador de 2026-09-26, revista em 2026-10-16)

O **crédito ao autor** e a **licença** que a trilha publicada declara SHALL ser apresentados em
**bloco recolhível de resumo neutro** no **rodapé da tela**, fora do fluxo de leitura do
conteúdo: são metadado da obra, não o que a criança veio ler. Recolhido, o crédito SHALL
continuar **alcançável** — recolher não é suprimir, e a atribuição que a licença exige
continua sendo cumprida.
(`RF-05-11`, documento 15 §§6.1, 6.4)

A **bibliografia** SHALL ficar em **bloco recolhível de resumo neutro**, junto da missão
seguinte, e SHALL ser **omitida** quando a missão não tiver bibliografia. Aberta, SHALL
indicar **título** e **capítulo** e, quando o Guerreiro(a) tiver ponto de apoio, **se há
exemplar disponível nele**; sem essa informação, a disponibilidade SHALL ficar
**indeterminada**, nunca afirmada nem negada por suposição. (`RF-05-12`, documento 15 §6.1,
decisão do fundador de 2026-10-15)

A imagem e o vídeo enviados SHALL ser **exibidos** — a imagem visível e o vídeo reproduzível —,
e o arquivo de apoio SHALL ser alcançável pelo Guerreiro(a). A **referência do armazenamento**
NEVER SHALL aparecer na tela: ela não é conteúdo, não diz nada a quem lê e ocupa o lugar do que
o Mestre escreveu. Conteúdo cujo envio não foi concluído SHALL ser omitido ou dito pendente,
nunca apresentado como quebrado. (`RF-05-11`, `RF-05-12`)

#### Scenario: O conteúdo abre na ordem do autor

- **WHEN** o Guerreiro(a) abre uma missão desbloqueada com quatro conteúdos
- **THEN** o primeiro conteúdo da ordem declarada aparece sozinho e o controle de avançar leva
  ao segundo

#### Scenario: A posição na sequência não é declarada

- **WHEN** o Guerreiro(a) percorre os conteúdos de uma missão, com ou sem leitor de tela
- **THEN** nenhuma contagem de posição é apresentada nem anunciada, e o que se lê é o conteúdo
  da vez

#### Scenario: O último conteúdo não oferece avançar

- **WHEN** o Guerreiro(a) alcança o último conteúdo da missão
- **THEN** a tela não oferece avançar para outro conteúdo

#### Scenario: Conteúdo único não pagina

- **WHEN** a missão tem um único conteúdo
- **THEN** ele aparece sem controle de avançar

#### Scenario: O crédito está recolhido, e continua alcançável

- **WHEN** o Guerreiro(a) abre o conteúdo de uma missão
- **THEN** o crédito ao Mestre autor e a licença não aparecem no fluxo de leitura, e sim num
  bloco fechado de resumo neutro **no rodapé da tela**, que abre ao ser acionado

#### Scenario: A bibliografia diz onde encontrar o livro

- **WHEN** a missão traz bibliografia vinculada a exemplar do ponto de apoio do Guerreiro(a),
  e o Guerreiro(a) abre o bloco dela
- **THEN** a tela indica título, capítulo e se há exemplar disponível nele

#### Scenario: Sem vínculo, a disponibilidade não é afirmada

- **WHEN** a bibliografia da missão não está vinculada a exemplar tombado, e o bloco dela
  está aberto
- **THEN** a tela mostra título e capítulo e nada afirma sobre disponibilidade

#### Scenario: A imagem do conteúdo aparece como imagem

- **WHEN** o Guerreiro(a) alcança, na sequência, o conteúdo de imagem com envio confirmado
- **THEN** a imagem é exibida na posição em que o Mestre a dispôs

#### Scenario: A referência do armazenamento não chega à tela

- **WHEN** a missão traz conteúdo de imagem, vídeo ou arquivo
- **THEN** nenhuma referência de armazenamento é apresentada como se fosse o conteúdo

#### Scenario: Envio não concluído não aparece quebrado

- **WHEN** a missão traz conteúdo de arquivo cujo envio nunca foi confirmado
- **THEN** a tela o omite ou o diz pendente, e nada quebrado é apresentado

#### Scenario: A bibliografia nasce fechada, junto da missão seguinte

- **WHEN** o Guerreiro(a) abre uma missão que tem bibliografia
- **THEN** a bibliografia aparece como bloco fechado de resumo neutro, no mesmo grupo da
  missão seguinte, fora do fluxo de leitura do conteúdo

#### Scenario: Missão sem bibliografia não apresenta o bloco

- **WHEN** a missão aberta não tem bibliografia alguma
- **THEN** nenhum bloco de bibliografia aparece, nem fechado nem vazio

### Requirement: A mídia exibida ao Guerreiro(a) usa moldura de tamanho fixo

Toda imagem e todo vídeo que a aplicação busca do núcleo em bytes — o conteúdo da missão e a
imagem da pergunta do desafio de desbloqueio — SHALL ser exibidos numa moldura de **tamanho
fixo**, igual para os dois casos, sem crescer além dela: a imagem ou o vídeo inteiro cabe
dentro da moldura, sem ser cortado para preenchê-la, e o espaço que sobrar fica em branco. A
moldura NEVER SHALL oferecer ampliação nem abrir a mídia em tamanho maior. (`RF-05-11`,
`RF-09-119`, decisão do fundador de 2026-09-17)

Enquanto a mídia da vez está sendo buscada, a moldura SHALL **dizer que está carregando** e
NEVER SHALL apresentar a mídia de **outro** item nem o erro de outro item: alcançado um item
novo na sequência, a moldura SHALL partir do zero. Mídia obsoleta sob o item errado é
informação falsa, não espera. (`RF-05-11`, `RF-09-119`, decisão do fundador de 2026-10-16)

Enquanto a moldura carrega, os controles de **avançar e voltar** da sequência SHALL ficar
indisponíveis, para que a troca não se acumule sobre uma mídia que ainda não chegou. A trava
SHALL ceder quando a busca **falha**: mídia que não abriu NEVER SHALL prender quem percorre a
sequência, sob pena de a rede ruim virar beco sem saída. (decisão do fundador de 2026-10-16)

#### Scenario: Imagem grande do conteúdo cabe na moldura fixa, sem cortar

- **WHEN** o Guerreiro(a) abre uma missão cujo conteúdo tem uma foto de alta resolução
- **THEN** a foto aparece inteira, dentro da moldura de tamanho fixo, sem estourar o layout

#### Scenario: Vídeo do conteúdo usa a mesma moldura da imagem

- **WHEN** o Guerreiro(a) abre uma missão cujo conteúdo tem vídeo
- **THEN** o vídeo aparece na mesma moldura de tamanho fixo que a imagem usa

#### Scenario: A imagem da pergunta do desbloqueio usa a mesma moldura

- **WHEN** o Guerreiro(a) abre o desafio de desbloqueio de uma pergunta que tem imagem
- **THEN** a imagem aparece na mesma moldura de tamanho fixo que o conteúdo da missão usa

#### Scenario: A moldura não amplia ao ser tocada

- **WHEN** o Guerreiro(a) toca numa imagem ou num vídeo exibidos em moldura fixa
- **THEN** nada se amplia; a mídia permanece no mesmo tamanho

#### Scenario: A moldura diz que está carregando

- **WHEN** o Guerreiro(a) alcança um item cuja mídia ainda está sendo buscada
- **THEN** a moldura diz que está carregando, e avançar e voltar ficam indisponíveis

#### Scenario: A mídia do item anterior não fica na tela

- **WHEN** o Guerreiro(a) vai de um item com imagem direto para outro item com imagem
- **THEN** a imagem do item anterior desaparece de imediato, e a moldura carrega a do item
  alcançado

#### Scenario: O erro de um item não gruda no seguinte

- **WHEN** a mídia de um item não abre e o Guerreiro(a) avança para o item seguinte
- **THEN** o aviso de falha não acompanha o item novo, cuja mídia é buscada do zero

#### Scenario: Mídia que não abre libera a navegação

- **WHEN** a busca da mídia do item da vez falha
- **THEN** a tela avisa que ela não abriu e avançar e voltar voltam a estar disponíveis

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
desafio que se cumpre por **declaração** não tem pergunta a responder, e o controle dele SHALL
seguir sempre disponível. O controle de enviar SHALL ser apresentado **junto** dos controles de
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

## REMOVED Requirements

### Requirement: A tela leva o Guerreiro(a) até a pergunta que falta

**Reason**: Substituído pelo controle de envio que só fica disponível com todas as perguntas
respondidas (decisão do fundador de 2026-10-16, opção A entre as três apresentadas). Com o
envio impedido antes do toque, não existe mais a tentativa de submeter incompleto que
disparava a sinalização e o salto — o enunciado ficaria descrevendo um caminho inalcançável.
Este requisito nunca foi bloco próprio na spec: o texto removido vivia dentro de "O
Guerreiro(a) faz o desafio de desbloqueio e repete sem ser punido", e está registrado aqui
porque a mudança **retira comportamento** que a spec exigia, e não só reescreve o enunciado.

**Migration**: Nenhuma migração de dado. Quem respondia parcialmente e tocava em enviar era
levado à primeira pergunta pendente; agora o controle de enviar permanece indisponível até a
última resposta, e a navegação pelas perguntas segue sendo o caminho para completá-las. O
fundador aceitou, conhecendo-o, o preço de a tela deixar de **dizer** o que falta — aquele
aviso era narrado de graça pelo componente de aviso, e com ele desaparece o único retorno
falado da pendência.
