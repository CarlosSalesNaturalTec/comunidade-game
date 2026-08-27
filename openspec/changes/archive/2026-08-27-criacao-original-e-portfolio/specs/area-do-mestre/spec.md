## ADDED Requirements

### Requirement: A App 09 mostra ao Mestre autor as criações originais a validar

A App 09 SHALL apresentar ao Mestre em sessão as criações originais **entregues** nas trilhas de
que ele é **autor**, cada uma com a **trilha**, o **critério de validação** que ele mesmo
declarou na culminância, a **produção entregue** e a **autoria creditada**. Na modalidade de
equipe, a lista SHALL trazer **cada integrante com o papel** que teve na entrega. A lista NEVER
SHALL alcançar criação de trilha de outro Mestre. (`RF-09-31`, `RF-09-32`)

#### Scenario: A fila traz as criações entregues das trilhas do Mestre autor

- **WHEN** o Mestre autor abre as criações originais a validar
- **THEN** a tela lista as entregues nas trilhas dele, com a produção e a autoria de cada uma

#### Scenario: A fila mostra o critério que o próprio Mestre declarou

- **WHEN** o Mestre autor abre uma criação a validar
- **THEN** a tela mostra o critério de validação declarado por ele na culminância daquela trilha

#### Scenario: Criação em equipe traz o papel de cada integrante

- **WHEN** a criação a validar foi entregue por uma equipe da trilha
- **THEN** a tela traz cada integrante creditado com o papel que teve

#### Scenario: Criação de trilha de outro Mestre não aparece

- **WHEN** existe criação original entregue numa trilha de que o Mestre não é autor
- **THEN** ela não aparece na fila dele

### Requirement: O Mestre autor valida a criação, creditando autoria e badge

A App 09 SHALL permitir ao Mestre autor **validar** a criação original entregue. Validada, a
tela SHALL informar que a autoria foi creditada e o **badge de autoria** liberado a cada
creditado, e a criação SHALL sair da fila. A App 09 NEVER SHALL oferecer ao Mestre editar a
produção entregue nem reatribuir a autoria. (`RF-09-31`, `RN-09-04`)

#### Scenario: Validação credita a autoria e libera o badge

- **WHEN** o Mestre autor valida uma criação original entregue
- **THEN** a tela confirma que a autoria foi creditada e o badge de autoria liberado, e a criação
  sai da fila

#### Scenario: A App 09 não edita a produção nem a autoria

- **WHEN** o Mestre autor abre uma criação a validar
- **THEN** a tela não oferece alterar a produção entregue nem reatribuir a autoria

### Requirement: O Mestre autor devolve a criação com motivo, sem tirar a autoria

A App 09 SHALL permitir ao Mestre autor **devolver** a criação original para ajuste, exigindo o
**motivo** escrito em linguagem simples — é ele que o Guerreiro(a) lerá na App 05. Devolução sem
motivo NEVER SHALL ser aceita. A devolução NEVER SHALL alterar a autoria do registro.
(`RF-09-34`, `RF-05-42`, `RN-09-04`)

#### Scenario: Devolução exige o motivo

- **WHEN** o Mestre autor tenta devolver uma criação sem escrever o motivo
- **THEN** a tela recusa a devolução e pede o motivo

#### Scenario: Devolução com motivo preserva a autoria

- **WHEN** o Mestre autor devolve a criação escrevendo o motivo
- **THEN** a criação volta ao Guerreiro(a) com o motivo, e a autoria permanece a mesma

### Requirement: A App 09 informa que a criação validada só vai à vitrine com autorização

A App 09 SHALL informar ao Mestre, na tela da criação validada, que ela só aparece na **vitrine
pública** quando **todos os creditados** têm autorização de divulgação vigente do responsável, e
que sem ela a criação existe apenas no portfólio do Guerreiro(a). A App 09 NEVER SHALL oferecer
ao Mestre conceder, alterar ou revogar essa autorização — é ato do responsável. (`RF-09-33`,
`RN-09-19`)

#### Scenario: A tela diz o que falta para a criação ir à vitrine

- **WHEN** o Mestre valida uma criação de Guerreiro(a) sem autorização de divulgação vigente
- **THEN** a tela informa que ela não irá à vitrine enquanto faltar a autorização do responsável

#### Scenario: A App 09 não altera a autorização de divulgação

- **WHEN** o Mestre vê uma criação validada dependente de autorização
- **THEN** a tela não oferece conceder nem revogar a autorização
