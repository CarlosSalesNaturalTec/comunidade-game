## Purpose

A App 08 é o canal de quem sustenta o projeto. Esta capacidade cobre como o Apoiador entra na
aplicação, a trava que a senha provisória impõe, o que a aplicação nunca oferece a quem não tem
cadastro — e, nesta fatia, a proposição e o acompanhamento do desafio extra.

## Requirements

### Requirement: A Área do Apoiador é autenticada e se identifica por chave

A App 08 SHALL apresentar a chave de aplicação dela em toda chamada ao núcleo, inclusive nas
chamadas públicas da porta de pré-cadastro, e NEVER SHALL expor tela do Apoiador a quem não tem
sessão aberta. Sem sessão, a aplicação SHALL apresentar apenas a **porta pública** — o
pré-cadastro — e a entrada de quem já tem cadastro. (`RF-01-02`, `RN-01-32`, `RF-14-01`,
PRD-14 §§4, 5.1)

#### Scenario: Quem não tem sessão vê a entrada

- **WHEN** alguém sem sessão aberta abre qualquer endereço da App 08
- **THEN** a aplicação apresenta a porta pública e o caminho de entrada, e nenhuma tela do
  Apoiador

### Requirement: A porta pública identifica sem documento e com perfil declarado

A porta pública da App 08 SHALL identificar quem se pré-cadastra por **nome ou razão social**,
**e-mail**, **WhatsApp**, **nick** pretendido e **perfil declarado** — pessoa física ou pessoa
jurídica — e NEVER SHALL pedir CPF, CNPJ ou documento de identidade. O perfil SHALL ser
declarado e não verificado, e SHALL definir apenas a escada de valores sugeridos que a tela
exibe. O núcleo SHALL guardar o perfil na solicitação. (`RF-14-01`, `RN-14-03`, `RN-14-39`,
PRD-14 §§5.1, 11)

#### Scenario: A porta pede identificação sem documento

- **WHEN** um visitante abre a porta pública
- **THEN** a tela pede nome ou razão social, e-mail, WhatsApp, nick e perfil, e não oferece
  campo de CPF, CNPJ ou documento de identidade

#### Scenario: O perfil declarado troca a escada exibida

- **WHEN** o visitante declara o perfil de pessoa física e depois o de pessoa jurídica
- **THEN** a tela exibe a escada de valores sugeridos correspondente a cada perfil, sem
  verificar nem exigir prova do perfil

#### Scenario: O perfil declarado chega ao núcleo com a solicitação

- **WHEN** o pré-cadastro é enviado com o perfil declarado
- **THEN** o núcleo guarda o perfil junto da solicitação de participação, para a gestão ler

### Requirement: A porta pública oferece as formas de declarar o aporte, sempre com o equivalente em moedas

A porta pública SHALL oferecer, a quem aporta em dinheiro, a **necessidade publicada**, o
**valor sugerido** da escada do perfil declarado e o **valor livre**, e SHALL exibir o
**equivalente em moedas** ao lado de cada valor, na mesma tela. O degrau da escada SHALL ser
sugestão e não piso: o valor livre SHALL aceitar qualquer quantia, com fração de duas casas.
(`RF-14-02`, `RF-14-03`, `RN-14-40`, PRD-14 §§5.1, 12)

#### Scenario: O visitante assume uma necessidade publicada

- **WHEN** o visitante escolhe uma das necessidades de recurso em aberto
- **THEN** a tela declara o aporte por aquela necessidade, com o que ela pede em moedas

#### Scenario: A escada do perfil aparece com o equivalente em moedas

- **WHEN** o visitante declara o perfil e vê os valores sugeridos
- **THEN** cada degrau aparece com o equivalente em moedas ao lado

#### Scenario: O valor livre aceita qualquer quantia

- **WHEN** o visitante informa um valor livre abaixo do menor degrau da sua escada, com fração
  de duas casas
- **THEN** a tela aceita o valor e exibe o equivalente em moedas antes do envio

