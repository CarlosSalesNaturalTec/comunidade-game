## Purpose

A trilha de auditoria é o registro consultável de quem escreveu o quê no núcleo, com que
papel, quando e a partir de qual aplicação — a prova, depois do fato, de toda escrita
aceita pela API.

## Requirements

### Requirement: Toda escrita bem-sucedida gera um registro de auditoria

O núcleo SHALL gravar um registro de auditoria para toda chamada de escrita
(`POST`/`PUT`/`PATCH`/`DELETE`) sob o prefixo de versão que termine em sucesso, qualquer que
seja a persona que a fez. Chamada de leitura NEVER gera registro. Chamada de escrita recusada
NEVER gera registro. (`RF-01-29`, PRD-01 §12)

#### Scenario: Escrita bem-sucedida gera registro

- **WHEN** uma persona autenticada faz uma chamada de escrita que o núcleo aceita
- **THEN** nasce um registro de auditoria correspondente àquela chamada

#### Scenario: Escrita recusada não gera registro

- **WHEN** uma chamada de escrita é recusada — por permissão, validação ou qualquer outro
  motivo
- **THEN** nenhum registro de auditoria nasce para aquela chamada

#### Scenario: Leitura não gera registro

- **WHEN** uma aplicação faz uma chamada de leitura, pública ou autenticada
- **THEN** nenhum registro de auditoria nasce para aquela chamada

### Requirement: O registro identifica autor, papel, ação, entidade afetada, momento e origem

Cada registro de auditoria SHALL conter a persona autora, o papel dela no momento da chamada,
a ação realizada, a entidade afetada, a data e a hora com fuso, e a aplicação de origem — a
que apresentou a chave na chamada. (`RF-01-29`, PRD-01 §8)

#### Scenario: Registro traz quem escreveu e com que papel

- **WHEN** uma persona autenticada com um papel realiza uma escrita aceita
- **THEN** o registro de auditoria identifica aquela persona e aquele papel

#### Scenario: Registro traz a aplicação de origem

- **WHEN** uma escrita aceita chega por uma aplicação identificada por sua chave
- **THEN** o registro de auditoria identifica a aplicação de origem daquela chamada

### Requirement: O registro é somente inserção

O núcleo SHALL recusar qualquer alteração ou remoção de um registro de auditoria já gravado.
Corrigir um engano de registro exige um registro novo, nunca a edição do anterior — o mesmo
princípio de guarda permanente que já vale para `Consentimento` e para o acesso ao _template_
biométrico. (PRD-01 §8, "Imutabilidade")

#### Scenario: Alteração de um registro é recusada

- **WHEN** algo tenta alterar um registro de auditoria já gravado
- **THEN** o núcleo recusa a operação e o registro original permanece inalterado

#### Scenario: Remoção de um registro é recusada

- **WHEN** algo tenta apagar um registro de auditoria já gravado
- **THEN** o núcleo recusa a operação e o registro permanece na trilha

### Requirement: A trilha é consultável por Admin

O núcleo SHALL expor a trilha de auditoria em rota de leitura restrita a Admin. Persona de
qualquer outro papel que chamar a rota SHALL receber recusa por permissão. (`RF-01-29`,
PRD-01 §9)

#### Scenario: Admin consulta a trilha

- **WHEN** um Admin chama a rota de consulta da trilha de auditoria
- **THEN** o núcleo devolve os registros de auditoria conforme os filtros aplicados

#### Scenario: Persona sem papel de Admin não consulta a trilha

- **WHEN** uma persona autenticada que não é Admin chama a rota de consulta da trilha de
  auditoria
- **THEN** o núcleo recusa por permissão

### Requirement: A consulta segue o contrato único de listagem

A consulta da trilha de auditoria SHALL ser paginada e SHALL aceitar os filtros universais de
listagem — período e persona — além de filtro por ação e por entidade afetada, no mesmo
contrato que as demais listagens do núcleo. (`RF-01-28`)

#### Scenario: Consulta sem filtro devolve a primeira página

- **WHEN** um Admin consulta a trilha sem informar filtro nem paginação
- **THEN** o núcleo devolve a primeira página, no tamanho padrão, com a informação de como
  obter a página seguinte

#### Scenario: Consulta filtra por período e por persona

- **WHEN** um Admin consulta a trilha informando um período e uma persona
- **THEN** o núcleo devolve apenas os registros daquela persona dentro daquele período

### Requirement: A trilha não reconstrói escrita anterior à sua entrada em vigor

O núcleo SHALL restringir a trilha a escritas aceitas depois de o middleware de auditoria
entrar em vigor, e NEVER gera registro retroativo para escrita aceita antes disso. Escrita
anterior segue rastreável pelos campos de autoria que a própria entidade já grava, fora da
trilha consultável.

#### Scenario: Escrita anterior à trilha não aparece na consulta

- **WHEN** um Admin consulta a trilha de auditoria
- **THEN** a resposta não inclui nenhuma escrita aceita antes de a trilha existir
