## MODIFIED Requirements

### Requirement: Solicitação de participação carrega o pré-cadastro do Apoiador

O núcleo SHALL registrar na solicitação de participação a pretensão — Mestre ou Apoiador —,
os dados de contato, a apresentação e, quando a pretensão for Apoiador, o **aporte
declarado**, o **perfil declarado** — pessoa física ou jurídica —, o **comprovante anexado** e
o **nick** escolhido por quem se pré-cadastra. A validação do comprovante SHALL ser ato de
Admin, e o núcleo SHALL NOT coletar CPF, CNPJ ou documento de identidade de quem aporta, em
nenhum campo da solicitação.

O perfil SHALL ser guardado como veio, sem verificação, e SHALL sair na leitura que a gestão
faz da fila. Solicitação com pretensão de **Mestre** NÃO SHALL declarar perfil, que existe só
no pré-cadastro do Apoiador.

O comprovante SHALL ser aceito apenas em **PDF, JPG ou PNG**; recebido em outro formato, o
núcleo SHALL recusar a solicitação informando os formatos válidos, e nada SHALL ser gravado.

O nick declarado SHALL passar pela conferência restrita a nicks de adulto, e a solicitação
NEVER SHALL criar persona nem gravar o nick como nick de persona: até a aprovação do Admin ele
é apenas o nick pretendido. Solicitação com pretensão de **Mestre** NÃO SHALL declarar nick —
o Mestre o define no primeiro acesso. (`RF-01-25`, `RN-01-28`, `RN-01-29`, `RN-01-30`,
`RF-14-01`, `RF-14-04`, `RF-14-13`, `RN-14-03`, `RN-14-06`, `RN-14-39`, 02 §1)

#### Scenario: Pré-cadastro de Apoiador grava aporte declarado e comprovante

- **WHEN** um visitante envia a solicitação de participação com pretensão de Apoiador, o
  aporte declarado e o comprovante
- **THEN** o núcleo grava os três na solicitação, sem homologar o aporte e sem creditar moeda

#### Scenario: Pré-cadastro de Apoiador grava o perfil declarado

- **WHEN** a solicitação chega com pretensão de Apoiador e o perfil de pessoa física ou de
  pessoa jurídica
- **THEN** o núcleo grava o perfil na solicitação, sem verificá-lo, e a leitura da fila o
  devolve à gestão

#### Scenario: Solicitação de Mestre não declara perfil

- **WHEN** a solicitação chega com pretensão de Mestre e um perfil declarado
- **THEN** o núcleo recusa a solicitação, porque o perfil só existe no pré-cadastro do Apoiador

#### Scenario: Comprovante em formato não aceito é recusado

- **WHEN** a solicitação chega com comprovante em formato diferente de PDF, JPG ou PNG
- **THEN** o núcleo recusa a solicitação informando os formatos válidos, e nenhuma solicitação
  é gravada

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
