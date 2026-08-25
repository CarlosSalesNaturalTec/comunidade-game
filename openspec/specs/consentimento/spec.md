## Purpose

O consentimento é a prova do que foi autorizado, por quem e quando. Esta capacidade cobre o
registro versionado e **somente inserção** que responde "o que valia naquela data": cada decisão
do responsável — conceder ou revogar — entra como registro novo, com a versão do termo, a autoria
e o momento, e nenhuma delas apaga a anterior. É esse registro que, na fatia seguinte, libera o
cadastro biométrico do Guerreiro(a).

## Requirements

### Requirement: O consentimento tem porta HTTP, sob sessão de adulto

O núcleo SHALL expor o registro de consentimento por **`POST /v1/consentimentos`**, restrita a
Admin e Mestre pela matriz. A rota SHALL receber o responsável que decide, o Guerreiro(a) a que
se refere, o tipo, a decisão, a origem do ato e a testemunha quando houver, e SHALL devolver o
identificador e o momento do registro. A rota NEVER SHALL devolver decisão de consentimento de
Guerreiro(a) algum: ela é de escrita. (`RF-01-19`, `RF-04-12`, `RN-01-12`, PRD-04 §9)

#### Scenario: Mestre registra o termo assinado no encontro

- **WHEN** um Mestre em sessão registra o consentimento de biometria de um Guerreiro(a)
  vinculado ao responsável que decidiu
- **THEN** o núcleo grava o registro com a testemunha, a data e a hora com fuso, e responde 201

#### Scenario: Papel sem permissão não registra consentimento

- **WHEN** uma persona que não é Admin nem Mestre chama a rota
- **THEN** o núcleo responde 403 e nenhum consentimento é gravado

#### Scenario: Consentimento sobre Guerreiro(a) sem vínculo é recusado

- **WHEN** a rota recebe um responsável que não tem vínculo vigente com aquele Guerreiro(a)
- **THEN** o núcleo recusa e nenhum consentimento é gravado

### Requirement: O consentimento é versionado, com autoria, data e hora

O núcleo SHALL registrar cada consentimento com o responsável que decidiu, o Guerreiro(a) a que
se refere, o **tipo**, a **versão do termo**, a **decisão**, a data e hora com fuso, a testemunha
quando houver, a origem do ato e quem o operou. A versão do termo SHALL ser obrigatória: sem ela
não há prova do que foi autorizado. O consentimento SHALL alcançar apenas Guerreiro(a) vinculado
ao responsável que decide. (`RF-01-19`, `RN-01-12`, `RF-01-15`, PRD-01 §§8, 11)

A versão do termo SHALL ser **carimbada pelo núcleo**, a partir da versão vigente que ele guarda
em configuração, e a porta HTTP NEVER SHALL recebê-la do cliente: quem consome a API não escolhe
a versão do termo que o registro vai afirmar. Trocar o termo SHALL ser trocar a configuração, e
registro gravado antes da troca SHALL continuar afirmando a versão que valia quando ele foi
feito. O valor inicial é `2026-08`. (`RF-04-12`, `RN-01-12`, documento 09 — decisão do fundador,
2026-08-24)

O **tipo** SHALL ser um valor de conjunto fechado, e não texto livre. São dois, e são os que a
documentação nomeia:

| Tipo                        | O que cobre                                                       |
| ---------------------------- | ----------------------------------------------------------------- |
| `autorizacao_de_divulgacao` | divulgação do perfil, do histórico e das criações, imagem em fotos e vídeos de eventos e captação da produção — uma só autorização (`RN-13-05`) |
| `biometria`                 | captura e tratamento biométrico do onboarding, de finalidade própria e termo impresso, fora da autorização única (`RN-13-06`, `RN-01-17`) |

Consentimento com tipo fora desse conjunto SHALL ser recusado com **422**. (`RN-13-05`,
`RN-13-06`)

#### Scenario: O registro guarda o que valia

