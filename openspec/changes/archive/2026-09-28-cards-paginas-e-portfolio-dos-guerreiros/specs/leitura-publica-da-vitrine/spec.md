# Spec Delta

## ADDED Requirements

### Requirement: O card e o perfil públicos levam a carta do Guerreiro(a) inteira

O núcleo SHALL devolver, em `/vitrine/guerreiros` e em `/vitrine/guerreiros/{nick}`, a
composição que a variante Guerreiro(a) do documento 11 §8.2 exige: **avatar**, **nick**,
**badges**, **poderes com o nível alcançado em cada um**, **desempenho** — a posição no ranking
público e os pontos regulares acumulados — e as **criações originais** creditadas a ele. A
projeção SHALL ser **a mesma nas duas rotas**: o que o card mostra é o que a página mostra,
resumido. (`RF-01-21`, `RF-01-28`, `RF-01-33`, `RN-01-10`, `RN-01-11`, documento 11 §§8.1, 8.2,
PRD-03 §9, decisão do fundador, 2026-09-28)

A composição SHALL sair **na própria listagem**, sem exigir de quem consome uma consulta por
nick para cada Guerreiro(a) exibido: a consulta por nick tem freio por origem, e montar uma
página de cards com ela seria barrado pelo próprio freio. (`RF-01-65`, `RN-01-27`)

O portão da divulgação SHALL continuar valendo sobre a composição inteira, e a projeção NEVER
SHALL ganhar campo de nome civil, nascimento, contato, imagem real, valor em reais ou
identificador interno de comunidade. A projeção **mínima** de avatar e nick SHALL continuar
sendo a das demais superfícies desta capacidade — a autoria creditada nas criações e o elenco
dos jogos —, que NEVER SHALL mudar por causa desta. (`RN-01-10`, `RN-01-11`, invariantes 8, 12
e 16 do documento 99 §6)

#### Scenario: O card traz a composição inteira

- **WHEN** uma consulta pública pede os Guerreiros e Guerreiras
- **THEN** cada item traz avatar, nick, badges, poderes com nível, desempenho e as criações
  originais creditadas a ele

#### Scenario: A página por nick traz a mesma composição

- **WHEN** uma consulta pública pede o perfil por nick exato de quem tem autorização vigente
- **THEN** a resposta traz a mesma composição que o card daquele Guerreiro(a)

#### Scenario: A composição sai sem consulta por nick

- **WHEN** uma consulta pública pede uma página inteira de Guerreiros e Guerreiras
- **THEN** a composição de todos eles vem naquela resposta, sem que outra consulta seja
  necessária

#### Scenario: O portão da divulgação vale sobre a composição

- **WHEN** um Guerreiro(a) não tem autorização de divulgação vigente
- **THEN** nem ele nem a composição dele aparecem em qualquer das duas rotas

#### Scenario: A composição não traz nada de pessoal

- **WHEN** qualquer das duas rotas responde
- **THEN** nenhum campo traz nome civil, nascimento, contato, imagem real nem valor em reais

#### Scenario: A projeção mínima das outras superfícies não muda

- **WHEN** uma criação original pública credita a autoria, ou o elenco dos jogos devolve um
  Guerreiro(a)
- **THEN** ele continua projetado como avatar e nick, sem a composição do card

## MODIFIED Requirements

### Requirement: Poderes, trilhas e criações originais respondem em leitura pública

O núcleo SHALL expor em rota pública o **catálogo de poderes** com as trilhas vinculadas a cada
um, e o **portfólio de criações originais** validadas. A criação original SHALL trazer a autoria
creditada, projetada como avatar e nick de **cada creditado** — os integrantes da equipe da
trilha, na modalidade em equipe, e o Guerreiro(a) que a entregou, na individual —, e
SHALL aparecer **apenas** quando todos os creditados nela tiverem autorização de divulgação
vigente. A trilha NEVER SHALL ser filtrada por comunidade nesta capacidade: ela é bem comum da
plataforma. (`RF-01-62`, `RF-01-26`, `RF-09-33`, `RN-01-13`, `RN-01-42`, `RN-09-19`, PRD-03 §9)

A criação original pública SHALL trazer também a **data de validação** e o **nome da trilha** de
que ela nasceu, que o portfólio público exibe junto da autoria. A criação original NEVER SHALL
trazer título: o modelo não tem esse campo, e nenhum documento-fonte o define. (`RF-03-08`,
decisão do fundador, 2026-09-28)

#### Scenario: Catálogo público traz poderes e trilhas

- **WHEN** uma consulta pública pede os poderes
- **THEN** a resposta traz cada poder com as trilhas vinculadas a ele

#### Scenario: Criação original pública credita a autoria

- **WHEN** uma criação original validada aparece no portfólio público
- **THEN** ela traz o avatar e o nick de cada integrante creditado

#### Scenario: Criação individual pública credita quem a entregou

- **WHEN** uma criação original individual validada aparece no portfólio público
- **THEN** ela traz o avatar e o nick do Guerreiro(a) que a entregou

#### Scenario: Criação com integrante sem autorização não aparece

- **WHEN** uma criação original tem entre os creditados um Guerreiro(a) sem autorização vigente
- **THEN** a criação não aparece no portfólio público

#### Scenario: Criação individual sem autorização não aparece

- **WHEN** uma criação original individual validada é de Guerreiro(a) sem autorização vigente
- **THEN** a criação não aparece no portfólio público

#### Scenario: A criação pública traz data e trilha

- **WHEN** uma criação original validada aparece no portfólio público
- **THEN** ela traz a data em que foi validada e o nome da trilha de que nasceu
