# Spec Delta

## ADDED Requirements

### Requirement: O escudo da marca tem o topo em ponta

O escudo que é a forma da marca do projeto SHALL ter o **topo em ponta**, formado por **duas
curvas que se encontram numa ponta central**, e NEVER SHALL ter o topo em aresta reta. A base
SHALL seguir em ponta, e o **monograma** SHALL continuar dentro do escudo. (documento 15 §13.1)

#### Scenario: O topo do escudo é uma ponta

- **WHEN** qualquer peça da marca que carrega o escudo é apresentada
- **THEN** o topo dele é uma ponta central formada por duas curvas, e não uma aresta reta

#### Scenario: O monograma continua dentro do escudo

- **WHEN** o símbolo do projeto é apresentado
- **THEN** o monograma aparece dentro do escudo, como antes da mudança de forma

### Requirement: O escudo tem uma forma só, em todas as peças da marca

Todas as peças da marca que carregam o escudo SHALL descrever a **mesma silhueta**, diferindo
entre si **apenas pela escala**. Nenhuma peça SHALL trazer correção de forma própria — raio de
canto, espessura de contorno e proporção SHALL guardar a mesma razão com a largura do escudo
em todas elas. Entre a versão colorida e a monocromática SHALL variar preenchimento e cor,
**nunca a geometria**. (documento 15 §§13.1, 13.3; `comum/marca/README.md` §7)

#### Scenario: As peças coincidem quando normalizadas

- **WHEN** o escudo de duas peças quaisquer da marca é normalizado pela largura declarada
- **THEN** as duas silhuetas coincidem dentro da tolerância de arredondamento

#### Scenario: A monocromática não diverge da colorida

- **WHEN** a silhueta da versão monocromática é comparada à da colorida na mesma escala
- **THEN** as duas coincidem, e o que difere é preenchimento e cor

#### Scenario: Uma peça que divergir é recusada

- **WHEN** uma peça da marca é alterada e passa a descrever silhueta diferente das demais
- **THEN** a verificação da camada comum recusa a alteração

### Requirement: A ponta do escudo sobrevive ao tamanho mínimo

A ponta do escudo SHALL continuar perceptível no **tamanho mínimo de uso** do símbolo, e o
contorno dela NEVER SHALL ser cortado pela borda da grade de desenho. (documento 15 §13.4)

#### Scenario: A ponta não é cortada pela grade

- **WHEN** qualquer peça da marca é desenhada
- **THEN** o ápice do escudo, somado a metade da espessura do contorno, cabe dentro da grade

#### Scenario: A ponta continua perceptível no tamanho mínimo

- **WHEN** o símbolo é apresentado no tamanho mínimo que o documento 15 fixa
- **THEN** a ponta continua distinguível de um topo reto
