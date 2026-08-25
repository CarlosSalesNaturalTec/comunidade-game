## ADDED Requirements

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
