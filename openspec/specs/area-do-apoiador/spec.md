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

A porta pública SHALL oferecer, a quem aporta em dinheiro, a **missão aberta**, a
**necessidade publicada**, o **valor sugerido** da escada do perfil declarado e o **valor
livre**, e SHALL exibir o **equivalente em moedas** ao lado de cada valor, na mesma tela. O
degrau da escada SHALL ser sugestão e não piso: o valor livre SHALL aceitar qualquer quantia,
com fração de duas casas. (`RF-14-02`, `RF-14-03`, `RN-14-40`, PRD-14 §§5.1, 12)

#### Scenario: O visitante assume uma missão aberta

- **WHEN** o visitante escolhe uma das missões abertas
- **THEN** a tela declara o aporte por aquela missão, com o que ela pede em moedas

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

### Requirement: A tela de identidade pública define nick e avatar

A App 08 SHALL apresentar ao Apoiador em sessão a tela de **identidade pública**, em que ele
define ou troca o **nick** e o **avatar** que aparecem no card, a qualquer tempo. Vindo o nick do
pré-cadastro, a tela NEVER SHALL pedi-lo de novo no primeiro acesso, e SHALL apresentá-lo já
preenchido. Recusado o nick por já estar em uso, a tela SHALL apresentar as **sugestões de
variação** que o núcleo devolve, e NEVER SHALL revelar de quem é o nick em uso. (`RF-14-12`,
`RF-14-13`, `RF-14-17`, `RN-14-10`, PRD-14 §§5.2, 12)

#### Scenario: O nick do pré-cadastro não é pedido de novo

- **WHEN** um Apoiador cujo cadastro nasceu com nick abre a identidade pública no primeiro acesso
- **THEN** a tela apresenta o nick que ele já tem, para trocar se quiser, e não o pede como se
  não existisse

#### Scenario: Nick já usado volta com sugestões

- **WHEN** o Apoiador tenta gravar um nick já usado por outro adulto
- **THEN** a tela recusa a gravação e apresenta as sugestões de variação, sem dizer de quem é o
  nick

#### Scenario: A troca vale a qualquer tempo

- **WHEN** um Apoiador que já tem nick e avatar troca os dois
- **THEN** a tela grava a troca e passa a apresentar os novos no card

### Requirement: Abaixo do piso a tela mostra o avatar padrão e quanto falta

Abaixo de **10 moedas acumuladas**, a App 08 SHALL apresentar o card com o **avatar padrão do
projeto**, o nick e o total de moedas, na mesma moldura comum a todos os apoiadores, e SHALL
dizer **quantas moedas faltam** para liberar o avatar próprio. A tela NEVER SHALL cobrar aporte
nem insistir para que ele aconteça, e NEVER SHALL marcar de outro modo quem está abaixo do piso.
Alcançado o piso, o envio do avatar próprio SHALL abrir sem ato algum da gestão. Toda saída
SHALL exibir **moedas**, nunca reais. (`RF-14-14`, `RF-14-15`, `RF-14-16`, `RN-14-09`,
`RN-14-11`, documento 11 §8.2, PRD-14 §12)

#### Scenario: Com 5 moedas o card é o padrão, e a tela diz o que falta

- **WHEN** um Apoiador com 5 moedas acumuladas abre a identidade pública
- **THEN** o card aparece com o avatar padrão, o nick e o total em moedas, e a tela diz que
  faltam 5 moedas para o avatar próprio, sem pedir o aporte

#### Scenario: Cruzado o piso, o envio abre sozinho

- **WHEN** o Apoiador cruza as 10 moedas acumuladas e volta à tela
- **THEN** o envio do avatar próprio está aberto, sem que a gestão tenha feito nada

#### Scenario: A recusa do núcleo aparece com quanto falta

- **WHEN** o Apoiador abaixo do piso tenta enviar o avatar próprio e o núcleo recusa
- **THEN** a tela apresenta a recusa dizendo quantas moedas faltam, e o card segue com o avatar
  padrão

### Requirement: A tela de comprobatórios declara que só o Admin publica

A App 08 SHALL apresentar ao Apoiador em sessão a tela de **documentos comprobatórios**, em que
ele declara currículo, portfólio, redes sociais, termos de doação e comprovantes por **endereço e
rótulo**, e NEVER SHALL oferecer anexo de arquivo. A tela SHALL declarar, **antes do envio**, que
o documento entra na fila da gestão e só vai à página pública quando um Admin o anexar ao
cadastro. Enviado, a tela SHALL apresentar o documento como **pendente**, e SHALL distinguir o
que já está **publicado** na página do Apoiador. (`RF-14-18`, `RF-14-19`, `RF-14-20`, `RN-14-12`,
PRD-14 §5.9)

