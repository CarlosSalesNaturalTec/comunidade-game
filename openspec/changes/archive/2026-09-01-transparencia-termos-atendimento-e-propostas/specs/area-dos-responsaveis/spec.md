## ADDED Requirements

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

## MODIFIED Requirements

### Requirement: A Área dos responsáveis é inteiramente autenticada e se identifica por chave

A App 07 SHALL apresentar a entrada a quem não tem sessão aberta, e NEVER SHALL servir tela de
dado de criança sem sessão de responsável. Toda chamada ao núcleo SHALL levar a **chave da
própria aplicação** e, havendo sessão, a credencial da persona.

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
