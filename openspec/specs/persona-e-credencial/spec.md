## Purpose

A persona é quem age no núcleo: os cinco papéis do PRD-01 §4, o vínculo de comunidade que
prende o Guerreiro(a) a um território, e as credenciais que ligam uma pessoa real a esse
registro. Esta capacidade cobre quem pode existir, quem cria quem, e o caso de exceção do
adulto que não tem conta social — inclusive a única persona que não é criada por ninguém: a do
fundador, semeada na implantação.

## Requirements

### Requirement: A persona existe nos cinco papéis

O núcleo SHALL manter a persona nos cinco papéis do PRD-01 §4 — Admin, Mestre, Guerreiro(a),
Responsável e Apoiador. Toda persona SHALL carregar o papel que exerce, e o papel SHALL ser o
que determina o que ela escreve e o que ela lê. (`RF-01-19`)

Vínculo de responsável e consentimento, que `RF-01-19` também nomeia, são da fatia seguinte:
esta cobre a persona.

#### Scenario: Persona carrega o papel que exerce

- **WHEN** uma persona é criada no núcleo, por qualquer caminho
- **THEN** o registro dela declara qual dos cinco papéis ela exerce

#### Scenario: Papel ausente não produz persona

- **WHEN** uma criação de persona chega sem papel declarado
- **THEN** o núcleo recusa a criação e nenhuma persona passa a existir

### Requirement: Só o Guerreiro(a) tem autocadastro

O núcleo SHALL aceitar autocadastro apenas do Guerreiro(a). Mestre e Apoiador SHALL ser
cadastrados por Admin; o responsável, por Admin ou Mestre; e Admin novo SHALL entrar apenas por
inclusão de outro Admin. Login NEVER SHALL criar persona. (`RN-01-01`, `RN-01-02`, `RN-01-04`)

#### Scenario: Adulto não se autocadastra

- **WHEN** uma criação de persona de Mestre, Apoiador ou responsável chega sem a autoria de um
  Admin — ou de um Mestre, no caso do responsável
- **THEN** o núcleo recusa a criação

#### Scenario: Admin novo exige Admin existente

- **WHEN** uma criação de persona de Admin chega sem a autoria de outro Admin
- **THEN** o núcleo recusa a criação, ressalvada a semeadura da implantação

### Requirement: Guerreiro(a) tem vínculo obrigatório a exatamente uma comunidade

O núcleo SHALL exigir que toda persona de Guerreiro(a) tenha vínculo a **exatamente uma**
Comunidade Virtual. A persona de Guerreiro(a) NEVER SHALL existir sem comunidade nem com mais de
uma vigente. (`RN-01-05`)

O vínculo NEVER SHALL ser atributo da persona: ele vive na entidade própria da capacidade
`comunidade-virtual`, com data de início, data de fim e histórico, e a comunidade vem da
**aula agendada** em que o Guerreiro(a) se cadastra, nunca de quem o cadastra (`RF-08-02`,
`RN-08-02`).

O comportamento da Comunidade Virtual — criação, hierarquia de locais, transferência — é do
PRD-08 (`RF-01-23`).

#### Scenario: Guerreiro(a) sem comunidade não é criado

- **WHEN** uma criação de persona de Guerreiro(a) chega sem comunidade
- **THEN** o núcleo recusa a criação

#### Scenario: Segundo vínculo vigente é recusado

- **WHEN** um segundo vínculo de comunidade vigente é pedido para o mesmo Guerreiro(a)
- **THEN** o núcleo recusa, e o vínculo existente permanece

#### Scenario: A comunidade do Guerreiro(a) continua consultável pelo vínculo vigente

- **WHEN** se consulta a comunidade de um Guerreiro(a) já cadastrado
- **THEN** o núcleo a resolve pelo vínculo vigente, e o resultado é o mesmo de antes da
  mudança

### Requirement: A implantação semeia a persona Admin do fundador

O núcleo SHALL criar, na implantação, a persona Admin do fundador, a partir da identidade social
declarada no ambiente. Essa SHALL ser a única persona criada sem a autoria de outro Admin, e a
semeadura NEVER SHALL criar uma segunda persona de qualquer outro papel. (`RF-01-61`,
documento 02 §1)

#### Scenario: A implantação cria o Admin fundador

- **WHEN** a implantação de um ambiente é executada com a identidade social do fundador
  declarada
- **THEN** existe naquele ambiente uma persona Admin vinculada àquela identidade social

