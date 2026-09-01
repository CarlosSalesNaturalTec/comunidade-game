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

### Requirement: A gestão lê a fila de solicitações de participação

O núcleo SHALL devolver as solicitações de participação com **nome**, **e-mail**,
**WhatsApp**, **pretensão** — Mestre ou Apoiador —, **apresentação**, **instituição** e
**links declarados**, mais a **situação**, o **prazo** e, quando já houver desfecho, **quem
avaliou**, o **parecer** e a **data**. Quando a pretensão for Apoiador, a leitura SHALL levar
também o **aporte declarado**, o **nick pretendido** e a indicação de que há **comprovante
anexado**. A leitura SHALL ser paginada.

A leitura SHALL marcar cada solicitação **em atraso** quando o prazo tiver vencido sem
desfecho. O atraso SHALL ser **derivado** do prazo no momento da consulta e NEVER SHALL ser
gravado como situação. (`RF-02-18`, `RF-02-65`, `RF-02-83`, `RF-01-25`, `RF-01-28`,
`RN-01-49`)

A leitura SHALL exigir **Admin** em sessão. Mestre, Apoiador, Guerreiro(a) e responsável SHALL
receber **403**. (`RF-01-16`, `RN-02-01`)

A leitura NEVER SHALL devolver o conteúdo do comprovante — apenas que ele existe. (`RN-01-28`)

#### Scenario: Admin lê a fila com as solicitações em aberto

- **WHEN** um Admin em sessão consulta a fila de solicitações de participação
- **THEN** vêm as solicitações com identificação, pretensão, apresentação, instituição, links,
  situação e prazo

#### Scenario: Solicitação de Apoiador traz o pré-cadastro

- **WHEN** a fila devolve uma solicitação com pretensão de Apoiador
- **THEN** ela vem com o aporte declarado, o nick pretendido e a indicação de comprovante
  anexado

#### Scenario: Solicitação com prazo vencido vem marcada em atraso

- **WHEN** um Admin consulta a fila e há solicitação sem desfecho cujo prazo de 7 dias já
  venceu
- **THEN** ela vem marcada como em atraso, e a situação gravada continua sendo **recebida**

#### Scenario: Solicitação já avaliada traz o desfecho

- **WHEN** a fila devolve uma solicitação que já teve desfecho
- **THEN** ela vem com a situação final, o parecer, quem avaliou e a data, e não vem marcada
  em atraso

#### Scenario: Quem não é Admin não lê a fila

- **WHEN** um Mestre, Apoiador, Guerreiro(a) ou responsável em sessão consulta a fila
- **THEN** o núcleo responde 403

#### Scenario: A fila não devolve o comprovante

- **WHEN** a fila devolve uma solicitação com comprovante anexado
- **THEN** vem apenas a indicação de que existe comprovante, e nunca o conteúdo do arquivo

### Requirement: O Admin registra o desfecho da solicitação de participação

O núcleo SHALL aceitar de um **Admin** em sessão o desfecho de uma solicitação de
participação, **aceita** ou **recusada**, gravando o **parecer**, o **autor da avaliação** e a
**data e hora**. Desfecho diferente de aceita ou recusada SHALL ser recusado com **422**.
(`RF-02-19`, `RF-02-86`, `RF-01-25`)

O desfecho NEVER SHALL criar persona, credencial ou qualquer acesso, nem na aprovação: o
cadastro correspondente SHALL depender de ato posterior do Admin. (`RN-01-03`, `RN-01-28`,
`RN-02-03`)

A solicitação **já avaliada** NEVER SHALL ser reavaliada: novo desfecho sobre ela SHALL ser
recusado com **409**, e o desfecho gravado SHALL permanecer intacto. (`RF-01-25`)

Quem não for Admin SHALL receber **403**. (`RN-02-01`, `RN-02-02`)

Toda escrita SHALL entrar na trilha de auditoria, com autor, papel, data e hora. (`RN-02-21`)

#### Scenario: Admin aceita a solicitação

- **WHEN** um Admin em sessão conclui uma solicitação como aceita, com parecer
- **THEN** o núcleo grava a situação aceita, o parecer, o autor e a data, e nenhuma persona é
  criada

