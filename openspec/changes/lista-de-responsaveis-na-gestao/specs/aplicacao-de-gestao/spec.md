# Spec Delta

## ADDED Requirements

### Requirement: A gestão apresenta os responsáveis cadastrados e retoma o vínculo de um deles

A App 03 SHALL apresentar, na sub-área **Responsáveis**, os responsáveis já cadastrados que o
núcleo lhe serve, cada um com o **nome** e com os Guerreiros e Guerreiras vinculados por
**nick** e **grau de parentesco**. Responsável **sem vínculo** SHALL aparecer na lista,
sinalizado como tal — é o cadastro interrompido, e é o que a lista existe para revelar.
(`RF-02-111`)

A aplicação SHALL oferecer, a partir de um responsável da lista, **vincular outro
Guerreiro(a)** a ele, declarando o grau de parentesco, sem exigir novo cadastro. O teto de
três responsáveis por Guerreiro(a) SHALL continuar a ser explicado quando o núcleo o recusar.
(`RF-02-111`, `RF-02-06`, `RN-02-08`, invariante 3 do documento 99 §6)

A lista NEVER SHALL apresentar credencial, senha, usuário de acesso ou contato do responsável,
nem imagem real, nome civil ou nascimento do Guerreiro(a). A tela SHALL exibir o aviso de
coleta que toda tela de dado pessoal da gestão já exibe. (`RF-02-111`, `RF-02-64`, `RN-02-23`)

#### Scenario: A sub-área Responsáveis apresenta quem já está cadastrado

- **WHEN** o Admin abre a sub-área Responsáveis
- **THEN** vê os responsáveis cadastrados, cada um com o nome e com os vinculados por nick e
  grau de parentesco

#### Scenario: Cadastro interrompido aparece sinalizado

- **WHEN** existe responsável cadastrado sem nenhum vínculo
- **THEN** ele aparece na lista, marcado como sem Guerreiro(a) vinculado

#### Scenario: O Admin retoma um responsável e vincula outro Guerreiro(a)

- **WHEN** o Admin escolhe um responsável da lista e vincula um Guerreiro(a) declarando o
  grau de parentesco
- **THEN** o vínculo é criado e passa a constar entre os vinculados daquele responsável, sem
  que um novo responsável tenha sido cadastrado

#### Scenario: O teto de três continua explicado na retomada

- **WHEN** o Admin retoma um responsável e tenta vinculá-lo a um Guerreiro(a) que já tem três
  responsáveis vigentes
- **THEN** a aplicação explica o teto de três e o vínculo não é criado

#### Scenario: Lista vazia é dita, não some

- **WHEN** nenhum responsável foi cadastrado ainda
- **THEN** a tela diz que não há cadastro e continua oferecendo cadastrar um

#### Scenario: A lista não expõe credencial nem dado civil da criança

- **WHEN** o Admin lê a lista
- **THEN** nenhuma linha traz credencial, senha, usuário ou contato do responsável, nem
  imagem real, nome civil ou nascimento de Guerreiro(a)
