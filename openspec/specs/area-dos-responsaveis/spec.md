## Purpose

A App 07, porta do responsável: por onde ele entra, o que a aplicação lhe mostra dos Guerreiros
e Guerreiras vinculados a ele, e o que ela deliberadamente não oferece — cadastro, vínculo,
criança de terceiro e o que a criança faz sozinha.

## Requirements

### Requirement: A Área dos responsáveis é inteiramente autenticada e se identifica por chave

A App 07 SHALL apresentar a entrada a quem não tem sessão aberta, e NEVER SHALL servir tela de
dado de criança sem sessão de responsável. Toda chamada ao núcleo SHALL levar a **chave da
própria aplicação** e, havendo sessão, a credencial da persona. (`RF-13-01`, `RF-01-02`,
`RN-01-32`)

A sessão de **Admin** ou de **Mestre** SHALL ser admitida na aplicação **apenas no modo
assistido**, e nenhuma outra persona SHALL entrar: quem chega com sessão de Guerreiro(a) ou de
Apoiador SHALL ser recusado com a orientação de que a área é dos responsáveis. (`RF-13-01`,
`RF-13-35`, `RF-01-02`, `RN-01-32`)

#### Scenario: Visitante sem sessão

- **WHEN** alguém abre a App 07 sem sessão aberta
- **THEN** só a entrada é apresentada, e nenhuma tela de dado de criança

#### Scenario: A aplicação se identifica com a própria chave

- **WHEN** a App 07 chama uma rota de dados do núcleo
- **THEN** a chamada leva a chave da App 07, e não a de outra aplicação

#### Scenario: A sessão de Mestre só alcança o modo assistido

- **WHEN** um Mestre entra na App 07
- **THEN** alcança o modo assistido e nada além dele

#### Scenario: Guerreiro(a) e Apoiador continuam recusados

- **WHEN** alguém entra na App 07 com sessão de Guerreiro(a) ou de Apoiador
- **THEN** a entrada é recusada, com a orientação de que a área é dos responsáveis

### Requirement: O responsável entra por login social ou por usuário e senha da gestão

A App 07 SHALL oferecer os dois caminhos de entrada do responsável: **login social** e
**usuário e senha** criados pela gestão. NEVER SHALL oferecer autocadastro. (`RF-13-01`,
`RN-13-01`)

#### Scenario: Entrada por login social

- **WHEN** um responsável já cadastrado entra por login social
- **THEN** a sessão é aberta e ele alcança as telas da aplicação

#### Scenario: Entrada por usuário e senha

- **WHEN** um responsável já cadastrado entra com o usuário e a senha criados pela gestão
- **THEN** a sessão é aberta e ele alcança as telas da aplicação

#### Scenario: Não há por onde se cadastrar

- **WHEN** o responsável percorre a entrada da aplicação
- **THEN** não há caminho de autocadastro

### Requirement: A senha provisória tranca todas as demais telas

A App 07 SHALL exigir a **troca da senha provisória** antes de qualquer outra tela, e NEVER
SHALL apresentar dado de criança enquanto a troca não acontecer. Não SHALL existir caminho de
contorno da troca. (`RF-13-02`)

#### Scenario: Entrada com senha provisória

- **WHEN** um responsável entra com a senha provisória criada pela gestão
- **THEN** a única tela apresentada é a da troca de senha

#### Scenario: Depois da troca

- **WHEN** o responsável troca a senha provisória
- **THEN** ele alcança a lista dos vinculados

### Requirement: Login não cria cadastro, e a recusa orienta a procurar a gestão

A App 07 SHALL recusar a entrada de conta **sem cadastro prévio** de responsável, e a recusa
SHALL orientar a **procurar a gestão no encontro**. A entrada NEVER SHALL criar persona.
(`RF-13-03`, `RN-13-02`)

#### Scenario: Conta social sem cadastro prévio

- **WHEN** alguém entra por login social com uma conta que não corresponde a responsável
  cadastrado
- **THEN** a entrada é recusada, a tela orienta a procurar a gestão no encontro e nenhuma
  persona é criada

### Requirement: A aplicação lista apenas os vinculados, com o grau de parentesco

