# aplicacao-da-aula-presencial Specification

## Purpose

A App 01 é a aplicação do encontro presencial, usada pelos próprios Guerreiros e Guerreiras no
aparelho do ponto de apoio. Esta capacidade cobre a sessão de trabalho do aparelho — que só
existe dentro da janela de uma aula agendada e é dela que sai a comunidade —, a tela inicial dos
dois caminhos, a entrada do Guerreiro(a) no encontro e a formação da equipe da aula.

## Requirements

### Requirement: A App 01 se identifica por chave e só opera dentro da janela de uma aula agendada

A App 01 SHALL apresentar a chave de aplicação dela em toda chamada ao núcleo. A aplicação
SHALL consultar as aulas vigentes para a data e a hora correntes e, **não havendo nenhuma**,
NEVER SHALL abrir: SHALL informar em **uma frase** que não há aula agendada, sem oferecer
caminho algum. (`RF-04-02`, `RN-04-01`, `RF-01-02`, PRD-04 §12)

#### Scenario: A chave acompanha toda chamada

- **WHEN** a aplicação chama qualquer rota de dados do núcleo
- **THEN** a chamada leva a chave de aplicação da App 01 do ambiente em que ela roda

#### Scenario: Sem aula vigente a aplicação não abre

- **WHEN** o aparelho é aberto fora da janela de qualquer aula agendada
- **THEN** a aplicação informa em uma frase que não há aula agendada, e nem o onboarding nem as
  trilhas ficam alcançáveis

#### Scenario: Nenhuma aula vigente não é erro

- **WHEN** a consulta de aulas vigentes devolve conjunto vazio
- **THEN** a aplicação trata a resposta como situação normal, sem apresentar código de erro cru

### Requirement: A comunidade vem da aula vigente, perguntada uma única vez

A App 01 SHALL adotar a comunidade da aula vigente sem perguntá-la a ninguém quando houver
**uma** aula. Havendo **mais de uma**, SHALL perguntar **uma única vez** em qual comunidade o
aparelho está operando e SHALL usar essa escolha até o fim da sessão de trabalho, sem repetir a
pergunta. O Guerreiro(a) NEVER SHALL informar a comunidade. (`RF-04-03`, `RN-04-02`, PRD-04 §12)

#### Scenario: Uma aula vigente dispensa a pergunta

- **WHEN** há exatamente uma aula vigente
- **THEN** a aplicação adota a comunidade daquela aula e não pergunta nada

#### Scenario: Duas aulas vigentes perguntam uma vez

- **WHEN** há duas aulas vigentes em comunidades diferentes
- **THEN** a aplicação pergunta uma única vez em qual comunidade opera

#### Scenario: A escolha não se repete na sessão

- **WHEN** a comunidade já foi escolhida e novos atendimentos acontecem na mesma sessão de
  trabalho
- **THEN** a aplicação segue na comunidade escolhida, sem perguntar de novo

### Requirement: A sessão de trabalho do aparelho é aberta por Mestre ou Admin e cai com a janela da aula

A App 01 SHALL exigir que a sessão de trabalho do aparelho seja aberta por **Mestre ou Admin**
autenticado por login social. A sessão SHALL valer pela **janela da aula agendada** e, encerrado
o horário final declarado no agendamento, a aplicação SHALL exigir nova autenticação do Mestre
ou do Admin antes de qualquer novo atendimento. (`RF-04-05`, `RN-04-29`, PRD-04 §13)

#### Scenario: Mestre abre a sessão de trabalho

- **WHEN** um Mestre autentica pela conta social no aparelho
- **THEN** a aplicação abre a sessão de trabalho e apresenta a tela inicial

#### Scenario: Admin abre a sessão de trabalho

- **WHEN** um Admin autentica pela conta social no aparelho
- **THEN** a aplicação abre a sessão de trabalho e apresenta a tela inicial

#### Scenario: Guerreiro(a) não abre a sessão de trabalho

- **WHEN** alguém tenta abrir a sessão de trabalho do aparelho com credencial de Guerreiro(a)
- **THEN** a aplicação recusa em linguagem simples e nenhuma sessão de trabalho é aberta

#### Scenario: Encerrada a janela, o aparelho exige nova autenticação

- **WHEN** o horário final da aula agendada passa
- **THEN** a aplicação encerra a sessão de trabalho e exige nova autenticação de Mestre ou Admin

### Requirement: A tela inicial encerra a sessão de trabalho, com o PIN de quem a abriu

A App 01 SHALL oferecer, **na tela inicial e somente nela**, o encerramento da sessão de trabalho do
aparelho. NEVER SHALL oferecê-lo nas telas de atendimento: a tela inicial é a que aparece entre um
atendimento e o seguinte (`RF-04-28`), e a criança que encerrasse a sessão no meio do atendimento
dela derrubaria a de quem abriu o aparelho — que só volta por login Google, indisponível sem rede.
(`RF-04-71`, `RF-04-05`)

O encerramento SHALL exigir o **PIN de quem abriu o aparelho**, digitado no ato, conferido contra o
verificador que a sessão de trabalho já guarda. O PIN NEVER SHALL ser gravado no aparelho, e a
conferência NEVER SHALL depender de rede: é a mesma conferência que a confirmação de identidade já
faz sem rede. (`RF-04-71`, `RN-04-41`, `RN-04-38`)

O contador de erros seguidos SHALL ser **o mesmo** da confirmação de identidade e da bancada de
medição: errar o PIN em qualquer um dos três SHALL contar para os três, e o bloqueio de cinco erros
SHALL recusar os três. (`RN-04-41`, `RN-04-38`)

Com o PIN **bloqueado**, a aplicação SHALL recusar o encerramento e SHALL dizer como fechar o
aparelho mesmo assim — a sessão de trabalho não sobrevive ao fechamento da aba. NEVER SHALL deixar o
aparelho sem saída alguma: a recusa sem alternativa trancaria o encontro. (`RN-04-41`)

Quem abriu o aparelho **sem PIN cadastrado** SHALL encerrar sem PIN, com o aviso que a aplicação já
apresenta nesse caso. (`RN-04-41`, `RN-04-38`)

Havendo **presença na fila local** ainda não sincronizada, a aplicação SHALL avisar antes de
encerrar, dizendo quantas aguardam e que a sincronização exige o aparelho aberto naquela aula.
NEVER SHALL descartar a fila ao encerrar: ela sobrevive ao encerramento e à recarga da página.
(`RF-04-71`, `RF-04-23`, `RF-04-25`)

Encerrada a sessão de trabalho, a aplicação SHALL descartar o verificador do PIN e SHALL voltar à
tela de abertura do aparelho, sem dado de atendimento algum em tela. (`RF-04-71`, `RF-04-28`,
`RN-04-38`)

#### Scenario: A saída existe na tela inicial e só nela

- **WHEN** a sessão de trabalho está aberta
- **THEN** a tela inicial apresenta o encerramento da sessão de trabalho, e nenhuma tela de
  atendimento o apresenta

#### Scenario: Encerrar pede o PIN de quem abriu

- **WHEN** quem opera aciona o encerramento e digita o PIN correto de quem abriu o aparelho
- **THEN** a sessão de trabalho encerra, o verificador é descartado e a aplicação volta à tela de
  abertura

#### Scenario: PIN errado no encerramento conta no mesmo contador

- **WHEN** o PIN digitado no encerramento está errado
- **THEN** a aplicação recusa o encerramento, o erro conta no mesmo contador da confirmação de
  identidade, e a sessão de trabalho continua aberta

#### Scenario: PIN bloqueado recusa, mas diz como fechar o aparelho

- **WHEN** o PIN está bloqueado por cinco erros seguidos e alguém aciona o encerramento
- **THEN** a aplicação recusa e diz que fechar a aba do navegador encerra a sessão de trabalho

#### Scenario: Sem PIN cadastrado, encerrar passa

- **WHEN** quem abriu o aparelho não tem PIN cadastrado e aciona o encerramento
- **THEN** a sessão de trabalho encerra, com o aviso de PIN não cadastrado que a aplicação já
  apresenta

#### Scenario: A fila local pendente é anunciada antes de encerrar

- **WHEN** há presença na fila local ainda não sincronizada e alguém aciona o encerramento
- **THEN** a aplicação diz quantas aguardam e que a sincronização exige o aparelho aberto naquela
  aula, antes de encerrar

#### Scenario: Encerrar não descarta a fila

- **WHEN** a sessão de trabalho é encerrada com presença na fila local
- **THEN** a fila continua guardada no aparelho, e sincroniza quando o aparelho for reaberto
  naquela aula

### Requirement: O aparelho entra na partida pela sessão do Guerreiro(a), e a equipe vem do núcleo

A App 01 SHALL levar quem escolhe o caminho do quiz à **entrada do Guerreiro(a) por nick e
imagem** quando não houver sessão dele aberta, nunca ao cadastro — o mesmo caminho da entrada
já em uso. Aberta a sessão, a aplicação SHALL perguntar ao núcleo as partidas da aula e SHALL
usar **a equipe que o núcleo derivou**, sem oferecer escolha de equipe em tela alguma. O
vínculo entre o aparelho e a equipe é **estado do próprio aparelho**, guardado na sessão dele e
desfeito ao fim do atendimento; a aplicação NEVER SHALL enviá-lo ao núcleo como registro nem
supor que o núcleo o guarde (documento 05 §5, decisão do fundador de 2026-08-25).

Não havendo partida na aula, ou não disputando o Guerreiro(a) por nenhuma equipe, a aplicação
SHALL dizê-lo em uma frase e SHALL oferecer a volta ao início, sem tela de resposta.
(`RF-04-41`, `RF-04-42`)

#### Scenario: Sem sessão aberta, o quiz leva à entrada

- **WHEN** alguém escolhe o caminho do quiz sem sessão de Guerreiro(a) aberta
- **THEN** a aplicação apresenta a entrada por nick e imagem, e nenhuma tela de cadastro aparece

#### Scenario: A equipe não é escolhida em tela

- **WHEN** o Guerreiro(a) entra e o núcleo devolve a equipe pela qual ele disputa
- **THEN** a aplicação usa aquela equipe, e em nenhum momento pede que ele escolha entre equipes

#### Scenario: Sem partida, a tela explica e volta

- **WHEN** a aula não tem partida aberta, ou o Guerreiro(a) não disputa por nenhuma equipe
- **THEN** a aplicação explica em uma frase e oferece a volta ao início, sem tela de resposta

#### Scenario: O atendimento seguinte não herda a equipe

- **WHEN** o atendimento termina e outro Guerreiro(a) entra no mesmo aparelho
- **THEN** a equipe do atendimento anterior não aparece, e a do novo vem do núcleo

### Requirement: A tela da partida acompanha a pergunta por sondagem a cada 2 segundos

A App 01 SHALL manter a tela da partida atualizada **sondando o núcleo a cada 2 segundos**, sem
recarga manual e sem conexão longa (documento 03 §1, decisão do fundador de 2026-08-25). A
pergunta no ar SHALL aparecer com o enunciado e as quatro alternativas. Sondagem que falha por
rede NEVER SHALL derrubar a partida nem apagar o que já está na tela: a aplicação SHALL avisar
que perdeu contato e SHALL retomar a pergunta corrente na sondagem seguinte, ainda que outra
tenha entrado no ar enquanto o aparelho esteve fora. (`RF-04-41`, `RF-04-58`, PRD-04 §12)

#### Scenario: A pergunta aparece sem recarga

- **WHEN** quem conduz põe uma pergunta no ar
- **THEN** ela aparece no aparelho da equipe na sondagem seguinte, sem que ninguém recarregue

#### Scenario: A rede caída no meio da pergunta não tira a equipe da partida

- **WHEN** a rede cai durante uma pergunta e volta depois de outra ter entrado no ar
- **THEN** a tela avisa que perdeu contato, mantém o que exibia e passa a mostrar a pergunta
  corrente, sem recuperar a que perdeu

#### Scenario: Entre uma pergunta e outra a tela espera

- **WHEN** nenhuma pergunta está no ar
- **THEN** a aplicação diz que a próxima pergunta está por vir, sem oferecer resposta

### Requirement: A equipe responde uma vez, e a aplicação recusa a segunda antes de enviar

A App 01 SHALL enviar **uma** resposta por equipe e pergunta e SHALL recusar a segunda **antes
de chegar ao núcleo**, dizendo em linguagem simples que a equipe já respondeu. A resposta
enviada SHALL valer para todos os integrantes da equipe. Recusada a segunda pelo núcleo — por
reenvio que cruzou com outro aparelho da mesma equipe —, a aplicação SHALL apresentar a mesma
mensagem, sem tratar a recusa como erro do aparelho. Enviada a resposta, a alternativa
escolhida SHALL permanecer em tela até a pergunta seguinte. (`RF-04-43`, PRD-04 §12)

#### Scenario: A equipe responde e a escolha fica em tela

- **WHEN** a equipe escolhe uma alternativa e envia
- **THEN** a aplicação confirma o envio e mantém a alternativa escolhida em tela até a pergunta
  seguinte

#### Scenario: A segunda tentativa é recusada na tela

- **WHEN** alguém tenta responder de novo a mesma pergunta no mesmo aparelho
- **THEN** a aplicação recusa antes de enviar, dizendo que a equipe já respondeu

#### Scenario: A recusa do núcleo por outro aparelho da equipe não vira erro

- **WHEN** o núcleo recusa a resposta porque outro aparelho da mesma equipe já respondeu
- **THEN** a aplicação apresenta a mesma mensagem de que a equipe já respondeu, sem tela de erro

### Requirement: O resultado aparece à equipe quando quem conduz o libera

A App 01 SHALL manter oculto o resultado da pergunta enquanto quem conduz não o liberar, e
NEVER SHALL revelar a alternativa correta antes disso. Liberado, a aplicação SHALL apresentar a
**alternativa correta**, **se a equipe acertou** e **qual equipe chegou primeiro**. A aplicação
NEVER SHALL exibir pontuação da partida: o crédito é do encerramento e aparece pelos pontos do
Guerreiro(a), não por esta tela. (`RF-04-44`)

