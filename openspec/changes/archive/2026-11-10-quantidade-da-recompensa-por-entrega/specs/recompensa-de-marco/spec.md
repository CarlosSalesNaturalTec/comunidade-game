## ADDED Requirements

### Requirement: A entrega é recusada antes de qualquer escrita

O núcleo SHALL recusar a entrega com **422**, sem gravar nem mover saldo, quando o tipo for
**durável**, faltar **lastro** no ponto de apoio, o Mestre **não for da comunidade** do
Guerreiro(a), o **marco não tiver sido alcançado** ou o Guerreiro(a) **já tiver recebido**
aquela recompensa. A resposta SHALL dizer qual recusou (`RF-07-13`, `RF-09-84`, `RN-07-07`,
`RN-09-26`, invariante 9, 02 §8.1).

#### Scenario: Recompensa de tipo durável não é entregue

- **WHEN** um Mestre confirma a entrega de uma recompensa cujo tipo de recurso é de natureza
  durável
- **THEN** o núcleo responde 422 dizendo que o saldo durável é patrimônio, e nada é gravado

#### Scenario: Mestre de outra comunidade não entrega

- **WHEN** um Mestre confirma a entrega a um Guerreiro(a) de Comunidade Virtual diferente
  daquela a que ele está vinculado
- **THEN** o núcleo responde 422 e nada é gravado

#### Scenario: Recusa não move nada

- **WHEN** qualquer das condições recusa a entrega
- **THEN** nenhuma entrega é gravada, nenhum lançamento é emitido e o saldo do ponto de apoio
  segue como estava

### Requirement: O lastro é reverificado no ato da entrega

O núcleo SHALL conferir o lastro **no ato da entrega**, contra o saldo do tipo no ponto de apoio
de onde o recurso sai, e não na declaração do marco nem na publicação da trilha, porque a
trilha é bem comum e o saldo é de um ponto de apoio (`RF-07-13`, `RN-09-27`, invariante 9,
02 §8.1, documento 11 §2.2).

#### Scenario: Lastro é reverificado no ato da entrega

- **WHEN** um Mestre confirma a entrega de uma recompensa de quantidade 1 num ponto de apoio
  cujo saldo disponível daquele tipo é zero
- **THEN** o núcleo responde 422 dizendo que falta lastro, e nada é gravado

### Requirement: Uma entrega por Guerreiro(a), sem teto da turma

Entregas da mesma recompensa a **outros** Guerreiros e Guerreiras NEVER SHALL recusar a entrega:
a quantidade declarada é o que cada um recebe, não um teto da turma, e o que limita quantos
recebem é o lastro. A segunda entrega ao **mesmo** Guerreiro(a) SHALL ser recusada com 422
(`RF-07-13`, `RF-09-76`, decisão do fundador de 2026-11-09, 02 §8.1).

#### Scenario: Entregas anteriores não recusam a seguinte

- **WHEN** um Mestre confirma a entrega de uma recompensa de marco de quantidade 1 que já foi
  entregue a outro Guerreiro(a), num ponto de apoio com saldo
- **THEN** o núcleo grava a entrega e dá baixa de 1 unidade

#### Scenario: O mesmo Guerreiro(a) não recebe duas vezes

- **WHEN** um Mestre confirma a entrega de uma recompensa a um Guerreiro(a) que já a recebeu
- **THEN** o núcleo responde 422 dizendo que a recompensa já foi entregue a ele, e nada é
  gravado

### Requirement: O marco alcançado é o desbloqueio da missão

O marco alcançado SHALL ser o **desbloqueio da missão** pelo Guerreiro(a), registrado pela
capacidade `desbloqueio-da-missao`, e não a existência de `Resultado` numa atividade da missão.
Desbloqueio por desafio prático ainda **não julgado** pelo Mestre autor NEVER SHALL contar como
marco alcançado (`RF-09-84`, `RN-09-26`, 02 §8.1).

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

## MODIFIED Requirements

### Requirement: O Mestre autor declara qual marco concede qual recompensa

O núcleo SHALL permitir que o **Mestre autor da trilha** declare, para um marco dela, qual tipo
de recurso é concedido como recompensa e em que **quantidade**. A quantidade SHALL ser o que
**cada** Guerreiro(a) que alcança o marco recebe numa entrega, e NEVER SHALL ser lida como total
da turma (decisão do fundador de 2026-11-09, 02 §8.1). Só o Mestre autor SHALL escrever a
recompensa de marco da sua trilha, como já vale para todo o restante dela.

