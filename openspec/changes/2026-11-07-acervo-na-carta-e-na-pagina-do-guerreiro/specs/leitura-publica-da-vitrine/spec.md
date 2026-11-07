# Spec Delta

## MODIFIED Requirements

### Requirement: O card e o perfil públicos levam a carta do Guerreiro(a) inteira

O núcleo SHALL devolver, em `/vitrine/guerreiros` e em `/vitrine/guerreiros/{nick}`, a
composição que a variante Guerreiro(a) do documento 11 §8.2 exige: **avatar**, **nick**,
**badges**, **poderes com o nível alcançado em cada um**, **desempenho** — a posição no ranking
público e os pontos regulares acumulados — e as **criações originais** creditadas a ele. A
projeção SHALL ser **a mesma nas duas rotas**: o que o card mostra é o que a página mostra,
resumido. (`RF-01-21`, `RF-01-28`, `RF-01-33`, `RN-01-10`, `RN-01-11`, documento 11 §§8.1, 8.2,
PRD-03 §9, decisão do fundador, 2026-09-28)

As **criações originais** da carta SHALL ser o **acervo público** do Guerreiro(a): a criação da
culminância e a comprovação do desafio prático, sob o **mesmo portão** do acervo da vitrine, em
ordem **decrescente** pela data de aprovação. Cada item SHALL ter o formato do item do acervo
— identificador, fonte, título, tipo, produção, trilha, data e autoria —, sem regra própria que
possa divergir dele. (`RF-03-86`, `RF-03-87`, `RN-03-41`, `RN-03-43`, decisão do fundador,
2026-11-07)

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

#### Scenario: A carta traz as duas fontes do acervo

- **WHEN** um Guerreiro(a) com autorização vigente tem uma criação da culminância validada e uma
  comprovação do prático julgada cumprida e publicável
- **THEN** as duas vêm nas criações originais da carta dele, nas duas rotas

#### Scenario: Comprovação fora do portão não entra na carta

- **WHEN** a comprovação do prático de um Guerreiro(a) não foi julgada, foi julgada não
  publicável ou é entrega presencial
- **THEN** ela não vem nas criações originais da carta dele

#### Scenario: O acervo da carta vem do mais recente ao mais antigo

- **WHEN** a carta de um Guerreiro(a) traz mais de um item do acervo
- **THEN** eles vêm em ordem decrescente pela data de aprovação do Mestre

#### Scenario: O item da carta é o item do acervo da vitrine

- **WHEN** um item aparece nas criações originais da carta e no acervo público
- **THEN** os dois trazem o mesmo identificador, fonte, título, tipo, produção, trilha, data e
  autoria
