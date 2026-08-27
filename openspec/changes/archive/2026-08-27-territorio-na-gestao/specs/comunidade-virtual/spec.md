## ADDED Requirements

### Requirement: A gestão lê o vínculo vigente do Guerreiro(a), e nada além disso

O núcleo SHALL devolver, na **listagem de Guerreiros e Guerreiras restrita ao Admin**, o
**vínculo vigente** de cada um: a **comunidade** e a **data de início** do vínculo. É o que a
gestão precisa para **conferir** o que a aula agendada atribuiu, sem tela de transferência.
(`RF-02-15`, `RF-08-02`, `RN-02-06`)

Guerreiro(a) **sem vínculo vigente** SHALL sair com a comunidade e a data **vazias**, e a
ausência NEVER SHALL virar erro da listagem. A leitura NEVER SHALL devolver o **histórico** dos
vínculos encerrados — só o vigente —, e NEVER SHALL abrir caminho de escrita: continua não
existindo rota que mova o Guerreiro(a) de comunidade no Ciclo 01 (`RF-08-03`). Persona que não é
Admin SHALL receber **403**, como já recebe da listagem.

#### Scenario: A listagem traz a comunidade e a data de início

- **WHEN** um Admin em sessão consulta a listagem de Guerreiros e Guerreiras
- **THEN** cada Guerreiro(a) sai com a comunidade do vínculo vigente e a data de início dele

#### Scenario: Guerreiro(a) sem vínculo vigente sai com os campos vazios

- **WHEN** a listagem alcança um Guerreiro(a) que não tem vínculo vigente
- **THEN** ele sai com comunidade e data de início vazias, e a listagem responde normalmente

#### Scenario: O histórico encerrado não sai na listagem

- **WHEN** um Guerreiro(a) tem vínculo encerrado além do vigente
- **THEN** a listagem devolve apenas o vigente

#### Scenario: A leitura não abre caminho de troca

- **WHEN** se procura, a partir desta leitura, rota que troque a comunidade do Guerreiro(a)
- **THEN** nenhuma existe, e a tentativa devolve **404**