O marco SHALL ser uma **missão** da trilha — o marco de uso corrente do documento 02 §8.1, e por
onde saem a camisa, o livro e o kit. As outras três espécies que o documento 02 §8.1 admite —
etapa, batalha e culminância — NÃO SHALL ser aceitas enquanto o núcleo não puder verificar que
foram alcançadas: `Batalha` é do PRD-10 e `Culminancia`, do PRD-09, e a etapa do ciclo ainda não
é atributo da `Missao`. Declarar marco inverificável tornaria inexequível a recusa por marco não
alcançado, do mesmo modo que a trilha sem ponto de apoio tornava inexequível a conferência de
lastro na publicação.

A declaração NEVER SHALL aceitar preço, saldo de pontos ou qualquer contrapartida do
Guerreiro(a): a recompensa de marco é **conquistada, nunca comprada nem trocada** (`RF-09-71`,
`RN-09-26`, `RN-09-39`, invariante 23, 02 §8.1).

#### Scenario: Mestre autor declara a recompensa de um marco

- **WHEN** o Mestre autor de uma trilha declara que o desbloqueio de uma missão dela concede 1
  unidade de um tipo de recurso
- **THEN** o núcleo grava a recompensa de marco com a trilha, o marco, o tipo e a quantidade, que
  é o que cada Guerreiro(a) receberá na entrega

#### Scenario: Mestre que não é autor não declara

- **WHEN** um Mestre que não é autor da trilha tenta declarar uma recompensa de marco nela
- **THEN** o núcleo recusa e nada é gravado

#### Scenario: A declaração não aceita preço

- **WHEN** chega uma declaração de recompensa de marco com preço em pontos extras ou em moedas
- **THEN** o núcleo responde 422 e nada é gravado

#### Scenario: Marco que não é missão é recusado

- **WHEN** o Mestre autor declara uma recompensa de marco cujo marco é etapa, batalha ou
  culminância
- **THEN** o núcleo responde 422 dizendo que só a missão é aceita como marco, e nada é gravado

### Requirement: O Mestre da comunidade confirma a entrega

O núcleo SHALL registrar a entrega da recompensa de marco a um Guerreiro(a) por ato de **Mestre
vinculado à Comunidade Virtual do Guerreiro(a)**, gravando o **ponto de apoio** de onde o
recurso saiu, o Mestre que entregou e a data. A entrega SHALL ser **uma por Guerreiro(a)** que
alcança o marco e SHALL entregar a **quantidade declarada**, inteira, a esse Guerreiro(a). A
`RecompensaDeMarco` NEVER SHALL guardar situação de entrega própria nem teto de entregas: cada
entrega é registro próprio, e o que limita quantos recebem é o lastro do ponto de apoio
(decisão do fundador de 2026-11-09, 02 §8.1).

O Admin NEVER SHALL ser quem confirma a entrega: quem estava no encontro é quem entrega
(`RF-07-13`, `RF-09-76`, `RF-02-50`, `RF-02-51`, `RN-02-17`, 02 §8.1, 05 §3).

#### Scenario: Mestre da comunidade entrega a recompensa

- **WHEN** um Mestre vinculado à comunidade de um Guerreiro(a) que alcançou o marco confirma a
  entrega num ponto de apoio com saldo
- **THEN** o núcleo grava a entrega com o Guerreiro(a), o ponto de apoio, o Mestre e a data

#### Scenario: Duas entregas da mesma recompensa de marco

- **WHEN** dois Guerreiros e Guerreiras alcançam o mesmo marco e recebem a recompensa
- **THEN** o núcleo grava duas entregas, e a recompensa de marco segue sem situação de entrega
  própria

#### Scenario: Recompensa de quantidade 1 chega a todos que alcançaram o marco

- **WHEN** a recompensa declara quantidade 1, três Guerreiros e Guerreiras alcançaram o marco e o
  ponto de apoio tem saldo de 3 unidades
- **THEN** o núcleo grava as três entregas, cada uma com baixa de 1 unidade, e nenhuma é
  recusada por já ter havido entrega anterior

#### Scenario: Admin não confirma a entrega

- **WHEN** um Admin tenta confirmar a entrega de uma recompensa de marco
- **THEN** o núcleo recusa e nada é gravado

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
condições da entrega — como o lastro no ponto de apoio —, que são reverificadas no ato pelo
Mestre; ela diz o que foi conquistado, não o que será entregue.

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

### Requirement: O marco alcançado vira pendência de entrega para o Mestre

O núcleo SHALL expor ao **Mestre em sessão** a fila das **entregas pendentes**: cada par de
Guerreiro(a) e recompensa de marco cujo **marco ele desbloqueou** e cuja **entrega ainda não foi
confirmada**. Cada pendência SHALL trazer o Guerreiro(a) pelo **nick e avatar**, a trilha, a
missão que é o marco, o **tipo de recurso** e a **quantidade**.

