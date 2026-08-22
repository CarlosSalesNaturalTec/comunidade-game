## ADDED Requirements

### Requirement: A aplicação reúne as filas numa lista só, com filtro por natureza

A App 03 SHALL apresentar as solicitações numa **área Filas** única, com **filtro por
natureza**, e NEVER SHALL abrir uma área separada por natureza. Cada item SHALL mostrar a
natureza a que pertence, quem enviou, a situação e o prazo, e SHALL distinguir visualmente o
que está **em atraso** — por rótulo e não apenas por cor. (`RF-02-18`, `RF-02-65`,
`RF-02-25`, PRD-02 §10, documento 15 §5)

A área SHALL ser aberta apenas por **Admin**; para os demais papéis a aplicação SHALL
apresentar a recusa em linguagem simples, e não um erro cru. (`RN-02-01`, `RF-01-16`)

Nesta fatia a área SHALL servir a natureza **participação**; as demais SHALL entrar sem que a
lista, o filtro ou a apresentação do atraso mudem de forma. (PRD-02 §6.2)

#### Scenario: Admin abre a área Filas

- **WHEN** um Admin em sessão abre a área Filas
- **THEN** vê as solicitações numa lista só, com o filtro por natureza e, em cada item, a
  natureza, quem enviou, a situação e o prazo

#### Scenario: O atraso é anunciado por rótulo, não só por cor

- **WHEN** a lista traz uma solicitação em atraso
- **THEN** ela vem com um rótulo textual que diz isso, legível também sem distinguir cores

#### Scenario: Quem não é Admin lê a recusa, não um erro

- **WHEN** um Mestre em sessão abre a área Filas
- **THEN** a aplicação explica em linguagem simples que a área é do Admin, sem exibir código
  nem mensagem técnica

### Requirement: O Admin avalia a solicitação de participação pela aplicação

A App 03 SHALL oferecer ao Admin o desfecho da solicitação de participação — **aceitar** ou
**recusar** — com o **parecer** informado na própria tela, e SHALL apresentar, depois do
desfecho, a situação final, o parecer, quem avaliou e a data. A recusa SHALL exigir o motivo
no parecer antes de chamar o núcleo. (`RF-02-19`, `RF-02-86`)

A tela SHALL apresentar a identificação, a pretensão, a apresentação, a instituição, os links
declarados e, no pré-cadastro de Apoiador, o **aporte declarado** e o **nick pretendido**.
(`RF-02-18`, `RF-02-83`)

A aplicação SHALL apresentar em linguagem simples a recusa do núcleo por solicitação já
avaliada, e NEVER SHALL oferecer reavaliação de solicitação com desfecho gravado.

#### Scenario: Admin aceita e vê o desfecho registrado

- **WHEN** um Admin aceita uma solicitação informando o parecer
- **THEN** a tela passa a mostrar a situação aceita, o parecer, quem avaliou e a data

#### Scenario: Recusa sem motivo é apontada antes de chamar o núcleo

- **WHEN** um Admin escolhe recusar e confirma com o parecer vazio
- **THEN** a aplicação aponta o campo em falta junto do rótulo dele, e nada é enviado ao núcleo

#### Scenario: Solicitação já avaliada não oferece desfecho

- **WHEN** o Admin abre uma solicitação que já tem desfecho gravado
- **THEN** a tela mostra o desfecho e não oferece aceitar nem recusar

### Requirement: A solicitação aceita abre o cadastro pré-preenchido, sem criar acesso

A App 03 SHALL oferecer, a partir de uma solicitação **aceita**, a abertura do cadastro de
**Mestre** ou de **Apoiador** conforme a pretensão declarada, com os campos **pré-preenchidos**
pelo que a solicitação trouxe. O cadastro SHALL continuar sendo ato explícito do Admin: aceitar
a solicitação NEVER SHALL criar persona, credencial ou acesso por si só. (`RF-02-20`,
`RN-02-03`, `RN-01-28`)

O pré-preenchimento SHALL ser editável pelo Admin antes da confirmação, e o cadastro SHALL
passar pelas mesmas exigências de sempre — entre elas ao menos um artefato comprobatório de
Mestre ou Apoiador. (`RF-02-04`, `RN-02-01`)

#### Scenario: Aceitar não cadastra ninguém

- **WHEN** um Admin aceita uma solicitação de participação
- **THEN** nenhuma persona passa a existir, e a aplicação apenas oferece abrir o cadastro

#### Scenario: O cadastro abre com o que a solicitação trouxe

- **WHEN** o Admin abre o cadastro a partir de uma solicitação aceita com pretensão de Apoiador
- **THEN** o formulário de Apoiador aparece com os dados da solicitação já preenchidos e
  editáveis

#### Scenario: O cadastro pré-preenchido cumpre as mesmas exigências

- **WHEN** o Admin confirma o cadastro pré-preenchido sem nenhum artefato comprobatório
- **THEN** a aplicação aponta a falta e o cadastro não é criado

### Requirement: O Admin homologa pela aplicação o aporte declarado no pré-cadastro

A App 03 SHALL oferecer ao Admin, sobre uma solicitação de participação com **aporte
declarado**, o registro do aporte apontando a solicitação de origem, e SHALL apresentar depois
o valor **em moedas** creditado. A tela NEVER SHALL apresentar o aporte em reais.
(`RF-02-84`, `RF-07-30`, `RN-02-19`, `RN-07-21`, invariante 16 do documento 99 §6)

A aplicação SHALL apresentar em linguagem simples a recusa do núcleo por solicitação **já
homologada**, e SHALL deixar de oferecer a homologação depois que ela ocorreu.

#### Scenario: Admin homologa o aporte declarado

- **WHEN** um Admin registra o aporte apontando a solicitação de participação de origem
- **THEN** a tela passa a mostrar o aporte homologado, com o valor em moedas

#### Scenario: A homologação não se repete

- **WHEN** o Admin abre uma solicitação cujo aporte declarado já foi homologado
- **THEN** a tela mostra a homologação registrada e não oferece homologar de novo

#### Scenario: O aporte aparece em moedas, nunca em reais

- **WHEN** a tela apresenta um aporte homologado
- **THEN** o valor aparece em moedas da plataforma, e nenhum valor em reais é exibido
