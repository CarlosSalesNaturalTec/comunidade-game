## Purpose

A credencial de dispositivo é como o sensor construído pelo Guerreiro(a) na trilha do Robô
Educa entra no núcleo. Ela é do **aparelho, nunca da criança**, e é o próprio registro dele —
não há cadastro de dispositivo além dela. Não amplia direito algum: não abre sessão, não lê
dado e só grava medição na série a que está presa.

## ADDED Requirements

### Requirement: Admin ou o Mestre autor do desafio emite a credencial do sensor

O núcleo SHALL permitir a um **Admin** ou ao **Mestre autor do desafio** da série emitir
credencial de dispositivo, vinculada ao **Guerreiro(a) coletor** e à **série** que o sensor
alimenta. A emissão SHALL gravar o **identificador do aparelho** e a **trilha em que ele foi
construído**, e SHALL devolver o identificador e o **segredo**. Mestre que não é o autor do
desafio da série SHALL receber **403**; persona de qualquer outro papel SHALL receber **403**.
A credencial NEVER SHALL ser cadastro de aparelho à parte: ela é o próprio registro dele.
(`RF-01-67`, `RN-01-53`, documento 03 §1.1)

#### Scenario: Admin emite a credencial de uma série

- **WHEN** um Admin emite a credencial de dispositivo de uma série, informando o identificador
  do aparelho e a trilha em que ele foi construído
- **THEN** o núcleo cria a credencial vinculada ao Guerreiro(a) coletor e àquela série, e
  devolve o identificador e o segredo

#### Scenario: O Mestre autor do desafio emite

- **WHEN** o Mestre que criou o desafio de coleta da série emite a credencial dela
- **THEN** o núcleo cria a credencial, como faria para um Admin

#### Scenario: Mestre que não é autor do desafio é recusado

- **WHEN** um Mestre que não criou o desafio da série tenta emitir a credencial dela
- **THEN** o núcleo responde 403 e nenhuma credencial é criada

#### Scenario: Quem não é Admin nem Mestre não emite

- **WHEN** um Guerreiro(a), um responsável ou um Apoiador tenta emitir credencial de
  dispositivo
- **THEN** o núcleo responde 403 e nenhuma credencial é criada

#### Scenario: A credencial guarda a trilha em que o aparelho foi construído

- **WHEN** uma credencial de dispositivo emitida é consultada pela gestão
- **THEN** ela mostra o identificador do aparelho e a trilha em que ele foi construído, sem
  que exista qualquer outro registro de dispositivo no núcleo

### Requirement: O segredo é devolvido uma única vez e nunca recuperável

O núcleo SHALL guardar apenas o **resumo criptográfico** do segredo da credencial de
dispositivo. O segredo em claro SHALL ser apresentado **uma única vez**, no momento da emissão,
e NEVER SHALL ser recuperável depois — por rota, por consulta ou por leitura da base.
(`RF-01-67`)

#### Scenario: A base guarda só o resumo

- **WHEN** uma credencial de dispositivo é emitida
- **THEN** o registro dela contém o resumo criptográfico do segredo, e o segredo em claro não é
  gravado em lugar nenhum

#### Scenario: Segunda leitura não recupera o segredo

- **WHEN** alguém consulta uma credencial de dispositivo já emitida
- **THEN** a resposta traz os dados da credencial e nunca o segredo, mesmo para um Admin

#### Scenario: O segredo não aparece em registro operacional

- **WHEN** uma chamada autenticada por credencial de dispositivo é processada, aceita ou
  recusada
- **THEN** nenhum registro operacional do núcleo contém o segredo em claro

### Requirement: Entre as credenciais ativas nunca há duas para a mesma série

O núcleo SHALL manter, entre as credenciais de dispositivo **ativas**, no máximo **uma por
série**, e o par de **identificador e série** SHALL ser único entre elas. O aparelho que
alimenta mais de uma série SHALL ter **uma credencial por série**, todas com o **mesmo
identificador** — o identificador do aparelho NEVER SHALL ser tratado como único no núcleo.
Emissão para série que já tem credencial ativa SHALL ser recusada. (`RN-01-53`, documento
03 §1.1)

#### Scenario: Segunda credencial ativa para a mesma série é recusada

- **WHEN** um Admin tenta emitir credencial para uma série que já tem credencial ativa
- **THEN** o núcleo recusa a emissão, e a credencial existente permanece como está

#### Scenario: O mesmo aparelho alimenta séries distintas

- **WHEN** um Admin emite, para outra série do mesmo Guerreiro(a), credencial com o **mesmo
  identificador de aparelho** já usado em uma série
- **THEN** o núcleo cria a credencial, porque a unicidade é por série e não por identificador

#### Scenario: Revogada a anterior, a série aceita credencial nova

- **WHEN** a credencial ativa de uma série é revogada e um Admin emite outra para a mesma série
- **THEN** o núcleo cria a credencial nova, e a revogada permanece revogada

### Requirement: A credencial se confere a cada chamada e nunca abre sessão

