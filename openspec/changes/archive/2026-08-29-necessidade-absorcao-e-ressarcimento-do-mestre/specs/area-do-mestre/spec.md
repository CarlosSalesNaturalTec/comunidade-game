## ADDED Requirements

### Requirement: A App 09 apresenta ao Mestre as necessidades de recurso das aulas dele

A App 09 SHALL apresentar ao Mestre a lista das **necessidades de recurso** das aulas das
comunidades a que ele está vinculado, cada uma com o **tipo de recurso**, a **quantidade que
falta**, o **valor em moedas**, o **ponto de apoio** e a **data e o horário da aula**
(`RF-09-56`). A falta é o que impede a atividade de acontecer: a necessidade existe justamente
para a falta virar pedido, e não recusa silenciosa (`RN-09-12`).

A lista SHALL vir **derivada do núcleo**: a aplicação NEVER SHALL somar, reordenar por saldo nem
recalcular a falta, e NEVER SHALL apresentar necessidade de aula de comunidade a que o Mestre
não está vinculado — o recorte é do núcleo, e a tela não o alarga.

A aplicação NEVER SHALL apresentar valor **em reais** nesta lista, nem dado de pessoa: a
necessidade descreve recurso, aula e lugar. Necessidade cujo tipo de recurso esteja **sem valor
de referência vigente** SHALL continuar aparecendo, com a quantidade que falta e declarando que
não há valor de referência vigente, e a aplicação NEVER SHALL arbitrar valor nem nome no lugar
do que o núcleo não serviu.

#### Scenario: O Mestre vê a falta das aulas da comunidade dele

- **WHEN** o Mestre abre a área de recursos e há aula pendente de lastro na comunidade dele
- **THEN** a aplicação apresenta a necessidade com o tipo de recurso, a quantidade que falta, o
  valor em moedas, o ponto de apoio e a data e o horário da aula

#### Scenario: A lista não traz reais

- **WHEN** as necessidades são apresentadas
- **THEN** nenhum valor em reais aparece na lista

#### Scenario: A necessidade sem valor de referência vigente continua na lista

- **WHEN** o tipo de recurso em falta não tem valor de referência vigente
- **THEN** a aplicação apresenta a necessidade com a quantidade que falta e declara que não há
  valor de referência vigente, sem arbitrar um

#### Scenario: Sem necessidade em aberto a lista diz isso

- **WHEN** não há aula pendente de lastro na comunidade do Mestre
- **THEN** a aplicação declara que não há necessidade de recurso em aberto

### Requirement: O Mestre assume a necessidade como absorção em um ato de confirmação

A App 09 SHALL oferecer, **a partir da própria necessidade**, assumir o recurso como **aporte
por absorção**, em um **ato de confirmação** — um passo só, sem homologação de Admin
(`RF-09-57`). A absorção SHALL declarar a **aula** cuja necessidade atende, e o tipo de recurso
e o ponto de apoio SHALL ser os da necessidade de origem, nunca escolhidos à parte.

A aplicação SHALL apresentar que o aporte nasce **em nome do próprio Mestre** e **marcado como
ressarcível**, e que a aula é confirmada assim que o saldo fechar, sem intervenção de Admin
(`RF-09-58`, `RN-09-13`). Ela NEVER SHALL oferecer registrar aporte em nome de outra persona,
homologar aporte algum, nem declarar a destinação — a absorção não a escolhe.

O formulário SHALL exigir o **valor de origem em reais** quando o tipo de recurso for de
natureza **consumível, durável ou financeira**, porque houve desembolso e é esse valor que o
ressarcimento devolve, e NEVER SHALL exigi-lo na natureza **serviço**. Onde o valor em reais for
pedido, a aplicação SHALL apresentá-lo **ao lado do equivalente em moedas**. O formulário SHALL
exigir o **comprovante** quando o tipo de recurso o exigir, e NEVER SHALL aceitar arquivo que não
seja PDF, JPG ou PNG.

Quantidade **menor que a falta** SHALL ser aceita: ela credita, a necessidade reaparece com a
falta abatida e a aula segue pendente de lastro. Fechado o saldo, a necessidade SHALL sair da
lista e a aula SHALL aparecer confirmada.

Recusado o registro pelo núcleo — valor de origem em falta, comprovante exigido e ausente, tipo
que a aula não consome ou tipo sem vigência que cubra a data —, a aplicação SHALL apresentar o
que está errado em **linguagem simples**, e a necessidade SHALL continuar na lista (`RN-09-16`).

#### Scenario: O Mestre absorve a necessidade em um ato

- **WHEN** o Mestre assume uma necessidade, informa a quantidade e o valor de origem em reais e
  confirma
- **THEN** a aplicação registra o aporte em nome dele, apresenta-o como ressarcível e recarrega
  a lista de necessidades

