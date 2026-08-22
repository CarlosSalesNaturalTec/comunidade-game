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