#### Scenario: Antes da liberação nada do resultado aparece

- **WHEN** a equipe respondeu e quem conduz ainda não liberou o resultado
- **THEN** a tela não mostra a alternativa correta nem diz se a equipe acertou

#### Scenario: Liberado, a equipe vê se acertou

- **WHEN** quem conduz libera o resultado
- **THEN** a tela mostra a alternativa correta, se a equipe acertou e qual equipe chegou
  primeiro

#### Scenario: A tela da partida não mostra pontuação

- **WHEN** o resultado de qualquer pergunta é liberado
- **THEN** nenhuma pontuação da partida aparece em tela

### Requirement: Sem rede, a resposta de quiz fica indisponível e a partida não trava

A App 01 SHALL manter legível a pergunta já carregada quando a rede cair, e SHALL apresentar a
resposta como **indisponível** enquanto não houver rede, dizendo-o em uma frase. A aplicação
NEVER SHALL enfileirar resposta de quiz para envio posterior — a ordem de chegada no servidor é
o critério de desempate, e resposta atrasada falsearia a disputa. Voltando a rede, a aplicação
SHALL retomar a sondagem e SHALL permitir a resposta da pergunta corrente, se a equipe ainda
não respondeu. (`RF-04-58`, documento 05 §5)

#### Scenario: A pergunta carregada continua legível sem rede

- **WHEN** a rede cai com uma pergunta em tela
- **THEN** o enunciado e as alternativas continuam legíveis

#### Scenario: Sem rede a resposta não é oferecida

- **WHEN** a equipe tenta responder com o aparelho sem rede
- **THEN** a aplicação diz que a resposta está indisponível sem rede, e nada é enfileirado

#### Scenario: Voltando a rede, a equipe responde a pergunta corrente

- **WHEN** a rede volta e a equipe ainda não respondeu a pergunta corrente
- **THEN** a aplicação retoma a sondagem e oferece a resposta

### Requirement: O momento de troca é aberto e fechado pelo Mestre, e só por ele

A App 01 SHALL oferecer a **abertura e o fechamento do momento de troca** apenas quando a sessão
de trabalho do aparelho for de um **Mestre**. Aparelho cuja sessão de trabalho for de **Admin**
NEVER SHALL oferecer a abertura, porque o registro da troca é ato do Mestre que entrega e o
núcleo recusa o de qualquer outro papel.

O momento SHALL começar **fechado** e SHALL ser um estado do próprio aparelho, sem registro no
núcleo. Perdido esse estado — recarga da página ou queda da sessão de trabalho —, o momento
SHALL voltar a **fechado**, e NEVER SHALL reabrir sozinho.

O momento NEVER SHALL abrir **sem rede**: a troca inteira é operação do núcleo, e não entra em
fila local. Fora do momento aberto, o catálogo avulso NEVER SHALL ser oferecido em tela alguma.
(`RF-04-49`, `RF-04-57`, `RN-04-27`, `RN-04-29`, PRD-04 §§5.10, 12)

#### Scenario: O Mestre abre o momento de troca

- **WHEN** o Mestre que abriu a sessão de trabalho do aparelho abre o momento de troca no
  encerramento do encontro
- **THEN** a aplicação passa a oferecer a troca aos Guerreiros e Guerreiras

#### Scenario: Aparelho aberto por Admin não oferece a troca

- **WHEN** a sessão de trabalho do aparelho é de um Admin
- **THEN** a aplicação não oferece a abertura do momento de troca, e nenhuma tela de catálogo
  aparece

#### Scenario: Fora do momento, o catálogo não aparece

- **WHEN** o momento de troca está fechado
- **THEN** o catálogo avulso não é oferecido em tela alguma, e não há caminho que chegue a ele

#### Scenario: Sem rede o momento não abre

- **WHEN** o Mestre tenta abrir o momento de troca com o aparelho sem rede
- **THEN** a aplicação recusa a abertura, explica que a troca exige rede e não enfileira nada

#### Scenario: O momento começa e volta a ficar fechado

- **WHEN** a aplicação é recarregada com o momento de troca aberto
- **THEN** o momento volta a ficar fechado, e o Mestre precisa abri-lo de novo

### Requirement: O Guerreiro(a) vê o catálogo da sua comunidade, o preço e o próprio saldo

Aberto o momento de troca, o Guerreiro(a) SHALL entrar pelo **nick e pela imagem**, pelo mesmo
caminho de entrada das trilhas, e a aplicação SHALL exibir o **catálogo avulso da comunidade
dele**, com o **preço em pontos extras** e o **estoque restante** de cada item, e o **saldo
disponível** de pontos extras dele.

A aplicação SHALL exibir o **saldo disponível**, e NEVER SHALL exibir o **acumulado** nesta tela:
o que a criança precisa saber é o que dá para trocar hoje. Item com **estoque zero** NEVER SHALL
ser oferecido para troca, ainda que o núcleo o devolva ativo no catálogo. Nenhuma tela desta
aplicação SHALL oferecer **ponto regular** como moeda de troca, e preço e diferença SHALL
aparecer sempre em **pontos**, nunca em reais nem em moedas da plataforma. (`RF-04-50`,
`RF-04-51`, `RF-04-54`, `RF-04-56`, `RN-04-23`, `RN-04-28`, PRD-04 §§5.10, 12)

#### Scenario: O catálogo da comunidade aparece com preço e estoque

- **WHEN** o Guerreiro(a) entra no momento de troca
- **THEN** a aplicação exibe os itens do catálogo avulso da comunidade dele, cada um com o preço
  em pontos extras e o estoque restante

#### Scenario: O saldo aparece, o acumulado não

- **WHEN** a tela da troca exibe o que o Guerreiro(a) tem
- **THEN** ela mostra o saldo disponível de pontos extras e não mostra o acumulado

#### Scenario: Item sem estoque não é oferecido

- **WHEN** o catálogo traz um item ativo cujo estoque é zero
- **THEN** esse item não aparece entre os que dá para trocar

#### Scenario: Ponto regular nunca é moeda

- **WHEN** qualquer tela da troca é exibida
- **THEN** nenhum ponto regular aparece como moeda, e nenhum preço aparece em reais nem em
  moedas da plataforma

### Requirement: O Mestre confirma a entrega, e a troca acontece num ato só

Escolhido o item, a aplicação SHALL registrar a troca **na confirmação da entrega pelo Mestre**,
num único envio ao núcleo. O envio SHALL ir **sob a sessão de trabalho do aparelho** — é o Mestre
que entrega, e é ele o autor da troca —, e o Guerreiro(a) SHALL ser identificado pela **persona
da sessão aberta na entrada**, NEVER por nick digitado nem por busca de persona.

Confirmada a troca, a aplicação SHALL voltar à tela inicial, pronta para o próximo. NEVER SHALL
haver reserva, fila ou promessa de entrega em encontro seguinte. (`RF-04-52`, `RF-04-55`,
`RN-04-24`, `RN-04-27`, `RF-04-28`, PRD-04 §§5.10, 12)

#### Scenario: A confirmação da entrega é o envio

- **WHEN** o Mestre confirma a entrega do item escolhido
- **THEN** a aplicação registra a troca num único envio, e a entrega não fica pendente de
  nenhum passo posterior

#### Scenario: O Guerreiro(a) vem da sessão, não de um nick

- **WHEN** a troca é registrada
- **THEN** o Guerreiro(a) da troca é o da sessão aberta na entrada, e nenhum nick é digitado nem
  consultado para identificá-lo

#### Scenario: O saldo cai o preço e o acumulado não muda

- **WHEN** uma troca de um item de 40 pontos extras é confirmada para um Guerreiro(a) de saldo
  disponível 100 e acumulado 300
- **THEN** a tela seguinte mostra saldo disponível 60, e o acumulado segue 300

#### Scenario: Feita a troca, o atendimento termina

- **WHEN** a troca é confirmada
- **THEN** a aplicação volta à tela inicial e não exibe dado do atendimento anterior

### Requirement: A recusa por saldo diz a diferença em pontos

A aplicação SHALL recusar a troca cujo preço for maior que o saldo disponível do Guerreiro(a),
dizendo a **diferença em pontos** que falta — nunca em reais nem em moedas da plataforma —, e
NEVER SHALL enviar ao núcleo uma troca que já sabe recusada.

Mudando o saldo ou o estoque entre a leitura da tela e o envio, a recusa do núcleo SHALL ser
apresentada em linguagem simples, dizendo qual condição barrou, e o Guerreiro(a) SHALL poder
escolher outro item sem recomeçar a entrada. (`RF-04-53`, `RN-04-25`, `RN-04-28`, PRD-04 §12)

#### Scenario: Saldo insuficiente é recusado com a diferença

- **WHEN** um Guerreiro(a) de saldo disponível 25 escolhe um item de 40 pontos extras
- **THEN** a aplicação recusa a troca dizendo que faltam 15 pontos, e nada é enviado ao núcleo

#### Scenario: A recusa do núcleo é dita em linguagem simples

- **WHEN** o núcleo recusa a troca porque o saldo ou o estoque mudou depois da leitura da tela
- **THEN** a aplicação diz qual condição barrou, em linguagem simples, e oferece a escolha de
  outro item sem repetir a entrada

### Requirement: O Guerreiro(a) entra por nick e imagem, e só o caminho Presença registra a presença

A App 01 SHALL oferecer, nos caminhos que pedem o Guerreiro(a) — **presença**, **equipes**,
**quiz** e **troca** —, a entrada por **nick e imagem**: o nick informado na tela e o
**descritor gerado no próprio aparelho**, na ordem prova de vivacidade e depois descritor
facial. Ao núcleo SHALL ir apenas o descritor; a fotografia SHALL ser descartada sem sair do
aparelho e NEVER SHALL ser gravada nem enviada.

A tela da entrada SHALL anunciar **qual caminho serve**, para que quem escolheu equipes, quiz
ou troca na tela inicial reconheça que chegou ao caminho escolhido, e não ao da presença. O
anúncio SHALL valer nas duas formas da entrada — a por nick e imagem e a por confirmação de
Mestre ou Admin —, que NEVER SHALL se apresentar com o mesmo enunciado nos quatro caminhos.
O que a entrada **faz** em cada caminho não muda com isso. (`RF-04-01`, `RF-04-67`,
`RF-04-68`)

A aplicação SHALL informar ao núcleo, no mesmo pedido, a **aula em curso** — é ela que determina
o ponto de apoio e, com ele, o limiar da comparação. A aula já é propriedade da tela da entrada,
herdada da sessão de trabalho do aparelho, e NEVER SHALL ser digitada nem escolhida por quem
opera. (`RF-04-18`, `RF-01-73`)

A tela SHALL apresentar o **visor ao vivo** da câmera enquanto a captura acontece, e SHALL
detectar **em laço** até a vivacidade passar ou o tempo se esgotar, em vez de julgar um único
quadro. O **quadro capturado** NEVER SHALL voltar à tela. (`RF-04-64`, `RN-04-34`)

O **retorno abstrato do laço** — rosto procurado, rosto encontrado, pessoa confirmada — SHALL
valer apenas enquanto a captura acontece, e NEVER SHALL permanecer na tela depois de a tentativa
ter desfecho. Nenhuma tela SHALL apresentar, ao mesmo tempo, o retorno do laço e o desfecho da
tentativa: quem opera leria as duas frases como um único julgamento contraditório. (`RF-04-64`,
`RN-04-34`)

Reconhecido o Guerreiro(a), a aplicação SHALL abrir a sessão dele. O registro da **presença do
dia no modo reconhecimento** SHALL acontecer **apenas no caminho presença**, no mesmo
atendimento; nos caminhos equipes, quiz e troca a entrada NEVER SHALL registrar presença nem
tratá-la como parte do reconhecimento. Presença já constante do encontro NEVER SHALL ser
duplicada nem tratada como erro: no caminho presença a aplicação SHALL avisar que ela já existe
e voltar à tela inicial. (`RF-04-18`, `RF-04-19`, `RF-04-29`, `RF-04-67`, `RN-04-12`,
`RN-04-06`, PRD-04 §5.4)

#### Scenario: Nick e imagem conferem

- **WHEN** o Guerreiro(a) informa o nick e a câmera captura a imagem dele na chegada, pelo
  caminho da presença
- **THEN** a aplicação abre a sessão do Guerreiro(a) e registra a presença do dia por
  reconhecimento

#### Scenario: Nos demais caminhos a entrada não registra presença

- **WHEN** o Guerreiro(a) entra por nick e imagem pelo caminho das equipes, do quiz ou da troca
- **THEN** a aplicação abre a sessão dele e nenhuma requisição de presença é enviada

#### Scenario: A entrada declara ao núcleo a aula em curso

- **WHEN** a aplicação pede a abertura da sessão por reconhecimento
- **THEN** o pedido carrega a aula do encontro, além do nick e do descritor, e quem opera não
  digitou nem escolheu aula alguma

#### Scenario: A presença do encontro já constava

- **WHEN** um Guerreiro(a) já com presença registrada naquela aula é reconhecido de novo pelo
  caminho da presença
- **THEN** a aplicação avisa que a presença já existe, não duplica registro algum e volta à tela
  inicial

#### Scenario: Nenhuma imagem de criança sai do aparelho

- **WHEN** a entrada por nick e imagem acontece
- **THEN** nenhuma requisição carrega fotografia, e nenhuma imagem fica gravada no aparelho
  compartilhado

#### Scenario: Quem chega se vê no visor antes de a captura julgar

- **WHEN** a entrada por nick e imagem abre a câmera
- **THEN** o visor ao vivo aparece na tela, e a detecção segue em laço até aprovar ou o tempo se
  esgotar

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

#### Scenario: A entrada anuncia o caminho que serve

- **WHEN** a entrada do Guerreiro(a) é aberta pelo caminho das equipes, do quiz ou da troca
- **THEN** a tela se anuncia pelo caminho escolhido, distinta da entrada do caminho da presença,
  tanto na forma por nick e imagem quanto na por confirmação de Mestre ou Admin