#### Scenario: A tela pede link, não arquivo

- **WHEN** o Apoiador abre a tela de comprobatórios
- **THEN** a tela pede endereço e rótulo de cada documento e não oferece campo de anexo de
  arquivo

#### Scenario: A declaração aparece antes do envio

- **WHEN** o Apoiador chega ao ponto de enviar o documento
- **THEN** a tela declara que ele só vai à página pública depois que um Admin o anexar

#### Scenario: A lista separa o publicado do pendente

- **WHEN** o Apoiador tem um documento já anexado por Admin e outro ainda não
- **THEN** a tela apresenta o primeiro como publicado na página dele e o segundo como pendente

### Requirement: A tela de "Meus aportes" mostra o que já foi homologado e o Poder Sustentador

A aplicação SHALL apresentar ao Apoiador em sessão os aportes dele **já homologados**, cada um
com **data, tipo e destino**, e o **Poder Sustentador** como **total acumulado em moedas**,
como o núcleo os devolve — sem somar, reordenar por valor nem recalcular. Apoiador sem aporte
homologado SHALL ver a tela com o total em zero e a explicação de que ainda não há aporte
homologado. (`RF-14-21`, `RF-14-22`, PRD-14 §6.3)

#### Scenario: Os aportes homologados aparecem com o total

- **WHEN** o Apoiador abre "Meus aportes"
- **THEN** cada aporte aparece com data, tipo e destino, e o Poder Sustentador aparece como
  total acumulado em moedas

#### Scenario: Sem aporte homologado a tela explica o vazio

- **WHEN** o Apoiador ainda não teve aporte homologado
- **THEN** a tela mostra o total em zero e diz que ainda não há aporte homologado

### Requirement: Nenhuma tela do Apoiador exibe reais, salvo a da declaração

A aplicação SHALL exibir todo valor **em moedas** e NEVER SHALL exibir reais em tela alguma,
com uma única exceção: a tela em que se **declara a transferência**, onde o valor transferido é
em reais e SHALL aparecer com o **equivalente em moedas** ao lado. (`RF-14-23`, `RN-14-09`,
invariante 16 do documento 99 §6)

#### Scenario: As telas de leitura só falam em moedas

- **WHEN** o Apoiador percorre "Meus aportes", as necessidades em aberto e a situação das
  declarações
- **THEN** nenhum valor aparece em reais

#### Scenario: A tela da declaração mostra reais com o equivalente em moedas

- **WHEN** o Apoiador informa o valor transferido
- **THEN** a tela mostra o valor em reais e, ao lado, o equivalente em moedas

### Requirement: As necessidades em aberto aparecem com atividade, comunidade e o que falta

A aplicação SHALL listar as **necessidades de recurso em aberto** como o núcleo as publica, com
a **atividade** — o recurso que falta, a data e o horário da aula e o ponto de apoio —, a
**comunidade** e **o que falta em moedas**. A aplicação NEVER SHALL somar, reordenar por valor
nem recalcular a falta, e necessidade de tipo **sem valor de referência vigente** SHALL
continuar aparecendo, com a quantidade que falta e sem valor arbitrado. Não havendo necessidade
em aberto, a tela SHALL dizê-lo, sem lista vazia sem explicação. (`RF-14-24`, `RN-14-09`,
PRD-14 §§5.3, 6.3)

#### Scenario: A lista traz a atividade, a comunidade e o que falta

- **WHEN** o Apoiador abre as necessidades em aberto
- **THEN** cada necessidade aparece com o recurso, a data e o horário da aula, o ponto de
  apoio, a comunidade e o que falta em moedas

#### Scenario: Necessidade sem valor de referência continua na lista

- **WHEN** uma necessidade é de tipo sem valor de referência vigente
- **THEN** ela aparece com a quantidade que falta e sem valor em moedas

#### Scenario: Sem necessidade em aberto a tela diz

- **WHEN** não há necessidade de recurso em aberto
- **THEN** a tela diz que não há necessidade em aberto

### Requirement: O Apoiador declara o aporte por necessidade, por sugestão ou por valor livre

