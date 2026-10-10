# Spec Delta

## MODIFIED Requirements

### Requirement: A abertura tem herói, com ilustração em primeiro plano

A abertura da vitrine SHALL apresentar, antes das seções, um **herói** com a ilustração
do elenco em primeiro plano, a frase que diz o que o projeto é, e a ação que a vitrine
já oferece — "Quero participar". NEVER SHALL oferecer ação que a vitrine não tenha em
outra tela.

O herói NEVER SHALL repetir o "Entrar": ele é do cabeçalho, que fica acima e o põe em
toda tela pública (`RF-03-58`). Dois botões de mesmo nome na mesma tela não acrescentam
ação alguma e atrapalham quem navega por leitor de tela (decisão do fundador de
2026-10-09).

O que o herói comunica NEVER SHALL depender da ilustração: some a ilustração — rede
fora, preferência do aparelho —, e a frase e a ação continuam de pé. A ilustração
NEVER SHALL entrar no caminho crítico da tela nem exigir recurso de domínio de terceiro.

A ilustração SHALL ser uma **composição**, e não quatro figuras em qualquer ordem: os dois
estudantes nas extremidades, e ao centro o professor ao lado da criatura que a mão dele
indica. A ordem NEVER SHALL mudar sem que a razão mude junto — o gesto do professor aponta
para o vazio se a criatura sair do lado dele.
(documento 15 §§1, 6, 13.6; `RF-03-01`, `RF-03-51`, `RF-03-58`, `RN-03-21`; decisão do
fundador de 2026-10-10)

#### Scenario: A abertura apresenta o herói antes das seções

- **WHEN** a raiz do domínio é aberta
- **THEN** o herói aparece antes da primeira seção, com a frase do projeto e a ação
  "Quero participar", e o "Entrar" do cabeçalho segue sendo o único da tela

#### Scenario: Sem a ilustração, a abertura continua inteira

- **WHEN** a ilustração do herói não carrega
- **THEN** a frase e a ação continuam visíveis e acionáveis

#### Scenario: O herói não oferece ação que a vitrine não tenha

- **WHEN** o herói é apresentado
- **THEN** a ação dele é a mesma que a vitrine oferece em outra tela, e nenhuma outra

#### Scenario: O herói não busca recurso de terceiro

- **WHEN** a abertura é servida
- **THEN** nenhuma requisição sai para domínio que não seja o próprio

#### Scenario: A composição põe o professor ao lado da criatura que ele indica

- **WHEN** a ilustração do herói é apresentada
- **THEN** o professor ocupa a posição vizinha à da criatura, do lado para onde a mão dele
  aponta, e os dois estudantes ficam nas extremidades

#### Scenario: Quem lê por leitor de tela ouve o elenco na ordem em que ele aparece

- **WHEN** a ilustração é alcançada por leitor de tela
- **THEN** ela é anunciada uma vez, como um grupo só, nomeando as quatro figuras na mesma
  ordem em que aparecem na tela
