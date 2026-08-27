## ADDED Requirements

### Requirement: O Admin lê os desafios de trilha publicada, com as séries ativas de cada um

O núcleo SHALL expor rota de **Admin** que lista os desafios de coleta **cuja missão pertence a
trilha em situação `publicada`**, cada um com o **tipo de coleta**, a **cadência**, a
**vigência**, a **granularidade exigida** e a **quantidade de séries de coleta no estado
`ativa`**. Persona de qualquer outro papel SHALL receber **403**, e a listagem SHALL ser
paginada como toda listagem do núcleo. (`RF-02-17`, `RF-08-06`, `RF-01-28`)

Desafio de missão de trilha em **rascunho** ou **despublicada** NEVER SHALL aparecer: "publicado"
é a situação da trilha, porque o desafio não tem situação própria (decisão do fundador,
2026-08-27). Desafio sem série alguma SHALL sair com **zero** séries ativas; série
`interrompida` ou `encerrada` NEVER SHALL ser contada entre as ativas.

A rota é **leitura**: ela NEVER SHALL criar, alterar nem apagar desafio de coleta — a autoria
continua sendo do Mestre autor da trilha, e o filtro de comunidade não se aplica, porque a
trilha é bem comum da plataforma e não tem comunidade (`RN-01-42`).

#### Scenario: Admin lê o desafio publicado com cadência, vigência e séries ativas

- **WHEN** um Admin em sessão consulta os desafios de coleta
- **THEN** o núcleo devolve os desafios de missões de trilhas publicadas, cada um com tipo,
  cadência, vigência, granularidade exigida e a quantidade de séries ativas

#### Scenario: Desafio de trilha em rascunho fica de fora

- **WHEN** existe desafio numa missão de trilha ainda em rascunho e outro numa trilha publicada
- **THEN** a listagem devolve apenas o da trilha publicada

#### Scenario: Só a série ativa é contada

- **WHEN** um desafio publicado tem séries nos estados `ativa`, `interrompida` e `encerrada`
- **THEN** a quantidade devolvida conta apenas as `ativa`

#### Scenario: Desafio sem série sai com zero

- **WHEN** um desafio publicado ainda não tem série aberta
- **THEN** ele sai na listagem com zero séries ativas

#### Scenario: Persona que não é Admin é recusada

- **WHEN** um Mestre, um Guerreiro(a), um responsável ou um Apoiador consulta a rota
- **THEN** o núcleo responde 403
