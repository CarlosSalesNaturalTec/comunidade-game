# Spec Delta

## MODIFIED Requirements

### Requirement: A App 09 mostra ao Mestre autor os desafios práticos a julgar

A aplicação SHALL listar ao **Mestre autor** os **desafios práticos declarados como cumpridos**
pelos Guerreiros e Guerreiras das suas trilhas e ainda **não julgados**, cada um com o
Guerreiro(a), a missão e quando foi declarado. Declaração de trilha de outro Mestre NEVER SHALL
aparecer nesta lista.

Cada pendência SHALL trazer, junto disso, **a produção entregue** e o **critério de aceite** que
o próprio Mestre declarou no desafio — julgar sem ver o que foi entregue é julgar às cegas, e o
critério é o que ele escreveu para julgar por ele. A tela SHALL **apresentar** a comprovação
conforme a forma dela: o corpo escrito e o endereço como texto, e a **imagem**, o **áudio** e o
**vídeo** exibidos ou tocados na própria bancada, buscando os bytes do núcleo. O **arquivo** que
não se exibe SHALL vir com o controle de abri-lo. A declaração de **entrega no encontro** SHALL
ser dita como tal — que o Guerreiro(a) vai entregar presencialmente —, e NEVER SHALL ser
apresentada como entrega faltando. A mídia que **não carrega** NEVER SHALL impedir o
julgamento: a tela SHALL dizer que não abriu e seguir permitindo julgar. (`RF-09-26`,
`RF-09-132`, `RF-09-130`, `RF-05-93`, `RF-05-13`, `RF-05-14`)

#### Scenario: A lista traz o que espera julgamento

- **WHEN** o Mestre autor abre a bancada dos desafios práticos
- **THEN** vê as declarações ainda não julgadas das suas trilhas, com Guerreiro(a), missão e
  data

#### Scenario: A produção entregue aparece na bancada

- **WHEN** o Mestre autor abre a bancada e uma pendência traz comprovação em imagem
- **THEN** a imagem é exibida na própria bancada, ao lado do critério de aceite que ele
  declarou

#### Scenario: A comprovação escrita aparece como texto

- **WHEN** a pendência traz comprovação em texto ou em link externo
- **THEN** a tela apresenta o corpo escrito ou o endereço, sem exigir que o Mestre o abra em
  outro lugar

#### Scenario: A entrega no encontro é dita como tal

- **WHEN** a pendência é uma declaração de entrega ao Mestre no encontro
- **THEN** a tela diz que a entrega é presencial, e não a apresenta como comprovação faltando

#### Scenario: A mídia que não carrega não impede julgar

- **WHEN** os bytes da comprovação não chegam
- **THEN** a tela diz que a mídia não abriu e os controles de julgamento seguem disponíveis

#### Scenario: Julgar abre a missão seguinte para aquele Guerreiro(a)

- **WHEN** o Mestre autor julga que um Guerreiro(a) cumpriu o desafio prático
- **THEN** a declaração sai da lista e a missão seguinte abre para aquele Guerreiro(a)

#### Scenario: Declaração de trilha alheia não aparece

- **WHEN** o Mestre abre a bancada dos desafios práticos
- **THEN** nenhuma declaração de trilha de que ele não é autor é listada

## ADDED Requirements

### Requirement: A bancada julga pelos dois vereditos, com o motivo

A bancada SHALL oferecer ao Mestre autor os **dois vereditos** em controles distintos —
**cumpriu** e **publicável** — e o campo do **motivo**, e SHALL enviá-los **num ato só** por
Guerreiro(a). A tela SHALL dizer, em linguagem do Mestre, o que cada veredito faz: que
**cumpriu** abre a missão seguinte e credita os **5 pontos**, e que **publicável** é o que leva
aquela entrega à vitrine pública — e apenas isso.

O controle de **publicável** SHALL ficar indisponível quando a declaração não admite o veredito
— quando o Mestre marcou que **não cumpriu**, e na **entrega presencial**, que não tem
comprovação a publicar —, em vez de ser recusado depois do toque. O **motivo** SHALL ser exigido
na própria tela quando o julgamento nega algo: o controle de julgar SHALL ficar indisponível
enquanto o motivo estiver vazio num julgamento de **não cumpriu** ou de **cumpriu e não
publicável**. A tela SHALL dizer que o motivo é lido **pelo Guerreiro(a)**, e por isso se
escreve em linguagem simples.

A tela SHALL dizer que **não passar não elimina** o Guerreiro(a) e que ele pode entregar de
novo. A recusa do núcleo SHALL chegar ao Mestre **com o motivo**, sem apagar o que ele escreveu
nem o veredito que marcou. Julgada, a pendência SHALL **sair da lista**. (`RF-09-133`,
`RF-09-134`, `RF-09-135`, `RN-09-52`, `RN-09-53`, `RF-09-117`)

#### Scenario: Os dois vereditos e o motivo vão num ato só

- **WHEN** o Mestre autor marca cumpriu e publicável e julga
- **THEN** o núcleo recebe os dois vereditos e o motivo numa única operação, e a pendência sai
  da lista

#### Scenario: A tela diz o que cada veredito faz

- **WHEN** o Mestre autor abre uma pendência da bancada
- **THEN** a tela diz que cumpriu abre a missão seguinte e credita 5 pontos, e que publicável
  leva a entrega à vitrine

#### Scenario: Publicável fica indisponível no que não cumpriu

- **WHEN** o Mestre autor marca que o Guerreiro(a) não cumpriu
- **THEN** o controle de publicável fica indisponível, sem precisar do toque para ser recusado

#### Scenario: Publicável fica indisponível na entrega presencial

- **WHEN** a pendência é uma declaração de entrega no encontro
- **THEN** o controle de publicável fica indisponível, e a tela diz que não há comprovação a
  publicar

#### Scenario: O motivo é exigido antes do toque

- **WHEN** o Mestre autor marca que não cumpriu e deixa o motivo vazio
- **THEN** o controle de julgar fica indisponível até ele escrever o motivo

#### Scenario: Cumpriu e publicável dispensa o motivo na tela

- **WHEN** o Mestre autor marca cumpriu e publicável, sem escrever motivo
- **THEN** o controle de julgar fica disponível

#### Scenario: A tela diz que não passar não elimina

- **WHEN** o Mestre autor abre a bancada
- **THEN** a tela diz que não passar não elimina o Guerreiro(a) e que ele pode entregar de novo

#### Scenario: A recusa do núcleo chega com o motivo e sem limpar a tela

- **WHEN** o núcleo recusa o julgamento
- **THEN** a tela apresenta o motivo da recusa, e o veredito marcado e o texto escrito
  permanecem como estavam