#### Scenario: Semear duas vezes não duplica a persona

- **WHEN** a implantação do mesmo ambiente é executada de novo
- **THEN** a persona Admin do fundador permanece a mesma, sem duplicata

#### Scenario: Sem identidade declarada não há semeadura

- **WHEN** a implantação é executada sem a identidade social do fundador declarada
- **THEN** o núcleo não cria persona alguma e a implantação falha de forma visível

#### Scenario: O Admin semeado entra pelo caminho comum

- **WHEN** o fundador autentica por login social com a identidade que foi semeada
- **THEN** o núcleo abre a sessão dele como abriria a de qualquer adulto com cadastro existente

### Requirement: Admin ou Mestre cria credencial de usuário e senha provisória

O núcleo SHALL permitir que Admin ou Mestre crie, para adulto sem conta social, uma credencial
de **usuário e senha provisória**, com o mesmo vínculo e as mesmas permissões que a persona já
tem. O usuário NOT SHALL precisar ser um e-mail. A senha SHALL ser guardada com hash, SHALL
valer para um único acesso e SHALL ser trocada pelo próprio adulto. (`RF-01-11`, `RN-01-18`)

#### Scenario: Credencial provisória nasce marcada para troca

- **WHEN** um Admin ou um Mestre cria a credencial de usuário e senha provisória de um adulto
- **THEN** a credencial nasce com a troca de senha pendente, e a senha é guardada apenas como
  hash

#### Scenario: Credencial não amplia o que a persona pode

- **WHEN** um adulto passa a ter credencial de usuário e senha além do vínculo que já tinha
- **THEN** o que ele escreve e lê continua sendo o do papel da persona, sem acréscimo

#### Scenario: Quem não é Admin nem Mestre não cria credencial

- **WHEN** uma persona de outro papel tenta criar credencial de usuário e senha
- **THEN** o núcleo responde 403 e nenhuma credencial é criada

#### Scenario: A senha em claro não é recuperável

- **WHEN** a credencial provisória já foi criada
- **THEN** nenhuma rota, consulta ou registro operacional devolve a senha em claro

### Requirement: O Guerreiro(a) tem nick, único em toda a plataforma

O núcleo SHALL exigir **nick** em toda persona de Guerreiro(a), e o nick SHALL ser único em toda
a plataforma — não apenas dentro da comunidade. A unicidade SHALL alcançar o nick de qualquer
persona que o tenha — Guerreiro(a), **Apoiador e Mestre** —, de modo que dois nicks de
personas diferentes NEVER SHALL coincidir, seja qual for o papel de cada uma.
Persona de Guerreiro(a) NEVER SHALL existir sem nick: é por ele que a criança entra e é por ele
que a família acompanha.

Persona de **adulto** — Apoiador e Mestre — SHALL poder existir **sem nick**, e SHALL poder
recebê-lo depois: o Apoiador o traz do pré-cadastro e o Mestre o define no primeiro acesso, e
nenhum dos dois caminhos pode travar o cadastro que um Admin já aprovou. (`RF-01-19`,
`RN-01-22`, `RN-01-30`, `RF-14-12`, `RN-14-10`, documento 02 §1)

A rota que cria o Guerreiro(a) e a conferência de unicidade durante a conversa de cadastro são do
PRD-04; a rota pela qual o adulto define o próprio nick é da capacidade `identidade-do-adulto`;
aqui nascem o atributo e a invariante que qualquer rota que venha a gravá-lo respeita.

#### Scenario: Guerreiro(a) sem nick não é criado

- **WHEN** uma criação de persona de Guerreiro(a) chega sem nick
- **THEN** o núcleo recusa a criação e nenhuma persona passa a existir

#### Scenario: Nick repetido é recusado

- **WHEN** uma criação de persona chega com nick já usado por outra persona, de qualquer papel
- **THEN** o núcleo recusa a criação, e a persona que já tinha o nick permanece intacta

#### Scenario: Apoiador é criado sem nick

- **WHEN** uma criação de persona de Apoiador chega sem nick
- **THEN** o núcleo cria a persona sem nick, e ela existe à espera de recebê-lo

#### Scenario: Mestre é criado sem nick

- **WHEN** uma criação de persona de Mestre chega sem nick
- **THEN** o núcleo cria a persona sem nick, e ela existe à espera de recebê-lo

#### Scenario: Nick de Mestre colide com nick de Guerreiro(a)

