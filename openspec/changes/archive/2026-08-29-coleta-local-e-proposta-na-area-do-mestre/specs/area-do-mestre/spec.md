## ADDED Requirements

### Requirement: O Mestre declara o desafio de coleta da missão

A App 09 SHALL oferecer ao Mestre autor, dentro de cada missão da sua trilha, a declaração do
**desafio de coleta**, com os cinco atributos que o núcleo exige: o **tipo** escolhido no
catálogo de tipos de coleta, a **cadência** — diária, semanal ou mensal —, a **vigência** com
início e fim, a **granularidade exigida** entre os seis níveis do território e **quantos
registros do mesmo período de cadência pontuam**. (`RF-09-27`, `RF-09-28`)

O tipo SHALL ser **escolhido** na lista lida do catálogo, e a aplicação NEVER SHALL oferecer a
criação de tipo novo nem a escolha de tipo desativado — o catálogo é cadastro de Admin. A
aplicação SHALL apresentar, junto do tipo escolhido, a **forma de registro** e a **unidade**
quando houver, para que o Mestre saiba o que o Guerreiro(a) vai medir.

Recusada a declaração pelo núcleo — cadência fora das três, vigência com fim antes do início,
quantidade menor que 1, campo em falta ou tipo desativado —, a aplicação SHALL apresentar o que
está errado em **linguagem simples**, apontando o campo, e NEVER SHALL apresentar código de erro
nem mensagem técnica. (`RN-09-16`)

#### Scenario: O Mestre declara o desafio completo

- **WHEN** o Mestre autor escolhe um tipo do catálogo e declara cadência semanal, vigência,
  granularidade `rua` e um registro que pontua por período
- **THEN** a aplicação grava o desafio na missão e o apresenta entre os desafios dela

#### Scenario: O tipo vem do catálogo, e a aplicação não cria nenhum

- **WHEN** o Mestre abre a declaração do desafio de coleta
- **THEN** a aplicação apresenta os tipos ativos do catálogo para escolha, e nenhuma ação de
  criar tipo novo

#### Scenario: O tipo escolhido mostra o que se mede

- **WHEN** o Mestre escolhe um tipo cuja forma de registro é número
- **THEN** a aplicação apresenta a unidade daquele tipo junto do nome

#### Scenario: A recusa do núcleo vira mensagem simples

- **WHEN** o Mestre declara vigência cujo fim precede o início e o núcleo recusa
- **THEN** a aplicação apresenta em linguagem simples que a data de fim tem de vir depois da de
  início, apontando o campo, sem código de erro

#### Scenario: A declaração não é oferecida em trilha alheia

- **WHEN** um Mestre abre uma missão de trilha de que não é autor
- **THEN** a aplicação não oferece a declaração do desafio de coleta

### Requirement: A App 09 apresenta os desafios de coleta já declarados na trilha

A App 09 SHALL apresentar, em cada missão da trilha do Mestre autor, os **desafios de coleta já
declarados**, com tipo, cadência, vigência, granularidade exigida e quantos registros do período
pontuam — inclusive na trilha em **rascunho**, que é onde eles nascem. Missão sem desafio SHALL
ser apresentada como tal, sem erro. (`RF-09-27`, `RF-09-28`)

A aplicação NEVER SHALL oferecer a declaração da **etiqueta ODS no desafio**: ela é herdada da
missão, ou da trilha na falta dela, e o núcleo recusa desafio que a declare. (`RN-09-36`)

#### Scenario: A trilha em rascunho mostra o desafio declarado

- **WHEN** o Mestre abre uma trilha em rascunho em que já declarou um desafio de coleta
- **THEN** a aplicação apresenta o desafio na missão a que ele pertence

#### Scenario: Missão sem desafio é apresentada como tal

- **WHEN** o Mestre abre uma missão que ainda não tem desafio de coleta
- **THEN** a aplicação apresenta que não há desafio declarado, e oferece declarar um

#### Scenario: O formulário do desafio não declara etiqueta ODS

- **WHEN** o Mestre abre a declaração do desafio de coleta
- **THEN** nenhum campo de etiqueta ODS é apresentado, porque a etiqueta é herdada

### Requirement: O Mestre avalia a solicitação de novo local dos desafios das suas trilhas

A App 09 SHALL apresentar ao Mestre as **solicitações de novo local em aberto** dos desafios das
**suas** trilhas, cada uma com o nível pretendido, o rótulo, a justificativa e o desafio de
origem, e SHALL oferecer **aprovar** ou **recusar** cada uma. A aprovação SHALL exigir o **local
pai** dentro da hierarquia da comunidade da solicitação; a recusa SHALL exigir o **motivo**, sem
o qual a aplicação NEVER SHALL enviá-la. (`RF-09-53`)

A aplicação NEVER SHALL apresentar solicitação de desafio de trilha de outro Mestre — o recorte
é do núcleo, e a tela não o alarga —, e NEVER SHALL oferecer o **cadastro direto de local** nem
a criação de Comunidade Virtual, que seguem privativos de Admin (PRD-09 §3.2). A solicitação já
avaliada SHALL sair da lista.

