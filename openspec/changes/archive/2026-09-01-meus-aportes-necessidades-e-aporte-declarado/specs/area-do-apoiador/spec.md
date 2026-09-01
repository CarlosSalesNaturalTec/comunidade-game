## ADDED Requirements

### Requirement: A tela de "Meus aportes" mostra o que já foi homologado e o Poder Sustentador

A aplicação SHALL apresentar ao Apoiador em sessão os aportes dele **já homologados**, cada um
com **data, tipo e destino**, e o **Poder Sustentador** como **total acumulado em moedas**,
como o núcleo os devolve — sem somar, reordenar por valor nem recalcular. Apoiador sem aporte
homologado SHALL ver a tela com o total em zero e a explicação de que ainda não há aporte
homologado. (`RF-14-21`, `RF-14-22`, PRD-14 §6.3)

#### Scenario: Os aportes homologados aparecem com o total

- **WHEN** o Apoiador abre "Meus aportes"
- **THEN** cada aporte aparece com data, tipo e destino, e o Poder Sustentador aparece como
  total acumulado em moedas

#### Scenario: Sem aporte homologado a tela explica o vazio

- **WHEN** o Apoiador ainda não teve aporte homologado
- **THEN** a tela mostra o total em zero e diz que ainda não há aporte homologado

### Requirement: Nenhuma tela do Apoiador exibe reais, salvo a da declaração

A aplicação SHALL exibir todo valor **em moedas** e NEVER SHALL exibir reais em tela alguma,
com uma única exceção: a tela em que se **declara a transferência**, onde o valor transferido é
em reais e SHALL aparecer com o **equivalente em moedas** ao lado. (`RF-14-23`, `RN-14-09`,
invariante 16 do documento 99 §6)

#### Scenario: As telas de leitura só falam em moedas

- **WHEN** o Apoiador percorre "Meus aportes", as necessidades em aberto e a situação das
  declarações
- **THEN** nenhum valor aparece em reais

#### Scenario: A tela da declaração mostra reais com o equivalente em moedas

- **WHEN** o Apoiador informa o valor transferido
- **THEN** a tela mostra o valor em reais e, ao lado, o equivalente em moedas

### Requirement: As necessidades em aberto aparecem com atividade, comunidade e o que falta

A aplicação SHALL listar as **necessidades de recurso em aberto** como o núcleo as publica, com
a **atividade** — o recurso que falta, a data e o horário da aula e o ponto de apoio —, a
**comunidade** e **o que falta em moedas**. A aplicação NEVER SHALL somar, reordenar por valor
nem recalcular a falta, e necessidade de tipo **sem valor de referência vigente** SHALL
continuar aparecendo, com a quantidade que falta e sem valor arbitrado. Não havendo necessidade
em aberto, a tela SHALL dizê-lo, sem lista vazia sem explicação. (`RF-14-24`, `RN-14-09`,
PRD-14 §§5.3, 6.3)

#### Scenario: A lista traz a atividade, a comunidade e o que falta

- **WHEN** o Apoiador abre as necessidades em aberto
- **THEN** cada necessidade aparece com o recurso, a data e o horário da aula, o ponto de
  apoio, a comunidade e o que falta em moedas

#### Scenario: Necessidade sem valor de referência continua na lista

- **WHEN** uma necessidade é de tipo sem valor de referência vigente
- **THEN** ela aparece com a quantidade que falta e sem valor em moedas

#### Scenario: Sem necessidade em aberto a tela diz

- **WHEN** não há necessidade de recurso em aberto
- **THEN** a tela diz que não há necessidade em aberto

### Requirement: O Apoiador declara o aporte por necessidade, por sugestão ou por valor livre

A aplicação SHALL oferecer ao Apoiador em sessão três caminhos para declarar um aporte novo: a
partir de uma **necessidade em aberto**, por um **valor sugerido** da escada do perfil que ele
declarar na própria tela, ou por **valor livre**. O degrau da escada SHALL ser sugestão e não
piso: o valor livre SHALL aceitar qualquer quantia, com fração de duas casas. A tela SHALL
exigir o **anexo do comprovante** da transferência para enviar e SHALL declarar os formatos
aceitos; recusado o comprovante pelo núcleo, SHALL apresentar a recusa com os formatos válidos.
(`RF-14-25`, `RF-14-26`, `RN-14-06`, PRD-14 §§5.3, 6.3, 12)

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

### Requirement: A tela declara que o aporte entra pendente e não credita nada

A aplicação SHALL declarar, **antes do envio**, que o aporte entra **pendente de homologação**,
que um Admin vai conferir o comprovante e que, até lá, ele não vira moeda, não compõe o Poder
Sustentador e não abate o que falta a necessidade alguma. Enviada a declaração, a aplicação
SHALL confirmar que ela entrou na fila da gestão e NEVER SHALL exibir a necessidade escolhida
como coberta antes da homologação. (`RF-14-26`, `RN-14-07`, PRD-14 §§5.3, 12)

#### Scenario: A declaração aparece antes do envio

- **WHEN** o Apoiador chega ao ponto de enviar a declaração
- **THEN** a tela diz que o aporte entra pendente, que um Admin confere o comprovante e que
  nada é creditado até lá

#### Scenario: Enviada a declaração, a necessidade não muda

- **WHEN** a declaração é enviada com sucesso
- **THEN** a aplicação confirma a entrada na fila da gestão e a necessidade escolhida continua
  com a mesma quantidade faltante

### Requirement: O Apoiador acompanha a situação de cada aporte declarado

A aplicação SHALL apresentar ao Apoiador a situação de cada aporte que ele declarou —
**pendente**, **homologado** ou **recusado** —, com o **valor declarado em moedas**, a data e a
origem da escolha, e, no recusado, o **motivo em linguagem simples**, dentro da plataforma.
Esta não é a tela em que se declara a transferência: aqui o valor aparece **em moedas**. A
aplicação NEVER SHALL oferecer edição, reenvio automático ou qualquer ato sobre a situação: a
mudança é da gestão. (`RF-14-27`, `RN-14-08`, PRD-14 §§3.2, 5.3)

#### Scenario: As três situações aparecem com o que cada uma tem

- **WHEN** o Apoiador abre a situação dos aportes declarados
- **THEN** cada um aparece com a situação, o valor declarado em moedas, a data e a origem da
  escolha, e o recusado traz o motivo em linguagem simples

#### Scenario: A tela não oferece ato sobre a situação

- **WHEN** o Apoiador vê um aporte pendente ou recusado
- **THEN** não há na tela botão de homologar, editar ou reenviar

### Requirement: Quem quer aportar material ou serviço é encaminhado à gestão

A aplicação NEVER SHALL aceitar declaração de aporte em **material, serviço ou divulgação** e
SHALL explicar, na própria tela de declaração, que essas formas entram pelo cadastro do Admin,
com termo de doação ou registro do material. Recusada a declaração pelo núcleo por essa razão,
a tela SHALL apresentar a orientação de procurar a gestão. (`RF-14-28`, `RN-14-05`, PRD-14
§§3.2, 12)

#### Scenario: A tela explica que só o dinheiro entra por aqui

- **WHEN** o Apoiador abre a tela de declaração
- **THEN** ela diz que o aporte pela aplicação é em dinheiro e que material, serviço e
  divulgação entram pelo cadastro do Admin

#### Scenario: A recusa do núcleo vira orientação na tela

- **WHEN** o núcleo recusa a declaração por ser de material ou serviço
- **THEN** a tela apresenta a orientação de procurar a gestão, e nada é enviado de novo