### Requirement: A falha de identificação oferece nova tentativa sem revelar nada

A App 01 SHALL responder à **recusa da conferência** com a **mesma frase** em todos os casos
que o núcleo funde numa recusa só — nick inexistente, Guerreiro(a) sem _template_ gravado,
descritor que não confere, ponto de apoio sem limiar medido e aula que não vale para aquele
Guerreiro(a) —, sem revelar qual deles ocorreu, e SHALL oferecer **nova tentativa** de captura.
Persistindo a falha, a aplicação SHALL encaminhar à **confirmação de Mestre ou Admin**, e
NEVER SHALL encerrar o atendimento deixando o Guerreiro(a) fora da aula. (`RF-04-20`,
`RN-01-22`, `RN-01-56`, `RN-04-09`, PRD-04 §5.5)

A mesma frase SHALL valer para os desfechos da **captura local** que dizem à criança a mesma
coisa — vivacidade reprovada e descritor que o aparelho não conseguiu gerar —, porque distingui-
los revelaria o que o `RF-04-20` manda esconder.

O que essa frase NEVER SHALL cobrir é a **falha de camada**: erro que o núcleo declara no corpo
único — validação, chave, freio por origem — e falha que não chega a ele, como a de rede. Nesses
casos a tela SHALL apresentar a causa declarada, pelo que ela é. Disfarçar falha de camada de
rosto que não confere esconde defeito que o núcleo já nomeou na resposta. (`RN-04-36`,
`RF-01-27`)

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

### Requirement: O Guerreiro(a) entra por confirmação de Mestre ou Admin, em qualquer caminho

A App 01 SHALL abrir a sessão do Guerreiro(a) pela **confirmação de identidade** feita pelo
Mestre ou Admin **que abriu a sessão de trabalho**, presente ao lado da criança, com registro de
quem confirmou. No **caminho presença**, a aplicação SHALL registrar, no mesmo ato, a **presença
do dia no modo confirmação**, com o mesmo adulto como confirmador; nos caminhos equipes, quiz e
troca a confirmação NEVER SHALL registrar presença (`RF-04-67`). A recusa de biometria e a
ausência de _template_ NEVER SHALL deixar o Guerreiro(a) fora da aula: a confirmação humana é a
alternativa equivalente.

A confirmação humana é o que o `RN-04-09` sempre disse que ela era — a alternativa de quem não
tem _template_, de quem recusou a biometria e de quem a câmera não reconheceu. A sessão que ela
abre SHALL ter os mesmos direitos da aberta por reconhecimento. (`RF-04-29`, `RF-04-15`,
`RF-04-21`, `RN-04-09`, PRD-04 §§5.3, 5.5)

Tocar em "Chamar Mestre ou Admin" SHALL levar a uma tela que pede o **nick** da criança e o
**PIN** do adulto, com o PIN mascarado. A sessão de trabalho aberta no aparelho, sozinha, NEVER
SHALL confirmar: sem o PIN digitado no ato, o botão de confirmar não age. PIN errado SHALL ser
dito como PIN errado, sem apagar o nick; PIN bloqueado e PIN não cadastrado SHALL ser ditos como
o que são — o bloqueado manda refazer o login Google, e o não cadastrado manda cadastrar o PIN
na App 09 ou na App 03. O campo do PIN SHALL ser limpo a cada tentativa e ao fim de cada
atendimento, e o PIN NEVER SHALL ser gravado no aparelho. (`RF-04-21`, `RN-04-37`, `RN-04-38`)

#### Scenario: Mestre confirma e a sessão do Guerreiro(a) abre

- **WHEN** o Guerreiro(a) informa o nick e o Mestre que abriu a sessão de trabalho digita o
  próprio PIN, no caminho da presença
- **THEN** a aplicação abre a sessão do Guerreiro(a), registra quem confirmou e grava a presença
  do dia por confirmação

#### Scenario: A confirmação fora do caminho da presença não registra presença

- **WHEN** a confirmação com PIN abre a sessão pelo caminho das equipes, do quiz ou da troca
- **THEN** a aplicação abre a sessão e nenhuma requisição de presença é enviada

#### Scenario: A recusa não exclui ninguém da aula

- **WHEN** um Guerreiro(a) sem _template_ gravado chega à entrada do Guerreiro(a)
- **THEN** a aplicação o encaminha à confirmação humana, sem impedi-lo de participar

#### Scenario: A presença confirmada guarda quem confirmou

- **WHEN** a sessão é aberta por confirmação presencial no caminho da presença
- **THEN** a presença gravada aponta o adulto que confirmou, e não o modo reconhecimento

#### Scenario: Nenhuma imagem de criança sai do aparelho nesta fatia

- **WHEN** a entrada acontece por confirmação humana
- **THEN** nenhuma requisição da aplicação carrega fotografia, e nenhuma imagem é gravada no
  aparelho compartilhado

#### Scenario: Sem PIN, a confirmação não acontece

- **WHEN** alguém toca em "Chamar Mestre ou Admin" e digita um nick sem digitar o PIN
- **THEN** a aplicação não confirma, não abre sessão e não registra presença

#### Scenario: PIN errado é dito como tal e o nick fica

- **WHEN** o PIN digitado não confere
- **THEN** a aplicação diz que o PIN está errado, limpa o PIN e mantém o nick

#### Scenario: PIN bloqueado manda refazer o login

- **WHEN** o núcleo responde que o PIN está bloqueado
- **THEN** a aplicação diz que o PIN foi bloqueado naquele aparelho e que é preciso entrar de
  novo pelo Google, e não oferece nova tentativa

#### Scenario: O PIN não fica no aparelho

- **WHEN** se examina o que a aplicação guardou no aparelho depois de uma confirmação
- **THEN** não há PIN em armazenamento algum

### Requirement: O Mestre ou o Admin recadastra a imagem de referência pela aplicação

A App 01 SHALL permitir que o **Mestre ou o Admin** em sessão de trabalho recadastre a imagem
de referência de um Guerreiro(a) atendido no encontro — captura ruim ou imagem que envelheceu
—, capturando nova imagem no aparelho e enviando **apenas o descritor**.

O identificador do Guerreiro(a) SHALL vir da **sessão dele já aberta** por confirmação
presencial, e NEVER SHALL ser obtido por consulta de nick: a App 01 NEVER SHALL dispor de rota
que resolva nick em identificador, e o alcance continua vedado pelo `RN-01-22`. A substituição
SHALL ficar registrada pelo núcleo. (`RF-04-22`, `RN-01-22`, `RN-04-12`, PRD-04 §5.5)

#### Scenario: A imagem de referência é substituída

- **WHEN** o Mestre recadastra a imagem de um Guerreiro(a) cuja sessão foi aberta por
  confirmação presencial
- **THEN** a aplicação captura nova imagem, envia só o descritor e o núcleo registra a
  substituição

#### Scenario: O recadastro não abre oráculo de nick

- **WHEN** se procura na aplicação um caminho que devolva o identificador de um Guerreiro(a) a
  partir do nick
- **THEN** nenhum existe: o identificador só aparece depois de uma sessão aberta por
  confirmação presencial

### Requirement: O Guerreiro(a) forma a equipe da aula pelo aparelho, com o papel declarado

A App 01 SHALL permitir ao Guerreiro(a) em sessão **criar** equipe da aula vigente, **entrar**
em equipe já formada e **sair** da que integra, **sem aprovação de terceiro**, declarando o
**papel** que terá — que vale para o encontro inteiro e é opcional. Criar SHALL exigir o
**nome** da equipe, obrigatório e de até 20 caracteres: a aplicação NEVER SHALL enviar a
criação com o nome em branco, e SHALL limitar o campo a 20 caracteres. A aplicação SHALL
apresentar as recusas do núcleo — sexto integrante, segundo integrante de 17 anos ou mais e
nome repetido na aula — em linguagem simples, sem código de erro cru. (`RF-04-30`, `RF-04-31`,
`RF-04-59`, `RF-04-69`, `RN-04-15`, `RN-04-16`, `RN-04-30`, `RN-04-39`, PRD-04 §12)

#### Scenario: Guerreiro(a) cria a equipe e entra nela

- **WHEN** um Guerreiro(a) em sessão cria uma equipe da aula vigente, dando o nome dela
- **THEN** a equipe nasce com aquele nome e com ele como primeiro integrante, sem aprovação de
  ninguém

#### Scenario: Criar sem nome não sai do aparelho

- **WHEN** um Guerreiro(a) pede para criar a equipe com o nome em branco
- **THEN** a aplicação pede o nome e não envia a criação

#### Scenario: Nome repetido na aula é recusado em linguagem simples

- **WHEN** um Guerreiro(a) cria a equipe com o nome de outra equipe da mesma aula
- **THEN** a aplicação apresenta a recusa em linguagem simples e nenhuma equipe é criada

#### Scenario: Papel declarado na entrada

- **WHEN** um Guerreiro(a) entra numa equipe declarando o papel que terá
- **THEN** a aplicação envia o papel junto da entrada

#### Scenario: Papel é opcional

- **WHEN** um Guerreiro(a) entra numa equipe sem declarar papel
- **THEN** a aplicação registra a entrada assim mesmo

#### Scenario: A sexta pessoa lê a recusa em linguagem simples

- **WHEN** uma sexta pessoa tenta entrar numa equipe de cinco
- **THEN** a aplicação apresenta a recusa em linguagem simples e a composição não muda

#### Scenario: Guerreiro(a) sai da equipe por conta própria

- **WHEN** um integrante pede para sair da equipe que integra
- **THEN** a aplicação registra a saída, sem aprovação de terceiro

### Requirement: A tela das equipes mostra apenas avatar e nick

A App 01 SHALL apresentar as equipes já formadas na aula vigente pelo **nome** da equipe e, em
cada uma, os integrantes por **avatar e nick**, e NEVER SHALL exibir nome civil, data de
nascimento, imagem ou qualquer outro dado pessoal de um Guerreiro(a) para outro. (`RF-04-34`,
`RN-04-14`, documento 99 §6 invariante 11)

O avatar SHALL ser **desenhado** a partir do objeto do documento 15 §7.2, e NEVER SHALL ser
apresentado como texto nem omitido: avatar ausente ou com traço desconhecido SHALL cair no **avatar
padrão do projeto** (documento 15 §7.3), na mesma moldura dos demais e sem nenhuma outra marca de
diferença. (`RF-04-34`, documento 15 §7)

#### Scenario: As equipes da aula aparecem por avatar e nick

- **WHEN** o Guerreiro(a) em sessão abre a tela das equipes da aula vigente
- **THEN** cada equipe aparece com o nome dela e com o avatar e o nick de cada integrante, e
  nada além disso

#### Scenario: Nenhuma imagem de um Guerreiro(a) é exibida a outro

- **WHEN** a tela das equipes é apresentada
- **THEN** nenhuma fotografia de Guerreiro(a) aparece em tela alguma

#### Scenario: Equipes de outra aula não aparecem

- **WHEN** a tela das equipes da aula vigente é apresentada
- **THEN** as equipes formadas em outras aulas não estão entre as exibidas

#### Scenario: O avatar aparece desenhado ao lado do nick

- **WHEN** a tela das equipes da aula apresenta os integrantes
- **THEN** cada um aparece com o avatar desenhado e o nick, e nenhum aparece com o avatar em texto

#### Scenario: Avatar que falta cai no padrão do projeto

- **WHEN** um integrante não tem avatar, ou o avatar dele traz traço que o catálogo não conhece
- **THEN** a tela desenha o avatar padrão do projeto, na mesma moldura, sem marca de diferença

### Requirement: A equipe forma a equipe da trilha pelo aparelho, a partir da programação

A App 01 SHALL oferecer, na programação do encontro, a formação da **equipe da trilha** da
atividade que a equipe escolheu: o Guerreiro(a) em sessão **cria** a equipe daquela trilha,
dando o **nome** dela com a mesma regra da equipe da aula, ou **entra** na que já existe,
declarando o **papel** que terá, sem aprovação de terceiro. A equipe da trilha SHALL aparecer
pelo nome.

A aplicação SHALL apresentar as recusas do núcleo em **linguagem simples**, sem código de erro
cru: o sexto integrante, o segundo integrante de 17 anos ou mais, a segunda equipe da mesma
trilha e o nome repetido na trilha. Enquanto a equipe da trilha **não** estiver homologada, a
aplicação SHALL oferecer a entrada e a saída; depois de homologada, NEVER SHALL oferecer
nenhuma das duas. (`RF-04-61`, `RF-04-69`, `RN-04-39`, `RN-01-44`, documento 99 §6
invariante 15)

#### Scenario: A formação parte da atividade escolhida

- **WHEN** a equipe declarou a atividade que está trabalhando e abre a formação da equipe da
  trilha
- **THEN** a aplicação forma a equipe da **trilha daquela atividade**, sem pedir que alguém a
  escolha de novo

#### Scenario: Guerreiro(a) cria a equipe da trilha e entra nela

- **WHEN** um Guerreiro(a) em sessão cria a equipe da trilha, dando o nome dela
- **THEN** a equipe nasce com aquele nome e com ele como primeiro integrante, sem aprovação de
  ninguém

#### Scenario: A segunda equipe da mesma trilha é recusada em linguagem simples

- **WHEN** um Guerreiro(a) que já integra uma equipe daquela trilha tenta criar outra
- **THEN** a aplicação apresenta a recusa em linguagem simples e ele segue na primeira

#### Scenario: Equipe homologada não oferece entrar nem sair

- **WHEN** a tela da equipe da trilha já homologada é apresentada
- **THEN** nenhuma ação de entrar ou de sair é oferecida

### Requirement: O Mestre presente homologa a equipe da trilha no mesmo aparelho

A App 01 SHALL oferecer a **homologação da equipe da trilha** ao **Mestre** sob a **sessão de
trabalho do aparelho**, no mesmo encontro em que a equipe se formou. A aplicação SHALL
apresentar a composição — avatar, nick e papel de cada integrante — antes de homologar, e SHALL
declarar que a composição **fica fixa** a partir dali.

