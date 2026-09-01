## ADDED Requirements

### Requirement: O Apoiador define o próprio avatar, acima do piso de moedas

A rota de identidade do adulto SHALL aceitar o **avatar** do Apoiador em sessão ao lado do nick
— logomarca ou outra imagem escolhida —, e SHALL gravá-lo **apenas** quando o Apoiador tiver
**10 moedas ou mais acumuladas em aportes homologados**. Abaixo do piso o núcleo SHALL recusar a
gravação com **409** e **quanto falta** em moedas, e o avatar anterior SHALL permanecer como
estava. Alcançado o piso, o envio SHALL passar **sem ato algum da gestão**. O avatar SHALL ser
opaco ao núcleo, que NEVER SHALL validar a forma dele. Persona que não seja Apoiador SHALL
receber **403** ao enviar avatar por esta rota. (`RF-14-12`, `RF-14-14`, `RF-14-17`, `RN-14-10`,
`RN-14-11`, PRD-14 §§5.2, 9, PRD-01 §9)

#### Scenario: Apoiador acima do piso grava o avatar próprio

- **WHEN** um Apoiador com 10 moedas acumuladas em aportes homologados envia o avatar próprio
- **THEN** o núcleo o grava na persona dele, sem intervenção da gestão

#### Scenario: Apoiador abaixo do piso é recusado com quanto falta

- **WHEN** um Apoiador com 5 moedas acumuladas envia o avatar próprio
- **THEN** o núcleo responde 409 dizendo quantas moedas faltam, e nenhum avatar é gravado

#### Scenario: O Apoiador troca o avatar depois de já o ter

- **WHEN** um Apoiador acima do piso envia um avatar novo no lugar do que já tinha
- **THEN** o núcleo grava o novo e o anterior deixa de valer

#### Scenario: Persona de outro papel não envia avatar por esta rota

- **WHEN** uma persona que não é Apoiador envia avatar pela rota de identidade do Apoiador
- **THEN** o núcleo responde 403 e nada é gravado

### Requirement: O acumulado que libera o avatar não regride

O piso do avatar próprio SHALL ser medido pela **soma, em moedas, dos aportes homologados** do
Apoiador, e NEVER SHALL ser medido pelo Poder Sustentador, que o ressarcimento pago derruba. O
direito alcançado SHALL permanecer alcançado: aporte ressarcido, ajuste no livro-razão ou queda
do Poder Sustentador NEVER SHALL retirar do Apoiador o avatar próprio já gravado nem fechar o
envio de outro. (`RF-14-14`, `RN-14-11`, documento 11 §8.2, PRD-07 §9)

#### Scenario: O ressarcimento não fecha o avatar próprio

- **WHEN** um Apoiador que cruzou as 10 moedas tem um aporte ressarcido, e o Poder Sustentador
  dele cai abaixo de 10 moedas
- **THEN** o avatar próprio dele continua gravado e o envio de outro continua aberto

#### Scenario: O piso conta o aporte homologado, não o pendente

- **WHEN** um Apoiador com 5 moedas homologadas tem outro aporte declarado ainda pendente, de
  valor que cruzaria o piso
- **THEN** o núcleo continua recusando o avatar próprio, contando apenas o que foi homologado

### Requirement: O Apoiador lê a própria identidade e o que falta para o avatar próprio

O núcleo SHALL responder à persona de **Apoiador em sessão** uma leitura da própria identidade
com o **nick**, o **avatar** que estiver gravado, o **total de moedas acumuladas** e, abaixo do
piso, **quantas moedas faltam** para liberar o avatar próprio. A leitura SHALL alcançar
**apenas a própria persona**, e persona de outro papel SHALL receber **403**. A resposta NEVER
SHALL trazer valor em reais. (`RF-14-15`, `RF-14-16`, `RN-14-09`, `RN-14-11`, PRD-14 §§5.2, 6.2)

#### Scenario: Abaixo do piso a leitura diz quanto falta

- **WHEN** um Apoiador com 5 moedas acumuladas lê a própria identidade
- **THEN** a resposta traz o nick, o total em moedas e as 5 moedas que faltam para o avatar
  próprio

#### Scenario: Acima do piso a leitura diz que o avatar próprio está liberado

- **WHEN** um Apoiador com 12 moedas acumuladas lê a própria identidade
- **THEN** a resposta traz o avatar próprio como liberado e nada a faltar

#### Scenario: A leitura não traz reais

- **WHEN** um Apoiador cujos aportes têm valor de origem em reais lê a própria identidade
- **THEN** a resposta traz apenas moedas, sem campo algum com o valor em reais
