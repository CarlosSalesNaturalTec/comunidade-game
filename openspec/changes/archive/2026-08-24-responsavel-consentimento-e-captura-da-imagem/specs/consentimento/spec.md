## ADDED Requirements

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

## MODIFIED Requirements

### Requirement: O consentimento é versionado, com autoria, data e hora

O núcleo SHALL registrar cada consentimento com o responsável que decidiu, o Guerreiro(a) a que
se refere, o **tipo**, a **versão do termo**, a **decisão**, a data e hora com fuso, a testemunha
quando houver, a origem do ato e quem o operou. A versão do termo SHALL ser obrigatória: sem ela
não há prova do que foi autorizado. O consentimento SHALL alcançar apenas Guerreiro(a) vinculado
ao responsável que decide. (`RF-01-19`, `RN-01-12`, `RF-01-15`, PRD-01 §§8, 11)

A versão do termo SHALL ser **carimbada pelo núcleo**, a partir da versão vigente que ele
guarda em configuração, e a porta HTTP NEVER SHALL recebê-la do cliente: quem consome a API não
escolhe a versão do termo que o registro vai afirmar. Trocar o termo SHALL ser trocar a
configuração, e registro gravado antes da troca SHALL continuar afirmando a versão que valia
quando ele foi feito. (`RF-04-12`, `RN-01-12`, documento 09 — decisão do fundador, 2026-08-24)

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

- **WHEN** um consentimento é registrado sem a versão do termo
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
