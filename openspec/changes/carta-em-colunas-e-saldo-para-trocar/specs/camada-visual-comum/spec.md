# Spec Delta

## MODIFIED Requirements

### Requirement: A camada comum entrega a carta do personagem

A camada comum SHALL entregar a **carta do personagem**, o átomo de interface comum às oito
aplicações, com os valores do documento 15 §8.1: superfície de carta, borda de 1 px, **raio que vem
do temperamento** da aplicação, avatar **quadrado recortado em círculo ocupando metade da largura**
e nick na família de destaque. O avatar, a identificação e a frase de desempenho SHALL ser
apresentados **centralizados**, nas quatro variantes. (documento 15 §8.1, documento 11 §8.2,
decisão do fundador de 2026-10-30)

A carta SHALL exibir **apenas** o que o documento 11 §8.2 atribui à variante dela, e NEVER SHALL
exibir o que aquela tabela lista como nunca exibido — para a variante Guerreiro(a): nem imagem real,
nem nome civil, nem rede social, nem qualquer canal de contato. (documento 11 §8.2, invariantes 9 e
10)

A camada comum NEVER SHALL oferecer carta **pela metade**: variante cuja leitura não devolve o que a
tabela do documento 11 §8.2 exige SHALL ser apresentada em outra forma, não em carta incompleta.
(documento 11 §8.2, decisão do fundador registrada no documento 09 §1)

Havendo **rotação**, ela SHALL respeitar a preferência por menos movimento e NEVER SHALL ser a única
via ao conteúdo do verso. (documento 15 §§5, 8.1)

#### Scenario: A carta se monta com os valores do documento 15

- **WHEN** uma carta é apresentada
- **THEN** ela traz o avatar em círculo ocupando metade da largura, o nick na família de destaque, e
  o raio que o temperamento da aplicação declara

#### Scenario: A identidade da carta aparece centralizada

- **WHEN** uma carta de qualquer das quatro variantes é apresentada
- **THEN** o avatar, a identificação e a frase de desempenho aparecem centralizados na carta

#### Scenario: A carta do Guerreiro(a) não expõe o que é vedado

- **WHEN** a carta de um Guerreiro(a) é apresentada
- **THEN** nela aparecem avatar, nick, badges, poderes com níveis e criações originais — e, em tela
  logada, o saldo de pontos extras que dá para trocar —, e não aparecem imagem real, nome civil,
  rede social nem canal de contato

#### Scenario: Sem o dado que a variante exige, não se usa carta

- **WHEN** a leitura disponível não devolve o que a tabela do documento 11 §8.2 exige daquela
  variante
- **THEN** a tela apresenta a informação em outra forma, e nenhuma carta incompleta é apresentada

## ADDED Requirements

### Requirement: A carta do Guerreiro(a) apresenta as seções em colunas, com símbolo acima do rótulo

A camada comum SHALL apresentar as seções da variante **Guerreiro(a)** em **colunas**, cada uma com
o **símbolo acima do rótulo** e o rótulo acima do conteúdo. SHALL dispor **duas colunas por linha**
no celular e **quatro em linha** a partir do marco de largura de `768` px, e o arranjo SHALL
acompanhar o número de seções presentes. As outras três variantes NEVER SHALL receber o arranjo em
colunas. (documento 15 §§4, 8.1, decisão do fundador de 2026-10-30)

#### Scenario: As seções aparecem em colunas no celular

- **WHEN** a carta de um Guerreiro(a) com as quatro seções é apresentada em largura de celular
- **THEN** as seções aparecem em duas colunas por linha, cada uma com o símbolo acima do rótulo e o
  rótulo acima do conteúdo

#### Scenario: A partir do marco de largura as colunas ficam em linha

- **WHEN** a mesma carta é apresentada a partir do marco de `768` px
- **THEN** as quatro seções aparecem em uma linha só

#### Scenario: O arranjo acompanha o número de seções

- **WHEN** a carta é apresentada sem a seção do saldo de pontos extras
- **THEN** o arranjo se fecha nas seções presentes, sem coluna vazia nem espaço reservado

#### Scenario: As outras variantes não ganham colunas

- **WHEN** a carta de um Mestre, de um Apoiador ou de uma Comunidade Virtual é apresentada
- **THEN** o conteúdo dela segue em fluxo único, e só a identidade aparece centralizada

### Requirement: O símbolo de uma coluna nunca é silhueta de família, escudo nem círculo

O símbolo que encabeça uma coluna da carta SHALL ser desenhado no sistema de ícone do documento 15
§11.1 e NEVER SHALL ser uma das silhuetas de família de badge da §8.3, o **escudo** da marca ou o
**círculo** da moeda: no cabeçalho, a silhueta de família afirmaria família errada, e as outras duas
formas carregam significado reservado. O símbolo NEVER SHALL aparecer sem o rótulo da coluna.
(documento 15 §§8.3, 8.4, 9, 11.1, invariante 24)

