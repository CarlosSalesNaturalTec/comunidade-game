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

### Requirement: A tela inicial oferece os dois caminhos e volta ao início a cada atendimento

A App 01 SHALL apresentar, na tela inicial, os dois caminhos — **onboarding** e **trilhas**. Ao
fim de cada atendimento, a aplicação SHALL voltar à tela inicial e NEVER SHALL exibir dado do
atendimento anterior. Quem escolhe **trilhas** sem sessão de Guerreiro(a) aberta SHALL ser
levado à entrada do Guerreiro(a), nunca ao cadastro.

Com o **momento de troca aberto**, a tela inicial SHALL apresentar também o caminho da **troca
por recompensa avulsa**, ao lado dos dois. Fechado o momento — que é o estado em que a aplicação
começa —, o caminho NEVER SHALL aparecer. (`RF-04-01`, `RF-04-28`, `RF-04-49`, PRD-04 §12)

#### Scenario: Os dois caminhos aparecem

- **WHEN** a sessão de trabalho está aberta
- **THEN** a tela inicial apresenta o caminho do onboarding e o caminho das trilhas

#### Scenario: Trilhas sem sessão leva à entrada, não ao cadastro

- **WHEN** alguém escolhe trilhas sem sessão de Guerreiro(a) aberta
- **THEN** a aplicação apresenta a entrada do Guerreiro(a), e nenhuma tela de cadastro aparece

#### Scenario: O atendimento seguinte começa limpo

- **WHEN** um atendimento termina e a aplicação volta à tela inicial
- **THEN** nenhum dado do atendimento anterior aparece em tela alguma

#### Scenario: O terceiro caminho só existe com o momento de troca aberto

- **WHEN** o Mestre abre o momento de troca
- **THEN** a tela inicial passa a apresentar também o caminho da troca, e volta a escondê-lo
  quando o momento é fechado

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

### Requirement: O Guerreiro(a) entra por nick e imagem, e a presença é registrada na entrada

A App 01 SHALL oferecer, no caminho das trilhas, a entrada por **nick e imagem**: o nick
informado na tela e o **descritor gerado no próprio aparelho**, na ordem prova de vivacidade e
depois descritor facial. Ao núcleo SHALL ir apenas o descritor; a fotografia SHALL ser
descartada sem sair do aparelho e NEVER SHALL ser exibida, gravada nem enviada.

Reconhecido o Guerreiro(a), a aplicação SHALL abrir a sessão dele e SHALL registrar a
**presença do dia no modo reconhecimento**, no mesmo atendimento. Presença já constante do
encontro NEVER SHALL ser duplicada nem tratada como erro: a aplicação SHALL avisar que ela já
existe e voltar à tela inicial. (`RF-04-18`, `RF-04-19`, `RF-04-29`, `RN-04-12`, `RN-04-06`,
PRD-04 §5.4)

#### Scenario: Nick e imagem conferem

- **WHEN** o Guerreiro(a) informa o nick e a câmera captura a imagem dele na chegada
- **THEN** a aplicação abre a sessão do Guerreiro(a) e registra a presença do dia por
  reconhecimento

#### Scenario: A presença do encontro já constava

- **WHEN** um Guerreiro(a) já com presença registrada naquela aula é reconhecido de novo
- **THEN** a aplicação avisa que a presença já existe, não duplica registro algum e volta à
  tela inicial

#### Scenario: Nenhuma imagem de criança sai do aparelho

- **WHEN** a entrada por nick e imagem acontece
- **THEN** nenhuma requisição carrega fotografia, e nenhuma imagem fica gravada no aparelho
  compartilhado

#### Scenario: Sem câmera, a entrada segue pela confirmação humana

- **WHEN** o aparelho não tem câmera disponível
- **THEN** a aplicação não oferece a captura e encaminha o Guerreiro(a) à confirmação de Mestre
  ou Admin, sem deixá-lo fora da aula

### Requirement: A falha de identificação oferece nova tentativa sem revelar nada

A App 01 SHALL responder à recusa do núcleo com a **mesma frase** em todos os casos — nick
inexistente, Guerreiro(a) sem _template_ gravado e descritor que não confere —, sem revelar
qual deles ocorreu, e SHALL oferecer **nova tentativa** de captura. Persistindo a falha, a
aplicação SHALL encaminhar à **confirmação de Mestre ou Admin**, e NEVER SHALL encerrar o
atendimento deixando o Guerreiro(a) fora da aula. (`RF-04-20`, `RN-01-22`, `RN-04-09`, PRD-04
§5.5)

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

### Requirement: O Guerreiro(a) entra no caminho das trilhas por confirmação de Mestre ou Admin

A App 01 SHALL abrir a sessão do Guerreiro(a) pela **confirmação de identidade** feita por
Mestre ou Admin presente no encontro, com registro de quem confirmou, e SHALL registrar, no
mesmo ato, a **presença do dia no modo confirmação**, com o mesmo adulto como confirmador. A
recusa de biometria e a ausência de _template_ NEVER SHALL deixar o Guerreiro(a) fora da aula:
a confirmação humana é a alternativa equivalente.

A confirmação humana deixa de ser o único caminho de entrada e passa a ser o que o `RN-04-09`
sempre disse que ela era — a alternativa de quem não tem _template_, de quem recusou a
biometria e de quem a câmera não reconheceu. A sessão que ela abre SHALL ter os mesmos direitos
da aberta por reconhecimento. (`RF-04-29`, `RF-04-15`, `RF-04-21`, `RN-04-09`, PRD-04 §§5.3,
5.5)

