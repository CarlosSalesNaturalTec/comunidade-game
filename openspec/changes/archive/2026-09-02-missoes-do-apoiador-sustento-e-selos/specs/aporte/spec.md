## MODIFIED Requirements

### Requirement: O Apoiador declara o aporte pela App 08, e a declaração nasce pendente

O núcleo SHALL aceitar do **Apoiador em sessão** a declaração de um aporte em dinheiro, com o
**valor transferido**, o **comprovante** e a **origem da escolha** — uma **missão aberta**, uma
necessidade de recurso publicada, um valor sugerido da escada do perfil declarado ou um valor
livre. Declarado por missão, o aporte SHALL apontar a missão escolhida e SHALL aceitar a
missão **inteira ou parte dela**; missão **concluída**, **vencida** ou inexistente SHALL ser
recusada com **409**, dizendo o que aconteceu com ela. A declaração SHALL nascer **pendente** e
NEVER SHALL, enquanto pendente, gerar lançamento, creditar saldo de tipo de recurso, compor o
Poder Sustentador, abater o que falta a necessidade ou missão alguma, ou concluir missão. O
comprovante SHALL ser obrigatório e SHALL seguir os formatos já aceitos no pré-cadastro; sem
ele, ou em formato não aceito, o núcleo SHALL responder **422** com os formatos válidos.
(`RF-14-25`, `RF-14-26`, `RF-14-63`, `RN-14-06`, `RN-14-07`, `RN-14-32`, PRD-14 §§5.3, 5.4, 9,
12)

#### Scenario: A declaração entra pendente e não credita

- **WHEN** o Apoiador declara um aporte com valor e comprovante
- **THEN** a declaração é gravada como pendente, nenhum lançamento é gerado e o Poder
  Sustentador dele permanece como estava

#### Scenario: A declaração por necessidade não abate o que falta

- **WHEN** o Apoiador declara o aporte escolhendo uma necessidade de recurso publicada
- **THEN** a declaração guarda a necessidade escolhida e a lista de necessidades continua
  mostrando a mesma quantidade faltante de antes

#### Scenario: A declaração por missão aceita a parte e não abate nada

- **WHEN** o Apoiador declara um aporte por parte do que uma missão aberta pede
- **THEN** a declaração guarda a missão escolhida e a missão continua mostrando o mesmo quanto
  falta de antes

#### Scenario: Missão fechada recusa a declaração

- **WHEN** o Apoiador declara aporte por uma missão já concluída ou vencida
- **THEN** o núcleo responde 409 dizendo o que aconteceu com a missão e nada é gravado

#### Scenario: Sem comprovante a declaração é recusada

- **WHEN** a declaração chega sem comprovante ou em formato não aceito
- **THEN** o núcleo responde 422 com os formatos válidos e nada é gravado

### Requirement: O Admin homologa a declaração registrando o aporte, e nunca a própria

O núcleo SHALL converter uma declaração pendente em aporte quando um **Admin** registrar o
aporte apontando a **declaração de origem**: o aporte SHALL nascer com **origem do registro
"App 08"**, SHALL ser valorado em moedas pela vigência da **data do aporte** e SHALL gerar o
lançamento de crédito, e a declaração SHALL passar a **homologada**. Registrar mais de um
aporte apontando a **mesma** declaração SHALL ser recusado com **422**. O Admin que homologa
NEVER SHALL ser o provedor da declaração; sendo, o núcleo SHALL responder **403**.

Sendo a declaração por **missão**, a mesma homologação SHALL abater o que falta àquela missão
e, quando o saldo fechar, SHALL concluí-la e creditar o selo dela a **cada participante**, no
mesmo ato. Fechando o saldo ou não, as moedas creditadas SHALL ser as do aporte de cada um.
(`RF-14-26`, `RF-14-64`, `RF-14-65`, `RF-14-66`, `RN-14-07`, `RN-14-08`, `RN-14-32`,
`RN-14-34`, PRD-14 §§5.3, 5.4, 8, 12)

#### Scenario: A homologação credita e fecha a declaração

- **WHEN** um Admin registra o aporte apontando a declaração de origem
- **THEN** o aporte é gravado com origem "App 08", convertido pela vigência da data do aporte,
  o lançamento de crédito é gerado e a declaração passa a homologada

#### Scenario: A homologação parcial abate e não conclui

- **WHEN** o Admin homologa uma declaração por missão que cobre parte do que ela pede
- **THEN** o quanto falta da missão cai pelo valor homologado, a missão segue aberta e nenhum
  selo é creditado

#### Scenario: A homologação que fecha o saldo conclui e credita os selos

- **WHEN** o Admin homologa a declaração que faz o que falta da missão chegar a zero
- **THEN** a missão passa a concluída e cada participante recebe o selo dela, cada um com as
  moedas do próprio aporte

#### Scenario: A mesma declaração não credita duas vezes

- **WHEN** um segundo aporte é registrado apontando uma declaração já homologada
- **THEN** o núcleo responde 422 e nada é gravado

#### Scenario: O provedor não homologa a própria declaração

- **WHEN** quem registra o aporte é o mesmo Apoiador que declarou
- **THEN** o núcleo responde 403 e nada é gravado
