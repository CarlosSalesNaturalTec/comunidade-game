## ADDED Requirements

### Requirement: A área Filas ganha a natureza dos desafios extras

A App 03 SHALL apresentar, na área **Filas** já existente, a natureza **desafios extras**, sob o
mesmo filtro por natureza das demais, e NEVER SHALL abrir área separada para ela. A lista SHALL
trazer só os desafios **já validados pelo Mestre da trilha** e SHALL mostrar de cada um a
trilha, a missão quando houver, a **modalidade**, a **recompensa** com o tipo de recurso, a
**quantidade**, o **ponto de apoio**, o **critério de atribuição**, os **pontos extras**, o
**formato**, o **custeio** e a **vigência**, além da marca de **lastro provido** ou do que falta
prover. A natureza é da gestão: NEVER SHALL ser alcançada por Mestre. Sem desafio algum na fila,
a aplicação SHALL informá-lo como informação, nunca como falha. (`RF-02-27`, `RN-02-10`,
PRD-02 §5.8)

#### Scenario: O filtro alcança os desafios extras

- **WHEN** um Admin em sessão abre a área Filas e escolhe a natureza dos desafios extras
- **THEN** a aplicação apresenta os desafios validados pelo Mestre, cada um com a recompensa, o
  critério, os pontos extras e a vigência

#### Scenario: Desafio sem validação do Mestre não é oferecido

- **WHEN** um Admin abre a natureza dos desafios extras e há uma proposta ainda em validação do
  Mestre
- **THEN** a proposta não aparece na lista

#### Scenario: A fila diz o que falta de lastro

- **WHEN** o desafio da fila está sem lastro provido
- **THEN** o item traz o que falta prover, e não apenas que falta

#### Scenario: Fila vazia não é falha

- **WHEN** não há desafio algum aguardando aprovação
- **THEN** a aplicação informa que a fila está vazia, como informação

#### Scenario: O Mestre não alcança a natureza

- **WHEN** um Mestre em sessão abre a área Filas
- **THEN** a natureza dos desafios extras não lhe é oferecida

### Requirement: A tela do desafio extra aprova com lastro ou recusa com motivo

A App 03 SHALL oferecer, sobre o desafio escolhido, a tela com o que a proposta oferece e as
duas saídas: **aprovar**, que publica o desafio, e **recusar**, que exige o **motivo**, apontado
no próprio campo antes de chamar o núcleo. A aprovação SHALL ser oferecida apenas quando o
**lastro da recompensa** estiver provido; faltando o lastro, a aplicação SHALL apresentar o que
falta prover no lugar da aprovação. Recusada a aprovação pelo núcleo — por falta de lastro, por
falta de disponível ou por validação do Mestre ausente —, a aplicação SHALL apresentar o motivo
devolvido e manter o desafio na fila. (`RF-02-28`, `RN-02-11`, `RF-07-39`, invariante 9)

#### Scenario: Sem lastro a aprovação não é oferecida

- **WHEN** o Admin abre um desafio cujo lastro não está provido
- **THEN** a aplicação mostra o que falta prover e não oferece o botão de aprovar

#### Scenario: Recusa sem motivo é apontada na tela

- **WHEN** o Admin recusa o desafio sem escrever o motivo
- **THEN** a aplicação aponta a falta no próprio campo e não chama o núcleo

#### Scenario: A aprovação publica e tira o desafio da fila

- **WHEN** o Admin aprova um desafio com lastro provido e recompensa que cabe na disponível
- **THEN** a aplicação informa que o desafio foi publicado e ele deixa de aparecer na fila

#### Scenario: A recusa do núcleo por falta de disponível aparece na tela

- **WHEN** o Admin aprova um desafio cuja recompensa não cabe na quantidade disponível
- **THEN** a aplicação apresenta o motivo devolvido pelo núcleo e o desafio segue na fila

### Requirement: A gestão encerra o desafio publicado e mostra o que a recompensa comprometeu

A App 03 SHALL apresentar, na mesma natureza da área Filas, os desafios extras **publicados**,
com a **quantidade restante** de recompensas e a **vigência**, e SHALL oferecer ao Admin o
**encerramento** de cada um, avisando antes que o encerramento **devolve ao ponto de apoio a
recompensa ainda não entregue** e que o desafio deixa de receber conclusão. Encerrado o desafio,
a aplicação SHALL mostrar **quem encerrou e quando**, e NEVER SHALL oferecer novo encerramento.
A aplicação NEVER SHALL oferecer edição de desafio publicado. (`RF-02-106`, `RF-07-40`,
`RF-14-38`)

#### Scenario: O publicado aparece com o que resta

- **WHEN** o Admin abre a natureza dos desafios extras
- **THEN** os desafios publicados aparecem com a quantidade restante de recompensas e a vigência

#### Scenario: O encerramento avisa o que devolve antes de acontecer

- **WHEN** o Admin escolhe encerrar um desafio publicado
- **THEN** a aplicação avisa que a recompensa ainda não entregue volta ao ponto de apoio e que o
  desafio deixa de receber conclusão, antes de confirmar

#### Scenario: Encerrado, o desafio mostra quem encerrou

- **WHEN** o Admin confirma o encerramento
- **THEN** a aplicação mostra quem encerrou e quando, e não oferece novo encerramento

#### Scenario: A gestão não edita desafio publicado

- **WHEN** o Admin abre um desafio publicado
- **THEN** a aplicação não oferece alterar recompensa, quantidade, critério, pontos ou vigência

### Requirement: Nenhuma tela do desafio extra identifica Guerreiro(a)

A App 03 NEVER SHALL apresentar, em nenhuma tela de desafio extra, nome real, contato, imagem ou
qualquer outro dado de identificação de Guerreiro(a) — nem do destinatário do direcionado, nem
de quem dispute o aberto. Do desafio direcionado a aplicação SHALL apresentar o **nick como o
proponente o digitou** e a **justificativa do vínculo**, e nada mais. (`RF-14-39`, `RN-14-20`,
invariante 12, PRD-02 §11)

#### Scenario: O direcionado mostra só o nick digitado

- **WHEN** o Admin abre um desafio extra direcionado
- **THEN** a tela traz o nick como o proponente o digitou e a justificativa do vínculo, sem
  avatar, nome real ou qualquer outro dado do destinatário

#### Scenario: Nenhuma tela conta quem disputa

- **WHEN** o Admin abre um desafio extra publicado
- **THEN** a tela não identifica Guerreiro(a) algum que o tenha concluído ou esteja disputando
