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

#### Scenario: Visitante sem sessão

- **WHEN** alguém abre a App 07 sem sessão aberta
- **THEN** só a entrada é apresentada, e nenhuma tela de dado de criança

#### Scenario: A aplicação se identifica com a própria chave

- **WHEN** a App 07 chama uma rota de dados do núcleo
- **THEN** a chamada leva a chave da App 07, e não a de outra aplicação

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
