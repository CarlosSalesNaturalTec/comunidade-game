# Spec Delta

## ADDED Requirements

### Requirement: A camada comum entrega o trio de estrelas da recompensa de marco

A camada comum SHALL entregar o glifo de **estrela cheia** do documento 15 §9, desenhado no
sistema de ícone da §11.1, e SHALL apresentá-lo em **trio** para marcar a recompensa de marco
conquistada. O trio SHALL levar preenchimento no degrau `ponto-500` e contorno no degrau
`ponto-700` da mesma família, pelos tokens semânticos — NEVER SHALL declarar valor de cor no
arquivo do glifo nem usar preto literal, que não acompanha o tema. (documento 15 §§9, 11.1,
`RF-05-45`)

#### Scenario: O trio é apresentado com três estrelas

- **WHEN** uma aplicação apresenta a marca da recompensa de marco conquistada
- **THEN** três estrelas cheias são apresentadas lado a lado

#### Scenario: A cor vem dos tokens da família ponto

- **WHEN** o trio é apresentado
- **THEN** o preenchimento e o contorno saem dos tokens semânticos da família ponto, e nenhum
  arquivo de glifo guarda valor de cor

#### Scenario: O trio acompanha o tema

- **WHEN** o tema claro dá lugar ao escuro
- **THEN** o trio continua apresentado pelos mesmos tokens, sem que a aplicação troque arquivo

### Requirement: O trio de estrelas nunca carrega sozinho o que foi conquistado

A camada comum SHALL apresentar o trio de estrelas como **segunda** via, e NEVER SHALL
permitir que ele seja a única forma de saber o que foi conquistado: o que a criança precisa
ler SHALL estar em **texto**, ao lado dele. O trio SHALL ser escondido de leitor de tela, para
que quem navega por ele alcance o texto da recompensa e não a descrição do desenho — é a mesma
exigência que o sistema de ícone já faz, aplicada a um glifo que não acompanha rótulo próprio.
(documento 15 §5, `RF-05-45`)

#### Scenario: O texto diz o que o trio não diz

- **WHEN** a recompensa conquistada é apresentada com o trio de estrelas
- **THEN** o que foi conquistado está escrito em texto ao lado dele, e o trio não é a única via

#### Scenario: Leitor de tela alcança o texto, não o desenho

- **WHEN** quem navega por leitor de tela chega à apresentação da recompensa
- **THEN** ouve o texto da recompensa, e nunca a contagem nem a descrição das estrelas

#### Scenario: Sem movimento, o fato continua legível

- **WHEN** a pessoa pede menos movimento no aparelho
- **THEN** o trio e o texto seguem apresentados, sem transição alguma, e nada do que foi
  conquistado se perde

## MODIFIED Requirements

### Requirement: O ícone é SVG servido pelo próprio domínio e nunca aparece sozinho

A camada comum SHALL entregar o sistema de ícone do documento 15 §11.1: SVG servido pelo **próprio
domínio** da aplicação, desenhado em grade de `24` px, com traço de `2` px de ponta e junta
arredondadas, **sem preenchimento**, e cor herdada do texto que o ícone acompanha. NEVER SHALL
buscar ícone em domínio de terceiro, e NEVER SHALL guardar valor de cor no arquivo do glifo: trocar
o tema SHALL trocar o ícone junto. (documento 15 §§11.1, 12, princípio 6)

São exceção ao **sem preenchimento** e à **cor herdada** apenas as duas peças que o documento
15 declara preenchidas: a **silhueta de badge** da §8.3 e a **ficha das grandezas** da §9 — e,
com ela, o trio de estrelas da recompensa de marco. Cada uma SHALL tirar o preenchimento e o
contorno dos **tokens semânticos** da sua família, e NEVER SHALL guardar valor de cor no
arquivo do glifo: a exceção é ao traço, nunca à regra de que o tema troca o ícone junto.

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

#### Scenario: A peça preenchida tira a cor dos tokens

- **WHEN** uma das peças que o documento 15 declara preenchidas é apresentada
- **THEN** o preenchimento e o contorno saem dos tokens semânticos da família dela, e o arquivo
  do glifo não guarda valor de cor algum
