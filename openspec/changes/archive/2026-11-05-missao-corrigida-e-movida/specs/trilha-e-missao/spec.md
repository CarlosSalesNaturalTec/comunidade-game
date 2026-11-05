# Spec Delta

## ADDED Requirements

### Requirement: O Mestre autor corrige a missão que já criou

O núcleo SHALL aceitar do **Mestre autor da trilha** a correção de uma missão já gravada,
alcançando **título**, **nível de dificuldade**, **obrigatoriedade**, **etapa do ciclo** e
**sondagem**, em **qualquer situação da trilha** — rascunho, publicada ou despublicada. Campo
ausente na correção SHALL permanecer como estava. A **posição** NEVER SHALL mudar pela
correção: ela muda só pelo movimento.

As recusas da criação SHALL valer na correção: título vazio, obrigatoriedade nula e etapa fora
dos quatro valores do documento 11 §2.4 SHALL responder **422**; marcar como sondagem missão
que não ocupa a primeira posição, ou uma segunda missão da mesma trilha, SHALL responder
**422**. A correção NEVER SHALL alterar desbloqueio, submissão, produção, Resultado, nível ou
ponto já gravados. Mestre que não é o autor e Admin SHALL receber **403**. (`RF-09-136`,
`RN-09-56`, `RN-09-57`, invariante 2)

#### Scenario: O Mestre autor corrige o título

- **WHEN** o Mestre autor corrige o título de uma missão da própria trilha
- **THEN** o núcleo grava o título corrigido, e a missão segue na mesma posição

#### Scenario: A correção alcança a trilha publicada

- **WHEN** o Mestre autor corrige a dificuldade, a obrigatoriedade e a etapa de uma missão de
  trilha publicada
- **THEN** o núcleo grava a correção, e a trilha permanece publicada

#### Scenario: O que o Guerreiro(a) já fez não é tocado

- **WHEN** o Mestre autor torna obrigatória uma missão opcional que um Guerreiro(a) já
  desbloqueou
- **THEN** o núcleo grava a correção, e o desbloqueio e o nível já certificados permanecem

#### Scenario: Correção sem título é recusada

- **WHEN** o Mestre autor corrige a missão deixando o título vazio
- **THEN** o núcleo responde 422 indicando o campo e nada é alterado

#### Scenario: Etapa fora dos quatro valores é recusada na correção

- **WHEN** chega uma correção cuja etapa do ciclo não é abertura, desenvolvimento, marcos nem
  fechamento
- **THEN** o núcleo responde 422 e nada é alterado

#### Scenario: Sondagem fora da primeira posição é recusada na correção

- **WHEN** o Mestre autor marca como sondagem, pela correção, a missão da terceira posição
- **THEN** o núcleo responde 422 e nada é alterado

#### Scenario: Segunda sondagem é recusada na correção

- **WHEN** o Mestre autor marca como sondagem uma missão de trilha que já tem sondagem
- **THEN** o núcleo responde 422 e a sondagem existente permanece

#### Scenario: A posição não muda pela correção

- **WHEN** chega uma correção que informa a posição
- **THEN** o núcleo responde 422 e nada é alterado

#### Scenario: Outro Mestre é recusado

- **WHEN** um Mestre que não é o autor corrige a missão
- **THEN** o núcleo responde 403 e a missão permanece como estava

### Requirement: O Mestre autor move a missão na sequência da trilha

O núcleo SHALL aceitar do **Mestre autor da trilha** o movimento de uma missão **para cima** ou
**para baixo**, em qualquer situação da trilha. O movimento SHALL trocar a posição da missão com
a da **vizinha** na sequência — a missão de posição imediatamente anterior ou seguinte — e
NEVER SHALL alterar a posição de nenhuma outra missão. Direção que não é cima nem baixo SHALL
responder **422**; mover a primeira para cima ou a última para baixo SHALL responder **422** sem
alterar nada.

A sondagem SHALL permanecer na primeira posição: movê-la para baixo, ou mover para cima a
missão que está logo depois dela, SHALL responder **422** sem alterar nada. O movimento NEVER
SHALL alterar desbloqueio ou outro fato gravado do Guerreiro(a). Mestre que não é o autor e
Admin SHALL receber **403**. (`RF-09-137`, `RN-09-56`, `RN-09-57`, invariante 5)

#### Scenario: O Mestre autor sobe uma missão

- **WHEN** o Mestre autor sobe a missão da terceira posição
- **THEN** ela passa à segunda posição, a que estava na segunda passa à terceira, e as demais
  ficam onde estavam

#### Scenario: O movimento alcança a trilha publicada

- **WHEN** o Mestre autor desce uma missão de trilha publicada
- **THEN** o núcleo grava as duas posições trocadas, e a trilha permanece publicada

#### Scenario: A primeira não sobe

- **WHEN** o Mestre autor sobe a missão da primeira posição de trilha sem sondagem
- **THEN** o núcleo responde 422 e nada é alterado

#### Scenario: A última não desce

- **WHEN** o Mestre autor desce a missão da última posição
- **THEN** o núcleo responde 422 e nada é alterado

#### Scenario: A sondagem não desce

- **WHEN** o Mestre autor desce a missão de sondagem
- **THEN** o núcleo responde 422 dizendo que a sondagem abre a trilha, e nada é alterado

#### Scenario: Nenhuma missão sobe para o lugar da sondagem

- **WHEN** o Mestre autor sobe a missão que está logo depois da sondagem
- **THEN** o núcleo responde 422 e nada é alterado

#### Scenario: O desbloqueio já gravado permanece

- **WHEN** o Mestre autor move uma missão que um Guerreiro(a) já desbloqueou
- **THEN** o desbloqueio dela permanece gravado

