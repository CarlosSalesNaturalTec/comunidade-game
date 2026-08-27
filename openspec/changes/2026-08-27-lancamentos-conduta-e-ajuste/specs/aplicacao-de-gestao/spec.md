## ADDED Requirements

### Requirement: A App 03 abre a área Lançamentos sobre a aula vigente

A App 03 SHALL apresentar a área **Lançamentos**, que opera sobre a **aula vigente** — a mesma
que o painel do dia mostra — e reúne os três atos que fecham o encontro antes de ele acabar:
lançar a atividade realizada, conferir e ajustar as presenças e registrar a infração ocorrida
na aula (`RF-02-46`, `RF-02-47`, PRD-02 §5.6).

A pendência `lancamento_da_atividade_realizada`, listada no painel do dia, SHALL levar o
operador a esta área — é aqui que a escrita acontece, e o painel permanece em leitura.

Fora da janela de toda aula agendada, a área SHALL dizer em uma frase que não há encontro em
andamento, sem apresentar tela vazia nem erro cru. (`RF-02-34`, `RF-02-36`, `RF-02-37`,
`RF-02-39`, PRD-02 §§5.6, 6.3, 12)

#### Scenario: A área abre sobre a aula vigente

- **WHEN** um Admin abre a área Lançamentos durante a janela de uma aula
- **THEN** a tela apresenta os participantes, as presenças e a atividade prevista daquela aula

#### Scenario: Sem encontro, a área explica em uma frase

- **WHEN** a área Lançamentos é aberta fora da janela de toda aula agendada
- **THEN** a tela diz que não há encontro em andamento, sem erro cru

#### Scenario: A pendência do painel leva à área

- **WHEN** o Admin escolhe a pendência de lançamento da atividade realizada no painel do dia
- **THEN** a aplicação o leva à área Lançamentos daquela aula

### Requirement: O lançamento atribui o desfecho de cada participante num ato só

A área Lançamentos SHALL apresentar, para a atividade prevista da aula, a lista dos
participantes e SHALL exigir de cada um o **desfecho** entre os três valores fechados —
**realizada**, **realizada com mérito** e **mérito extra por auxílio aos colegas** —, além do
momento do fato e da produção. É o terceiro valor que credita o ponto extra a quem ajudou o
colega, e a tela NEVER SHALL oferecer campo de valor: o número vem da tabela do documento 11
§5 (`RF-02-39`).

O lançamento SHALL ser enviado como **um único ato por aula**, com todos os participantes
juntos, e a tela SHALL informar que ele converteu as reservas em baixa e passou a aula a
realizada. Participante sem desfecho SHALL impedir o envio, com a falta dita na tela.
(`RF-02-34`, `RF-02-39`, `RN-02-21`, PRD-02 §§6.3, 12)

#### Scenario: O Admin lança os participantes com o desfecho de cada um

- **WHEN** o Admin atribui o desfecho de cada participante e envia o lançamento
- **THEN** a aplicação envia um único lançamento com todos eles e informa que a aula passou a
  realizada e que as reservas viraram baixa

#### Scenario: O mérito extra por auxílio é um dos três desfechos

- **WHEN** o Admin marca "mérito extra por auxílio aos colegas" para o Guerreiro(a) que ajudou
- **THEN** a aplicação envia esse desfecho, sem que a tela peça ou aceite o valor da pontuação

#### Scenario: Participante sem desfecho impede o envio

- **WHEN** o Admin tenta enviar o lançamento com um participante sem desfecho
- **THEN** a aplicação não envia e diz qual participante está sem desfecho

#### Scenario: O lançamento gravado não se edita

- **WHEN** o Admin volta à área depois de a aula ter sido lançada
- **THEN** a tela apresenta o lançamento em leitura e não oferece caminho de edição nem de
  remoção

### Requirement: A área confere as presenças e registra o ajuste

