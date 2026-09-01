## ADDED Requirements

### Requirement: O ato assistido registra a autorização em nome do responsável presente

O núcleo SHALL aceitar de um **Admin** ou de um **Mestre** em sessão a decisão da autorização
única de um Guerreiro(a) **em nome do responsável presente**, para o caso de quem não tem
smartphone. O registro SHALL gravar o **responsável como quem decide**, **quem operou** o ato, a
**testemunha**, a origem **assistida** e a **versão do termo carimbada pela configuração** — a
rota NEVER SHALL receber a versão do cliente.

O **responsável presente** SHALL ser identificado e SHALL ter **vínculo vigente** com aquele
Guerreiro(a): ato sem responsável identificado SHALL ser recusado com **422**, e responsável sem
vínculo vigente SHALL ser recusado com **403**. A **testemunha** SHALL ser obrigatória: ato sem
ela SHALL ser recusado com **422**.

O ato assistido SHALL ter a **mesma força** do registrado pelo próprio responsável: entra na
mesma derivação do estado vigente, conta na mesma regra de que a recusa prevalece e aparece no
mesmo histórico. Persona de qualquer outro papel SHALL receber **403**. (`RF-13-35`,
`RF-13-36`, `RF-13-38`, `RN-13-16`, `RN-13-07`, PRD-13 §§5.8, 6.6, 9)

#### Scenario: Mestre registra a concessão em nome do responsável presente

- **WHEN** um Mestre registra a concessão da autorização única com o responsável presente e uma
  testemunha
- **THEN** o núcleo grava a decisão em nome do responsável, com origem assistida, quem operou,
  a testemunha e a versão vigente do termo

#### Scenario: O ato assistido produz o mesmo estado que o ato do próprio

- **WHEN** a concessão é registrada pelo modo assistido e o vinculado não tem recusa de outro
  responsável
- **THEN** o estado da autorização passa a concedido, igual ao que o próprio responsável
  produziria no aparelho

#### Scenario: Ato assistido sem responsável presente identificado é recusado

- **WHEN** o ato assistido chega sem identificar o responsável presente
- **THEN** o núcleo responde 422 e nada é gravado

#### Scenario: Ato assistido sem testemunha é recusado

- **WHEN** o ato assistido chega sem a testemunha
- **THEN** o núcleo responde 422 e nada é gravado

#### Scenario: Responsável sem vínculo vigente é recusado

- **WHEN** o ato assistido nomeia um responsável que não tem vínculo vigente com aquele
  Guerreiro(a)
- **THEN** o núcleo responde 403 e nada é gravado

#### Scenario: A recusa assistida prevalece como qualquer outra

- **WHEN** o modo assistido registra a recusa de um responsável sobre vinculado que outro já
  havia concedido
- **THEN** o estado passa a suspenso, com quem o motivou, data e hora

#### Scenario: Quem não é Admin nem Mestre não opera o ato assistido

- **WHEN** um responsável, um Apoiador ou um Guerreiro(a) chama a rota do ato assistido
- **THEN** o núcleo responde 403 e nada é gravado
