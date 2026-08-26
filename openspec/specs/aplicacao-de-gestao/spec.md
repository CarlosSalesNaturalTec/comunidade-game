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

### Requirement: O Admin desativa e reativa o ponto de apoio pela aplicação

A App 03 SHALL oferecer ao Admin, no ponto de apoio já cadastrado, as ações de **desativar** e
**reativar**, cada uma exigindo motivo antes de confirmar. A lista de pontos de apoio SHALL
distinguir o ativo do inativo, e o inativo SHALL continuar visível — é histórico, não some. As
ações NEVER SHALL ser oferecidas a quem não é Admin. (`RF-07-47`, `RN-07-33`, `RN-02-21`,
PRD-02 §4)

#### Scenario: Admin desativa um ponto de apoio

- **WHEN** um Admin em sessão desativa um ponto de apoio informando o motivo
- **THEN** o ponto passa a aparecer como inativo na lista, e o motivo fica registrado

#### Scenario: Inativo continua na lista

- **WHEN** um Admin abre a lista de pontos de apoio de uma comunidade que tem um inativo
- **THEN** o inativo aparece, distinguido do ativo

#### Scenario: Mestre não vê a ação

- **WHEN** um Mestre em sessão abre um ponto de apoio
- **THEN** as ações de desativar e reativar não lhe são oferecidas

#### Scenario: Sem motivo não confirma

- **WHEN** o Admin tenta confirmar a desativação com o motivo vazio
- **THEN** a aplicação aponta o campo em falta e nada é enviado ao núcleo

### Requirement: A recusa da desativação diz o que está prendendo o espaço

A App 03 SHALL apresentar em linguagem simples por que a desativação foi recusada: **quantas
aulas futuras** prendem o ponto de apoio, ou **quais tipos de recurso** ainda têm saldo nele. A
aplicação SHALL oferecer, na recusa por saldo, o caminho da **transferência**, e NEVER SHALL
apresentar código de erro cru. (`RF-07-47`, `RN-07-01`, `RN-07-15`, PRD-02 §10)

#### Scenario: Recusa por aula futura é explicada

- **WHEN** o núcleo recusa a desativação porque há aulas futuras no ponto de apoio
- **THEN** a aplicação diz quantas aulas o prendem, sem jargão de TI

#### Scenario: Recusa por saldo oferece a transferência

- **WHEN** o núcleo recusa a desativação porque ainda há saldo no ponto de apoio
- **THEN** a aplicação diz quais tipos têm saldo e oferece o caminho de transferi-los

### Requirement: O Admin transfere o saldo de um ponto de apoio para outro

A App 03 SHALL oferecer ao Admin a **transferência** de um tipo de recurso de um ponto de apoio
para outro, informando tipo, quantidade, destino e motivo. A aplicação SHALL apresentar o saldo
disponível na origem antes de confirmar, NEVER SHALL oferecer como destino um ponto de apoio
inativo nem o próprio ponto de origem, e SHALL apresentar a transferência confirmada como **um
fato só**, não como dois lançamentos soltos. (`RF-07-19`, `RN-07-15`, `RN-07-33`)

#### Scenario: Admin transfere um tipo de recurso

- **WHEN** um Admin informa tipo, quantidade, ponto de apoio de destino e motivo, e confirma
- **THEN** a transferência acontece e os saldos dos dois pontos de apoio aparecem atualizados

#### Scenario: O destino inativo não é oferecido

- **WHEN** o Admin escolhe o destino da transferência
- **THEN** os pontos de apoio inativos e o próprio ponto de origem não aparecem entre as
  opções

#### Scenario: Quantidade acima do saldo é barrada antes de enviar

- **WHEN** o Admin informa quantidade maior que o saldo disponível na origem
- **THEN** a aplicação aponta o limite e nada é enviado ao núcleo

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

### Requirement: O Admin cadastra e edita o Guerreiro(a) pela aplicação

A App 03 SHALL oferecer ao Admin o cadastro de Guerreiro(a) com nome, data de nascimento, nick
e características do avatar, e a edição do que já foi cadastrado. A aplicação SHALL apontar o
campo em falta antes de chamar o núcleo e SHALL apresentar em linguagem simples a recusa por
nick em uso, **sem dizer de quem é o nick**. A aplicação NEVER SHALL exibir a imagem do
Guerreiro(a): a representação é o avatar. (`RF-02-01`, `RN-02-22`, invariante 12 do documento
99 §6, PRD-02 §11)

