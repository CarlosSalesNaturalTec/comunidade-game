## Purpose

A missão do Apoiador é o chamado que a gestão publica a partir de uma necessidade de recurso
já publicada: o que se pede, quanto falta em moedas, o prazo e o selo que rende. Esta
capacidade cobre a publicação pelo Admin, a leitura pública das missões abertas, a cobertura
parcial e coletiva, o vencimento e a conclusão por homologação de aporte.

## Requirements

### Requirement: A missão do Apoiador nasce de uma necessidade de recurso publicada

O núcleo SHALL aceitar a publicação de uma `MissaoDoApoiador` apenas quando ela apontar uma
**necessidade de recurso publicada**; sem ela, SHALL responder **422** dizendo que falta a
necessidade de origem. A missão SHALL guardar o **nível de necessidade** que sustenta —
existir, acontecer, reconhecer ou permanecer —, o **título**, **o que se pede**, a
**quantidade** em moedas ou itens, o **prazo**, o **selo que rende**, a **situação** e o
**Admin que publicou**. A missão NEVER SHALL conceder ponto: o que ela rende é moeda e selo.
(`RF-14-71`, `RN-14-30`, `RN-14-31`, `RN-14-33`, `RF-02-102`, `RF-02-103`, `RN-02-31`)

#### Scenario: A missão publicada guarda a necessidade de origem

- **WHEN** um Admin publica a missão apontando uma necessidade de recurso em aberto, com nível,
  título, o que se pede, quantidade, prazo e selo
- **THEN** a missão é gravada na situação aberta, com o Admin que a publicou registrado

#### Scenario: Missão sem necessidade por trás é recusada

- **WHEN** a publicação chega sem necessidade de recurso publicada por trás
- **THEN** o núcleo responde 422 e nada é gravado

#### Scenario: A missão não credita ponto

- **WHEN** uma missão é publicada e concluída
- **THEN** nenhum ponto é lançado a quem a cobriu, em nenhuma etapa

### Requirement: Só o Admin publica e despublica a missão

O núcleo SHALL aceitar a publicação e a despublicação da missão apenas de um **Admin** em
sessão; de qualquer outra persona SHALL responder **403**. A despublicação SHALL tirar a missão
das listas e NEVER SHALL estornar aporte já homologado. Despublicar missão já **concluída**
SHALL ser recusado com **409**. (`RF-02-102`, `RF-02-105`, `RN-02-31`, `RN-14-32`)

#### Scenario: O Apoiador não publica missão

- **WHEN** um Apoiador em sessão tenta publicar uma missão
- **THEN** o núcleo responde 403 e nada é gravado

#### Scenario: A despublicação não estorna o que já foi homologado

- **WHEN** o Admin despublica uma missão que já recebeu um aporte homologado
- **THEN** a missão sai das listas, o aporte segue no livro-razão e as moedas seguem no Poder
  Sustentador de quem as deu

#### Scenario: Missão concluída não se despublica

- **WHEN** o Admin tenta despublicar uma missão já concluída
- **THEN** o núcleo responde 409 e a missão segue concluída

### Requirement: A leitura pública traz as missões abertas por nível de necessidade

O núcleo SHALL responder a leitura das missões **abertas** sem token de sessão, exigindo a
**chave de aplicação válida** como toda rota de dados sob `/v1`, agrupadas pelo **nível de
necessidade** que sustentam. Cada missão SHALL trazer o que se pede, **quanto falta em
moedas**, o prazo e o selo que rende, e o **quanto já foi coberto em quantidade**. A resposta
NEVER SHALL identificar quem cobriu — nem nick, nem avatar, nem valor individual. Missão
**concluída**, **vencida** ou **despublicada** NEVER SHALL aparecer nessa leitura, e a consulta
direta a ela SHALL responder **404**. (`RF-14-60`, `RF-14-61`, `RF-14-62`, `RF-14-71`,
`RF-14-72`, `RF-02-104`)

#### Scenario: As missões abertas vêm agrupadas por nível

- **WHEN** a leitura pública das missões é consultada com chave válida
- **THEN** a resposta traz as missões abertas agrupadas por existir, acontecer, reconhecer e
  permanecer, cada uma com o que se pede, o que falta em moedas, o prazo e o selo

#### Scenario: O coberto aparece sem quem cobriu

- **WHEN** duas pessoas já cobriram parte de uma missão aberta
- **THEN** a missão mostra a quantidade já coberta e nenhum nick, avatar ou valor individual

#### Scenario: Missão vencida sai da lista

- **WHEN** o prazo de uma missão aberta vence sem que o saldo feche
- **THEN** ela deixa de aparecer entre as abertas e a consulta direta a ela responde 404

### Requirement: O quanto falta é derivado dos aportes homologados

O **quanto falta** de uma missão SHALL ser derivado dos aportes **homologados** ligados à
necessidade de origem, nunca armazenado. Aporte **pendente** NEVER SHALL abater o que falta nem
alterar o coberto. (`RF-14-64`, `RN-14-32`, PRD-14 §8)

#### Scenario: O aporte pendente não move o que falta

- **WHEN** um Apoiador declara um aporte para uma missão e a declaração segue pendente
- **THEN** a missão continua mostrando o mesmo quanto falta de antes

#### Scenario: A homologação abate o que falta

- **WHEN** o Admin homologa um aporte parcial de uma missão
- **THEN** o quanto falta cai pelo valor em moedas do aporte homologado

### Requirement: A missão conclui só quando o saldo fecha, por homologação

A missão SHALL passar a **concluída** apenas quando a homologação de um aporte fizer o saldo
fechar; enquanto faltar, ela SHALL permanecer **aberta** com o restante atualizado. Declaração
pendente NEVER SHALL concluir missão. Aporte declarado para missão já **concluída** ou
**vencida** SHALL ser recusado com **409**, dizendo o que aconteceu com ela. (`RF-14-63`,
`RF-14-64`, `RF-14-65`, `RN-14-32`)

#### Scenario: A cobertura parcial mantém a missão aberta

- **WHEN** um aporte homologado cobre parte do que a missão pede
- **THEN** a missão segue aberta com o restante atualizado e ninguém recebe selo

#### Scenario: O aporte que fecha o saldo conclui a missão

- **WHEN** a homologação de um aporte faz o que falta chegar a zero
- **THEN** a missão passa a concluída

#### Scenario: Missão fechada não aceita novo aporte

- **WHEN** um Apoiador declara aporte para uma missão já concluída ou vencida
- **THEN** o núcleo responde 409 dizendo o que aconteceu com a missão

### Requirement: Na missão coletiva cada um recebe as moedas do que aportou

As moedas de cada participante SHALL ser as do **próprio** aporte homologado, e ninguém SHALL
receber crédito em moedas pelo que outro deu. A missão vencida sem fechar NEVER SHALL estornar
aporte já homologado: as moedas SHALL permanecer no Poder Sustentador de quem as deu.
(`RF-14-66`, `RF-14-72`, `RN-14-34`)

#### Scenario: Duas pessoas fecham a mesma missão

- **WHEN** dois apoiadores cobrem partes diferentes da mesma missão e ela conclui
- **THEN** cada um tem no Poder Sustentador apenas as moedas do próprio aporte, e nenhum vê o
  nome do outro

#### Scenario: A missão vencida não estorna nada

- **WHEN** uma missão coberta pela metade vence
- **THEN** nenhum aporte homologado é estornado e as moedas seguem com quem as deu
