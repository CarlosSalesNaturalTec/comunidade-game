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

#### Scenario: O que se grava é o objeto versionado

- **WHEN** o cadastro é concluído
- **THEN** o campo do avatar leva o objeto versionado do documento 15 §7.2, e a forma de tratamento
  segue em campo próprio

#### Scenario: Compor não depende de rede

- **WHEN** a composição do avatar acontece
- **THEN** nenhuma requisição sai do aparelho para desenhar o avatar

### Requirement: A tela das equipes mostra apenas avatar e nick

A App 01 SHALL apresentar as equipes já formadas na aula vigente pelo **nome** da equipe e, em
cada uma, os integrantes por **avatar e nick**, e NEVER SHALL exibir nome civil, data de
nascimento, imagem ou qualquer outro dado pessoal de um Guerreiro(a) para outro. (`RF-04-34`,
`RN-04-14`, documento 99 §6 invariante 11)

O avatar SHALL ser **desenhado** a partir do objeto do documento 15 §7.2, e NEVER SHALL ser
apresentado como texto nem omitido: avatar ausente ou com traço desconhecido SHALL cair no **avatar
padrão do projeto** (documento 15 §7.3), na mesma moldura dos demais e sem nenhuma outra marca de
diferença. (`RF-04-34`, documento 15 §7)

#### Scenario: As equipes da aula aparecem por avatar e nick

- **WHEN** o Guerreiro(a) em sessão abre a tela das equipes da aula vigente
- **THEN** cada equipe aparece com o nome dela e com o avatar e o nick de cada integrante, e
  nada além disso

#### Scenario: Nenhuma imagem de um Guerreiro(a) é exibida a outro

- **WHEN** a tela das equipes é apresentada
- **THEN** nenhuma fotografia de Guerreiro(a) aparece em tela alguma

#### Scenario: Equipes de outra aula não aparecem

- **WHEN** a tela das equipes da aula vigente é apresentada
- **THEN** as equipes formadas em outras aulas não estão entre as exibidas

#### Scenario: O avatar aparece desenhado ao lado do nick

- **WHEN** a tela das equipes da aula apresenta os integrantes
- **THEN** cada um aparece com o avatar desenhado e o nick, e nenhum aparece com o avatar em texto

#### Scenario: Avatar que falta cai no padrão do projeto

- **WHEN** um integrante não tem avatar, ou o avatar dele traz traço que o catálogo não conhece
- **THEN** a tela desenha o avatar padrão do projeto, na mesma moldura, sem marca de diferença
