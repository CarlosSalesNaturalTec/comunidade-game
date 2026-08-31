## ADDED Requirements

### Requirement: O Guerreiro(a) lê os próprios desafios em aberto

O núcleo SHALL servir, em `GET /v1/eu/desafios`, as **atividades em aberto** do Guerreiro(a)
**em sessão**: as das missões que ele já **desbloqueou**, nas trilhas em que está **inscrito**,
e para as quais o Mestre ainda **não lançou Resultado** para ele. Cada atividade SHALL trazer
**modalidade** e **formato**, além do título, da descrição, da produção esperada e da missão e
trilha a que pertence.

A leitura SHALL alcançar apenas o Guerreiro(a) da sessão, identificado pelo contexto e nunca
por identificador vindo do cliente, e NEVER SHALL devolver atividade de trilha em que ele não
está inscrito, de missão que ele ainda não desbloqueou nem atividade cujo Resultado já foi
lançado para ele. Guerreiro(a) sem nada em aberto SHALL receber **200** com conjunto vazio,
nunca erro. Persona que não é Guerreiro(a) SHALL receber **403**. (`RF-05-19`, `RN-05-21`,
`RN-05-06`)

#### Scenario: As atividades das missões desbloqueadas são devolvidas

- **WHEN** um Guerreiro(a) em sessão consulta os próprios desafios e tem missões desbloqueadas
  com atividades sem Resultado lançado
- **THEN** o núcleo devolve essas atividades, cada uma com modalidade e formato

#### Scenario: Atividade de missão ainda bloqueada não aparece

- **WHEN** existe atividade numa missão que o Guerreiro(a) ainda não desbloqueou
- **THEN** essa atividade não entra na leitura

#### Scenario: Atividade já lançada pelo Mestre sai da lista

- **WHEN** o Mestre lança o Resultado do Guerreiro(a) numa atividade que estava em aberto
- **THEN** a leitura seguinte não a devolve mais

#### Scenario: Atividade de trilha em que não se inscreveu não aparece

- **WHEN** existe atividade em trilha na qual o Guerreiro(a) não está inscrito
- **THEN** essa atividade não entra na leitura

#### Scenario: Sem nada em aberto a resposta é conjunto vazio

- **WHEN** o Guerreiro(a) em sessão não tem nenhuma atividade em aberto
- **THEN** o núcleo responde 200 com conjunto vazio, nunca erro

#### Scenario: Persona que não é Guerreiro(a) não lê

- **WHEN** um Mestre, Admin, Apoiador ou responsável em sessão consulta a rota
- **THEN** o núcleo responde 403 e nada é devolvido

### Requirement: A App 05 mostra os desafios em aberto, com modalidade e formato

A App 05 SHALL apresentar ao Guerreiro(a) os **desafios em aberto** dele, cada um com a
**modalidade** — individual, em equipe ou em equipe com familiar — e o **formato** —
presencial ou on-line —, em linguagem da criança, junto do que se espera que ele produza e da
missão e trilha a que o desafio pertence. Guerreiro(a) sem desafio em aberto SHALL ver uma
mensagem que diz isso, e NEVER SHALL receber lista vazia sem explicação.

A tela NEVER SHALL oferecer lançar resultado, presença ou mérito, e NEVER SHALL apresentar o
desafio como comprável ou trocável. (`RF-05-19`, `RN-05-06`)

#### Scenario: Cada desafio diz a modalidade e o formato

- **WHEN** o Guerreiro(a) abre o bloco dos desafios com atividades em aberto
- **THEN** vê cada desafio com a modalidade e o formato dele, e o que precisa produzir

#### Scenario: Sem desafio em aberto a tela explica

- **WHEN** o Guerreiro(a) não tem nenhum desafio em aberto
- **THEN** a tela diz isso em linguagem simples, sem lista vazia muda

#### Scenario: Nenhuma tela do bloco lança resultado

- **WHEN** o Guerreiro(a) percorre o bloco dos desafios
- **THEN** nenhuma ação de lançar resultado, presença ou mérito é oferecida

### Requirement: A App 05 mostra as equipes de que o Guerreiro(a) participa

A App 05 SHALL apresentar ao Guerreiro(a) as **equipes de que ele participa** — as da aula e as
da trilha —, o **papel** dele em cada uma e as **atividades** de cada equipe. Cada colega SHALL
aparecer **apenas por avatar e nick**, e a tela NEVER SHALL exibir imagem real, nome civil,
data de nascimento nem qualquer outro dado pessoal de outra criança.

Guerreiro(a) que não integra nenhuma equipe SHALL ver uma mensagem que diz isso e onde a equipe
se forma. (`RF-05-22`, `RF-05-23`, `RN-05-15`, `RN-05-21`)

#### Scenario: As equipes vêm com papel e atividades

- **WHEN** o Guerreiro(a) abre o bloco das equipes e integra equipes de aula e de trilha
- **THEN** vê cada equipe, o papel dele nela e as atividades daquela equipe

#### Scenario: Colega aparece só por avatar e nick

- **WHEN** a tela exibe os integrantes de uma equipe
- **THEN** cada integrante aparece por avatar e nick, e nenhum dado pessoal é exibido

#### Scenario: Sem equipe a tela explica onde ela se forma

- **WHEN** o Guerreiro(a) não integra nenhuma equipe
- **THEN** a tela diz isso e informa que a equipe se forma no encontro, no App 01

### Requirement: A App 05 não forma nem edita equipe e não tem canal de conversa

A App 05 NEVER SHALL oferecer **formar, editar, entrar em, sair de nem homologar** equipe: a
formação acontece no App 01, a cada aula, e a homologação da equipe da trilha é do Mestre. A
tela de equipes SHALL dizer, em linguagem simples, onde a equipe se forma.

Nenhuma tela desta aplicação SHALL oferecer **canal de conversa** entre pessoas — nem mensagem
a colega, nem comentário em equipe, nem contato com Mestre, responsável ou Apoiador.
(`RF-05-24`, `RN-05-12`, `RN-05-22`)

#### Scenario: Nenhuma ação de formar ou editar equipe é oferecida

- **WHEN** o Guerreiro(a) percorre o bloco das equipes
- **THEN** nenhuma ação de criar, editar, entrar, sair ou homologar equipe aparece

#### Scenario: A tela diz onde a equipe se forma

- **WHEN** o Guerreiro(a) abre o bloco das equipes
- **THEN** a tela informa que a formação acontece no encontro, no App 01

#### Scenario: Nenhum canal de conversa em nenhuma tela

- **WHEN** o Guerreiro(a) percorre os blocos dos desafios e das equipes
- **THEN** nenhuma caixa de mensagem, comentário ou contato entre pessoas é oferecida