A área Lançamentos SHALL apresentar as presenças daquela aula vindas do App 01, cada uma com o
**modo de comprovação** e, quando houver, quem confirmou. A tela SHALL oferecer dois ajustes:
**registrar por confirmação** a presença que faltou, gravando quem confirmou, e **anular** a
presença registrada por engano, exigindo o **motivo**. Anulada uma presença, a tela SHALL
permitir registrar em seguida a presença correta do mesmo Guerreiro(a) naquela aula.

A presença anulada SHALL permanecer visível, marcada como anulada e com o motivo — a correção
nunca apaga o registro (`RN-02-12`). A tela SHALL apresentar a recusa do núcleo em uma frase, e
NEVER SHALL exibir imagem real do Guerreiro(a): a representação é o avatar e o nick
(`RN-02-22`). (`RF-02-36`, `RN-02-12`, `RN-02-21`, `RN-02-22`, PRD-02 §§6.3, 12)

#### Scenario: O Admin registra a presença que faltou

- **WHEN** o Admin confirma a presença de um Guerreiro(a) que chegou e não foi reconhecido
- **THEN** a aplicação grava a presença por confirmação, com ele como confirmador, e a lista
  passa a mostrá-la

#### Scenario: O Admin anula a presença registrada por engano

- **WHEN** o Admin anula, com motivo, uma presença registrada por engano
- **THEN** a aplicação grava a anulação e a lista mostra a presença marcada como anulada, com
  o motivo

#### Scenario: Anulação sem motivo não é enviada

- **WHEN** o Admin tenta anular uma presença sem escrever o motivo
- **THEN** a aplicação não envia e diz que o motivo é obrigatório

#### Scenario: A lista de presenças mostra avatar e nick

- **WHEN** a área apresenta as presenças do encontro
- **THEN** cada Guerreiro(a) aparece por nick e avatar, e nenhuma imagem real é exibida

### Requirement: A área registra a infração ocorrida na aula, sem revisão de terceiro

A área Lançamentos SHALL oferecer o registro da **infração** ocorrida na aula, vinculada ao
**encontro**, à **atividade** e ao **Guerreiro(a)**, com o **motivo** em texto livre. O
registro SHALL valer **no ato**, sem fila de revisão e sem intervenção de outro adulto
(`RN-02-13`). A tela NEVER SHALL oferecer campo de valor da pontuação negativa: o número vem da
tabela do documento 11 §5.

A tela SHALL declarar, junto ao campo do motivo, que **descuido acidental com material comum
não é infração e não gera pontuação negativa** (`RN-02-14`). Infração sem motivo SHALL impedir
o envio, e a recusa do núcleo — entre elas o teto da aula já alcançado e a atividade que não é
daquela aula — SHALL ser apresentada em uma frase. (`RF-02-37`, `RN-02-13`, `RN-02-14`,
`RN-02-21`, PRD-02 §§6.3, 12)

#### Scenario: O registro vale no ato

- **WHEN** o operador registra a infração de um Guerreiro(a) declarando a atividade e o motivo
- **THEN** a aplicação a grava e informa que ela valeu no ato, sem fila de revisão

#### Scenario: A tela não pede o valor

- **WHEN** o operador preenche o registro da infração
- **THEN** a tela não apresenta campo de valor da pontuação negativa

#### Scenario: A tela avisa que descuido acidental não é infração

- **WHEN** o operador abre o registro da infração
- **THEN** a tela declara que descuido acidental com material comum não é infração e não gera
  pontuação negativa

#### Scenario: Infração sem motivo não é enviada

- **WHEN** o operador tenta registrar a infração sem escrever o motivo
- **THEN** a aplicação não envia e diz que o motivo é obrigatório

#### Scenario: O teto da aula é dito em uma frase

- **WHEN** o núcleo recusa a infração porque o teto daquele Guerreiro(a) na aula foi alcançado
- **THEN** a tela apresenta a recusa em uma frase, sem erro cru

