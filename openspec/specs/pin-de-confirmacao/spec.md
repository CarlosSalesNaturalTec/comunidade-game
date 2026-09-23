# pin-de-confirmacao Specification

## Purpose
O PIN de confirmação é o segundo fator do Mestre e do Admin no encontro: prova que o adulto que
abriu a sessão de trabalho do aparelho está ao lado da criança no momento em que confirma a
identidade dela. Esta capacidade cobre o cadastro e a troca do PIN, a guarda só do verificador,
a entrega do verificador ao aparelho e o bloqueio por erros seguidos.

## Requirements

### Requirement: Mestre e Admin cadastram e trocam o próprio PIN de confirmação

O núcleo SHALL permitir que um **Mestre** ou um **Admin** em sessão cadastre ou troque o
**próprio** PIN de confirmação, de **exatamente 4 dígitos**, pela rota
`PUT /v1/eu/pin-de-confirmacao`. A troca SHALL substituir o PIN anterior sem pedir o antigo: é o
login Google da sessão que autentica o adulto. PIN fora do formato SHALL ser recusado na
validação do corpo. Persona de qualquer outro papel SHALL receber **403**. (`RF-01-75`,
`RF-09-121`, `RF-02-110`, documento 03 §1.1)

O núcleo SHALL guardar **apenas o verificador** do PIN: resumo com sal, por derivação lenta de
chave. NEVER SHALL gravar o PIN, nem devolvê-lo em rota alguma, nem escrevê-lo em registro de
auditoria ou log. (`RF-01-75`)

#### Scenario: Mestre cadastra o PIN

- **WHEN** um Mestre em sessão envia um PIN de 4 dígitos
- **THEN** o núcleo grava o verificador do PIN, e a resposta não traz o PIN

#### Scenario: A troca não pede o PIN antigo

- **WHEN** um Admin que já tinha PIN envia um PIN novo
- **THEN** o núcleo substitui o verificador, e o PIN antigo deixa de conferir

#### Scenario: PIN fora do formato é recusado

- **WHEN** chega um PIN com 3 dígitos, 5 dígitos ou letras
- **THEN** o núcleo recusa a validação do corpo e o verificador anterior não muda

#### Scenario: Quem não é Mestre nem Admin não cadastra PIN

- **WHEN** um Apoiador ou um responsável em sessão envia um PIN
- **THEN** o núcleo responde 403

#### Scenario: O PIN nunca é gravado

- **WHEN** se examinam o banco, o registro de auditoria e os logs depois de um cadastro
- **THEN** não há PIN, só o verificador com sal

### Requirement: O aparelho da sessão de trabalho recebe só o verificador de quem a abriu

O núcleo SHALL entregar, pela rota `GET /v1/eu/pin-de-confirmacao/verificador`, o verificador
do PIN **da própria persona da sessão** — sal, parâmetros da derivação e resumo —, e apenas à
**chave do App 01**, que é onde a confirmação sem rede acontece. Outra chave de aplicação SHALL
receber **403**. Sem PIN cadastrado, a rota SHALL responder com o erro que diz isso, para que o
App 01 oriente o adulto. A rota NEVER SHALL devolver verificador de outra persona. (`RF-01-75`,
`RN-04-38`, documento 03 §3.4)

#### Scenario: O App 01 recebe o verificador de quem abriu a sessão

- **WHEN** o Mestre que abriu a sessão de trabalho pede o verificador pela chave do App 01
- **THEN** o núcleo devolve o verificador do PIN dele, e nunca o PIN

#### Scenario: Outra aplicação não recebe verificador

- **WHEN** o mesmo Mestre pede o verificador pela chave da App 09
- **THEN** o núcleo responde 403

#### Scenario: Sem PIN cadastrado, a resposta diz isso

- **WHEN** um Admin sem PIN cadastrado pede o verificador pelo App 01
- **THEN** o núcleo responde com o erro de PIN não cadastrado, sem corpo de verificador

### Requirement: Cinco erros seguidos bloqueiam o PIN na sessão de trabalho

O núcleo SHALL contar os erros **seguidos** de PIN de cada **sessão de trabalho** — a sessão
do adulto no aparelho. O acerto SHALL zerar a contagem. No **quinto** erro seguido, o PIN SHALL
ficar **bloqueado naquela sessão**: toda confirmação seguinte SHALL ser recusada com o erro de
PIN bloqueado, **mesmo com o PIN certo**, até o adulto abrir uma **nova sessão** pelo login
Google. Outra sessão do mesmo adulto, em outro aparelho, NEVER SHALL herdar o bloqueio.
(`RN-01-59`, `RN-04-38`, documento 03 §1.1)

#### Scenario: O quinto erro bloqueia

- **WHEN** o adulto erra o PIN cinco vezes seguidas na mesma sessão de trabalho
- **THEN** a sexta tentativa é recusada como PIN bloqueado, ainda que o PIN esteja certo

#### Scenario: O acerto zera a contagem

- **WHEN** o adulto erra quatro vezes, acerta, e erra mais quatro
- **THEN** o PIN segue desbloqueado

#### Scenario: O novo login desbloqueia

- **WHEN** o adulto com PIN bloqueado encerra a sessão e entra de novo pelo Google no aparelho
- **THEN** a nova sessão de trabalho confere o PIN normalmente

#### Scenario: O bloqueio não passa para outro aparelho

- **WHEN** o PIN está bloqueado na sessão de um aparelho e o mesmo adulto confirma em outro
  aparelho, na sessão aberta lá
- **THEN** a confirmação nesse outro aparelho confere o PIN normalmente
