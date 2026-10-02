# Spec Delta

## ADDED Requirements

### Requirement: O cabeçalho apresenta o símbolo do projeto, nas oito aplicações

A camada comum SHALL apresentar o **símbolo do projeto** no cabeçalho das oito aplicações,
servido pelo **próprio domínio** e nunca por domínio de terceiro, com o **nome do projeto em
texto** ao lado dele. O símbolo NEVER SHALL ser a única via ao nome: quem não vê a imagem lê o
nome. (documento 15 §§1, 5, princípios 3 e 6)

#### Scenario: O cabeçalho apresenta o símbolo

- **WHEN** qualquer uma das oito aplicações é aberta
- **THEN** o cabeçalho apresenta o símbolo do projeto, servido pelo próprio domínio

#### Scenario: O nome não depende da imagem

- **WHEN** o símbolo não carrega
- **THEN** o nome do projeto continua legível em texto no cabeçalho

#### Scenario: O nome não aparece em dobro

- **WHEN** o cabeçalho é apresentado
- **THEN** o nome do projeto aparece uma única vez, e a peça apresentada ao lado dele não o
  repete em imagem

### Requirement: A marca tem uma versão colorida e uma monocromática

A marca SHALL ter uma versão **colorida**, para o modo claro, e uma **monocromática**, que
herda a cor do texto e atende tanto o **modo escuro** quanto o uso **sobre a foto de
comunidade**. O contraste da marca apresentada SHALL ser medido sobre superfície opaca, como o
de qualquer outro elemento. (documento 15 §§3.3, 5, 6.3)

#### Scenario: O modo escuro recebe a monocromática

- **WHEN** a aplicação é apresentada no modo escuro
- **THEN** a marca apresentada é a monocromática, que herda a cor do texto

#### Scenario: Sobre foto, a marca continua legível

- **WHEN** a marca é apresentada sobre a foto de comunidade
- **THEN** ela é a monocromática, e o contraste é medido sobre a superfície opaca que a
  moldura garante

### Requirement: Nenhuma aplicação serve marca de terceiro

Nenhuma aplicação SHALL servir marca de outro produto. O **favicon** de cada uma SHALL ser o
do projeto, a partir de **arquivo único** da camada comum, e NEVER SHALL ser o do andaime de
construção. (documento 15 §1, princípios 4 e 6; documento 03 §1)

#### Scenario: O favicon é o do projeto

- **WHEN** o favicon de qualquer aplicação é buscado
- **THEN** ele é a marca do projeto, e nunca a de outro produto

#### Scenario: O favicon vem de um arquivo só

- **WHEN** o favicon de duas aplicações diferentes é comparado
- **THEN** ambos vêm do mesmo arquivo da camada comum

## MODIFIED Requirements

### Requirement: Cada família de badge tem silhueta própria, legível sem cor

A camada comum SHALL entregar **uma silhueta por família de badge** do documento 15 §8.3 —
losango para nível, estrela para conquista, coração para valores e causas, gota para
território, folha com canto dobrado para autoria e hexágono para protagonismo —, cada uma
legível a **`24` px** e reconhecível **sem depender de cor**. (documento 15 §8.3)

A silhueta SHALL dizer a **família**, nunca o poder: dois badges de nível são ambos losango. O
que os separa SHALL ser o **glifo do poder**. (documento 15 §§8.3, 8.4)

Nenhuma silhueta de badge SHALL ser o **escudo**, que é a forma da marca do projeto: badge e
marca NEVER SHALL se confundir na mesma tela, porque aqui a forma carrega significado
(documento 99, invariante 24). (documento 15 §§8.3, 8.4)

#### Scenario: A família se reconhece pela forma

- **WHEN** badges de famílias diferentes são apresentados juntos
- **THEN** cada um traz a silhueta da família dele, distinguível a `24` px e sem depender de cor

#### Scenario: Dois badges da mesma família se distinguem pelo poder

- **WHEN** dois badges de nível de poderes diferentes são apresentados
- **THEN** ambos trazem losango, e o glifo do poder dentro deles é o que os separa

#### Scenario: O badge não se confunde com a marca

- **WHEN** um badge e a marca do projeto são apresentados na mesma tela
- **THEN** nenhuma silhueta de badge é o escudo, e a marca se distingue de todas elas pela forma
