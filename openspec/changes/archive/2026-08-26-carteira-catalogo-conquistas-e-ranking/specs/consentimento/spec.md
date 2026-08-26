## ADDED Requirements

### Requirement: O Guerreiro(a) lê o estado da própria autorização de divulgação

O núcleo SHALL declarar, na leitura da persona em sessão, se a **autorização de divulgação** do
Guerreiro(a) está **vigente**, derivada pela mesma resolução do histórico que já vale para toda
a plataforma — sem estado à parte e sem consulta nova. É o que permite à App 05 dizer à criança
qual é o estado do perfil público dela. (`RF-05-50`, `RN-05-14`, `RN-05-21`)

A leitura SHALL devolver **apenas se está ou não vigente**. NEVER SHALL dizer **qual**
responsável decidiu, **quando** decidiu ou **por quê**: a criança lê o estado do próprio perfil,
nunca o ato do adulto sobre ela. Autorizar continua sendo ato do responsável, na App 07, e esta
leitura NEVER SHALL oferecer caminho de conceder, recusar ou revogar. (`RN-05-21`, documento 03
§12)

#### Scenario: Autorização vigente aparece como vigente

- **WHEN** o responsável concedeu a autorização de divulgação e um Guerreiro(a) lê a própria
  persona em sessão
- **THEN** a resposta diz que a autorização está vigente

#### Scenario: Sem decisão nenhuma, o estado é não autorizado

- **WHEN** nenhum responsável decidiu sobre a divulgação daquele Guerreiro(a)
- **THEN** a resposta diz que a autorização não está vigente

#### Scenario: A revogação de um responsável aparece à criança

- **WHEN** um dos responsáveis vinculados revogou a autorização
- **THEN** a resposta diz que a autorização não está vigente

#### Scenario: O estado não revela quem decidiu

- **WHEN** o Guerreiro(a) lê o estado da própria divulgação
- **THEN** a resposta não traz responsável, data nem motivo da decisão

#### Scenario: A leitura não abre caminho de decidir

- **WHEN** o Guerreiro(a) lê o estado da própria divulgação
- **THEN** nenhuma operação de conceder, recusar ou revogar lhe é oferecida
