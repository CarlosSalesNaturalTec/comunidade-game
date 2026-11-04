# Spec Delta

## ADDED Requirements

### Requirement: O Guerreiro(a) entrega a comprovação do desafio prático

A submissão do desafio em forma de **desafio prático** SHALL trazer a **comprovação** na
**forma que o Mestre autor declarou aceitar**, e o núcleo SHALL gravá-la com a declaração, no
mesmo ato. Comprovação em forma **diferente** da aceita SHALL ser recusada com **422**,
nomeando a forma esperada. O núcleo NEVER SHALL aferir a comprovação: ela existe para o
**julgamento do Mestre autor**. O **quiz** NEVER SHALL trazer comprovação. (`RF-05-91`,
documento 02 §4, documento 11 §2.2)

#### Scenario: A comprovação é gravada com a declaração

- **WHEN** o Guerreiro(a) inscrito declara que cumpriu o prático cuja forma aceita é vídeo, e
  entrega o vídeo
- **THEN** o núcleo grava a declaração com a comprovação, e a missão segue aguardando o Mestre

#### Scenario: Comprovação em texto é gravada como o corpo escrito

- **WHEN** a forma aceita é texto e o Guerreiro(a) entrega o corpo escrito
- **THEN** o núcleo grava o texto com a declaração, sem interpretá-lo nem aferi-lo

#### Scenario: Comprovação em link externo é gravada como o endereço

- **WHEN** a forma aceita é link externo e o Guerreiro(a) entrega o endereço
- **THEN** o núcleo grava o endereço com a declaração

#### Scenario: Forma diferente da aceita é recusada

- **WHEN** a forma aceita é imagem e a submissão traz comprovação em link externo
- **THEN** o núcleo responde **422** nomeando a forma esperada, e nada é gravado

#### Scenario: O quiz não traz comprovação

- **WHEN** a submissão de um desafio em forma de quiz traz comprovação
- **THEN** o núcleo responde **422** dizendo que o campo não se aplica ao quiz, e nada é gravado

### Requirement: A comprovação é exigida, e a entrega no encontro é a alternativa

Declarar que cumpriu o prático SHALL exigir a comprovação: declaração **sem** comprovação e
**sem** a alternativa SHALL ser recusada com **422**, nomeando o que falta. O Guerreiro(a) SHALL
poder, em lugar dela, declarar que **entrega ao Mestre no encontro**: a declaração é gravada
**sem mídia**, marcada como **entrega presencial**, e NEVER SHALL fazer perder a missão, ser
recusada nem contar como tentativa falha. (`RN-05-51`, `RF-05-78`, `RN-05-20`, PRD-05 §11,
decisão do fundador de 2026-11-04)

#### Scenario: Declaração sem comprovação e sem alternativa é recusada

- **WHEN** o Guerreiro(a) declara que cumpriu o prático sem entregar a comprovação e sem
  escolher a entrega no encontro
- **THEN** o núcleo responde **422** nomeando o que falta, e nada é gravado

#### Scenario: A entrega no encontro grava a declaração sem mídia

- **WHEN** o Guerreiro(a) declara que cumpriu escolhendo entregar ao Mestre no encontro
- **THEN** o núcleo grava a declaração sem comprovação, marcada como entrega presencial, e a
  missão segue aguardando o Mestre

#### Scenario: A entrega presencial não é tentativa falha

- **WHEN** o Guerreiro(a) escolhe a entrega no encontro
- **THEN** nada é contado contra ele, a missão segue sem reprovação e o percurso a exibe como
  aguardando o Mestre

### Requirement: A mídia da comprovação entra por envio retomável

Comprovação em **imagem**, **áudio**, **vídeo** ou **arquivo** SHALL nascer **sem o arquivo** e
recebê-lo por **sessão de envio retomável**, e SHALL passar a servir bytes só quando o envio
**conclui**. O núcleo SHALL aplicar à comprovação a **mesma lista fechada de tipos** e os
**mesmos tetos de tamanho** da criação original, recusando com **422** o tipo fora da lista e o
tamanho acima do teto, dizendo o teto. (`RF-05-91`, `RF-01-78`)

#### Scenario: A comprovação em mídia nasce sem arquivo e o recebe depois

- **WHEN** o Guerreiro(a) declara que cumpriu entregando comprovação em vídeo
- **THEN** o núcleo grava a declaração sem mídia, e ela passa a existir quando o envio do
  arquivo conclui

#### Scenario: Tipo de arquivo fora da lista é recusado

- **WHEN** o envio da comprovação declara tipo de arquivo que não está na lista fechada
- **THEN** o núcleo responde **422** e nenhum byte é aceito

#### Scenario: Tamanho acima do teto é recusado

- **WHEN** o envio da comprovação declara tamanho acima do teto do tipo dela
- **THEN** o núcleo responde **422** dizendo o teto, e nenhum byte é aceito

