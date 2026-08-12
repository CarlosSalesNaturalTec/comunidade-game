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

O núcleo SHALL aceitar o mesmo Guerreiro(a) em **mais de uma** equipe da mesma aula. (`RF-01-39`,
documento 02 §5)

#### Scenario: Mesmo Guerreiro(a) em duas equipes da aula

- **WHEN** um Guerreiro(a) que já integra uma equipe da aula entra em outra equipe da mesma aula
- **THEN** o núcleo grava a entrada e ele passa a integrar as duas

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

