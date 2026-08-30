## ADDED Requirements

### Requirement: O Mestre cadastra o tópico e recebe a estrutura sugerida da missão

A App 09 SHALL oferecer, na missão de que o Mestre é autor, um campo de **texto corrente** para
ele cadastrar o **tópico que quer ensinar**, e SHALL apresentar a **estrutura sugerida** que o
núcleo devolve: as atividades propostas, com modalidade e formato, a produção que cada uma pede,
o desafio de desbloqueio, a retomada sugerida e a etiqueta ODS proposta.

O campo NEVER SHALL pedir formato, marcação, palavra-chave nem qualquer instrução técnica: o
Mestre escreve como falaria. Não vindo a sugestão do núcleo, a aplicação SHALL dizer em
linguagem simples que ela não veio e SHALL manter aberto todo o caminho de escrever a missão à
mão. (`RF-09-85`, `RF-09-91`, `RF-09-95`, `RF-09-116`, `RN-09-16`, PRD-09 §10)

#### Scenario: O Mestre escreve o tópico como falaria

- **WHEN** o Mestre autor abre o template de uma missão dele
- **THEN** encontra um campo de texto corrente para o tópico, sem pedido de formato, marcação ou
  palavra-chave

#### Scenario: A estrutura sugerida é apresentada

- **WHEN** o Mestre autor envia o tópico
- **THEN** a aplicação apresenta as atividades propostas, a retomada sugerida e a etiqueta ODS
  proposta

#### Scenario: Sugestão que não veio não trava a autoria

- **WHEN** o núcleo não consegue devolver a sugestão
- **THEN** a aplicação diz em linguagem simples que ela não veio, sem código de erro, e o Mestre
  segue escrevendo a missão à mão

### Requirement: A App 09 mostra as lacunas e não grava nada sem o Mestre confirmar

A App 09 SHALL apresentar as **lacunas** da missão em linguagem simples — sem atividade,
atividade sem produção do Guerreiro(a), retomada não declarada e, em trilha de poder técnico,
missão sem atividade desplugada — e SHALL permitir ao Mestre **aceitar, recusar ou alterar** cada
sugestão, uma a uma.

Nenhuma sugestão SHALL ser gravada na trilha sem o Mestre confirmar, e a aplicação NEVER SHALL
apresentar como já gravado o que ainda é proposta. O que ele aceita ou altera SHALL ser gravado
pelas mesmas telas e rotas de autoria que já existem, com as mesmas recusas. A App 09 NEVER
SHALL escrever o **conteúdo** da missão a partir da sugestão: o conteúdo é escrito pelo Mestre,
autor creditado. (`RF-09-86`, `RF-09-87`, `RF-09-89`, `RN-09-33`, PRD-09 §12)

#### Scenario: As lacunas aparecem em linguagem simples

- **WHEN** a missão está sem atividade e sem retomada declarada
- **THEN** a aplicação diz que falta ao menos uma atividade e que a retomada não foi declarada,
  sem jargão e sem código de erro

#### Scenario: A sugestão fica distinta do que já está gravado

- **WHEN** a aplicação apresenta a estrutura sugerida
- **THEN** cada item vem marcado como proposta, distinto do que já está gravado na missão

#### Scenario: O Mestre aceita uma sugestão por vez

- **WHEN** o Mestre autor aceita uma das atividades sugeridas
- **THEN** só ela é gravada, pelo mesmo caminho de criação de atividade, e as demais seguem como
  proposta

#### Scenario: O Mestre altera antes de gravar

- **WHEN** o Mestre autor altera o texto de uma sugestão e a aceita
- **THEN** o que a aplicação grava é o texto dele

#### Scenario: A recusa não muda a missão

- **WHEN** o Mestre autor recusa a estrutura sugerida
- **THEN** nada é gravado e a missão permanece exatamente como estava

#### Scenario: O template não escreve o conteúdo

- **WHEN** o Mestre autor aceita tudo o que foi sugerido
- **THEN** o conteúdo da missão continua vazio até que ele o escreva

### Requirement: O Mestre declara a recompensa que o desbloqueio da missão libera

A App 09 SHALL permitir ao **Mestre autor** declarar, junto da missão, que o **desbloqueio** dela
libera **recompensa**, escolhendo o tipo de recurso e a **quantidade**, e SHALL apresentar a
recompensa declarada junto da missão na trilha.

A tela NEVER SHALL oferecer preço, saldo de pontos ou qualquer contrapartida do Guerreiro(a): a
recompensa de marco é conquistada, nunca comprada nem trocada. A aplicação NEVER SHALL exigir
lastro na declaração nem avisar que ele falta: a conferência acontece na entrega.
(`RF-09-84`, `RF-09-71`, `RF-09-72`, `RN-09-26`, `RN-09-27`, `RN-09-39`, invariante 23)

#### Scenario: O Mestre autor declara a recompensa do desbloqueio

- **WHEN** o Mestre autor declara que o desbloqueio de uma missão dele libera 30 unidades de um
  tipo de recurso
- **THEN** a aplicação grava a declaração e a apresenta junto da missão

