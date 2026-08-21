## ADDED Requirements

### Requirement: O Admin cadastra e edita o Guerreiro(a) pela aplicação

A App 03 SHALL oferecer ao Admin o cadastro de Guerreiro(a) com nome, data de nascimento, nick
e características do avatar, e a edição do que já foi cadastrado. A aplicação SHALL apontar o
campo em falta antes de chamar o núcleo e SHALL apresentar em linguagem simples a recusa por
nick em uso, **sem dizer de quem é o nick**. A aplicação NEVER SHALL exibir a imagem do
Guerreiro(a): a representação é o avatar. (`RF-02-01`, `RN-02-22`, invariante 12 do documento
99 §6, PRD-02 §11)

#### Scenario: Admin cadastra o Guerreiro(a)

- **WHEN** um Admin em sessão informa nome, nascimento, nick e avatar e confirma
- **THEN** o Guerreiro(a) passa a existir e a aplicação o apresenta entre os cadastrados

#### Scenario: Nick em uso é explicado sem revelar o dono

- **WHEN** o núcleo recusa o cadastro porque o nick já está em uso
- **THEN** a aplicação pede outro nick, sem informar quem o usa nem de que papel

#### Scenario: A gestão não vê a imagem da criança

- **WHEN** um Admin abre o cadastro de um Guerreiro(a)
- **THEN** a tela mostra avatar e nick, e nenhuma imagem real aparece

### Requirement: O Admin cadastra Mestre e Apoiador declarando os artefatos

A App 03 SHALL oferecer ao Admin o cadastro de Mestre e de Apoiador com nome, e-mail, WhatsApp
opcional e os artefatos comprobatórios, cada um com endereço e rótulo. A aplicação SHALL
impedir a confirmação sem ao menos um artefato e SHALL explicar por quê. A tela NEVER SHALL
oferecer anexo de arquivo como artefato, nem exigir nick. (`RF-02-02`, `RF-02-03`, `RF-02-04`,
`RN-02-01`, documento 02 §1)

#### Scenario: Admin cadastra Mestre com um link

- **WHEN** um Admin informa nome, e-mail e um link de currículo com rótulo e confirma
- **THEN** o Mestre passa a existir e a aplicação o apresenta entre os cadastrados

#### Scenario: Sem artefato a aplicação não deixa confirmar

- **WHEN** o Admin tenta confirmar o cadastro de um Apoiador sem artefato algum
- **THEN** a aplicação explica que ao menos um é obrigatório e nada é enviado ao núcleo

#### Scenario: A tela de adulto não pede nick ao Admin

- **WHEN** um Admin abre o cadastro de Mestre
- **THEN** a tela não exige nick, porque o Mestre o define no primeiro acesso

### Requirement: A aplicação oferece ao Admin gravar o nick do adulto na colisão

A App 03 SHALL oferecer ao Admin, na ficha de um Mestre ou de um Apoiador, o caminho de gravar
ou trocar o nick daquela persona, e SHALL sinalizar na lista quem está **sem nick**. A
aplicação SHALL apresentar em linguagem simples que o adulto sem nick não aparece em superfície
pública, e NEVER SHALL sugerir ao Admin um nick nem revelar de quem é o nick recusado.
(`RF-02-01`, `RN-01-30`, `RN-14-10`)

#### Scenario: Adulto sem nick é sinalizado na lista

- **WHEN** um Admin abre a lista de Mestres e Apoiadores
- **THEN** quem está sem nick aparece sinalizado, com o caminho de gravá-lo

#### Scenario: Admin grava o nick que recebeu por fora

- **WHEN** o Admin grava um nick disponível na ficha de um Apoiador sem nick
- **THEN** o nick passa a valer e a sinalização de ausência some

#### Scenario: A aplicação não sugere nick ao Admin

- **WHEN** o Admin abre o caminho de gravar nick
- **THEN** a tela não oferece sugestão alguma, e o nick é o que a pessoa lhe passou

### Requirement: O Admin inclui outro Admin e cadastra o responsável com o vínculo

A App 03 SHALL oferecer ao Admin a inclusão manual de outro Admin (`RF-02-05`) e o cadastro de
responsável com o **vínculo** a Guerreiros e Guerreiras já cadastrados, declarando o **grau de
parentesco** em texto livre (`RF-02-06`). A aplicação SHALL impedir o quarto vínculo de um
mesmo Guerreiro(a), respeitando o teto de três responsáveis, e SHALL oferecer a criação de
**credencial de usuário e senha provisória** para o adulto sem conta social (`RF-02-07`).
(`RN-02-02`, `RN-02-08`, invariante 3 do documento 99 §6)

#### Scenario: Admin inclui outro Admin

- **WHEN** um Admin em sessão informa nome e e-mail de um novo Admin e confirma
- **THEN** o Admin novo passa a existir, sem nenhum caminho de autocadastro envolvido

#### Scenario: Responsável é vinculado com grau de parentesco

- **WHEN** o Admin cadastra um responsável e o vincula a um Guerreiro(a) declarando o
  parentesco
- **THEN** o vínculo passa a existir com o parentesco declarado

#### Scenario: Quarto responsável é barrado

- **WHEN** o Admin tenta vincular um quarto responsável ao mesmo Guerreiro(a)
- **THEN** a aplicação explica o teto de três e o vínculo não é criado

#### Scenario: Adulto sem conta social recebe senha provisória

- **WHEN** o Admin cria credencial de usuário e senha provisória para um adulto cadastrado
- **THEN** a aplicação exibe a senha provisória uma vez, para entrega, e não a recupera depois