A homologação NEVER SHALL ser oferecida ao **Guerreiro(a)** em sessão, e a App 01 SHALL seguir
sem oferecer a Mestre ou Admin a **formação** ou a **alteração da composição** de equipe alguma
— homologar não é formar. Decisão do fundador, 2026-08-26: as duas coisas acontecem na App 01.
(`RF-04-62`, `RN-04-18`, `RF-01-16`, documento 99 §6 invariante 15)

#### Scenario: O Mestre homologa sob a sessão de trabalho

- **WHEN** o Mestre em sessão de trabalho homologa a equipe da trilha formada no encontro
- **THEN** a aplicação registra a homologação e a composição fica fixa

#### Scenario: A composição é mostrada antes de homologar

- **WHEN** a tela de homologação é apresentada
- **THEN** ela mostra avatar, nick e papel de cada integrante e avisa que a composição fica fixa

#### Scenario: O Guerreiro(a) não vê a homologação

- **WHEN** um Guerreiro(a) em sessão abre a tela da equipe da trilha
- **THEN** nenhuma ação de homologar é oferecida a ele

#### Scenario: A sessão de trabalho segue sem formar equipe

- **WHEN** a sessão de trabalho do aparelho está aberta
- **THEN** a aplicação oferece homologar, e não oferece criar equipe, entrar nem sair

### Requirement: O caminho do onboarding cadastra o Guerreiro(a) no encontro

A App 01 SHALL oferecer, na tela inicial, o caminho do **onboarding** em estado operante, e por
ele SHALL conduzir o cadastro do Guerreiro(a) coletando **nome**, **nick**, **forma de
tratamento**, **data de nascimento** e **características do avatar**. A aplicação NEVER SHALL
perguntar a comunidade: ela vem da aula vigente adotada na sessão de trabalho. O cadastro SHALL
ser feito **na presença** de Mestre ou Admin, cuja sessão de trabalho autentica a escrita sem
tornar-se autora dela. (`RF-04-01`, `RF-04-07`, `RF-04-10`, `RN-04-02`, `RN-04-04`, PRD-04 §12,
documento 99 §6 invariante 3)

Nesta fatia o cadastro é **formulário guiado**, não conversa conduzida por modelo de IA: a
condução por áudio e chat é de fatia posterior, e até lá a ordem dos campos é a da tela.

O campo das **características do avatar** SHALL ser a composição do avatar no **catálogo fechado**
da camada comum, nas nove camadas do documento 15 §7.1, e NEVER SHALL ser texto livre: o traço
ditado em palavras não se desenha depois. A **forma de tratamento** SHALL continuar campo próprio,
separado do avatar, porque nenhum item do catálogo carrega marca de gênero. O que a aplicação grava
no campo `avatar` SHALL ser o **objeto versionado** do documento 15 §7.2. (`RF-04-07`, documento 15
§7)

A composição SHALL acontecer **no próprio aparelho, sem rede**, e NEVER SHALL depender de requisição
ao núcleo nem a terceiro para desenhar o avatar. (documento 15 §7, princípio 6)

#### Scenario: O caminho do onboarding está alcançável

- **WHEN** a sessão de trabalho do aparelho está aberta e a tela inicial é apresentada
- **THEN** o caminho do onboarding é alcançável e conduz ao cadastro do Guerreiro(a)

#### Scenario: O cadastro coleta os cinco dados

- **WHEN** uma criança chega ao caminho do onboarding
- **THEN** a aplicação coleta nome, nick, forma de tratamento, data de nascimento e
  características do avatar, e não conclui o cadastro faltando qualquer um deles

#### Scenario: A comunidade nunca é perguntada à criança

- **WHEN** o cadastro do encontro é concluído
- **THEN** o Guerreiro(a) fica vinculado à comunidade da aula vigente, e em nenhum momento a
  aplicação lhe perguntou qual é

#### Scenario: Sem sessão de trabalho não há cadastro

- **WHEN** não há sessão de trabalho do aparelho aberta
- **THEN** o caminho do onboarding não é alcançável e nenhum cadastro é enviado ao núcleo

#### Scenario: O avatar nasce do catálogo, não de texto livre

- **WHEN** o cadastro do onboarding chega ao avatar
- **THEN** a criança compõe o avatar escolhendo no catálogo das nove camadas, e nenhum campo pede
  característica em texto livre

#### Scenario: O que se grava é o objeto versionado

- **WHEN** o cadastro é concluído
- **THEN** o campo do avatar leva o objeto versionado do documento 15 §7.2, e a forma de tratamento
  segue em campo próprio

#### Scenario: Compor não depende de rede

- **WHEN** a composição do avatar acontece
- **THEN** nenhuma requisição sai do aparelho para desenhar o avatar

### Requirement: A aplicação recusa o nick em uso e oferece as variações devolvidas pelo núcleo

A App 01 SHALL apresentar a recusa de **nick já usado** em linguagem simples, sem código de erro
cru, e SHALL oferecer as **variações** que o núcleo devolveu na própria recusa, aceitando que a
criança escolha uma delas e conclua o cadastro. A aplicação NEVER SHALL afirmar que um nick está
disponível antes de o núcleo aceitar a gravação, e NEVER SHALL dizer de quem é o nick em uso nem
de que papel. (`RF-04-08`, `RN-04-05`, PRD-04 §12)

#### Scenario: Nick em uso é recusado sem concluir o cadastro

- **WHEN** a criança conclui o cadastro com um nick já usado por qualquer persona
- **THEN** a aplicação apresenta a recusa em linguagem simples e nenhum cadastro passa a existir

#### Scenario: A variação sugerida é aceita

- **WHEN** a criança escolhe uma das variações oferecidas na recusa e conclui de novo
- **THEN** o cadastro é criado com a variação escolhida

#### Scenario: A recusa não revela o dono do nick

- **WHEN** a recusa de nick é apresentada
- **THEN** ela não diz de quem é o nick nem de que papel é a persona que o tem

### Requirement: Idade fora da faixa interrompe o cadastro e chama o Mestre ou o Admin

A App 01 SHALL interromper o cadastro quando a data de nascimento informada resultar em idade
**fora da faixa de 6 a 16 anos**, SHALL orientar a chamar o Mestre ou o Admin presente, e NEVER
SHALL criar o cadastro. (`RF-04-09`, `RN-04-11`, PRD-04 §12, documento 99 §6 invariante 2)

#### Scenario: Idade abaixo da faixa não cria cadastro

- **WHEN** a data de nascimento informada resulta em idade menor que 6 anos
- **THEN** a aplicação interrompe o cadastro, orienta a chamar o Mestre ou o Admin, e nenhuma
  persona passa a existir

#### Scenario: Idade acima da faixa não cria cadastro

- **WHEN** a data de nascimento informada resulta em idade maior que 16 anos
- **THEN** a aplicação interrompe o cadastro, orienta a chamar o Mestre ou o Admin, e nenhuma
  persona passa a existir

#### Scenario: Idade dentro da faixa segue

- **WHEN** a data de nascimento informada resulta em idade entre 6 e 16 anos, inclusive nos
  extremos
- **THEN** o cadastro segue sem interrupção

### Requirement: O cadastro do encontro nasce ativo, sem imagem, e registra a presença no mesmo ato

A App 01 SHALL criar o cadastro **ativo**, sem exigir autorização do responsável para que ele
exista, e **sem imagem** — nesta fatia nenhuma captura é oferecida. A **presença do dia** na
aula vigente SHALL ser registrada **no mesmo ato** do cadastro, de modo que nenhum Guerreiro(a)
recém-cadastrado fique sem a presença do encontro em que se cadastrou. Nenhuma requisição da
aplicação SHALL carregar fotografia, e nenhuma imagem SHALL ser gravada no aparelho
compartilhado. (`RF-04-15`, `RF-04-17`, `RF-04-28`, `RN-04-10`, `RN-04-12`, PRD-04 §12)

#### Scenario: O cadastro nasce ativo e sem imagem

- **WHEN** o cadastro do encontro é concluído
- **THEN** o Guerreiro(a) passa a existir ativo, sem _template_ biométrico, e participa de tudo

#### Scenario: A presença do dia acompanha o cadastro

- **WHEN** o cadastro do encontro é concluído
- **THEN** a presença daquele Guerreiro(a) na aula vigente está registrada, sem ato adicional de
  ninguém

#### Scenario: Cadastro recusado não deixa presença órfã

- **WHEN** o cadastro é recusado pelo núcleo por qualquer motivo
- **THEN** nenhuma persona e nenhuma presença passam a existir

#### Scenario: Nenhuma imagem sai do aparelho nesta fatia

- **WHEN** qualquer cadastro do encontro acontece
- **THEN** nenhuma requisição carrega fotografia e nenhuma imagem fica gravada no aparelho

#### Scenario: O atendimento seguinte começa limpo depois de um cadastro

- **WHEN** um cadastro termina e a aplicação volta à tela inicial
- **THEN** nenhum dado da criança recém-cadastrada aparece em tela alguma

### Requirement: O onboarding cadastra o responsável mínimo e o vínculo no ato do encontro

A App 01 SHALL oferecer, no caminho do onboarding, o cadastro do **responsável mínimo** — apenas
o **nome** — e do **vínculo** dele com o Guerreiro(a) recém-cadastrado, com o **grau de
parentesco** declarado ali. O cadastro SHALL acontecer sob a sessão de trabalho do aparelho,
depois de o Guerreiro(a) existir, porque o vínculo só alcança quem já está cadastrado. A App 01
NEVER SHALL colher e-mail, criar credencial de acesso à App 07 ou anexar a digitalização do
termo: os três são atos da gestão. (`RF-04-60`, `RF-01-13`, `RN-01-20`, PRD-04 §§3.2, 5.2)

#### Scenario: O responsável presente é cadastrado com o vínculo

- **WHEN** a criança conclui o cadastro com o responsável presente
- **THEN** a aplicação cadastra o responsável pelo nome e cria o vínculo com o grau de
  parentesco declarado

#### Scenario: O grau de parentesco é exigido na tela

- **WHEN** a tela do responsável é enviada sem o grau de parentesco
- **THEN** a aplicação recusa e pede o grau antes de seguir para o termo

#### Scenario: A tela não pede e-mail nem senha do responsável

- **WHEN** o responsável é cadastrado no encontro
- **THEN** nenhuma tela pede e-mail, senha ou documento, e a orientação diz que o acesso da
  família é resolvido pela gestão

### Requirement: O termo é exibido e a assinatura é testemunhada antes da captura

A App 01 SHALL exibir o **termo de consentimento** na tela antes de qualquer captura, e SHALL
colher do Mestre ou do Admin presente a confirmação de que o termo impresso foi **assinado pelo
responsável**. Quem confirma SHALL ficar registrado como **testemunha** do consentimento. A
aplicação NEVER SHALL capturar imagem antes de o consentimento estar registrado no núcleo.
(`RF-04-11`, `RF-04-12`, `RF-04-13`, `RN-04-07`, documento 99 §6 invariante 11)

A leitura do termo **em voz alta** depende da modalidade áudio, que ainda não existe na
aplicação: esta fatia entrega a exibição em tela, e a locução acompanha a conversa conduzida por
IA quando ela chegar. (`RF-04-06`, `RF-04-11`)

Recusada a captura, a tela SHALL apresentar **a recusa que o núcleo deu** — a mensagem que a
camada de acesso já entrega —, e NEVER SHALL atribuir ao consentimento uma recusa de outra
causa. A tela SHALL ter frase própria apenas quando não houver corpo de erro do núcleo.
(`RF-04-13`, `RF-04-20`, `RF-01-02`, PRD-01 §2)

#### Scenario: O termo aparece antes da câmera

- **WHEN** o cadastro chega ao passo da imagem com o responsável presente
- **THEN** a aplicação exibe o termo e não abre a câmera enquanto a confirmação não for dada

#### Scenario: Quem confirma fica registrado como testemunha

- **WHEN** o Mestre confirma que o termo impresso foi assinado
- **THEN** o consentimento é registrado no núcleo com ele como testemunha, e só então a câmera é
  aberta

#### Scenario: Captura sem consentimento registrado é recusada

- **WHEN** o envio do descritor é tentado sem consentimento de biometria registrado
- **THEN** o núcleo recusa com 422 e a aplicação apresenta a recusa dele em linguagem simples

#### Scenario: Recusa de outra causa não vira recusa de consentimento

- **WHEN** o núcleo recusa o envio do descritor por motivo diferente do consentimento
- **THEN** a tela apresenta o motivo que o núcleo deu, e não a frase do consentimento

#### Scenario: Falha sem resposta do núcleo tem frase própria

- **WHEN** a captura falha antes de qualquer resposta do núcleo chegar
- **THEN** a tela diz que a captura falhou, sem atribuir ao núcleo uma recusa que ele não deu

### Requirement: O descritor nasce no aparelho, depois da prova de vivacidade

A App 01 SHALL gerar o _template_ no **navegador do próprio aparelho**, na ordem **prova de
vivacidade e, depois, descritor facial**, e SHALL enviar ao núcleo **apenas o descritor**. A
aplicação NEVER SHALL pôr a fotografia em corpo de requisição, em registro de erro ou em
armazenamento do aparelho. A fotografia SHALL ser descartada na geração do descritor.
(`RF-04-14`, `RF-04-48`, `RN-04-06`, `RN-04-08`, `RN-04-12`, `RN-04-14`, documento 03 §3.3,
documento 99 §6 invariante 12)

A tela SHALL apresentar o **visor ao vivo** da câmera — que mostra a pessoa a si mesma antes de
existir captura, não guarda e não reexibe — e SHALL confirmar por **retorno abstrato** que há
rosto enquadrado e que a vivacidade passou. A **imagem capturada** NEVER SHALL ser exibida, em
tela alguma, antes ou depois de gerar o descritor: quadro congelado devolvido à tela é proibido.
(`RF-04-64`, `RN-04-34`, documento 03 §3.3, documento 99 §6 invariante 12)

