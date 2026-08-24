## ADDED Requirements

### Requirement: O Guerreiro(a) entra por nick e imagem, e a presença é registrada na entrada

A App 01 SHALL oferecer, no caminho das trilhas, a entrada por **nick e imagem**: o nick
informado na tela e o **descritor gerado no próprio aparelho**, na ordem prova de vivacidade e
depois descritor facial. Ao núcleo SHALL ir apenas o descritor; a fotografia SHALL ser
descartada sem sair do aparelho e NEVER SHALL ser exibida, gravada nem enviada.

Reconhecido o Guerreiro(a), a aplicação SHALL abrir a sessão dele e SHALL registrar a
**presença do dia no modo reconhecimento**, no mesmo atendimento. Presença já constante do
encontro NEVER SHALL ser duplicada nem tratada como erro: a aplicação SHALL avisar que ela já
existe e voltar à tela inicial. (`RF-04-18`, `RF-04-19`, `RF-04-29`, `RN-04-12`, `RN-04-06`,
PRD-04 §5.4)

#### Scenario: Nick e imagem conferem

- **WHEN** o Guerreiro(a) informa o nick e a câmera captura a imagem dele na chegada
- **THEN** a aplicação abre a sessão do Guerreiro(a) e registra a presença do dia por
  reconhecimento

#### Scenario: A presença do encontro já constava

- **WHEN** um Guerreiro(a) já com presença registrada naquela aula é reconhecido de novo
- **THEN** a aplicação avisa que a presença já existe, não duplica registro algum e volta à
  tela inicial

#### Scenario: Nenhuma imagem de criança sai do aparelho

- **WHEN** a entrada por nick e imagem acontece
- **THEN** nenhuma requisição carrega fotografia, e nenhuma imagem fica gravada no aparelho
  compartilhado

#### Scenario: Sem câmera, a entrada segue pela confirmação humana

- **WHEN** o aparelho não tem câmera disponível
- **THEN** a aplicação não oferece a captura e encaminha o Guerreiro(a) à confirmação de Mestre
  ou Admin, sem deixá-lo fora da aula

### Requirement: A falha de identificação oferece nova tentativa sem revelar nada

A App 01 SHALL responder à recusa do núcleo com a **mesma frase** em todos os casos — nick
inexistente, Guerreiro(a) sem _template_ gravado e descritor que não confere —, sem revelar
qual deles ocorreu, e SHALL oferecer **nova tentativa** de captura. Persistindo a falha, a
aplicação SHALL encaminhar à **confirmação de Mestre ou Admin**, e NEVER SHALL encerrar o
atendimento deixando o Guerreiro(a) fora da aula. (`RF-04-20`, `RN-01-22`, `RN-04-09`, PRD-04
§5.5)

#### Scenario: A imagem não confere

- **WHEN** o núcleo recusa a abertura da sessão por nick e imagem
- **THEN** a aplicação oferece nova tentativa com uma frase que não diz se o nick existe

#### Scenario: A falha persiste

- **WHEN** as tentativas de reconhecimento seguem falhando
- **THEN** a aplicação oferece o caminho da confirmação de Mestre ou Admin, que abre a sessão e
  registra a presença

#### Scenario: A frase da recusa não varia com a causa

- **WHEN** se comparam as telas de recusa de um nick inexistente e de um descritor que não
  confere
- **THEN** elas são indistinguíveis para quem está diante do aparelho

### Requirement: O Mestre ou o Admin recadastra a imagem de referência pela aplicação

A App 01 SHALL permitir que o **Mestre ou o Admin** em sessão de trabalho recadastre a imagem
de referência de um Guerreiro(a) atendido no encontro — captura ruim ou imagem que envelheceu
—, capturando nova imagem no aparelho e enviando **apenas o descritor**.

O identificador do Guerreiro(a) SHALL vir da **sessão dele já aberta** por confirmação
presencial, e NEVER SHALL ser obtido por consulta de nick: a App 01 NEVER SHALL dispor de rota
que resolva nick em identificador, e o alcance continua vedado pelo `RN-01-22`. A substituição
SHALL ficar registrada pelo núcleo. (`RF-04-22`, `RN-01-22`, `RN-04-12`, PRD-04 §5.5)

#### Scenario: A imagem de referência é substituída

- **WHEN** o Mestre recadastra a imagem de um Guerreiro(a) cuja sessão foi aberta por
  confirmação presencial
