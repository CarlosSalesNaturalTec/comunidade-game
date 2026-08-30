# equipe Specification

## Purpose
A equipe é o grupo livre que os Guerreiros e Guerreiras formam entre si, em dois tempos de vida:
a da aula, que serve às atividades do dia e termina com ela, e a da trilha, fixa depois de
homologada pelo Mestre e sujeito da criação original que encerra a trilha.
## Requirements
### Requirement: A equipe se vincula a uma aula ou a uma trilha, nunca às duas

O núcleo SHALL manter a equipe vinculada a **exatamente uma** aula **ou** a **exatamente uma**
trilha — nunca as duas ao mesmo tempo, nem nenhuma das duas. O vínculo SHALL declarar qual dos
dois tempos de vida a equipe tem. Equipe sem vínculo, ou com os dois, SHALL ser recusada com
**422**. (`RF-01-37`, `RF-01-63`, documento 02 §5)

#### Scenario: Equipe da aula nasce vinculada à aula

- **WHEN** um Guerreiro(a) cria uma equipe numa aula
- **THEN** o núcleo grava a equipe vinculada àquela aula, sem trilha

#### Scenario: Equipe da trilha nasce vinculada à trilha

- **WHEN** um Guerreiro(a) cria uma equipe numa trilha que percorre
- **THEN** o núcleo grava a equipe vinculada àquela trilha, sem aula

#### Scenario: Equipe sem vínculo é recusada

- **WHEN** chega uma equipe sem aula e sem trilha
- **THEN** o núcleo responde 422 e nada é gravado

#### Scenario: Equipe com aula e trilha ao mesmo tempo é recusada

- **WHEN** chega uma equipe vinculada a uma aula e a uma trilha ao mesmo tempo
- **THEN** o núcleo responde 422 e nada é gravado

### Requirement: A equipe é criada pelo Guerreiro(a), que entra como primeiro integrante

O núcleo SHALL restringir a criação de equipe ao **Guerreiro(a)**, que SHALL ser gravado como
**primeiro integrante** dela. A gestão NEVER SHALL formar equipe nem alterar composição —
Admin e Mestre que tentarem criar equipe ou incluir e remover integrante SHALL receber **403**.
(`RF-01-37`, `RF-01-16`, documento 99 §6 invariante 15)

#### Scenario: Quem cria entra como primeiro integrante

- **WHEN** um Guerreiro(a) cria uma equipe
- **THEN** o núcleo grava a equipe com ele como primeiro integrante

#### Scenario: Admin não forma equipe

- **WHEN** um Admin tenta criar uma equipe ou incluir integrante nela
- **THEN** o núcleo responde 403 e a composição não muda

#### Scenario: Mestre não altera composição

- **WHEN** um Mestre tenta remover um integrante de uma equipe
- **THEN** o núcleo responde 403 e a composição não muda

### Requirement: A equipe recusa o sexto integrante e o segundo integrante de 17 anos ou mais

O núcleo SHALL recusar com **422** o **sexto** integrante de uma equipe e o **segundo**
integrante de **17 anos ou mais**. Como a faixa do Guerreiro(a) é 6 a 16, o integrante de 17 anos
ou mais é aquele cujo papel **não é Guerreiro(a)**. Em ambas as recusas a composição existente
SHALL permanecer válida. (`RF-01-38`, documento 02 §5, documento 99 §6 invariantes 2 e 15)

#### Scenario: Quinto integrante é aceito

- **WHEN** um quinto Guerreiro(a) entra numa equipe de quatro
- **THEN** o núcleo grava a entrada

#### Scenario: Sexto integrante é recusado

- **WHEN** um sexto integrante tenta entrar numa equipe de cinco
- **THEN** o núcleo responde 422 e os cinco integrantes seguem na equipe

#### Scenario: Primeiro integrante de 17 anos ou mais é aceito

- **WHEN** uma persona que não é Guerreiro(a) entra numa equipe que só tem Guerreiros e
  Guerreiras
- **THEN** o núcleo grava a entrada

#### Scenario: Segundo integrante de 17 anos ou mais é recusado

- **WHEN** uma segunda persona que não é Guerreiro(a) tenta entrar na mesma equipe
- **THEN** o núcleo responde 422 e a composição não muda

### Requirement: A equipe da aula encerra com a aula e não é reaproveitada

A equipe vinculada a uma aula SHALL valer **apenas** para aquela aula: encerrada a aula, o núcleo
NEVER SHALL aceitar entrada ou saída de integrante nela, e a equipe NEVER SHALL aparecer em outra
aula. (`RF-01-37`)

#### Scenario: Equipe de uma aula não aparece em outra

- **WHEN** se consultam as equipes de uma aula diferente daquela em que a equipe foi formada
- **THEN** aquela equipe não está entre as devolvidas

#### Scenario: Equipe de aula encerrada não recebe integrante

- **WHEN** um Guerreiro(a) tenta entrar numa equipe cuja aula já se encerrou
- **THEN** o núcleo responde 422 e a composição não muda

### Requirement: O Guerreiro(a) integra mais de uma equipe da mesma aula