A detecção SHALL correr **em laço** até a vivacidade passar ou o tempo se esgotar, e NEVER SHALL
julgar um único quadro colhido no instante do acionamento. (`RF-04-64`)

A garantia de que o descritor veio de um rosto presente é **também presencial** — aula agendada,
aparelho do ponto de apoio e Mestre ou Admin na sala —, porque o descritor nasce em código que
roda no aparelho e o núcleo não tem como reconferi-la. (documento 03 §3.3)

#### Scenario: Nenhuma requisição carrega imagem

- **WHEN** a captura é concluída e o descritor é enviado
- **THEN** o corpo da requisição carrega apenas o descritor, e nenhuma imagem aparece em
  requisição, em registro de erro ou no armazenamento do aparelho

#### Scenario: A fotografia não sobrevive à captura

- **WHEN** o descritor é gerado
- **THEN** a fotografia original é descartada no aparelho e não existe em lugar nenhum

#### Scenario: O visor mostra a pessoa a si mesma

- **WHEN** a captura do onboarding abre a câmera
- **THEN** o visor ao vivo aparece na tela, e o retorno de rosto enquadrado e de vivacidade
  confirmada é abstrato, nunca a fotografia

#### Scenario: O quadro capturado não volta à tela

- **WHEN** o descritor é gerado a partir do quadro aprovado
- **THEN** nenhuma tela apresenta aquele quadro, nem antes nem depois da geração

### Requirement: A captura se prepara antes de reprovar, e a falha de preparo se diz distinta

A App 01 SHALL preparar a câmera e os modelos de biometria **antes** de julgar a vivacidade, e
SHALL distinguir na tela, com frases diferentes, **três desfechos que hoje se confundem**: o
preparo que não se concluiu, a vivacidade que reprovou e a recusa do núcleo. Preparo que falhou
NEVER SHALL ser apresentado como ausência de pessoa diante da câmera. (`RF-04-65`, `RF-04-13`,
`RF-04-48`, documento 03 §3.3)

A preparação SHALL concluir em **aparelho sem aceleração gráfica disponível** — o aparelho do
ponto de apoio é modesto, e a aplicação não escolhe o hardware do encontro. (`RF-04-65`,
documento 03 §3.2)

A distinção NEVER SHALL alcançar a **recusa do núcleo**, que segue indistinguível entre nick
inexistente, Guerreiro(a) sem _template_ e descritor que não confere. (`RF-04-20`, `RN-01-22`)

#### Scenario: Preparo que falha não vira reprovação de vivacidade

- **WHEN** os modelos de biometria não chegam a carregar no aparelho
- **THEN** a tela diz que a captura não pôde ser preparada, com frase distinta da reprovação de
  vivacidade, e não afirma que não há pessoa diante da câmera

#### Scenario: Aparelho sem aceleração gráfica captura do mesmo jeito

- **WHEN** a captura é aberta em aparelho cujo navegador não disponibiliza aceleração gráfica
- **THEN** o preparo conclui, os modelos carregam e a captura acontece

#### Scenario: A recusa do núcleo continua sem revelar a causa

- **WHEN** o núcleo recusa a abertura da sessão por nick e imagem
- **THEN** a frase apresentada segue a mesma para nick inexistente, Guerreiro(a) sem _template_
  e descritor que não confere

### Requirement: Sem câmera, fecha a captura e não o onboarding

A App 01 SHALL verificar a presença de câmera no aparelho e, não havendo, SHALL **oferecer o
onboarding assim mesmo**, concluindo o cadastro ativo e sem imagem pelo caminho do Guerreiro(a)
que chega sem o responsável, com registro de quem confirmou. A aplicação SHALL avisar na tela
que a captura exige outro aparelho. A falta de câmera NEVER SHALL deixar uma criança sem cadastro
no dia do encontro. (`RF-04-04`, `RF-04-15`, `RN-04-03`, `RN-04-09`, documento 99 §6 invariante
11, documento 09 — decisão do fundador, 2026-08-24)

#### Scenario: Aparelho sem câmera cadastra sem imagem

- **WHEN** o onboarding é aberto em aparelho sem câmera
- **THEN** o cadastro é concluído ativo e sem imagem, e a tela avisa que a captura exige outro
  aparelho

#### Scenario: A ausência de câmera não fecha o caminho

- **WHEN** a aplicação detecta que não há câmera
- **THEN** o caminho do onboarding continua oferecido na tela inicial

### Requirement: A App 01 não oferece a captura de quem já se cadastrou sem imagem

A App 01 NEVER SHALL oferecer, nesta fatia, a captura de imagem do Guerreiro(a) que **já se
cadastrou sem ela** — a criança cujo responsável comparece num encontro posterior. O que falta
não é o alcance do identificador, que esta fatia resolve, e sim rodar a jornada 5.2 sobre um
cadastro que já existe: vínculo do responsável, consentimento e só então a captura. O
Guerreiro(a) sem _template_ SHALL continuar atendido por inteiro pela confirmação humana, e
nenhuma recusa SHALL deixá-lo fora da aula. (`RF-04-16`, `RN-04-07`, `RN-04-09`, PRD-04 §5.2)

#### Scenario: O responsável comparece num encontro posterior

- **WHEN** um Guerreiro(a) cadastrado sem imagem volta ao encontro com o responsável
- **THEN** a aplicação não oferece a captura nesta fatia, e o Guerreiro(a) segue participando
  pela confirmação humana

### Requirement: O caminho das trilhas leva a equipe à programação do encontro

Escolhida a equipe do momento, a App 01 SHALL mostrar à equipe a **programação do encontro**:
para cada atividade presencial declarada naquela aula, a **missão** em que ela está, o
**conteúdo** da missão e a **atividade do dia**, com a bibliografia de apoio (`RF-04-35`,
jornada 5.8).

Havendo mais de uma atividade no encontro, a aplicação SHALL apresentá-las como **escolha da
equipe** — nenhuma é eleita pela aplicação, e a escolha NEVER SHALL ser enviada ao núcleo. É o
encontro assíncrono do documento 05 §4: cada equipe avança no seu ritmo.

A aplicação SHALL mostrar o conteúdo da missão nos tipos que o núcleo serve — texto formatado,
imagem, link externo, vídeo e arquivo de apoio —, com a **fonte** do conteúdo de terceiro e o
**crédito ao Mestre autor** que a trilha publicada declara. Encontro sem programação declarada
SHALL exibir aviso em linguagem simples, e não erro nem tela vazia.

Nenhuma tela deste caminho SHALL exibir dado pessoal de Guerreiro(a): a equipe segue
identificada por **avatar e nick**, como já vale para a tela das equipes (`RF-04-34`,
`RN-04-14`). (`RF-04-35`, `RF-04-29`, `RN-04-15`, documento 05 §4, PRD-04 §9)

#### Scenario: A equipe vê a missão, o conteúdo e a atividade do dia

- **WHEN** a equipe escolhida entra no caminho das trilhas num encontro com programação
  declarada
- **THEN** a aplicação mostra a missão, o conteúdo dela e a atividade do dia

#### Scenario: Duas atividades no encontro viram escolha da equipe

- **WHEN** a programação do encontro traz duas atividades, de trilhas diferentes
- **THEN** a aplicação apresenta as duas e a equipe escolhe, sem que a escolha seja enviada ao
  núcleo

#### Scenario: Encontro sem programação avisa em linguagem simples

- **WHEN** a equipe entra no caminho das trilhas e a programação do encontro está vazia
- **THEN** a aplicação avisa que o encontro ainda não tem atividade declarada, sem erro na tela

#### Scenario: O conteúdo de terceiro sai com a fonte

- **WHEN** a missão do dia tem conteúdo de terceiro
- **THEN** a aplicação exibe a fonte registrada junto do conteúdo

#### Scenario: Nenhum dado pessoal aparece no caminho das trilhas

- **WHEN** a equipe percorre as telas do caminho das trilhas
- **THEN** os integrantes aparecem apenas por avatar e nick, e nenhuma imagem de Guerreiro(a) é
  exibida

### Requirement: A equipe declara pelo aparelho em que atividade da programação está

A App 01 SHALL oferecer, na tela da programação do encontro, a **escolha** da atividade em que a
equipe vai trabalhar, e SHALL declará-la ao núcleo. É o que enche a missão de cada equipe no
painel do dia da App 03 (`RF-02-42`) e o que fecha o "a missão **em que está**" do `RF-04-35`.

A escolha SHALL ser **trocável** durante o encontro, quantas vezes a equipe quiser, e a tela
SHALL mostrar qual está corrente. A aplicação NEVER SHALL escolher por conta própria quando a
programação traz mais de uma atividade: sem declaração da equipe, a escolha fica em branco.

A declaração SHALL exigir rede. Sem rede, o **conteúdo já carregado continua legível** e a
aplicação SHALL dizer que a escolha não é declarada agora, **sem enfileirar** a declaração —
mesma regra da resposta de quiz, porque o que o painel mostra tem de ser o que está acontecendo
(`RF-04-58`). (`RF-04-35`, `RF-02-42`, `RF-04-58`, PRD-04 §6.2)

#### Scenario: A equipe escolhe a atividade e o aparelho declara

- **WHEN** a equipe escolhe uma das atividades da programação
- **THEN** a aplicação declara a escolha ao núcleo e a apresenta como corrente

#### Scenario: A equipe troca de atividade no mesmo encontro

- **WHEN** a equipe escolhe outra atividade da programação
- **THEN** a aplicação declara a nova e passa a apresentá-la como corrente

#### Scenario: Programação com duas atividades não é decidida pela aplicação

- **WHEN** a programação traz duas atividades e a equipe não escolheu nenhuma
- **THEN** a aplicação não declara escolha alguma e a tela segue sem corrente

#### Scenario: Sem rede, a escolha não é declarada nem enfileirada

- **WHEN** a equipe tenta escolher com o aparelho sem rede
- **THEN** a aplicação diz que a escolha está indisponível sem rede, o conteúdo já carregado
  segue legível e nada é enfileirado

### Requirement: Sem rede, o conteúdo da missão já carregado continua legível

A App 01 SHALL manter legível, com a rede fora, o **conteúdo da missão já carregado** naquele
aparelho, para que a equipe siga trabalhando durante a queda. A aplicação NEVER SHALL exigir
nova chamada ao núcleo para reexibir o que já mostrou.

Com a rede fora, a aplicação SHALL avisar que a programação **não pode ser atualizada**, e
NEVER SHALL enfileirar leitura para reenvio — a programação é leitura, não fato a sincronizar.
(`RF-04-58`, documento 03 §3.4)

#### Scenario: A rede cai e o conteúdo segue na tela

- **WHEN** a rede cai enquanto a equipe lê o conteúdo da missão do dia
- **THEN** o conteúdo já carregado continua legível e a equipe segue trabalhando

#### Scenario: Sem rede, a programação não se atualiza e a aplicação avisa

- **WHEN** a equipe pede a programação do encontro com a rede fora
- **THEN** a aplicação avisa que não consegue atualizar agora e mantém o que já tinha

#### Scenario: Leitura não vai para fila

- **WHEN** a rede volta depois de a equipe ter navegado o conteúdo sem rede
- **THEN** a aplicação não envia nada ao núcleo por conta dessas leituras

### Requirement: A equipe entrega a produção da missão pelo aparelho e lê a devolutiva

A App 01 SHALL oferecer à equipe, na atividade que ela declarou estar trabalhando, a **entrega
da produção** em **uma** de três formas: **texto** digitado, **fala** transcrita no aparelho ou
**foto** do que a equipe fez à mão. A tela SHALL apresentar a **produção esperada** declarada na
atividade, para a equipe saber o que entregar.

Entregue, a aplicação SHALL apresentar a **devolutiva** que o núcleo devolveu, e SHALL dizer,
na própria tela, que ela **não vale ponto** e que o resultado é lançado pelo Mestre. Devolutiva
que não veio numa entrega por texto ou por fala SHALL ser apresentada como tal, com a entrega
registrada — nunca como perda do que a equipe produziu; entrega por foto que o núcleo recusou
por leitura indisponível SHALL ser apresentada como pedido de reenvio, em linguagem simples.

O microfone SHALL abrir por **ação do Guerreiro(a)** e fechar ao fim da fala; a aplicação NEVER
SHALL captar o áudio ambiente da aula. A fala SHALL ser **transcrita no próprio aparelho**, e
ao núcleo SHALL seguir **a transcrição**, nunca o áudio: a aplicação NEVER SHALL gravar o áudio
em arquivo, em armazenamento do navegador ou em qualquer lugar do aparelho compartilhado. A
transcrição SHALL aparecer no campo da produção **antes do envio** e SHALL ser editável ali,
como qualquer produção digitada. A aplicação NEVER SHALL guardar no aparelho a foto da produção
depois de enviá-la.

Onde o navegador do aparelho não oferecer a transcrição da fala, a tela SHALL **dizê-lo em
linguagem simples** e SHALL manter as formas que não dependem dela — escrever e fotografar —, e
NEVER SHALL cair de volta no envio de áudio ao núcleo. O mesmo aviso SHALL valer quando a
transcrição falhar ou não entender nada da fala, sem perder o que já estava escrito.
(`RF-04-45`, `RF-04-46`, `RF-04-47`, `RN-04-20`, `RN-04-12`, `RF-05-76`, `RN-05-32`,
documento 03 §§1.12, 12.2)

#### Scenario: A equipe entrega por texto

- **WHEN** a equipe escreve a produção e envia
- **THEN** a aplicação registra a entrega e apresenta a devolutiva devolvida pelo núcleo

#### Scenario: A equipe entrega por fala

- **WHEN** um integrante toca o botão de falar e fala a produção
- **THEN** o microfone fecha ao fim da fala, a transcrição aparece no campo da produção e o que
  segue ao núcleo é o texto transcrito, sem áudio algum

#### Scenario: A equipe corrige a transcrição antes de enviar