- **THEN** a aplicação captura nova imagem, envia só o descritor e o núcleo registra a
  substituição

#### Scenario: O recadastro não abre oráculo de nick

- **WHEN** se procura na aplicação um caminho que devolva o identificador de um Guerreiro(a) a
  partir do nick
- **THEN** nenhum existe: o identificador só aparece depois de uma sessão aberta por
  confirmação presencial

### Requirement: A App 01 não oferece a captura de quem já se cadastrou sem imagem

A App 01 NEVER SHALL oferecer, nesta fatia, a captura de imagem do Guerreiro(a) que **já se
cadastrou sem ela** — a criança cujo responsável comparece num encontro posterior. O que falta
não é o alcance do identificador, que esta fatia resolve, e sim rodar a jornada 5.2 sobre um
cadastro que já existe: vínculo do responsável, consentimento e só então a captura. O
Guerreiro(a) sem _template_ SHALL continuar atendido por inteiro pela confirmação humana, e
nenhuma recusa SHALL deixá-lo fora da aula. (`RF-04-16`, `RN-04-07`, `RN-04-09`, PRD-04 §5.2)

#### Scenario: O responsável comparece num encontro posterior

- **WHEN** um Guerreiro(a) cadastrado sem imagem volta ao encontro com o responsável
- **THEN** a aplicação não oferece a captura nesta fatia, e o Guerreiro(a) segue participando
  pela confirmação humana

## MODIFIED Requirements

### Requirement: O Guerreiro(a) entra no caminho das trilhas por confirmação de Mestre ou Admin

A App 01 SHALL abrir a sessão do Guerreiro(a) pela **confirmação de identidade** feita por
Mestre ou Admin presente no encontro, com registro de quem confirmou, e SHALL registrar, no
mesmo ato, a **presença do dia no modo confirmação**, com o mesmo adulto como confirmador. A
recusa de biometria e a ausência de _template_ NEVER SHALL deixar o Guerreiro(a) fora da aula:
a confirmação humana é a alternativa equivalente.

A confirmação humana deixa de ser o único caminho de entrada e passa a ser o que o `RN-04-09`
sempre disse que ela era — a alternativa de quem não tem _template_, de quem recusou a
biometria e de quem a câmera não reconheceu. A sessão que ela abre SHALL ter os mesmos direitos
da aberta por reconhecimento. (`RF-04-29`, `RF-04-15`, `RF-04-21`, `RN-04-09`, PRD-04 §§5.3,
5.5)

#### Scenario: Mestre confirma e a sessão do Guerreiro(a) abre

- **WHEN** o Guerreiro(a) informa o nick e o Mestre presente confirma a identidade dele
- **THEN** a aplicação abre a sessão do Guerreiro(a), registra quem confirmou e grava a
  presença do dia por confirmação

#### Scenario: A recusa não exclui ninguém da aula

- **WHEN** um Guerreiro(a) sem _template_ gravado chega ao caminho das trilhas
- **THEN** a aplicação o encaminha à confirmação humana, sem impedi-lo de participar

#### Scenario: A presença confirmada guarda quem confirmou

- **WHEN** a sessão é aberta por confirmação presencial
- **THEN** a presença gravada aponta o adulto que confirmou, e não o modo reconhecimento

#### Scenario: Nenhuma imagem de criança sai do aparelho nesta fatia

- **WHEN** a entrada acontece por confirmação humana
- **THEN** nenhuma requisição da aplicação carrega fotografia, e nenhuma imagem é gravada no
  aparelho compartilhado

## REMOVED Requirements

### Requirement: A App 01 não oferece entrada por imagem nem captura de quem já se cadastrou

**Reason**: A fatia que o requisito delimitava terminou. A entrada por reconhecimento facial
passa a ser oferecida (jornadas 5.4 e 5.5), e o motivo que ele dava — resolver o Guerreiro(a) a
partir do nick esbarraria no `RN-01-22` — não se sustenta: o identificador vem da sessão aberta
por confirmação presencial, não de consulta alguma.

**Migration**: O que dele continua valendo — a captura de quem já se cadastrou sem imagem
(`RF-04-16`) — passa ao requisito "A App 01 não oferece a captura de quem já se cadastrou sem
imagem", agora por recorte de fatia e não por bloqueio.
