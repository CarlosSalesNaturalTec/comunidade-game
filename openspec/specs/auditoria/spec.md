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

### Requirement: A trilha registra o Guerreiro(a) que a escrita alcança

O núcleo SHALL registrar, junto da linha da trilha, **qual Guerreiro(a) aquela escrita
alcançou**, sempre que o pedido o nomeia — e **todos eles**, quando a mesma escrita alcança mais
de um, como o lançamento do resultado de uma atividade inteira. O registro SHALL continuar
sendo obtido **sem que rota alguma declare nada**, no mesmo princípio da trilha, e SHALL manter
a trilha **somente inserção**.

Escrita que não nomeia Guerreiro(a) SHALL entrar na trilha sem esse recorte, e NEVER SHALL
aparecer no histórico de acessos de criança alguma. (`RF-13-30`, PRD-01 §8)

#### Scenario: Escrita sobre uma criança fica ligada a ela

- **WHEN** um Mestre confirma a presença de um Guerreiro(a)
- **THEN** a linha da trilha fica ligada àquele Guerreiro(a)

#### Scenario: Escrita sobre várias crianças fica ligada a todas

- **WHEN** um Mestre lança de uma vez o resultado de todos os participantes de uma atividade
- **THEN** a linha da trilha fica ligada a cada um dos Guerreiros e Guerreiras lançados

#### Scenario: Escrita que não nomeia criança não entra em histórico algum

- **WHEN** um Admin cadastra uma trilha ou emite uma chave de aplicação
- **THEN** a linha entra na trilha sem recorte de Guerreiro(a), e não aparece no histórico de
  acessos de nenhuma criança

### Requirement: O responsável lê o histórico de acessos do vinculado

O núcleo SHALL responder ao **responsável em sessão**, sobre um Guerreiro(a) **vinculado a
ele**, o histórico das escritas que alcançaram aquela criança, cada uma com **data e hora com
fuso**, **quem acessou**, **em que papel** e **qual dado**. A consulta SHALL ser paginada, no
mesmo contrato de listagem das demais consultas do núcleo, e SHALL vir da ordem mais recente
para a mais antiga.

O histórico NEVER SHALL trazer escrita que alcançou **outra criança**, nem o **conteúdo** do
dado escrito — apenas qual dado foi tocado. Responsável sem vínculo vigente com aquele
Guerreiro(a) SHALL receber **403**, e persona de outro papel SHALL receber **403** na mesma
rota. (`RF-13-30`, `RN-13-04`, PRD-13 §§6.5, 9, 12)

#### Scenario: O acesso de rotina do Mestre aparece com data, hora e dado

- **WHEN** o responsável abre o histórico de acessos de um vinculado cuja presença o Mestre da
  turma confirmou
- **THEN** o acesso aparece com a data, a hora, o nome de quem acessou, o papel de Mestre e o
  dado consultado

#### Scenario: O histórico não vaza acesso a outra criança

- **WHEN** a mesma escrita alcançou dois Guerreiros e Guerreiras de responsáveis diferentes
- **THEN** cada responsável vê apenas a linha do seu vinculado, sem saber da outra criança

#### Scenario: O histórico não traz o conteúdo do dado

- **WHEN** o responsável lê uma linha do histórico
- **THEN** vê qual dado foi tocado, e não o valor que foi gravado

#### Scenario: Guerreiro(a) não vinculado é recusado

- **WHEN** o responsável pede o histórico de um Guerreiro(a) que não é vinculado a ele
- **THEN** o núcleo responde 403 e não revela dado algum daquela criança

### Requirement: A trilha é consultável por Admin

O núcleo SHALL expor a trilha de auditoria **inteira** em rota de leitura restrita a Admin.
Persona de qualquer outro papel que chamar essa rota SHALL receber recusa por permissão — o
recorte que o responsável lê é **outra rota**, restrita ao Guerreiro(a) vinculado a ele, e não
alcança a trilha inteira. (`RF-01-29`, `RF-13-30`, PRD-01 §9)

#### Scenario: Admin consulta a trilha

- **WHEN** um Admin chama a rota de consulta da trilha de auditoria
- **THEN** o núcleo devolve os registros de auditoria conforme os filtros aplicados

#### Scenario: Persona sem papel de Admin não consulta a trilha

- **WHEN** uma persona autenticada que não é Admin chama a rota de consulta da trilha de
  auditoria
- **THEN** o núcleo recusa por permissão

#### Scenario: O responsável não alcança a trilha inteira

- **WHEN** um responsável em sessão chama a rota de consulta da trilha de auditoria
- **THEN** o núcleo recusa por permissão, e ele segue lendo apenas o histórico do vinculado

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