- **WHEN** a transcrição da fala aparece no campo da produção e a equipe a edita
- **THEN** o que segue ao núcleo é o texto corrigido, com a forma "áudio" declarada

#### Scenario: O áudio não fica no aparelho

- **WHEN** a produção falada é enviada
- **THEN** nenhum áudio permanece no aparelho — nem em arquivo, nem em armazenamento do
  navegador

#### Scenario: A equipe entrega a foto do manuscrito

- **WHEN** a equipe fotografa o que fez à mão e envia
- **THEN** a aplicação envia a foto e não a mantém no aparelho depois do envio

#### Scenario: A tela diz que a devolutiva não vale ponto

- **WHEN** a devolutiva é apresentada
- **THEN** a tela diz, em linguagem simples, que ela não credita ponto e que quem lança o
  resultado é o Mestre

#### Scenario: A produção esperada aparece antes da entrega

- **WHEN** a tela da entrega é apresentada
- **THEN** ela mostra a produção esperada declarada na atividade

#### Scenario: Devolutiva que não veio não perde a entrega por texto

- **WHEN** o núcleo registra a produção em texto sem devolutiva
- **THEN** a aplicação confirma a entrega e avisa que o retorno não veio desta vez

#### Scenario: Devolutiva que não veio não perde a entrega falada

- **WHEN** o núcleo registra a produção falada sem devolutiva
- **THEN** a aplicação confirma a entrega e avisa que o retorno não veio desta vez

#### Scenario: Leitura indisponível pede reenvio

- **WHEN** o núcleo recusa a entrega por foto porque a leitura não veio
- **THEN** a aplicação pede o reenvio em linguagem simples, sem dizer que a produção se perdeu

#### Scenario: O navegador não transcreve

- **WHEN** a tela da entrega abre num navegador sem a transcrição de fala
- **THEN** a tela avisa que ali a entrega é por texto ou por foto, e não oferece a fala

#### Scenario: A transcrição não entendeu a fala

- **WHEN** um integrante fala e o aparelho não devolve transcrição alguma
- **THEN** a tela o diz em linguagem simples, sem perder o que estava escrito, e a equipe pode
  falar de novo ou digitar

### Requirement: Quem recusa foto e áudio entrega por texto, sem perder a missão

A App 01 SHALL oferecer a entrega **por texto** como alternativa sempre disponível: a equipe
que não quiser usar foto nem microfone SHALL entregar assim mesmo, **sem perder a missão**.
A aplicação NEVER SHALL condicionar a entrega ao uso da câmera ou do microfone.
(`RF-04-45`, `RN-04-09`, documento 99 §6 invariante 11)

#### Scenario: A entrega por texto está sempre oferecida

- **WHEN** a tela da entrega é apresentada
- **THEN** a forma texto está entre as oferecidas, qualquer que seja o aparelho

#### Scenario: Aparelho sem câmera nem microfone entrega assim mesmo

- **WHEN** o aparelho não tem câmera nem microfone disponíveis
- **THEN** a aplicação oferece a entrega por texto e a equipe conclui a produção

### Requirement: A equipe alcança o assistente de trilhas pela programação e pergunta por texto ou por fala

A App 01 SHALL oferecer o **assistente de trilhas** a partir da programação do encontro, para o
Guerreiro(a) em sessão que integra a equipe, e SHALL aceitar a pergunta **por texto** e **por
fala**, com a alternativa por texto **sempre disponível** — a sala é barulhenta e a fala pode
não sair.

A aplicação SHALL apresentar a resposta em tela e SHALL manter a conversa daquele atendimento
visível enquanto ele durar. A aplicação NEVER SHALL oferecer o assistente a quem não tem sessão
de Guerreiro(a) aberta. (`RF-04-36`, `RF-04-39`, PRD-04 §§5.8, 14)

#### Scenario: A equipe chega ao assistente pela programação

- **WHEN** a equipe está na programação do encontro com a atividade corrente declarada
- **THEN** o assistente de trilhas é alcançável dali

#### Scenario: As duas formas de perguntar estão em tela

- **WHEN** a tela do assistente é apresentada
- **THEN** a equipe pode escrever a pergunta e pode falá-la, sem que uma exclua a outra

#### Scenario: A resposta aparece na tela da equipe

- **WHEN** o núcleo devolve a resposta do assistente
- **THEN** a aplicação a apresenta em tela, junto da pergunta que a originou

### Requirement: O microfone abre por ação do Guerreiro(a) e fecha ao fim da fala

A App 01 SHALL abrir o microfone **somente** quando o Guerreiro(a) aciona o botão de falar, e
SHALL fechá-lo **ao fim da fala**. A aplicação NEVER SHALL manter o microfone aberto entre uma
pergunta e outra, NEVER SHALL captar o áudio ambiente da aula e NEVER SHALL transcrever a
conversa da turma.

A fala SHALL ser **transcrita no próprio aparelho**, e ao núcleo SHALL seguir **a transcrição**,
nunca o áudio. A aplicação NEVER SHALL gravar o áudio em arquivo, em armazenamento do navegador
ou em qualquer lugar do aparelho compartilhado. A transcrição SHALL aparecer no campo da
pergunta **antes do envio** e SHALL ser editável ali, como qualquer pergunta digitada.
(`RF-04-39`, `RF-04-40`, `RN-04-20`, `RN-04-21`, documento 03 §1.12, PRD-04 §11)

#### Scenario: Sem toque não há captação

- **WHEN** a tela do assistente está aberta e ninguém aciona o botão de falar
- **THEN** o microfone permanece fechado e nada é captado

#### Scenario: Terminada a fala, o microfone fecha

- **WHEN** o Guerreiro(a) encerra a pergunta falada
- **THEN** a aplicação fecha o microfone antes de enviar a pergunta

#### Scenario: O que segue ao núcleo é a transcrição

- **WHEN** a pergunta falada é enviada
- **THEN** a aplicação manda o texto transcrito no aparelho, e nenhum áudio sai dele

#### Scenario: O áudio não fica no aparelho

- **WHEN** a pergunta falada é enviada
- **THEN** nenhum áudio permanece no aparelho — nem em arquivo, nem em armazenamento do
  navegador

#### Scenario: A equipe corrige a transcrição antes de enviar

- **WHEN** a transcrição da fala aparece no campo da pergunta e a equipe a edita
- **THEN** o que segue ao núcleo é o texto corrigido

### Requirement: Sem transcrição no navegador, a tela avisa e mantém a pergunta por texto

Onde o navegador do aparelho não oferecer a transcrição da fala, a App 01 SHALL **dizê-lo em
linguagem simples** e SHALL manter disponível a pergunta **por texto digitado** — o caminho que
a tela já oferece sempre, ao lado do botão de falar, nunca escondido atrás de uma escolha de
forma. A aplicação NEVER SHALL deixar a equipe sem caminho para perguntar, e NEVER SHALL cair de
volta no envio de áudio ao núcleo (`RF-04-39`, `RF-04-40`, documento 03 §1.12).

O mesmo aviso SHALL valer quando a transcrição falhar ou não entender nada da fala: a pergunta
digitada continua à mão, e a fala pode ser refeita.

#### Scenario: O navegador não transcreve

- **WHEN** a tela do assistente abre num navegador sem a transcrição de fala
- **THEN** a tela avisa que ali a pergunta é por texto, e o campo de texto segue disponível

#### Scenario: A transcrição não entendeu a fala

- **WHEN** o Guerreiro(a) fala e o aparelho não devolve transcrição alguma
- **THEN** a tela o diz em linguagem simples, sem perder o que estava escrito, e a equipe pode
  falar de novo ou digitar

### Requirement: A recusa e o encaminhamento aparecem à equipe como resposta, nunca como erro

A App 01 SHALL apresentar a **recusa explicada** da pergunta fora do corpus e o
**encaminhamento à App 05** da pergunta de tarefa escolar como **resposta do assistente**, na
mesma tela e no mesmo lugar de qualquer outra. A aplicação NEVER SHALL apresentá-las como falha,
erro ou tela de exceção — a equipe perguntou o que podia perguntar.

Não vindo resposta alguma do núcleo, a aplicação SHALL dizer em **uma frase** que o assistente
não respondeu agora e SHALL oferecer perguntar de novo. (`RF-04-37`, `RF-04-38`, PRD-04 §§5.8,
9)

#### Scenario: A recusa vem como resposta

- **WHEN** o núcleo devolve a recusa explicada de uma pergunta fora do corpus
- **THEN** a aplicação a apresenta como resposta do assistente, com a orientação de procurar um
  Mestre no encontro, e nenhuma tela de erro aparece

#### Scenario: A tarefa escolar é encaminhada em tela

- **WHEN** o núcleo devolve o encaminhamento à App 05
- **THEN** a aplicação diz à equipe que esse apoio é da App 05, sem apresentar erro

#### Scenario: O assistente que não respondeu convida a tentar de novo

- **WHEN** o núcleo responde que a resposta está indisponível
- **THEN** a aplicação explica em uma frase e oferece perguntar de novo

### Requirement: A conversa com o assistente termina com o atendimento

A App 01 SHALL descartar a conversa com o assistente ao fim do atendimento, junto com a sessão
do Guerreiro(a), e NEVER SHALL apresentá-la ao próximo que usar o aparelho. A conversa NEVER
SHALL ser gravada no armazenamento do navegador: o que sobrevive é a transcrição no núcleo, que
é do Mestre e da gestão, não da tela seguinte. (`RF-04-28`, PRD-04 §§10, 11)

#### Scenario: O próximo atendimento não vê a conversa anterior

- **WHEN** um atendimento termina e outro Guerreiro(a) abre o assistente no mesmo aparelho
- **THEN** nenhuma pergunta ou resposta do atendimento anterior aparece

### Requirement: Sem rede o assistente fica indisponível, e nenhuma pergunta é enfileirada

A App 01 SHALL apresentar o assistente como **indisponível** enquanto não houver rede, dizendo-o
em uma frase, e NEVER SHALL enfileirar pergunta para envio posterior — resposta que chega depois
do encontro não serve à equipe que perguntou. Voltando a rede, a aplicação SHALL voltar a
aceitar perguntas. (`RF-04-58`, PRD-04 §5.6)

#### Scenario: Sem rede a pergunta não é oferecida

- **WHEN** a equipe tenta perguntar com o aparelho sem rede
- **THEN** a aplicação diz que o assistente está indisponível sem rede, e nada é enfileirado

#### Scenario: Voltando a rede, o assistente volta

- **WHEN** a rede volta
- **THEN** a aplicação volta a aceitar a pergunta, por texto e por fala

### Requirement: A aplicação avisa na tela que está operando sem conexão

A App 01 SHALL apresentar, em **toda tela**, um aviso de que está operando **sem conexão**
enquanto a rede estiver fora, e SHALL retirá-lo assim que a rede voltar. O aviso SHALL dizer, em
linguagem simples, o que continua funcionando e o que não funciona agora — o Mestre na porta
precisa saber sem sair da tela. (`RF-04-23`, `RF-04-24`, PRD-04 §5.6)

#### Scenario: A queda de rede aparece em tela

- **WHEN** uma chamada ao núcleo falha por falta de rede
- **THEN** a aplicação passa a apresentar o aviso de operação sem conexão

#### Scenario: Voltando a rede, o aviso sai

- **WHEN** a rede volta e uma chamada ao núcleo é concluída
- **THEN** a aplicação retira o aviso de operação sem conexão

### Requirement: Sem rede, a presença confirmada pelo Mestre entra na fila local

A App 01 SHALL continuar registrando a **presença** com a rede fora: o Mestre ou o Admin da
sessão de trabalho confirma a criança **pelo nick**, e o registro SHALL entrar na **fila local**
do aparelho, com a **hora do fato** — a hora em que a criança chegou. A confirmação sem rede
SHALL pedir o **PIN** de quem abriu a sessão de trabalho e conferi-lo **no aparelho**, contra o
verificador recebido na abertura; só com o PIN conferido o registro entra na fila. Cada erro
conta, no aparelho, para o bloqueio: no **quinto erro seguido** a aplicação SHALL parar de
confirmar até um novo login Google, com ou sem rede. Sem verificador — o adulto não tinha PIN
cadastrado quando abriu a sessão —, a confirmação sem rede SHALL ficar indisponível, com aviso
que diz por quê. (`RF-04-23`, `RN-04-38`)

A fila SHALL guardar **apenas presença**: nick, hora do fato e a aula do encontro. Ela NEVER
SHALL guardar imagem, fotografia, descritor ou _template_ de criança, nem o PIN, e NEVER SHALL enfileirar
cadastro, resposta de quiz, produção da missão, troca ou consulta ao assistente. (`RF-04-23`,
`RN-04-12`, `RN-04-13`, PRD-04 §8)

#### Scenario: A criança que chega sem rede entra na aula

- **WHEN** a rede está fora e o Mestre confirma a criança que chegou pelo nick e pelo PIN
  certo
- **THEN** a aplicação enfileira a presença com a hora do fato e diz à criança que ela está na
  aula

#### Scenario: A fila não guarda imagem

- **WHEN** se examina o que a aplicação guardou no aparelho durante a queda
- **THEN** há apenas presença enfileirada, e nenhuma imagem, descritor ou _template_

#### Scenario: Só a presença é enfileirada

- **WHEN** a rede cai durante um cadastro, uma partida, uma entrega de produção ou uma troca
- **THEN** nada disso vai para a fila local

#### Scenario: PIN errado sem rede não enfileira

- **WHEN** a rede está fora e o PIN digitado não confere com o verificador
- **THEN** nada entra na fila, e a aplicação diz que o PIN está errado

#### Scenario: O quinto erro sem rede bloqueia o aparelho

- **WHEN** o PIN é errado cinco vezes seguidas sem rede
- **THEN** a aplicação para de confirmar, com ou sem rede, até um novo login Google

#### Scenario: A sincronização não abre sessão

- **WHEN** a rede volta e a fila sincroniza
- **THEN** cada presença é registrada sem abrir sessão de Guerreiro(a)

### Requirement: Sem rede, cadastro novo e reconhecimento facial ficam indisponíveis

