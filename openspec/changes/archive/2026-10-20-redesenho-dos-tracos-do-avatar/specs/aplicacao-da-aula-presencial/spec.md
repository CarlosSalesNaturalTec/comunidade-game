# Spec Delta

## MODIFIED Requirements

### Requirement: O caminho do onboarding cadastra o Guerreiro(a) no encontro

A App 01 SHALL oferecer, na tela inicial, o caminho do **onboarding** em estado operante, e por
ele SHALL conduzir o cadastro do Guerreiro(a) coletando **nome**, **nick**, **forma de
tratamento**, **data de nascimento** e **características do avatar**. A aplicação NEVER SHALL
perguntar a comunidade: ela vem da aula vigente adotada na sessão de trabalho. O cadastro SHALL
ser feito **na presença** de Mestre ou Admin, cuja sessão de trabalho autentica a escrita sem
tornar-se autora dela. (`RF-04-01`, `RF-04-07`, `RF-04-10`, `RN-04-02`, `RN-04-04`, PRD-04 §12,
documento 99 §6 invariante 3)

Nesta fatia o cadastro é **formulário guiado**, não conversa conduzida por modelo de IA: a
condução por áudio e chat é de fatia posterior, e até lá a ordem dos campos é a da tela.

O campo das **características do avatar** SHALL ser a composição do avatar no **catálogo fechado**
da camada comum, nas nove camadas do documento 15 §7.1, e NEVER SHALL ser texto livre: o traço
ditado em palavras não se desenha depois. A **forma de tratamento** SHALL continuar campo próprio,
separado do avatar, porque nenhum item do catálogo carrega marca de gênero. O que a aplicação grava
no campo `avatar` SHALL ser o **objeto versionado** do documento 15 §7.2. (`RF-04-07`, documento 15
§7)

A composição de partida da montagem SHALL abrir com a **cor do fundo diferente da cor da roupa**,
para que o primeiro avatar que a criança vê tenha corpo. A escolha continua inteira dela: trocar
depois para as duas cores iguais SHALL ser permitido. A composição de partida é da tela, e NEVER
SHALL alterar o padrão de camada do catálogo nem o avatar padrão do projeto do documento 15 §7.3.
(`RF-04-06`, `RF-04-07`, documento 15 §7)

A composição SHALL acontecer **no próprio aparelho, sem rede**, e NEVER SHALL depender de requisição
ao núcleo nem a terceiro para desenhar o avatar. (documento 15 §7, princípio 6)

#### Scenario: O caminho do onboarding está alcançável

- **WHEN** a sessão de trabalho do aparelho está aberta e a tela inicial é apresentada
- **THEN** o caminho do onboarding é alcançável e conduz ao cadastro do Guerreiro(a)

#### Scenario: O cadastro coleta os cinco dados

- **WHEN** uma criança chega ao caminho do onboarding
- **THEN** a aplicação coleta nome, nick, forma de tratamento, data de nascimento e
  características do avatar, e não conclui o cadastro faltando qualquer um deles

#### Scenario: A comunidade nunca é perguntada à criança

- **WHEN** o cadastro do encontro é concluído
- **THEN** o Guerreiro(a) fica vinculado à comunidade da aula vigente, e em nenhum momento a
  aplicação lhe perguntou qual é

#### Scenario: Sem sessão de trabalho não há cadastro

- **WHEN** não há sessão de trabalho do aparelho aberta
- **THEN** o caminho do onboarding não é alcançável e nenhum cadastro é enviado ao núcleo

#### Scenario: O avatar nasce do catálogo, não de texto livre

- **WHEN** o cadastro do onboarding chega ao avatar
- **THEN** a criança compõe o avatar escolhendo no catálogo das nove camadas, e nenhum campo pede
  característica em texto livre

#### Scenario: A montagem abre com fundo e roupa de cores diferentes

- **WHEN** a tela de cadastro apresenta o avatar pela primeira vez
- **THEN** a cor do fundo e a cor da roupa são diferentes entre si

#### Scenario: Escolher fundo e roupa da mesma cor continua permitido

- **WHEN** a criança escolhe, na montagem, cor de fundo igual à cor da roupa
- **THEN** a escolha é aceita e gravada, sem aviso nem recusa

#### Scenario: O que se grava é o objeto versionado

- **WHEN** o cadastro é concluído
- **THEN** o campo do avatar leva o objeto versionado do documento 15 §7.2, e a forma de tratamento
  segue em campo próprio

#### Scenario: Compor não depende de rede

- **WHEN** a composição do avatar acontece
- **THEN** nenhuma requisição sai do aparelho para desenhar o avatar