A App 07 SHALL apresentar ao responsável **apenas os Guerreiros e Guerreiras vinculados a ele**,
cada um com o **grau de parentesco** declarado no cadastro. NEVER SHALL apresentar criança não
vinculada, nem por busca, nem por endereço direto. (`RF-13-04`, `RN-13-04`)

#### Scenario: A lista traz os vinculados com o parentesco

- **WHEN** um responsável com dois vinculados abre a aplicação
- **THEN** os dois aparecem, cada um com o grau de parentesco declarado

#### Scenario: Criança não vinculada não aparece nem por busca

- **WHEN** o responsável procura por um Guerreiro(a) que não é seu vinculado
- **THEN** a aplicação não o apresenta, e a recusa do núcleo não revela dado algum daquela
  criança

### Requirement: O responsável alterna entre os vinculados sem sair da aplicação

A App 07 SHALL permitir ao responsável com mais de um vinculado **alternar entre eles** sem
encerrar a sessão e sem voltar à entrada. (`RF-13-05`)

#### Scenario: Troca de criança

- **WHEN** o responsável está vendo a evolução de um vinculado e escolhe outro
- **THEN** a aplicação passa a apresentar o segundo, com a mesma sessão

### Requirement: A aplicação não cadastra responsável nem cria ou edita vínculo

A App 07 NEVER SHALL oferecer tela de cadastro de responsável, de criação de vínculo, de edição
de vínculo ou de mudança do grau de parentesco: tudo isso é ato da gestão. (`RF-13-06`,
`RN-13-01`)

#### Scenario: Nenhum caminho de cadastro ou de vínculo

- **WHEN** o responsável percorre todas as telas da aplicação
- **THEN** não há caminho de cadastro de responsável nem de criação, edição ou remoção de
  vínculo

### Requirement: O painel apresenta a evolução do vinculado, com o nível como percurso

A App 07 SHALL apresentar, do vinculado escolhido, **presença, atividades realizadas, pontos,
poderes, badges e nível**, o **progresso de cada trilha como percurso** — o que foi concluído e
o que falta —, e as **criações originais validadas** com título, trilha e data. O nível NEVER
SHALL ser apresentado como saldo de pontos. (`RF-13-07`, `RF-13-08`, `RF-13-10`)

#### Scenario: Painel de um vinculado com histórico

- **WHEN** o responsável abre o painel de um vinculado que tem presença, atividades, pontos,
  poderes, badges, nível, trilha em andamento e criação validada
- **THEN** a tela apresenta todos esses itens, com o progresso da trilha em missões concluídas e
  faltantes

#### Scenario: O nível não é saldo

- **WHEN** a tela apresenta o nível do vinculado
- **THEN** o que o exprime é o percurso da trilha, e não o saldo de pontos

### Requirement: A ocorrência de conduta é apresentada com motivo e data

A App 07 SHALL apresentar as **ocorrências de conduta** do vinculado, cada uma com o **motivo**
e a **data**, em linguagem simples e sem código de erro. Ocorrência sem motivo guardado SHALL
ser apresentada com a data, sem inventar texto no lugar do motivo. (`RF-13-09`, `RN-13-21`)

#### Scenario: Ocorrência com motivo

- **WHEN** o vinculado tem ocorrência de conduta com motivo guardado
- **THEN** a tela a apresenta com o motivo e a data

#### Scenario: Ocorrência de ciclo anterior

- **WHEN** o vinculado tem ocorrência cujo motivo já foi apagado pelo encerramento do ciclo
- **THEN** a tela a apresenta com a data e sem motivo, sem texto substituto

### Requirement: Nenhuma tela expõe o que a criança faz sozinha nem dado de outra criança

A App 07 NEVER SHALL apresentar consulta ao assistente, transcrição de apoio escolar ou dado
identificável de **outra criança** — nem em equipe, nem em ranking, nem em criação coletiva.
(`RF-13-11`, `RF-13-12`, `RN-13-20`)

#### Scenario: Vinculado que usou o assistente e integra equipe

- **WHEN** o responsável percorre o painel de um vinculado que fez consultas ao assistente, teve
  apoio escolar transcrito e integra equipe de trilha
- **THEN** nenhuma tela apresenta consulta, transcrição ou dado identificável das outras
  crianças

### Requirement: A tela declara o que a autorização libera e o que não depende dela, antes do ato