A App 01 SHALL apresentar o **cadastro novo** e a **entrada por reconhecimento facial** como
indisponíveis enquanto não houver rede, com aviso na tela dizendo por quê: o descritor nasce no
aparelho, mas a **comparação é no núcleo**, e nenhuma imagem de criança fica guardada no
aparelho compartilhado.

A aplicação SHALL oferecer, no lugar deles, a **confirmação pelo Mestre ou Admin** — a
alternativa equivalente que o `RN-04-09` garante. (`RF-04-24`, `RN-04-12`, PRD-04 §5.6)

#### Scenario: Sem rede o onboarding não abre

- **WHEN** alguém escolhe o caminho do onboarding com a rede fora
- **THEN** a aplicação diz que o cadastro exige rede e não coleta dado algum

#### Scenario: Sem rede a câmera não é oferecida

- **WHEN** o Guerreiro(a) chega à entrada com a rede fora
- **THEN** a aplicação não oferece a entrada por reconhecimento e encaminha à confirmação pelo
  Mestre ou Admin

### Requirement: A fila sincroniza sozinha, preservando a hora do fato e sem duplicar

A App 01 SHALL sincronizar a fila local **sozinha**, assim que a rede voltar, sem ato de
ninguém, enviando cada presença com a **hora do fato** — nunca a hora do envio. O núcleo devolve
o registro já existente sem erro, e a aplicação SHALL tratar essa devolução como **sucesso**,
retirando o item da fila: presença reenviada NEVER SHALL virar registro novo nem erro em tela.

Sincronizado o item, a aplicação SHALL **descartá-lo da fila**. (`RF-04-25`, `RN-04-13`,
PRD-04 §§5.6, 8)

#### Scenario: A rede volta e a fila anda sozinha

- **WHEN** a rede volta com presenças na fila local
- **THEN** a aplicação as envia sem que ninguém acione nada

#### Scenario: A hora do fato é a da chegada

- **WHEN** uma presença enfileirada às 14h é enviada às 15h
- **THEN** a presença registrada no núcleo aponta a hora da chegada, não a do envio

#### Scenario: O reenvio não duplica nem alarma

- **WHEN** o núcleo devolve o registro que já existia para uma presença da fila
- **THEN** a aplicação tira o item da fila sem apresentar erro, e nenhum registro novo nasce

#### Scenario: Sincronizada, a presença some do aparelho

- **WHEN** uma presença da fila é sincronizada
- **THEN** ela é descartada do aparelho e não é reenviada de novo

### Requirement: O que falha na sincronização fica visível ao Mestre presente

A App 01 SHALL apresentar ao **Mestre ou Admin da sessão de trabalho** o que ainda está na fila
e o que **falhou** ao sincronizar — o nick e a hora do fato de cada um —, e SHALL permitir que
ele **tente de novo**. A aplicação NEVER SHALL apresentar essa lista ao Guerreiro(a) nem em tela
de atendimento dele.

A falha de sincronização NEVER SHALL ser reportada ao núcleo nesta fatia: a fila é estado do
aparelho, e listá-la no painel do dia é pendência aberta (PRD-04 §5.6.5, documento 09 §1,
decisão do fundador de 2026-08-30). (`RF-04-23`, `RF-04-25`, `RN-04-14`)

#### Scenario: O Mestre vê o que ainda não subiu

- **WHEN** o Mestre em sessão de trabalho consulta a fila local
- **THEN** a aplicação lista o nick e a hora do fato de cada presença pendente ou falha

#### Scenario: O Mestre tenta de novo

- **WHEN** o Mestre aciona a nova tentativa de um item que falhou
- **THEN** a aplicação o reenvia, e o retira da fila se o núcleo o aceitar

#### Scenario: A fila não aparece para a criança

- **WHEN** um Guerreiro(a) usa o aparelho
- **THEN** nenhuma tela dele apresenta a fila local nem o nick de outra criança

### Requirement: A tela inicial e a tela de captura avisam o que a aplicação coleta

A App 01 SHALL apresentar, na **tela inicial** e na **tela de captura da imagem**, um aviso
**discreto** do que a aplicação coleta, com um **caminho alcançável** para a área detalhada de
direitos. O aviso SHALL estar em linguagem de criança e NEVER SHALL ocupar a tela a ponto de
disputar com o que se está fazendo — o aparelho é operado de pé, na porta da aula.
(`RF-04-26`, `RN-03-23`, PRD-04 §§10, 11)

#### Scenario: A tela inicial traz o aviso

- **WHEN** a tela inicial é apresentada
- **THEN** ela traz o aviso discreto do que a aplicação coleta, com caminho para a área
  detalhada

#### Scenario: A tela de captura traz o aviso

- **WHEN** a tela de captura da imagem é apresentada
- **THEN** ela traz o aviso do que está sendo coletado ali, com caminho para a área detalhada

### Requirement: O Mestre mede no aparelho a distância entre descritores

A App 01 SHALL oferecer ao **Mestre ou ao Admin em sessão de trabalho** uma tela que captura
descritores no aparelho, compara-os entre si e apresenta a **distância** na mesma unidade que o
núcleo usa para comparar — a medição que calibra o limiar de comparação. **Descritor e imagem**
NEVER SHALL sair do aparelho: a comparação inteira acontece nele, e ao núcleo SHALL ir apenas o
**limiar confirmado e as distâncias medidas**, quando a medição concluir. (`RF-04-63`,
`RF-04-66`, documento 03 §3.3)

Abrir essa tela SHALL exigir o **PIN de quem abriu o aparelho**, digitado no ato, pela mesma
conferência e pelo mesmo contador de erros da confirmação de identidade e do encerramento da sessão
de trabalho: a medição grava o número que decide se o reconhecimento confere naquele ponto de apoio,
e a sessão de trabalho sozinha não prova que o adulto responsável está ali. PIN bloqueado NEVER
SHALL abrir a tela; quem não tem PIN cadastrado SHALL abri-la, com o aviso que a aplicação já
apresenta. A exigência é **da tela**: o núcleo segue guardando a gravação pela permissão de quem
grava, e NEVER SHALL ser lida como conferência do núcleo. (`RN-04-41`, `RN-04-37`, `RN-04-38`,
decisão do fundador de 2026-09-25)

A tela SHALL guardar **um** descritor de referência por vez. Cada captura seguinte SHALL ser
comparada com ele e **descartada no mesmo ato** — os dois coexistem apenas durante o cálculo —,
e a tela NEVER SHALL apresentar nem persistir o descritor, só a distância. (`RN-04-32`,
documento 99 §6 invariante 12)

A tela SHALL apresentar o **visor ao vivo** enquanto captura, com o mesmo retorno abstrato das
demais telas de câmera, e NEVER SHALL devolver o quadro capturado. (`RF-04-64`, `RN-04-34`)

Sobre **Guerreiro(a)**, a medição SHALL ser oferecida **apenas dentro do onboarding, depois de
o consentimento de biometria ter sido registrado naquela mesma sessão**. Fora do onboarding, a
tela SHALL medir somente quem opera, e NEVER SHALL abrir a câmera sobre um Guerreiro(a).
(`RN-04-33`, `RN-04-07`, documento 99 §6 invariante 11)

A tela SHALL permanecer na aplicação depois da calibração, como ferramenta de diagnóstico de
quem conduz o encontro. (`RF-04-63`, decisão do fundador, 2026-09-17)

#### Scenario: A distância aparece na unidade do núcleo

- **WHEN** o Mestre captura duas vezes e pede a comparação
- **THEN** a tela apresenta a distância entre os dois descritores, no mesmo cálculo que o núcleo
  usa para decidir se confere

#### Scenario: Só um descritor de referência fica guardado

- **WHEN** uma terceira captura é comparada com a referência
- **THEN** a segunda já havia sido descartada, e em nenhum momento houve mais de um descritor
  de referência guardado

#### Scenario: A medição não fala com o núcleo

- **WHEN** as capturas e as comparações da medição são executadas
- **THEN** nenhuma requisição sai do aparelho: só a gravação do limiar confirmado fala com o
  núcleo, e ela acontece depois de a medição ter concluído

#### Scenario: Nem descritor nem imagem chegam ao núcleo

- **WHEN** a medição inteira é executada, inclusive a gravação do limiar
- **THEN** nenhuma requisição carrega descritor ou imagem, e o que sai do aparelho é o limiar
  confirmado com as distâncias medidas

#### Scenario: A bancada mede com o visor aberto

- **WHEN** a bancada captura a referência ou uma comparação
- **THEN** o visor ao vivo aparece na tela, e o quadro capturado não é devolvido

#### Scenario: Fora do onboarding a câmera não se abre sobre criança

- **WHEN** a tela é alcançada fora do onboarding
- **THEN** ela mede apenas quem opera, e não oferece caminho que capture um Guerreiro(a)

#### Scenario: Dentro do onboarding, mede depois do consentimento

- **WHEN** o onboarding chega ao passo da imagem com o consentimento já registrado
- **THEN** a medição é oferecida ali, sobre o Guerreiro(a) daquele cadastro

#### Scenario: A bancada não abre sem o PIN

- **WHEN** alguém escolhe o caminho da medição na tela inicial
- **THEN** a aplicação pede o PIN de quem abriu o aparelho, e a câmera não é preparada antes de ele
  conferir

#### Scenario: PIN bloqueado não abre a bancada

- **WHEN** o PIN está bloqueado por cinco erros seguidos
- **THEN** a bancada não abre, e a recusa diz o mesmo que a das demais recusas por PIN bloqueado

### Requirement: A área detalhada diz o destino de cada dado e o canal do responsável

A App 01 SHALL apresentar uma **área detalhada de direitos**, alcançável dos avisos, dizendo em
linguagem simples, para **cada dado que a aplicação coleta**: para que serve, por quanto tempo
fica e quem o acessa — como o PRD-04 §11 os declara.

A área SHALL dizer ainda que:

- a **fotografia é apagada** assim que o _template_ é gerado, e nunca sai do aparelho;
- a **imagem nunca é exibida** a ninguém — não vira avatar, não vai para a vitrine, não aparece
  em ranking e não é mostrada a outro Guerreiro(a);
- **recusar a biometria não exclui ninguém**: a confirmação do Mestre no encontro é a
  alternativa equivalente;
- a **medição do limiar** também abre a câmera, compara no aparelho e descarta no ato, sem
  enviar nada — e sobre Guerreiro(a) só acontece sob o termo já assinado;
- **pedido de acesso, correção ou exclusão é do responsável, pela App 07, com resposta em 7
  dias** — a aplicação NEVER SHALL atendê-los nem prometer atendê-los.

(`RF-04-26`, `RF-04-63`, `RN-04-06`, `RN-04-08`, `RN-04-09`, `RN-04-14`, `RN-04-32`, PRD-04 §11)

#### Scenario: A área detalha cada dado coletado

- **WHEN** alguém abre a área detalhada de direitos
- **THEN** ela apresenta, para cada dado coletado, a finalidade, o prazo de guarda e quem acessa

#### Scenario: A área declara a medição do limiar

- **WHEN** a área detalhada é lida
- **THEN** ela diz que a medição do limiar abre a câmera, compara no aparelho, descarta no ato e
  não envia nada

#### Scenario: A área diz o canal e o prazo

- **WHEN** a área detalhada é lida até o fim
- **THEN** ela diz que o pedido de acesso, correção ou exclusão é feito pelo responsável na
  App 07, com resposta em 7 dias

#### Scenario: A aplicação não recebe pedido de direitos

- **WHEN** alguém procura, na área detalhada, um jeito de pedir exclusão ali mesmo
- **THEN** não há nenhum: a aplicação apenas informa o canal

### Requirement: A conversa do onboarding encerra dizendo como entrar da próxima vez

A App 01 SHALL encerrar o atendimento do onboarding dizendo ao Guerreiro(a), em linguagem
simples, **como ele entra da próxima vez**, conforme o cadastro tenha ficado com ou sem imagem:

- **com imagem capturada**: pelo nick e pela câmera;
- **sem imagem** — sem responsável presente, sem câmera no aparelho ou por recusa da biometria
  —: pelo nick, com a **confirmação do Mestre ou do Admin** no encontro, dito como o caminho
  normal dele e nunca como falta.

Dita a despedida, a aplicação SHALL voltar à tela inicial, pronta para o próximo.
(`RF-04-27`, `RF-04-28`, `RN-04-09`, PRD-04 §§5.2, 5.3)

#### Scenario: Quem capturou a imagem ouve o caminho da câmera

- **WHEN** o cadastro termina com a imagem capturada
- **THEN** a aplicação diz que da próxima vez ele entra pelo nick e pela câmera

#### Scenario: Quem ficou sem imagem ouve o caminho do Mestre

- **WHEN** o cadastro termina sem imagem
- **THEN** a aplicação diz que da próxima vez ele entra pelo nick, com o Mestre confirmando, sem
  tratar isso como problema

#### Scenario: A despedida devolve o aparelho ao início

- **WHEN** a despedida é apresentada e o atendimento se encerra
- **THEN** a aplicação volta à tela inicial, sem dado algum do atendimento anterior

### Requirement: A bancada mede em duas séries e grava o limiar do ponto de apoio

A bancada SHALL medir em **duas séries declaradas**, e quem opera SHALL escolher em qual está
capturando:

- o **piso**, capturas da **mesma pessoa** contra a referência;
- o **teto**, capturas de **pessoas diferentes** da referência.

A tela SHALL apresentar as duas séries **separadas**, com o maior valor do piso e o menor valor
do teto em destaque, e SHALL deixar claro a qual série cada medição pertence. (`RF-04-66`,
decisão do fundador, 2026-09-18)

A medição SHALL ser considerada **concluída** quando reunir, ao mesmo tempo:

- ao menos **8 medições de piso**;
- ao menos **8 medições de teto**, de ao menos **2 pessoas diferentes** da referência;
- **maior piso estritamente menor que menor teto**.

