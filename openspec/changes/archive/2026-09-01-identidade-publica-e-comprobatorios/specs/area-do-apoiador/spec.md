## ADDED Requirements

### Requirement: A tela de identidade pública define nick e avatar

A App 08 SHALL apresentar ao Apoiador em sessão a tela de **identidade pública**, em que ele
define ou troca o **nick** e o **avatar** que aparecem no card, a qualquer tempo. Vindo o nick do
pré-cadastro, a tela NEVER SHALL pedi-lo de novo no primeiro acesso, e SHALL apresentá-lo já
preenchido. Recusado o nick por já estar em uso, a tela SHALL apresentar as **sugestões de
variação** que o núcleo devolve, e NEVER SHALL revelar de quem é o nick em uso. (`RF-14-12`,
`RF-14-13`, `RF-14-17`, `RN-14-10`, PRD-14 §§5.2, 12)

#### Scenario: O nick do pré-cadastro não é pedido de novo

- **WHEN** um Apoiador cujo cadastro nasceu com nick abre a identidade pública no primeiro acesso
- **THEN** a tela apresenta o nick que ele já tem, para trocar se quiser, e não o pede como se
  não existisse

#### Scenario: Nick já usado volta com sugestões

- **WHEN** o Apoiador tenta gravar um nick já usado por outro adulto
- **THEN** a tela recusa a gravação e apresenta as sugestões de variação, sem dizer de quem é o
  nick

#### Scenario: A troca vale a qualquer tempo

- **WHEN** um Apoiador que já tem nick e avatar troca os dois
- **THEN** a tela grava a troca e passa a apresentar os novos no card

### Requirement: Abaixo do piso a tela mostra o avatar padrão e quanto falta

Abaixo de **10 moedas acumuladas**, a App 08 SHALL apresentar o card com o **avatar padrão do
projeto**, o nick e o total de moedas, na mesma moldura comum a todos os apoiadores, e SHALL
dizer **quantas moedas faltam** para liberar o avatar próprio. A tela NEVER SHALL cobrar aporte
nem insistir para que ele aconteça, e NEVER SHALL marcar de outro modo quem está abaixo do piso.
Alcançado o piso, o envio do avatar próprio SHALL abrir sem ato algum da gestão. Toda saída
SHALL exibir **moedas**, nunca reais. (`RF-14-14`, `RF-14-15`, `RF-14-16`, `RN-14-09`,
`RN-14-11`, documento 11 §8.2, PRD-14 §12)

#### Scenario: Com 5 moedas o card é o padrão, e a tela diz o que falta

- **WHEN** um Apoiador com 5 moedas acumuladas abre a identidade pública
- **THEN** o card aparece com o avatar padrão, o nick e o total em moedas, e a tela diz que
  faltam 5 moedas para o avatar próprio, sem pedir o aporte

#### Scenario: Cruzado o piso, o envio abre sozinho

- **WHEN** o Apoiador cruza as 10 moedas acumuladas e volta à tela
- **THEN** o envio do avatar próprio está aberto, sem que a gestão tenha feito nada

#### Scenario: A recusa do núcleo aparece com quanto falta

- **WHEN** o Apoiador abaixo do piso tenta enviar o avatar próprio e o núcleo recusa
- **THEN** a tela apresenta a recusa dizendo quantas moedas faltam, e o card segue com o avatar
  padrão

### Requirement: A tela de comprobatórios declara que só o Admin publica

A App 08 SHALL apresentar ao Apoiador em sessão a tela de **documentos comprobatórios**, em que
ele declara currículo, portfólio, redes sociais, termos de doação e comprovantes por **endereço e
rótulo**, e NEVER SHALL oferecer anexo de arquivo. A tela SHALL declarar, **antes do envio**, que
o documento entra na fila da gestão e só vai à página pública quando um Admin o anexar ao
cadastro. Enviado, a tela SHALL apresentar o documento como **pendente**, e SHALL distinguir o
que já está **publicado** na página do Apoiador. (`RF-14-18`, `RF-14-19`, `RF-14-20`, `RN-14-12`,
PRD-14 §5.9)

#### Scenario: A tela pede link, não arquivo

- **WHEN** o Apoiador abre a tela de comprobatórios
- **THEN** a tela pede endereço e rótulo de cada documento e não oferece campo de anexo de
  arquivo

#### Scenario: A declaração aparece antes do envio

- **WHEN** o Apoiador chega ao ponto de enviar o documento
- **THEN** a tela declara que ele só vai à página pública depois que um Admin o anexar

#### Scenario: A lista separa o publicado do pendente

- **WHEN** o Apoiador tem um documento já anexado por Admin e outro ainda não
- **THEN** a tela apresenta o primeiro como publicado na página dele e o segundo como pendente