- **WHEN** um consentimento é gravado
- **THEN** o registro carrega a versão do termo, a decisão, quem decidiu e a data e hora com fuso

#### Scenario: A versão vem da configuração, não do cliente

- **WHEN** um consentimento é registrado pela porta HTTP
- **THEN** o registro carrega a versão vigente que o núcleo guarda, e nenhum campo do corpo da
  requisição a determina

#### Scenario: Versão trocada não reescreve o passado

- **WHEN** a versão vigente do termo é trocada na configuração
- **THEN** os consentimentos já gravados continuam afirmando a versão que valia quando foram
  feitos

#### Scenario: Consentimento sem versão do termo é recusado

- **WHEN** um consentimento chega sem a versão do termo
- **THEN** o núcleo responde 422 indicando o campo em falta, e nada é gravado

#### Scenario: Responsável não consente por criança que não é sua

- **WHEN** um responsável decide sobre um Guerreiro(a) que não está vinculado a ele
- **THEN** o núcleo recusa e nenhum consentimento é gravado

#### Scenario: Tipo fora do conjunto é recusado

- **WHEN** um consentimento chega com tipo que não é `autorizacao_de_divulgacao` nem `biometria`
- **THEN** o núcleo responde 422 indicando o campo em falta, e nada é gravado

#### Scenario: A biometria não entra na autorização única

- **WHEN** um responsável concede a `autorizacao_de_divulgacao` de um Guerreiro(a)
- **THEN** nenhum consentimento de `biometria` passa a existir por consequência, e o cadastro
  biométrico continua exigindo o consentimento próprio dele

### Requirement: A autorização vigente se resolve pelo histórico, e a recusa prevalece

O núcleo SHALL derivar a **vigência** de um consentimento do histórico somente inserção, sem
guardar estado à parte: para cada par de Guerreiro(a) e tipo, vale a decisão **mais recente** de
cada responsável vinculado. Havendo mais de um responsável, a **recusa prevalece**: basta que um
deles tenha revogado ou negado, na decisão mais recente dele, para que a autorização **não**
esteja vigente. A resolução SHALL responder também **por data**, devolvendo o que valia em
qualquer momento anterior. (`RF-01-19`, `RN-01-12`, `RN-01-10`, `RN-13-07`)

#### Scenario: Concessão única torna a autorização vigente

- **WHEN** o único responsável vinculado concede a autorização de divulgação
- **THEN** a autorização está vigente para aquele Guerreiro(a)

#### Scenario: A decisão mais recente de cada responsável é a que vale

- **WHEN** um responsável concede, revoga e concede de novo, nessa ordem
- **THEN** vale a última concessão, e as duas decisões anteriores continuam consultáveis

#### Scenario: Recusa de um responsável derruba a autorização

- **WHEN** dois responsáveis estão vinculados, um concedeu e o outro revogou
- **THEN** a autorização não está vigente

#### Scenario: Sem decisão nenhuma, não há autorização

- **WHEN** nenhum responsável decidiu sobre a autorização de divulgação de um Guerreiro(a)
- **THEN** a autorização não está vigente

#### Scenario: A vigência responde por data anterior

- **WHEN** se pergunta se a autorização estava vigente numa data anterior a uma revogação
- **THEN** o núcleo responde pela decisão que valia naquela data, e não pela mais recente

### Requirement: O consentimento é somente inserção

O núcleo SHALL tratar o consentimento como registro de **somente inserção**. Revogar SHALL ser a
gravação de um registro novo com a decisão contrária, e o registro anterior SHALL continuar
consultável. Nenhuma rota, comando ou operação do núcleo SHALL editar ou apagar um consentimento
já gravado. (`RF-01-19`, `RN-01-12`, PRD-01 §8)

#### Scenario: Revogar cria registro novo

- **WHEN** um responsável revoga um consentimento que havia concedido
- **THEN** o núcleo grava um registro novo com a decisão de revogação, e o anterior continua
  consultável

#### Scenario: Consentimento gravado não é editado nem apagado