O núcleo SHALL aceitar o mesmo Guerreiro(a) em **mais de uma** equipe da mesma aula. Na
**partida de quiz**, porém, ele SHALL disputar por **uma única** das equipes: a abertura de
partida que o traga em duas ou mais das equipes disputantes SHALL ser recusada com **422**.
(`RF-01-39`, documento 02 §5, documento 03 §4.1)

#### Scenario: Mesmo Guerreiro(a) em duas equipes da aula

- **WHEN** um Guerreiro(a) que já integra uma equipe da aula entra em outra equipe da mesma aula
- **THEN** o núcleo grava a entrada e ele passa a integrar as duas

#### Scenario: As duas equipes não disputam a mesma partida

- **WHEN** alguém tenta abrir uma partida de quiz entre duas equipes da aula que compartilham
  um integrante
- **THEN** o núcleo responde 422 e nenhuma partida é aberta

#### Scenario: Cada equipe do Guerreiro(a) disputa uma partida diferente

- **WHEN** um Guerreiro(a) integra duas equipes da aula e cada uma disputa uma partida
  diferente
- **THEN** o núcleo aceita as duas partidas, porque em nenhuma delas ele aparece duas vezes

### Requirement: A equipe da trilha é uma por trilha percorrida

O núcleo SHALL aceitar, para cada Guerreiro(a) e cada trilha, **no máximo uma** equipe da trilha.
O pedido de entrada numa segunda equipe da mesma trilha SHALL ser recusado com **422**.
(`RN-01-44`, documento 02 §5)

#### Scenario: Segunda equipe da mesma trilha é recusada

- **WHEN** um Guerreiro(a) que já integra uma equipe de uma trilha tenta entrar em outra equipe
  da mesma trilha
- **THEN** o núcleo responde 422 e ele segue só na primeira

#### Scenario: Equipes de trilhas diferentes convivem

- **WHEN** um Guerreiro(a) que integra a equipe de uma trilha entra na equipe de outra trilha
- **THEN** o núcleo grava a entrada e ele passa a integrar uma equipe em cada trilha

### Requirement: A equipe da trilha fica fixa depois de homologada pelo Mestre

O núcleo SHALL registrar a **homologação** da equipe da trilha pelo **Mestre**, com quem
homologou e quando. A partir da homologação, o núcleo NEVER SHALL aceitar entrada ou saída de
integrante naquela equipe, respondendo **422**. Homologar SHALL ser operação de Mestre ou Admin;
o Guerreiro(a) que tentar SHALL receber **403**. O núcleo NEVER SHALL conferir onde a homologação
aconteceu — "em encontro presencial" é regra de operação, não conferência do núcleo. (`RF-01-63`,
`RN-01-44`, `RF-01-16`, documento 02 §5)

#### Scenario: Mestre homologa e a composição congela

- **WHEN** o Mestre homologa uma equipe da trilha
- **THEN** o núcleo grava quem homologou e quando, e a composição fica fixa

#### Scenario: Entrada depois da homologação é recusada

- **WHEN** um Guerreiro(a) tenta entrar numa equipe da trilha já homologada
- **THEN** o núcleo responde 422 e a composição registrada na homologação não muda

#### Scenario: Saída depois da homologação é recusada

- **WHEN** um integrante tenta sair de uma equipe da trilha já homologada
- **THEN** o núcleo responde 422 e ele segue na equipe

#### Scenario: Guerreiro(a) não homologa

- **WHEN** um Guerreiro(a) tenta homologar a própria equipe da trilha
- **THEN** o núcleo responde 403 e a equipe segue não homologada

#### Scenario: Equipe da trilha ainda não homologada aceita composição

- **WHEN** um Guerreiro(a) entra numa equipe da trilha que ainda não foi homologada
- **THEN** o núcleo grava a entrada

### Requirement: A equipe da trilha é alcançável por HTTP pelo Guerreiro(a) em sessão

O núcleo SHALL expor a formação da equipe da trilha por `POST /v1/trilhas/{id}/equipes`, sob a
**sessão do Guerreiro(a)** e sob a chave de aplicação, pelas convenções de erro do PRD-01. Quem
cria SHALL entrar como **primeiro integrante**, e a entrada e a saída dos demais SHALL correr
pelas rotas de integrante que já existem — `POST /v1/equipes/{id}/integrantes` e
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

### Requirement: O integrante guarda o papel que teve na equipe

O núcleo SHALL guardar, em cada integrante de equipe, o **papel** que ele teve — quem constrói,
quem registra, quem apresenta, quem media —, em texto livre e opcional. O papel NEVER SHALL
alterar a pontuação nem a composição. (`RF-01-64`, documento 02 §§4, 5)

#### Scenario: Papel declarado é guardado com o integrante

- **WHEN** um integrante entra na equipe com o papel declarado
- **THEN** o núcleo grava o papel junto do vínculo dele com a equipe

#### Scenario: Integrante sem papel declarado é aceito

- **WHEN** um integrante entra na equipe sem declarar papel
- **THEN** o núcleo grava a entrada com o papel em branco

