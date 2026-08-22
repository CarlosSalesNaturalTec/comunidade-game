## MODIFIED Requirements

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