Recusada a avaliação pelo núcleo — hierarquia inválida, recusa sem motivo ou solicitação já
avaliada —, a aplicação SHALL apresentar o que está errado em linguagem simples, e a solicitação
SHALL continuar em aberto na tela. (`RN-09-16`)

#### Scenario: O Mestre aprova a solicitação informando o local pai

- **WHEN** o Mestre aprova uma solicitação de novo local escolhendo o local pai na hierarquia da
  comunidade
- **THEN** a aplicação apresenta a solicitação como aprovada e ela sai da lista das em aberto

#### Scenario: A recusa exige o motivo antes de enviar

- **WHEN** o Mestre recusa uma solicitação sem escrever o motivo
- **THEN** a aplicação não envia a recusa e pede o motivo

#### Scenario: A tela não alcança solicitação de trilha alheia

- **WHEN** há solicitações de desafios de trilhas de outro Mestre na mesma comunidade
- **THEN** a aplicação não as apresenta

#### Scenario: A App 09 não cadastra local nem comunidade

- **WHEN** o Mestre abre a área de território
- **THEN** nenhuma ação de cadastrar local diretamente ou de criar Comunidade Virtual é oferecida

#### Scenario: A hierarquia inválida vira mensagem simples

- **WHEN** o Mestre aprova informando local pai de nível que não é o imediatamente acima e o
  núcleo recusa
- **THEN** a aplicação apresenta em linguagem simples que o local pai precisa ser do nível acima,
  e a solicitação continua em aberto

### Requirement: A App 09 alerta enquanto houver solicitação de local sem desfecho

A App 09 SHALL apresentar **alerta** enquanto houver ao menos uma solicitação de novo local dos
desafios das trilhas do Mestre **sem desfecho**, visível fora da área de território, para que ele
não precise entrar nela para saber que há pedido parado. O alerta SHALL desaparecer quando a
última solicitação em aberto for aprovada ou recusada. (`RF-09-54`)

O alerta SHALL alcançar **todas as comunidades** em que há solicitação em aberto das trilhas do
Mestre, e NEVER SHALL depender de o Mestre escolher uma comunidade antes: a trilha é bem comum da
plataforma e alcança todas elas. (`RN-01-42`)

#### Scenario: O alerta aparece enquanto há pedido parado

- **WHEN** existe solicitação de novo local em aberto num desafio de trilha do Mestre
- **THEN** a aplicação apresenta o alerta fora da área de território

#### Scenario: O alerta some quando a última é tratada

- **WHEN** o Mestre trata a última solicitação em aberto
- **THEN** o alerta deixa de ser apresentado

#### Scenario: O alerta não depende de escolher comunidade

- **WHEN** o Mestre entra na aplicação e há solicitação em aberto em comunidade que ele não
  selecionou
- **THEN** o alerta é apresentado assim mesmo

#### Scenario: Solicitação de trilha alheia não gera alerta

- **WHEN** a única solicitação em aberto é de um desafio de trilha de outro Mestre
- **THEN** nenhum alerta é apresentado ao Mestre

### Requirement: O Mestre registra a proposta de evolução e acompanha o status

A App 09 SHALL oferecer ao Mestre o registro de **proposta de evolução da plataforma**, em
**texto**, na fila única da gestão, e SHALL apresentar as propostas que ele registrou com a
**situação**, o **prazo** e, concluídas, o **desfecho** — e, na não adotada, o **motivo do
retorno em linguagem simples**. (`RF-09-55`)

A aplicação NEVER SHALL oferecer envio de **áudio**, e NEVER SHALL apresentar proposta de outra
persona. O retorno SHALL ser lido **dentro da aplicação**: nenhuma notificação por e-mail é
construída. (`RN-09-23`)

A aplicação NEVER SHALL oferecer ao Mestre avaliar proposta alguma, a sua inclusive — a avaliação
é ato de Admin, na App 03 (PRD-09 §3.2).

#### Scenario: O Mestre registra a proposta em texto

- **WHEN** o Mestre escreve uma proposta de evolução da plataforma e a envia
- **THEN** a aplicação apresenta a proposta registrada, com a situação recebida e o prazo

#### Scenario: A aplicação não oferece áudio

- **WHEN** o Mestre abre o registro da proposta
- **THEN** nenhum campo ou botão de gravação de áudio é apresentado

#### Scenario: O Mestre acompanha o desfecho na própria aplicação

- **WHEN** uma proposta do Mestre é concluída como não adotada
- **THEN** a aplicação apresenta a situação e o motivo do retorno em linguagem simples, sem que
  nenhum e-mail seja enviado

#### Scenario: A lista não mostra proposta de outra persona

- **WHEN** há propostas de outros Mestres e de Guerreiros e Guerreiras na fila única
- **THEN** a aplicação apresenta apenas as do Mestre em sessão

#### Scenario: A avaliação não é oferecida ao Mestre

- **WHEN** o Mestre abre uma proposta que registrou
- **THEN** nenhuma ação de adotar ou não adotar é apresentada
