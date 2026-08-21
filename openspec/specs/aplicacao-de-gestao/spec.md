# aplicacao-de-gestao Specification

## Purpose

A App 03 é a mesa de comando do projeto: é nela que o Admin cadastra, aprova, lança e confere,
e é dela que sai a Comunidade Virtual, raiz de todo vínculo da plataforma. Esta capacidade
cobre como o adulto entra na aplicação, como a sessão e o papel governam o que ele alcança, e
o cadastro de Comunidade Virtual de ponta a ponta.

## Requirements

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

### Requirement: O Admin cadastra o ponto de apoio da comunidade

A App 03 SHALL permitir ao Admin cadastrar o ponto de apoio informando **nome** e a
**comunidade** a que ele pertence, e SHALL apresentar os pontos de apoio já cadastrados antes
de oferecer o cadastro, para que ele saiba o que já há. A apresentação SHALL ser **lista
densa**, no temperamento Operação, como a das comunidades.

O ponto de apoio SHALL nascer **sem responsável pelo acervo**, e a aplicação NEVER SHALL
apresentar essa ausência como falha: a designação é ato posterior e não é desta fatia.
(`RF-07-47`, `RF-07-49`, `RN-07-34`, documento 15 §6)

#### Scenario: Admin cadastra o ponto de apoio

- **WHEN** um Admin em sessão informa nome e comunidade e confirma
- **THEN** o ponto de apoio passa a existir e a aplicação o apresenta entre os existentes

#### Scenario: Campo obrigatório em falta

- **WHEN** o Admin confirma o cadastro com nome ou comunidade vazios
- **THEN** a aplicação aponta o campo em falta, no próprio campo, e nenhum ponto de apoio
  passa a existir

#### Scenario: Ponto de apoio sem responsável não é apresentado como pendência

- **WHEN** a lista apresenta um ponto de apoio ainda sem responsável pelo acervo
- **THEN** a ausência aparece como informação, e não como aviso de erro

#### Scenario: Quem não é Admin não alcança o cadastro

- **WHEN** um Mestre em sessão abre a área de pontos de apoio
- **THEN** o caminho de cadastro não lhe é oferecido, e a recusa do núcleo, se ocorrer, é
  apresentada em linguagem simples

### Requirement: O Admin agenda a aula com comunidade, data e horários

A App 03 SHALL permitir ao Admin agendar a aula informando **comunidade**, **data**, **horário
inicial**, **horário final** e o **ponto de apoio** em que ela acontece. A data e os horários
SHALL trafegar com **fuso**, e a aplicação NEVER SHALL enviar horário sem ele.

A aplicação SHALL oferecer, como ponto de apoio, apenas os da **comunidade escolhida**, e SHALL
apresentar no próprio campo a recusa do núcleo a horário final não posterior ao inicial e a
ponto de apoio de outra comunidade. Aula agendada sem recurso declarado SHALL nascer
**confirmada**, e a aplicação SHALL apresentar a situação como ela vem do núcleo, sem
recalculá-la. (`RF-02-12`, `RF-02-30`, `RN-02-09`, PRD-02 §5.1)

#### Scenario: Admin agenda a aula

- **WHEN** um Admin em sessão informa comunidade, data, horário inicial, horário final e ponto
  de apoio, e confirma
- **THEN** a aula passa a existir, confirmada, e a aplicação a apresenta na agenda

#### Scenario: Horário final anterior ao inicial é apontado no campo

- **WHEN** o Admin confirma o agendamento com horário final não posterior ao inicial
- **THEN** a aplicação aponta o erro no próprio campo e nenhuma aula passa a existir

#### Scenario: O ponto de apoio oferecido é o da comunidade escolhida

- **WHEN** o Admin escolhe a comunidade no formulário
- **THEN** só os pontos de apoio daquela comunidade lhe são oferecidos

#### Scenario: Quem não é Admin não alcança o agendamento

