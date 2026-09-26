# Spec Delta

## MODIFIED Requirements

### Requirement: O Guerreiro(a) percorre o conteúdo e a bibliografia da missão

A aplicação SHALL exibir o **conteúdo da missão** — texto, imagens, vídeo e arquivos — na ordem
em que o Mestre autor o dispôs, **um conteúdo por vez**, com um controle de **avançar** que
leva ao seguinte; avançar SHALL apenas percorrer, e NEVER SHALL gravar nem submeter coisa
alguma. A tela SHALL dizer **onde o Guerreiro(a) está na sequência**, para que percorrer não
vire caminhar às cegas, e no último conteúdo NEVER SHALL oferecer avançar para lugar nenhum.
Missão com **um único** conteúdo NEVER SHALL apresentar controle de avançar. (`RF-05-11`,
documento 15 §6.4, decisão do fundador de 2026-09-26)

O **crédito ao autor** e a **licença** que a trilha publicada declara SHALL ser apresentados em
**bloco recolhível de resumo neutro**, fora do fluxo de leitura do conteúdo: são metadado da
obra, não o que a criança veio ler. Recolhido, o crédito SHALL continuar **alcançável** —
recolher não é suprimir, e a atribuição que a licença exige continua sendo cumprida.
(`RF-05-11`, documento 15 §§6.1, 6.4)

A **bibliografia** SHALL indicar **título** e **capítulo** e, quando o
Guerreiro(a) tiver ponto de apoio, **se há exemplar disponível nele**; sem essa informação, a
disponibilidade SHALL ficar **indeterminada**, nunca afirmada nem negada por suposição.

A imagem e o vídeo enviados SHALL ser **exibidos** — a imagem visível e o vídeo reproduzível —,
e o arquivo de apoio SHALL ser alcançável pelo Guerreiro(a). A **referência do armazenamento**
NEVER SHALL aparecer na tela: ela não é conteúdo, não diz nada a quem lê e ocupa o lugar do que
o Mestre escreveu. Conteúdo cujo envio não foi concluído SHALL ser omitido ou dito pendente,
nunca apresentado como quebrado. (`RF-05-11`, `RF-05-12`)

#### Scenario: O conteúdo abre na ordem do autor

- **WHEN** o Guerreiro(a) abre uma missão desbloqueada com quatro conteúdos
- **THEN** o primeiro conteúdo da ordem declarada aparece sozinho, a tela diz onde ele está na
  sequência, e o controle de avançar leva ao segundo

#### Scenario: O último conteúdo não oferece avançar

- **WHEN** o Guerreiro(a) alcança o último conteúdo da missão
- **THEN** a tela não oferece avançar para outro conteúdo

#### Scenario: Conteúdo único não pagina

- **WHEN** a missão tem um único conteúdo
- **THEN** ele aparece sem controle de avançar

#### Scenario: O crédito está recolhido, e continua alcançável

- **WHEN** o Guerreiro(a) abre o conteúdo de uma missão
- **THEN** o crédito ao Mestre autor e a licença não aparecem no fluxo de leitura, e sim num
  bloco fechado de resumo neutro, que abre ao ser acionado

#### Scenario: A bibliografia diz onde encontrar o livro

- **WHEN** a missão traz bibliografia vinculada a exemplar do ponto de apoio do Guerreiro(a)
- **THEN** a tela indica título, capítulo e se há exemplar disponível nele

#### Scenario: Sem vínculo, a disponibilidade não é afirmada

- **WHEN** a bibliografia da missão não está vinculada a exemplar tombado
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

### Requirement: O Guerreiro(a) faz o desafio de desbloqueio e repete sem ser punido

A aplicação SHALL permitir ao Guerreiro(a) **realizar o desafio de desbloqueio** da missão. No
**quiz**, a tela SHALL apresentar **uma pergunta por vez**, na ordem declarada pelo Mestre
autor, com um controle de **avançar** para a seguinte, e SHALL submeter as respostas **de uma
vez só** ao fim, nunca uma pergunta por submissão: o critério de aprovação é do conjunto
(`RN-05-45`), e submeter por pergunta o tornaria incalculável. A resposta já dada SHALL ser
guardada **no aparelho** enquanto o Guerreiro(a) percorre as demais, e ele SHALL poder
**voltar** a uma pergunta anterior para trocá-la antes de submeter. Pergunta ainda **sem
resposta** SHALL ser sinalizada antes do envio, e a tela SHALL **levar** o Guerreiro(a) até
ela, porque com uma pergunta por vez apenas contá-la não diz onde ela está. (documento 15
§6.4, decisão do fundador de 2026-09-26)

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

#### Scenario: Voltar a uma pergunta anterior troca a resposta

- **WHEN** o Guerreiro(a) na quarta pergunta volta à segunda
- **THEN** a resposta que ele deu à segunda está lá, e ele pode trocá-la antes de submeter

#### Scenario: A submissão leva todas as respostas de uma vez

- **WHEN** o Guerreiro(a) percorre as seis perguntas do quiz e conclui
- **THEN** as seis respostas vão numa única submissão, ao fim, nunca uma por pergunta

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

#### Scenario: Pergunta sem resposta é sinalizada

- **WHEN** o Guerreiro(a) tenta enviar o quiz com uma pergunta ainda sem alternativa escolhida
- **THEN** a tela aponta a pergunta que falta, leva o Guerreiro(a) até ela e não envia

#### Scenario: Não passar convida a tentar de novo

- **WHEN** o Guerreiro(a) submete o quiz e não passa
- **THEN** a tela diz quantas perguntas ele acertou, de quantas, e o convida a tentar de novo,
  sem punição e sem exibir contagem de fracassos

#### Scenario: A sondagem não fala em aprovação

- **WHEN** o Guerreiro(a) responde a missão de sondagem
- **THEN** a tela agradece e segue para a trilha, sem dizer que ele passou ou não passou