### Requirement: O pré-cadastro exige comprovante em PDF, JPG ou PNG

A porta pública SHALL exigir o **anexo do comprovante** da transferência para enviar o
pré-cadastro e SHALL declarar os formatos aceitos — PDF, JPG ou PNG. Recusado o formato pelo
núcleo, a tela SHALL apresentar a recusa com os formatos válidos. A porta NEVER SHALL aceitar
aporte em material, serviço ou divulgação. (`RF-14-04`, `RN-14-05`, `RN-14-06`, PRD-14 §§9, 12)

#### Scenario: Sem comprovante o pré-cadastro não é enviado

- **WHEN** o visitante tenta enviar o pré-cadastro sem anexar comprovante
- **THEN** a tela recusa o envio e diz quais formatos valem

#### Scenario: Formato não aceito volta com os formatos válidos

- **WHEN** o núcleo recusa o comprovante por formato não aceito
- **THEN** a tela apresenta a recusa com a lista de formatos válidos, e o pré-cadastro não é
  registrado

### Requirement: A porta declara que o pré-cadastro não cria cadastro nem acesso

A porta pública SHALL declarar, **antes do envio**, que o pré-cadastro não cria cadastro nem
acesso, que um Admin vai conferir o comprovante e que a plataforma não emite recibo — quem
precisar de um o pede à pessoa jurídica vinculada, fora da plataforma. Enviado o pré-cadastro,
a aplicação SHALL confirmar que o pedido entrou na fila da gestão e NEVER SHALL abrir sessão,
área autenticada ou qualquer acesso a partir dele. (`RF-14-05`, `RN-14-01`, PRD-14 §§3.2, 5.1,
12)

#### Scenario: A declaração aparece antes do envio

- **WHEN** o visitante chega ao ponto de enviar o pré-cadastro
- **THEN** a tela declara que aquilo não cria cadastro nem acesso, que um Admin confere o
  comprovante e que a plataforma não emite recibo

#### Scenario: Enviado o pré-cadastro, nenhuma tela de Apoiador abre

- **WHEN** o pré-cadastro é enviado com sucesso
- **THEN** a aplicação confirma que o pedido entrou na fila da gestão e continua sem sessão,
  apresentando a porta pública e a entrada

### Requirement: A repetição da mesma origem mostra o tempo de espera

Recusado o envio pelo freio por origem do núcleo, a porta pública SHALL apresentar o **tempo de
espera em linguagem simples** e SHALL preservar o que o visitante já preencheu. A porta NEVER
SHALL opor CAPTCHA nem bloqueio definitivo a quem repete o envio. (`RF-14-06`, PRD-14 §§9, 12)

#### Scenario: Envio repetido volta com o tempo de espera

- **WHEN** o núcleo recusa o envio por excesso de tentativas da mesma origem
- **THEN** a tela apresenta o tempo de espera em linguagem simples, sem CAPTCHA e sem bloqueio
  definitivo, e o que foi preenchido continua na tela

### Requirement: Quem apoia sem transferir dinheiro é encaminhado ao formulário da vitrine

A porta pública SHALL encaminhar ao **formulário de solicitação de participação da vitrine**
quem quer apoiar em material, serviço ou divulgação, e NEVER SHALL registrar esse apoio como
aporte declarado. Sem endereço do formulário configurado, a tela SHALL explicar o caminho em
texto, sem oferecer link. (`RF-14-07`, `RN-14-05`, PRD-14 §§3.2, 5.1)

#### Scenario: Apoio sem dinheiro sai da porta para a vitrine

- **WHEN** o visitante declara que quer apoiar com material, serviço ou divulgação
- **THEN** a porta o encaminha ao formulário da vitrine e não abre a declaração de aporte

#### Scenario: Sem endereço configurado, a tela explica o caminho

- **WHEN** o endereço do formulário da vitrine não está configurado no ambiente
- **THEN** a tela explica em texto por onde esse apoio entra, sem link quebrado

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
