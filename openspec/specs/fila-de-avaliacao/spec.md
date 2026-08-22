## Purpose

A fila única onde a gestão avalia tudo o que chega de fora e de dentro sem criar acesso:
solicitação de participação, de dados e de chave, vindas das rotas públicas da vitrine, e
sugestões e propostas vindas das personas autenticadas. Nenhuma delas cadastra ninguém — o
cadastro é sempre ato posterior de um Admin.

## Requirements

### Requirement: A fila reúne quatro naturezas sobre um ciclo comum de avaliação

O núcleo SHALL manter em fila única de avaliação a **solicitação de participação**, a
**solicitação de dados**, a **solicitação de chave** e a **sugestão ou proposta**, cada uma
com os seus próprios campos e todas sobre o mesmo ciclo: **situação**, **prazo**, **quem
avaliou**, **parecer** e **data do desfecho**. O prazo de resposta SHALL ser de **7 dias**
nas quatro naturezas. Vencido o prazo sem desfecho, a solicitação SHALL permanecer aberta e
identificável como em atraso. (`RF-01-25`, `RF-01-46`, `RF-01-49`, `RN-01-49`, 02 §1,
03 §§7, 8, 12.3)

#### Scenario: Solicitação nasce recebida com o prazo correndo

- **WHEN** qualquer das quatro naturezas é registrada
- **THEN** o núcleo grava a situação **recebida**, com o prazo de 7 dias contado do registro

#### Scenario: Prazo vencido sem desfecho não encerra a solicitação

- **WHEN** passam 7 dias do registro sem desfecho
- **THEN** a solicitação continua aberta e o núcleo a identifica como em atraso

#### Scenario: Desfecho registra quem avaliou, o parecer e a data

- **WHEN** um Admin conclui a avaliação de uma solicitação
- **THEN** o núcleo grava a situação final, o parecer, o autor da avaliação e a data e hora

### Requirement: Nenhuma solicitação cria cadastro, persona ou acesso

O núcleo SHALL registrar as solicitações **sem criar cadastro, persona, credencial ou
qualquer acesso**, em nenhuma das quatro naturezas e em nenhuma situação — inclusive quando
aprovadas. O envio SHALL devolver apenas o registro e o prazo, e SHALL NOT devolver dado,
arquivo, chave ou acesso no ato. Aprovada a solicitação, o cadastro correspondente SHALL
depender de ato posterior de um Admin. (`RN-01-03`, `RN-01-25`, `RN-01-28`, `RN-01-37`,
02 §1)

#### Scenario: Envio de formulário público não devolve acesso

- **WHEN** um visitante envia a solicitação de participação, a de dados ou a de chave
- **THEN** o núcleo grava o registro e devolve o protocolo e o prazo, sem criar persona nem
  credencial e sem devolver dado, arquivo ou chave

#### Scenario: Solicitação aprovada continua sem criar cadastro

- **WHEN** um Admin aprova uma solicitação de participação
- **THEN** o núcleo registra o desfecho e **nenhuma persona é criada** pela aprovação

#### Scenario: Login não nasce de solicitação

- **WHEN** quem enviou uma solicitação tenta autenticar-se com os dados que informou
- **THEN** o núcleo recusa a autenticação, porque a solicitação não criou credencial

### Requirement: Solicitação de participação carrega o pré-cadastro do Apoiador

O núcleo SHALL registrar na solicitação de participação a pretensão — Mestre ou Apoiador —,
os dados de contato, a apresentação e, quando a pretensão for Apoiador, o **aporte
declarado**, o **comprovante anexado** e o **nick** escolhido por quem se pré-cadastra. A
validação do comprovante SHALL ser ato de Admin, e o núcleo SHALL NOT coletar CPF, CNPJ ou
documento de identidade de quem aporta, em nenhum campo da solicitação.

O nick declarado SHALL passar pela conferência restrita a nicks de adulto, e a solicitação
NEVER SHALL criar persona nem gravar o nick como nick de persona: até a aprovação do Admin ele
é apenas o nick pretendido. Solicitação com pretensão de **Mestre** NÃO SHALL declarar nick —
o Mestre o define no primeiro acesso. (`RF-01-25`, `RN-01-28`, `RN-01-29`, `RN-01-30`,
`RF-14-13`, 02 §1)

#### Scenario: Pré-cadastro de Apoiador grava aporte declarado e comprovante

- **WHEN** um visitante envia a solicitação de participação com pretensão de Apoiador, o
  aporte declarado e o comprovante
- **THEN** o núcleo grava os três na solicitação, sem homologar o aporte e sem creditar moeda

#### Scenario: Documento fiscal é recusado

