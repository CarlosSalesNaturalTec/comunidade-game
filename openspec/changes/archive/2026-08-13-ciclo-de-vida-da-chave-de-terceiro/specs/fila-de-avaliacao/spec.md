## MODIFIED Requirements

### Requirement: Solicitação de chave entra na fila sem emitir chave

O núcleo SHALL registrar a solicitação de chave com o **solicitante**, o **contato**, a
**instituição opcional** e **o que pretende construir**, e SHALL NOT emitir chave, criar
cadastro ou criar persona no envio. Esta superfície SHALL NOT ter freio por origem, porque
nova solicitação é sempre possível, e SHALL permanecer protegida apenas pela cota da chave da
aplicação que a chama. Aprovada a solicitação, ela SHALL guardar a **chave emitida** a partir
dela, e a aprovação SHALL ser a condição da emissão: nenhuma chave de terceiro nasce sem
solicitação aprovada. (`RF-01-49`, `RF-01-50`, `RN-01-37`, `RN-01-46`, `RN-01-51`, 03 §8)

#### Scenario: Envio devolve registro, nunca chave

- **WHEN** um visitante envia a solicitação de chave
- **THEN** o núcleo grava o registro e devolve o protocolo e o prazo, sem emitir chave nenhuma

#### Scenario: Solicitação de chave repetida da mesma origem não é freada

- **WHEN** a mesma origem envia a solicitação de chave repetidas vezes
- **THEN** o núcleo processa os envios sem atraso progressivo, porque a superfície não tem
  freio por origem

#### Scenario: Aprovação por si não emite a chave

- **WHEN** um Admin conclui a avaliação de uma solicitação de chave como aprovada
- **THEN** o núcleo grava o desfecho e não emite chave alguma: a emissão é ato seguinte e
  próprio do Admin

#### Scenario: A solicitação guarda a chave que rendeu

- **WHEN** a chave de uma solicitação aprovada é emitida
- **THEN** a solicitação passa a apontar a chave emitida, e as duas ficam consultáveis juntas

#### Scenario: Recusa não rende chave em tempo algum

- **WHEN** um Admin conclui a avaliação de uma solicitação de chave como recusada
- **THEN** nenhuma emissão é possível sobre ela, agora ou depois