Não havendo folga entre as séries, a bancada NEVER SHALL gravar limiar algum: ela SHALL dizer
que não existe limiar viável com aquelas capturas e SHALL oferecer nova medição. (`RN-04-35`)

Concluída a medição, a bancada SHALL **propor** como limiar o **ponto médio entre o maior piso e
o menor teto**, e SHALL gravá-lo somente depois de **Mestre ou Admin confirmar** o valor
proposto. A gravação SHALL alcançar o **ponto de apoio da aula em curso** e SHALL levar ao núcleo
o número e as **duas séries de distâncias** — e nada mais. (`RF-04-66`, `RN-04-35`)

A tela SHALL dizer, antes da gravação, qual ponto de apoio receberá o limiar, e SHALL apresentar
o desfecho da gravação a quem confirmou. (`RF-04-66`)

#### Scenario: As duas séries aparecem separadas

- **WHEN** quem opera captura medições de piso e, em seguida, medições de teto
- **THEN** a tela apresenta as duas séries separadas, com o maior piso e o menor teto em destaque

#### Scenario: A medição incompleta não grava

- **WHEN** a medição tem menos que o mínimo de uma das séries, ou o teto veio de uma pessoa só
- **THEN** a bancada não oferece a gravação e diz o que ainda falta medir

#### Scenario: Séries que se sobrepõem não geram limiar

- **WHEN** o maior valor do piso alcança ou ultrapassa o menor valor do teto
- **THEN** a bancada diz que não existe limiar viável com aquelas capturas, oferece nova medição
  e nada é gravado

#### Scenario: O valor proposto é o ponto médio, e quem opera confirma

- **WHEN** a medição conclui com folga entre as séries
- **THEN** a bancada propõe o ponto médio entre o maior piso e o menor teto, e só grava depois
  da confirmação de Mestre ou Admin

#### Scenario: A gravação alcança o ponto de apoio da aula em curso

- **WHEN** o limiar é confirmado
- **THEN** ele é gravado no ponto de apoio da aula em que a sessão de trabalho está aberta, com
  as duas séries de distâncias, e a tela apresenta o desfecho

### Requirement: A sessão de trabalho recebe o verificador do PIN de quem a abriu

Ao abrir a sessão de trabalho, com rede, a App 01 SHALL pedir ao núcleo o **verificador** do
PIN de quem se autenticou e guardá-lo **só enquanto durar aquela sessão de trabalho**, no mesmo
lugar do token dela, descartando-o quando ela encerra ou expira. O aparelho NEVER SHALL receber
nem guardar o PIN. Sem PIN cadastrado, a sessão de trabalho SHALL abrir mesmo assim, com aviso
de que confirmar identidade exige cadastrar o PIN na App 09 ou na App 03. (`RN-04-38`,
`RF-04-23`, PRD-04 §5.1)

#### Scenario: O verificador chega com a sessão de trabalho

- **WHEN** um Mestre com PIN cadastrado abre a sessão de trabalho com rede
- **THEN** o aparelho guarda o verificador do PIN dele, e nenhum PIN

#### Scenario: O verificador sai com a sessão

- **WHEN** a sessão de trabalho encerra ou expira
- **THEN** o verificador é apagado do aparelho

#### Scenario: Sem PIN, o aparelho abre e avisa

- **WHEN** um Admin sem PIN cadastrado abre a sessão de trabalho
- **THEN** o aparelho abre, e a tela avisa que confirmar identidade exige cadastrar o PIN

### Requirement: Quem integra a equipe a renomeia pelo aparelho

A App 01 SHALL oferecer **renomear** a equipe a quem a integra, na tela das equipes da aula e
na da equipe da trilha, com a mesma regra do nome da criação. A aplicação NEVER SHALL oferecer
renomear a quem não integra a equipe, nem à equipe da trilha já homologada. A recusa do núcleo
— nome repetido, em branco ou longo demais, aula encerrada — SHALL aparecer em linguagem
simples, e o nome anterior SHALL continuar na tela. (`RF-04-70`, `RN-04-39`, `RN-04-36`)

#### Scenario: Integrante troca o nome da equipe

- **WHEN** um integrante em sessão renomeia a equipe para um nome livre na aula
- **THEN** a tela passa a mostrar a equipe com o nome novo

#### Scenario: Quem não integra não vê a opção de renomear

- **WHEN** a tela das equipes mostra uma equipe de que o Guerreiro(a) em sessão não participa
- **THEN** a aplicação não oferece renomeá-la

#### Scenario: Nome repetido é recusado em linguagem simples

- **WHEN** um integrante tenta renomear a equipe com o nome de outra equipe da aula
- **THEN** a aplicação apresenta a recusa em linguagem simples e o nome anterior continua

#### Scenario: Equipe da trilha homologada não oferece renomear

- **WHEN** a tela da equipe da trilha já homologada é apresentada
- **THEN** a aplicação não oferece renomeá-la

### Requirement: A tela inicial oferece os três caminhos e volta ao início a cada atendimento

A App 01 SHALL apresentar, na tela inicial, os três caminhos — **onboarding**, **presença** e
**equipes**. Ao fim de cada atendimento, a aplicação SHALL voltar à tela inicial e NEVER SHALL
exibir dado do atendimento anterior. Quem escolhe **presença** ou **equipes** sem sessão de
Guerreiro(a) aberta SHALL ser levado à entrada do Guerreiro(a), nunca ao cadastro. (`RF-04-01`,
`RF-04-28`)

O caminho **presença** SHALL terminar no registro da presença: feito o registro, a aplicação
SHALL voltar à tela inicial e NEVER SHALL levar às equipes, que são outro momento (`RF-04-67`,
PRD-04 §5.4).

O caminho **equipes** SHALL levar à formação da equipe da aula e, escolhida a equipe, ao
trabalho da trilha — programação, missão, produção e assistente. Trabalhar a trilha NEVER SHALL
ser alcançável fora dele (`RF-04-68`, PRD-04 §§5.7, 5.8).

Com o **momento de troca aberto**, a tela inicial SHALL apresentar também o caminho da **troca
por recompensa avulsa**, ao lado dos três. Fechado o momento — que é o estado em que a aplicação
começa —, o caminho NEVER SHALL aparecer.

A tela inicial SHALL apresentar ainda o caminho do **quiz**, sempre disponível na sessão de
trabalho: diferentemente da troca, o PRD-04 não põe a partida atrás de um momento aberto por
Mestre, e é a própria tela do quiz que diz não haver partida quando não há. (`RF-04-01`,
`RF-04-28`, `RF-04-41`, `RF-04-49`, PRD-04 §12)

Cada caminho SHALL apresentar, **ao lado do rótulo textual que já tem**, o glifo do sistema de
ícone da camada comum, para que a criança reconheça o caminho antes de ler a linha inteira. O
glifo NEVER SHALL substituir o rótulo nem ser a única forma de distinguir um caminho do outro.
(`RF-04-01`, documento 15 §§5, 11.1, decisão do fundador de 2026-09-25)

#### Scenario: Os três caminhos aparecem

- **WHEN** a sessão de trabalho está aberta
- **THEN** a tela inicial apresenta o caminho do onboarding, o da presença e o das equipes

#### Scenario: Equipes sem sessão leva à entrada, não ao cadastro

- **WHEN** alguém escolhe equipes sem sessão de Guerreiro(a) aberta
- **THEN** a aplicação apresenta a entrada do Guerreiro(a), e nenhuma tela de cadastro aparece

#### Scenario: O caminho da presença termina no registro

- **WHEN** a presença é registrada pelo caminho da presença
- **THEN** a aplicação volta à tela inicial, e nenhuma tela de equipe aparece no mesmo
  atendimento

#### Scenario: Trabalhar a trilha acontece dentro das equipes

- **WHEN** a equipe do momento é escolhida no caminho das equipes
- **THEN** a aplicação mostra a programação do encontro, e esse é o único caminho que chega a
  ela

#### Scenario: O atendimento seguinte começa limpo

- **WHEN** um atendimento termina e a aplicação volta à tela inicial
- **THEN** nenhum dado do atendimento anterior aparece em tela alguma

#### Scenario: O caminho da troca só existe com o momento de troca aberto

- **WHEN** o Mestre abre o momento de troca
- **THEN** a tela inicial passa a apresentar também o caminho da troca, e volta a escondê-lo
  quando o momento é fechado

#### Scenario: O caminho do quiz não depende de momento aberto

- **WHEN** a sessão de trabalho está aberta e o momento de troca está fechado
- **THEN** a tela inicial apresenta o caminho do quiz

#### Scenario: Cada caminho leva glifo ao lado do rótulo

- **WHEN** a tela inicial é apresentada
- **THEN** cada caminho apresenta um glifo junto do rótulo textual, o rótulo continua legível por
  inteiro e nenhum caminho se identifica só pelo desenho

### Requirement: Os caminhos Equipes, Quiz e Troca só abrem para quem tem presença registrada

Aberta a sessão do Guerreiro(a) nos caminhos **equipes**, **quiz** e **troca**, a App 01 SHALL
consultar o núcleo sobre a presença dele na **aula em curso** e SHALL recusar o caminho a quem
não a tem, dizendo em linguagem simples que é preciso registrar a presença antes e oferecendo o
caminho **presença** ali mesmo. A recusa NEVER SHALL deixar o Guerreiro(a) sem desfecho na tela.
Quiz e troca entram nessa exigência por decisão do fundador de 2026-09-23, que estende o
`RN-04-40` aos dois. (`RF-04-68`, `RN-04-40`)

A aplicação SHALL encerrar a sessão aberta quando recusar o caminho, para que o atendimento
seguinte comece limpo (`RF-04-28`).

A recusa do núcleo à formação de equipe por falta de presença SHALL ser apresentada como o que
é, nunca como recusa do reconhecimento nem como falha de rede (`RN-04-36`).

Sem rede, esses três caminhos SHALL seguir indisponíveis como já são, e NEVER SHALL enfileirar
presença: a fila local é do caminho **presença** (`RF-04-23`, `RF-04-58`).

#### Scenario: Sem presença, o caminho das equipes não abre

- **WHEN** um Guerreiro(a) sem presença registrada no encontro entra pelo caminho das equipes
- **THEN** a aplicação diz que é preciso registrar a presença antes, oferece o caminho da
  presença e não mostra equipe alguma

#### Scenario: Com presença registrada, a volta às equipes passa

- **WHEN** um Guerreiro(a) que já registrou a presença no encontro volta pelo caminho das
  equipes
- **THEN** a aplicação abre a sessão dele e mostra as equipes da aula, sem aviso de presença já
  registrada

#### Scenario: Quiz e troca seguem a mesma exigência

- **WHEN** um Guerreiro(a) sem presença registrada entra pelo caminho do quiz ou pelo da troca
- **THEN** a aplicação recusa do mesmo modo e o encaminha ao caminho da presença

#### Scenario: A recusa do núcleo aparece como falta de presença

- **WHEN** o núcleo recusa a formação de equipe por falta de presença
- **THEN** a aplicação apresenta a falta de presença, e não a frase da recusa do reconhecimento

#### Scenario: Recusado o caminho, o atendimento não deixa sessão aberta

- **WHEN** o caminho é recusado por falta de presença e a tela volta ao início
- **THEN** nenhuma sessão de Guerreiro(a) segue aberta no aparelho

### Requirement: A tela de propósito único abre com o campo que ela existe para preencher focado

A App 01 SHALL declarar como campo inicial, nas telas cujo propósito é preencher um campo, aquele
campo — para que o atendimento comece na digitação, e não em alcançar o campo. O encontro
recomeça a cada Guerreiro(a) que chega (`RF-04-28`), e o gesto se paga em toda chegada.

As telas e os campos SHALL ser:

| Tela                                          | Campo inicial       | Origem                 |
| --------------------------------------------- | ------------------- | ---------------------- |
| Cadastro do onboarding                        | nome                | `RF-04-07`             |
| Entrada do Guerreiro(a) por nick e imagem     | nick                | `RF-04-18`, `RF-04-29` |
| Entrada do Guerreiro(a) por confirmação       | nick                | `RF-04-21`             |
| Formação da equipe da aula                    | nome da equipe      | `RF-04-30`, `RF-04-69` |
| Troca do nome da equipe                       | nome novo           | `RF-04-70`             |
| Equipe da trilha                              | nome da equipe      | `RF-04-61`             |
| Cadastro do responsável mínimo                | nome do responsável | `RF-04-60`             |

A aplicação NEVER SHALL declarar como inicial **mais de um campo** da mesma tela, e NEVER SHALL
declarar os campos **seguintes** — nick e data de nascimento no cadastro, papel na equipe, PIN na
confirmação. Eles são alcançados pelo percurso a partir do primeiro, e disputar o foco tiraria a
pessoa de onde ela está. Em particular, o **PIN** NEVER SHALL tomar o foco da tela de
confirmação: o nick é o primeiro dado do ato (`RF-04-21`).

O foco inicial NEVER SHALL alterar validação, rótulo, recusa ou qualquer desfecho das telas
alcançadas.

#### Scenario: A entrada do Guerreiro(a) abre com o nick focado

- **WHEN** a entrada do Guerreiro(a) é aberta por qualquer um dos quatro caminhos — presença,
  equipes, quiz ou troca
- **THEN** o campo do nick está com o foco

#### Scenario: A confirmação por PIN também começa no nick

- **WHEN** a tela de confirmação de Mestre ou Admin é apresentada
- **THEN** o campo do nick está com o foco, e o campo do PIN não

#### Scenario: O cadastro do onboarding abre com o nome focado

- **WHEN** a tela de cadastro do onboarding é apresentada
- **THEN** o campo do nome está com o foco, e os campos seguintes não

#### Scenario: A formação da equipe abre com o nome da equipe focado

- **WHEN** a tela das equipes da aula é apresentada
- **THEN** o campo do nome da equipe está com o foco, e o campo do papel não

#### Scenario: O foco inicial não muda o que a tela faz

- **WHEN** uma dessas telas é usada até o desfecho
- **THEN** a validação, as recusas e o desfecho são os mesmos de antes do foco inicial