A aplicação SHALL oferecer ao Apoiador em sessão três caminhos para declarar um aporte novo: a
partir de uma **necessidade em aberto**, por um **valor sugerido** da escada do perfil que ele
declarar na própria tela, ou por **valor livre**. O degrau da escada SHALL ser sugestão e não
piso: o valor livre SHALL aceitar qualquer quantia, com fração de duas casas. A tela SHALL
exigir o **anexo do comprovante** da transferência para enviar e SHALL declarar os formatos
aceitos; recusado o comprovante pelo núcleo, SHALL apresentar a recusa com os formatos válidos.
(`RF-14-25`, `RF-14-26`, `RN-14-06`, PRD-14 §§5.3, 6.3, 12)

#### Scenario: A necessidade escolhida abre a declaração

- **WHEN** o Apoiador escolhe cobrir uma necessidade em aberto
- **THEN** a tela declara o aporte por aquela necessidade, com o que ela pede em moedas

#### Scenario: A escada do perfil aparece com o equivalente em moedas

- **WHEN** o Apoiador declara o perfil na tela e vê os valores sugeridos
- **THEN** cada degrau aparece com o equivalente em moedas ao lado

#### Scenario: O valor livre aceita qualquer quantia

- **WHEN** o Apoiador informa um valor livre abaixo do menor degrau da escada, com fração de
  duas casas
- **THEN** a tela aceita o valor e mostra o equivalente em moedas antes do envio

#### Scenario: Sem comprovante a declaração não é enviada

- **WHEN** o Apoiador tenta enviar a declaração sem anexar comprovante
- **THEN** a tela recusa o envio e diz quais formatos valem

### Requirement: A tela declara que o aporte entra pendente e não credita nada

A aplicação SHALL declarar, **antes do envio**, que o aporte entra **pendente de homologação**,
que um Admin vai conferir o comprovante e que, até lá, ele não vira moeda, não compõe o Poder
Sustentador e não abate o que falta a necessidade alguma. Enviada a declaração, a aplicação
SHALL confirmar que ela entrou na fila da gestão e NEVER SHALL exibir a necessidade escolhida
como coberta antes da homologação. (`RF-14-26`, `RN-14-07`, PRD-14 §§5.3, 12)

#### Scenario: A declaração aparece antes do envio

- **WHEN** o Apoiador chega ao ponto de enviar a declaração
- **THEN** a tela diz que o aporte entra pendente, que um Admin confere o comprovante e que
  nada é creditado até lá

#### Scenario: Enviada a declaração, a necessidade não muda

- **WHEN** a declaração é enviada com sucesso
- **THEN** a aplicação confirma a entrada na fila da gestão e a necessidade escolhida continua
  com a mesma quantidade faltante

### Requirement: O Apoiador acompanha a situação de cada aporte declarado

A aplicação SHALL apresentar ao Apoiador a situação de cada aporte que ele declarou —
**pendente**, **homologado** ou **recusado** —, com o **valor declarado em moedas**, a data e a
origem da escolha, e, no recusado, o **motivo em linguagem simples**, dentro da plataforma.
Esta não é a tela em que se declara a transferência: aqui o valor aparece **em moedas**. A
aplicação NEVER SHALL oferecer edição, reenvio automático ou qualquer ato sobre a situação: a
mudança é da gestão. (`RF-14-27`, `RN-14-08`, PRD-14 §§3.2, 5.3)

#### Scenario: As três situações aparecem com o que cada uma tem

- **WHEN** o Apoiador abre a situação dos aportes declarados
- **THEN** cada um aparece com a situação, o valor declarado em moedas, a data e a origem da
  escolha, e o recusado traz o motivo em linguagem simples

#### Scenario: A tela não oferece ato sobre a situação

- **WHEN** o Apoiador vê um aporte pendente ou recusado
- **THEN** não há na tela botão de homologar, editar ou reenviar

### Requirement: Quem quer aportar material ou serviço é encaminhado à gestão

A aplicação NEVER SHALL aceitar declaração de aporte em **material, serviço ou divulgação** e
SHALL explicar, na própria tela de declaração, que essas formas entram pelo cadastro do Admin,
com termo de doação ou registro do material. Recusada a declaração pelo núcleo por essa razão,
a tela SHALL apresentar a orientação de procurar a gestão. (`RF-14-28`, `RN-14-05`, PRD-14
§§3.2, 12)

#### Scenario: A tela explica que só o dinheiro entra por aqui

- **WHEN** o Apoiador abre a tela de declaração
- **THEN** ela diz que o aporte pela aplicação é em dinheiro e que material, serviço e
  divulgação entram pelo cadastro do Admin

#### Scenario: A recusa do núcleo vira orientação na tela