#### Scenario: Admin recusa a solicitação com o motivo

- **WHEN** um Admin em sessão conclui uma solicitação como recusada, com o motivo no parecer
- **THEN** o núcleo grava a situação recusada com o motivo, o autor e a data

#### Scenario: Desfecho fora do vocabulário é recusado

- **WHEN** o desfecho enviado não é aceita nem recusada
- **THEN** o núcleo responde 422 e nada é gravado

#### Scenario: Solicitação avaliada não se reavalia

- **WHEN** um Admin envia novo desfecho para uma solicitação que já tem desfecho gravado
- **THEN** o núcleo responde 409 e o desfecho original permanece como estava

#### Scenario: Quem não é Admin não avalia

- **WHEN** um Mestre em sessão tenta concluir uma solicitação de participação
- **THEN** o núcleo responde 403 e nada é gravado

#### Scenario: O desfecho entra na trilha de auditoria

- **WHEN** um Admin conclui uma solicitação
- **THEN** a trilha de auditoria registra o ato com autor, papel, data e hora

### Requirement: A gestão lê a fila de solicitações de dados

O núcleo SHALL devolver as solicitações de dados com **solicitante**, **instituição**,
**finalidade declarada** e **recorte pedido**, mais a **situação**, o **prazo** e, quando já
houver desfecho, **quem avaliou**, o **parecer** e a **data**. A leitura SHALL ser paginada e
SHALL marcar como **em atraso** a solicitação sem desfecho cujo prazo tenha vencido, derivando
o atraso do prazo no momento da consulta. (`RF-02-77`, `RF-01-46`, `RN-01-49`)

A leitura SHALL exigir **Admin** em sessão; os demais papéis SHALL receber **403**.
(`RF-01-16`, `RN-02-01`)

#### Scenario: Admin lê a fila de pedidos de dados

- **WHEN** um Admin em sessão consulta a fila de solicitações de dados
- **THEN** vêm as solicitações com solicitante, instituição, finalidade declarada, recorte
  pedido, situação e prazo

#### Scenario: Pedido de dados com prazo vencido vem em atraso

- **WHEN** há solicitação de dados sem desfecho cujo prazo de 7 dias já venceu
- **THEN** ela vem marcada em atraso, e a situação gravada continua sendo **recebida**

#### Scenario: Quem não é Admin não lê a fila de dados

- **WHEN** um Mestre em sessão consulta a fila de solicitações de dados
- **THEN** o núcleo responde 403

### Requirement: O Admin aprova ou recusa a solicitação de dados sob os três critérios

O núcleo SHALL aceitar de um **Admin** em sessão o desfecho da solicitação de dados,
**aceita** ou **recusada**, com **parecer obrigatório**. A aprovação SHALL exigir, além do
parecer, o **compromisso de não tentar reidentificar ninguém**, afirmado no ato do desfecho;
sem ele o núcleo SHALL recusar com **422**. O parecer vazio SHALL ser recusado com **422**,
tanto na aprovação quanto na recusa. (`RF-02-78`, `RF-02-93`, `RF-01-46`, `RN-01-48`)

Os três critérios de aprovação SHALL ser: **solicitante identificado** — garantido no registro
—, **finalidade declarada compatível** — apurada pelo Admin no parecer — e **compromisso de não
reidentificação** — afirmado no desfecho. (`RF-02-93`, `RN-02-26`)

**Nenhum conjunto de dados** SHALL sair sem aprovação de Admin registrada, e a entrega SHALL
ser **gratuita** e **anonimizada**. O núcleo SHALL registrar **o que foi entregue e a quem**.
(`RF-02-79`, `RF-01-47`, `RN-02-26`, invariante 17 do documento 99 §6)

A solicitação já avaliada NEVER SHALL ser reavaliada: novo desfecho SHALL ser recusado com
**409**. Quem não for Admin SHALL receber **403**, e toda escrita SHALL entrar na trilha de
auditoria. (`RN-02-01`, `RN-02-21`)

#### Scenario: Admin aprova com o compromisso afirmado

