# Spec Delta

## ADDED Requirements

### Requirement: A vitrine aplica o temperamento Arena do cabeçalho ao rodapé

A App 06 SHALL apresentar toda tela pública no temperamento **Arena**, inclusive o painel
do território e os rankings, e NEVER SHALL reproduzir em tela nenhuma a densidade da
Operação — tabela, lote e painel de declaração são da outra família.

Toda tela pública SHALL trazer a **moldura de fundo de comunidade**: a cor chapada com a
foto da comunidade atrás dela quando houver foto, e **só a cor chapada** quando não
houver. O que a tela comunica NEVER SHALL depender da foto, e os pisos de contraste
SHALL continuar medidos sobre superfície opaca, nunca sobre a fotografia. (documento 15
§§6, 6.3, `RF-03-51`, `RN-03-22`)

#### Scenario: Toda tela pública traz a moldura da Arena

- **WHEN** qualquer tela pública da vitrine é aberta
- **THEN** ela é apresentada dentro da moldura de fundo de comunidade

#### Scenario: Sem foto, a tela é exatamente a mesma

- **WHEN** a comunidade não tem foto escolhida, ou a foto não carrega
- **THEN** a tela apresenta só a cor chapada, e nada do que ela comunica se perde

#### Scenario: A moldura não busca recurso de terceiro

- **WHEN** a moldura é apresentada
- **THEN** nenhuma requisição sai para domínio que não seja o próprio

### Requirement: A carta domina a página individual, com uma decisão só

A **página individual** de Guerreiro(a), de Mestre, de Apoiador e de comunidade SHALL
apresentar a carta como o **elemento maior da tela**, e SHALL pedir **uma decisão só**. O
que a página ainda comunica SHALL ficar **abaixo e menor** que a carta, sem disputar o
primeiro plano com ela.

Voltar NEVER SHALL contar como decisão: é saída, e mora na ação do cabeçalho.
(documento 15 §6, `RF-03-03`, `RF-03-05`, `RF-03-15`)

#### Scenario: A carta é o elemento maior da página de Guerreiro(a)

- **WHEN** a página individual de um Guerreiro(a) com autorização vigente é aberta
- **THEN** a carta domina a tela, e o portfólio e o desempenho ficam abaixo dela

#### Scenario: A página individual pede uma decisão só

- **WHEN** uma das quatro páginas individuais é aberta
- **THEN** ela apresenta uma única decisão, e sair não é contado como decisão

### Requirement: O ícone acompanha ação e estado, e nunca aparece sozinho

A App 06 SHALL usar o sistema de ícone da camada comum onde a tela tem ação ou estado, e
o ícone NEVER SHALL aparecer sem o rótulo textual que ele acompanha.

Nenhum estado SHALL passar a se comunicar apenas pelo ícone: a cor, a forma e o glifo
acompanham numeral ou rótulo, nunca o substituem. (documento 15 §§5, 11.1, princípio 3)

#### Scenario: Ação com ícone mantém o rótulo

- **WHEN** uma ação da vitrine é apresentada com ícone
- **THEN** o rótulo textual dela continua visível ao lado do glifo

#### Scenario: Nenhum estado depende do ícone

- **WHEN** uma tela apresenta estado com glifo
- **THEN** o mesmo estado continua legível em texto, numeral ou forma
