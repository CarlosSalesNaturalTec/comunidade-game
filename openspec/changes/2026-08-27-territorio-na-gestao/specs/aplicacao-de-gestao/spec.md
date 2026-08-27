## ADDED Requirements

### Requirement: A App 03 abre a área Território sob a comunidade escolhida

A App 03 SHALL abrir a área **Território** ao adulto em sessão, com a **comunidade escolhida
no seletor** que as áreas Pontos de Apoio e Filas já usam, e SHALL apresentar os locais já
cadastrados naquela comunidade **na hierarquia de seis níveis**, cada local sob o seu pai, para
que o Admin saiba o que já há antes de cadastrar. A apresentação SHALL ser **lista densa**, no
temperamento Operação, como a das comunidades e a dos pontos de apoio.

Comunidade **sem local algum** SHALL ser apresentada como comunidade vazia — o estado normal de
quem acabou de nascer (`RN-08-01`) —, e a ausência NEVER SHALL ser apresentada como falha.
(`RF-02-16`, `RF-08-04`, `RF-01-18`, documento 15 §6)

#### Scenario: A área abre com os locais da comunidade escolhida

- **WHEN** o adulto em sessão abre a área Território e escolhe uma comunidade que já tem locais
- **THEN** a aplicação apresenta os locais daquela comunidade, cada um sob o local pai dele

#### Scenario: Trocar a comunidade troca a hierarquia apresentada

- **WHEN** o adulto troca a comunidade no seletor
- **THEN** a aplicação passa a apresentar os locais da comunidade escolhida, e nenhum local de
  outra comunidade aparece na lista

#### Scenario: Comunidade sem local não é apresentada como falha

- **WHEN** a comunidade escolhida ainda não tem local algum cadastrado
- **THEN** a aplicação informa que a comunidade está sem locais, como informação, e não como
  aviso de erro

### Requirement: O Admin cadastra o local do território pela aplicação

A App 03 SHALL permitir ao **Admin** cadastrar local informando **nível**, **rótulo** e **local
pai**, dentro da comunidade escolhida. O nível SHALL ser escolhido entre os seis da hierarquia,
e o local pai SHALL ser escolhido **entre os locais já cadastrados** daquela comunidade — a
aplicação NEVER SHALL pedir que o Admin digite um identificador. O nível `comunidade` SHALL ser
o único que dispensa o pai.

A recusa do núcleo — pai de nível que não é o imediatamente acima, pai de outra comunidade, ou
nível fora dos seis — SHALL ser apresentada **em linguagem simples**, no campo que a originou,
e o caminho de cadastro NEVER SHALL ser oferecido a quem não é Admin. (`RF-02-16`, `RF-08-04`,
`RN-08-18`, documento 15 §6)

#### Scenario: Admin cadastra o local sob o pai escolhido

- **WHEN** um Admin em sessão informa nível `rua`, um rótulo e um local pai de nível `bairro`
  da mesma comunidade, e confirma
- **THEN** o local passa a existir e a aplicação o apresenta na hierarquia, sob aquele pai

#### Scenario: O nível `comunidade` é o único oferecido sem pai

- **WHEN** o Admin escolhe o nível `comunidade` no formulário
- **THEN** a aplicação não exige local pai; escolhido qualquer outro nível, ela o exige antes
  de deixar confirmar

#### Scenario: A recusa da hierarquia é apresentada no campo

- **WHEN** o núcleo recusa o cadastro por hierarquia inválida
- **THEN** a aplicação apresenta a recusa em linguagem simples, no campo que a originou, e
  nenhum local passa a existir

#### Scenario: Quem não é Admin não alcança o cadastro

- **WHEN** um Mestre em sessão abre a área Território
- **THEN** o caminho de cadastro de local não lhe é oferecido

### Requirement: A área Território alerta enquanto houver solicitação de local em aberto

A App 03 SHALL apresentar as **solicitações de novo local em aberto** da comunidade escolhida, e
SHALL **alertar enquanto houver ao menos uma sem desfecho**, para que a fila não fique
esquecida. Cada solicitação SHALL aparecer com **quem pediu**, o **nível pretendido**, o
**rótulo**, a **justificativa** e o **desafio de coleta de origem**.

O alerta SHALL desaparecer quando a última solicitação da comunidade receber desfecho, e a
solicitação já avaliada NEVER SHALL continuar na fila. A solicitação de local NEVER SHALL
aparecer na área Filas: ela não é uma das quatro naturezas daquela fila e não tem prazo de 7
dias. Quem pediu SHALL ser apresentado por **nick e avatar**, nunca por imagem real.
(`RF-02-21`, `RF-08-24`, `RN-02-22`, documento 99 §6 invariante 12)

#### Scenario: A fila alerta enquanto há solicitação sem desfecho

- **WHEN** o adulto abre a área Território de uma comunidade com solicitações em aberto
- **THEN** a aplicação alerta que há solicitação aguardando e apresenta cada uma com
  solicitante, nível pretendido, rótulo, justificativa e desafio de origem

#### Scenario: O alerta cessa quando a fila esvazia

- **WHEN** a última solicitação em aberto da comunidade recebe desfecho
- **THEN** o alerta deixa de aparecer e a fila é apresentada vazia

#### Scenario: A solicitação de local não aparece na área Filas

- **WHEN** o adulto abre a área Filas com solicitações de local em aberto
- **THEN** nenhuma delas aparece ali, e nenhuma é apresentada como em atraso