### Requirement: Entrega nova antes do julgamento substitui a anterior

Enquanto o Mestre autor **não julgou**, o Guerreiro(a) SHALL poder entregar de novo, e a entrega
nova SHALL **substituir** a anterior em vez de criar segundo registro. Julgado que **não
passou**, a declaração é apagada e a comprovação SHALL ir com ela, de modo que a declaração
seguinte comece sem resíduo da anterior. Depois de julgado que **passou**, nova entrega SHALL
ser recusada com **422**. (`RN-05-52`, `RN-05-20`)

#### Scenario: Entregar de novo antes do julgamento substitui o que estava

- **WHEN** o Guerreiro(a) entrega a comprovação e, antes de o Mestre julgar, entrega outra
- **THEN** o núcleo guarda só a última, e segue havendo uma única declaração daquele par

#### Scenario: Julgado que não passou, a comprovação vai com a declaração

- **WHEN** o Mestre autor julga que o Guerreiro(a) não passou
- **THEN** a declaração e a comprovação dela deixam de existir, e ele pode declarar de novo,
  sem limite e sem punição

#### Scenario: Depois de aprovado, nova entrega é recusada

- **WHEN** o Guerreiro(a) tenta entregar comprovação de um prático já julgado como cumprido
- **THEN** o núcleo responde **422** e a comprovação gravada permanece como estava

### Requirement: A comprovação é servida a quem pode vê-la

O núcleo SHALL servir os **bytes** da comprovação em mídia ao **próprio Guerreiro(a)** que a
entregou e ao **Mestre autor** da trilha — a ele porque é quem julga, a ele porque foi avisado
de que a mídia fica guardada. Persona que não é nenhum dos dois SHALL ser recusada com **403**.
Comprovação **sem mídia**, ou com envio **não concluído**, SHALL responder **404**. (`RF-05-93`,
decisão do fundador de 2026-11-04)

#### Scenario: O Guerreiro(a) reencontra o que entregou

- **WHEN** o Guerreiro(a) pede a comprovação que entregou
- **THEN** o núcleo devolve os bytes dela, com o tipo do arquivo que guardou

#### Scenario: O Mestre autor alcança a comprovação

- **WHEN** o Mestre autor da trilha pede a comprovação entregue naquela missão
- **THEN** o núcleo devolve os bytes dela

#### Scenario: Quem não é o autor nem quem entregou é recusado

- **WHEN** outro Guerreiro(a), ou um Mestre que não é o autor da trilha, pede a comprovação
- **THEN** o núcleo responde **403** e nenhum byte é servido

#### Scenario: Comprovação sem mídia responde 404

- **WHEN** se pedem os bytes de uma declaração de entrega presencial, ou de uma cujo envio não
  concluiu
- **THEN** o núcleo responde **404**

## MODIFIED Requirements

### Requirement: O desafio prático é julgado pelo Mestre autor

No desafio em forma de **desafio prático**, o núcleo NEVER SHALL aferir a submissão sozinho: o
Guerreiro(a) SHALL **declarar que cumpriu**, **entregando a comprovação** na forma aceita ou
declarando que a entrega ao Mestre no encontro, e o **Mestre autor da trilha** SHALL **julgar se
passou**. Passando o julgamento, o núcleo SHALL marcar a missão como desbloqueada por aquele
Guerreiro(a), abrindo a seguinte para ele. Não passando, o Guerreiro(a) SHALL poder declarar de
novo, sem limite e sem punição. Persona que não é o Mestre autor SHALL ser recusada com
**403**. Enquanto o Mestre não julgar, o percurso SHALL exibir a missão como **aguardando o
Mestre**, nunca como reprovada. (`RF-05-13`, `RF-05-14`, `RF-05-91`, `RF-09-26`, `RN-05-06`,
`RN-05-51`, decisão do fundador em 2026-08-27, ampliada em 2026-11-03)

#### Scenario: O Mestre autor julga o prático e a missão desbloqueia

- **WHEN** o Guerreiro(a) declara ter cumprido o desafio prático e o Mestre autor julga que
  passou
- **THEN** o núcleo marca a missão como desbloqueada por ele e abre a seguinte para ele

#### Scenario: Enquanto o Mestre não julga, nada é reprovado

- **WHEN** o Guerreiro(a) declarou ter cumprido o desafio prático e o Mestre ainda não julgou
- **THEN** o percurso exibe a missão como aguardando o Mestre, e ela segue travada sem
  reprovação

#### Scenario: Quem não é o autor não julga

- **WHEN** um Mestre que não é o autor da trilha tenta julgar o desafio prático de uma missão
  dela
- **THEN** o núcleo responde 403 e nada é gravado

#### Scenario: Julgado como não passou, o Guerreiro(a) declara de novo

- **WHEN** o Mestre autor julga que o Guerreiro(a) não passou no desafio prático
- **THEN** a missão segue travada e ele pode declarar de novo, sem limite e sem punição