A App 07 SHALL apresentar, **antes de qualquer botão de decisão**, o que a autorização única
libera — divulgação do perfil, do histórico e das criações, imagem em fotos e vídeos de eventos e
captação da produção por foto do manuscrito ou áudio — e o que **não** depende dela: a
participação nas atividades, que é livre, e a biometria do onboarding, que tem termo impresso
próprio. O texto SHALL estar em **linguagem simples de adulto**, sem jargão jurídico e sem código
de erro. A tela NEVER SHALL oferecer decisão separada por finalidade: a autorização é uma só.
(`RF-13-13`, `RN-13-05`, `RN-13-06`)

#### Scenario: A declaração vem antes da decisão

- **WHEN** o responsável abre a tela da autorização de um vinculado
- **THEN** o que a autorização libera e o que não depende dela aparecem antes de qualquer botão
  de conceder ou revogar

#### Scenario: Uma decisão só, para tudo

- **WHEN** o responsável percorre a tela da autorização
- **THEN** não há caminho de autorizar a divulgação sem a imagem em eventos, nem qualquer outra
  decisão por finalidade separada

### Requirement: O responsável concede e revoga pela tela, com o efeito dito no mesmo ato

A App 07 SHALL oferecer ao responsável **conceder** e **revogar** a autorização do vinculado
escolhido, e SHALL dizer, no mesmo ato, o efeito do que ele acaba de fazer: concedida, o perfil
passa a aparecer na vitrine e nos rankings públicos; revogada, perfil, criações e elenco do jogo
saem do que é público **na hora**, sem apagar nada e sem prejuízo da participação. A tela NEVER
SHALL sugerir que a revogação apaga registro ou tira a criança de atividade. (`RF-13-14`,
`RF-13-15`, `RF-13-16`, `RN-13-08`, `RN-13-09`)

Conceder e revogar **exigem rede**, porque geram registro versionado. Falhando a chamada, a App
07 SHALL dizer que a decisão **não foi registrada** e NEVER SHALL apresentar sucesso, apresentar
o estado novo ou dar a decisão por tomada. (PRD-13 §10)

#### Scenario: Concessão e o que ela produz

- **WHEN** o responsável concede a autorização de um vinculado
- **THEN** a tela passa a apresentar o estado vigente e diz que o perfil passa a aparecer na
  vitrine e nos rankings públicos

#### Scenario: Revogação e o que ela produz

- **WHEN** o responsável revoga a autorização de um vinculado
- **THEN** a tela diz que perfil, criações e elenco do jogo saem do que é público na hora, que
  nada é apagado e que a participação segue

#### Scenario: Sem rede, nada é dado por registrado

- **WHEN** a chamada da decisão falha por rede
- **THEN** a tela diz que a decisão não foi registrada, e o estado apresentado continua sendo o
  anterior

### Requirement: A tela informa a alternativa equivalente enquanto não houver autorização

A App 07 SHALL apresentar, sempre que a autorização do vinculado **não estiver vigente** — não
autorizada ou suspensa —, a **alternativa equivalente** em vigor: o Guerreiro(a) entrega a
produção ao Mestre no encontro, participa de tudo e não aparece publicamente. A tela NEVER SHALL
apresentar a ausência de autorização como perda, punição ou pendência da criança. (`RF-13-20`,
`RN-13-09`)

#### Scenario: Sem autorização, a alternativa aparece

- **WHEN** o responsável abre a tela de um vinculado sem autorização vigente
- **THEN** a tela apresenta a entrega da produção ao Mestre no encontro como alternativa, e diz
  que a criança participa de tudo

#### Scenario: A alternativa também vale no estado suspenso

- **WHEN** a autorização do vinculado está suspensa
- **THEN** a mesma alternativa equivalente é apresentada

### Requirement: O estado suspenso aparece com quem o motivou, data e hora

A App 07 SHALL apresentar os **três estados** da autorização do vinculado — vigente, suspensa e
não autorizada — em linguagem simples, e, estando **suspensa**, SHALL nomear **quem a motivou**
com a **data e a hora** daquela recusa, e dizer que a gestão vai tratar com a família. A tela
NEVER SHALL apresentar o estado suspenso como erro nem oferecer caminho de sobrepor a recusa do
outro responsável. (`RF-13-17`, `RF-13-18`, `RN-13-07`)

