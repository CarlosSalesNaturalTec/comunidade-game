## MODIFIED Requirements

### Requirement: O lançamento atribui o desfecho de cada participante num ato só

A área Lançamentos SHALL apresentar, para a atividade prevista da aula, a lista dos
participantes e SHALL exigir de cada um o **desfecho** entre os três valores fechados —
**realizada**, **realizada com mérito** e **mérito extra por auxílio aos colegas** —, além do
momento do fato e da produção. A tela NEVER SHALL oferecer campo de valor: o número vem da
tabela do documento 11 §5 (`RF-02-39`).

O lançamento SHALL ser enviado como **um único ato por aula**, com todos os participantes
juntos, e a tela SHALL informar que os resultados foram gravados, sem dizer que a aula foi
fechada nem que houve baixa: isso é do sistema, no fim do horário. Participante sem desfecho
SHALL impedir o envio, com a falta dita na tela. (`RF-02-33`, `RF-02-34`, `RF-02-35`,
`RF-02-39`, `RN-02-21`)

#### Scenario: O Admin lança os participantes com o desfecho de cada um

- **WHEN** o Admin atribui o desfecho de cada participante e envia o lançamento
- **THEN** a aplicação envia um único lançamento com todos eles e informa que os resultados foram
  gravados, sem falar em fechamento nem em baixa

#### Scenario: O mérito extra por auxílio é um dos três desfechos

- **WHEN** o Admin marca "mérito extra por auxílio aos colegas" para o Guerreiro(a) que ajudou
- **THEN** a aplicação envia esse desfecho, sem que a tela peça ou aceite o valor da pontuação

#### Scenario: Participante sem desfecho impede o envio

- **WHEN** o Admin tenta enviar o lançamento com um participante sem desfecho
- **THEN** a aplicação não envia e diz qual participante está sem desfecho

#### Scenario: O lançamento gravado não se edita

- **WHEN** o Admin envia de novo o resultado de um participante já lançado na mesma atividade
- **THEN** o núcleo recusa o Resultado repetido, a tela apresenta a recusa, e o lançamento
  gravado segue sem caminho de edição nem de remoção

## ADDED Requirements

### Requirement: A agenda rotula a aula realizada sem lastro

A agenda da App 03 SHALL apresentar a situação **realizada sem lastro** pelo rótulo
"Realizada sem lastro", como apresenta as demais. (`RN-02-09`, `RF-07-55`)

#### Scenario: A aula pendente que terminou aparece realizada sem lastro

- **WHEN** a agenda traz uma aula na situação realizada sem lastro
- **THEN** a linha dela diz "Realizada sem lastro"
