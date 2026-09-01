## ADDED Requirements

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