Recebendo a recusa do núcleo à concessão que colide com a recusa de outro responsável, a App 07
SHALL apresentar o estado suspenso e a **orientação de procurar a gestão**, nunca um código de
erro. (PRD-13 §§9, 10)

#### Scenario: Suspensa nomeia quem recusou

- **WHEN** o responsável abre a tela de um vinculado cuja autorização está suspensa
- **THEN** a tela diz que está suspensa, quem a motivou, quando, e que a gestão vai tratar com a
  família

#### Scenario: A concessão que colide vira orientação, não erro

- **WHEN** o responsável concede e o núcleo recusa porque outro responsável tem recusa vigente
- **THEN** a tela apresenta o estado suspenso e a orientação de procurar a gestão, sem código de
  erro

### Requirement: O histórico da autorização mostra cada decisão, com a versão do termo

A App 07 SHALL apresentar o **histórico da autorização** do vinculado — cada concessão e cada
revogação, do mais recente ao mais antigo, com **quem decidiu**, a **versão do termo**, a data e
a hora. A tela NEVER SHALL oferecer caminho de editar ou apagar decisão do histórico: o registro
é somente inserção. (`RF-13-21`, `RN-13-10`)

#### Scenario: Histórico de quem concedeu, revogou e concedeu de novo

- **WHEN** o responsável abre o histórico de um vinculado com três decisões registradas
- **THEN** as três aparecem, da mais recente à mais antiga, cada uma com quem decidiu, a versão
  do termo, a data e a hora

#### Scenario: Nada se apaga no histórico

- **WHEN** o responsável percorre o histórico
- **THEN** não há caminho de editar nem de apagar decisão alguma

### Requirement: O responsável alcança a autorização do vinculado sem sair da aplicação

A App 07 SHALL oferecer, do vinculado escolhido, o caminho entre a **evolução** e a
**autorização** sem encerrar a sessão e sem voltar à entrada, e SHALL manter a alternância entre
vinculados válida nas duas. A tela da autorização NEVER SHALL alcançar Guerreiro(a) não
vinculado. (`RF-13-05`, `RN-13-04`)

#### Scenario: Da evolução à autorização e de volta

- **WHEN** o responsável está na evolução de um vinculado e escolhe a autorização
- **THEN** a aplicação apresenta a autorização daquele vinculado, com a mesma sessão, e o
  caminho de volta à evolução

#### Scenario: Trocar de vinculado troca a autorização apresentada

- **WHEN** o responsável está na autorização de um vinculado e escolhe outro
- **THEN** a aplicação passa a apresentar a autorização do segundo

### Requirement: O responsável abre solicitação nos quatro tipos, sobre o vinculado escolhido

A App 07 SHALL oferecer ao responsável a abertura de solicitação nos **quatro tipos** — acesso,
correção, exclusão e esclarecimento —, sempre sobre um **vinculado**, com o texto do pedido. A
tela NEVER SHALL oferecer criança não vinculada, e a confirmação SHALL apresentar o **protocolo**
e o **prazo de 7 dias** que o núcleo devolveu, sem inventar nenhum dos dois. A segunda
solicitação idêntica em aberto, que o núcleo recusa, SHALL ser explicada em linguagem simples,
apontando a que já está na fila. (`RF-13-22`, `RF-13-24`, `RN-13-13`, `RN-13-14`)

#### Scenario: Pedido de acesso confirmado

- **WHEN** o responsável abre uma solicitação de acesso sobre um vinculado
- **THEN** a tela apresenta o protocolo e o prazo de 7 dias devolvidos pelo núcleo

#### Scenario: Só os vinculados aparecem na escolha

- **WHEN** o responsável escolhe sobre quem abrir a solicitação
- **THEN** apenas os vinculados a ele aparecem

#### Scenario: Duplicata em aberto é explicada

- **WHEN** o responsável tenta abrir a segunda solicitação do mesmo tipo sobre o mesmo vinculado
  com a primeira ainda sem desfecho
- **THEN** a tela explica que já existe uma na fila e não apresenta protocolo novo

### Requirement: O pedido de exclusão declara o limite antes do aceite