#### Scenario: Admin cadastra o Guerreiro(a)

- **WHEN** um Admin em sessão informa nome, nascimento, nick e avatar e confirma
- **THEN** o Guerreiro(a) passa a existir e a aplicação o apresenta entre os cadastrados

#### Scenario: Nick em uso é explicado sem revelar o dono

- **WHEN** o núcleo recusa o cadastro porque o nick já está em uso
- **THEN** a aplicação pede outro nick, sem informar quem o usa nem de que papel

#### Scenario: A gestão não vê a imagem da criança

- **WHEN** um Admin abre o cadastro de um Guerreiro(a)
- **THEN** a tela mostra avatar e nick, e nenhuma imagem real aparece

### Requirement: O Admin cadastra Mestre e Apoiador declarando os artefatos

A App 03 SHALL oferecer ao Admin o cadastro de Mestre e de Apoiador com nome, e-mail, WhatsApp
opcional e os artefatos comprobatórios, cada um com endereço e rótulo. A aplicação SHALL
impedir a confirmação sem ao menos um artefato e SHALL explicar por quê. A tela NEVER SHALL
oferecer anexo de arquivo como artefato, nem exigir nick. (`RF-02-02`, `RF-02-03`, `RF-02-04`,
`RN-02-01`, documento 02 §1)

#### Scenario: Admin cadastra Mestre com um link

- **WHEN** um Admin informa nome, e-mail e um link de currículo com rótulo e confirma
- **THEN** o Mestre passa a existir e a aplicação o apresenta entre os cadastrados

#### Scenario: Sem artefato a aplicação não deixa confirmar

- **WHEN** o Admin tenta confirmar o cadastro de um Apoiador sem artefato algum
- **THEN** a aplicação explica que ao menos um é obrigatório e nada é enviado ao núcleo

#### Scenario: A tela de adulto não pede nick ao Admin

- **WHEN** um Admin abre o cadastro de Mestre
- **THEN** a tela não exige nick, porque o Mestre o define no primeiro acesso

### Requirement: A aplicação oferece ao Admin gravar o nick do adulto na colisão

A App 03 SHALL oferecer ao Admin, na ficha de um Mestre ou de um Apoiador, o caminho de gravar
ou trocar o nick daquela persona, e SHALL sinalizar na lista quem está **sem nick**. A
aplicação SHALL apresentar em linguagem simples que o adulto sem nick não aparece em superfície
pública, e NEVER SHALL sugerir ao Admin um nick nem revelar de quem é o nick recusado.
(`RF-02-01`, `RN-01-30`, `RN-14-10`)

#### Scenario: Adulto sem nick é sinalizado na lista

- **WHEN** um Admin abre a lista de Mestres e Apoiadores
- **THEN** quem está sem nick aparece sinalizado, com o caminho de gravá-lo

#### Scenario: Admin grava o nick que recebeu por fora

- **WHEN** o Admin grava um nick disponível na ficha de um Apoiador sem nick
- **THEN** o nick passa a valer e a sinalização de ausência some

#### Scenario: A aplicação não sugere nick ao Admin

- **WHEN** o Admin abre o caminho de gravar nick
- **THEN** a tela não oferece sugestão alguma, e o nick é o que a pessoa lhe passou

### Requirement: O Admin inclui outro Admin e cadastra o responsável com o vínculo

A App 03 SHALL oferecer ao Admin a inclusão manual de outro Admin (`RF-02-05`) e o cadastro de
responsável com o **vínculo** a Guerreiros e Guerreiras já cadastrados, declarando o **grau de
parentesco** em texto livre (`RF-02-06`). A aplicação SHALL impedir o quarto vínculo de um
mesmo Guerreiro(a), respeitando o teto de três responsáveis, e SHALL oferecer a criação de
**credencial de usuário e senha provisória** para o adulto sem conta social (`RF-02-07`).
(`RN-02-02`, `RN-02-08`, invariante 3 do documento 99 §6)

#### Scenario: Admin inclui outro Admin

