## ADDED Requirements

### Requirement: A programação do encontro mostra os materiais da missão

A programação do encontro (`GET /v1/equipes/{id}/missao`) SHALL devolver, em cada item, os
`missao_materiais` declarados pelo Mestre autor. A App 01 SHALL mostrá-los junto da missão, sob
o rótulo **Materiais para a aula**, antes do conteúdo; missão sem materiais NEVER SHALL exibir
o rótulo. Mostrar os materiais SHALL apenas ler: NEVER SHALL gravar nem enviar coisa alguma, e
NEVER SHALL exibir dado pessoal de Guerreiro(a). (`RF-04-79`, `RF-04-35`, `RF-09-140`)

#### Scenario: Missão com materiais

- **WHEN** a equipe abre a programação de missão que declara "cola" e "papel"
- **THEN** a tela mostra "Materiais para a aula" com os dois nomes, junto da missão

#### Scenario: Missão sem materiais

- **WHEN** a equipe abre a programação de missão sem materiais
- **THEN** a tela não exibe o rótulo dos materiais
