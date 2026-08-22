## MODIFIED Requirements

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

## ADDED Requirements

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