- **WHEN** um Admin em sessão informa nome e e-mail de um novo Admin e confirma
- **THEN** o Admin novo passa a existir, sem nenhum caminho de autocadastro envolvido

#### Scenario: Responsável é vinculado com grau de parentesco

- **WHEN** o Admin cadastra um responsável e o vincula a um Guerreiro(a) declarando o
  parentesco
- **THEN** o vínculo passa a existir com o parentesco declarado

#### Scenario: Quarto responsável é barrado

- **WHEN** o Admin tenta vincular um quarto responsável ao mesmo Guerreiro(a)
- **THEN** a aplicação explica o teto de três e o vínculo não é criado

#### Scenario: Adulto sem conta social recebe senha provisória

- **WHEN** o Admin cria credencial de usuário e senha provisória para um adulto cadastrado
- **THEN** a aplicação exibe a senha provisória uma vez, para entrega, e não a recupera depois

### Requirement: A aplicação reúne as filas numa lista só, com filtro por natureza

A App 03 SHALL apresentar as solicitações numa **área Filas** única, com **filtro por
natureza**, e NEVER SHALL abrir uma área separada por natureza. Cada item SHALL mostrar a
natureza a que pertence, quem enviou, a situação e o prazo, e SHALL distinguir visualmente o
que está **em atraso** — por rótulo e não apenas por cor. (`RF-02-18`, `RF-02-65`,
`RF-02-25`, PRD-02 §10, documento 15 §5)

A área SHALL ser aberta apenas por **Admin**; para os demais papéis a aplicação SHALL
apresentar a recusa em linguagem simples, e não um erro cru. (`RN-02-01`, `RF-01-16`)

Nesta fatia a área SHALL servir a natureza **participação**; as demais SHALL entrar sem que a
lista, o filtro ou a apresentação do atraso mudem de forma. (PRD-02 §6.2)

#### Scenario: Admin abre a área Filas

- **WHEN** um Admin em sessão abre a área Filas
- **THEN** vê as solicitações numa lista só, com o filtro por natureza e, em cada item, a
  natureza, quem enviou, a situação e o prazo

#### Scenario: O atraso é anunciado por rótulo, não só por cor

- **WHEN** a lista traz uma solicitação em atraso
- **THEN** ela vem com um rótulo textual que diz isso, legível também sem distinguir cores

#### Scenario: Quem não é Admin lê a recusa, não um erro

- **WHEN** um Mestre em sessão abre a área Filas
- **THEN** a aplicação explica em linguagem simples que a área é do Admin, sem exibir código
  nem mensagem técnica

### Requirement: O Admin avalia a solicitação de participação pela aplicação

A App 03 SHALL oferecer ao Admin o desfecho da solicitação de participação — **aceitar** ou
**recusar** — com o **parecer** informado na própria tela, e SHALL apresentar, depois do
desfecho, a situação final, o parecer, quem avaliou e a data. A recusa SHALL exigir o motivo
no parecer antes de chamar o núcleo. (`RF-02-19`, `RF-02-86`)

A tela SHALL apresentar a identificação, a pretensão, a apresentação, a instituição, os links
declarados e, no pré-cadastro de Apoiador, o **aporte declarado** e o **nick pretendido**.
(`RF-02-18`, `RF-02-83`)

A aplicação SHALL apresentar em linguagem simples a recusa do núcleo por solicitação já
avaliada, e NEVER SHALL oferecer reavaliação de solicitação com desfecho gravado.

#### Scenario: Admin aceita e vê o desfecho registrado

- **WHEN** um Admin aceita uma solicitação informando o parecer
- **THEN** a tela passa a mostrar a situação aceita, o parecer, quem avaliou e a data

#### Scenario: Recusa sem motivo é apontada antes de chamar o núcleo

- **WHEN** um Admin escolhe recusar e confirma com o parecer vazio
- **THEN** a aplicação aponta o campo em falta junto do rótulo dele, e nada é enviado ao núcleo

#### Scenario: Solicitação já avaliada não oferece desfecho

- **WHEN** o Admin abre uma solicitação que já tem desfecho gravado
- **THEN** a tela mostra o desfecho e não oferece aceitar nem recusar

### Requirement: A solicitação aceita abre o cadastro pré-preenchido, sem criar acesso

