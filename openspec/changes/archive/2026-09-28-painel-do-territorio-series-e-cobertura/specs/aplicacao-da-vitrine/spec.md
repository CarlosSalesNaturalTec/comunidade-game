# Spec Delta

## ADDED Requirements

### Requirement: A seção de comunidades apresenta cada Comunidade Virtual em card e em página

A App 06 SHALL apresentar a seção **Comunidades Virtuais** com um card por comunidade, na
variante Comunidade Virtual da carta, e cada card SHALL abrir a **página da comunidade** em
endereço próprio, alcançável direto e compartilhável. Comunidade cuja leitura não devolve o que
a carta exige SHALL ser apresentada em outra forma, nunca em carta incompleta.

A seção SHALL aparecer nos três recortes de leitura em que o PRD-03 §5 a descreve, sem mudar o
conteúdo de um recorte para outro. (`RF-03-02`, `RF-03-15`, documento 11 §8.2, PRD-03 §§5.1,
5.2, 5.3)

#### Scenario: Cada comunidade sai em card

- **WHEN** a seção de comunidades é aberta e o núcleo devolve três comunidades
- **THEN** três cards aparecem, cada um com nome, território, representação visual, séries
  ativas e o número de vinculados

#### Scenario: O card abre a página da comunidade em endereço próprio

- **WHEN** o visitante abre o card de uma comunidade
- **THEN** a página daquela comunidade abre em endereço próprio, e o mesmo endereço, aberto
  direto, leva à mesma página

#### Scenario: Comunidade sem os indicadores não vira card incompleto

- **WHEN** o núcleo devolve uma comunidade com os quatro indicadores nulos
- **THEN** ela aparece na seção em outra forma, com o que a leitura devolveu, e nenhum card
  incompleto é apresentado

### Requirement: O painel da comunidade exibe as séries do território agregadas até o bairro

A página da comunidade SHALL exibir as **séries históricas do território**, agregadas até o
**bairro**, com a evolução no tempo. Nenhuma tela da vitrine SHALL exibir nick, nome, avatar ou
código de coletor, e nenhuma SHALL oferecer recorte, filtro ou ordenação por coletor.

O painel NEVER SHALL pedir nem apresentar granularidade abaixo do bairro; quem precisa do
conjunto completo SHALL ser encaminhado ao formulário de solicitação de dados. (`RF-03-15`,
`RF-03-16`, `RN-03-09`, `RN-03-10`, invariantes 7 e 12 do documento 99 §6, PRD-03 §5.2)

#### Scenario: A série aparece por tipo de coleta e bairro

- **WHEN** a página de uma comunidade com registros de dois tipos de coleta em dois bairros é
  aberta
- **THEN** o painel apresenta os recortes por tipo e bairro, com a evolução no tempo de cada um

#### Scenario: Nenhuma tela do painel identifica quem coletou

- **WHEN** o visitante percorre o painel inteiro de uma comunidade
- **THEN** nenhum nick, nome, avatar ou código de coletor aparece, e não há como recortar a
  série por uma pessoa

#### Scenario: O painel não oferece granularidade abaixo do bairro

- **WHEN** o visitante procura no painel um recorte de rua, condomínio, bloco ou quadra
- **THEN** nenhum existe, e a tela diz que a granularidade fina sai pela solicitação do
  conjunto de dados

### Requirement: Cada recorte do painel declara a metodologia e os registros válidos

O painel SHALL declarar, para cada recorte publicado, **o que se mede** com a unidade, a
**cadência**, o **período coberto**, a **origem da medição** — registro manual, por voz ou por
sensor construído na trilha — e o **número de registros válidos** do período apresentado.

A declaração SHALL acompanhar o recorte na própria tela, em linguagem legível por quem não
conhece a plataforma, e NEVER SHALL exigir que o visitante abra outra página para saber o que
está olhando. (`RF-03-17`, `RF-03-18`, PRD-03 §5.2)

#### Scenario: O recorte apresenta a metodologia junto do gráfico

- **WHEN** o visitante abre um recorte do painel
- **THEN** ele lê ali o que se mede com a unidade, a cadência, o período coberto, a origem da
  medição e quantos registros válidos sustentam aquele recorte

#### Scenario: A metodologia acompanha o período apresentado

- **WHEN** o painel apresenta um período mais estreito que a série inteira
- **THEN** o período coberto e a contagem de registros válidos exibidos são os daquele período

### Requirement: O recorte inativo aparece sinalizado, sem sumir do painel

