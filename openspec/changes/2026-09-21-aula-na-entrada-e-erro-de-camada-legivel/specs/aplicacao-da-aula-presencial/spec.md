## MODIFIED Requirements

### Requirement: O Guerreiro(a) entra por nick e imagem, e a presença é registrada na entrada

A App 01 SHALL oferecer, no caminho das trilhas, a entrada por **nick e imagem**: o nick
informado na tela e o **descritor gerado no próprio aparelho**, na ordem prova de vivacidade e
depois descritor facial. Ao núcleo SHALL ir apenas o descritor; a fotografia SHALL ser
descartada sem sair do aparelho e NEVER SHALL ser gravada nem enviada.

A aplicação SHALL informar ao núcleo, no mesmo pedido, a **aula em curso** — é ela que
determina o ponto de apoio e, com ele, o limiar da comparação. A aula já é propriedade da tela
da entrada, herdada da sessão de trabalho do aparelho, e NEVER SHALL ser digitada nem escolhida
por quem opera. (`RF-04-18`, `RF-01-73`)

A tela SHALL apresentar o **visor ao vivo** da câmera enquanto a captura acontece, e SHALL
detectar **em laço** até a vivacidade passar ou o tempo se esgotar, em vez de julgar um único
quadro. O **quadro capturado** NEVER SHALL voltar à tela. (`RF-04-64`, `RN-04-34`)

O **retorno abstrato do laço** — rosto procurado, rosto encontrado, pessoa confirmada — SHALL
valer apenas enquanto a captura acontece, e NEVER SHALL permanecer na tela depois de a
tentativa ter desfecho. Nenhuma tela SHALL apresentar, ao mesmo tempo, o retorno do laço e o
desfecho da tentativa: quem opera leria as duas frases como um único julgamento contraditório.
(`RF-04-64`, `RN-04-34`)

Reconhecido o Guerreiro(a), a aplicação SHALL abrir a sessão dele e SHALL registrar a
**presença do dia no modo reconhecimento**, no mesmo atendimento. Presença já constante do
encontro NEVER SHALL ser duplicada nem tratada como erro: a aplicação SHALL avisar que ela já
existe e voltar à tela inicial. (`RF-04-18`, `RF-04-19`, `RF-04-29`, `RN-04-12`, `RN-04-06`,
PRD-04 §5.4)

#### Scenario: Nick e imagem conferem

- **WHEN** o Guerreiro(a) informa o nick e a câmera captura a imagem dele na chegada
- **THEN** a aplicação abre a sessão do Guerreiro(a) e registra a presença do dia por
  reconhecimento

#### Scenario: A entrada declara ao núcleo a aula em curso

- **WHEN** a aplicação pede a abertura da sessão por reconhecimento
- **THEN** o pedido carrega a aula do encontro, além do nick e do descritor, e quem opera não
  digitou nem escolheu aula alguma

#### Scenario: A presença do encontro já constava

- **WHEN** um Guerreiro(a) já com presença registrada naquela aula é reconhecido de novo
- **THEN** a aplicação avisa que a presença já existe, não duplica registro algum e volta à
  tela inicial

#### Scenario: Nenhuma imagem de criança sai do aparelho

- **WHEN** a entrada por nick e imagem acontece
- **THEN** nenhuma requisição carrega fotografia, e nenhuma imagem fica gravada no aparelho
  compartilhado

#### Scenario: Quem chega se vê no visor antes de a captura julgar

- **WHEN** a entrada por nick e imagem abre a câmera
- **THEN** o visor ao vivo aparece na tela, e a detecção segue em laço até aprovar ou o tempo
  se esgotar

#### Scenario: O retorno do laço não sobrevive à recusa do núcleo

- **WHEN** a vivacidade é confirmada e, em seguida, o núcleo recusa a abertura da sessão
- **THEN** a tela apresenta apenas a frase da recusa, e o retorno do laço já não está na tela

#### Scenario: O retorno do laço não sobrevive à falha de preparo nem à vivacidade reprovada

- **WHEN** a tentativa termina por preparo que falhou ou por vivacidade reprovada
- **THEN** a tela apresenta apenas a frase daquele desfecho, sem o retorno do laço ao lado

#### Scenario: Sem câmera, a entrada segue pela confirmação humana

- **WHEN** o aparelho não tem câmera disponível
- **THEN** a aplicação não oferece a captura e encaminha o Guerreiro(a) à confirmação de Mestre
  ou Admin, sem deixá-lo fora da aula

### Requirement: A falha de identificação oferece nova tentativa sem revelar nada

A App 01 SHALL responder à **recusa da conferência** com a **mesma frase** em todos os casos
que o núcleo funde numa recusa só — nick inexistente, Guerreiro(a) sem _template_ gravado,
descritor que não confere, ponto de apoio sem limiar medido e aula que não vale para aquele
Guerreiro(a) —, sem revelar qual deles ocorreu, e SHALL oferecer **nova tentativa** de captura.
Persistindo a falha, a aplicação SHALL encaminhar à **confirmação de Mestre ou Admin**, e
NEVER SHALL encerrar o atendimento deixando o Guerreiro(a) fora da aula. (`RF-04-20`,
`RN-01-22`, `RN-01-56`, `RN-04-09`, PRD-04 §5.5)

Essa frase SHALL valer **apenas** para a recusa que o núcleo declarou como tal. Erro que o
núcleo declara no corpo único — validação, chave, freio por origem — e falha que não chega a
ele, como a de rede, NEVER SHALL ser apresentado como recusa do reconhecimento: a tela SHALL
apresentar a causa declarada, pelo que ela é. Disfarçar falha de camada de rosto que não
confere esconde defeito que o núcleo já nomeou na resposta. (`RN-04-36`, `RF-01-27`)

O tratamento da recusa SHALL alcançar **apenas a conferência**. O que roda depois dela —
leitura de quem entrou, registro da presença e abertura da sessão local — SHALL ter tratamento
próprio, porque falha ali acontece com o rosto **já reconhecido** e NEVER SHALL ser apresentada
como recusa dele. (`RN-04-36`, `RF-04-18`)

#### Scenario: A imagem não confere

- **WHEN** o núcleo recusa a abertura da sessão por nick e imagem
- **THEN** a aplicação oferece nova tentativa com uma frase que não diz se o nick existe

#### Scenario: A falha persiste

- **WHEN** as tentativas de reconhecimento seguem falhando
- **THEN** a aplicação oferece o caminho da confirmação de Mestre ou Admin, que abre a sessão e
  registra a presença

#### Scenario: A frase da recusa não varia com a causa

- **WHEN** se comparam as telas de recusa de um nick inexistente e de um descritor que não
  confere
- **THEN** elas são indistinguíveis para quem está diante do aparelho

#### Scenario: Erro de validação não se disfarça de rosto que não confere

- **WHEN** o núcleo recusa o pedido da sessão por erro de validação, declarando o campo em
  falta no corpo único
- **THEN** a tela apresenta o que o núcleo declarou, e não a frase da recusa do reconhecimento

#### Scenario: Falha depois do reconhecimento não se disfarça de recusa

- **WHEN** o núcleo confere o rosto e, em seguida, falha o registro da presença ou a leitura de
  quem entrou
- **THEN** a tela apresenta aquela falha pelo que ela é, e NEVER diz que o rosto não foi
  reconhecido