A App 03 SHALL oferecer, a partir de uma solicitação **aceita**, a abertura do cadastro de
**Mestre** ou de **Apoiador** conforme a pretensão declarada, com os campos **pré-preenchidos**
pelo que a solicitação trouxe. O cadastro SHALL continuar sendo ato explícito do Admin: aceitar
a solicitação NEVER SHALL criar persona, credencial ou acesso por si só. (`RF-02-20`,
`RN-02-03`, `RN-01-28`)

O pré-preenchimento SHALL ser editável pelo Admin antes da confirmação, e o cadastro SHALL
passar pelas mesmas exigências de sempre — entre elas ao menos um artefato comprobatório de
Mestre ou Apoiador. (`RF-02-04`, `RN-02-01`)

#### Scenario: Aceitar não cadastra ninguém

- **WHEN** um Admin aceita uma solicitação de participação
- **THEN** nenhuma persona passa a existir, e a aplicação apenas oferece abrir o cadastro

#### Scenario: O cadastro abre com o que a solicitação trouxe

- **WHEN** o Admin abre o cadastro a partir de uma solicitação aceita com pretensão de Apoiador
- **THEN** o formulário de Apoiador aparece com os dados da solicitação já preenchidos e
  editáveis

#### Scenario: O cadastro pré-preenchido cumpre as mesmas exigências

- **WHEN** o Admin confirma o cadastro pré-preenchido sem nenhum artefato comprobatório
- **THEN** a aplicação aponta a falta e o cadastro não é criado

### Requirement: O Admin homologa pela aplicação o aporte declarado no pré-cadastro

A App 03 SHALL oferecer ao Admin, sobre uma solicitação de participação com **aporte
declarado**, o registro do aporte apontando a solicitação de origem, e SHALL apresentar depois
o valor **em moedas** creditado. A tela NEVER SHALL apresentar o aporte em reais.
(`RF-02-84`, `RF-07-30`, `RN-02-19`, `RN-07-21`, invariante 16 do documento 99 §6)

A aplicação SHALL apresentar em linguagem simples a recusa do núcleo por solicitação **já
homologada**, e SHALL deixar de oferecer a homologação depois que ela ocorreu.

#### Scenario: Admin homologa o aporte declarado

- **WHEN** um Admin registra o aporte apontando a solicitação de participação de origem
- **THEN** a tela passa a mostrar o aporte homologado, com o valor em moedas

#### Scenario: A homologação não se repete

- **WHEN** o Admin abre uma solicitação cujo aporte declarado já foi homologado
- **THEN** a tela mostra a homologação registrada e não oferece homologar de novo

#### Scenario: O aporte aparece em moedas, nunca em reais

- **WHEN** a tela apresenta um aporte homologado
- **THEN** o valor aparece em moedas da plataforma, e nenhum valor em reais é exibido

### Requirement: A área Filas serve as quatro naturezas sob o mesmo filtro

A App 03 SHALL apresentar, na área Filas já existente, também as solicitações de **dados**, as
de **chave** e as **sugestões e propostas**, sob o mesmo filtro por natureza e com a mesma
apresentação do atraso. A aplicação NEVER SHALL abrir área separada para nenhuma delas.
(`RF-02-25`, `RF-02-77`, `RF-02-87`, PRD-02 §6.2)

Cada natureza SHALL mostrar o que lhe é próprio: a de dados, o solicitante, a instituição, a
finalidade declarada e o recorte pedido; a de chave, quem pediu e o que pretende construir; a
sugestão, o autor, a persona dele e o teor. (`RF-02-77`, `RF-02-87`, `RF-02-25`)

#### Scenario: O filtro alcança as quatro naturezas

- **WHEN** um Admin em sessão abre a área Filas e percorre o filtro por natureza
- **THEN** pode ver participação, dados, chave e sugestões, cada uma com os seus campos

#### Scenario: Cada natureza mostra o que lhe é próprio

- **WHEN** o Admin filtra pela natureza dados
- **THEN** cada item traz solicitante, instituição, finalidade declarada e recorte pedido

### Requirement: A tela da solicitação de dados apresenta ao Admin os três critérios

