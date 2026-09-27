# Spec Delta

## ADDED Requirements

### Requirement: O Mestre consulta os responsáveis que alcança e retoma o vínculo de um deles

A App 09 SHALL abrir a área **Responsáveis** apresentando os responsáveis que o núcleo serve
ao Mestre em sessão, cada um com o **nome** e com os Guerreiros e Guerreiras vinculados por
**nick** e **grau de parentesco**. A aplicação NEVER SHALL recortar a lista por conta própria:
o alcance do Mestre — as comunidades em que atua somadas aos responsáveis que ele próprio
cadastrou — é do núcleo. (`RF-09-122`, `RF-09-62`)

Responsável **sem vínculo** SHALL aparecer sinalizado como tal. É o cadastro interrompido no
encontro, e é o caso que mais alcança o Mestre, que cadastra presencialmente. (`RF-09-122`)

O **cadastro** de responsável SHALL continuar disponível, alcançável a partir da lista, e
NEVER SHALL ser o que a área apresenta primeiro. A aplicação SHALL oferecer, a partir de um
responsável da lista, **vincular outro Guerreiro(a)** a ele declarando o grau de parentesco,
sem exigir novo cadastro; o teto de três SHALL continuar explicado quando o núcleo o recusar.
(`RF-09-122`, `RF-09-62`, `RF-09-63`, `RN-09-15`)

A lista NEVER SHALL apresentar credencial, senha, usuário de acesso ou contato do responsável,
nem imagem real, nome civil ou nascimento do Guerreiro(a). A área SHALL exibir o aviso de
coleta que toda tela de dado pessoal da App 09 já exibe. (`RF-09-122`, `RN-09-18`, invariante
12 do documento 99 §6)

#### Scenario: A área abre na lista dos responsáveis que o Mestre alcança

- **WHEN** o Mestre abre a área Responsáveis
- **THEN** vê os responsáveis que o núcleo lhe serve, cada um com o nome e os vinculados por
  nick e grau de parentesco, e não é levado direto ao cadastro

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

#### Scenario: A lista não expõe credencial nem dado civil da criança

- **WHEN** o Mestre lê a lista
- **THEN** nenhuma linha traz credencial, senha, usuário ou contato do responsável, nem imagem
  real, nome civil ou nascimento de Guerreiro(a)
