## Purpose

O painel vivo que responde ao Apoiador o que o apoio dele produziu — quais desafios engajaram,
quantos Guerreiros e Guerreiras concluíram, em que trilhas, quanto foi aportado e a que
objetivos da Agenda 2030 aquilo contribuiu — sempre agregado e sem identificar criança.

## ADDED Requirements

### Requirement: O painel de efetividade é vivo, sem fechamento nem periodicidade

O núcleo SHALL devolver ao Apoiador em sessão um painel de efetividade que reflete a **última
conclusão registrada**, sem espera por período, fechamento ou consolidação. NEVER SHALL existir
rota, arquivo ou tela de **relatório fechado** de efetividade no Ciclo 01. (`RF-14-40`,
`RN-14-21`, PRD-14 §§5.7, 12)

#### Scenario: A conclusão do dia já aparece no painel

- **WHEN** uma conclusão de desafio extra é registrada e o proponente abre o painel no mesmo dia
- **THEN** o painel já contabiliza essa conclusão

#### Scenario: Não há relatório fechado

- **WHEN** o Apoiador procura um fechamento periódico da efetividade
- **THEN** nenhuma rota o oferece, e a leitura disponível é sempre o painel vivo

### Requirement: O painel lista os desafios do proponente por situação

O painel SHALL trazer os desafios extras **do próprio proponente** separados entre
**propostos**, **publicados** e **concluídos**, e NEVER SHALL trazer desafio de outro
proponente. Desafio é **concluído** quando há ao menos uma conclusão registrada para ele.
(`RF-14-41`, PRD-14 §5.7)

#### Scenario: Cada desafio aparece na sua situação

- **WHEN** o Apoiador abre o painel tendo desafios em validação, publicados e com conclusão
  registrada
- **THEN** o painel os apresenta separados entre propostos, publicados e concluídos

#### Scenario: O painel não alcança desafio alheio

- **WHEN** outro Apoiador propôs desafios na mesma trilha
- **THEN** nenhum deles aparece no painel de quem consulta

### Requirement: O painel informa quantos concluíram, em que trilha e em que período

Para cada desafio, o painel SHALL trazer a **quantidade de conclusões registradas**, a
**trilha** a que o desafio se vincula e o **período** em que as conclusões aconteceram — a data
da primeira e a da última. (`RF-14-42`, PRD-14 §5.7)

#### Scenario: O desafio concluído traz contagem, trilha e período

- **WHEN** o Apoiador abre um desafio com conclusões registradas
- **THEN** o painel traz quantos concluíram, a trilha do desafio e a data da primeira e da
  última conclusão

#### Scenario: Desafio sem conclusão traz contagem zero

- **WHEN** o desafio está publicado e ninguém o concluiu
- **THEN** o painel traz contagem zero e nenhum período

### Requirement: O painel mostra as moedas aportadas e o que elas custearam

O painel SHALL trazer o total de **moedas aportadas** pelo Apoiador, com o que cada aporte
custeou: a necessidade ou a missão do Apoiador que atendeu e o desafio extra a que serviu de
lastro. Todo valor SHALL sair em **moedas**; NEVER SHALL sair em reais. Aporte **pendente de
homologação** NEVER SHALL compor o painel. (`RF-14-43`, `RN-14-09`, `RN-14-07`, PRD-14 §5.7,
invariante 16)

#### Scenario: Cada aporte aparece com o que custeou

- **WHEN** o Apoiador abre o painel
- **THEN** cada aporte homologado aparece com o valor em moedas e com o que custeou

#### Scenario: A declaração pendente não entra no painel

- **WHEN** o Apoiador tem aporte declarado ainda não homologado
- **THEN** ele não aparece no painel nem soma ao total de moedas

#### Scenario: Nenhum valor sai em reais

- **WHEN** o painel é montado
- **THEN** nenhum campo dele traz valor em reais

### Requirement: A cobertura de ODS é herdada, agregada e descritiva