A App 03 SHALL apresentar, na avaliação da solicitação de dados, os **três critérios de
aprovação** — solicitante identificado, finalidade compatível e não reidentificação — e SHALL
exigir do Admin a afirmação do **compromisso de não reidentificação** antes de aprovar. O
parecer SHALL ser obrigatório na aprovação e na recusa, apontado no próprio campo antes de
chamar o núcleo. (`RF-02-93`, `RF-02-78`, `RN-02-26`)

A aplicação SHALL apresentar, depois do desfecho, **o que foi entregue e a quem**, e SHALL
deixar claro que a entrega é **gratuita e anonimizada**. (`RF-02-79`)

#### Scenario: Os critérios aparecem antes da decisão

- **WHEN** um Admin abre uma solicitação de dados para avaliar
- **THEN** a tela apresenta os três critérios de aprovação antes de oferecer aprovar ou recusar

#### Scenario: Aprovar exige afirmar o compromisso

- **WHEN** o Admin escolhe aprovar sem marcar o compromisso de não reidentificação
- **THEN** a aplicação aponta a falta junto do rótulo e nada é enviado ao núcleo

#### Scenario: A entrega registrada aparece na tela

- **WHEN** o Admin abre uma solicitação de dados já aprovada e entregue
- **THEN** a tela mostra o que foi entregue e a quem, e diz que a entrega foi gratuita e
  anonimizada

### Requirement: A aprovação do pedido de chave e a emissão são dois atos na tela

A App 03 SHALL oferecer ao Admin, sobre a solicitação de chave, primeiro o **desfecho** —
aprovar ou recusar, com parecer — e só depois, sobre a solicitação aprovada, a **emissão**. A
aplicação NEVER SHALL emitir a chave no mesmo ato da aprovação. (`RF-02-88`, `RF-02-89`)

A emissão SHALL apresentar o **identificador** e o **segredo**, com o aviso de que o segredo
aparece **uma única vez** e não é recuperável depois. A aplicação NEVER SHALL guardar o segredo
nem reapresentá-lo em consulta posterior. (`RF-02-89`, `RN-02-28`)

A solicitação que já rendeu chave NEVER SHALL oferecer emissão de novo.

#### Scenario: Aprovar não emite

- **WHEN** um Admin aprova uma solicitação de chave
- **THEN** a tela mostra o desfecho gravado e passa a oferecer a emissão como ato seguinte

#### Scenario: O segredo é mostrado uma vez, com o aviso

- **WHEN** o Admin emite a chave
- **THEN** a tela apresenta o identificador e o segredo, avisando que o segredo não será
  mostrado de novo

#### Scenario: O segredo não volta numa consulta posterior

- **WHEN** o Admin volta à mesma solicitação depois de sair da tela de emissão
- **THEN** o segredo não aparece, e a tela mostra apenas que a chave foi emitida

#### Scenario: Solicitação que já rendeu chave não emite outra

- **WHEN** o Admin abre uma solicitação aprovada cuja chave já foi emitida
- **THEN** a tela não oferece emitir de novo

### Requirement: A aplicação apresenta o painel das chaves emitidas

A App 03 SHALL apresentar ao Admin as chaves emitidas com **prazo de apresentação**, **URL
apresentada** quando houver e **situação**, e SHALL **destacar** as que estão com o prazo a
vencer e as **revogadas automaticamente por prazo vencido**. O destaque SHALL ser legível sem
distinguir cores. (`RF-02-90`, `RF-02-91`, `RN-02-29`, documento 15 §5)

A App 03 SHALL oferecer ao Admin a **revogação a qualquer tempo, com motivo**, exigido antes de
chamar o núcleo. (`RF-02-92`)

O painel NEVER SHALL apresentar o segredo nem o seu resumo criptográfico. (`RN-02-28`)

#### Scenario: O painel mostra o ciclo de vida de cada chave

- **WHEN** um Admin em sessão abre o painel de chaves
- **THEN** cada chave aparece com prazo, URL apresentada quando houver e situação

#### Scenario: Prazo a vencer e revogação por decurso são destacados por rótulo

- **WHEN** o painel traz uma chave com prazo a vencer e outra revogada por prazo vencido
- **THEN** as duas vêm com rótulo textual que diz isso, legível também sem distinguir cores

#### Scenario: Revogar exige o motivo

- **WHEN** o Admin escolhe revogar uma chave e confirma sem informar o motivo
- **THEN** a aplicação aponta o campo em falta e nada é enviado ao núcleo

