## MODIFIED Requirements

### Requirement: A equipe da aula lê a programação do encontro

O núcleo SHALL servir, ao **Guerreiro(a) em sessão**, a **programação do encontro** da aula a
que a sua equipe pertence: as **atividades presenciais que declararam aquela aula**, cada uma
com a sua **missão**, o **conteúdo** e a **bibliografia** da missão. É o que o aparelho da
equipe mostra no caminho das trilhas (`RF-04-35`).

A programação SHALL ser **lista**, e não uma única atividade: o encontro do documento 05 §4 é
assíncrono, com vários Mestres e várias trilhas ao mesmo tempo, e é a **equipe quem escolhe**
em qual trabalhar.

A leitura SHALL trazer apenas atividade cuja trilha esteja **publicada**; atividade de trilha
em rascunho ou despublicada NEVER SHALL aparecer. Aula sem atividade presencial declarada SHALL
devolver **lista vazia**, não erro — é o encontro cuja programação ainda não foi declarada.

Quem lê SHALL ser **integrante daquela equipe**; Guerreiro(a) em sessão que não a integra SHALL
receber **403**. (`RF-04-35`, `RF-01-16`, documento 05 §4, documento 02 §5, PRD-04 §9)

#### Scenario: A equipe recebe a programação do seu encontro

- **WHEN** um integrante da equipe da aula lê a programação do encontro
- **THEN** o núcleo devolve as atividades presenciais declaradas naquela aula, cada uma com a
  missão, o conteúdo e a bibliografia dela

#### Scenario: Duas trilhas no mesmo encontro saem as duas

- **WHEN** dois Mestres declararam, na mesma aula, atividades de trilhas diferentes
- **THEN** a programação devolve as duas, e o núcleo não elege nenhuma

#### Scenario: Encontro sem programação declarada devolve lista vazia

- **WHEN** um integrante lê a programação de uma aula em que nenhuma atividade presencial foi
  declarada
- **THEN** o núcleo devolve lista vazia e não responde erro

#### Scenario: Atividade de trilha em rascunho não aparece

- **WHEN** uma atividade declarada na aula pertence a uma trilha ainda em rascunho
- **THEN** ela não aparece na programação devolvida à equipe

#### Scenario: Quem não integra a equipe é recusado

- **WHEN** um Guerreiro(a) em sessão que não integra aquela equipe pede a programação dela
- **THEN** o núcleo responde 403 e nada é devolvido

#### Scenario: A leitura não grava escolha alguma

- **WHEN** a equipe lê a programação e trabalha uma das atividades sem declará-la
- **THEN** o núcleo não grava escolha nem progresso por causa da leitura: quem grava a escolha
  é a declaração da equipe, e sem ela a corrente segue em branco

## ADDED Requirements

### Requirement: A equipe da aula declara em que atividade da programação está

O núcleo SHALL guardar, na **equipe da aula**, a **atividade da programação** que ela está
trabalhando, declarada pelo aparelho da equipe. É o que o painel do dia lê para dizer ao Mestre
em que missão cada equipe está (`RF-02-42`), e o que fecha o "a missão **em que está**" do
`RF-04-35`.

A declaração SHALL ser trocada quantas vezes a equipe quiser durante o encontro, e SHALL guardar
sempre **apenas a corrente** — o núcleo NEVER SHALL acumular histórico das escolhas anteriores.
A escolha SHALL morrer com a aula, como a própria equipe da aula, que encerra com ela e não é
reaproveitada. Ela é estado do **encontro em andamento**, e NEVER SHALL ser lida como percurso
da trilha, progresso do Guerreiro(a) nem missão concluída: continua valendo que a equipe da aula
NEVER SHALL guardar estado de percurso (documento 02 §5).

A atividade declarada SHALL pertencer à **programação daquela aula**; atividade fora dela SHALL
ser recusada com **422**. Declarar SHALL ser ato de **integrante daquela equipe**; qualquer outro
Guerreiro(a) em sessão SHALL receber **403**. Equipe sem escolha declarada SHALL ser servida com
a escolha **em branco**, não erro — é a equipe que ainda não começou.

Decisão do fundador, 2026-08-25: a escolha passa a ser gravada, revertendo a frase da sétima
fatia do PRD-04 que a proibia. (`RF-02-42`, `RF-04-35`, `RF-01-16`, documento 02 §5,
documento 05 §4)

#### Scenario: A equipe declara a atividade que está trabalhando

- **WHEN** um integrante declara, pelo aparelho, qual atividade da programação a equipe escolheu
- **THEN** o núcleo grava a escolha na equipe da aula e passa a servi-la como a corrente

#### Scenario: Trocar de atividade substitui a escolha

- **WHEN** a equipe declara uma segunda atividade da programação no mesmo encontro
- **THEN** o núcleo passa a servir a segunda como corrente e não guarda a primeira

#### Scenario: Atividade fora da programação da aula é recusada

- **WHEN** um integrante declara uma atividade que não está na programação daquela aula
- **THEN** o núcleo responde 422 e a escolha anterior permanece

#### Scenario: Quem não integra a equipe não declara por ela

- **WHEN** um Guerreiro(a) em sessão que não integra a equipe tenta declarar a escolha dela
- **THEN** o núcleo responde 403 e nada é gravado

#### Scenario: Equipe que ainda não começou sai com a escolha em branco

- **WHEN** o painel do dia lê uma equipe que não declarou escolha alguma
- **THEN** ela sai com a escolha em branco, e o núcleo não responde erro

#### Scenario: A escolha não sobrevive à aula

- **WHEN** a aula se encerra e as equipes dela deixam de valer
- **THEN** a escolha declarada não é reaproveitada em encontro algum, e nenhum percurso é
  gravado a partir dela