- **WHEN** um Admin conclui a solicitação de dados como aceita, com parecer e afirmando o
  compromisso de não reidentificação
- **THEN** o núcleo grava a situação aceita, o parecer, o autor e a data

#### Scenario: Aprovação sem o compromisso é recusada

- **WHEN** um Admin conclui como aceita, com parecer, mas sem afirmar o compromisso de não
  reidentificação
- **THEN** o núcleo responde 422 e nada é gravado

#### Scenario: Desfecho sem parecer é recusado

- **WHEN** um Admin conclui a solicitação de dados com o parecer vazio
- **THEN** o núcleo responde 422 e nada é gravado

#### Scenario: Nenhum conjunto sai sem aprovação registrada

- **WHEN** alguém tenta liberar um conjunto de dados de uma solicitação sem desfecho ou
  recusada
- **THEN** o núcleo recusa a liberação

#### Scenario: A entrega aprovada fica registrada

- **WHEN** um conjunto de dados é liberado sobre uma solicitação aprovada
- **THEN** o núcleo registra o que foi entregue e a quem, e a entrega é gratuita e anonimizada

#### Scenario: Solicitação de dados avaliada não se reavalia

- **WHEN** um Admin envia novo desfecho para uma solicitação de dados já avaliada
- **THEN** o núcleo responde 409 e o desfecho original permanece

### Requirement: A gestão lê a fila de solicitações de chave

O núcleo SHALL devolver as solicitações de chave com **quem pediu** e **o que pretende
construir**, mais a **situação**, o **prazo** e, quando já houver desfecho, **quem avaliou**, o
**parecer** e a **data**. A leitura SHALL ser paginada, SHALL marcar o **atraso** derivado do
prazo e SHALL indicar se a solicitação **já rendeu chave**. (`RF-02-87`, `RF-01-49`,
`RN-01-49`, `RN-01-51`)

A leitura SHALL exigir **Admin** em sessão; os demais papéis SHALL receber **403**.
(`RF-01-16`, `RN-02-27`)

A leitura NEVER SHALL devolver o segredo da chave, em nenhuma situação. (`RN-02-28`,
`RN-01-35`)

#### Scenario: Admin lê a fila de pedidos de chave

- **WHEN** um Admin em sessão consulta a fila de solicitações de chave
- **THEN** vêm as solicitações com quem pediu, o que pretende construir, situação e prazo

#### Scenario: Solicitação que já rendeu chave vem marcada

- **WHEN** a fila devolve uma solicitação aceita sobre a qual a chave já foi emitida
- **THEN** ela vem indicando que a chave já foi emitida

#### Scenario: A fila de chaves nunca devolve o segredo

- **WHEN** a fila devolve uma solicitação que já rendeu chave
- **THEN** o segredo não aparece em nenhum campo

### Requirement: O Admin aprova ou recusa a solicitação de chave, e a emissão vem depois

O núcleo SHALL aceitar de um **Admin** em sessão o desfecho da solicitação de chave,
**aceita** ou **recusada**, gravando o **parecer**, o **autor** e a **data**. O desfecho
NEVER SHALL emitir chave: a emissão SHALL continuar sendo ato separado, sobre solicitação já
aceita, e SHALL devolver o segredo uma única vez. (`RF-02-88`, `RF-02-89`, `RF-01-49`,
`RF-01-50`, `RN-02-27`, `RN-01-51`)

Decisão do fundador em 2026-08-22, que completa o PRD-02 §9: o desfecho da solicitação de
chave é rota própria, simétrica às das outras naturezas, e `POST /v1/chaves` segue emitindo
apenas sobre solicitação já aceita.

A solicitação já avaliada NEVER SHALL ser reavaliada: novo desfecho SHALL ser recusado com
**409**. Quem não for Admin SHALL receber **403**, e toda escrita SHALL entrar na trilha de
auditoria. (`RN-02-01`, `RN-02-21`)

#### Scenario: Admin aprova o pedido de chave sem emitir nada

- **WHEN** um Admin conclui a solicitação de chave como aceita, com parecer
- **THEN** o núcleo grava o desfecho e **nenhuma chave é emitida** por esse ato

#### Scenario: A emissão só alcança solicitação aceita