#### Scenario: O painel nunca mostra o segredo

- **WHEN** o painel apresenta qualquer chave
- **THEN** o segredo não aparece em campo algum

### Requirement: O Admin avalia a sugestão e a tela mostra o retorno a quem propôs

A App 03 SHALL oferecer ao Admin o desfecho da sugestão — **adotada** ou **não adotada** —, com
o **motivo do retorno** exigido na não adotada, em linguagem simples, apontado antes de chamar
o núcleo. A tela SHALL apresentar, depois do desfecho, o retorno que chegará a quem propôs.
(`RF-02-26`, `RN-02-25`)

A aplicação SHALL apresentar, na sugestão adotada, que **20 pontos extras e o badge de
protagonismo** foram creditados a quem propôs. (`RF-01-56`, `RN-01-50`)

Todo o retorno SHALL acontecer **dentro da plataforma**: a aplicação NEVER SHALL oferecer envio
por e-mail. (`RN-02-25`)

#### Scenario: Não adotada exige o motivo do retorno

- **WHEN** o Admin escolhe não adotar e confirma sem o motivo do retorno
- **THEN** a aplicação aponta o campo em falta e nada é enviado ao núcleo

#### Scenario: Adotada mostra o que foi creditado

- **WHEN** o Admin adota uma sugestão
- **THEN** a tela mostra que 20 pontos extras e o badge de protagonismo foram creditados a quem
  propôs

#### Scenario: O retorno não sai por e-mail

- **WHEN** o Admin conclui a avaliação de uma sugestão
- **THEN** a aplicação não oferece envio por e-mail, e o retorno fica dentro da plataforma

### Requirement: A App 03 abre a partida sobre a atividade e as equipes da aula

A aplicação SHALL oferecer ao Mestre que conduz — e ao Admin — a abertura da partida de Quiz
ao Vivo a partir da aula em andamento, escolhendo a **atividade de competição ao vivo** sobre
a qual ela corre e as **equipes formadas na App 01** naquele encontro. A tela SHALL apresentar
as equipes por **avatar e nick**, sem dado pessoal algum, e NEVER SHALL exibir imagem real de
Guerreiro(a). Não havendo equipe formada na aula, a aplicação SHALL dizê-lo em uma frase, sem
oferecer a abertura. (`RF-02-59`, `RF-02-61`, PRD-02 §§11, 12)

#### Scenario: O Mestre abre a partida escolhendo atividade e equipes

- **WHEN** o Mestre que conduz escolhe a atividade de competição ao vivo e marca as equipes
  disputantes
- **THEN** a aplicação abre a partida e passa à tela de condução

#### Scenario: As equipes aparecem por avatar e nick

- **WHEN** a tela de abertura lista as equipes da aula
- **THEN** cada integrante aparece por avatar e nick, sem nome, idade ou imagem real

#### Scenario: Aula sem equipe formada não abre partida

- **WHEN** a aula em andamento não tem equipe formada
- **THEN** a aplicação informa em uma frase que não há equipe e não oferece a abertura

### Requirement: A tela de condução governa o ritmo da partida

A aplicação SHALL oferecer a quem conduz, na partida aberta, quatro atos: **pôr uma pergunta
no ar**, escolhida do banco da missão daquela atividade; **liberar o resultado** da pergunta
no ar; **anular** a pergunta contestada; e **encerrar** a partida. Não há tempo por pergunta —
o ritmo é de quem conduz. A tela SHALL mostrar, enquanto o resultado não está liberado,
quantas equipes já responderam, sem revelar o que responderam; liberado, SHALL mostrar a
alternativa correta, as equipes que acertaram e a primeira delas. O encerramento SHALL avisar
que a pontuação será lançada automaticamente às equipes. (`RF-02-60`, `RF-02-62`, `RF-02-72`,
`RF-02-73`, documento 05 §5)

#### Scenario: Quem conduz põe a pergunta no ar

- **WHEN** quem conduz escolhe uma pergunta do banco da missão e dá o _start_
- **THEN** a tela passa a mostrar a pergunta no ar e quantas equipes já responderam

#### Scenario: Antes de liberar, a tela não revela as respostas

