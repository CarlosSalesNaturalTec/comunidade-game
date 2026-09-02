## MODIFIED Requirements

### Requirement: A porta pública oferece as formas de declarar o aporte, sempre com o equivalente em moedas

A porta pública SHALL oferecer, a quem aporta em dinheiro, a **missão aberta**, a
**necessidade publicada**, o **valor sugerido** da escada do perfil declarado e o **valor
livre**, e SHALL exibir o **equivalente em moedas** ao lado de cada valor, na mesma tela. O
degrau da escada SHALL ser sugestão e não piso: o valor livre SHALL aceitar qualquer quantia,
com fração de duas casas. (`RF-14-02`, `RF-14-03`, `RN-14-40`, PRD-14 §§5.1, 12)

#### Scenario: O visitante assume uma missão aberta

- **WHEN** o visitante escolhe uma das missões abertas
- **THEN** a tela declara o aporte por aquela missão, com o que ela pede em moedas

#### Scenario: O visitante assume uma necessidade publicada

- **WHEN** o visitante escolhe uma das necessidades de recurso em aberto
- **THEN** a tela declara o aporte por aquela necessidade, com o que ela pede em moedas

#### Scenario: A escada do perfil aparece com o equivalente em moedas

- **WHEN** o visitante declara o perfil e vê os valores sugeridos
- **THEN** cada degrau aparece com o equivalente em moedas ao lado

#### Scenario: O valor livre aceita qualquer quantia

- **WHEN** o visitante informa um valor livre abaixo do menor degrau da sua escada, com fração
  de duas casas
- **THEN** a tela aceita o valor e exibe o equivalente em moedas antes do envio

### Requirement: O Apoiador declara o aporte por necessidade, por sugestão ou por valor livre

A aplicação SHALL oferecer ao Apoiador em sessão quatro caminhos para declarar um aporte novo:
a partir de uma **missão aberta**, de uma **necessidade em aberto**, por um **valor sugerido**
da escada do perfil que ele declarar na própria tela, ou por **valor livre**. O degrau da
escada SHALL ser sugestão e não piso: o valor livre SHALL aceitar qualquer quantia, com fração
de duas casas. A tela SHALL exigir o **anexo do comprovante** da transferência para enviar e
SHALL declarar os formatos aceitos; recusado o comprovante pelo núcleo, SHALL apresentar a
recusa com os formatos válidos. (`RF-14-25`, `RF-14-26`, `RF-14-63`, `RN-14-06`, PRD-14
§§5.3, 5.4, 6.3, 12)

#### Scenario: A missão escolhida abre a declaração

- **WHEN** o Apoiador escolhe cobrir uma missão aberta, inteira ou em parte
- **THEN** a tela declara o aporte por aquela missão, com o que falta a ela em moedas

#### Scenario: A necessidade escolhida abre a declaração

- **WHEN** o Apoiador escolhe cobrir uma necessidade em aberto
- **THEN** a tela declara o aporte por aquela necessidade, com o que ela pede em moedas

#### Scenario: A escada do perfil aparece com o equivalente em moedas

- **WHEN** o Apoiador declara o perfil na tela e vê os valores sugeridos
- **THEN** cada degrau aparece com o equivalente em moedas ao lado

#### Scenario: O valor livre aceita qualquer quantia

- **WHEN** o Apoiador informa um valor livre abaixo do menor degrau da escada, com fração de
  duas casas
- **THEN** a tela aceita o valor e mostra o equivalente em moedas antes do envio

#### Scenario: Sem comprovante a declaração não é enviada

- **WHEN** o Apoiador tenta enviar a declaração sem anexar comprovante
- **THEN** a tela recusa o envio e diz quais formatos valem

## ADDED Requirements

### Requirement: A área Missões agrupa as missões abertas pelo nível de necessidade

