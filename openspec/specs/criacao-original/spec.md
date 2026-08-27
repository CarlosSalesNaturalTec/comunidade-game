## Purpose

A Criação Original é o registro de que um Guerreiro(a) — sozinho ou em equipe — entregou, ao
final da trilha, algo criado a partir do que aprendeu — a trava viva da regra "toda trilha
termina em criação original" (documento 99 §6 invariante 5), com autoria que nunca se perde.

## Requirements

### Requirement: Guerreiro(a) entrega a criação original contra uma trilha

O núcleo SHALL registrar a entrega de uma **criação original** da trilha a que ela pertence, com
a produção declarada e situação inicial **entregue**. Quem entrega SHALL seguir a **modalidade**
declarada na culminância daquela trilha (`RF-09-30`):

- modalidade **em equipe**: entrega um **integrante** da equipe da trilha, e vale pela equipe
  inteira;
- modalidade **individual**: entrega o próprio **Guerreiro(a) inscrito** na trilha, e vale por
  ele.

A entrega SHALL ser endereçada pela **culminância** da trilha. Entrega contra trilha **sem
culminância declarada** SHALL ser recusada com **409**, dizendo que a trilha ainda não declarou
o que a criação precisa ser. Criação original sem produção declarada SHALL ser recusada com
**422**, indicando o campo em falta; entrega em desacordo com a modalidade declarada — um
integrante entregando pela equipe numa culminância individual, ou um Guerreiro(a) entregando
sozinho numa culminância em equipe — SHALL ser recusada com **422**. Quem não integra a equipe
NEVER SHALL entregar por ela, e SHALL receber **403**.

Enquanto a criação **não estiver validada**, uma nova entrega do mesmo autor — o Guerreiro(a) na
modalidade individual, a equipe na modalidade em equipe — SHALL **substituir** a produção da
entrega existente e devolvê-la à situação **entregue**, sem criar um segundo registro: é assim
que o reenvio depois da devolução para ajuste acontece (`RF-05-42`). Criação já **validada**
NEVER SHALL ser substituída, e a nova entrega SHALL ser recusada com **409**. O núcleo SHALL
manter, portanto, no máximo **uma** criação original por equipe da trilha e **uma** por
Guerreiro(a) e trilha. (`RF-01-26`, `RF-01-64`, `RF-05-40`, `RF-09-30`, PRD-05 §9)

#### Scenario: Entrega registrada com produção declarada

- **WHEN** um integrante da equipe da trilha entrega uma criação original com produção, na
  culminância declarada em equipe
- **THEN** o núcleo grava o registro com situação "entregue", vinculado àquela equipe

#### Scenario: Entrega individual registrada em nome do Guerreiro(a)

- **WHEN** o Guerreiro(a) inscrito na trilha entrega a criação original de uma culminância
  declarada individual
- **THEN** o núcleo grava o registro com situação "entregue", vinculado a ele e sem equipe

#### Scenario: Entrega sem produção é recusada

- **WHEN** chega uma criação original sem a produção declarada
- **THEN** o núcleo responde 422 indicando o campo em falta e nada é gravado

#### Scenario: Entrega em trilha sem culminância declarada é recusada

- **WHEN** chega uma criação original contra trilha que ainda não tem culminância declarada
- **THEN** o núcleo responde 409 e nada é gravado

#### Scenario: Entrega em desacordo com a modalidade é recusada

- **WHEN** um integrante tenta entregar pela equipe numa culminância declarada individual
- **THEN** o núcleo responde 422 e nada é gravado

#### Scenario: Entrega sem equipe da trilha é recusada

- **WHEN** chega uma criação original de culminância em equipe sem a equipe da trilha vinculada
- **THEN** o núcleo responde 422 indicando o campo em falta e nada é gravado

#### Scenario: Nova entrega antes da validação substitui a anterior

- **WHEN** o autor de uma criação original ainda não validada entrega uma produção nova
- **THEN** o núcleo substitui a produção do registro existente, devolve-o à situação "entregue"
  e não cria um segundo registro

#### Scenario: Nova entrega depois de validada é recusada

- **WHEN** o autor de uma criação original já validada tenta entregar de novo
- **THEN** o núcleo responde 409 e o registro validado permanece como está

#### Scenario: Segunda entrega da mesma equipe é recusada