O núcleo SHALL conferir a credencial de dispositivo **a cada chamada**, pelo identificador e
pelo segredo apresentados, e NEVER SHALL abrir sessão para ela nem devolver credencial de
sessão de espécie alguma. Chamada com identificador desconhecido, segredo que não confere ou
credencial revogada SHALL ser recusada. A **chave de aplicação** SHALL continuar exigida na
chamada, como em toda rota de dados. (`RN-08-23`, `RN-01-34`, `RF-01-48`)

#### Scenario: Chamada com credencial válida é processada

- **WHEN** um sensor apresenta identificador e segredo de uma credencial ativa, com chave de
  aplicação vigente
- **THEN** o núcleo processa a chamada segundo as demais regras da rota

#### Scenario: A credencial não rende sessão

- **WHEN** um sensor se autentica por credencial de dispositivo
- **THEN** o núcleo não abre sessão, não devolve credencial de sessão e não trata o aparelho
  como persona autenticada

#### Scenario: Segredo que não confere é recusado

- **WHEN** um sensor apresenta o identificador de uma credencial ativa com segredo diferente do
  emitido
- **THEN** o núcleo recusa a chamada e nada é gravado

#### Scenario: A chave de aplicação continua exigida

- **WHEN** um sensor apresenta credencial de dispositivo válida e nenhuma chave de aplicação
- **THEN** o núcleo responde 401, como faria com qualquer chamada sem chave

### Requirement: A credencial não lê dado e não escreve fora da sua série

O núcleo SHALL restringir a credencial de dispositivo a **uma única operação**: gravar registro
de coleta na **série a que ela está presa**. A credencial NEVER SHALL autorizar leitura de dado
algum, NEVER SHALL autorizar qualquer outra escrita e NEVER SHALL gravar registro em série
diferente da sua — nem em outra série do mesmo Guerreiro(a). (`RN-08-23`, `RN-01-34`)

#### Scenario: Registro em outra série é recusado

- **WHEN** um sensor autenticado pela credencial de uma série envia medição para série diferente
- **THEN** o núcleo recusa e nada é gravado, ainda que a outra série seja do mesmo Guerreiro(a)

#### Scenario: A credencial não lê

- **WHEN** uma chamada autenticada por credencial de dispositivo alcança qualquer rota de
  consulta
- **THEN** o núcleo recusa, porque a credencial não lê dado algum

#### Scenario: A credencial não alcança outra escrita

- **WHEN** uma chamada autenticada por credencial de dispositivo alcança qualquer rota de
  escrita que não seja a gravação de registro de coleta
- **THEN** o núcleo recusa a escrita

### Requirement: Admin ou o Mestre autor revoga a credencial, com motivo e autoria

O núcleo SHALL permitir a um **Admin** ou ao **Mestre autor do desafio** da série revogar a
credencial de dispositivo a qualquer tempo, registrando **motivo**, **autoria** e **data e hora**
da revogação. Revogação sem motivo SHALL ser recusada. O aparelho alcançado SHALL perder o
acesso na **chamada seguinte**. A revogação NEVER SHALL desfazer registro algum: as medições já
gravadas permanecem na série, porque o registro é somente inserção. (`RF-01-68`, `RN-08-10`)

A segunda metade do `RF-01-68` — a credencial **cair ao fim do vínculo do Guerreiro(a)** — SHALL
ser comportamento de **entrega posterior**, e a sua ausência aqui NEVER SHALL impedir a emissão,
a conferência ou a revogação por ato. O marco de fim do vínculo, definido no documento 03 §12.2,
não existe no núcleo: a via do pedido do responsável é do PRD-13, e a dos 12 meses sem atividade
registrada depende de critério que nenhum documento define. `VinculoJogador.data_fim` NEVER SHALL
ser tomado por esse marco — ele é o vínculo com a Comunidade Virtual, e não com o projeto.

#### Scenario: A revogação grava motivo e quem revogou

- **WHEN** um Admin revoga uma credencial de dispositivo informando o motivo
- **THEN** o núcleo grava o motivo, a autoria e a data e hora da revogação

#### Scenario: O Mestre autor do desafio revoga

- **WHEN** o Mestre que criou o desafio de coleta da série revoga a credencial dela
- **THEN** o núcleo revoga, como faria para um Admin

#### Scenario: Mestre que não é autor do desafio não revoga

- **WHEN** um Mestre que não criou o desafio da série tenta revogar a credencial dela
- **THEN** o núcleo responde 403, e a credencial permanece ativa

#### Scenario: Revogação sem motivo é recusada

- **WHEN** um Admin chama a revogação sem informar o motivo
- **THEN** o núcleo recusa, e a credencial permanece ativa

#### Scenario: O acesso cai na chamada seguinte

- **WHEN** o sensor cuja credencial foi revogada envia a medição seguinte
- **THEN** o núcleo recusa a chamada e nada é gravado

#### Scenario: Revogar não desfaz medição

- **WHEN** uma credencial de dispositivo é revogada
- **THEN** os registros que ela gravou permanecem na série, inalterados

#### Scenario: A transferência de comunidade não derruba a credencial

- **WHEN** o vínculo do Guerreiro(a) com uma Comunidade Virtual é encerrado
- **THEN** a credencial de dispositivo dele permanece ativa, porque esse não é o fim do vínculo
  de que trata o `RF-01-68`
