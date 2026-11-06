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
apresentada como entrega faltando. A declaração **sem texto nem arquivo** SHALL dizer o que
de fato aconteceu: no prático **sem forma declarada**, que nada foi pedido; na forma em
**mídia**, que o arquivo **não chegou** e que o Guerreiro(a) ainda pode enviá-lo até o
julgamento — e NEVER SHALL afirmar envio em andamento que não existe. A mídia que **não
carrega** NEVER SHALL impedir o julgamento: a tela SHALL dizer que não abriu e seguir permitindo julgar. (`RF-09-26`,
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

#### Scenario: Prático sem forma declarada, declarado sem comprovação

- **WHEN** a pendência é de um prático sem forma declarada e não traz texto nem arquivo
- **THEN** a tela diz que o desafio não pedia comprovação, e os controles de julgamento seguem
  disponíveis

#### Scenario: Mídia cujo arquivo não chegou

- **WHEN** a pendência é de um prático em mídia e não traz arquivo nem entrega no encontro
- **THEN** a tela diz que o arquivo não chegou e que o Guerreiro(a) ainda pode enviá-lo, sem
  dizer que um envio está em andamento
