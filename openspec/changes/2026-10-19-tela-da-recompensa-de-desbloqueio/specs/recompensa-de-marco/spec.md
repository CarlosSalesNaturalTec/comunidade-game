# Spec Delta

## ADDED Requirements

### Requirement: A ciência da recompensa conquistada é fato do Guerreiro(a)

O núcleo SHALL registrar a **ciência** de uma recompensa de marco por um Guerreiro(a) — o ato
de ele ter sido avisado do que conquistou. A ciência SHALL ser **do par** recompensa e
Guerreiro(a), nunca da recompensa sozinha, que é uma só para quantos alcancem o marco. Só o
próprio Guerreiro(a) SHALL dar ciência das suas; persona que não é ele SHALL ser recusada com
**403**. Ciência NEVER SHALL ser entrega, NEVER SHALL creditar ponto e NEVER SHALL alterar a
situação da entrega. (`RF-05-45`, `RN-05-50`)

#### Scenario: O Guerreiro(a) dá ciência da recompensa que conquistou

- **WHEN** o Guerreiro(a) que alcançou o marco dá ciência daquela recompensa
- **THEN** o núcleo grava a ciência dele naquela recompensa, com o instante

#### Scenario: A ciência de um não alcança os colegas

- **WHEN** um integrante da equipe dá ciência de uma recompensa de marco
- **THEN** os demais Guerreiros e Guerreiras que alcançaram o mesmo marco seguem sem ciência

#### Scenario: Dar ciência de novo não duplica nem falha

- **WHEN** o Guerreiro(a) dá ciência de uma recompensa de que já tinha dado
- **THEN** o núcleo mantém a ciência que havia, sem criar uma segunda e sem erro

#### Scenario: Ciência de recompensa não conquistada é recusada

- **WHEN** o Guerreiro(a) dá ciência de uma recompensa cujo marco ele ainda não desbloqueou
- **THEN** o núcleo responde **422** e nada é gravado

#### Scenario: Ninguém dá ciência pelo outro

- **WHEN** alguém que não é o Guerreiro(a) dá ciência de uma recompensa dele
- **THEN** o núcleo responde **403** e nada é gravado

#### Scenario: A ciência não move a entrega nem o saldo

- **WHEN** a ciência é gravada
- **THEN** nenhuma entrega é registrada, nenhum lançamento é emitido, nenhum ponto é creditado
  e a recompensa segue aguardando a confirmação do Mestre

### Requirement: A ciência do desafio prático só nasce depois do julgamento

A recompensa de marco de missão cujo desbloqueio é **desafio prático** NEVER SHALL admitir
ciência enquanto o **Mestre autor** não tiver julgado que o Guerreiro(a) passou: antes do
julgamento o marco não está alcançado, e a recompensa não consta da leitura dele. É a mesma
condição que a recusa de entrega já confere na capacidade — a regra é uma só e não se duplica.
(`RF-05-14`, `RF-05-45`, `RN-05-50`)

#### Scenario: Declarou que cumpriu e o Mestre não julgou

- **WHEN** o Guerreiro(a) declarou ter cumprido o desafio prático da missão que é marco com
  recompensa e dá ciência dela
- **THEN** o núcleo responde **422** dizendo que o marco não foi alcançado, e nada é gravado

#### Scenario: Julgado como passou, a ciência é admitida

- **WHEN** o Mestre autor julga que o Guerreiro(a) passou no desafio prático daquela missão
- **THEN** a recompensa passa a constar da leitura dele sem ciência, e a ciência é admitida

## MODIFIED Requirements

### Requirement: O Guerreiro(a) lê as recompensas que conquistou, entregues ou não

O núcleo SHALL expor, ao **Guerreiro(a) em sessão**, as recompensas de marco cujo **marco ele já
alcançou**, em qualquer trilha que percorra. Cada uma SHALL trazer a **trilha**, o **marco**, o
**tipo de recurso** — com o **nome** e a **unidade** dele, e não só o identificador —, a
**quantidade**, a **situação da entrega** (entregue, com a data, ou **aguardando a confirmação
do Mestre**) e se o Guerreiro(a) já tem **ciência** dela. Sem o nome e a unidade do tipo, a
leitura não distingue o livro da camisa nem do kit, e quem a apresenta não tem o que dizer à
criança. (`RF-05-45`, `RF-07-13`, `RN-09-26`, `RN-05-50`)

O marco alcançado SHALL ser o **desbloqueio da missão**, o mesmo que a recusa de entrega já
confere na capacidade — a consulta é uma só e não se duplica. A leitura NEVER SHALL antecipar as demais
condições da entrega — lastro no ponto de apoio e quantidade esgotada —, que são reverificadas
no ato pelo Mestre; ela diz o que foi conquistado, não o que será entregue.

A saída NEVER SHALL trazer valor em moedas nem em reais, pela mesma razão que o histórico de
entregas não os traz, e NEVER SHALL oferecer caminho de aquisição: recompensa de marco se
conquista e nunca se compra, com ponto de qualquer natureza. (`RF-05-46`, `RN-05-07`,
`RN-05-41`, invariantes 16 e 23)

#### Scenario: Marco alcançado aparece como conquistado

- **WHEN** um Guerreiro(a) desbloqueia a missão declarada como marco numa trilha que percorre
- **THEN** a recompensa daquele marco passa a aparecer na leitura dele, aguardando a confirmação
  do Mestre

#### Scenario: Marco não alcançado não aparece

- **WHEN** a trilha tem recompensa declarada numa missão que o Guerreiro(a) ainda não
  desbloqueou
- **THEN** ela não aparece na leitura dele

#### Scenario: A recompensa entregue mostra a data

- **WHEN** o Mestre já confirmou a entrega
- **THEN** a mesma recompensa aparece como entregue, com a data da confirmação

#### Scenario: A leitura nomeia o recurso conquistado

- **WHEN** o Guerreiro(a) lê uma recompensa conquistada
- **THEN** ela traz o nome e a unidade do tipo de recurso, além da quantidade, e não apenas o
  identificador do tipo

#### Scenario: A leitura diz se já houve ciência

- **WHEN** o Guerreiro(a) lê as recompensas conquistadas depois de ter dado ciência de uma delas
- **THEN** aquela consta com ciência, e as demais sem

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