#### Scenario: Mestre confirma e a sessão do Guerreiro(a) abre

- **WHEN** o Guerreiro(a) informa o nick e o Mestre presente confirma a identidade dele
- **THEN** a aplicação abre a sessão do Guerreiro(a), registra quem confirmou e grava a
  presença do dia por confirmação

#### Scenario: A recusa não exclui ninguém da aula

- **WHEN** um Guerreiro(a) sem _template_ gravado chega ao caminho das trilhas
- **THEN** a aplicação o encaminha à confirmação humana, sem impedi-lo de participar

#### Scenario: A presença confirmada guarda quem confirmou

- **WHEN** a sessão é aberta por confirmação presencial
- **THEN** a presença gravada aponta o adulto que confirmou, e não o modo reconhecimento

#### Scenario: Nenhuma imagem de criança sai do aparelho nesta fatia

- **WHEN** a entrada acontece por confirmação humana
- **THEN** nenhuma requisição da aplicação carrega fotografia, e nenhuma imagem é gravada no
  aparelho compartilhado

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
**papel** que terá — que vale para o encontro inteiro e é opcional. A aplicação SHALL apresentar
as recusas do núcleo — sexto integrante e segundo integrante de 17 anos ou mais — em linguagem
simples, sem código de erro cru. (`RF-04-30`, `RF-04-31`, `RF-04-59`, `RN-04-15`, `RN-04-16`,
`RN-04-30`, PRD-04 §12)

#### Scenario: Guerreiro(a) cria a equipe e entra nela

- **WHEN** um Guerreiro(a) em sessão cria uma equipe da aula vigente
- **THEN** a equipe nasce com ele como primeiro integrante, sem aprovação de ninguém

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

A App 01 SHALL apresentar as equipes já formadas na aula vigente por **avatar e nick**, e
NEVER SHALL exibir nome, data de nascimento, imagem ou qualquer outro dado pessoal de um
Guerreiro(a) para outro. (`RF-04-34`, `RN-04-14`, documento 99 §6 invariante 11)

#### Scenario: As equipes da aula aparecem por avatar e nick

- **WHEN** o Guerreiro(a) em sessão abre a tela das equipes da aula vigente
- **THEN** cada equipe aparece com o avatar e o nick de cada integrante, e nada além disso

#### Scenario: Nenhuma imagem de um Guerreiro(a) é exibida a outro

- **WHEN** a tela das equipes é apresentada
- **THEN** nenhuma fotografia de Guerreiro(a) aparece em tela alguma

#### Scenario: Equipes de outra aula não aparecem

- **WHEN** a tela das equipes da aula vigente é apresentada
- **THEN** as equipes formadas em outras aulas não estão entre as exibidas

### Requirement: A App 01 não forma equipe pela gestão nem homologa equipe da trilha

A App 01 NEVER SHALL oferecer a Mestre ou Admin a formação ou a alteração da composição de
equipe: a sessão de trabalho do aparelho autentica o encontro, e quem forma equipe é o
Guerreiro(a) em sessão. A **homologação da equipe da trilha** NEVER SHALL aparecer nesta
aplicação — é ato do Mestre, na App 09. (`RN-04-18`, `RF-01-16`, `RF-01-63`, documento 99 §6
invariante 15)

#### Scenario: A sessão de trabalho não forma equipe

- **WHEN** a sessão de trabalho do aparelho está aberta e nenhum Guerreiro(a) tem sessão
- **THEN** a aplicação não oferece criar equipe, entrar nem sair

#### Scenario: A homologação não aparece na App 01

- **WHEN** qualquer tela de equipe é apresentada
- **THEN** nenhuma ação de homologar equipe da trilha é oferecida

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

#### Scenario: O termo aparece antes da câmera

- **WHEN** o cadastro chega ao passo da imagem com o responsável presente
- **THEN** a aplicação exibe o termo e não abre a câmera enquanto a confirmação não for dada

#### Scenario: Quem confirma fica registrado como testemunha

- **WHEN** o Mestre confirma que o termo impresso foi assinado
- **THEN** o consentimento é registrado no núcleo com ele como testemunha, e só então a câmera é
  aberta

#### Scenario: Captura sem consentimento registrado é recusada

- **WHEN** o envio do descritor é tentado sem consentimento de biometria registrado
- **THEN** o núcleo recusa com 422 e a aplicação explica a recusa em linguagem simples

### Requirement: O descritor nasce no aparelho, depois da prova de vivacidade

A App 01 SHALL gerar o _template_ no **navegador do próprio aparelho**, na ordem **prova de
vivacidade e, depois, descritor facial**, e SHALL enviar ao núcleo **apenas o descritor**. A
aplicação NEVER SHALL pôr a fotografia em corpo de requisição, em registro de erro ou em
armazenamento do aparelho, e NEVER SHALL exibir a imagem de um Guerreiro(a) em tela alguma. A
fotografia SHALL ser descartada na geração do descritor. (`RF-04-14`, `RF-04-48`, `RN-04-06`,
`RN-04-08`, `RN-04-12`, `RN-04-14`, documento 03 §3.3, documento 99 §6 invariante 12)

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
