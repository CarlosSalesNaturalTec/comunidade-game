# Spec Delta

## ADDED Requirements

### Requirement: A linha da missão corrige e move a missão

A App 09 SHALL oferecer, em cada missão listada na trilha, o caminho de **corrigi-la** — título,
nível de dificuldade, obrigatoriedade, etapa do ciclo e sondagem — e de **movê-la** para cima ou
para baixo, em qualquer situação da trilha. A correção SHALL reaproveitar o formulário da
criação, já preenchido com o que está gravado, e NEVER SHALL oferecer a posição como campo. A
aplicação SHALL apresentar a recusa do núcleo com o motivo que ele declarou, nunca com código
de erro cru. Depois do movimento, a lista SHALL apresentar as missões na ordem que o núcleo
gravou. (`RF-09-136`, `RF-09-137`, `RN-09-57`)

#### Scenario: O Mestre corrige o título da missão

- **WHEN** o Mestre autor abre a correção de uma missão, troca o título e confirma
- **THEN** a aplicação grava a correção e passa a apresentar o título corrigido na linha

#### Scenario: A correção que muda a etapa leva a missão de página

- **WHEN** o Mestre autor corrige a etapa de uma missão de desenvolvimento para marcos
- **THEN** a missão deixa de aparecer em desenvolvimento e passa a aparecer em marcos

#### Scenario: O Mestre sobe uma missão

- **WHEN** o Mestre autor comanda subir a missão da terceira posição
- **THEN** a lista passa a apresentá-la na segunda posição, e a que estava ali na terceira

#### Scenario: A recusa do movimento chega com o motivo

- **WHEN** o Mestre autor comanda descer a missão de sondagem
- **THEN** a aplicação apresenta o motivo que o núcleo declarou, e a ordem segue a mesma

### Requirement: A tela avisa antes da correção que despublica a trilha

Quando o Mestre autor confirma a correção que desmarca a sondagem de trilha **publicada**, a App
09 SHALL dizer, **antes** de gravar, que a trilha sai do ar e que vai faltar a missão de
sondagem para publicar de novo, e SHALL gravar só se o Mestre confirmar. Depois de gravar, a
tela SHALL apresentar a trilha como despublicada, com o motivo da resposta, sem precisar
recarregar. Correção que não despublica NEVER SHALL pedir essa confirmação. (`RF-09-139`,
`RN-09-59`)

#### Scenario: O aviso aparece antes de gravar

- **WHEN** o Mestre autor desmarca a sondagem de missão de trilha publicada e confirma o
  formulário
- **THEN** a tela diz que a trilha vai sair do ar e que falta a sondagem, e nada é gravado ainda

#### Scenario: O Mestre desiste

- **WHEN** o Mestre autor recusa o aviso
- **THEN** nada é gravado e a trilha segue publicada

#### Scenario: O Mestre confirma

- **WHEN** o Mestre autor confirma o aviso
- **THEN** a correção é gravada e a tela apresenta a trilha despublicada, com o motivo

#### Scenario: Correção comum não pede confirmação

- **WHEN** o Mestre autor corrige o título de missão de trilha publicada
- **THEN** a aplicação grava sem pedir confirmação de despublicação

## MODIFIED Requirements

### Requirement: A aplicação apresenta ao Mestre as trilhas dele, com a situação de cada uma

A App 09 SHALL apresentar ao Mestre em sessão as trilhas de que ele é autor, com nome, poder,
área do conhecimento e **situação** — rascunho, publicada ou despublicada —, e NEVER SHALL
apresentar-lhe o rascunho de outro Mestre. Na trilha despublicada, a aplicação SHALL apresentar
o **motivo** registrado — pelo Admin, ou pelo núcleo quando a correção do próprio Mestre a
despublicou —, para que o autor saiba o que corrigir, e NEVER SHALL atribuir ao Admin o motivo
que ele não registrou. (`RF-09-04`, `RF-09-10`, `RN-09-59`)

#### Scenario: O Mestre lê os próprios rascunhos

- **WHEN** um Mestre em sessão abre a lista das trilhas dele
- **THEN** a aplicação apresenta as trilhas de que ele é autor, rascunhos inclusive, com a
  situação de cada uma

#### Scenario: Rascunho alheio não aparece

- **WHEN** um Mestre em sessão abre a lista das trilhas dele e outro Mestre tem trilha em
  rascunho
- **THEN** a trilha do outro Mestre não aparece na lista

#### Scenario: O motivo da despublicação aparece ao autor

- **WHEN** um Mestre em sessão abre a lista e uma trilha dele está despublicada
- **THEN** a aplicação apresenta a situação despublicada e o motivo registrado

#### Scenario: O motivo gerado pela correção não é atribuído ao Admin

- **WHEN** uma trilha do Mestre foi despublicada pela correção que ele próprio fez
- **THEN** a aplicação apresenta o motivo sem dizer que foi registrado pelo Admin