- **WHEN** qualquer caminho do núcleo tenta alterar ou remover um consentimento já gravado
- **THEN** a operação é recusada e o registro permanece como foi gravado

#### Scenario: O histórico responde por data

- **WHEN** se pergunta o que valia para um Guerreiro(a) em uma data anterior
- **THEN** o núcleo responde pelo registro vigente naquela data, e não pela decisão mais recente

### Requirement: Recusa de consentimento não exclui o Guerreiro(a) da atividade

O núcleo NEVER SHALL usar a recusa ou a revogação de um consentimento para impedir a
participação do Guerreiro(a) na atividade. A decisão do responsável SHALL restringir apenas o que
aquele termo cobre, e o Guerreiro(a) SHALL continuar participando como qualquer outro.
(`RN-01-21`, PRD-01 §11)

#### Scenario: Criança sem consentimento participa igual

- **WHEN** o responsável de um Guerreiro(a) recusa um consentimento
- **THEN** o Guerreiro(a) continua podendo participar da atividade, e nenhuma operação de
  participação é recusada por causa disso

#### Scenario: A revogação não desfaz a participação

- **WHEN** um responsável revoga um consentimento que havia concedido
- **THEN** o que o Guerreiro(a) já realizou permanece registrado, e ele segue participando

### Requirement: O termo impresso assinado no encontro recebe a digitalização anexada

O consentimento de tipo `biometria` é o único firmado em **termo impresso**, assinado no
encontro e confirmado na App 01 pelo Mestre ou pelo Admin que testemunhou (`RF-04-12`). O núcleo
SHALL aceitar, depois do ato, a **digitalização** desse termo, anexada pela gestão.

O anexo SHALL ser gravado como **registro próprio**, que aponta para o consentimento e guarda
quem anexou e quando; ele NEVER SHALL alterar campo algum do consentimento, que permanece de
somente inserção. Anexo de consentimento que já tem digitalização SHALL ser recusado com **409**:
substituir digitalização não é operação do Ciclo 01.

O núcleo SHALL aceitar a digitalização em **PDF, JPG ou PNG** e SHALL recusar com **422**
qualquer outro formato, guardando-a pela porta de armazenamento. A digitalização NEVER SHALL ser
servida em rota pública, e alcançá-la SHALL exigir credencial de gestão.

Anexar SHALL ser ato de **Admin**; qualquer outra persona SHALL receber **403**. Anexo sobre
consentimento de tipo `autorizacao_de_divulgacao` SHALL ser recusado com **422**: esse tipo é
decidido na aplicação, sem termo impresso a digitalizar. (`RF-02-68`, `RN-02-21`, `RN-01-12`,
PRD-02 §§6.3, 9)

#### Scenario: Admin anexa a digitalização do termo de biometria

- **WHEN** um Admin anexa um PDF ao consentimento de biometria de um Guerreiro(a)
- **THEN** o núcleo guarda a digitalização pela porta de armazenamento e grava quem anexou e
  quando, sem alterar o consentimento

#### Scenario: Formato fora dos três é recusado

- **WHEN** chega uma digitalização que não é PDF, JPG nem PNG
- **THEN** o núcleo responde 422 e nada é guardado

#### Scenario: Segunda digitalização no mesmo consentimento é recusada

- **WHEN** um Admin anexa digitalização a um consentimento que já tem uma
- **THEN** o núcleo responde 409 e a digitalização anterior permanece

#### Scenario: Consentimento de divulgação não recebe anexo

- **WHEN** um Admin tenta anexar digitalização a um consentimento de tipo
  `autorizacao_de_divulgacao`
- **THEN** o núcleo responde 422 e nada é guardado

#### Scenario: Quem não é Admin não anexa

- **WHEN** um Mestre tenta anexar a digitalização de um termo de biometria
- **THEN** o núcleo responde 403 e nada é guardado

#### Scenario: A digitalização não é servida sem credencial de gestão

- **WHEN** a digitalização é pedida sem credencial de gestão
- **THEN** o núcleo recusa e o arquivo não é servido