A App 07 SHALL apresentar, **antes de o responsável confirmar** um pedido de exclusão, o limite
declarado do pedido, em linguagem simples de adulto: o **registro de dado do território é
despersonalizado, não apagado** — o vínculo de autoria é rompido e o mapeamento destruído, e a
medição permanece na série sem apontar pessoa alguma —, e o **_template_ biométrico é a exceção:
esse é apagado**. O aceite NEVER SHALL ficar disponível antes de o limite ser apresentado, e o
limite NEVER SHALL aparecer só depois da confirmação. (`RF-13-23`, `RN-13-12`, `RN-13-22`,
documento 03 §§9, 12.1)

#### Scenario: O limite aparece antes do botão

- **WHEN** o responsável escolhe o tipo exclusão
- **THEN** a tela apresenta o limite da despersonalização e a exceção do _template_ antes de
  oferecer a confirmação

#### Scenario: O limite não é surpresa posterior

- **WHEN** o responsável confirma o pedido de exclusão
- **THEN** nada sobre o limite é dito ali pela primeira vez: o texto já estava na tela do aceite

#### Scenario: Os outros três tipos não trazem o limite

- **WHEN** o responsável abre uma solicitação de acesso, correção ou esclarecimento
- **THEN** a tela não apresenta o texto do limite da exclusão, que não se aplica a eles

### Requirement: O responsável acompanha as próprias solicitações, com o atraso à vista

A App 07 SHALL apresentar ao responsável **apenas as próprias** solicitações, cada uma com
protocolo, tipo, vinculado, situação, prazo e, quando houver, o desfecho e a data. A solicitação
**em atraso** SHALL ser sinalizada como tal, e a sinalização SHALL ser a que o núcleo derivou —
a aplicação NEVER SHALL calcular atraso por conta própria. A tela NEVER SHALL apresentar
solicitação de outro responsável. (`RF-13-25`, `RF-13-26`, `RN-13-13`, `RN-13-14`)

#### Scenario: A lista traz protocolo, situação e prazo

- **WHEN** o responsável abre as próprias solicitações
- **THEN** cada uma aparece com protocolo, tipo, vinculado, situação e prazo

#### Scenario: A solicitação vencida aparece em atraso

- **WHEN** uma solicitação passou dos 7 dias sem desfecho
- **THEN** a tela a sinaliza em atraso, e ela continua na lista como aberta

#### Scenario: O desfecho aparece com a data

- **WHEN** a gestão trata uma solicitação
- **THEN** a tela passa a mostrar a situação final, o texto do desfecho e a data

#### Scenario: A lista não alcança outra família

- **WHEN** o responsável abre as próprias solicitações
- **THEN** nenhuma solicitação aberta por outro responsável aparece

### Requirement: A tela da recusa da imagem tem termo próprio e não oferece concessão

A App 07 SHALL oferecer ao responsável a **recusa da imagem captada no onboarding**, apresentando
o **termo próprio da biometria** — distinto do termo da autorização única — e dizendo, antes do
ato, para que a imagem serve: identificar o Guerreiro(a) na presença e na entrada, e nada mais.
A tela NEVER SHALL oferecer a **concessão** da biometria: essa é do termo impresso assinado no
encontro, e a aplicação SHALL dizê-lo a quem quiser voltar atrás. A recusa NEVER SHALL aparecer
misturada com a autorização única, nem alterá-la. (`RF-13-27`, `RN-13-05`, `RN-13-06`,
PRD-13 §3.2)

#### Scenario: A tela apresenta o termo próprio antes do ato

- **WHEN** o responsável abre a recusa da imagem do onboarding
- **THEN** o termo próprio da biometria e a finalidade da imagem são apresentados antes de a
  recusa ser oferecida

#### Scenario: Não há por onde conceder a biometria

- **WHEN** o responsável percorre a tela
- **THEN** nenhum caminho concede a biometria, e a tela informa que a concessão é o termo
  impresso assinado no encontro

#### Scenario: A recusa não mexe na autorização única

- **WHEN** o responsável recusa a imagem do onboarding
- **THEN** o estado da autorização única do vinculado permanece como estava

### Requirement: A tela declara a alternativa equivalente e o apagamento, com a data