- **WHEN** um integrante entrega uma criação original numa trilha em que a criação da equipe dele
  já foi validada
- **THEN** o núcleo responde 409 e a entrega validada permanece

#### Scenario: Quem não é integrante não entrega pela equipe

- **WHEN** um Guerreiro(a) que não integra a equipe tenta entregar a criação original dela
- **THEN** o núcleo responde 403 e nada é gravado

### Requirement: Mestre autor da trilha valida ou devolve a criação original entregue

O núcleo SHALL restringir a validação e a devolução da criação original ao **Mestre autor** da
trilha a que ela pertence, ou a um **Admin** — a mesma matriz de posse que já vale para trilha,
missão, atividade e resultado. Mestre que não é o autor SHALL receber **403**, e a situação SHALL
permanecer inalterada. A devolução SHALL registrar o **motivo**, escrito pelo Mestre em
linguagem simples; devolução sem motivo SHALL ser recusada com **422**. A validação NEVER SHALL
exigir motivo. (`RF-01-26`, `RF-01-16`, `RF-05-42`, `RF-09-31`, `RF-09-34`, `RN-09-04`)

#### Scenario: Mestre autor valida a entrega

- **WHEN** o Mestre autor da trilha valida uma criação original com situação "entregue"
- **THEN** o núcleo muda a situação para "validada"

#### Scenario: Mestre autor devolve a entrega

- **WHEN** o Mestre autor da trilha devolve uma criação original com situação "entregue",
  declarando o motivo
- **THEN** o núcleo muda a situação para "devolvida" e guarda o motivo com o registro

#### Scenario: Devolução sem motivo é recusada

- **WHEN** o Mestre autor tenta devolver uma criação original sem declarar o motivo
- **THEN** o núcleo responde 422 e a situação não muda

#### Scenario: Mestre que não é o autor é recusado

- **WHEN** um Mestre que não é o autor da trilha tenta validar ou devolver a criação original
  dela
- **THEN** o núcleo responde 403 e a situação não muda

### Requirement: Autoria da criação original nunca se perde

A criação original SHALL manter a mesma autoria por toda a vida do registro, inclusive quando
devolvida para ajuste e quando a produção é substituída por um reenvio — devolver e reenviar
mudam a situação e a produção, nunca a autoria. Na modalidade **em equipe**, a autoria SHALL ser
a **equipe da trilha** e os seus **integrantes**, cada um com o papel que teve; como a composição
fica fixa na homologação (`RN-01-44`), a autoria creditada é a que estava registrada naquele
momento. Na modalidade **individual**, a autoria SHALL ser o **Guerreiro(a)** que entregou.
(`RN-01-13`, `RF-01-64`, `RF-05-41`, `RN-05-13`, `RF-09-32`)

#### Scenario: Devolução preserva a autoria

- **WHEN** uma criação original entregue é devolvida
- **THEN** o registro continua com a mesma autoria, sem reatribuição

#### Scenario: Reenvio preserva a autoria

- **WHEN** o autor reenvia a produção de uma criação original devolvida
- **THEN** o registro continua com a mesma autoria, e só a produção e a situação mudam

#### Scenario: A autoria é a composição homologada

- **WHEN** se lê a autoria de uma criação original em equipe
- **THEN** ela traz cada integrante da equipe homologada, com o papel de cada um

#### Scenario: A autoria individual é o Guerreiro(a) que entregou

- **WHEN** se lê a autoria de uma criação original individual
- **THEN** ela traz o Guerreiro(a) que a entregou, e nenhuma equipe

### Requirement: A produção da criação original é texto, imagem, vídeo, arquivo ou link

A criação original SHALL declarar o **tipo da produção** entre os cinco valores fechados —
**texto**, **imagem**, **vídeo**, **arquivo** e **link externo** —, os mesmos que o conteúdo da
missão já usa. Produção de tipo **texto** SHALL trazer o corpo escrito e a de tipo **link
externo**, o endereço, ambos no ato da entrega. Produção de tipo **imagem**, **vídeo** ou
**arquivo** SHALL ser enviada em ato próprio, depois de criado o registro, e a criação SHALL
permanecer sem mídia até que o envio conclua. Tipo fora dos cinco valores SHALL ser recusado com
**422**. (`RF-05-40`, documento 02 §4)

