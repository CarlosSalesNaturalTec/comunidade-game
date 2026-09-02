## ADDED Requirements

### Requirement: O desafio extra publicado alcança o Guerreiro(a) elegível

O núcleo SHALL servir ao **Guerreiro(a) em sessão** os desafios extras que lhe são elegíveis:
os que estão em **publicado**, com a **vigência correndo na data da consulta**, vinculados a
uma trilha em que ele está **inscrito**, e que sejam **abertos** ou **direcionados ao nick
dele**. O nick SHALL ser comparado sem distinguir maiúsculas de minúsculas, no mesmo critério
de unicidade do nick.

Desafio em **em validação do Mestre**, **em aprovação do Admin** ou **recusado** NEVER SHALL
aparecer, e desafio **já encerrado pelo Admin** NEVER SHALL aparecer ainda que a vigência dele
siga correndo; desafio fora da vigência NEVER SHALL aparecer; desafio de trilha em que o
Guerreiro(a) não está inscrito NEVER SHALL aparecer, **inclusive quando direcionado ao nick
dele**. Guerreiro(a) sem desafio elegível SHALL receber conjunto vazio, nunca erro.
(`RF-05-20`, `RF-14-33`, `RN-14-16`, `RN-14-17`)

#### Scenario: O aberto alcança todos os inscritos na trilha

- **WHEN** um desafio extra aberto está publicado e vigente numa trilha em que o Guerreiro(a)
  está inscrito
- **THEN** ele aparece na leitura desse Guerreiro(a)

#### Scenario: O direcionado alcança só o dono do nick

- **WHEN** um desafio extra direcionado está publicado e vigente numa trilha em que dois
  Guerreiros estão inscritos, com o nick de um deles
- **THEN** ele aparece só na leitura do dono daquele nick

#### Scenario: O nick casa sem distinguir maiúsculas

- **WHEN** o proponente digitou o nick do destinatário com grafia diferente da cadastrada,
  variando só maiúsculas e minúsculas
- **THEN** o desafio aparece na leitura do dono do nick, como se a grafia coincidisse

#### Scenario: O direcionado a quem não está na trilha não aparece

- **WHEN** um desafio extra direcionado traz o nick de um Guerreiro(a) que não está inscrito na
  trilha do desafio
- **THEN** ele não aparece na leitura desse Guerreiro(a)

#### Scenario: Desafio ainda não publicado não aparece

- **WHEN** um desafio extra está em validação do Mestre ou em aprovação do Admin numa trilha em
  que o Guerreiro(a) está inscrito
- **THEN** ele não aparece na leitura

#### Scenario: Desafio recusado ou encerrado não aparece

- **WHEN** um desafio extra foi recusado, ou foi publicado e depois encerrado pelo Admin
- **THEN** ele não aparece na leitura de Guerreiro(a) algum

#### Scenario: Desafio fora da vigência não aparece

- **WHEN** a data da consulta é anterior ao início ou posterior ao fim da vigência de um
  desafio publicado
- **THEN** ele não aparece na leitura

#### Scenario: Sem desafio elegível a resposta é conjunto vazio

- **WHEN** o Guerreiro(a) em sessão não tem nenhum desafio extra elegível
- **THEN** o núcleo responde com conjunto vazio, nunca erro

### Requirement: A leitura do Guerreiro(a) traz o que o desafio oferece e não identifica pessoa

Cada desafio extra devolvido ao Guerreiro(a) SHALL trazer a **recompensa oferecida** — o tipo
de recurso e o ponto de apoio em que está —, a **quantidade disponível**, a **quantidade
restante**, o **período de vigência**, o **critério de atribuição**, os **pontos extras** que
vale, o **formato**, a **modalidade** e a trilha e a missão a que se prende. O desafio cuja
quantidade restante é **zero** SHALL continuar sendo devolvido enquanto vigente e publicado,
com a restante em zero.

A resposta NEVER SHALL trazer o **nick do destinatário** de um direcionado — nem o do próprio
leitor, nem o de terceiro —, a **justificativa do vínculo ou pedagógica**, o **parecer do
Mestre**, o **motivo da recusa**, o **custeio**, o **lastro** ou qualquer outro dado do
proponente ou de outro Guerreiro(a). (`RF-05-21`, `RN-05-18`, `RN-05-21`, `RN-14-20`)

#### Scenario: A leitura traz a recompensa, a quantidade e a vigência

- **WHEN** o Guerreiro(a) lê um desafio extra elegível
- **THEN** a resposta traz a recompensa oferecida, a quantidade disponível, a quantidade
  restante, a vigência, o critério, os pontos extras e o formato

#### Scenario: O esgotado continua sendo devolvido

- **WHEN** um desafio extra publicado e vigente já teve todas as recompensas entregues
- **THEN** ele continua na leitura, com quantidade restante zero

#### Scenario: A leitura não devolve nick de destinatário

- **WHEN** o Guerreiro(a) lê um desafio extra direcionado a ele
- **THEN** a resposta não traz o nick do destinatário nem a justificativa que o proponente
  registrou

#### Scenario: A leitura não devolve o trâmite da proposta

- **WHEN** o Guerreiro(a) lê um desafio extra elegível
- **THEN** a resposta não traz parecer do Mestre, motivo de recusa, custeio nem estado do
  lastro