O painel SHALL trazer a **cobertura de ODS** herdada das missões a que os desafios do Apoiador
se vincularam — e, quando o desafio não declara missão, das etiquetas da trilha —, **agregada
por Comunidade Virtual e por ciclo**. A cobertura SHALL ser apresentada como **descrição do que
foi tocado**, NEVER como mérito, nota, pontuação ou classificação do apoio, e NEVER SHALL
descer ao Guerreiro(a). (`RF-14-44`, `RN-14-28`, PRD-14 §5.7, invariante 20)

#### Scenario: A cobertura sai por comunidade e ciclo

- **WHEN** o Apoiador abre a cobertura de ODS do painel
- **THEN** os objetivos aparecem agregados por Comunidade Virtual e por ciclo

#### Scenario: A cobertura não vira mérito

- **WHEN** a cobertura de ODS é apresentada
- **THEN** ela não traz nota, pontuação, posição nem comparação entre apoiadores

#### Scenario: Cada desafio traz as etiquetas que herdou

- **WHEN** o painel apresenta um desafio publicado ainda sem conclusão
- **THEN** ele traz as etiquetas de ODS herdadas da missão, ou da trilha quando não há missão
  declarada, e não entra na agregação por comunidade

#### Scenario: A cobertura não desce ao indivíduo

- **WHEN** a cobertura é montada
- **THEN** nenhum objetivo aparece ligado a um Guerreiro(a)

### Requirement: Quem concluiu aparece só por avatar e nick, e só com divulgação autorizada

O painel SHALL identificar quem concluiu um desafio **apenas por avatar e nick**, e **somente**
quando o Guerreiro(a) tem **autorização de divulgação vigente**. Sem ela, a conclusão SHALL
entrar **apenas na contagem agregada**, sem avatar, sem nick e sem qualquer outro dado. NEVER
SHALL o painel trazer nome real, contato, idade, turma, evolução ou qualquer dado de
identificação de Guerreiro(a). (`RF-14-45`, `RF-14-46`, `RF-14-39`, `RN-14-20`, `RN-14-22`,
PRD-14 §§11, 12, invariantes 10 e 12)

#### Scenario: Com divulgação autorizada aparece avatar e nick

- **WHEN** quem concluiu tem autorização de divulgação vigente
- **THEN** o painel mostra o avatar e o nick, e nada além disso

#### Scenario: Sem divulgação autorizada entra só na contagem

- **WHEN** quem concluiu não tem autorização de divulgação vigente
- **THEN** a conclusão soma à contagem do desafio e nenhum avatar ou nick é exibido

#### Scenario: A revogação tira o avatar do painel

- **WHEN** a autorização de divulgação de quem concluiu é revogada
- **THEN** a leitura seguinte do painel deixa de exibir o avatar e o nick, mantendo a contagem

### Requirement: No direcionado o proponente vê apenas que houve conclusão

Para o desafio **direcionado**, o painel SHALL informar somente **se houve conclusão**. NEVER
SHALL trazer avatar, nick, trilha do destinatário, evolução ou qualquer outro dado dele — nem
quando o destinatário tem autorização de divulgação vigente. (`RF-14-47`, `RN-14-22`,
`RN-14-18`, PRD-14 §5.7, invariante 12)

#### Scenario: O direcionado concluído informa só o fato

- **WHEN** o desafio direcionado do Apoiador é concluído
- **THEN** o painel informa que houve conclusão, sem avatar, nick, trilha ou qualquer dado do
  destinatário

#### Scenario: O direcionado não concluído não revela nada

- **WHEN** o desafio direcionado ainda não foi concluído
- **THEN** o painel informa apenas que não houve conclusão, sem dizer se o nick existe

### Requirement: O painel é do próprio Apoiador e de mais ninguém

O painel de efetividade SHALL exigir **sessão de Apoiador** e SHALL responder sempre com os
dados de **quem está em sessão**. NEVER SHALL aceitar identificador de outro Apoiador no
caminho ou em parâmetro, e outro papel SHALL receber recusa de permissão. (`RF-14-40`,
`RN-14-20`, PRD-14 §§4, 9)

#### Scenario: Outro papel é recusado

- **WHEN** uma sessão que não é de Apoiador pede o painel
- **THEN** o núcleo recusa com permissão negada

#### Scenario: Não há como apontar para outro Apoiador

- **WHEN** o painel é consultado
- **THEN** a resposta traz apenas os desafios e aportes de quem está em sessão