- **WHEN** equipes respondem e o resultado ainda não foi liberado
- **THEN** a tela mostra apenas a contagem de quem respondeu, sem a alternativa de ninguém

#### Scenario: Liberado o resultado, a tela mostra quem acertou

- **WHEN** quem conduz libera o resultado da pergunta no ar
- **THEN** a tela mostra a alternativa correta, as equipes que acertaram e qual chegou
  primeiro

#### Scenario: A pergunta contestada é anulada

- **WHEN** quem conduz anula a pergunta contestada
- **THEN** a tela marca a pergunta como anulada e informa que ela não credita ninguém

#### Scenario: O encerramento avisa do lançamento

- **WHEN** quem conduz encerra a partida
- **THEN** a aplicação confirma o encerramento e informa que a pontuação foi lançada às
  equipes

### Requirement: A tela de condução acompanha a partida por sondagem a cada 2 segundos

A aplicação SHALL manter a tela de condução atualizada **sondando o núcleo a cada 2
segundos**, sem recarga manual e sem conexão longa (documento 03 §1, decisão do fundador de
2026-08-25). Sondagem que falha por rede NEVER SHALL derrubar a partida nem apagar o que já
está na tela: a aplicação SHALL avisar que perdeu contato e SHALL retomar o estado corrente na
sondagem seguinte. (`RF-02-60`, PRD-02 §§10, 12)

#### Scenario: A tela acompanha sem recarga

- **WHEN** a partida está aberta e equipes vão respondendo
- **THEN** a contagem na tela avança sozinha, sem que quem conduz recarregue

#### Scenario: A queda de rede não derruba a partida

- **WHEN** uma sondagem falha por rede
- **THEN** a tela avisa que perdeu contato, mantém o que já exibia e volta ao estado corrente
  na sondagem seguinte

### Requirement: O Mestre alcança a condução da partida e nada mais da gestão

A aplicação SHALL permitir ao Mestre autenticado ler o painel e conduzir a partida de quiz da
aula dele, e SHALL apresentar a recusa do núcleo em qualquer outra escrita de gestão. Mestre
que tenta conduzir a partida de uma aula que não é dele SHALL receber a recusa, dita em uma
frase, sem que a tela ofereça caminho alternativo. (`RF-02-49`, `RN-02-20`, PRD-02 §12)

#### Scenario: Mestre conduz a partida da sua aula

- **WHEN** o Mestre autenticado abre a condução da partida da aula dele
- **THEN** a aplicação oferece os quatro atos da condução

#### Scenario: Mestre de outra aula é recusado

- **WHEN** o Mestre tenta conduzir a partida de uma aula que não é dele
- **THEN** a aplicação apresenta a recusa em uma frase e não oferece caminho alternativo

### Requirement: A App 03 abre a área Painel do dia, em leitura

A App 03 SHALL apresentar a área **Painel do dia**, que mostra o encontro em andamento numa tela
só: quem chegou, quem aguarda aparelho, as equipes com a missão de cada uma, a atividade prevista
e os recursos providos, o saldo dos tipos de recurso do ponto de apoio e os lançamentos
pendentes do encontro (`RF-02-41` a `RF-02-47`, `RF-02-69`).

A área SHALL ser de **leitura**: ela NEVER SHALL oferecer botão que lance, que edite equipe ou
que altere presença. Cada pendência listada SHALL levar o operador à tela que já a resolve, e é
lá que a escrita acontece.

Fora da janela de toda aula agendada, a área SHALL dizer em uma frase que não há encontro em
andamento, sem apresentar tela vazia nem erro cru. (`RF-02-41` a `RF-02-47`, `RF-02-69`,
`RN-02-12`, PRD-02 §§6.4, 12)

#### Scenario: A área mostra o encontro em andamento

- **WHEN** um Admin abre o Painel do dia durante a janela de uma aula
- **THEN** a tela apresenta presenças, espera, equipes com missão, previsto e provido, saldo e
  lançamentos pendentes

#### Scenario: Sem encontro, a área explica em uma frase

- **WHEN** o Painel do dia é aberto fora da janela de toda aula agendada
- **THEN** a tela diz que não há encontro em andamento, sem erro cru

#### Scenario: A área não oferece escrita

- **WHEN** o operador procura lançar ou alterar algo pela tela do painel
- **THEN** a tela não oferece caminho de escrita, e leva à tela que resolve aquela pendência