#### Scenario: A tela não oferece preço nem troca

- **WHEN** o Mestre autor abre a declaração de recompensa
- **THEN** nenhum campo pede preço, pontos ou contrapartida do Guerreiro(a)

#### Scenario: A declaração não exige lastro

- **WHEN** o Mestre autor declara recompensa de um tipo sem saldo em ponto de apoio algum
- **THEN** a aplicação grava a declaração normalmente, sem aviso de falta de lastro

### Requirement: A App 09 apresenta ao Mestre as entregas de recompensa pendentes

A App 09 SHALL apresentar ao Mestre, em **Minhas turmas**, a fila das **entregas pendentes**: os
Guerreiros e Guerreiras da comunidade dele que alcançaram marco com recompensa declarada e ainda
não a receberam, com a trilha, o marco, o tipo de recurso e a quantidade. Confirmada a entrega
pelo Mestre, a pendência SHALL sair da fila.

Cada Guerreiro(a) SHALL aparecer por **nick e avatar**, e nenhuma imagem real SHALL ser exibida.
A fila NEVER SHALL exibir valor em moedas nem em reais. Recusada a entrega pelo núcleo, a
aplicação SHALL dizer em linguagem simples qual foi o motivo — falta de lastro, quantidade
esgotada ou marco não alcançado —, sem código de erro. (`RF-09-75`, `RF-09-76`, `RN-09-18`,
invariantes 12 e 16, PRD-09 §12)

#### Scenario: A fila mostra quem conquistou e ainda não recebeu

- **WHEN** um Guerreiro(a) da comunidade do Mestre desbloqueia missão com recompensa declarada
- **THEN** a aplicação passa a apresentá-lo na fila de entregas pendentes, com a trilha, o marco,
  o tipo de recurso e a quantidade

#### Scenario: A entrega confirmada sai da fila

- **WHEN** o Mestre confirma a entrega pela aplicação
- **THEN** a pendência deixa de aparecer na fila

#### Scenario: A recusa da entrega é traduzida

- **WHEN** o núcleo recusa a entrega por falta de lastro no ponto de apoio
- **THEN** a aplicação diz em linguagem simples que falta o recurso naquele ponto de apoio, sem
  código de erro

#### Scenario: A fila não exibe imagem real nem custo

- **WHEN** a aplicação apresenta a fila de entregas pendentes
- **THEN** cada Guerreiro(a) aparece por nick e avatar, e nenhum campo traz valor em moedas ou
  em reais

### Requirement: O Mestre duplica uma trilha pela lista de trilhas

A App 09 SHALL permitir ao Mestre **duplicar** uma trilha a partir da lista de trilhas, criando
uma trilha nova **em rascunho** sob a autoria dele, e SHALL levá-lo à trilha nova logo em
seguida, para que ele a edite.

A aplicação SHALL deixar claro, antes de duplicar, que a cópia nasce em **rascunho**, que ela
traz as missões e as atividades da origem e que **não** traz o percurso de Guerreiro(a) algum. A
trilha de origem NEVER SHALL ser apresentada como alterada pela duplicação. (`RF-09-13`,
`RF-09-04`, `RN-09-05`)

#### Scenario: O Mestre duplica e cai na trilha nova

- **WHEN** o Mestre pede a duplicação de uma trilha publicada
- **THEN** a aplicação cria a cópia em rascunho sob a autoria dele e o leva à trilha nova

#### Scenario: A aplicação diz o que a cópia traz e o que não traz

- **WHEN** o Mestre pede a duplicação
- **THEN** a aplicação avisa, antes de duplicar, que a cópia nasce em rascunho, traz missões e
  atividades e não traz percurso de Guerreiro(a) algum

#### Scenario: A trilha de origem segue como estava

- **WHEN** a duplicação termina
- **THEN** a trilha de origem continua na lista com a mesma situação e o mesmo autor

## MODIFIED Requirements

### Requirement: O Mestre declara a cadência de retomada da missão

A App 09 SHALL permitir ao Mestre autor declarar a **cadência de retomada** de uma missão e
SHALL permitir deixá-la **sem retomada**. A cadência declarada é sempre a do Mestre: a de 2, 7 e
21 dias que o _template_ de missão propõe é **sugestão**, apresentada já preenchida no campo e
alterável à vontade, e NEVER SHALL ser gravada sem ele confirmar. (`RF-09-83`, `RF-09-116`,
`RF-09-101`)

#### Scenario: Mestre declara a cadência

- **WHEN** o Mestre autor declara a cadência de retomada de uma missão dele
- **THEN** a aplicação a grava na missão e a apresenta junto dela

#### Scenario: Missão sem retomada é aceita

- **WHEN** o Mestre autor deixa a missão sem cadência de retomada
- **THEN** a aplicação a aceita, e a missão fica sem retomada declarada

#### Scenario: A sugestão do template vem preenchida e alterável

- **WHEN** o Mestre autor recebe a estrutura sugerida de uma missão
- **THEN** a cadência de 2, 7 e 21 dias aparece preenchida como proposta, e ele a altera ou a
  descarta antes de qualquer gravação
