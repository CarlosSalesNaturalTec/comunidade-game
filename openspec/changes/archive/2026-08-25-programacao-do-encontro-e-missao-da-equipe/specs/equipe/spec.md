## ADDED Requirements

### Requirement: A equipe da aula lê a programação do encontro

O núcleo SHALL servir, ao **Guerreiro(a) em sessão**, a **programação do encontro** da aula a
que a sua equipe pertence: as **atividades presenciais que declararam aquela aula**, cada uma
com a sua **missão**, o **conteúdo** e a **bibliografia** da missão. É o que o aparelho da
equipe mostra no caminho das trilhas (`RF-04-35`).

A programação SHALL ser **lista**, e não uma única atividade: o encontro do documento 05 §4 é
assíncrono, com vários Mestres e várias trilhas ao mesmo tempo, e é a **equipe quem escolhe**
em qual trabalhar. A escolha NEVER SHALL ser gravada — a equipe da aula encerra com a aula e
não guarda estado de percurso (documento 02 §5).

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

- **WHEN** a equipe lê a programação e trabalha uma das atividades
- **THEN** o núcleo não grava vínculo, escolha nem progresso na equipe da aula