A App 07 SHALL declarar, no mesmo ato da recusa, que **a criança não fica de fora de nada**: sem
captura ela entra por **nick e confirmação do Mestre ou de um Admin no encontro**, e participa
igual. Havendo apagamento marcado — pela recusa, pelo pedido de exclusão deferido ou pelo fim do
vínculo —, a aplicação SHALL exibir ao responsável **em que data** o _template_ será apagado, o
que o originou, e o que isso significa caso o Guerreiro(a) volte: **nova captura, com novo
termo**. O aviso SHALL viver na própria aplicação, sem notificação por e-mail. A data exibida
SHALL ser a que o núcleo devolveu. (`RF-13-28`, `RF-13-43`, `RF-13-44`, `RN-13-09`, `RN-13-15`,
`RN-13-22`, decisão do fundador, 2026-08-31, documento 09 §1)

#### Scenario: A alternativa é dita antes da recusa

- **WHEN** o responsável está prestes a recusar a imagem do onboarding
- **THEN** a tela diz que a criança segue participando de tudo, entrando por nick e confirmação
  humana no encontro

#### Scenario: O aviso do apagamento traz a data

- **WHEN** o _template_ de um vinculado está marcado para apagamento
- **THEN** a aplicação exibe a data do apagamento, o que o originou e que a volta exige nova
  captura com novo termo

#### Scenario: O aviso aparece também quando veio do fim do vínculo

- **WHEN** o vínculo do Guerreiro(a) com o projeto é encerrado pela gestão
- **THEN** o responsável vê na aplicação o aviso do apagamento com a data, sem ter pedido nada

#### Scenario: Sem marca, nenhum aviso é exibido

- **WHEN** o vinculado não tem apagamento marcado
- **THEN** nenhuma data de apagamento é exibida

### Requirement: A aplicação mostra o que a plataforma guarda do vinculado

A App 07 SHALL apresentar, para o vinculado escolhido, a lista dos **dados armazenados**, cada
um com a **finalidade** e o **prazo de guarda**, em **linguagem simples de adulto** — sem
jargão jurídico, sem termo técnico e sem código de erro na tela. A tela SHALL marcar o que o
núcleo **não guarda hoje** daquele vinculado, e SHALL declarar que a consulta ao assistente e a
transcrição de apoio escolar são **restritas à gestão**, porque o que a criança faz sozinha
continua dela.

A tela é de **leitura**: NEVER SHALL oferecer escrita, exclusão ou exportação de dado — o
pedido de acesso, correção ou exclusão continua sendo a solicitação, que a aplicação já
oferece. (`RF-13-29`, `RN-13-20`, PRD-13 §§10, 11)

#### Scenario: A tela apresenta dado, finalidade e prazo

- **WHEN** o responsável abre a transparência de um vinculado
- **THEN** vê cada dado armazenado com a finalidade e por quanto tempo ele fica

#### Scenario: O que a criança faz sozinha aparece como restrito à gestão

- **WHEN** o responsável percorre a lista
- **THEN** a consulta ao assistente e a transcrição de apoio escolar aparecem marcadas como
  restritas à gestão, sem nenhum conteúdo

#### Scenario: A tela não escreve nem exporta

- **WHEN** o responsável lê a transparência
- **THEN** não lhe é oferecida escrita, exclusão nem exportação, e o caminho do pedido é a
  solicitação

### Requirement: A aplicação lista quem acessou os dados do vinculado

A App 07 SHALL apresentar o **histórico de acessos** do vinculado, cada linha com **data**,
**hora**, **quem acessou**, **em que papel** e **qual dado**, da mais recente para a mais
antiga. O acesso de **rotina** — o trabalho do Mestre da turma — SHALL ser apresentado como
rotina, e a tela NEVER SHALL sugerir irregularidade onde há trabalho normal.

A tela NEVER SHALL apresentar acesso a dado de **outra criança** nem o **conteúdo** do que foi
escrito. (`RF-13-30`, `RN-13-04`, PRD-13 §§5.6, 12)

#### Scenario: O acesso do Mestre da turma aparece com data, hora e dado

- **WHEN** o responsável abre o histórico de acessos de um vinculado
- **THEN** o acesso do Mestre da turma aparece com data, hora, quem acessou, o papel e o dado
  consultado

#### Scenario: O acesso de rotina não é apresentado como suspeita

- **WHEN** a linha do histórico é de trabalho de rotina do Mestre
- **THEN** a tela a apresenta como rotina, sem alerta nem linguagem de irregularidade