#### Scenario: A tela não exibe imagem real de criança

- **WHEN** o painel apresenta presenças e equipes
- **THEN** cada Guerreiro(a) aparece por nick e avatar, e nenhuma imagem real é exibida

### Requirement: O painel se atualiza sozinho durante o encontro

A App 03 SHALL manter o Painel do dia atualizado **por sondagem**, sem recarga manual, no mesmo
padrão já usado na condução da partida de quiz. O operador NEVER SHALL precisar recarregar a
página para ver quem acabou de chegar ou a equipe que acabou de trocar de missão.

Caindo a rede, a tela SHALL manter legível o que já carregou e SHALL dizer que parou de
atualizar, retomando sozinha quando a rede voltar. (`RF-02-48`, PRD-02 §6.4)

#### Scenario: A chegada aparece sem recarga

- **WHEN** um Guerreiro(a) tem a presença registrada pela App 01 com o painel aberto
- **THEN** ele passa a aparecer no painel sem que ninguém recarregue a página

#### Scenario: A troca de missão aparece sem recarga

- **WHEN** uma equipe declara outra atividade da programação com o painel aberto
- **THEN** o painel passa a mostrá-la na missão nova sem recarga

#### Scenario: Sem rede, a tela avisa e não apaga o que carregou

- **WHEN** a rede cai com o painel aberto
- **THEN** a tela segue legível, diz que parou de atualizar e retoma sozinha quando a rede volta

### Requirement: A gestão anexa a digitalização do termo pela tela do painel

A App 03 SHALL oferecer ao **Admin**, a partir da lista de termos que aguardam digitalização, o
caminho para **anexar a digitalização** do termo de biometria assinado no encontro, em PDF, JPG
ou PNG (`RF-02-68`).

A tela SHALL dizer em linguagem simples a recusa de formato fora dos três e a recusa do termo
que já tem digitalização. O Mestre NEVER SHALL receber o caminho de anexar: ele lê o painel e
não escreve nele (`RN-02-20`). (`RF-02-68`, `RF-02-69`, `RN-02-20`, PRD-02 §§6.3, 6.4)

#### Scenario: O Admin anexa a digitalização a partir da pendência

- **WHEN** um Admin escolhe um termo pendente e envia a digitalização em PDF
- **THEN** a aplicação a anexa e a pendência sai da lista na atualização seguinte

#### Scenario: Formato recusado é explicado

- **WHEN** o Admin envia um arquivo que não é PDF, JPG nem PNG
- **THEN** a tela diz em linguagem simples quais formatos valem, e nada é enviado

#### Scenario: O Mestre não recebe o caminho de anexar

- **WHEN** um Mestre abre o painel com termos aguardando digitalização
- **THEN** a tela lista a pendência e não oferece a ele o caminho de anexar

### Requirement: O Admin encerra o ciclo por uma tela da gestão

A App 03 SHALL oferecer ao Admin a tela do **encerramento do ciclo**, e SHALL exigir
confirmação explícita antes de executá-lo, porque o expurgo do motivo das ocorrências de
conduta não se desfaz. A tela SHALL dizer, antes da confirmação, os dois efeitos do ato — o
expurgo dos motivos guardados e a saída das ocorrências do ranking público — e SHALL deixar
claro que o ciclo seguinte **não** é declarado ali. (`RF-02-99`, `RF-02-100`, `RN-02-30`)

#### Scenario: O ato pede confirmação antes de executar

- **WHEN** o Admin aciona o encerramento do ciclo na App 03
- **THEN** a tela apresenta os dois efeitos do ato e pede confirmação explícita, sem executar
  nada ainda

#### Scenario: Confirmado, o ato é executado e o resultado é exibido

- **WHEN** o Admin confirma o encerramento
- **THEN** a App 03 executa o ato no núcleo e exibe o resultado dele

#### Scenario: Desistir não executa nada

- **WHEN** o Admin desiste diante da confirmação
- **THEN** nenhum motivo é expurgado e nada muda

#### Scenario: A tela não oferece declarar o ciclo seguinte

- **WHEN** a tela do encerramento do ciclo é apresentada
- **THEN** ela não oferece campo, opção nem etapa para declarar o ciclo seguinte