- **WHEN** um Admin tenta emitir a chave de uma solicitação recusada ou ainda sem desfecho
- **THEN** o núcleo recusa a emissão

#### Scenario: Aprovada, a emissão passa a ser possível

- **WHEN** um Admin emite a chave de uma solicitação que ele aprovou
- **THEN** o núcleo emite a chave e devolve o segredo uma única vez

#### Scenario: Admin recusa o pedido de chave com o motivo

- **WHEN** um Admin conclui a solicitação de chave como recusada, com o motivo no parecer
- **THEN** o núcleo grava a recusa com o motivo, o autor e a data, e nenhuma chave existe

#### Scenario: Quem não é Admin não avalia pedido de chave

- **WHEN** um Apoiador em sessão tenta concluir uma solicitação de chave
- **THEN** o núcleo responde 403 e nada é gravado

### Requirement: A gestão lê a fila única de sugestões e propostas

O núcleo SHALL devolver as sugestões e propostas com o **autor** e a **persona** de quem
propôs, o teor, a **situação**, o **prazo** e, quando já houver desfecho, **quem avaliou**, o
**parecer**, o **motivo do retorno** e a **data**. A leitura SHALL ser paginada, SHALL reunir
numa fila só o que vem das Apps 05, 07, 08 e 09 e SHALL marcar o **atraso** derivado do prazo.
(`RF-02-25`, `RF-01-25`, `RN-01-49`)

A leitura SHALL exigir **Admin** em sessão; os demais papéis SHALL receber **403**.
(`RF-01-16`, `RN-02-01`)

#### Scenario: Admin lê a fila de sugestões das quatro aplicações

- **WHEN** um Admin em sessão consulta a fila de sugestões
- **THEN** vêm as sugestões das Apps 05, 07, 08 e 09 numa lista só, cada uma identificando o
  autor e a persona dele

#### Scenario: Sugestão com prazo vencido vem em atraso

- **WHEN** há sugestão sem desfecho cujo prazo de 7 dias já venceu
- **THEN** ela vem marcada em atraso

### Requirement: O Admin avalia a sugestão e o retorno chega a quem propôs

O núcleo SHALL aceitar de um **Admin** em sessão o desfecho da sugestão, **adotada** ou **não
adotada**, gravando o **parecer**, o **autor** e a **data**. A sugestão **não adotada** SHALL
exigir o **motivo do retorno** em linguagem simples, sem o qual o núcleo SHALL recusar com
**422**, e SHALL marcar a data de descarte da transcrição, 90 dias à frente. A sugestão
**adotada** SHALL creditar **20 pontos extras** e o **badge de protagonismo** a quem propôs, na
mesma operação, e SHALL guardar transcrição e autoria de forma permanente. (`RF-02-26`,
`RF-01-25`, `RF-01-56`, `RN-01-50`)

O crédito SHALL alcançar **apenas autor com papel de Guerreiro(a)**: a pontuação é da criança, e
proposta de **responsável**, de Mestre ou de Apoiador NEVER SHALL creditar ponto extra nem
badge. O desfecho dessas propostas SHALL ser gravado do mesmo jeito, com parecer, autor, data e
o motivo do retorno quando não adotada — o que muda é só o crédito. (`RN-13-18`, PRD-13 §§5.7,
7)

O crédito SHALL ser **idempotente**: regravar o desfecho adotada NEVER SHALL creditar de novo.

O retorno a quem propôs SHALL acontecer **dentro da plataforma**, e o núcleo NEVER SHALL
enviar e-mail por causa dele. (`RN-02-25`, `RN-13-15`)

A sugestão já avaliada NEVER SHALL ser reavaliada: novo desfecho SHALL ser recusado com
**409**. Quem não for Admin SHALL receber **403**, e toda escrita SHALL entrar na trilha de
auditoria. (`RN-02-01`, `RN-02-21`)

#### Scenario: Sugestão adotada credita os extras e o badge

- **WHEN** um Admin conclui como adotada uma sugestão de Guerreiro(a)
- **THEN** o núcleo grava o desfecho e credita 20 pontos extras e o badge de protagonismo a
  quem propôs, na mesma operação

