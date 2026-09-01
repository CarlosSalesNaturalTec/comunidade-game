## ADDED Requirements

### Requirement: Admin e Mestre leem quem responde por um Guerreiro(a)

O núcleo SHALL responder, a um **Admin** ou a um **Mestre** em sessão, os **responsáveis com
vínculo vigente** com um Guerreiro(a), cada um com o **grau de parentesco**, para que o
atendimento assistido escolha **qual deles está presente**. A leitura SHALL ser a mesma operação
de vínculo que a matriz de permissões já concede aos dois papéis — nenhuma `Operacao` nova — e
persona de qualquer outro papel SHALL receber **403**.

A resposta SHALL trazer apenas o que identifica o responsável para a escolha — nome e grau de
parentesco —, e NEVER SHALL trazer credencial, senha nem contato. Vínculo já encerrado NEVER
SHALL aparecer. (`RF-13-35`, `RN-13-03`, decisão do fundador de 2026-09-01)

#### Scenario: O Mestre vê quem responde pelo Guerreiro(a)

- **WHEN** um Mestre consulta os responsáveis de um Guerreiro(a)
- **THEN** o núcleo devolve os responsáveis com vínculo vigente, cada um com o grau de
  parentesco

#### Scenario: Vínculo encerrado não aparece

- **WHEN** um dos responsáveis teve o vínculo encerrado
- **THEN** ele não aparece na resposta

#### Scenario: A resposta não traz credencial nem contato

- **WHEN** um Admin consulta os responsáveis de um Guerreiro(a)
- **THEN** a resposta traz nome e grau de parentesco, e nenhuma credencial, senha ou contato

#### Scenario: Outro papel não alcança a lista

- **WHEN** um responsável, um Apoiador ou um Guerreiro(a) chama a rota
- **THEN** o núcleo responde 403
