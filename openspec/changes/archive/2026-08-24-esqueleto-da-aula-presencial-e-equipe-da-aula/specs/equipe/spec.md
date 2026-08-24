## ADDED Requirements

### Requirement: A equipe da aula é alcançável por HTTP pelo Guerreiro(a) em sessão

O núcleo SHALL expor a formação da equipe da aula pelas quatro rotas do PRD-04 §9 —
`GET /v1/aulas/{id}/equipes`, `POST /v1/aulas/{id}/equipes`,
`POST /v1/equipes/{id}/integrantes` e `DELETE /v1/equipes/{id}/integrantes/eu` —, todas sob a
**sessão do Guerreiro(a)** e sob a chave de aplicação, pelas convenções de erro e paginação do
PRD-01. As rotas SHALL reexpor as recusas já vigentes desta capacidade, sem afrouxar nenhuma:
os dois tetos, a equipe de aula encerrada, a equipe única por trilha e a vedação de Admin e
Mestre alterarem composição. (`RF-04-30`, `RF-04-31`, `RF-04-32`, `RF-04-33`, `RF-04-59`,
`RF-01-37`, `RF-01-38`, `RF-01-16`)

#### Scenario: Guerreiro(a) cria a equipe da aula por HTTP

- **WHEN** um Guerreiro(a) em sessão pede a criação de equipe numa aula vigente
- **THEN** o núcleo responde 201 com a equipe criada, tendo-o como primeiro integrante

#### Scenario: Guerreiro(a) entra em equipe existente por HTTP

- **WHEN** um Guerreiro(a) em sessão pede entrada numa equipe da aula
- **THEN** o núcleo responde 201 e ele passa a integrar a equipe

#### Scenario: Guerreiro(a) sai da própria equipe por HTTP

- **WHEN** um integrante pede a própria saída da equipe que integra
- **THEN** o núcleo responde 204 e ele deixa de integrá-la

#### Scenario: O sexto integrante é recusado pela porta

- **WHEN** um sexto integrante pede entrada numa equipe de cinco
- **THEN** o núcleo responde 422 e a composição não muda

#### Scenario: O segundo integrante de 17 anos ou mais é recusado pela porta

- **WHEN** uma segunda persona que não é Guerreiro(a) pede entrada na mesma equipe
- **THEN** o núcleo responde 422 e a composição não muda

#### Scenario: Equipe de aula encerrada não recebe integrante pela porta

- **WHEN** um Guerreiro(a) pede entrada numa equipe cuja aula já se encerrou
- **THEN** o núcleo responde 422 e a composição não muda

#### Scenario: Admin não cria equipe pela porta

- **WHEN** um Admin em sessão pede a criação de equipe numa aula
- **THEN** o núcleo responde 403 e nenhuma equipe é criada

#### Scenario: Mestre não altera composição pela porta

- **WHEN** um Mestre em sessão pede entrada ou saída de integrante numa equipe
- **THEN** o núcleo responde 403 e a composição não muda

#### Scenario: Sem sessão de persona a porta não abre

- **WHEN** chega um pedido de criação de equipe sem credencial de persona
- **THEN** o núcleo recusa e nenhuma equipe é criada

#### Scenario: O papel do integrante entra pela porta

- **WHEN** um Guerreiro(a) cria equipe ou entra em equipe declarando o papel
- **THEN** o núcleo grava o papel junto do vínculo dele com a equipe

### Requirement: A leitura das equipes da aula devolve apenas avatar e nick

O núcleo SHALL devolver, em `GET /v1/aulas/{id}/equipes`, as equipes vinculadas **àquela** aula,
com os integrantes identificados **apenas por avatar e nick**. A leitura NEVER SHALL devolver
nome, data de nascimento, imagem, _template_ biométrico ou qualquer outro dado pessoal do
Guerreiro(a), e NEVER SHALL trazer equipe de outra aula nem equipe da trilha. A leitura SHALL
ser restrita à persona em sessão pela operação `equipes_da_aula_em_andamento` da matriz.
(`RF-04-34`, `RN-04-14`, `RF-01-37`, documento 99 §6 invariantes 11 e 12)

#### Scenario: As equipes daquela aula são devolvidas

- **WHEN** um Guerreiro(a) em sessão consulta as equipes de uma aula
- **THEN** o núcleo devolve as equipes vinculadas àquela aula, cada uma com os integrantes

#### Scenario: Só avatar e nick de cada integrante

- **WHEN** a leitura devolve os integrantes de uma equipe
- **THEN** cada integrante traz avatar e nick, e nenhum outro dado pessoal

#### Scenario: Equipe da trilha não aparece na leitura da aula

- **WHEN** existem equipes de trilha além das equipes da aula consultada
- **THEN** o núcleo devolve apenas as equipes da aula, sem as da trilha

#### Scenario: Aula sem equipe devolve conjunto vazio

- **WHEN** a aula consultada ainda não tem equipe formada
- **THEN** o núcleo responde 200 com conjunto vazio, nunca erro