#### Scenario: Entrega em texto traz o corpo escrito

- **WHEN** o Guerreiro(a) entrega a criação original declarando tipo texto e o corpo
- **THEN** o núcleo grava a produção escrita com o registro

#### Scenario: Entrega em link externo traz o endereço

- **WHEN** o Guerreiro(a) entrega a criação original declarando tipo link externo e o endereço
- **THEN** o núcleo grava o endereço com o registro

#### Scenario: Entrega em mídia nasce sem o arquivo e o recebe depois

- **WHEN** o Guerreiro(a) entrega a criação original declarando tipo imagem, vídeo ou arquivo
- **THEN** o núcleo grava o registro sem mídia, e ela passa a existir quando o envio do arquivo
  conclui

#### Scenario: Tipo fora dos cinco valores é recusado

- **WHEN** chega uma criação original com tipo de produção diferente dos cinco
- **THEN** o núcleo responde 422 e nada é gravado

### Requirement: O Guerreiro(a) lê o próprio portfólio, com a situação de exposição de cada criação

O núcleo SHALL expor ao Guerreiro(a) em sessão o **portfólio** das criações originais
**validadas** de que ele é creditado — pela equipe ou individualmente —, cada uma com a
**trilha**, a **data da validação**, a **autoria creditada** e a **situação de exposição
pública**. A situação de exposição SHALL dizer se a criação está **pública** ou se **depende de
autorização do responsável**, e SHALL seguir a mesma condição da vitrine: pública apenas quando
**todos** os creditados nela têm autorização de divulgação vigente. Criação validada sem essa
autorização SHALL aparecer no portfólio do Guerreiro(a) e NEVER SHALL aparecer em rota pública.
O portfólio NEVER SHALL trazer criação de outro Guerreiro(a). (`RF-05-43`, `RF-05-44`,
`RF-09-33`, `RN-05-14`, `RN-05-21`, `RN-09-19`, PRD-05 §9)

#### Scenario: Portfólio traz as criações validadas com trilha, data e autoria

- **WHEN** o Guerreiro(a) em sessão consulta o próprio portfólio
- **THEN** o núcleo devolve cada criação validada de que ele é creditado, com a trilha, a data da
  validação e a autoria

#### Scenario: Criação sem autorização aparece como dependente de autorização

- **WHEN** uma criação validada tem entre os creditados alguém sem autorização de divulgação
  vigente
- **THEN** ela aparece no portfólio marcada como dependente de autorização do responsável, e não
  aparece em rota pública

#### Scenario: Criação entregue e ainda não validada não entra no portfólio

- **WHEN** o Guerreiro(a) tem criação original com situação "entregue" ou "devolvida"
- **THEN** ela não aparece no portfólio, que reúne apenas as validadas

#### Scenario: O portfólio não alcança criação de terceiro

- **WHEN** o Guerreiro(a) em sessão consulta o portfólio
- **THEN** o núcleo devolve apenas criações de que ele é creditado

### Requirement: O Mestre autor lê as criações originais entregues que lhe cabe decidir

O núcleo SHALL expor ao **Mestre autor** em sessão as criações originais com situação
**entregue** das trilhas de que ele é autor, cada uma com a **trilha**, a **culminância** que a
rege, a **produção** e a **autoria creditada** — na modalidade em equipe, cada integrante com o
papel que teve. A lista NEVER SHALL alcançar criação de trilha de outro Mestre. Admin SHALL ler
a mesma lista sem a restrição de autoria, pela matriz de posse já vigente. (`RF-09-31`,
`RF-09-32`, `RF-01-16`)

#### Scenario: Mestre autor lê as criações entregues das suas trilhas

- **WHEN** o Mestre autor em sessão consulta as criações originais a decidir
- **THEN** o núcleo devolve as entregues das trilhas de que ele é autor, com produção e autoria

#### Scenario: A lista não alcança trilha de outro Mestre

- **WHEN** existe criação original entregue numa trilha de outro Mestre
- **THEN** ela não aparece na lista do Mestre que não é o autor dela

#### Scenario: Criação em equipe traz o papel de cada integrante

- **WHEN** o Mestre autor lê uma criação original entregue por uma equipe
- **THEN** a resposta traz cada integrante creditado com o papel que teve
