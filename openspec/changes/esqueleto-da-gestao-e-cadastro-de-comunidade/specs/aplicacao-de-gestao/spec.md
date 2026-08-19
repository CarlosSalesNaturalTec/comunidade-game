## Purpose

A App 03 é a mesa de comando do projeto: é nela que o Admin cadastra, aprova, lança e confere,
e é dela que sai a Comunidade Virtual, raiz de todo vínculo da plataforma. Esta capacidade
cobre como o adulto entra na aplicação, como a sessão e o papel governam o que ele alcança, e
o cadastro de Comunidade Virtual de ponta a ponta.

## ADDED Requirements

### Requirement: A aplicação é inteiramente autenticada e se identifica por chave

A App 03 SHALL apresentar a chave de aplicação dela em toda chamada ao núcleo e NEVER SHALL
expor tela de dados a quem não tem sessão aberta. Visitante não alcança tela alguma.
(`RF-01-02`, `RN-01-32`, PRD-02 §4)

#### Scenario: Quem não tem sessão vê a entrada

- **WHEN** alguém abre qualquer endereço da aplicação sem sessão aberta
- **THEN** a aplicação apresenta a tela de entrada, e nenhum dado de gestão aparece

#### Scenario: A chave acompanha toda chamada

- **WHEN** a aplicação chama qualquer rota de dados do núcleo
- **THEN** a chamada leva a chave de aplicação da App 03 do ambiente em que ela roda

### Requirement: O adulto entra por login social

A App 03 SHALL abrir sessão para o adulto que autentica pela conta social e SHALL guardar o
papel que o núcleo devolveu, que é o que governa o que ele alcança dali em diante.
(`RF-01-09`, documento 03 §1.1)

#### Scenario: Admin com cadastro entra

- **WHEN** um Admin autentica pela conta social associada ao cadastro dele
- **THEN** a aplicação abre a sessão e apresenta as telas de gestão do papel de Admin

#### Scenario: O papel vem do núcleo, não da tela

- **WHEN** a sessão é aberta
- **THEN** o papel que governa a aplicação é o que o núcleo devolveu, e nenhuma escolha na
  tela o altera

### Requirement: Conta sem cadastro é recusada com o caminho da solicitação

A App 03 SHALL apresentar a recusa de quem autentica com conta social sem cadastro
correspondente, orientando a pedir participação pela vitrine, e NEVER SHALL sugerir que o
acesso se resolve tentando de novo. (`RF-01-10`, `RN-01-04`)

#### Scenario: Conta social sem cadastro lê a orientação

- **WHEN** um adulto autentica com conta social que não corresponde a persona cadastrada
- **THEN** a aplicação apresenta a recusa com a orientação de solicitar participação pela
  vitrine, e nenhuma sessão é aberta

### Requirement: Sessão encerrada ou expirada devolve à entrada

A App 03 SHALL devolver o adulto à tela de entrada quando a sessão dele expira ou é
encerrada, e SHALL distinguir essa recusa da recusa da chave — são credenciais independentes.
(`RF-01-09`, `RN-01-34`)

#### Scenario: Sessão expirada durante o uso

- **WHEN** o adulto aciona uma tela de gestão e o núcleo recusa a sessão por expirada
- **THEN** a aplicação o devolve à tela de entrada, informando que a sessão terminou

#### Scenario: O adulto encerra a própria sessão

- **WHEN** o adulto aciona a saída
- **THEN** a sessão é encerrada no núcleo e a aplicação volta à tela de entrada

### Requirement: O Admin cria a Comunidade Virtual, que nasce vazia

A App 03 SHALL permitir ao Admin criar a Comunidade Virtual informando nome, localização e
granularidade máxima, e a comunidade criada SHALL nascer sem Guerreiro(a), sem local e sem
aula. (`RF-02-11`, `RN-02-04`, invariante 4)

#### Scenario: Admin cria a comunidade

- **WHEN** um Admin em sessão informa nome, localização e granularidade máxima e confirma
- **THEN** a comunidade passa a existir, vazia, e a aplicação a apresenta entre as existentes

#### Scenario: Campo obrigatório em falta

- **WHEN** o Admin confirma a criação com nome, localização ou granularidade máxima vazios
- **THEN** a aplicação aponta o campo em falta e nenhuma comunidade passa a existir

### Requirement: Quem não é Admin lê a recusa, não um erro cru

A App 03 SHALL apresentar em linguagem simples a recusa do núcleo a quem tenta criar
Comunidade Virtual sem ser Admin, e NEVER SHALL oferecer o caminho de criação a quem não pode
percorrê-lo. (`RN-02-04`, `RN-08-01`, PRD-02 §4)

#### Scenario: Mestre não alcança a criação

- **WHEN** um Mestre em sessão abre a aplicação
- **THEN** o caminho de criação de comunidade não lhe é oferecido

#### Scenario: Recusa do núcleo é explicada

- **WHEN** o núcleo recusa a criação por papel
- **THEN** a aplicação apresenta que só o Admin cria Comunidade Virtual, sem jargão de TI e
  sem código de erro cru

### Requirement: A aplicação apresenta as comunidades já criadas

A App 03 SHALL apresentar ao adulto em sessão as Comunidades Virtuais existentes, para que
ele saiba o que já há antes de criar. Comunidade abaixo do piso de coletores SHALL aparecer
sem os indicadores do território, e a ausência deles NEVER SHALL ser apresentada como falha.
(`RF-08-30`, `RF-08-31`, `RN-08-28`)

#### Scenario: Comunidade recém-criada aparece sem indicadores

- **WHEN** o adulto abre a lista logo após criar uma comunidade
- **THEN** a comunidade nova aparece nela, sem os indicadores do território e sem mensagem de
  erro

### Requirement: A aplicação cumpre o piso de acessibilidade das oito aplicações

A App 03 SHALL ser Web App responsivo projetado primeiro para o celular e SHALL cumprir o
piso do documento 15 §5: contraste, alvo de toque de 48 px, foco sempre visível, nenhum
significado por cor sozinha, ícone acionável nunca sem rótulo e `prefers-reduced-motion`
respeitado. A linguagem das telas e dos erros SHALL ser simples, sem jargão de TI.
(PRD-02 §10, documento 15 §5, invariante 1)

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