O painel SHALL apresentar o recorte cuja coleta parou **sinalizado como inativo**, mantendo os
pontos já registrados e a metodologia dele — o dado é permanente, e o que muda é o sinal. O
recorte inativo NEVER SHALL ser removido, ocultado por padrão ou apresentado como ausência de
dado. (`RF-03-19`, documento 11 §8.3, invariante 7 do documento 99 §6)

#### Scenario: A série interrompida continua no painel, marcada

- **WHEN** um recorte da comunidade está inativo
- **THEN** ele aparece no painel com os seus pontos, marcado como inativo

#### Scenario: A marca de inativo é legível sem depender de cor

- **WHEN** o recorte inativo é apresentado
- **THEN** a condição de inativo se lê em texto, não só por cor

### Requirement: A comunidade sem dado aparece vazia, e o desenho cresce com o dado

A App 06 SHALL apresentar a comunidade recém-criada como **território vazio**, com nome e
contorno, em vez de omiti-la ou de apresentar erro, e SHALL fazer a representação visual
**crescer** conforme os registros acumulam, pela representação da camada comum.

Nenhum elemento do desenho SHALL aparecer sem fato que o sustente. (`RF-03-20`, `RF-03-21`,
documento 11 §8.3, documento 15 §5)

#### Scenario: Comunidade sem registro aparece vazia, não ausente

- **WHEN** uma comunidade criada por Admin ainda não tem registro algum
- **THEN** ela aparece na seção com nome e contorno, como território vazio

#### Scenario: O território ganha corpo conforme o dado chega

- **WHEN** a mesma comunidade passa a ter séries e registros válidos
- **THEN** a representação dela cresce e ganha detalhe na medida desse acúmulo

### Requirement: A cobertura da Agenda 2030 é da comunidade e do ciclo, nunca de um Guerreiro(a)

A App 06 SHALL apresentar o painel de **cobertura da Agenda 2030** agregado por **comunidade** e
por **ciclo**, com o rótulo do ciclo a que os números se referem. A cobertura NEVER SHALL
aparecer vinculada a um Guerreiro(a), nem por nick, avatar ou qualquer recorte que isole
alguém: a etiqueta é descritiva e agregada.

O painel SHALL destacar a contribuição do projeto à **meta 17.18** — dado local desagregado do
território — e SHALL registrar o **ODS 18** como **adoção voluntária do Brasil**, nunca como
objetivo oficial da ONU. (`RF-03-22`, `RF-03-23`, `RF-03-24`, `RN-03-19`, `RN-03-20`, PRD-03
§5.3)

#### Scenario: A cobertura sai por comunidade e por ciclo

- **WHEN** o painel de cobertura é aberto
- **THEN** ele apresenta, por comunidade, os objetivos que as trilhas e os desafios daquela
  comunidade tocaram, com o rótulo do ciclo

#### Scenario: Nenhuma etiqueta aparece por Guerreiro(a)

- **WHEN** o visitante percorre o painel de cobertura inteiro
- **THEN** nenhuma etiqueta ODS aparece ligada a uma pessoa

#### Scenario: A meta 17.18 e o ODS 18 saem com a redação correta

- **WHEN** o painel de cobertura é apresentado
- **THEN** a meta 17.18 aparece como a contribuição própria do projeto, e o ODS 18 aparece
  declarado como adoção voluntária do Brasil, não como objetivo da ONU

### Requirement: O recorte de gestores públicos abre com o bloco sobre a utilidade ao município

O recorte **gestores públicos** SHALL abrir com um **bloco em destaque**, **antes** do painel,
que traduza a plataforma para quem decide: que dado ela produz e para que serve, com **usos
concretos** do dado, o **caminho para pedir o conjunto completo**, como apoiar e como replicar o
modelo, já que o código é aberto.

O mesmo bloco SHALL declarar os limites: o dado é **agregado e anonimizado, nunca por
Guerreiro(a)**, e **não substitui indicador oficial** — é evidência produzida por moradores
sobre o próprio lugar. (`RF-03-63`, `RF-03-64`, `RF-03-65`, `RN-03-28`, PRD-03 §5.3)

#### Scenario: O bloco abre o recorte, antes do painel

- **WHEN** o visitante entra pelo recorte de gestores públicos
- **THEN** o bloco em destaque é a primeira coisa da tela, e o painel do território vem abaixo
  dele

#### Scenario: O bloco nomeia usos concretos e o caminho do conjunto completo

- **WHEN** o bloco é apresentado
- **THEN** ele lista usos concretos do dado e diz por onde se pede o conjunto completo

#### Scenario: O bloco declara os dois limites

- **WHEN** o bloco é apresentado
- **THEN** ele diz que o dado é agregado e nunca sai por Guerreiro(a), e que não substitui
  indicador oficial
