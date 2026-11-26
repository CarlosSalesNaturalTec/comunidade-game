## MODIFIED Requirements

### Requirement: A lista de Guerreiros e Guerreiras mostra o vínculo, sem caminho de troca

A App 03 SHALL apresentar, na lista de Guerreiros e Guerreiras da área Personas, o **nick**, o
**nome** e a **comunidade do vínculo vigente** de cada um, em **leitura**, sem coluna de avatar
nem de início do vínculo. NEVER SHALL oferecer caminho de mudar a comunidade (no Ciclo 01 não há
transferência) nem exibir imagem real; Guerreiro(a) sem vínculo vigente SHALL aparecer com a
ausência informada em linguagem simples. (`RF-02-15`, `RN-02-06`, `RN-02-22`, `RF-08-02`,
`RF-08-03`, documento 99 §6 invariantes 4 e 12)

#### Scenario: A lista apresenta a comunidade herdada da aula

- **WHEN** o Admin abre a lista de Guerreiros e Guerreiras
- **THEN** cada um aparece com o nick, o nome e a comunidade do vínculo vigente

#### Scenario: A lista não traz avatar nem início do vínculo

- **WHEN** o Admin abre a lista de Guerreiros e Guerreiras
- **THEN** não há coluna "Avatar" nem "Início do vínculo", e nenhuma imagem real aparece

#### Scenario: Não existe tela de transferência de comunidade

- **WHEN** o Admin procura, na lista ou na edição do Guerreiro(a), um caminho para mudar a
  comunidade dele
- **THEN** nenhum lhe é oferecido em lugar algum da aplicação

#### Scenario: Guerreiro(a) sem vínculo vigente é informado, não acusado

- **WHEN** a lista alcança um Guerreiro(a) sem vínculo vigente
- **THEN** a ausência aparece em linguagem simples, como informação, e não como aviso de erro