#### Scenario: Nenhuma linha é de outra criança

- **WHEN** o responsável percorre o histórico
- **THEN** nenhuma linha se refere a criança que não é vinculada a ele

### Requirement: O responsável abre esclarecimento a partir de um acesso listado

A App 07 SHALL oferecer, **em cada linha do histórico de acessos**, o caminho para abrir uma
solicitação de **esclarecimento** sobre aquele acesso, sem sair da tela. A solicitação SHALL
entrar como qualquer outra — com protocolo, prazo de 7 dias e acompanhamento —, e a tela SHALL
levar junto a referência do acesso que a originou. (`RF-13-31`, `RN-13-14`)

#### Scenario: O esclarecimento nasce da linha do acesso

- **WHEN** o responsável não entende um acesso listado e aciona o esclarecimento ali mesmo
- **THEN** a solicitação de esclarecimento é aberta com a referência daquele acesso, com
  protocolo e prazo de 7 dias

### Requirement: A aplicação apresenta o termo vigente e registra a leitura

A App 07 SHALL apresentar o **texto do termo vigente** em linguagem simples e SHALL **registrar
a leitura** do responsável, com data e hora. O registro SHALL acontecer quando ele **lê** o
termo, e a tela SHALL dizer que o registro aconteceu e o que ele significa — prova de ciência,
não consentimento.

A tela do termo NEVER SHALL conceder nem revogar autorização: a decisão continua sendo a da
tela de autorização. (`RF-13-32`, PRD-13 §§6.5, 11)

#### Scenario: O responsável lê o termo e a leitura fica registrada

- **WHEN** o responsável abre o termo vigente
- **THEN** vê o texto em linguagem simples, e a leitura é registrada com data e hora

#### Scenario: Ler o termo não decide a autorização

- **WHEN** o responsável lê o termo da autorização única
- **THEN** o estado da autorização do vinculado não muda, e a tela não oferece decisão ali

### Requirement: O histórico de termos mostra a versão que valia em cada data

A App 07 SHALL permitir consultar as **versões anteriores** do termo, cada uma com o texto e o
período em que valeu, e SHALL apontar, a partir de cada decisão do histórico da autorização, o
**texto da versão que valia** naquela data. (`RF-13-33`)

#### Scenario: A versão de uma decisão antiga é alcançável

- **WHEN** o responsável abre uma decisão antiga no histórico da autorização
- **THEN** alcança o texto da versão do termo que valia naquela data, e não o da versão vigente

### Requirement: O termo apresentado declara a entrega de dados

A App 07 SHALL apresentar, no termo, a declaração de que os dados podem ser **entregues de
graça e anonimizados** a pesquisadores e gestores públicos, com aprovação caso a caso de um
Admin e sob licença que obriga a **creditar a comunidade**. A tela NEVER SHALL oferecer decisão
separada sobre essa entrega. (`RF-13-34`, `RN-13-19`)

#### Scenario: O responsável encontra a declaração no termo

- **WHEN** o responsável lê o termo vigente
- **THEN** encontra a declaração da entrega gratuita e anonimizada, com a aprovação do Admin e
  a obrigação de creditar a comunidade

### Requirement: O responsável registra a proposta e acompanha o retorno

A App 07 SHALL permitir ao responsável registrar **proposta de evolução da plataforma** em
texto, que entra na **fila única da gestão** — a mesma das sugestões do Guerreiro(a), do
Apoiador e do Mestre —, e SHALL apresentar o **status** de cada proposta até o retorno, com o
**motivo em linguagem simples** quando não adotada.

O retorno SHALL acontecer **dentro da plataforma**: a aplicação NEVER SHALL prometer aviso por
e-mail. A tela NEVER SHALL prometer ponto, badge ou recompensa pela proposta: a pontuação é da
criança. (`RF-13-39`, `RF-13-40`, `RN-13-15`, `RN-13-18`)

#### Scenario: A proposta entra na fila única

- **WHEN** o responsável registra uma proposta em texto
- **THEN** ela entra na fila única da gestão e passa a aparecer entre as propostas dele

#### Scenario: O retorno chega com o motivo em linguagem simples

- **WHEN** a gestão conclui a proposta como não adotada
- **THEN** o responsável vê o status e o motivo em linguagem simples, dentro da plataforma