- **WHEN** a solicitação chega com CPF, CNPJ ou documento de identidade
- **THEN** o núcleo recusa a solicitação, porque a plataforma não coleta esse dado

#### Scenario: Pré-cadastro de Apoiador grava o nick pretendido

- **WHEN** um visitante envia a solicitação com pretensão de Apoiador e um nick disponível
- **THEN** o núcleo grava o nick na solicitação, sem criar persona alguma

#### Scenario: Pré-cadastro com nick de adulto em uso é recusado

- **WHEN** a solicitação chega com um nick já usado por um Apoiador ou por um Mestre
- **THEN** o núcleo recusa a solicitação e nada é gravado

#### Scenario: Solicitação de Mestre não declara nick

- **WHEN** a solicitação chega com pretensão de Mestre e um nick declarado
- **THEN** o núcleo recusa a solicitação, porque o nick do Mestre não nasce no pré-cadastro

### Requirement: O nick do pré-cadastro fica reservado por sete dias

O núcleo SHALL manter o nick declarado numa solicitação de participação **reservado por sete
dias** contados do envio. Enquanto a reserva durar, o núcleo SHALL tratar aquele nick como
**indisponível** na conferência restrita e SHALL recusar outra solicitação que o declare.
Vencidos os sete dias sem desfecho da solicitação, a reserva SHALL expirar e o nick SHALL
voltar a ficar disponível, sem que a solicitação seja alterada por isso.

A reserva SHALL cessar também quando a solicitação tiver desfecho: aprovada, o nick segue para
a persona criada pelo Admin; recusada, ele volta a ficar disponível. A reserva NEVER SHALL
alcançar nick de Guerreiro(a) nem impedir que uma criança escolha o seu. (`RF-01-25`,
`RN-01-28`, `RN-01-30`, documento 02 §1)

#### Scenario: Nick reservado sai como indisponível na conferência

- **WHEN** a conferência recebe um nick reservado por uma solicitação dentro dos sete dias
- **THEN** o núcleo responde que o nick está indisponível

#### Scenario: Segunda solicitação com o mesmo nick é recusada

- **WHEN** chega uma solicitação declarando um nick já reservado por outra dentro dos sete dias
- **THEN** o núcleo recusa a segunda solicitação e a primeira permanece intacta

#### Scenario: Reserva vencida libera o nick

- **WHEN** passam sete dias do envio de uma solicitação sem desfecho
- **THEN** o nick que ela declarou volta a ficar disponível, e a solicitação continua na fila
  como estava

#### Scenario: Solicitação recusada libera o nick

- **WHEN** um Admin recusa uma solicitação que declarava nick
- **THEN** o nick volta a ficar disponível

#### Scenario: Reserva não impede o cadastro de um Guerreiro(a) com aquele nick

- **WHEN** um nick está reservado por uma solicitação e um Guerreiro(a) é cadastrado com ele
- **THEN** o núcleo cria o Guerreiro(a) normalmente, porque a reserva vale na conferência de
  adulto e a unicidade da gravação corre contra personas, e a reserva não é persona

### Requirement: Solicitação de dados declara finalidade e nada sai sem aprovação

O núcleo SHALL registrar na solicitação de dados o **solicitante**, a **instituição**, o
**e-mail**, a **finalidade declarada** e o **recorte pedido**, e SHALL registrar o desfecho
com quem avaliou e o que foi entregue. O núcleo SHALL NOT liberar conjunto de dados sem
aprovação de Admin registrada, e a saída aprovada SHALL ser sempre anonimizada. A aprovação
SHALL exigir **solicitante identificado**, **finalidade declarada compatível com pesquisa ou
política pública** e **compromisso de não tentar reidentificar ninguém**; a recusa SHALL
registrar o motivo nessas mesmas três frentes. (`RF-01-46`, `RF-01-47`, `RN-01-25`,
`RN-01-48`, 03 §12.3)

#### Scenario: Solicitação sem finalidade declarada é recusada

- **WHEN** a solicitação de dados chega sem finalidade declarada
- **THEN** o núcleo recusa o registro

#### Scenario: Conjunto não sai sem aprovação registrada

- **WHEN** alguém pede o conjunto de dados de uma solicitação ainda sem aprovação de Admin
- **THEN** o núcleo recusa a liberação

#### Scenario: Recusa registra o motivo

- **WHEN** um Admin recusa a solicitação de dados
- **THEN** o núcleo grava o motivo, o autor e a data, e a solicitação fica encerrada como
  recusada

### Requirement: Solicitação de chave entra na fila sem emitir chave

