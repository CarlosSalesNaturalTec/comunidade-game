## ADDED Requirements

### Requirement: A presença registrada por engano é anulada, sem apagar o registro

O núcleo SHALL oferecer ao **Admin** a **anulação** de uma presença já registrada — o caso do
reconhecimento que apontou a pessoa errada —, guardando **motivo**, **autor** e **momento da
anulação**. A anulação NEVER SHALL apagar o registro: a presença anulada permanece consultável
com o modo, o confirmador e o momento do fato originais, e é assim que o ajuste manual do
`RF-02-36` fica registrado, como manda a `RN-02-12`.

Anulação sem motivo SHALL ser recusada com **422**. Anulação de presença já anulada SHALL ser
recusada com **409**. Quem não é Admin SHALL receber **403** — o Mestre confirma presença, não
a desfaz. A presença anulada NEVER SHALL contar como presença: ela sai do painel do dia e não
alcança o lançamento da atividade realizada. (`RF-02-36`, `RF-01-20`, `RN-02-12`, `RN-02-21`,
documento 03 §5)

#### Scenario: O Admin anula a presença registrada por engano

- **WHEN** um Admin anula, com motivo, a presença de um Guerreiro(a) reconhecido por engano
- **THEN** o núcleo grava a anulação com motivo, autor e momento, e a presença permanece
  consultável com o modo e o momento do fato originais

#### Scenario: Anulação sem motivo é recusada

- **WHEN** chega uma anulação sem motivo, ou com motivo em branco
- **THEN** o núcleo responde 422 indicando o campo em falta e nada é gravado

#### Scenario: A mesma presença não se anula duas vezes

- **WHEN** chega a anulação de uma presença já anulada
- **THEN** o núcleo responde 409 e a anulação original permanece como está

#### Scenario: O Mestre não anula presença

- **WHEN** um Mestre em sessão tenta anular a presença de um Guerreiro(a)
- **THEN** o núcleo responde 403 e nada é gravado

#### Scenario: A presença anulada sai do painel do dia

- **WHEN** o painel do dia é lido depois de uma presença daquela aula ter sido anulada
- **THEN** o Guerreiro(a) não aparece entre quem chegou

## MODIFIED Requirements

### Requirement: A presença é única por aula e Guerreiro(a)

O núcleo SHALL manter **no máximo uma** presença **não anulada** por aula e Guerreiro(a). O
reenvio da mesma presença — o caso do App 01 que operou com a rede fora e sincroniza depois —
SHALL deixar o registro existente inalterado, sem duplicar e sem erro. Anulada a presença
daquele par, o núcleo SHALL aceitar o **registro correto** da presença do mesmo Guerreiro(a)
naquela aula, sem que a anulada seja tocada: é o que fecha o ajuste manual do `RF-02-36`.
(`RF-01-20`, `RF-02-36`, PRD-01 §10, documento 09, "App 01 com a rede fora")

#### Scenario: Reenvio da mesma presença não duplica

- **WHEN** a presença de um Guerreiro(a) já registrada naquela aula é enviada de novo
- **THEN** o núcleo mantém um único registro e não responde erro

#### Scenario: Sincronização depois da rede voltar preserva o primeiro registro

- **WHEN** uma presença confirmada na fila local chega depois de a mesma presença já ter sido
  gravada
- **THEN** o núcleo mantém o registro existente, com o confirmador e o momento originais

#### Scenario: Anulada a presença, a correta é registrada

- **WHEN** a presença de um Guerreiro(a) numa aula é anulada e, em seguida, a presença correta
  dele naquela mesma aula é registrada por confirmação
- **THEN** o núcleo grava a presença nova e a anulada permanece gravada, sem ser alterada
