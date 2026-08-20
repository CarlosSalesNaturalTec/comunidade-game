## MODIFIED Requirements

### Requirement: A aplicação cumpre o piso de acessibilidade das oito aplicações

A App 03 SHALL ser Web App responsivo projetado primeiro para o celular e SHALL cumprir o
piso do documento 15 §5: contraste, alvo de toque de 48 px, foco sempre visível, nenhum
significado por cor sozinha, ícone acionável nunca sem rótulo e `prefers-reduced-motion`
respeitado. A linguagem das telas e dos erros SHALL ser simples, sem jargão de TI.
As telas SHALL cumprir esse piso consumindo a camada visual comum, e NEVER SHALL
reimplementar por conta própria o alvo de toque, o foco, a associação do erro ao campo nem a
tipografia. (PRD-02 §10, documento 15 §5, invariante 1)

#### Scenario: Operação pelo teclado

- **WHEN** o adulto percorre a aplicação apenas pelo teclado
- **THEN** todo elemento acionável recebe foco visível e a ordem de foco acompanha a leitura
  da tela

#### Scenario: Quem pediu menos movimento

- **WHEN** o aparelho declara `prefers-reduced-motion`
- **THEN** a aplicação não anima transição alguma, e nenhum conteúdo depende do movimento
  para ser lido

#### Scenario: Operação em pé, no celular

- **WHEN** a aplicação é aberta na largura de um celular
- **THEN** as telas desta fatia são operáveis sem rolagem horizontal, com alvos de toque de
  ao menos 48 px

#### Scenario: Erro de campo anunciado no próprio campo

- **WHEN** o Admin confirma a criação com um campo obrigatório vazio e depois alcança esse
  campo pelo teclado ou por leitor de tela
- **THEN** a mensagem que aponta o campo em falta é anunciada junto com o rótulo dele, e o
  campo é anunciado como inválido

#### Scenario: As telas usam a tipografia do documento 15

- **WHEN** qualquer tela da aplicação é apresentada
- **THEN** o texto é desenhado por Atkinson Hyperlegible Next e o título por Archivo, ambas
  servidas pelo próprio domínio da aplicação

### Requirement: A aplicação apresenta as comunidades já criadas

A App 03 SHALL apresentar ao adulto em sessão as Comunidades Virtuais existentes, para que
ele saiba o que já há antes de criar. Comunidade abaixo do piso de coletores SHALL aparecer
sem os indicadores do território, e a ausência deles NEVER SHALL ser apresentada como falha.
A apresentação SHALL ser lista densa, no temperamento Operação, e NEVER SHALL usar a carta do
documento 15 §8.1 enquanto a lista não devolver o que o documento 11 §8.2 exige dela.
(`RF-08-30`, `RF-08-31`, `RN-08-28`, documento 15 §6)

#### Scenario: Comunidade recém-criada aparece sem indicadores

- **WHEN** o adulto abre a lista logo após criar uma comunidade
- **THEN** a comunidade nova aparece nela, sem os indicadores do território e sem mensagem de
  erro

#### Scenario: A ausência de indicadores se distingue do erro

- **WHEN** uma comunidade aparece sem os indicadores do território
- **THEN** o que a lista informa é a ausência de indicadores, apresentada como informação, e
  não como aviso de erro
