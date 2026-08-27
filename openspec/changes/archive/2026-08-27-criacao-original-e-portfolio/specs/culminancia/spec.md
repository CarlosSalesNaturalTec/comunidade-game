## MODIFIED Requirements

### Requirement: A criação original se resolve pela trilha, sem referência própria à culminância

Com uma culminância por trilha, a `CriacaoOriginal` SHALL continuar referenciando **a trilha**,
e o núcleo SHALL resolver por ela a culminância aplicável. Nenhuma referência nova SHALL ser
exigida da criação original já gravada. A culminância SHALL ser, ainda assim, o **endereço da
entrega**: o Guerreiro(a) entrega a criação contra a culminância, e o núcleo resolve por ela a
trilha do registro. A **modalidade** declarada na culminância SHALL reger quem entrega — o
Guerreiro(a) sozinho, na individual; um integrante pela equipe da trilha, na em equipe —, e a
entrega em desacordo com ela SHALL ser recusada. Trilha sem culminância declarada NEVER SHALL
receber entrega. (`RF-09-30`, `RF-05-40`, PRD-09 §8, PRD-05 §9)

#### Scenario: A culminância aplicável vem da trilha da criação

- **WHEN** uma criação original entregue contra uma trilha que tem culminância é consultada
- **THEN** a culminância aplicável é a daquela trilha

#### Scenario: Criação anterior à culminância continua válida

- **WHEN** existe criação original entregue antes de a trilha ter culminância declarada
- **THEN** o registro dela permanece íntegro e nada nele é exigido a mais

#### Scenario: A entrega endereçada à culminância grava a trilha dela

- **WHEN** o Guerreiro(a) entrega a criação original endereçando a culminância
- **THEN** o núcleo grava o registro na trilha daquela culminância

#### Scenario: A modalidade da culminância rege quem entrega

- **WHEN** a culminância da trilha está declarada individual
- **THEN** a entrega é do próprio Guerreiro(a), e a entrega pela equipe é recusada