#### Scenario: Direção inválida é recusada

- **WHEN** chega um movimento com direção que não é cima nem baixo
- **THEN** o núcleo responde 422 e nada é alterado

### Requirement: A correção que tira a sondagem da trilha publicada a despublica

Quando a correção desmarca a sondagem de missão de trilha **publicada**, o núcleo SHALL aceitar
a correção e, na mesma transação, SHALL passar a trilha a **despublicada**, gravando o **Mestre
autor** como autor da situação, o papel dele, o momento e um **motivo gerado pelo núcleo** que
nomeia a missão e a trava que ficou faltando. A resposta da correção SHALL dizer a situação e o
motivo resultantes. Correção de trilha em rascunho ou despublicada NEVER SHALL mudar a
situação dela, e a despublicação NEVER SHALL alterar fato gravado do Guerreiro(a). O Mestre
autor SHALL republicar pela rota e pelas travas de sempre. (`RN-09-59`, `RF-09-136`,
`RF-09-11`, invariante 5)

#### Scenario: Desmarcar a sondagem de trilha publicada despublica

- **WHEN** o Mestre autor desmarca a sondagem da missão da primeira posição de trilha publicada
- **THEN** o núcleo grava a correção, a trilha passa a despublicada com o Mestre como autor da
  situação, e o motivo nomeia a missão e a sondagem que falta

#### Scenario: A resposta diz que a trilha saiu do ar

- **WHEN** a correção despublica a trilha
- **THEN** a resposta traz a situação despublicada e o motivo gerado

#### Scenario: Rascunho não muda de situação

- **WHEN** o Mestre autor desmarca a sondagem de trilha em rascunho
- **THEN** o núcleo grava a correção e a trilha segue em rascunho

#### Scenario: Correção que não quebra trava não despublica

- **WHEN** o Mestre autor corrige o título de missão de trilha publicada
- **THEN** a trilha permanece publicada

#### Scenario: O autor republica depois de corrigir

- **WHEN** o Mestre autor volta a marcar a sondagem e publica a trilha despublicada pela
  correção
- **THEN** o núcleo publica a trilha e o motivo deixa de acompanhá-la

## MODIFIED Requirements

### Requirement: Só o Mestre autor escreve na sua trilha

O núcleo SHALL restringir a escrita de uma trilha, das missões dela e das atividades dela ao
**Mestre autor** da trilha e a **Admin**. Mestre que não é o autor SHALL receber **403**, ainda
que o papel dele permita escrever trilhas em geral. A leitura de trilha publicada SHALL seguir a
regra da capacidade, não a autoria. A **correção** e o **movimento** da missão são exceção: SHALL
ter autoria **estrita**, e o Admin SHALL receber **403**, como a correção do conteúdo e da
atividade. (`RF-01-16`, `RN-09-56`, PRD-01 §4)

#### Scenario: Mestre autor altera a sua trilha

- **WHEN** o Mestre autor de uma trilha altera a trilha ou uma missão dela
- **THEN** o núcleo executa a alteração e grava a autoria

#### Scenario: Outro Mestre é recusado

- **WHEN** um Mestre que não é o autor tenta alterar a trilha
- **THEN** o núcleo responde 403 e a trilha permanece como estava

#### Scenario: Admin alcança qualquer trilha

- **WHEN** um Admin acrescenta missão a uma trilha de que não é autor
- **THEN** o núcleo executa a escrita, porque a matriz do PRD-01 §4 dá tudo ao Admin

#### Scenario: Admin não corrige nem move a missão

- **WHEN** um Admin corrige ou move uma missão de trilha de que não é autor
- **THEN** o núcleo responde 403 e a missão permanece como estava

### Requirement: Só o Admin despublica, sempre com motivo, e o autor lê o motivo

O núcleo SHALL permitir que **somente Admin** despublique trilha publicada **a pedido**, **sempre
com motivo** — pedido sem motivo SHALL responder 422 e pedido de Mestre SHALL responder **403**.
A única despublicação que não é pedido do Admin é a que decorre da correção da missão que tira
a sondagem da trilha publicada, de que trata o requisito próprio. (`RN-09-59`) A
despublicação SHALL gravar, junto da situação, o **motivo**, o **autor** do ato, o **papel**
dele e o **momento**, e o núcleo SHALL entregar o motivo ao **Mestre autor** na leitura das
trilhas dele. Despublicar NEVER SHALL alterar missão, atividade, resultado, presença ou
pontuação já gravados: o percurso já realizado pelos Guerreiros e Guerreiras permanece
íntegro. (`RF-09-10`, `RF-09-11`, `RN-09-01`)

#### Scenario: Admin despublica com motivo

- **WHEN** um Admin despublica trilha publicada informando o motivo
- **THEN** o núcleo grava a situação despublicada com motivo, autor, papel e momento

#### Scenario: Despublicação sem motivo é recusada

- **WHEN** um Admin despublica sem informar motivo
- **THEN** o núcleo responde 422 e a trilha segue publicada

#### Scenario: Mestre não despublica

- **WHEN** o Mestre autor pede a despublicação da própria trilha
- **THEN** o núcleo responde 403 e a trilha segue publicada

#### Scenario: O Mestre autor lê o motivo

- **WHEN** o Mestre autor consulta as trilhas dele depois de uma despublicação
- **THEN** o motivo registrado vem junto da trilha despublicada

#### Scenario: O percurso já realizado permanece

- **WHEN** uma trilha com resultados e presenças já gravados é despublicada
- **THEN** nenhum resultado, presença ou ponto é alterado ou removido

#### Scenario: Trilha em rascunho não é despublicável

- **WHEN** um Admin pede a despublicação de trilha em rascunho
- **THEN** o núcleo responde 422 e a situação permanece rascunho
