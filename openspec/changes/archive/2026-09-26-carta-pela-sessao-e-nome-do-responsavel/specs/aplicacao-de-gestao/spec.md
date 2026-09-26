# Spec Delta

## MODIFIED Requirements

### Requirement: O Admin inclui outro Admin e cadastra o responsável com o vínculo

A App 03 SHALL oferecer ao Admin a inclusão manual de outro Admin (`RF-02-05`) e o cadastro de
responsável com o **vínculo** a Guerreiros e Guerreiras já cadastrados, declarando o **grau de
parentesco** em texto livre (`RF-02-06`). A aplicação SHALL impedir o quarto vínculo de um
mesmo Guerreiro(a), respeitando o teto de três responsáveis, e SHALL oferecer a criação de
**credencial de usuário e senha provisória** para o adulto sem conta social (`RF-02-07`).
(`RN-02-02`, `RN-02-08`, invariante 3 do documento 99 §6)

O cadastro do responsável SHALL declarar o **nome** dele, e NEVER SHALL ser enviado sem o
nome: é sobre esse nome que se apoia o consentimento que autoriza a captura da imagem da
criança, e o núcleo o exige de toda aplicação que cadastra responsável. (`RF-02-06`,
`responsavel-e-vinculo`)

#### Scenario: Admin inclui outro Admin

- **WHEN** um Admin em sessão informa nome e e-mail de um novo Admin e confirma
- **THEN** o Admin novo passa a existir, sem nenhum caminho de autocadastro envolvido

#### Scenario: O responsável é cadastrado com o nome dele

- **WHEN** o Admin informa o nome do responsável e confirma o cadastro
- **THEN** o responsável passa a existir com o nome declarado, e o cadastro segue para o
  vínculo

#### Scenario: Cadastro sem nome não chega ao núcleo

- **WHEN** o Admin tenta cadastrar um responsável sem informar o nome
- **THEN** a aplicação pede o nome e não envia o cadastro

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
