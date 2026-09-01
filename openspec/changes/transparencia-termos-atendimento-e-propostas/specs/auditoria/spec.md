## ADDED Requirements

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

## MODIFIED Requirements

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
