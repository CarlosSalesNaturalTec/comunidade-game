## MODIFIED Requirements

### Requirement: A presença registrada por engano é anulada, sem apagar o registro

O núcleo SHALL oferecer ao **Admin** a **anulação** de uma presença já registrada — o caso do
reconhecimento que apontou a pessoa errada —, guardando **motivo**, **autor** e **momento da
anulação**. A anulação NEVER SHALL apagar o registro: a presença anulada permanece consultável
com o modo, o confirmador e o momento do fato originais, e é assim que o ajuste manual do
`RF-02-36` fica registrado, como manda a `RN-02-12`.

Anulação sem motivo SHALL ser recusada com **422**. Anulação de presença já anulada SHALL ser
recusada com **409**. Quem não é Admin SHALL receber **403** — o Mestre confirma presença, não
a desfaz. A presença anulada NEVER SHALL contar como presença: ela sai do painel do dia e não
alcança o lançamento da atividade realizada. A anulação SHALL estornar, na mesma operação, os
pontos extras que a presença creditou, como manda a capacidade `ponto-extra`; anulação NEVER
SHALL ser recusada por falta de saldo disponível. (`RF-02-36`, `RF-01-20`, `RF-01-83`,
`RN-02-12`, `RN-02-21`, `RN-01-64`, documento 03 §5)

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

#### Scenario: A anulação estorna os extras da presença

- **WHEN** um Admin anula, com motivo, uma presença que creditou 5 pontos extras
- **THEN** o núcleo grava a anulação e estorna os 5 extras do Guerreiro(a) na mesma operação;
  se o estorno falhar, a anulação também não é gravada