- **WHEN** chega um nick de Mestre já usado por um Guerreiro(a)
- **THEN** o núcleo recusa a gravação, porque a unicidade alcança os dois papéis

#### Scenario: Nick de Mestre colide com nick de Apoiador

- **WHEN** chega um nick de Mestre já usado por um Apoiador
- **THEN** o núcleo recusa a gravação, porque a unicidade alcança qualquer persona que tenha
  nick

### Requirement: O Guerreiro(a) tem avatar, e é por ele que aparece em público

O núcleo SHALL guardar, em toda persona de Guerreiro(a), as **características do avatar** — a
representação pública dele, ao lado do nick. O avatar SHALL ser o **único** retrato do
Guerreiro(a) em qualquer superfície pública: a imagem do onboarding NEVER SHALL virar avatar,
nem ser exibida em lugar algum.

O núcleo SHALL guardar **avatar** também nas personas de **Apoiador e Mestre**, onde ele é
opcional como o nick. O avatar próprio do Apoiador SHALL obedecer ao piso de moedas de
`RN-14-11`; o avatar do Mestre NÃO SHALL ter piso, porque o piso é regra de marca do Apoiador.
(`RN-01-10`, `RN-01-15`, `RN-14-10`, `RN-14-11`, invariante 12 do documento 99 §6, documentos
02 §1 e 11 §8.2)

A rota que grava o avatar no cadastro é do PRD-04 (`RF-04-07`), a que permite ao Guerreiro(a)
alterá-lo é do PRD-05 (`RF-05-51`) e a que permite ao Mestre alterá-lo é do PRD-09; aqui nascem
o atributo e a invariante que qualquer rota que venha a gravá-lo respeita — a mesma divisão já
aplicada ao nick.

#### Scenario: A persona de Guerreiro(a) carrega o avatar

- **WHEN** uma persona de Guerreiro(a) existe no núcleo
- **THEN** ela carrega as características do avatar dela

#### Scenario: A imagem do onboarding não vira avatar

- **WHEN** o _template_ biométrico de um Guerreiro(a) é gravado
- **THEN** nenhum avatar é derivado dele, e a imagem continua sem ser exibida em lugar algum

#### Scenario: O avatar é o que a superfície pública exibe

- **WHEN** uma superfície pública precisa retratar um Guerreiro(a)
- **THEN** ela usa o avatar e o nick, e nenhum outro retrato existe para ela usar

#### Scenario: A persona de Mestre carrega avatar

- **WHEN** uma persona de Mestre existe no núcleo
- **THEN** ela pode carregar avatar, sem piso de moedas para tê-lo

### Requirement: O núcleo nunca descobre nem sugere um nick

O núcleo SHALL responder a busca por nick **apenas por correspondência exata**. O núcleo NEVER
SHALL expor listagem de nicks, busca parcial, ordenação por semelhança, contagem de resultados
ou sugestão de variação que **alcance nick de Guerreiro(a)** — a vedação é definida pelo que a
resposta alcança, não por quem pergunta, e por isso vale igualmente para persona autenticada
como adulto e para visitante sem sessão. A recusa por nick inexistente NEVER SHALL ser
distinguível da recusa por outro motivo. (`RN-01-22`, `RN-14-23`, invariante 12 do documento
99 §6)

A conferência de disponibilidade restrita a **nicks de adulto**, da capacidade
`identidade-do-adulto`, é a única exceção declarada, e ela existe precisamente porque não
alcança nick de Guerreiro(a).

A consulta pública por nick exato (`RF-01-33`) e a ausência de busca parcial na vitrine
(`RF-01-34`) são de outra fatia; esta grava a invariante que aquelas rotas herdam.

#### Scenario: Busca por nick é exata

- **WHEN** o núcleo procura uma persona por nick, em qualquer caminho interno ou de rota
- **THEN** a correspondência é exata, e nick parcial não alcança persona alguma

#### Scenario: Não existe rota que liste ou sugira nick

- **WHEN** se procura no núcleo uma rota que liste nicks de Guerreiro(a), complete um nick
  parcial de Guerreiro(a) ou sugira variações a partir dele
- **THEN** nenhuma existe

#### Scenario: Adulto autenticado não descobre nick de Guerreiro(a)

- **WHEN** uma persona autenticada como adulto consulta um nick que não é de adulto
- **THEN** a resposta não distingue nick inexistente de nick de Guerreiro(a)
