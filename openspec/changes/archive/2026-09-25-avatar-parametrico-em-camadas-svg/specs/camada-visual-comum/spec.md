# Spec Delta

## ADDED Requirements

### Requirement: A camada comum compõe o avatar paramétrico no próprio aparelho

A camada comum SHALL entregar o avatar do Guerreiro(a) como composição **paramétrica em camadas
SVG**, montada de **catálogo fechado**, nas nove camadas e na ordem do documento 15 §7.1 — fundo,
tom de pele, cabelo, cor do cabelo, rosto, olhos, boca, roupa e acessório. NEVER SHALL aceitar
traço fora do catálogo, e NEVER SHALL desenhar avatar a partir de texto livre. (documento 15 §7)

Cada traço do catálogo SHALL ter **nome dizível em português simples** — "cabelo black power", não
"modelo 7" —, porque no onboarding o avatar nasce de características ditas em voz alta por uma
criança de 6 anos. (documento 15 §7, `RF-04-06`)

A escala de **tons de pele** SHALL abrir pelo **mais retinto**, e as texturas de **cabelo crespo**
SHALL vir antes das lisas. É requisito de conteúdo do catálogo, não ordem de tabela: o documento 15
declara a representatividade como construção, e a ordem é onde ela se realiza. (documento 15 §7.1)

Nenhum item do catálogo SHALL carregar marca de gênero, e todo item SHALL ser oferecido a qualquer
pessoa. A **forma de tratamento** é campo próprio da persona e NEVER SHALL derivar do avatar nem
restringi-lo. (documento 15 §7)

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

#### Scenario: A escala de pele abre pelo mais retinto

- **WHEN** a camada de tom de pele é apresentada
- **THEN** a escala começa pelo tom mais retinto, e as texturas de cabelo crespo vêm antes das lisas

#### Scenario: Nenhum item é de um gênero

- **WHEN** qualquer camada do catálogo é apresentada
- **THEN** todos os itens dela são oferecidos, sem depender da forma de tratamento da persona

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
