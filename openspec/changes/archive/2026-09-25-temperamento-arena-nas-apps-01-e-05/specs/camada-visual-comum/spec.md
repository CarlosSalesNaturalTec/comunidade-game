# Spec Delta

## ADDED Requirements

### Requirement: A camada declara os dois temperamentos, e cada aplicação declara o seu

A camada comum SHALL declarar a camada de tema dos **dois** temperamentos do documento 15 §6 —
Operação e Arena —, e cada aplicação SHALL declarar na raiz do documento o temperamento que o
documento 15 §6 lhe atribui: **Operação** nas Apps 03, 07, 08 e 09; **Arena** nas Apps 01, 04, 05
e 06. NEVER SHALL uma aplicação declarar o temperamento da outra família, e NEVER SHALL o
temperamento valer por região de uma tela: ele é da aplicação inteira. (documento 15 §6,
invariante 24)

A camada de tema da Arena SHALL declarar o que o documento 15 §6 fixa em número para ela: **raio
de carta de `12` px** e **duração de transição de `300` ms**. A supressão de movimento por
preferência do aparelho SHALL continuar valendo sobre os dois temperamentos. (documento 15 §§5, 6)

A camada NEVER SHALL declarar, para a Arena, valor que o documento 15 não fixe. A densidade da
Arena é descrita como composição — poucos elementos, uma decisão por tela —, sem número, e o token
de densidade é lido apenas pelas telas densas da Operação. (documento 15 §6)

#### Scenario: Cada aplicação declara o temperamento do documento 15

- **WHEN** a App 01 ou a App 05 é aberta
- **THEN** o documento declara o temperamento Arena, e nenhuma das duas declara Operação

#### Scenario: A Arena tem camada de tema própria

- **WHEN** uma aplicação declara o temperamento Arena
- **THEN** o raio de carta vale `12` px e a duração de transição vale `300` ms, em vez dos valores
  da Operação

#### Scenario: As aplicações da Operação seguem como estão

- **WHEN** as Apps 03, 07, 08 e 09 são abertas
- **THEN** cada uma declara o temperamento Operação, e a densidade progressiva delas continua
  valendo a partir do marco de largura

#### Scenario: Menos movimento vence o temperamento

- **WHEN** o aparelho declara preferir menos movimento numa aplicação da Arena
- **THEN** nenhuma transição acontece, como já vale na Operação

### Requirement: O ícone é SVG servido pelo próprio domínio e nunca aparece sozinho

A camada comum SHALL entregar o sistema de ícone do documento 15 §11.1: SVG servido pelo **próprio
domínio** da aplicação, desenhado em grade de `24` px, com traço de `2` px de ponta e junta
arredondadas, **sem preenchimento**, e cor herdada do texto que o ícone acompanha. NEVER SHALL
buscar ícone em domínio de terceiro, e NEVER SHALL guardar valor de cor no arquivo do glifo: trocar
o tema SHALL trocar o ícone junto. (documento 15 §§11.1, 12, princípio 6)

Todo ícone SHALL ser apresentado com **rótulo textual** visível ou acessível. NEVER SHALL um ícone
ser a única forma de identificar um elemento acionável, e NEVER SHALL substituir o rótulo que o
elemento já tem. (documento 15 §5)

#### Scenario: Nenhum ícone vem de fora

- **WHEN** uma aplicação apresenta um ícone
- **THEN** ele é servido pelo próprio domínio, e nenhum pedido vai para domínio de terceiro

#### Scenario: O ícone acompanha o tema

- **WHEN** o tema claro dá lugar ao escuro
- **THEN** o ícone muda de cor junto com o texto que acompanha, sem que arquivo algum declare cor

#### Scenario: O ícone não aparece sozinho

- **WHEN** um elemento acionável é apresentado com ícone
- **THEN** ele tem rótulo textual visível ou acessível, e quem navega por leitor de tela alcança o
  rótulo, não a descrição do desenho
