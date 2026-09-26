# Spec Delta

## ADDED Requirements

### Requirement: O desfecho da presença apresenta a carta sem repetir a frase nem anunciar espera

A App 01 SHALL apresentar, no desfecho da presença, a **carta do Guerreiro(a)** que acabou de
registrá-la, montada como a da Área do Guerreiro(a) e sem depender de ele ter aberto **série
de coleta**: o encontro é onde a criança chega primeiro, e a carta é o que ela vem ver.
(`RF-04-67`, `RF-05-50`, `RF-05-51`)

A tela NEVER SHALL repetir, em dois lugares ao mesmo tempo, que a presença foi registrada: a
confirmação SHALL ser dita **uma vez**. (`RF-04-67`)

Não sendo possível apresentar a carta, a tela SHALL dizê-lo em um tom que declare **falta**, e
NEVER SHALL usar o tom de **coisa em curso** para o que já terminou — anunciar espera onde não
há nada a esperar faz a criança ficar olhando uma tela que não vai mudar. (`RF-04-67`,
documento 15 §5)

#### Scenario: A carta aparece a quem acabou de registrar presença

- **WHEN** a presença é registrada pelo caminho da presença
- **THEN** o desfecho apresenta a carta do Guerreiro(a), ainda que ele nunca tenha aberto
  série de coleta

#### Scenario: A confirmação é dita uma vez só

- **WHEN** o desfecho da presença é apresentado
- **THEN** a frase que confirma o registro da presença aparece uma única vez na tela

#### Scenario: Sem carta, a tela declara falta e não espera

- **WHEN** a carta não pode ser apresentada por faltar o que a variante exige
- **THEN** a tela diz o que falta em tom de falta, e nada na tela anuncia que algo está em
  curso