- **WHEN** um Mestre em sessão abre a agenda
- **THEN** o caminho de agendamento não lhe é oferecido

### Requirement: A aplicação apresenta a agenda das aulas

A App 03 SHALL apresentar as aulas com **comunidade**, **ponto de apoio**, **data**, **horários**
e **situação**, em lista densa, filtráveis por comunidade e por período. A aula **pendente de
lastro** SHALL se distinguir da **confirmada** na apresentação, e a aula **cancelada** SHALL
exibir o **motivo** registrado.

O **Mestre** SHALL ler a agenda das comunidades a que está vinculado; a aplicação NEVER SHALL
lhe apresentar aula de comunidade a que não pertence. (`RF-02-12`, `RF-01-18`, `RN-02-09`,
`RN-02-20`, documento 15 §6)

#### Scenario: A agenda distingue as situações

- **WHEN** a agenda apresenta uma aula confirmada e uma pendente de lastro
- **THEN** cada uma aparece com a sua situação, distinguíveis sem depender só de cor

#### Scenario: Aula cancelada mostra o motivo

- **WHEN** a agenda apresenta uma aula cancelada
- **THEN** o motivo registrado no cancelamento aparece junto dela

#### Scenario: Mestre lê só a agenda das suas comunidades

- **WHEN** um Mestre vinculado a uma comunidade abre a agenda
- **THEN** só aparecem as aulas daquela comunidade

### Requirement: A aula agendada é cancelada com motivo

A App 03 SHALL permitir o cancelamento da aula agendada ao **Admin** e ao **Mestre da comunidade
da aula**, exigindo o **motivo** e NEVER SHALL aceitar o cancelamento sem ele. A aplicação SHALL
apresentar, antes de confirmar, que o cancelamento **libera os recursos reservados** e que ele
não se desfaz.

Cancelada a aula, a aplicação SHALL apresentá-la com a situação cancelada e o motivo, e NEVER
SHALL oferecer o cancelamento de aula que já teve desfecho. (`RF-02-95`, `RF-01-72`,
`RN-02-20`, PRD-02 §5.4)

#### Scenario: Admin cancela a aula com motivo

- **WHEN** um Admin em sessão confirma o cancelamento informando o motivo
- **THEN** a aula passa a cancelada, com o motivo, e a agenda a apresenta assim

#### Scenario: Cancelamento sem motivo é recusado no campo

- **WHEN** quem cancela confirma sem informar o motivo
- **THEN** a aplicação aponta o campo em falta e a aula segue como estava

#### Scenario: Mestre da comunidade da aula cancela

- **WHEN** um Mestre vinculado à comunidade da aula confirma o cancelamento com motivo
- **THEN** a aula passa a cancelada, e a aplicação não lhe oferece nenhuma outra escrita da
  agenda

#### Scenario: Aula com desfecho não oferece cancelamento

- **WHEN** a agenda apresenta uma aula já cancelada ou já realizada
- **THEN** o caminho de cancelamento não é oferecido para ela

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

### Requirement: A dependência externa de identidade só é acionada quando configurada

A App 03 SHALL acionar o provedor externo de identidade apenas quando o client ID do ambiente
em que ela roda estiver configurado, e NEVER SHALL carregar o script dele em ambiente que não
o tenha — conferência à mão, execução de teste ou demonstração. A tela de entrada SHALL
continuar apresentável nesse ambiente, sem apresentar a ausência do provedor como falha.
(documento 03 §1 princípio 2, PRD-02 §10)

#### Scenario: Ambiente sem client ID configurado

- **WHEN** a tela de entrada é apresentada num ambiente cujo client ID não está configurado
- **THEN** nenhum script do provedor externo de identidade é carregado, e a tela continua
  apresentável, sem mensagem de erro

#### Scenario: Ambiente com client ID configurado

- **WHEN** a tela de entrada é apresentada num ambiente cujo client ID está configurado
- **THEN** o caminho de entrada pela conta social é oferecido ao adulto
