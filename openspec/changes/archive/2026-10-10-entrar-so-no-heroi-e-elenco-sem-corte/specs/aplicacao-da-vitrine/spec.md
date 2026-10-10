# Spec Delta

## MODIFIED Requirements

### Requirement: A abertura tem herói, com ilustração em primeiro plano

A abertura da vitrine SHALL apresentar, antes das seções, um **herói** com a ilustração
do elenco em primeiro plano, a frase que diz o que o projeto é, e as ações que a vitrine
já oferece — "Quero participar" e "Entrar". NEVER SHALL oferecer ação que a vitrine não
tenha em outra tela.

O "Entrar" da vitrine é **do herói, e só dele**: nenhuma outra tela pública o apresenta, e
o cabeçalho NEVER SHALL trazer um segundo. Dois botões de mesmo nome na mesma tela não
acrescentam ação alguma e atrapalham quem navega por leitor de tela (decisão do fundador de
2026-10-10).

As duas ações SHALL ser apresentadas como um **par de iguais**: lado a lado, de mesma
altura, mesma forma e mesmo peso, distinguidas **por cor e por rótulo**, nunca por
tamanho. A distinção NEVER SHALL se apoiar só na cor — o rótulo de cada uma já a carrega.

O que o herói comunica NEVER SHALL depender da ilustração: some a ilustração — rede
fora, preferência do aparelho —, e a frase e as ações continuam de pé. A ilustração
NEVER SHALL entrar no caminho crítico da tela nem exigir recurso de domínio de terceiro.

A ilustração SHALL ser uma **composição**, e não quatro figuras em qualquer ordem: os dois
estudantes nas extremidades, e ao centro o professor ao lado da criatura que a mão dele
indica. A ordem NEVER SHALL mudar sem que a razão mude junto — o gesto do professor aponta
para o vazio se a criatura sair do lado dele. As quatro SHALL aparecer **inteiras**, sem
corte nem redução de uma em relação às outras, do celular modesto ao aparelho largo.
(documento 15 §§1, 3.2, 4, 6, 13.6; `RF-03-01`, `RF-03-51`, `RF-03-58`, `RN-03-21`)

#### Scenario: A abertura apresenta o herói antes das seções

- **WHEN** a raiz do domínio é aberta
- **THEN** o herói aparece antes da primeira seção, com a frase do projeto e as ações
  "Quero participar" e "Entrar"

#### Scenario: O "Entrar" do herói é o único da tela

- **WHEN** a abertura é apresentada
- **THEN** existe exatamente um "Entrar" na tela, o do herói, e o cabeçalho não traz
  nenhum

#### Scenario: As duas ações se leem como um par de iguais

- **WHEN** o herói é apresentado
- **THEN** "Quero participar" e "Entrar" aparecem lado a lado, de mesma altura, forma e
  peso, e cada uma se identifica pelo próprio rótulo, sem depender da cor

#### Scenario: Sem a ilustração, a abertura continua inteira

- **WHEN** a ilustração do herói não carrega
- **THEN** a frase e as duas ações continuam visíveis e acionáveis

#### Scenario: O herói não oferece ação que a vitrine não tenha

- **WHEN** o herói é apresentado
- **THEN** cada ação dele é uma que a vitrine oferece em outra tela, e nenhuma outra

#### Scenario: O herói não busca recurso de terceiro

- **WHEN** a abertura é servida
- **THEN** nenhuma requisição sai para domínio que não seja o próprio

#### Scenario: A composição põe o professor ao lado da criatura que ele indica

- **WHEN** a ilustração do herói é apresentada
- **THEN** o professor ocupa a posição vizinha à da criatura, do lado para onde a mão dele
  aponta, e os dois estudantes ficam nas extremidades

#### Scenario: As quatro figuras aparecem inteiras, em qualquer largura de tela

- **WHEN** a abertura é aberta num visor estreito de celular ou num aparelho largo
- **THEN** as quatro figuras cabem na largura disponível, nenhuma é cortada na borda e a
  tela não ganha rolagem horizontal

#### Scenario: Quem lê por leitor de tela ouve o elenco na ordem em que ele aparece

- **WHEN** a ilustração é alcançada por leitor de tela
- **THEN** ela é anunciada uma vez, como um grupo só, nomeando as quatro figuras na mesma
  ordem em que aparecem na tela

## REMOVED Requirements

### Requirement: O botão "Entrar" fica sempre visível e pergunta qual persona está entrando

**Reason**: O enunciado exigia o botão em **toda tela pública**, e o fundador decidiu em
2026-10-10 que na vitrine ele existe **somente no herói** — logo, somente na abertura. O
requisito não é afrouxado nem abandonado: é substituído pelo que o situa, abaixo. A regra
de origem, no documento 03 §8, foi corrigida antes desta change, e o `RF-03-58` do PRD-03
acompanha.

**Migration**: Ver o requisito "O 'Entrar' é da abertura, e pergunta qual persona está
entrando" nesta mesma capacidade. Tudo que o requisito antigo exigia do **comportamento**
do botão — perguntar quem está entrando, apresentar as seis personas, não encaminhar antes
da resposta — continua exigido, sem exceção; o que muda é **onde** ele está.

## ADDED Requirements

### Requirement: O "Entrar" é da abertura, e pergunta qual persona está entrando

A App 06 SHALL apresentar o botão **"Entrar"** na **abertura**, dentro do herói, e NEVER
SHALL apresentá-lo em outra tela pública. Ao ser acionado ele SHALL perguntar **quem está
entrando**, apresentando as personas que têm aplicação: Guerreiro(a), responsável, Mestre,
Apoiador, gestão e o **aparelho da aula**.

Quem está em outra tela pública SHALL alcançar a entrada pela **marca do projeto**, que leva
à abertura em toda tela. (`RF-03-58`, PRD-03 §5.9, documento 03 §8; decisão do fundador de
2026-10-10)

#### Scenario: O botão está na abertura

- **WHEN** o visitante abre a raiz do domínio
- **THEN** o botão "Entrar" está visível, no herói

#### Scenario: Nenhuma outra tela pública traz o botão

- **WHEN** o visitante percorre os outros recortes e as demais telas públicas
- **THEN** nenhuma delas apresenta um "Entrar"

#### Scenario: A marca leva de volta à abertura

- **WHEN** o visitante está em outra tela pública e quer entrar
- **THEN** a marca do projeto, presente em toda tela, o leva à abertura, onde o "Entrar"
  está

#### Scenario: O botão pergunta antes de encaminhar

- **WHEN** o visitante aciona "Entrar"
- **THEN** a vitrine pergunta qual persona está entrando, sem encaminhar ninguém antes da
  resposta

#### Scenario: A pergunta apresenta as seis personas que têm aplicação

- **WHEN** a pergunta do "Entrar" é apresentada
- **THEN** ela oferece Guerreiro(a), responsável, Mestre, Apoiador, gestão e o aparelho da
  aula, sem escolha pré-marcada