A fila SHALL alcançar apenas os Guerreiros e Guerreiras das **Comunidades Virtuais a que o
Mestre está vinculado** — a mesma condição que a entrega já exige — e NEVER SHALL se limitar às
trilhas de autoria dele: quem entrega é quem está no encontro, não quem escreveu a trilha.
Estando o Mestre vinculado a mais de uma comunidade, a fila SHALL trazer as pendências de
**todas elas**. Mestre sem vínculo com comunidade alguma SHALL receber fila **vazia**, nunca
erro. Persona que não é Mestre SHALL ser recusada com **403**.

Confirmada a entrega, a pendência SHALL **sair** da fila. A fila diz o que o Guerreiro(a)
conquistou e NEVER SHALL marcar a pendência como esgotada pelas entregas a outros Guerreiros e
Guerreiras: a quantidade é o que cada um recebe, e a recusa por lastro segue acontecendo no ato
(decisão do fundador de 2026-11-09). A saída NEVER SHALL trazer valor em moedas nem
em reais, nem imagem real de Guerreiro(a). (`RF-09-75`, `RF-09-76`, `RN-09-26`, invariantes 12 e
16, PRD-09 §12)

#### Scenario: Marco desbloqueado aparece como pendência do Mestre

- **WHEN** um Guerreiro(a) da comunidade do Mestre desbloqueia a missão declarada como marco com
  recompensa
- **THEN** a fila do Mestre passa a trazer aquela pendência, com o nick e o avatar do
  Guerreiro(a), a trilha, o marco, o tipo de recurso e a quantidade

#### Scenario: A fila reúne as pendências de todas as comunidades do Mestre

- **WHEN** um Mestre vinculado a duas comunidades consulta a fila, e há marco desbloqueado com
  recompensa em cada uma delas
- **THEN** a fila traz as pendências das duas

#### Scenario: Entrega confirmada sai da fila

- **WHEN** o Mestre confirma a entrega daquela recompensa àquele Guerreiro(a)
- **THEN** a pendência deixa de aparecer na fila dele

#### Scenario: A entrega a um não marca a pendência dos outros

- **WHEN** o Mestre entrega a recompensa de quantidade 1 a um Guerreiro(a), e outros dois da
  mesma comunidade alcançaram o mesmo marco
- **THEN** a pendência dos outros dois segue na fila, sem marca de esgotada

#### Scenario: A fila é da comunidade, não da autoria

- **WHEN** um Guerreiro(a) da comunidade do Mestre desbloqueia o marco de uma trilha escrita por
  outro Mestre
- **THEN** a pendência aparece na fila dele assim mesmo

#### Scenario: Guerreiro(a) de outra comunidade não aparece

- **WHEN** um Guerreiro(a) de Comunidade Virtual diversa das do Mestre desbloqueia um marco com
  recompensa
- **THEN** a pendência não aparece na fila daquele Mestre

#### Scenario: Mestre sem vínculo recebe fila vazia

- **WHEN** um Mestre sem vínculo com comunidade alguma consulta a fila
- **THEN** recebe a fila vazia, e nenhum erro

#### Scenario: Quem não é Mestre não lê a fila

- **WHEN** uma persona que não é Mestre consulta a fila de entregas pendentes
- **THEN** o núcleo responde 403 e nada da fila é servido

#### Scenario: A fila não mostra custo nem imagem real

- **WHEN** o Mestre consulta a fila de entregas pendentes
- **THEN** nenhum campo traz valor em moedas ou em reais, e o Guerreiro(a) aparece por nick e
  avatar

## REMOVED Requirements

### Requirement: Cinco condições recusam a entrega antes de qualquer escrita

**Reason**: a recusa por "quantidade esgotada" lia a quantidade declarada como teto da turma, e o
lastro e a baixa a leem como o que cada Guerreiro(a) recebe. Decisão do fundador de 2026-11-09
(02 §8.1): a quantidade é por entrega, e o limite é o lastro.

**Migration**: substituído por quatro requisitos — "A entrega é recusada antes de qualquer
escrita", "O lastro é reverificado no ato da entrega", "Uma entrega por Guerreiro(a), sem teto
da turma" e "O marco alcançado é o desbloqueio da missão" —, com os mesmos cenários, menos a
quantidade esgotada. A recusa da segunda entrega ao mesmo Guerreiro(a) aplica no núcleo o "uma
por Guerreiro(a)" que a spec já exigia e que só a fila garantia. Nenhum dado muda.