### Requirement: A área Pontos de Apoio apresenta o extrato e corrige por ajuste

A área **Pontos de Apoio** SHALL apresentar, para o ponto de apoio escolhido, o **extrato do
livro-razão** — natureza, tipo de recurso, quantidade, moedas e data de cada lançamento, com
filtro por período e por tipo de recurso. Sobre cada lançamento a tela SHALL oferecer o
**ajuste**, com quantidade, moedas e **motivo**.

A tela NEVER SHALL oferecer caminho de edição nem de remoção de lançamento: a correção é
sempre um lançamento novo, que referencia o original e o deixa intacto (`RN-02-12`). Gravado o
ajuste, o extrato SHALL apresentá-lo referenciando o lançamento corrigido, com o motivo e o
autor. Ajuste sem motivo SHALL impedir o envio. (`RF-02-40`, `RN-02-12`, `RN-02-21`, PRD-02
§§6.3, 12)

#### Scenario: O extrato apresenta os lançamentos do ponto de apoio

- **WHEN** o Admin abre o extrato de um ponto de apoio
- **THEN** a tela lista os lançamentos daquele ponto de apoio, com natureza, tipo de recurso,
  quantidade, moedas e data

#### Scenario: A correção se faz por ajuste

- **WHEN** o Admin lança um ajuste sobre um lançamento errado, com motivo
- **THEN** a aplicação grava o ajuste, o extrato o apresenta referenciando o original, e o
  lançamento original permanece como estava

#### Scenario: A tela não oferece edição de lançamento

- **WHEN** o Admin procura corrigir um lançamento no extrato
- **THEN** a tela só oferece o ajuste, e nenhum caminho de edição ou de remoção

#### Scenario: Ajuste sem motivo não é enviado

- **WHEN** o Admin tenta lançar um ajuste sem escrever o motivo
- **THEN** a aplicação não envia e diz que o motivo é obrigatório

## MODIFIED Requirements

### Requirement: O Mestre alcança a condução da partida e nada mais da gestão

A aplicação SHALL permitir ao Mestre autenticado ler o painel, conduzir a partida de quiz da
aula dele e **registrar a infração ocorrida na aula, sobre atividade de trilha que ele autora**
— e SHALL apresentar a recusa do núcleo em qualquer outra escrita de gestão. Mestre que tenta
conduzir a partida de uma aula que não é dele, ou registrar infração sobre atividade de trilha
que não é dele, SHALL receber a recusa, dita em uma frase, sem que a tela ofereça caminho
alternativo.

O Mestre NEVER SHALL alcançar o lançamento da atividade realizada por aula, que é do Admin, nem
o ajuste das presenças. (`RF-02-49`, `RN-02-20`, `RF-02-37`, `RN-02-13`, PRD-02 §§4, 12)

#### Scenario: Mestre conduz a partida da sua aula

- **WHEN** o Mestre autenticado abre a condução da partida da aula dele
- **THEN** a aplicação oferece os quatro atos da condução

#### Scenario: Mestre de outra aula é recusado

- **WHEN** o Mestre tenta conduzir a partida de uma aula que não é dele
- **THEN** a aplicação apresenta a recusa em uma frase e não oferece caminho alternativo

#### Scenario: Mestre registra a infração da atividade que autora

- **WHEN** o Mestre autor da trilha registra a infração ocorrida na aula sobre uma atividade
  dela
- **THEN** a aplicação a grava e informa que ela valeu no ato

#### Scenario: Mestre que não é o autor é recusado

- **WHEN** o Mestre tenta registrar infração sobre atividade de trilha que não é dele
- **THEN** a aplicação apresenta a recusa em uma frase e não oferece caminho alternativo

#### Scenario: O Mestre não alcança o lançamento nem o ajuste de presença

- **WHEN** o Mestre abre a área Lançamentos
- **THEN** a tela lhe oferece apenas o registro da infração, e nem o lançamento da atividade
  realizada nem o ajuste das presenças