#### Scenario: A absorção parcial abate a falta e a aula segue pendente

- **WHEN** o Mestre absorve quantidade menor do que a falta
- **THEN** a aplicação apresenta a mesma necessidade com a falta abatida

#### Scenario: A absorção que fecha o saldo tira a necessidade da lista

- **WHEN** o Mestre absorve exatamente o que faltava à aula
- **THEN** a necessidade deixa de ser apresentada e a aula aparece confirmada

#### Scenario: O valor de origem é exigido onde houve desembolso

- **WHEN** o Mestre assume uma necessidade de tipo de natureza consumível
- **THEN** a aplicação pede o valor de origem em reais, ao lado do equivalente em moedas, e não
  envia o registro sem ele

#### Scenario: A absorção de serviço não pede reais

- **WHEN** o Mestre assume uma necessidade de tipo de natureza serviço
- **THEN** nenhum campo de valor em reais é apresentado, e o registro é enviado sem ele

#### Scenario: A aplicação não oferece homologação nem provedor alheio

- **WHEN** o Mestre abre o ato de absorção
- **THEN** nenhum campo de provedor, de homologação ou de destinação é apresentado

#### Scenario: A recusa do núcleo vira mensagem simples

- **WHEN** o núcleo recusa o registro porque o tipo de recurso não tem vigência que cubra a data
  do aporte
- **THEN** a aplicação apresenta o motivo em linguagem simples e a necessidade continua na lista

### Requirement: O Mestre acompanha a situação do ressarcimento do que absorveu

A App 09 SHALL apresentar ao Mestre as absorções **dele mesmo**, cada uma com o **tipo de
recurso**, a **quantidade**, o **ponto de apoio**, o **valor em moedas**, a **data** e a
**situação de ressarcimento** — em aberto, ressarcido ou não se aplica (`RF-09-59`).

A leitura SHALL ser **somente leitura**: a aplicação NEVER SHALL oferecer exigir, apressar,
reordenar ou cancelar ressarcimento, e NEVER SHALL apresentar absorção de outra persona.

A aplicação SHALL apresentar a situação **não se aplica** como o que ela é — absorção de
serviço, em que quem absorve dá tempo e não há desembolso a devolver — e NEVER SHALL apresentá-la
como pendência.

#### Scenario: O Mestre vê o que absorveu e a situação de cada aporte

- **WHEN** o Mestre abre o acompanhamento e absorveu recursos antes
- **THEN** a aplicação apresenta cada aporte com tipo, quantidade, ponto de apoio, moedas, data e
  a situação de ressarcimento

#### Scenario: A tela não oferece apressar o ressarcimento

- **WHEN** o Mestre abre um aporte com ressarcimento em aberto
- **THEN** nenhuma ação de exigir, apressar, reordenar ou cancelar é apresentada

#### Scenario: A absorção de outro Mestre não aparece

- **WHEN** há absorções em aberto de outro Mestre
- **THEN** elas não são apresentadas

#### Scenario: A absorção de serviço não aparece como pendência

- **WHEN** o Mestre absorveu um serviço
- **THEN** a aplicação apresenta a situação como não se aplica, e não como ressarcimento em
  aberto

### Requirement: A App 09 não coleta nem exibe dado bancário

A App 09 NEVER SHALL apresentar campo que colete **chave PIX, banco ou conta**, e NEVER SHALL
exibir dado bancário de ninguém: a plataforma não o guarda, e do trâmite ela retém apenas o
**comprovante da transferência**, anexado pelo Admin ao registrar o ressarcimento (`RF-09-60`).

Onde o Mestre acompanha o que absorveu, a aplicação SHALL declarar que o ressarcimento ocorre
havendo receita destinada a ele e que, nessa etapa, a **chave PIX é enviada por e-mail ao
Admin** — o único retorno por e-mail do Ciclo 01, e ato da pessoa, fora da plataforma. A
aplicação NEVER SHALL enviar e-mail, nem construir notificação por e-mail (`RN-09-23`).

#### Scenario: Nenhum campo pede dado bancário

- **WHEN** o Mestre percorre a área de recursos, do ato de absorção ao acompanhamento
- **THEN** nenhum campo de chave PIX, banco ou conta é apresentado

#### Scenario: A tela orienta o envio da chave por e-mail ao Admin

- **WHEN** o Mestre abre o acompanhamento do que absorveu
- **THEN** a aplicação declara que a plataforma não guarda dado bancário e que a chave PIX é
  enviada por e-mail ao Admin quando houver receita destinada

#### Scenario: A aplicação não envia e-mail

- **WHEN** um aporte do Mestre passa a ressarcido
- **THEN** a situação é lida dentro da aplicação, sem que nenhum e-mail seja enviado por ela
