## ADDED Requirements

### Requirement: O Painel do dia apresenta a equipe pelo nome e o papel de cada integrante

A App 03 SHALL apresentar, no Painel do dia, cada equipe pelo **nome** que os Guerreiros e
Guerreiras lhe deram no App 01, e cada integrante pelo **nick** com o **papel** declarado ao
lado; integrante sem papel SHALL aparecer só pelo nick, sem rótulo vazio. A tela NEVER SHALL
oferecer renomear a equipe nem trocar o papel de alguém. (`RF-02-08`, `RF-02-09`, PRD-02 §6.4)

#### Scenario: A equipe aparece pelo nome, com o papel de cada um

- **WHEN** o painel traz a equipe "Leões", com um integrante que declarou "quem apresenta"
- **THEN** a tela mostra "Leões" e, abaixo, o nick daquele integrante com "quem apresenta"

#### Scenario: Integrante sem papel aparece só pelo nick

- **WHEN** um integrante da equipe não declarou papel
- **THEN** a tela mostra apenas o nick dele, sem rótulo vazio

#### Scenario: O painel não renomeia a equipe

- **WHEN** o operador procura trocar o nome da equipe pelo painel
- **THEN** a tela não oferece esse caminho
