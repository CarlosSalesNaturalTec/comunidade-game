## ADDED Requirements

### Requirement: O Guerreiro(a) lê as recompensas que conquistou, entregues ou não

O núcleo SHALL expor, ao **Guerreiro(a) em sessão**, as recompensas de marco cujo **marco ele já
alcançou**, em qualquer trilha que percorra. Cada uma SHALL trazer a **trilha**, o **marco**, o
**tipo de recurso**, a **quantidade** e a **situação da entrega**: entregue, com a data, ou
**aguardando a confirmação do Mestre**. (`RF-05-45`, `RF-07-13`, `RN-09-26`)

O marco alcançado SHALL ser derivado do **mesmo percurso** que a recusa de entrega já confere na
capacidade — a consulta é uma só e não se duplica. A leitura NEVER SHALL antecipar as demais
condições da entrega — lastro no ponto de apoio e quantidade esgotada —, que são reverificadas
no ato pelo Mestre; ela diz o que foi conquistado, não o que será entregue.

A saída NEVER SHALL trazer valor em moedas nem em reais, pela mesma razão que o histórico de
entregas não os traz, e NEVER SHALL oferecer caminho de aquisição: recompensa de marco se
conquista e nunca se compra, com ponto de qualquer natureza. (`RF-05-46`, `RN-05-07`,
`RN-05-41`, invariantes 16 e 23)

#### Scenario: Marco alcançado aparece como conquistado

- **WHEN** um Guerreiro(a) alcança o marco declarado numa trilha que percorre
- **THEN** a recompensa daquele marco passa a aparecer na leitura dele, aguardando a confirmação
  do Mestre

#### Scenario: Marco não alcançado não aparece

- **WHEN** a trilha tem recompensa declarada num marco que o Guerreiro(a) ainda não alcançou
- **THEN** ela não aparece na leitura dele

#### Scenario: A recompensa entregue mostra a data

- **WHEN** o Mestre já confirmou a entrega
- **THEN** a mesma recompensa aparece como entregue, com a data da confirmação

#### Scenario: A leitura não antecipa a recusa da entrega

- **WHEN** o ponto de apoio está sem lastro do tipo de recurso da recompensa conquistada
- **THEN** ela continua aparecendo como conquistada e aguardando o Mestre, e a conferência do
  lastro segue acontecendo no ato da entrega

#### Scenario: Nenhum valor de custo chega à criança

- **WHEN** o Guerreiro(a) lê as recompensas conquistadas
- **THEN** nenhum campo traz valor em moedas nem em reais

#### Scenario: Só as próprias recompensas

- **WHEN** um Guerreiro(a) consulta esta leitura
- **THEN** recebe apenas as recompensas do próprio percurso, e nenhuma de outra criança