#### Scenario: O solicitante aparece por nick e avatar

- **WHEN** a fila apresenta uma solicitação
- **THEN** o Guerreiro(a) que a abriu aparece por nick e avatar, e nenhuma imagem real dele é
  exibida

### Requirement: O Admin aprova a solicitação informando o local pai, ou recusa com motivo

A App 03 SHALL permitir ao **Admin** dar o desfecho da solicitação de novo local em dois
caminhos: **aprovar**, informando o **local pai** escolhido entre os locais já cadastrados da
comunidade, o que **cria o local**; ou **recusar**, informando o **motivo**, sem criar local
algum. A aplicação NEVER SHALL deixar confirmar a recusa sem motivo.

A recusa do núcleo por hierarquia inválida SHALL ser apresentada em linguagem simples, e a
solicitação SHALL continuar na fila, em aberto. Solicitação já avaliada NEVER SHALL receber
segundo desfecho pela aplicação. Aprovada, o local criado SHALL aparecer na hierarquia da área
sem que o adulto precise recarregar a tela. (`RF-02-22`, `RF-08-23`, `RF-08-04`, `RN-08-18`)

#### Scenario: A aprovação cria o local e ele aparece na hierarquia

- **WHEN** um Admin aprova a solicitação informando o local pai
- **THEN** o local passa a existir, a solicitação sai da fila e o local aparece na hierarquia
  apresentada

#### Scenario: A recusa exige motivo

- **WHEN** o Admin tenta confirmar a recusa sem escrever o motivo
- **THEN** a aplicação aponta o motivo em falta e nenhum desfecho é registrado

#### Scenario: Recusa com motivo não cria local

- **WHEN** o Admin recusa a solicitação com motivo
- **THEN** a solicitação sai da fila como recusada e nenhum local passa a existir

#### Scenario: A hierarquia inválida devolve a solicitação à fila

- **WHEN** o núcleo recusa a aprovação por local pai de nível ou comunidade inválidos
- **THEN** a aplicação apresenta a recusa em linguagem simples e a solicitação continua na
  fila, em aberto

### Requirement: A área Território apresenta os desafios de coleta publicados, em leitura

A App 03 SHALL apresentar ao adulto em sessão os **desafios de coleta de trilha publicada**,
cada um com o **tipo de coleta**, a **cadência**, a **vigência** e a **quantidade de séries
ativas**. A apresentação SHALL ser **em leitura**: a aplicação NEVER SHALL oferecer caminho de
criar, editar ou apagar desafio de coleta, que é autoria do Mestre na App 09 (PRD-02 §3.2).

Desafio de trilha ainda em rascunho NEVER SHALL aparecer, e desafio sem série aberta SHALL
aparecer com zero séries ativas, como informação e não como falha. (`RF-02-17`, `RF-08-06`,
documento 15 §6)

#### Scenario: O adulto lê os desafios publicados com o que a fatia exige

- **WHEN** o adulto abre a área Território
- **THEN** a aplicação apresenta os desafios de coleta de trilha publicada, cada um com tipo,
  cadência, vigência e quantidade de séries ativas

#### Scenario: Desafio de trilha em rascunho não aparece

- **WHEN** há desafio de coleta numa missão de trilha ainda em rascunho
- **THEN** ele não aparece na lista

#### Scenario: A leitura não oferece escrita

- **WHEN** o adulto abre a lista dos desafios de coleta
- **THEN** nenhum caminho de criar, editar ou apagar desafio lhe é oferecido

#### Scenario: Desafio sem série não é apresentado como falha

- **WHEN** um desafio publicado ainda não tem série aberta
- **THEN** ele aparece com zero séries ativas, como informação, e não como aviso de erro

### Requirement: A lista de Guerreiros e Guerreiras mostra o vínculo, sem caminho de troca

A App 03 SHALL apresentar, na lista de Guerreiros e Guerreiras da área Personas, a **comunidade
do vínculo vigente** de cada um e a **data de início** desse vínculo, para que o Admin **confira**
o que a aula agendada atribuiu. A apresentação SHALL ser em **leitura**.

A aplicação NEVER SHALL oferecer caminho de mudar a comunidade do Guerreiro(a): no Ciclo 01 não
há transferência, e o histórico existe apenas no modelo. Guerreiro(a) ainda **sem vínculo
vigente** SHALL aparecer com a ausência informada em linguagem simples, e a lista NEVER SHALL
exibir imagem real de Guerreiro(a). (`RF-02-15`, `RN-02-06`, `RN-02-22`, `RF-08-02`, `RF-08-03`,
documento 99 §6 invariantes 4 e 12)

#### Scenario: A lista apresenta a comunidade herdada da aula

- **WHEN** o Admin abre a lista de Guerreiros e Guerreiras
- **THEN** cada um aparece com a comunidade do vínculo vigente e a data de início dele

#### Scenario: Não existe tela de transferência de comunidade

- **WHEN** o Admin procura, na lista ou na edição do Guerreiro(a), um caminho para mudar a
  comunidade dele
- **THEN** nenhum lhe é oferecido em lugar algum da aplicação

#### Scenario: Guerreiro(a) sem vínculo vigente é informado, não acusado

- **WHEN** a lista alcança um Guerreiro(a) sem vínculo vigente
- **THEN** a ausência aparece em linguagem simples, como informação, e não como aviso de erro
