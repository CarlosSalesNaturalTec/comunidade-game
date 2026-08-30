## MODIFIED Requirements

### Requirement: Cinco condições recusam a entrega antes de qualquer escrita

O núcleo SHALL recusar a entrega com **422**, sem gravar nada e sem mover saldo algum, quando:

1. o tipo de recurso da recompensa for de natureza **durável** — o saldo durável é patrimônio e
   nunca lastreia recompensa;
2. o **lastro** não se confirmar no ato — a quantidade disponível do tipo no **ponto de apoio da
   entrega** for menor que a quantidade da recompensa;
3. a **quantidade** declarada na recompensa de marco já estiver esgotada pelas entregas
   anteriores;
4. o Mestre **não estiver vinculado à comunidade** do Guerreiro(a);
5. o Guerreiro(a) **não tiver desbloqueado a missão** declarada como marco.

O marco alcançado SHALL ser o **desbloqueio da missão** pelo Guerreiro(a), registrado pela
capacidade `desbloqueio-da-missao` — é o desbloqueio que libera a recompensa, e não a existência
de `Resultado` numa atividade da missão. Desbloqueio de missão em forma de desafio prático ainda
**não julgado** pelo Mestre autor NEVER SHALL contar como marco alcançado: enquanto o Mestre não
julga, a missão aguarda.

A resposta SHALL dizer qual das condições recusou. O lastro SHALL ser reverificado **no ato da
entrega**, e não na declaração do marco nem na publicação da trilha, porque a trilha é bem comum
e o saldo é de um ponto de apoio (`RF-07-13`, `RF-09-84`, `RN-07-07`, `RN-09-26`, `RN-09-27`,
invariante 9, 02 §8.1, 02 §8.2, documento 11 §2.2).

#### Scenario: Recompensa de tipo durável não é entregue

- **WHEN** um Mestre confirma a entrega de uma recompensa cujo tipo de recurso é de natureza
  durável
- **THEN** o núcleo responde 422 dizendo que o saldo durável é patrimônio, e nada é gravado

#### Scenario: Lastro é reverificado no ato da entrega

- **WHEN** um Mestre confirma a entrega de uma recompensa de quantidade 1 num ponto de apoio
  cujo saldo disponível daquele tipo é zero
- **THEN** o núcleo responde 422 dizendo que falta lastro, e nada é gravado

#### Scenario: Quantidade esgotada recusa a entrega

- **WHEN** um Mestre confirma a entrega de uma recompensa de marco de quantidade 30 que já teve
  30 entregas registradas
- **THEN** o núcleo responde 422 e nada é gravado

#### Scenario: Mestre de outra comunidade não entrega

- **WHEN** um Mestre confirma a entrega a um Guerreiro(a) de Comunidade Virtual diferente
  daquela a que ele está vinculado
- **THEN** o núcleo responde 422 e nada é gravado

#### Scenario: Marco não alcançado recusa a entrega

- **WHEN** um Mestre confirma a entrega a um Guerreiro(a) que ainda não desbloqueou a missão
  declarada como marco
- **THEN** o núcleo responde 422 dizendo que o marco não foi alcançado, e nada é gravado

#### Scenario: Desafio prático não julgado ainda não é marco alcançado

- **WHEN** o Guerreiro(a) declarou ter cumprido o desafio prático da missão declarada como marco
  e o Mestre autor ainda não julgou
- **THEN** o núcleo responde 422 dizendo que o marco não foi alcançado, e nada é gravado

#### Scenario: Resultado na atividade não alcança o marco sozinho

- **WHEN** um Mestre confirma a entrega a um Guerreiro(a) que tem Resultado lançado numa
  atividade da missão declarada como marco, mas ainda não a desbloqueou
- **THEN** o núcleo responde 422 dizendo que o marco não foi alcançado, e nada é gravado

#### Scenario: Recusa não move nada

- **WHEN** qualquer das cinco condições recusa a entrega
- **THEN** nenhuma entrega é gravada, nenhum lançamento é emitido e o saldo do ponto de apoio
  segue como estava