#### Scenario: Nenhuma coluna é encabeçada por silhueta de família

- **WHEN** as colunas da carta são apresentadas
- **THEN** nenhum símbolo de cabeçalho é losango, estrela cheia, coração, gota, folha com canto
  dobrado ou hexágono, e nenhum é o escudo da marca nem o círculo da moeda

#### Scenario: O símbolo da coluna não aparece sozinho

- **WHEN** uma coluna da carta é apresentada
- **THEN** o símbolo vem acompanhado do rótulo da coluna, e quem navega por leitor de tela alcança o
  rótulo

### Requirement: A frase de desempenho leva a estrela da grandeza ponto regular

A camada comum SHALL apresentar a frase de desempenho da variante Guerreiro(a) acompanhada da
**estrela cheia**, que é o glifo da grandeza **ponto regular** do documento 15 §9. A estrela SHALL
tirar preenchimento e contorno dos tokens semânticos da família ponto, pela exceção que a §9 já
abre à regra de traço sem preenchimento, e NEVER SHALL carregar sozinha o significado: a frase
continua sendo a via ao conteúdo. (documento 15 §§5, 9, 11.1)

#### Scenario: A estrela acompanha a frase

- **WHEN** a carta de um Guerreiro(a) é apresentada
- **THEN** a frase de desempenho aparece com a estrela cheia ao lado, e a frase diz o desempenho
  por inteiro sem depender da estrela

#### Scenario: A estrela tira a cor dos tokens

- **WHEN** o tema claro dá lugar ao escuro
- **THEN** o preenchimento e o contorno da estrela mudam com os tokens da família ponto, e arquivo
  algum guarda valor de cor

### Requirement: A carta do Guerreiro(a) mostra o saldo de pontos extras que dá para trocar

A camada comum SHALL apresentar, na variante Guerreiro(a), uma seção com o **saldo disponível** de
pontos extras — o que dá para trocar por recompensa avulsa —, com **rótulo que o identifique como
saldo**. NEVER SHALL apresentar o **acumulado** nessa seção, e NEVER SHALL somar as duas contas nem
confundi-las com ponto regular. O símbolo da seção SHALL ser a **estrela vazada** da grandeza ponto
extra, na cor herdada do texto. (`RF-05-82`, documento 15 §9, documento 11 §8.2, invariante 23)

#### Scenario: A seção mostra o saldo, rotulado

- **WHEN** a carta do próprio Guerreiro(a) é apresentada em tela logada
- **THEN** a seção traz o saldo disponível de pontos extras, com rótulo que diz ser o saldo e que
  é o que dá para trocar

#### Scenario: O acumulado não entra na seção

- **WHEN** a seção do saldo é apresentada
- **THEN** o acumulado não aparece ali, nenhuma soma das duas contas é apresentada e nenhum ponto
  regular é apresentado como trocável

#### Scenario: A estrela vazada separa a grandeza

- **WHEN** a seção do saldo e a frase de desempenho aparecem na mesma carta
- **THEN** a grandeza ponto extra aparece com a estrela vazada e a regular com a estrela cheia,
  cada uma com o rótulo próprio

### Requirement: O saldo de pontos extras nunca aparece em superfície pública

A seção do saldo SHALL existir **apenas** onde quem vê é o próprio Guerreiro(a) em sessão, e NEVER
SHALL ser apresentada em superfície pública — vitrine, cards, rankings públicos, portfólio e jogos.
A **ausência** do saldo NEVER SHALL tornar a carta incompleta: a decisão de apresentar carta segue
sendo a do documento 11 §8.2, sem o saldo entre o que ela exige. (invariantes 8, 12 e 23,
`RF-03-06`, `RF-01-21`)

#### Scenario: A carta pública não traz o saldo

- **WHEN** a carta de um Guerreiro(a) é apresentada em superfície pública
- **THEN** a seção do saldo não aparece, e nada na carta revela quanto ele tem para trocar

#### Scenario: Sem o saldo, a carta continua se apresentando

- **WHEN** a leitura não traz o saldo, porque a superfície não tem como lê-lo
- **THEN** a carta se apresenta com as demais seções, e a falta do saldo não a torna incompleta

### Requirement: O contorno da família ponto é discernível nos dois temas

O contorno da família **ponto** SHALL ter valor próprio no tema escuro, de modo que toda peça que o
usa — a estrela da grandeza e o trio de estrelas da recompensa de marco — mantenha limite
discernível contra a superfície dos dois temas. (documento 15 §§3.3, 9)

#### Scenario: O contorno sobrevive ao tema escuro

- **WHEN** uma peça da família ponto é apresentada no tema escuro
- **THEN** o contorno dela continua discernível contra a superfície, e a razão de contraste medida
  está registrada no documento 15 §3.3
