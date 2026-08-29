## Purpose

A App 08 é o canal de quem sustenta o projeto. Esta capacidade cobre como o Apoiador entra na
aplicação, a trava que a senha provisória impõe, o que a aplicação nunca oferece a quem não tem
cadastro — e, nesta fatia, a proposição e o acompanhamento do desafio extra.

## Requirements

### Requirement: A Área do Apoiador é autenticada e se identifica por chave

A App 08 SHALL apresentar a chave de aplicação dela em toda chamada ao núcleo e NEVER SHALL
expor tela do Apoiador a quem não tem sessão aberta. (`RF-01-02`, `RN-01-32`, PRD-14 §4)

#### Scenario: Quem não tem sessão vê a entrada

- **WHEN** alguém sem sessão aberta abre qualquer endereço da App 08
- **THEN** a aplicação apresenta a entrada e nenhuma tela do Apoiador

### Requirement: O Apoiador entra por login social ou por usuário e senha

A App 08 SHALL oferecer os dois caminhos de entrada do adulto — **login social** e **usuário e
senha** criados pela gestão — e SHALL abrir a sessão com o papel que a persona já tem.
(`RF-14-08`, PRD-14 §5.2)

#### Scenario: Entrada por login social abre a sessão

- **WHEN** um Apoiador cadastrado autentica por login social
- **THEN** a aplicação abre a sessão dele e apresenta a área autenticada

#### Scenario: Entrada por usuário e senha abre a sessão

- **WHEN** um Apoiador cadastrado autentica pela credencial de usuário e senha criada pela
  gestão
- **THEN** a aplicação abre a sessão dele e apresenta a área autenticada

### Requirement: A senha provisória tranca todas as demais telas

A App 08 SHALL exigir a **troca da senha provisória** antes de apresentar qualquer outra tela ao
Apoiador que entrou com ela, e NEVER SHALL oferecer caminho de contorno. (`RF-14-09`, PRD-14
§§5.2, 12)

#### Scenario: Entrada com senha provisória leva à troca

- **WHEN** um Apoiador entra com senha provisória
- **THEN** a aplicação apresenta a troca de senha e nenhuma outra tela

#### Scenario: Trocada a senha, a área abre

- **WHEN** o Apoiador troca a senha provisória
- **THEN** a aplicação apresenta a área autenticada

### Requirement: Login não cria cadastro, e a recusa orienta o pré-cadastro

A App 08 SHALL recusar a entrada de conta que não corresponda a persona cadastrada, NEVER SHALL
criar cadastro a partir dela, e SHALL apresentar a orientação de usar o **pré-cadastro** da
porta pública. (`RF-14-10`, `RN-14-02`, PRD-14 §12)

#### Scenario: Conta sem cadastro é recusada com orientação

- **WHEN** alguém autentica por login social com conta que não corresponde a persona cadastrada
- **THEN** a aplicação recusa a entrada, orienta usar o pré-cadastro e nenhum cadastro passa a
  existir

### Requirement: A aplicação não oferece convite, delegação nem segundo acesso

A App 08 NEVER SHALL apresentar tela ou caminho de convite, de delegação ou de criação de um
segundo acesso ao mesmo cadastro: no Ciclo 01 é **um usuário por cadastro**, inclusive no
institucional. (`RF-14-11`, `RN-14-04`)

#### Scenario: Não há caminho para um segundo usuário

- **WHEN** um Apoiador percorre as telas da aplicação
- **THEN** nenhuma delas oferece convidar outra pessoa, delegar o acesso ou criar um segundo
  usuário para o cadastro

### Requirement: O Apoiador propõe o desafio extra pela aplicação

A App 08 SHALL oferecer ao Apoiador a proposição do desafio extra sobre uma **trilha em
andamento**, declarando recompensa, quantidade disponível, critério de atribuição, vigência,
**modalidade**, **pontos extras**, **formato** e **custeio**; no direcionado, o **nick do
destinatário** e a **justificativa do vínculo**. A tela NEVER SHALL confirmar se o nick
informado existe, e NEVER SHALL exibir dado algum do destinatário. (`RF-14-29` a `RF-14-33`,
`RF-14-74` a `RF-14-76`)

#### Scenario: Proposta direcionada com nick desconhecido é aceita na tela

- **WHEN** o Apoiador envia uma proposta direcionada com um nick que não existe
- **THEN** a tela aceita o envio como qualquer outro, sem indicar que o nick não existe

#### Scenario: A tela recusa pontos extras acima do teto

- **WHEN** o Apoiador declara mais de 10 pontos extras
- **THEN** a tela recusa o envio e informa o teto de 10

### Requirement: A tela mostra o lastro que falta prover

A App 08 SHALL exibir, no desafio cujo lastro da recompensa não está provido, **o que falta
prover** e que sem isso ele não é publicado. (`RF-14-34`, PRD-14 §12)

#### Scenario: Desafio sem lastro mostra o que falta

- **WHEN** o Apoiador abre um desafio que propôs sem lastro provido
- **THEN** a tela mostra o que falta prover e que sem isso o desafio não é publicado

### Requirement: O Apoiador acompanha o estado do desafio e a quantidade restante

A App 08 SHALL exibir, para cada desafio proposto, o **estado** no fluxo — validação do Mestre,
aprovação do Admin, publicado ou recusado —, o **motivo** da recusa em linguagem simples e, no
publicado, a **quantidade de recompensas restante**. A aplicação NEVER SHALL oferecer edição de
desafio publicado: a correção é proposta nova. (`RF-14-35` a `RF-14-38`, PRD-14 §12)

#### Scenario: Desafio recusado aparece com o motivo

- **WHEN** o Mestre recusa um desafio na validação
- **THEN** a tela do proponente mostra o desafio como recusado, com o motivo em linguagem
  simples

#### Scenario: Desafio publicado não oferece edição

- **WHEN** o Apoiador abre um desafio publicado
- **THEN** a tela mostra a quantidade restante e não oferece edição, indicando que a correção é
  propor de novo

### Requirement: Nenhuma tela de desafio identifica Guerreiro(a) nem abre canal

Nenhuma tela de desafio da App 08 SHALL exibir nome real, contato ou dado de identificação de
Guerreiro(a), e NEVER SHALL oferecer campo de mensagem, telefone ou e-mail de Guerreiro(a),
família ou Mestre. (`RF-14-39`, `RN-14-20`, PRD-14 §12)

#### Scenario: A tela do desafio não traz identificação nem canal

- **WHEN** o Apoiador percorre as telas de proposição e de acompanhamento do desafio
- **THEN** nenhuma delas exibe nome real ou contato de Guerreiro(a), nem oferece campo de
  mensagem