### Requirement: O Guerreiro(a) lê as recompensas que conquistou, entregues ou não

O núcleo SHALL expor, ao **Guerreiro(a) em sessão**, as recompensas de marco cujo **marco ele já
alcançou**, em qualquer trilha que percorra. Cada uma SHALL trazer a **trilha**, o **marco**, o
**tipo de recurso**, a **quantidade** e a **situação da entrega**: entregue, com a data, ou
**aguardando a confirmação do Mestre**. (`RF-05-45`, `RF-07-13`, `RN-09-26`)

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
## ADDED Requirements

### Requirement: O marco alcançado vira pendência de entrega para o Mestre

O núcleo SHALL expor ao **Mestre em sessão** a fila das **entregas pendentes**: cada par de
Guerreiro(a) e recompensa de marco cujo **marco ele desbloqueou** e cuja **entrega ainda não foi
confirmada**. Cada pendência SHALL trazer o Guerreiro(a) pelo **nick e avatar**, a trilha, a
missão que é o marco, o **tipo de recurso** e a **quantidade**.

A fila SHALL alcançar apenas os Guerreiros e Guerreiras da **Comunidade Virtual a que o Mestre
está vinculado** — a mesma condição que a entrega já exige — e NEVER SHALL se limitar às trilhas
de autoria dele: quem entrega é quem está no encontro, não quem escreveu a trilha. Mestre sem
vínculo vigente SHALL receber fila **vazia**, nunca erro. Persona que não é Mestre SHALL ser
recusada com **403**.

Confirmada a entrega, a pendência SHALL **sair** da fila. A pendência cuja quantidade declarada
já se esgotou nas entregas anteriores SHALL continuar na fila, marcada com o motivo, porque é o
Mestre quem precisa saber que falta recompensa a entregar — a fila diz o que o Guerreiro(a)
conquistou, e a recusa segue acontecendo no ato. A saída NEVER SHALL trazer valor em moedas nem
em reais, nem imagem real de Guerreiro(a). (`RF-09-75`, `RF-09-76`, `RN-09-26`, invariantes 12 e
16, PRD-09 §12)

#### Scenario: Marco desbloqueado aparece como pendência do Mestre

- **WHEN** um Guerreiro(a) da comunidade do Mestre desbloqueia a missão declarada como marco com
  recompensa
- **THEN** a fila do Mestre passa a trazer aquela pendência, com o nick e o avatar do
  Guerreiro(a), a trilha, o marco, o tipo de recurso e a quantidade

#### Scenario: Entrega confirmada sai da fila

- **WHEN** o Mestre confirma a entrega daquela recompensa àquele Guerreiro(a)
- **THEN** a pendência deixa de aparecer na fila dele

#### Scenario: A fila é da comunidade, não da autoria

- **WHEN** um Guerreiro(a) da comunidade do Mestre desbloqueia o marco de uma trilha escrita por
  outro Mestre
- **THEN** a pendência aparece na fila dele assim mesmo

#### Scenario: Guerreiro(a) de outra comunidade não aparece

- **WHEN** um Guerreiro(a) de Comunidade Virtual diversa da do Mestre desbloqueia um marco com
  recompensa
- **THEN** a pendência não aparece na fila daquele Mestre

#### Scenario: Mestre sem vínculo recebe fila vazia

- **WHEN** um Mestre sem vínculo vigente com comunidade alguma consulta a fila
- **THEN** recebe a fila vazia, e nenhum erro

#### Scenario: Quem não é Mestre não lê a fila

- **WHEN** uma persona que não é Mestre consulta a fila de entregas pendentes
- **THEN** o núcleo responde 403 e nada da fila é servido

#### Scenario: A fila não mostra custo nem imagem real

- **WHEN** o Mestre consulta a fila de entregas pendentes
- **THEN** nenhum campo traz valor em moedas ou em reais, e o Guerreiro(a) aparece por nick e
  avatar