#### Scenario: A tela não promete e-mail nem ponto

- **WHEN** o responsável registra a proposta
- **THEN** a tela não promete aviso por e-mail e não promete ponto, badge nem recompensa

### Requirement: Toda tela da App 07 que grava dado avisa o que ali se coleta

A App 07 SHALL exibir um **aviso discreto** do que está sendo coletado em toda tela em que grava
dado — a troca da senha provisória; a decisão da autorização; a recusa da imagem do onboarding;
a abertura de solicitação; o registro da proposta; e o ato assistido. Cada aviso SHALL nomear o
dado **daquela** tela e SHALL oferecer o acesso à **área detalhada**, que na App 07 é a tela de
transparência do vinculado.

O aviso NEVER SHALL bloquear a tela, NEVER SHALL exigir confirmação para continuar e NEVER
SHALL impedir o envio do formulário. (`RF-13-41`, PRD-13 §11, documento 03 §12)

#### Scenario: A tela da solicitação traz o aviso

- **WHEN** o responsável abre a abertura de solicitação
- **THEN** um aviso discreto informa o que aquela tela coleta e dá acesso à área detalhada

#### Scenario: O aviso nomeia o dado daquela tela

- **WHEN** o responsável abre a decisão da autorização e depois o registro da proposta
- **THEN** cada aviso nomeia o dado da sua própria tela, e não o da outra

#### Scenario: O aviso leva à transparência

- **WHEN** o responsável aciona o acesso à área detalhada a partir do aviso
- **THEN** chega à tela de transparência do vinculado

#### Scenario: O aviso não atrapalha o uso

- **WHEN** o aviso está exibido numa tela de decisão ou de formulário
- **THEN** o responsável envia o formulário sem confirmar o aviso, e nada fica bloqueado

### Requirement: A aplicação não abre canal com Apoiador nem com terceiro

A App 07 NEVER SHALL oferecer canal de contato, mensagem, comentário ou dado de contato de
**Apoiador**, de **terceiro** ou de **outro parente** da criança, em tela alguma — a área é
canal entre a família e a plataforma, e nada mais. Nem o histórico de acessos, nem a
transparência, nem a proposta SHALL expor endereço, telefone ou e-mail de quem quer que seja.
(`RF-13-42`, `RN-13-17`)

#### Scenario: Nenhum caminho de contato com terceiro

- **WHEN** o responsável percorre todas as telas da aplicação
- **THEN** não há campo de mensagem, canal de contato nem dado de contato de Apoiador, de
  terceiro ou de outro parente

### Requirement: A aplicação opera o ato assistido para quem não tem smartphone

A App 07 SHALL oferecer o **modo assistido**: um Admin ou um Mestre, com o responsável
**presente**, escolhe o Guerreiro(a), escolhe **qual dos responsáveis vinculados está
presente**, percorre com ele o texto do termo e registra a decisão da autorização única **em
nome dele**, informando **quem testemunhou**. A tela SHALL declarar, antes do registro, que o
ato é gravado em nome do responsável e tem a mesma força do que ele faria sozinho.

O modo assistido SHALL alcançar **apenas** a decisão da autorização única: NEVER SHALL abrir a
evolução, as solicitações, a transparência ou o histórico de acessos do vinculado, e NEVER SHALL
oferecer cadastro de responsável ou de vínculo. (`RF-13-35`, `RF-13-36`, `RF-13-38`,
`RN-13-16`, PRD-13 §5.8)

#### Scenario: O Mestre registra o ato em nome do responsável presente

- **WHEN** um Mestre abre o modo assistido, escolhe o vinculado e o responsável presente, e
  registra a concessão com a testemunha
- **THEN** o ato é gravado em nome do responsável, com quem operou e quem testemunhou

#### Scenario: O ato assistido aparece no histórico em nome do responsável

- **WHEN** o responsável abre depois o histórico da autorização do vinculado
- **THEN** a decisão aparece em nome dele, com a origem assistida, quem operou e quem
  testemunhou

#### Scenario: O modo assistido não abre os dados da criança

- **WHEN** o Admin ou o Mestre está no modo assistido
- **THEN** não alcança a evolução, as solicitações, a transparência nem o histórico de acessos
  do vinculado