O núcleo SHALL registrar a solicitação de chave com o **solicitante**, o **contato**, a
**instituição opcional** e **o que pretende construir**, e SHALL NOT emitir chave, criar
cadastro ou criar persona no envio. Esta superfície SHALL NOT ter freio por origem, porque
nova solicitação é sempre possível, e SHALL permanecer protegida apenas pela cota da chave da
aplicação que a chama. Aprovada a solicitação, ela SHALL guardar a **chave emitida** a partir
dela, e a aprovação SHALL ser a condição da emissão: nenhuma chave de terceiro nasce sem
solicitação aprovada. (`RF-01-49`, `RF-01-50`, `RN-01-37`, `RN-01-46`, `RN-01-51`, 03 §8)

#### Scenario: Envio devolve registro, nunca chave

- **WHEN** um visitante envia a solicitação de chave
- **THEN** o núcleo grava o registro e devolve o protocolo e o prazo, sem emitir chave nenhuma

#### Scenario: Solicitação de chave repetida da mesma origem não é freada

- **WHEN** a mesma origem envia a solicitação de chave repetidas vezes
- **THEN** o núcleo processa os envios sem atraso progressivo, porque a superfície não tem
  freio por origem

#### Scenario: Aprovação por si não emite a chave

- **WHEN** um Admin conclui a avaliação de uma solicitação de chave como aprovada
- **THEN** o núcleo grava o desfecho e não emite chave alguma: a emissão é ato seguinte e
  próprio do Admin

#### Scenario: A solicitação guarda a chave que rendeu

- **WHEN** a chave de uma solicitação aprovada é emitida
- **THEN** a solicitação passa a apontar a chave emitida, e as duas ficam consultáveis juntas

#### Scenario: Recusa não rende chave em tempo algum

- **WHEN** um Admin conclui a avaliação de uma solicitação de chave como recusada
- **THEN** nenhuma emissão é possível sobre ela, agora ou depois

### Requirement: Os dois formulários da vitrine são superfícies do freio por origem

O núcleo SHALL tratar a rota de envio da **solicitação de participação** e a da **solicitação
de dados** como as superfícies de formulário do freio por origem já definido na capacidade
`protecao-das-rotas-publicas`, contadas em separado uma da outra. (`RF-01-65`, `RN-01-27`,
03 §8)

#### Scenario: Envio repetido de formulário encontra o freio

- **WHEN** uma origem excede o limite de envios do formulário de participação na janela
- **THEN** o núcleo recusa com **429**, com o tempo de espera

#### Scenario: Cada formulário conta em separado

- **WHEN** uma origem é freada no formulário de participação e envia o de dados pela primeira
  vez
- **THEN** o envio é processado

### Requirement: Sugestão e proposta entram por rota autenticada, com autor e persona

O núcleo SHALL registrar a sugestão ou proposta com o **autor e a sua persona**, o **alvo** —
atividade, trilha ou plataforma —, o **texto**, a **situação** (recebida, em avaliação,
adotada ou não adotada) e, quando não adotada, o **motivo do retorno em linguagem simples**.
A rota SHALL ser autenticada. O núcleo SHALL receber e guardar **texto**: áudio de qualquer
origem é descartado na transcrição e SHALL NOT ser aceito por rota alguma. (`RF-01-25`,
03 §§7, 12.2)

#### Scenario: Sugestão registrada guarda autor, persona e alvo

- **WHEN** uma persona autenticada registra uma sugestão
- **THEN** o núcleo grava o autor, a persona, o alvo, o texto e a situação **recebida**

#### Scenario: Rota de sugestão não aceita áudio

- **WHEN** o envio traz áudio em vez de texto
- **THEN** o núcleo recusa, porque o áudio é descartado na transcrição e não chega ao núcleo

#### Scenario: Sugestão não adotada devolve o motivo em linguagem simples

- **WHEN** um Admin conclui a avaliação como **não adotada**
- **THEN** o núcleo grava o motivo do retorno em linguagem simples, consultável por quem
  sugeriu

#### Scenario: Sugestão anônima é recusada

- **WHEN** a rota de sugestão é chamada sem credencial de persona
- **THEN** o núcleo recusa com 401

### Requirement: A guarda da sugestão depende do desfecho

O núcleo SHALL guardar a transcrição da **sugestão não adotada por 90 dias** contados do
retorno a quem sugeriu, e a da **sugestão adotada de forma permanente, com a autoria
preservada** — é contribuição creditada. (`RF-01-25`, 03 §12.2)

#### Scenario: Sugestão não adotada é descartada após o prazo

- **WHEN** passam 90 dias do retorno de uma sugestão não adotada
- **THEN** o núcleo descarta a transcrição

#### Scenario: Sugestão adotada permanece com autoria

- **WHEN** uma sugestão é adotada
- **THEN** o núcleo guarda a transcrição e a autoria de forma permanente
