## Purpose

O canal pelo qual o responsável exerce, em nome do Guerreiro(a) sob a sua responsabilidade, o
direito de pedir acesso, correção, exclusão ou esclarecimento sobre os dados da criança: cada
pedido nasce com protocolo e prazo de 7 dias, é tratado pela gestão e tem o desfecho registrado
com quem tratou e quando.

## Requirements

### Requirement: O responsável abre a solicitação nos quatro tipos, com protocolo e prazo

O núcleo SHALL registrar a solicitação aberta por um responsável em sessão nos quatro tipos —
**acesso**, **correção**, **exclusão** e **esclarecimento** —, sempre sobre um Guerreiro(a) a que
ele esteja vinculado, com o texto do pedido. O registro SHALL nascer na situação **recebida**,
com **protocolo** e **prazo de 7 dias** contados do registro, e a resposta do envio SHALL trazer
o protocolo e o prazo, e nada mais. O responsável NEVER SHALL abrir solicitação sobre
Guerreiro(a) a que não esteja vinculado: a titularidade não se transfere, e ele exerce o direito
em nome da criança. (`RF-13-22`, `RF-13-24`, `RN-13-13`, `RN-13-14`, 03 §9)

#### Scenario: Pedido de acesso nasce com protocolo e prazo

- **WHEN** um responsável abre solicitação de acesso sobre um Guerreiro(a) a que está vinculado
- **THEN** o núcleo grava a solicitação na situação recebida e devolve o protocolo e o prazo de
  7 dias

#### Scenario: Pedido de exclusão é aceito como qualquer outro tipo

- **WHEN** um responsável abre solicitação do tipo exclusão
- **THEN** o núcleo a registra como as demais, sem recusar o pedido

#### Scenario: Guerreiro(a) não vinculado recusa a abertura

- **WHEN** um responsável abre solicitação sobre um Guerreiro(a) a que não está vinculado
- **THEN** o núcleo recusa com **403** e nada é gravado

#### Scenario: Só o responsável abre a solicitação

- **WHEN** uma persona de outro papel tenta abrir a solicitação do responsável
- **THEN** o núcleo recusa e nada é gravado

### Requirement: Segunda solicitação idêntica em aberto é recusada

O núcleo SHALL recusar com **409** a solicitação do **mesmo responsável**, sobre o **mesmo
Guerreiro(a)** e do **mesmo tipo** quando já houver uma sem desfecho, sem gravar nada. Tratada a
primeira, uma nova do mesmo tipo SHALL ser aceita. (`RF-13-22`, PRD-13 §9)

#### Scenario: Duplicata em aberto não entra na fila

- **WHEN** um responsável abre a segunda solicitação de correção sobre o mesmo Guerreiro(a) com a
  primeira ainda sem desfecho
- **THEN** o núcleo recusa com 409 e a fila segue com uma só

#### Scenario: Tratada a primeira, a nova é aceita

- **WHEN** a primeira solicitação recebeu desfecho e o responsável abre outra do mesmo tipo
- **THEN** o núcleo a registra normalmente, com protocolo e prazo próprios

### Requirement: O responsável acompanha as próprias solicitações

O núcleo SHALL devolver ao responsável em sessão **apenas as próprias** solicitações, com
protocolo, tipo, Guerreiro(a), situação, prazo, a marca de **em atraso** e, quando houver, o
desfecho e a data. Ele NEVER SHALL ler a solicitação de outro responsável. (`RF-13-25`,
`RF-13-26`, `RN-13-13`)

#### Scenario: A família vê protocolo, situação e prazo

- **WHEN** um responsável consulta as próprias solicitações
- **THEN** recebe, de cada uma, protocolo, tipo, situação e prazo

#### Scenario: A consulta não alcança a solicitação de outra família

- **WHEN** um responsável consulta as próprias solicitações
- **THEN** nenhuma solicitação aberta por outro responsável aparece

### Requirement: O atraso é derivado do prazo vencido e não fecha a solicitação

O núcleo SHALL identificar como **em atraso** a solicitação sem desfecho cujo prazo já venceu, e
essa marca SHALL ser **derivada** do prazo e do desfecho — NEVER uma situação gravada. A
solicitação em atraso SHALL permanecer **aberta** e tratável, e o atraso SHALL aparecer tanto
para o responsável quanto na fila do Admin. (`RF-02-66`, `RF-13-26`, `RN-13-14`)

#### Scenario: Prazo vencido sem desfecho marca o atraso

- **WHEN** passam 7 dias do registro sem desfecho
- **THEN** a solicitação aparece em atraso, para o responsável e para o Admin, e continua aberta

#### Scenario: Desfecho registrado encerra o atraso

- **WHEN** o Admin trata uma solicitação vencida
- **THEN** ela deixa de aparecer em atraso, com o desfecho e a data gravados

### Requirement: O Admin lê a fila e registra o desfecho com quem tratou e quando

O núcleo SHALL expor ao **Admin** a fila das solicitações do responsável, com protocolo, tipo,
responsável, Guerreiro(a), texto, situação, prazo e a marca de em atraso, da mais antiga para a
mais recente. O Admin SHALL registrar o desfecho — **aceita** ou **recusada** —, com o texto do
que foi tratado, e o núcleo SHALL gravar **quem tratou** e **quando**. Solicitação já tratada
NEVER SHALL receber segundo desfecho, e a fila NEVER SHALL ser alcançada por outro papel.
(`RF-02-23`, `RF-02-24`, `RN-13-14`)

#### Scenario: A fila chega ao Admin com o que a tela precisa

- **WHEN** o Admin lê a fila das solicitações do responsável
- **THEN** cada item traz protocolo, tipo, situação, prazo e a marca de em atraso

#### Scenario: O desfecho grava quem tratou e quando

- **WHEN** o Admin registra o desfecho de uma solicitação
- **THEN** o núcleo grava a situação final, o texto do desfecho, o Admin que tratou e a data e
  hora

#### Scenario: Solicitação tratada não recebe segundo desfecho

- **WHEN** o Admin tenta tratar uma solicitação que já tem desfecho
- **THEN** o núcleo recusa e o desfecho original permanece

#### Scenario: Mestre não alcança a fila do responsável

- **WHEN** um Mestre tenta ler a fila das solicitações do responsável ou registrar desfecho
- **THEN** o núcleo recusa

### Requirement: O desfecho registra o tratamento e não executa o pedido por si

O desfecho gravado nesta fila SHALL ser **registro do tratamento**, e NEVER SHALL, por si só,
apagar, despersonalizar ou alterar dado do Guerreiro(a). A execução do pedido de exclusão — a
despersonalização do registro de dado do território (`RN-13-12`) e o apagamento do _template_
biométrico (`RN-13-22`) — é do PRD-13 e NOT SHALL ser presumida como efeito automático do
desfecho. (`RF-02-24`, `RN-13-12`, `RN-13-22`)

#### Scenario: Desfecho de exclusão não apaga nada por si

- **WHEN** o Admin registra o desfecho aceito de uma solicitação de exclusão
- **THEN** o núcleo grava apenas o desfecho, e nenhum registro de território, _template_
  biométrico ou dado do Guerreiro(a) é apagado ou despersonalizado por esse ato