A App 08 SHALL abrir a área **Missões** com as missões abertas **agrupadas pelo nível de
necessidade** que sustentam — existir, acontecer, reconhecer, permanecer —, cada uma com o que
se pede, **quanto falta em moedas**, o prazo e o **selo que rende**. O quanto já foi coberto
SHALL aparecer como **quantidade**, e a tela NEVER SHALL identificar quem cobriu. Missão sem
necessidade publicada por trás, vencida ou concluída NEVER SHALL aparecer na área.
(`RF-14-60`, `RF-14-61`, `RF-14-62`, `RF-14-71`, `RF-14-72`)

#### Scenario: As missões aparecem agrupadas pelo nível

- **WHEN** o Apoiador abre a área Missões
- **THEN** as missões abertas aparecem em quatro grupos, cada missão com o que se pede, o que
  falta em moedas, o prazo e o selo

#### Scenario: O coberto aparece sem nome de quem cobriu

- **WHEN** uma missão já foi coberta em parte
- **THEN** a tela mostra a quantidade coberta e nenhum nick, avatar ou valor de quem cobriu

#### Scenario: A missão vencida some da área

- **WHEN** o prazo de uma missão vence sem que ela feche
- **THEN** ela deixa de aparecer na área Missões

### Requirement: A tela declara que só a homologação abate e conclui

A área Missões SHALL declarar, antes do envio, que o aporte nasce **pendente**, que não abate o
que falta e que não conclui missão alguma até o Admin homologar. Coberta em parte, a tela SHALL
mostrar a missão ainda **aberta** com o restante atualizado, sem selo creditado. (`RF-14-64`,
`RF-14-65`, `RN-14-32`, PRD-14 §5.4)

#### Scenario: A tela avisa que a declaração não abate nada

- **WHEN** o Apoiador vai declarar um aporte por uma missão
- **THEN** a tela declara que o aporte entra pendente e não abate o que falta nem conclui a
  missão

#### Scenario: A cobertura parcial mostra o restante

- **WHEN** um aporte do Apoiador para uma missão é homologado e ela segue aberta
- **THEN** a tela mostra a missão aberta com o restante atualizado e nenhum selo novo

### Requirement: A área de sustento mostra o nível, os selos e a frente que falta

A App 08 SHALL apresentar ao Apoiador o **nível de sustento** alcançado, os **selos
conquistados agrupados por família** e a **frente que falta** para o próximo nível — **uma
vez, sem insistir**: sem repetição em outras telas, sem lembrete e sem contagem regressiva.
Concluída uma missão, a tela SHALL mostrar o **selo novo** e, quando houver, o nível alcançado.
A aplicação NEVER SHALL exibir nível ou selo regredindo. (`RF-14-67`, `RF-14-68`, `RF-14-69`,
`RN-14-36`, PRD-14 §5.4)

#### Scenario: O sustento aparece com a frente que falta

- **WHEN** o Apoiador abre a área de sustento
- **THEN** a tela mostra o nível atual, os selos agrupados por família e a frente que falta para
  o próximo nível

#### Scenario: A frente que falta aparece uma vez

- **WHEN** o Apoiador navega pelas demais telas da aplicação
- **THEN** nenhuma delas repete o convite ao próximo nível

#### Scenario: A conclusão mostra o selo novo

- **WHEN** uma missão de que o Apoiador participou é concluída
- **THEN** a tela mostra o selo novo e, se for o caso, o nível de sustento alcançado

### Requirement: Nenhuma tela do Apoiador compara apoiadores por valor

Nenhuma tela da App 08 SHALL ordenar, classificar ou comparar apoiadores por valor aportado, e
NEVER SHALL apresentar pódio, posição ou ranking. O card e a página públicos do Apoiador SHALL
exibir o **nível de sustento** e os **selos**. (`RF-14-70`, `RF-14-73`, `RN-14-38`)

#### Scenario: Nenhuma lista ordena por valor

- **WHEN** o Apoiador percorre as telas da aplicação
- **THEN** nenhuma delas apresenta apoiadores em ordem de valor, posição ou pódio

#### Scenario: O card público mostra nível e selos

- **WHEN** a página pública do Apoiador é montada
- **THEN** ela exibe o nível de sustento e os selos conquistados, ao lado do avatar, do nick e
  do total em moedas
