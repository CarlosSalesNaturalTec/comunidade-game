## MODIFIED Requirements

### Requirement: O Mestre cadastra o responsável que se apresentou no encontro

A App 09 SHALL oferecer ao Mestre em sessão o cadastro da persona de **responsável**, com o
**nome** dela. A tela SHALL declarar que o cadastro pressupõe que o responsável **se apresentou
pessoalmente**, e a aplicação NEVER SHALL oferecer caminho de cadastro à distância — solicitação,
convite ou autocadastro do responsável. A tela NEVER SHALL exigir e-mail, documento ou
digitalização do termo: documento e termo são atos da gestão, na App 03. O **e-mail** SHALL ser
oferecido como campo **opcional**, declarado como o da conta Google com que o responsável
entrará na App 07; e-mail já usado por outra pessoa SHALL ser recusado em linguagem simples, no
campo. (`RF-09-147`, `RF-01-92`, decisão do fundador de 2026-11-27) O responsável SHALL ser a **única**
persona que a App 09 cadastra. (`RF-09-62`, `RN-09-15`, invariante 3 do documento 99 §6)

#### Scenario: O Mestre cadastra o responsável

- **WHEN** o Mestre informa o nome do responsável apresentado no encontro e confirma
- **THEN** a aplicação cadastra a persona de responsável e segue para o vínculo

#### Scenario: O Mestre cadastra o responsável com o e-mail da conta Google

- **WHEN** o Mestre informa nome e e-mail do responsável e confirma
- **THEN** o responsável passa a existir com o e-mail, e pode entrar na App 07 pela conta
  Google desse e-mail

#### Scenario: O e-mail não é exigido

- **WHEN** o Mestre confirma o cadastro só com o nome
- **THEN** o responsável é cadastrado sem e-mail, e o cadastro segue para o vínculo

#### Scenario: A tela declara a apresentação presencial

- **WHEN** o Mestre abre o cadastro de responsável
- **THEN** a tela declara que o cadastro pressupõe a apresentação pessoal do responsável

#### Scenario: Cadastro sem nome é recusado em linguagem simples

- **WHEN** o Mestre confirma o cadastro sem informar o nome
- **THEN** a aplicação aponta o campo em falta, em linguagem simples, e nada é cadastrado

#### Scenario: A App 09 não cadastra outra persona

- **WHEN** o Mestre percorre a área de responsáveis
- **THEN** não lhe é oferecido cadastrar Guerreiro(a), Mestre, Apoiador nem Admin

### Requirement: O Mestre consulta os responsáveis que alcança e retoma o vínculo de um deles

A App 09 SHALL abrir a área **Responsáveis** apresentando os responsáveis que o núcleo serve
ao Mestre em sessão, cada um com o **nome** e com os Guerreiros e Guerreiras vinculados por
**nick**, **nome** e **grau de parentesco**. Vinculado sem nick ou sem nome SHALL ter a
ausência sinalizada, sem sumir da linha. A aplicação NEVER SHALL recortar a lista por conta
própria: o alcance do Mestre — as comunidades em que atua somadas aos responsáveis que ele
próprio cadastrou — é do núcleo. (`RF-09-122`, `RF-09-62`, decisão de exibição do fundador de
2026-11-26)

Responsável **sem vínculo** SHALL aparecer sinalizado como tal. É o cadastro interrompido no
encontro, e é o caso que mais alcança o Mestre, que cadastra presencialmente. (`RF-09-122`)

O **cadastro** de responsável SHALL continuar disponível, alcançável a partir da lista, e
NEVER SHALL ser o que a área apresenta primeiro. A aplicação SHALL oferecer, a partir de um
responsável da lista, **vincular outro Guerreiro(a)** a ele declarando o grau de parentesco,
sem exigir novo cadastro; o teto de três SHALL continuar explicado quando o núcleo o recusar.
(`RF-09-122`, `RF-09-62`, `RF-09-63`, `RN-09-15`)

Cada linha SHALL apresentar o **acesso** do responsável: o e-mail do login social e o usuário
da credencial de usuário e senha, quando existem, e a indicação de **sem acesso** quando nenhum
dos dois existe. A lista NEVER SHALL apresentar senha, nem imagem real, nascimento ou contato
do Guerreiro(a). A App 09 NEVER SHALL oferecer a edição da ficha, que é do Admin.
(`RF-09-122`, `RF-01-92`, decisão do fundador de 2026-11-27) A área SHALL exibir o aviso de coleta
que toda tela de dado pessoal da App 09 já exibe. (`RF-09-122`, `RN-09-18`, invariante 12 do
documento 99 §6)

#### Scenario: A área abre na lista dos responsáveis que o Mestre alcança

- **WHEN** o Mestre abre a área Responsáveis
- **THEN** vê os responsáveis que o núcleo lhe serve, cada um com o nome e os vinculados por
  nick, nome e grau de parentesco, e não é levado direto ao cadastro

#### Scenario: Cadastro interrompido no encontro aparece sinalizado

- **WHEN** o Mestre cadastrou um responsável e saiu antes de criar qualquer vínculo
- **THEN** aquele responsável aparece na lista, marcado como sem Guerreiro(a) vinculado

#### Scenario: O cadastro continua alcançável a partir da lista

- **WHEN** o Mestre precisa cadastrar um responsável novo
- **THEN** alcança o cadastro a partir da lista, e ao concluir volta à lista com o que criou

#### Scenario: O Mestre retoma um responsável e vincula outro Guerreiro(a)

- **WHEN** o Mestre escolhe um responsável da lista e vincula um Guerreiro(a) declarando o grau
  de parentesco
- **THEN** o vínculo é criado para aquele responsável, e nenhum responsável novo é cadastrado

#### Scenario: O teto de três continua explicado na retomada

- **WHEN** o Mestre retoma um responsável e tenta vinculá-lo a um Guerreiro(a) que já tem três
  responsáveis vigentes
- **THEN** a aplicação explica o teto de três e o vínculo não é criado

#### Scenario: Lista vazia é dita, não some

- **WHEN** o Mestre não alcança responsável algum
- **THEN** a área diz que não há responsável e continua oferecendo cadastrar um

#### Scenario: A linha mostra como o responsável entra

- **WHEN** o Mestre lê a lista e um responsável tem e-mail e usuário de acesso
- **THEN** a linha dele apresenta o e-mail e o usuário

#### Scenario: Responsável sem acesso é sinalizado

- **WHEN** um responsável não tem e-mail nem usuário de acesso
- **THEN** a linha dele o marca como sem acesso

#### Scenario: A lista não expõe credencial nem dado civil da criança

- **WHEN** o Mestre lê a lista
- **THEN** nenhuma linha traz senha, nem imagem real, nascimento ou contato de Guerreiro(a), e
  não há ação de editar a ficha
