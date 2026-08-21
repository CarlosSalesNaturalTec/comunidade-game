## ADDED Requirements

### Requirement: A dependência externa de identidade só é acionada quando configurada

A App 03 SHALL acionar o provedor externo de identidade apenas quando o client ID do ambiente
em que ela roda estiver configurado, e NEVER SHALL carregar o script dele em ambiente que não
o tenha — conferência à mão, execução de teste ou demonstração. A tela de entrada SHALL
continuar apresentável nesse ambiente, sem apresentar a ausência do provedor como falha.
(documento 03 §1 princípio 2, PRD-02 §10)

#### Scenario: Ambiente sem client ID configurado

- **WHEN** a tela de entrada é apresentada num ambiente cujo client ID não está configurado
- **THEN** nenhum script do provedor externo de identidade é carregado, e a tela continua
  apresentável, sem mensagem de erro

#### Scenario: Ambiente com client ID configurado

- **WHEN** a tela de entrada é apresentada num ambiente cujo client ID está configurado
- **THEN** o caminho de entrada pela conta social é oferecido ao adulto
