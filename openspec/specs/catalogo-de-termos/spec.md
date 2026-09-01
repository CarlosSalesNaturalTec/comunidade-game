## Purpose

O texto dos termos que a plataforma apresenta ao responsável: cada versão guardada com o que
ela diz, a versão vigente, o histórico que responde pela versão que valia numa data e o
registro de que o responsável leu — a prova de ciência que sustenta a hipótese H2.

## Requirements

### Requirement: O núcleo guarda o texto de cada versão do termo

O núcleo SHALL guardar, por **tipo de termo** e por **versão**, o **texto** que aquela versão
apresenta ao responsável, em **linguagem simples** — sem jargão jurídico e sem termo técnico —,
com a data em que a versão passou a valer. A versão **vigente** SHALL ser a que a configuração
do núcleo carimba nos consentimentos: nenhuma rota SHALL escolher, criar ou editar versão de
termo, e trocar o termo SHALL continuar sendo trocar a configuração. (`RF-13-32`, `RN-01-12`,
PRD-13 §§6.5, 9)

A leitura do catálogo SHALL exigir persona autenticada, de **qualquer papel**, e NEVER SHALL
exigir vínculo com Guerreiro(a): o texto do termo não é dado de criança.

#### Scenario: A consulta devolve o termo vigente com o texto

- **WHEN** uma persona autenticada consulta os termos
- **THEN** o núcleo devolve a versão vigente de cada tipo, com o texto que ela apresenta e a
  data em que passou a valer

#### Scenario: A consulta sem credencial de persona é recusada

- **WHEN** o catálogo de termos é chamado sem credencial de persona
- **THEN** o núcleo recusa com 401

#### Scenario: Nenhuma rota cria ou edita termo

- **WHEN** qualquer persona, inclusive Admin, tenta criar ou alterar o texto ou a versão de um
  termo por rota
- **THEN** não há rota que o faça, e a versão vigente continua sendo a da configuração

### Requirement: O histórico responde pela versão que valia em cada data

O núcleo SHALL devolver, além da vigente, as **versões anteriores** de cada tipo de termo, cada
uma com o texto e o período em que valeu, de modo que a pergunta "o que este termo dizia
naquela data" seja respondida sem reconstituição. (`RF-13-33`, PRD-13 §6.5)

#### Scenario: O histórico traz as versões anteriores

- **WHEN** uma persona autenticada consulta o histórico de um tipo de termo
- **THEN** o núcleo devolve as versões anteriores, cada uma com o texto e o período em que valeu

#### Scenario: A versão de uma data é identificável

- **WHEN** um consentimento gravado aponta uma versão de termo já substituída
- **THEN** o texto daquela versão continua consultável, e não o da versão vigente

### Requirement: O termo declara a entrega gratuita e anonimizada dos dados

O texto do termo apresentado ao responsável SHALL declarar que os dados produzidos pela
participação **podem ser entregues a pesquisadores e a gestores públicos**, e SHALL dizer, em
linguagem simples: que a entrega é **gratuita**; que sai **anonimizada**, sem nome, sem nick e
sem vínculo de autoria; que **depende de aprovação de um Admin caso a caso**, com solicitante
identificado, finalidade declarada e compromisso de não reidentificar, respondida em **7 dias**;
que o pedido, a resposta e o que foi entregue ficam **registrados**; e que quem usa o dado
**credita a comunidade** e o derivado **herda a mesma licença** (CC BY-SA). (`RF-13-34`,
`RN-13-19`, documento 03 §12.3)

O texto NEVER SHALL prometer ao responsável recusa ou opt-out dessa entrega: o que sai é
anônimo, e a declaração é de transparência, não de consentimento à parte.

#### Scenario: O termo vigente declara a entrega

- **WHEN** o responsável lê o termo vigente
- **THEN** encontra a declaração da entrega gratuita e anonimizada, a aprovação caso a caso do
  Admin e a licença que obriga a creditar a comunidade

#### Scenario: A declaração não vira consentimento à parte

- **WHEN** o responsável lê a cláusula de entrega de dados
- **THEN** não lhe é oferecida decisão separada sobre ela, e recusá-la não é caminho da tela

### Requirement: A leitura do termo é registrada, com data e hora

O núcleo SHALL registrar a **leitura do termo** por um responsável, guardando **quem leu**, a
**versão lida** e a **data e hora com fuso**. O registro SHALL ser **permanente** — é prova de
ciência e o instrumento que mede a hipótese H2 — e SHALL ser **um por responsável e versão**:
reler a mesma versão NEVER SHALL gerar segundo registro, e a data do primeiro SHALL permanecer.

O registro SHALL ser ato do **responsável** em sessão; qualquer outro papel SHALL receber
**403**. Versão que não existe no catálogo SHALL ser recusada com **404**. O registro de leitura
NEVER SHALL valer como consentimento: ler o termo não concede nem revoga autorização.
(`RF-13-32`, PRD-13 §§11, 12)

#### Scenario: O responsável registra a leitura do termo vigente

- **WHEN** um responsável em sessão registra a leitura da versão vigente
- **THEN** o núcleo grava quem leu, a versão e a data e hora com fuso

#### Scenario: A releitura da mesma versão não gera segundo registro

- **WHEN** o mesmo responsável registra de novo a leitura da mesma versão
- **THEN** nenhum registro novo é criado, e a data do primeiro permanece

#### Scenario: Ler o termo não concede autorização

- **WHEN** um responsável registra a leitura do termo da autorização única
- **THEN** o estado da autorização do vinculado permanece o que era, e nenhum consentimento é
  gravado

#### Scenario: Quem não é responsável não registra leitura

- **WHEN** um Mestre, um Apoiador ou um Guerreiro(a) tenta registrar a leitura de um termo
- **THEN** o núcleo responde 403 e nada é gravado

#### Scenario: Versão inexistente é recusada

- **WHEN** a leitura é registrada sobre uma versão que não está no catálogo
- **THEN** o núcleo responde 404 e nada é gravado
