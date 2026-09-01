## ADDED Requirements

### Requirement: O Apoiador declara o aporte pela App 08, e a declaração nasce pendente

O núcleo SHALL aceitar do **Apoiador em sessão** a declaração de um aporte em dinheiro, com o
**valor transferido**, o **comprovante** e a **origem da escolha** — uma necessidade de recurso
publicada, um valor sugerido da escada do perfil declarado ou um valor livre. A declaração
SHALL nascer **pendente** e NEVER SHALL, enquanto pendente, gerar lançamento, creditar saldo de
tipo de recurso, compor o Poder Sustentador ou abater o que falta a necessidade alguma. O
comprovante SHALL ser obrigatório e SHALL seguir os formatos já aceitos no pré-cadastro; sem
ele, ou em formato não aceito, o núcleo SHALL responder **422** com os formatos válidos.
(`RF-14-25`, `RF-14-26`, `RN-14-06`, `RN-14-07`, PRD-14 §§5.3, 9, 12)

#### Scenario: A declaração entra pendente e não credita

- **WHEN** o Apoiador declara um aporte com valor e comprovante
- **THEN** a declaração é gravada como pendente, nenhum lançamento é gerado e o Poder
  Sustentador dele permanece como estava

#### Scenario: A declaração por necessidade não abate o que falta

- **WHEN** o Apoiador declara o aporte escolhendo uma necessidade de recurso publicada
- **THEN** a declaração guarda a necessidade escolhida e a lista de necessidades continua
  mostrando a mesma quantidade faltante de antes

#### Scenario: Sem comprovante a declaração é recusada

- **WHEN** a declaração chega sem comprovante ou em formato não aceito
- **THEN** o núcleo responde 422 com os formatos válidos e nada é gravado

### Requirement: A declaração pela App 08 é sempre em dinheiro

O núcleo SHALL aceitar pela App 08 apenas o aporte em **dinheiro** e NEVER SHALL aceitar por
essa via aporte em material, serviço ou divulgação; recebendo a declaração de qualquer uma
dessas formas, SHALL responder **422** com a orientação de procurar a gestão, que os registra
com termo de doação ou registro do material. (`RF-14-28`, `RN-14-05`, PRD-14 §§3.2, 9, 12)

#### Scenario: Aporte em material devolve a orientação

- **WHEN** a declaração chega com forma de material, serviço ou divulgação
- **THEN** o núcleo responde 422 com a orientação de procurar a gestão e nada é gravado

### Requirement: O Apoiador acompanha a situação de cada declaração

O núcleo SHALL responder ao **Apoiador em sessão** a situação de cada declaração dele —
**pendente**, **homologada** ou **recusada** —, com o **valor declarado da transferência**, a
data, a origem da escolha e, na recusada, o **motivo** em linguagem simples. O valor sai como o
Apoiador o declarou, porque a valoração em moedas só nasce na homologação, pela vigência da
data do aporte (`RF-07-05`); apresentá-lo é da aplicação. A leitura SHALL alcançar apenas as
declarações do próprio Apoiador e NEVER SHALL exibir declaração de outra pessoa. (`RF-14-27`,
PRD-14 §§5.3, 9)

#### Scenario: As três situações aparecem ao Apoiador

- **WHEN** o Apoiador lê as próprias declarações
- **THEN** cada uma sai com a situação, o valor declarado, a data e a origem da escolha, e a
  recusada traz também o motivo

#### Scenario: A leitura não alcança declaração alheia

- **WHEN** o Apoiador lê as próprias declarações e existem declarações de outro Apoiador
- **THEN** a resposta traz apenas as dele

### Requirement: O Admin homologa a declaração registrando o aporte, e nunca a própria

O núcleo SHALL converter uma declaração pendente em aporte quando um **Admin** registrar o
aporte apontando a **declaração de origem**: o aporte SHALL nascer com **origem do registro
"App 08"**, SHALL ser valorado em moedas pela vigência da **data do aporte** e SHALL gerar o
lançamento de crédito, e a declaração SHALL passar a **homologada**. Registrar mais de um
aporte apontando a **mesma** declaração SHALL ser recusado com **422**. O Admin que homologa
NEVER SHALL ser o provedor da declaração; sendo, o núcleo SHALL responder **403**. (`RF-14-26`,
`RN-14-07`, `RN-14-08`, PRD-14 §§5.3, 8, 12)

#### Scenario: A homologação credita e fecha a declaração

- **WHEN** um Admin registra o aporte apontando a declaração de origem
- **THEN** o aporte é gravado com origem "App 08", convertido pela vigência da data do aporte,
  o lançamento de crédito é gerado e a declaração passa a homologada

#### Scenario: A mesma declaração não credita duas vezes

- **WHEN** um segundo aporte é registrado apontando uma declaração já homologada
- **THEN** o núcleo responde 422 e nada é gravado

#### Scenario: O provedor não homologa a própria declaração

- **WHEN** quem registra o aporte é o mesmo Apoiador que declarou
- **THEN** o núcleo responde 403 e nada é gravado

### Requirement: O Admin recusa a declaração com motivo, e a recusa não credita

O núcleo SHALL permitir que um **Admin** recuse uma declaração **pendente**, com **motivo
obrigatório**, e a declaração SHALL passar a **recusada**, com o motivo visível ao Apoiador que
a fez. A recusa NEVER SHALL gerar lançamento nem creditar moeda. Recusar declaração que não
esteja pendente SHALL ser respondido com **409**, e recusar sem motivo, com **422**.
(`RF-14-27`, `RN-14-07`, decisão do fundador de 2026-09-01)

#### Scenario: A recusa grava o motivo e não credita

- **WHEN** um Admin recusa uma declaração pendente com motivo
- **THEN** a declaração passa a recusada com o motivo, nenhum lançamento é gerado e o Poder
  Sustentador permanece como estava

#### Scenario: Declaração já resolvida não se recusa

- **WHEN** um Admin recusa uma declaração já homologada ou já recusada
- **THEN** o núcleo responde 409 e nada muda

#### Scenario: Recusa sem motivo não é aceita

- **WHEN** a recusa chega sem motivo
- **THEN** o núcleo responde 422 e a declaração continua pendente
