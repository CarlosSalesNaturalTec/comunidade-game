## ADDED Requirements

### Requirement: A gestão lê os pontos de apoio, filtrados por comunidade

O núcleo SHALL devolver os pontos de apoio com **nome**, **comunidade** a que pertencem,
**responsável designado** — quando já houver — e se estão **ativos**. A leitura SHALL ser
paginada e SHALL aceitar filtro por **comunidade**.

A leitura SHALL exigir persona de gestão em sessão: o **Admin** SHALL ler todas as comunidades e
o **Mestre**, apenas as comunidades a que está vinculado. **Apoiador**, **Guerreiro(a)** e
**responsável** SHALL receber **403**.

O ponto de apoio ainda **sem responsável designado** SHALL sair na leitura assim mesmo — a
designação é posterior ao cadastro, e a ausência dela NEVER SHALL impedir que o espaço seja
lido ou escolhido no agendamento. (`RF-07-47`, `RF-07-49`, `RF-01-28`, `RF-01-18`, `RF-01-16`,
`RN-07-34`, PRD-07 §§8, 10)

#### Scenario: Admin lê os pontos de apoio de uma comunidade

- **WHEN** um Admin em sessão consulta os pontos de apoio filtrando por uma comunidade
- **THEN** vêm apenas os pontos de apoio daquela comunidade, com nome, responsável designado e
  se estão ativos

#### Scenario: Mestre lê apenas os pontos de apoio das suas comunidades

- **WHEN** um Mestre vinculado a uma comunidade consulta os pontos de apoio
- **THEN** vêm apenas os daquela comunidade

#### Scenario: Guerreiro(a) não lê os pontos de apoio da gestão

- **WHEN** um Guerreiro(a) em sessão consulta os pontos de apoio
- **THEN** o núcleo responde 403

#### Scenario: Ponto de apoio sem responsável designado é lido assim mesmo

- **WHEN** um ponto de apoio recém-cadastrado, ainda sem responsável pelo acervo, é consultado
- **THEN** ele vem na leitura, com o responsável ausente e sem que isso seja erro
