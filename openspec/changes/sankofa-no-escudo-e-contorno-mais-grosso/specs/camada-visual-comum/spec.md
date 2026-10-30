# Spec Delta

## REMOVED Requirements

### Requirement: O escudo da marca tem o topo em ponta

**Reason**: O requisito amarrava a forma do escudo ao **monograma**, que deixa de existir —
exigia que *"o monograma SHALL continuar dentro do escudo"*, com cenário homônimo. A forma do
escudo não muda nesta change; o que muda é a figura que ele guarda.

**Migration**: Substituído por **"O escudo da marca tem o topo em ponta e guarda a figura do
símbolo"**, abaixo, que repete integralmente o que este exigia da forma — topo em ponta por
duas curvas, nunca aresta reta, base em ponta — e troca o monograma pela figura.

## ADDED Requirements

### Requirement: O escudo da marca tem o topo em ponta e guarda a figura do símbolo

O escudo que é a forma da marca do projeto SHALL ter o **topo em ponta**, formado por **duas
curvas que se encontram numa ponta central**, e NEVER SHALL ter o topo em aresta reta. A base
SHALL seguir em ponta, e a **figura do símbolo** SHALL ficar inteira dentro do escudo.
(documento 15 §13.1)

#### Scenario: O topo do escudo é uma ponta

- **WHEN** qualquer peça da marca que carrega o escudo é apresentada
- **THEN** o topo dele é uma ponta central formada por duas curvas, e não uma aresta reta

#### Scenario: A base do escudo segue em ponta

- **WHEN** qualquer peça da marca que carrega o escudo é apresentada
- **THEN** a base dela termina em ponta, como antes da troca da figura

#### Scenario: A figura fica dentro do escudo

- **WHEN** o símbolo do projeto é apresentado
- **THEN** a figura aparece inteira dentro do escudo, sem encostar no contorno

### Requirement: A figura dentro do escudo é o pássaro Sankofa

O símbolo SHALL trazer dentro do escudo o **pássaro Sankofa**, e NEVER SHALL trazer monograma
ou letra. A figura SHALL preservar os dois elementos que dão o sentido do símbolo — a
**cabeça virada para trás** e o **ovo**, alcançado pelo bico. (documento 15 §13.1)

#### Scenario: O símbolo não traz letra

- **WHEN** qualquer peça da marca que carrega o escudo é apresentada
- **THEN** dentro do escudo aparece o pássaro, e nenhuma letra ou monograma

#### Scenario: O gesto do Sankofa está presente

- **WHEN** o símbolo é apresentado no tamanho em que a figura se distingue
- **THEN** a cabeça aparece virada para trás e o ovo aparece à frente do bico

#### Scenario: A figura é a mesma em todas as peças

- **WHEN** a figura de duas peças quaisquer da marca é comparada
- **THEN** as duas descrevem o mesmo desenho, diferindo apenas pela escala e pelo encaixe

### Requirement: As contraformas da figura são vazadas, nunca pintadas

As contraformas da figura — olho, penas e vazados do corpo — SHALL ser **aberturas** que
deixam ver o que está atrás, e NEVER SHALL ser desenhadas como segunda cor. A versão
monocromática NEVER SHALL declarar cor alguma. (documento 15 §13.3; `comum/marca/README.md` §7)

#### Scenario: Na colorida a contraforma mostra o escudo

- **WHEN** o símbolo colorido é apresentado
- **THEN** o olho e os vazados deixam ver o preenchimento do escudo, e não uma cor própria

#### Scenario: Na monocromática a contraforma mostra o fundo

- **WHEN** a versão monocromática é apresentada sobre o modo escuro ou sobre a foto de
  comunidade
- **THEN** o olho e os vazados deixam ver o fundo, e a figura inteira herda a cor do texto

### Requirement: O reconhecimento no tamanho mínimo é do escudo, não da figura

No **tamanho mínimo de uso** do símbolo a figura SHALL poder fechar-se numa mancha sem que
isso seja defeito: o reconhecimento ali é carregado pelo **escudo e pela cor**. A figura SHALL
ser legível no tamanho do cabeçalho. (documento 15 §§13.4, 13.5)

#### Scenario: No favicon a figura pode fechar

- **WHEN** o símbolo é apresentado no tamanho mínimo que o documento 15 §13.4 fixa
- **THEN** a marca segue reconhecível pelo escudo e pela cor, ainda que a figura não se resolva

#### Scenario: No cabeçalho a figura se distingue

- **WHEN** o símbolo é apresentado no cabeçalho de uma aplicação
- **THEN** a silhueta do pássaro se distingue de uma mancha, com cabeça e corpo separáveis
