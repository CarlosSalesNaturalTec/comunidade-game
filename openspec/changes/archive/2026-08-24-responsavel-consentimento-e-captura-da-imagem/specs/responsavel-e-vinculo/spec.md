## MODIFIED Requirements

### Requirement: Admin ou Mestre cadastra o responsável

O núcleo SHALL permitir que um Admin ou um Mestre cadastre a persona de responsável. O
responsável SHALL ser a única persona que o Mestre cadastra. O cadastro NEVER SHALL, por si só,
dar ao responsável acesso a Guerreiro(a) algum — o que ele alcança vem do vínculo, não do
cadastro.
Persona de outro papel que tentar cadastrar responsável SHALL receber **403**. (`RF-01-13`,
`RN-01-01`, PRD-01 §§4, 5.3, 9)

O cadastro SHALL receber o **nome** do responsável, e SHALL recusá-lo em branco: é sobre esse
nome que se apoia o consentimento que autoriza a captura da imagem da criança, e responsável
sem nome não sustenta a base legal do tratamento. O cadastro NEVER SHALL exigir e-mail,
credencial de acesso ou a digitalização do termo — o acesso à App 07 e o arquivo do documento
continuam sendo atos da gestão, depois do encontro. (`RF-04-60`, PRD-04 §§3.2, 11, PRD-13 §11,
documento 09 — decisão do fundador, 2026-08-24)

#### Scenario: Mestre cadastra responsável

- **WHEN** um Mestre cadastra a persona de um responsável com o nome dela
- **THEN** o núcleo cria a persona de responsável, guarda o nome e registra a autoria do Mestre

#### Scenario: Cadastro sem nome é recusado

- **WHEN** o cadastro de responsável chega sem nome, ou com nome em branco
- **THEN** o núcleo responde 422 indicando o campo em falta, e nenhuma persona é criada

#### Scenario: O cadastro não cria acesso

- **WHEN** um responsável é cadastrado no encontro
- **THEN** nenhuma credencial de acesso nasce com ele, e a entrada na App 07 continua dependendo
  de ato da gestão

#### Scenario: Responsável recém-cadastrado não alcança ninguém

- **WHEN** um responsável acabou de ser cadastrado e ainda não tem vínculo
- **THEN** ele autentica normalmente e não enxerga Guerreiro(a) algum

#### Scenario: Papel sem permissão não cadastra responsável

- **WHEN** uma persona que não é Admin nem Mestre tenta cadastrar um responsável
- **THEN** o núcleo responde 403 e nenhuma persona é criada
