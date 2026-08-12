## Purpose

O consentimento é a prova do que foi autorizado, por quem e quando. Esta capacidade cobre o
registro versionado e **somente inserção** que responde "o que valia naquela data": cada decisão
do responsável — conceder ou revogar — entra como registro novo, com a versão do termo, a autoria
e o momento, e nenhuma delas apaga a anterior. É esse registro que, na fatia seguinte, libera o
cadastro biométrico do Guerreiro(a).

## ADDED Requirements

### Requirement: O consentimento é versionado, com autoria, data e hora

O núcleo SHALL registrar cada consentimento com o responsável que decidiu, o Guerreiro(a) a que
se refere, o **tipo**, a **versão do termo**, a **decisão**, a data e hora com fuso, a testemunha
quando houver, a origem do ato e quem o operou. A versão do termo SHALL ser obrigatória: sem ela
não há prova do que foi autorizado. O consentimento SHALL alcançar apenas Guerreiro(a) vinculado
ao responsável que decide. (`RF-01-19`, `RN-01-12`, `RF-01-15`, PRD-01 §§8, 11)

#### Scenario: O registro guarda o que valia

- **WHEN** um consentimento é gravado
- **THEN** o registro carrega a versão do termo, a decisão, quem decidiu e a data e hora com fuso

#### Scenario: Consentimento sem versão do termo é recusado

- **WHEN** um consentimento chega sem a versão do termo
- **THEN** o núcleo responde 422 indicando o campo em falta, e nada é gravado

#### Scenario: Responsável não consente por criança que não é sua

- **WHEN** um responsável decide sobre um Guerreiro(a) que não está vinculado a ele
- **THEN** o núcleo recusa e nenhum consentimento é gravado

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