#### Scenario: Papel não muda pontuação

- **WHEN** dois integrantes da mesma equipe têm papéis diferentes
- **THEN** o núcleo credita a ambos o mesmo que creditaria sem papel declarado

### Requirement: A equipe da aula é alcançável por HTTP pelo Guerreiro(a) em sessão

O núcleo SHALL expor a formação da equipe da aula pelas quatro rotas do PRD-04 §9 —
`GET /v1/aulas/{id}/equipes`, `POST /v1/aulas/{id}/equipes`,
`POST /v1/equipes/{id}/integrantes` e `DELETE /v1/equipes/{id}/integrantes/eu` —, todas sob a
**sessão do Guerreiro(a)** e sob a chave de aplicação, pelas convenções de erro e paginação do
PRD-01. As rotas SHALL reexpor as recusas já vigentes desta capacidade, sem afrouxar nenhuma:
os dois tetos, a equipe de aula encerrada, a equipe única por trilha e a vedação de Admin e
Mestre alterarem composição. (`RF-04-30`, `RF-04-31`, `RF-04-32`, `RF-04-33`, `RF-04-59`,
`RF-01-37`, `RF-01-38`, `RF-01-16`)

#### Scenario: Guerreiro(a) cria a equipe da aula por HTTP

- **WHEN** um Guerreiro(a) em sessão pede a criação de equipe numa aula vigente
- **THEN** o núcleo responde 201 com a equipe criada, tendo-o como primeiro integrante

#### Scenario: Guerreiro(a) entra em equipe existente por HTTP

- **WHEN** um Guerreiro(a) em sessão pede entrada numa equipe da aula
- **THEN** o núcleo responde 201 e ele passa a integrar a equipe

#### Scenario: Guerreiro(a) sai da própria equipe por HTTP

- **WHEN** um integrante pede a própria saída da equipe que integra
- **THEN** o núcleo responde 204 e ele deixa de integrá-la

#### Scenario: O sexto integrante é recusado pela porta

- **WHEN** um sexto integrante pede entrada numa equipe de cinco
- **THEN** o núcleo responde 422 e a composição não muda

#### Scenario: O segundo integrante de 17 anos ou mais é recusado pela porta

- **WHEN** uma segunda persona que não é Guerreiro(a) pede entrada na mesma equipe
- **THEN** o núcleo responde 422 e a composição não muda

#### Scenario: Equipe de aula encerrada não recebe integrante pela porta

- **WHEN** um Guerreiro(a) pede entrada numa equipe cuja aula já se encerrou
- **THEN** o núcleo responde 422 e a composição não muda

#### Scenario: Admin não cria equipe pela porta

- **WHEN** um Admin em sessão pede a criação de equipe numa aula
- **THEN** o núcleo responde 403 e nenhuma equipe é criada

#### Scenario: Mestre não altera composição pela porta

- **WHEN** um Mestre em sessão pede entrada ou saída de integrante numa equipe
- **THEN** o núcleo responde 403 e a composição não muda

#### Scenario: Sem sessão de persona a porta não abre

- **WHEN** chega um pedido de criação de equipe sem credencial de persona
- **THEN** o núcleo recusa e nenhuma equipe é criada

#### Scenario: O papel do integrante entra pela porta

- **WHEN** um Guerreiro(a) cria equipe ou entra em equipe declarando o papel
- **THEN** o núcleo grava o papel junto do vínculo dele com a equipe

### Requirement: A leitura das equipes da aula devolve apenas avatar e nick

O núcleo SHALL devolver, em `GET /v1/aulas/{id}/equipes`, as equipes vinculadas **àquela** aula,
com os integrantes identificados **apenas por avatar e nick**. A leitura NEVER SHALL devolver
nome, data de nascimento, imagem, _template_ biométrico ou qualquer outro dado pessoal do
Guerreiro(a), e NEVER SHALL trazer equipe de outra aula nem equipe da trilha. A leitura SHALL
ser restrita à persona em sessão pela operação `equipes_da_aula_em_andamento` da matriz.
(`RF-04-34`, `RN-04-14`, `RF-01-37`, documento 99 §6 invariantes 11 e 12)

#### Scenario: As equipes daquela aula são devolvidas

- **WHEN** um Guerreiro(a) em sessão consulta as equipes de uma aula
- **THEN** o núcleo devolve as equipes vinculadas àquela aula, cada uma com os integrantes

#### Scenario: Só avatar e nick de cada integrante

- **WHEN** a leitura devolve os integrantes de uma equipe
- **THEN** cada integrante traz avatar e nick, e nenhum outro dado pessoal

#### Scenario: Equipe da trilha não aparece na leitura da aula

- **WHEN** existem equipes de trilha além das equipes da aula consultada
- **THEN** o núcleo devolve apenas as equipes da aula, sem as da trilha

#### Scenario: Aula sem equipe devolve conjunto vazio

- **WHEN** a aula consultada ainda não tem equipe formada
- **THEN** o núcleo responde 200 com conjunto vazio, nunca erro

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