#### Scenario: Proposta de responsável adotada não pontua

- **WHEN** um Admin conclui como adotada a proposta de um responsável
- **THEN** o núcleo grava o desfecho, e nenhum ponto extra e nenhum badge são creditados

#### Scenario: Proposta de Mestre ou de Apoiador adotada não pontua

- **WHEN** um Admin conclui como adotada a proposta de um Mestre ou de um Apoiador
- **THEN** o núcleo grava o desfecho, e nenhum ponto extra e nenhum badge são creditados

#### Scenario: O crédito da sugestão adotada não se repete

- **WHEN** o desfecho adotada é gravado sobre uma sugestão que já foi creditada
- **THEN** nenhum ponto extra e nenhum badge são creditados de novo

#### Scenario: Sugestão não adotada exige o motivo do retorno

- **WHEN** um Admin conclui uma sugestão como não adotada sem informar o motivo do retorno
- **THEN** o núcleo responde 422 e nada é gravado

#### Scenario: Sugestão não adotada marca o descarte da transcrição

- **WHEN** um Admin conclui uma sugestão como não adotada com o motivo do retorno
- **THEN** o núcleo grava o motivo e a data de descarte da transcrição, 90 dias à frente

#### Scenario: Sugestão avaliada não se reavalia

- **WHEN** um Admin envia novo desfecho para uma sugestão já avaliada
- **THEN** o núcleo responde 409 e o desfecho original permanece

### Requirement: Quem propôs acompanha as próprias sugestões e propostas

O núcleo SHALL devolver à **persona autenticada** as sugestões e propostas que **ela mesma**
registrou, para que quem propõe acompanhe o status na fila única sem depender do Admin.
`RF-09-55` exige as duas metades — registrar e acompanhar —, e hoje só o Admin lê a fila.
(`RF-09-55`, `RF-01-25`, `RF-01-28`, 03 §§7, 12.2)

Cada registro SHALL sair com o **alvo** — atividade, trilha ou plataforma —, o **texto**, a
**situação** — recebida, em avaliação, adotada ou não adotada —, o **prazo** e a marca de
**em atraso** derivada dele, e, quando já houver desfecho, a **data** e, na não adotada, o
**motivo do retorno em linguagem simples**. É por esta leitura que o retorno chega a quem
propôs, **dentro da plataforma**: o núcleo NEVER SHALL enviar e-mail por causa dele.
(`RN-02-25`)

A consulta NEVER SHALL devolver sugestão de outro autor, nem o **parecer** interno da avaliação,
que é da leitura de Admin. Ela SHALL ser paginada como toda listagem do núcleo, e a leitura de
Admin da fila NEVER SHALL mudar por causa dela.

#### Scenario: O autor vê as próprias propostas em qualquer situação

- **WHEN** uma persona autenticada consulta as suas sugestões e propostas
- **THEN** o núcleo devolve as que ela registrou, com alvo, texto, situação e prazo

#### Scenario: A proposta não adotada devolve o motivo do retorno

- **WHEN** a lista inclui uma proposta concluída como não adotada
- **THEN** ela sai com a situação `não adotada`, o motivo do retorno em linguagem simples e a
  data do desfecho

#### Scenario: A proposta com prazo vencido sai marcada em atraso

- **WHEN** a lista inclui uma proposta sem desfecho cujo prazo de 7 dias já venceu
- **THEN** ela sai marcada em atraso, e a situação gravada continua sendo **recebida**

#### Scenario: A consulta não alcança proposta de outro autor

- **WHEN** uma persona consulta as suas propostas e há propostas de outras personas na fila
- **THEN** o núcleo devolve apenas as dela

#### Scenario: O parecer interno não sai por esta porta

- **WHEN** a lista inclui uma proposta já avaliada
- **THEN** o parecer da avaliação não aparece em campo algum: quem propôs recebe o motivo do
  retorno, não o parecer

#### Scenario: O retorno chega sem e-mail

- **WHEN** um Admin conclui a avaliação de uma proposta
- **THEN** quem propôs passa a ver o desfecho nesta leitura, e nenhum e-mail é enviado