- **WHEN** o núcleo recusa a declaração por ser de material ou serviço
- **THEN** a tela apresenta a orientação de procurar a gestão, e nada é enviado de novo

### Requirement: A área Missões agrupa as missões abertas pelo nível de necessidade

A App 08 SHALL abrir a área **Missões** com as missões abertas **agrupadas pelo nível de
necessidade** que sustentam — existir, acontecer, reconhecer, permanecer —, cada uma com o que
se pede, **quanto falta em moedas**, o prazo e o **selo que rende**. O quanto já foi coberto
SHALL aparecer como **quantidade**, e a tela NEVER SHALL identificar quem cobriu. Missão sem
necessidade publicada por trás, vencida ou concluída NEVER SHALL aparecer na área.
(`RF-14-60`, `RF-14-61`, `RF-14-62`, `RF-14-71`, `RF-14-72`)

#### Scenario: As missões aparecem agrupadas pelo nível

- **WHEN** o Apoiador abre a área Missões
- **THEN** as missões abertas aparecem em quatro grupos, cada missão com o que se pede, o que
  falta em moedas, o prazo e o selo

#### Scenario: O coberto aparece sem nome de quem cobriu

- **WHEN** uma missão já foi coberta em parte
- **THEN** a tela mostra a quantidade coberta e nenhum nick, avatar ou valor de quem cobriu

#### Scenario: A missão vencida some da área

- **WHEN** o prazo de uma missão vence sem que ela feche
- **THEN** ela deixa de aparecer na área Missões

### Requirement: A tela declara que só a homologação abate e conclui

A área Missões SHALL declarar, antes do envio, que o aporte nasce **pendente**, que não abate o
que falta e que não conclui missão alguma até o Admin homologar. Coberta em parte, a tela SHALL
mostrar a missão ainda **aberta** com o restante atualizado, sem selo creditado. (`RF-14-64`,
`RF-14-65`, `RN-14-32`, PRD-14 §5.4)

#### Scenario: A tela avisa que a declaração não abate nada

- **WHEN** o Apoiador vai declarar um aporte por uma missão
- **THEN** a tela declara que o aporte entra pendente e não abate o que falta nem conclui a
  missão

#### Scenario: A cobertura parcial mostra o restante

- **WHEN** um aporte do Apoiador para uma missão é homologado e ela segue aberta
- **THEN** a tela mostra a missão aberta com o restante atualizado e nenhum selo novo

### Requirement: A área de sustento mostra o nível, os selos e a frente que falta

A App 08 SHALL apresentar ao Apoiador o **nível de sustento** alcançado, os **selos
conquistados agrupados por família** e a **frente que falta** para o próximo nível — **uma
vez, sem insistir**: sem repetição em outras telas, sem lembrete e sem contagem regressiva.
Concluída uma missão, a tela SHALL mostrar o **selo novo** e, quando houver, o nível alcançado.
A aplicação NEVER SHALL exibir nível ou selo regredindo. (`RF-14-67`, `RF-14-68`, `RF-14-69`,
`RN-14-36`, PRD-14 §5.4)

#### Scenario: O sustento aparece com a frente que falta

- **WHEN** o Apoiador abre a área de sustento
- **THEN** a tela mostra o nível atual, os selos agrupados por família e a frente que falta para
  o próximo nível

#### Scenario: A frente que falta aparece uma vez

- **WHEN** o Apoiador navega pelas demais telas da aplicação
- **THEN** nenhuma delas repete o convite ao próximo nível

#### Scenario: A conclusão mostra o selo novo

- **WHEN** uma missão de que o Apoiador participou é concluída
- **THEN** a tela mostra o selo novo e, se for o caso, o nível de sustento alcançado

### Requirement: Nenhuma tela do Apoiador compara apoiadores por valor

Nenhuma tela da App 08 SHALL ordenar, classificar ou comparar apoiadores por valor aportado, e
NEVER SHALL apresentar pódio, posição ou ranking. O card e a página públicos do Apoiador SHALL
exibir o **nível de sustento** e os **selos**. (`RF-14-70`, `RF-14-73`, `RN-14-38`)

#### Scenario: Nenhuma lista ordena por valor

- **WHEN** o Apoiador percorre as telas da aplicação
- **THEN** nenhuma delas apresenta apoiadores em ordem de valor, posição ou pódio

#### Scenario: O card público mostra nível e selos

- **WHEN** a página pública do Apoiador é montada
- **THEN** ela exibe o nível de sustento e os selos conquistados, ao lado do avatar, do nick e
  do total em moedas
