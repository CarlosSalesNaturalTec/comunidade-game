# Spec Delta

## MODIFIED Requirements

### Requirement: A camada comum compõe o avatar paramétrico no próprio aparelho

A camada comum SHALL entregar o avatar do Guerreiro(a) como composição **paramétrica em camadas
SVG**, montada de **catálogo fechado**, nas nove camadas e na ordem do documento 15 §7.1 — fundo,
tom de pele, cabelo, cor do cabelo, rosto, olhos, boca, roupa e acessório. NEVER SHALL aceitar
traço fora do catálogo, e NEVER SHALL desenhar avatar a partir de texto livre. (documento 15 §7)

Cada traço do catálogo SHALL ter **nome dizível em português simples** — "cabelo black power", não
"modelo 7" —, porque no onboarding o avatar nasce de características ditas em voz alta por uma
criança de 6 anos. (documento 15 §7, `RF-04-06`)

Cada traço SHALL ser **distinguível no desenho**: escolher um traço SHALL mudar o que se vê, e
NEVER SHALL existir traço cujo desenho fique inteiramente coberto por outra camada. Nome dizível
sem desenho correspondente devolve à criança outro traço que não o escolhido, e anula junto a
camada que depende dele. (documento 15 §7, `RF-04-06`)

A escala de **tons de pele** SHALL abrir pelo **mais retinto**, e as texturas de **cabelo crespo**
SHALL vir antes das lisas. É requisito de conteúdo do catálogo, não ordem de tabela: o documento 15
declara a representatividade como construção, e a ordem é onde ela se realiza. (documento 15 §7.1)

Nenhum item do catálogo SHALL carregar marca de gênero, e todo item SHALL ser oferecido a qualquer
pessoa. A **forma de tratamento** é campo próprio da persona e NEVER SHALL derivar do avatar nem
restringi-lo. (documento 15 §7)

A camada de **rosto** SHALL admitir, além da silhueta do rosto, as **orelhas** e a **peça do cabelo
que cai à frente da testa**, esta na cor escolhida na camada de cor do cabelo. As nove camadas e a
ordem delas SHALL permanecer as do documento 15 §7.1. (documento 15 §7.1)

A camada de **roupa** SHALL sair com **contorno**, para que a silhueta do torso permaneça legível
quando a cor da roupa coincidir com a cor do fundo. Escolher as duas iguais SHALL continuar
permitido. (documento 15 §7.1)

A composição SHALL acontecer **no próprio aparelho, sem rede**, e o desenho NEVER SHALL depender de
requisição ao núcleo nem a domínio de terceiro. (documento 15 §7, princípio 6)

A camada comum SHALL ler e escrever o avatar como o **objeto pequeno e versionado** do documento 15
§7.2. **Traço desconhecido** SHALL cair no padrão da camada e NEVER SHALL quebrar a renderização —
é o que permite crescer o catálogo sem migrar avatar de ninguém, e o que faz o avatar gravado antes
deste contrato continuar renderizando. (documento 15 §7.2)

A camada comum SHALL entregar o **avatar padrão do projeto** — mesmo sistema, composição fixa e
neutra, em cores da marca — e SHALL usá-lo no lugar de **qualquer avatar que falte**, na mesma
moldura e sem nenhuma outra marca de diferença. (documento 15 §7.3)

#### Scenario: O avatar se compõe pelas nove camadas do catálogo

- **WHEN** um avatar é composto
- **THEN** ele se monta pelas nove camadas do documento 15 §7.1, na ordem delas, e cada escolha vem
  do catálogo fechado

#### Scenario: Cada traço tem nome dizível

- **WHEN** o catálogo é apresentado a quem escolhe
- **THEN** cada traço aparece com nome em português simples, e nenhum aparece como código ou número

#### Scenario: Trocar um traço muda o desenho

- **WHEN** um traço de qualquer camada é trocado por outro da mesma camada
- **THEN** o desenho resultante difere do anterior, e nenhum traço do catálogo desenha o mesmo que
  outro traço da mesma camada

#### Scenario: Nenhuma camada fica anulada pelo traço escolhido

- **WHEN** uma textura de cabelo é escolhida e a cor do cabelo é trocada
- **THEN** a troca de cor aparece no desenho, qualquer que seja a textura escolhida

#### Scenario: A escala de pele abre pelo mais retinto

- **WHEN** a camada de tom de pele é apresentada
- **THEN** a escala começa pelo tom mais retinto, e as texturas de cabelo crespo vêm antes das lisas

#### Scenario: Nenhum item é de um gênero

- **WHEN** qualquer camada do catálogo é apresentada
- **THEN** todos os itens dela são oferecidos, sem depender da forma de tratamento da persona

#### Scenario: O cabelo da frente é pintado por cima do rosto

- **WHEN** um avatar é desenhado com qualquer textura de cabelo
- **THEN** a peça da frente sai dentro da camada de rosto, na cor do cabelo, e as nove camadas
  continuam na ordem do documento 15 §7.1

#### Scenario: O torso continua legível sobre fundo da mesma cor

- **WHEN** a cor da roupa escolhida coincide com a cor do fundo escolhida
- **THEN** a silhueta do torso permanece distinguível do fundo, e a escolha não é recusada

#### Scenario: Compor e desenhar não pedem rede

- **WHEN** um avatar é composto e desenhado
- **THEN** nenhuma requisição sai do aparelho por causa do avatar

#### Scenario: Traço desconhecido cai no padrão da camada

- **WHEN** um avatar guardado traz traço que o catálogo não conhece, ou não traz o objeto do
  documento 15 §7.2
- **THEN** a camada desconhecida cai no padrão dela, o avatar é desenhado, e nada quebra

#### Scenario: Avatar que falta usa o padrão do projeto

- **WHEN** uma persona não tem avatar algum
- **THEN** o avatar padrão do projeto é desenhado, na mesma moldura dos demais e sem marca de
  diferença
