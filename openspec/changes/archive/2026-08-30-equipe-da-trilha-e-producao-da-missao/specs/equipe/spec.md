## ADDED Requirements

### Requirement: A equipe da trilha é alcançável por HTTP pelo Guerreiro(a) em sessão

O núcleo SHALL expor a formação da equipe da trilha por `POST /v1/trilhas/{id}/equipes`, sob a
**sessão do Guerreiro(a)** e sob a chave de aplicação, pelas convenções de erro do PRD-01.
Quem cria SHALL entrar como **primeiro integrante**, e a entrada e a saída dos demais SHALL
correr pelas rotas de integrante que já existem — `POST /v1/equipes/{id}/integrantes` e
`DELETE /v1/equipes/{id}/integrantes/eu`.

A rota SHALL reexpor as recusas já vigentes desta capacidade, sem afrouxar nenhuma: o sexto
integrante e o segundo integrante de 17 anos ou mais (**422**), a equipe única por trilha
percorrida (**422**), a composição fixa depois da homologação (**422**) e a vedação de Admin e
Mestre formarem equipe (**403**). Trilha inexistente SHALL responder **404**.
(`RF-04-61`, `RF-01-37`, `RF-01-38`, `RF-01-16`, `RN-01-44`, PRD-04 §9)

#### Scenario: Guerreiro(a) cria a equipe da trilha por HTTP

- **WHEN** um Guerreiro(a) em sessão pede a criação de equipe numa trilha publicada
- **THEN** o núcleo responde 201 com a equipe da trilha, tendo-o como primeiro integrante

#### Scenario: Os limites de composição valem na equipe da trilha

- **WHEN** um sexto integrante, ou um segundo integrante de 17 anos ou mais, pede entrada
- **THEN** o núcleo responde 422 e a composição não muda

#### Scenario: Segunda equipe da mesma trilha é recusada pela porta

- **WHEN** um Guerreiro(a) que já integra uma equipe daquela trilha pede a criação de outra
- **THEN** o núcleo responde 422 e ele segue só na primeira

#### Scenario: Admin não cria equipe da trilha pela porta

- **WHEN** um Admin ou um Mestre em sessão pede a criação de equipe numa trilha
- **THEN** o núcleo responde 403 e nenhuma equipe é criada

#### Scenario: Trilha inexistente não forma equipe

- **WHEN** um Guerreiro(a) pede a criação de equipe numa trilha que não existe
- **THEN** o núcleo responde 404 e nenhuma equipe é criada

#### Scenario: Sem sessão de persona a porta não abre

- **WHEN** chega um pedido de criação de equipe da trilha sem credencial de persona
- **THEN** o núcleo recusa e nenhuma equipe é criada

### Requirement: A homologação da equipe da trilha é alcançável por HTTP pelo Mestre

O núcleo SHALL expor a homologação por `POST /v1/equipes/{id}/homologacao`, sob a credencial de
**Mestre ou Admin** — é a única escrita do caminho das trilhas que **não** corre sob a sessão
do Guerreiro(a). A resposta SHALL trazer quem homologou e quando.

Guerreiro(a) que tentar homologar SHALL receber **403**. Homologação de **equipe da aula** SHALL
ser recusada com **422** — só a equipe da trilha se homologa. O núcleo NEVER SHALL conferir
onde a homologação aconteceu — "em encontro presencial" é regra de operação, não conferência do
núcleo. (`RF-04-62`, `RF-01-63`, `RF-01-16`, PRD-04 §9)

#### Scenario: O Mestre homologa pela porta

- **WHEN** um Mestre em sessão homologa uma equipe da trilha
- **THEN** o núcleo responde 200 com quem homologou e quando, e a composição fica fixa

#### Scenario: Depois da homologação a composição não muda pela porta

- **WHEN** um Guerreiro(a) pede entrada ou saída numa equipe da trilha já homologada
- **THEN** o núcleo responde 422 e a composição registrada na homologação não muda

#### Scenario: Guerreiro(a) não homologa pela porta

- **WHEN** um Guerreiro(a) em sessão pede a homologação da própria equipe da trilha
- **THEN** o núcleo responde 403 e a equipe segue não homologada

#### Scenario: Equipe da aula não se homologa

- **WHEN** um Mestre pede a homologação de uma equipe da aula
- **THEN** o núcleo responde 422 e nada é gravado

## MODIFIED Requirements

### Requirement: A equipe da aula lê a programação do encontro

O núcleo SHALL servir, ao **Guerreiro(a) em sessão**, a **programação do encontro** da aula a
que a sua equipe pertence: as **atividades presenciais que declararam aquela aula**, cada uma
com a sua **missão**, o **conteúdo** e a **bibliografia** da missão. É o que o aparelho da
equipe mostra no caminho das trilhas (`RF-04-35`).

Cada item da programação SHALL trazer também a **trilha** a que a missão pertence — o
identificador e o título. É o que o aparelho precisa para oferecer à equipe a formação da
**equipe daquela trilha** (`RF-04-61`); sem isso o aparelho conhece a missão e não conhece a
trilha.

A programação SHALL ser **lista**, e não uma única atividade: o encontro do documento 05 §4 é
assíncrono, com vários Mestres e várias trilhas ao mesmo tempo, e é a **equipe quem escolhe**
em qual trabalhar.

A leitura SHALL trazer apenas atividade cuja trilha esteja **publicada**; atividade de trilha
em rascunho ou despublicada NEVER SHALL aparecer. Aula sem atividade presencial declarada SHALL
devolver **lista vazia**, não erro — é o encontro cuja programação ainda não foi declarada.

Quem lê SHALL ser **integrante daquela equipe**; Guerreiro(a) em sessão que não a integra SHALL
receber **403**. (`RF-04-35`, `RF-04-61`, `RF-01-16`, documento 05 §4, documento 02 §5,
PRD-04 §9)

#### Scenario: A equipe recebe a programação do seu encontro

- **WHEN** um integrante da equipe da aula lê a programação do encontro
- **THEN** o núcleo devolve as atividades presenciais declaradas naquela aula, cada uma com a
  missão, o conteúdo e a bibliografia dela

#### Scenario: Cada item traz a trilha da missão

- **WHEN** a programação é devolvida
- **THEN** cada item traz o identificador e o título da trilha a que a missão pertence

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
