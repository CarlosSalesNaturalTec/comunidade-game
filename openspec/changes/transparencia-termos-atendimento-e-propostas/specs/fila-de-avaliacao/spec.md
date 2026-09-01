## MODIFIED Requirements

### Requirement: O Admin avalia a sugestão e o retorno chega a quem propôs

O núcleo SHALL aceitar de um **Admin** em sessão o desfecho da sugestão, **adotada** ou **não
adotada**, gravando o **parecer**, o **autor** e a **data**. A sugestão **não adotada** SHALL
exigir o **motivo do retorno** em linguagem simples, sem o qual o núcleo SHALL recusar com
**422**, e SHALL marcar a data de descarte da transcrição, 90 dias à frente. A sugestão
**adotada** SHALL creditar **20 pontos extras** e o **badge de protagonismo** a quem propôs, na
mesma operação, e SHALL guardar transcrição e autoria de forma permanente. (`RF-02-26`,
`RF-01-25`, `RF-01-56`, `RN-01-50`)

O crédito SHALL alcançar **apenas autor com papel de Guerreiro(a)**: a pontuação é da criança, e
proposta de **responsável**, de Mestre ou de Apoiador NEVER SHALL creditar ponto extra nem
badge. O desfecho dessas propostas SHALL ser gravado do mesmo jeito, com parecer, autor, data e
o motivo do retorno quando não adotada — o que muda é só o crédito. (`RN-13-18`, PRD-13 §§5.7,
7)

O crédito SHALL ser **idempotente**: regravar o desfecho adotada NEVER SHALL creditar de novo.

O retorno a quem propôs SHALL acontecer **dentro da plataforma**, e o núcleo NEVER SHALL
enviar e-mail por causa dele. (`RN-02-25`, `RN-13-15`)

A sugestão já avaliada NEVER SHALL ser reavaliada: novo desfecho SHALL ser recusado com
**409**. Quem não for Admin SHALL receber **403**, e toda escrita SHALL entrar na trilha de
auditoria. (`RN-02-01`, `RN-02-21`)

#### Scenario: Sugestão adotada credita os extras e o badge

- **WHEN** um Admin conclui como adotada uma sugestão de Guerreiro(a)
- **THEN** o núcleo grava o desfecho e credita 20 pontos extras e o badge de protagonismo a
  quem propôs, na mesma operação

#### Scenario: Proposta de responsável adotada não pontua

- **WHEN** um Admin conclui como adotada a proposta de um responsável
- **THEN** o núcleo grava o desfecho, e nenhum ponto extra e nenhum badge são creditados

#### Scenario: Proposta de Mestre ou de Apoiador adotada não pontua

- **WHEN** um Admin conclui como adotada a proposta de um Mestre ou de um Apoiador
- **THEN** o núcleo grava o desfecho, e nenhum ponto extra e nenhum badge são creditados

#### Scenario: O crédito da sugestão adotada não se repete

- **WHEN** o desfecho adotada é gravado sobre uma sugestão que já foi creditada
- **THEN** nenhum ponto extra e nenhum badge são creditados de novo

#### Scenario: Sugestão não adotada exige o motivo do retorno

- **WHEN** um Admin conclui uma sugestão como não adotada sem informar o motivo do retorno
- **THEN** o núcleo responde 422 e nada é gravado

#### Scenario: Sugestão não adotada marca o descarte da transcrição

- **WHEN** um Admin conclui uma sugestão como não adotada com o motivo do retorno
- **THEN** o núcleo grava o motivo e a data de descarte da transcrição, 90 dias à frente

#### Scenario: Sugestão avaliada não se reavalia

- **WHEN** um Admin envia novo desfecho para uma sugestão já avaliada
- **THEN** o núcleo responde 409 e o desfecho original permanece
