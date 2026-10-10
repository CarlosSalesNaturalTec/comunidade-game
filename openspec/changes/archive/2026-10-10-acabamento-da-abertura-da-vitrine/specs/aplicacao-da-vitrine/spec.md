# Spec Delta

## MODIFIED Requirements

### Requirement: A abertura tem herói, com ilustração em primeiro plano

A abertura da vitrine SHALL apresentar, antes das seções, um **herói** com a ilustração
do elenco em primeiro plano, a frase que diz o que o projeto é, e as ações que a vitrine
já oferece — "Quero participar" e "Entrar". NEVER SHALL oferecer ação que a vitrine não
tenha em outra tela.

O "Entrar" **migra para o herói, e nunca se repete**: na tela que tem herói ele é do
herói, e o cabeçalho dessa tela NEVER SHALL trazer um segundo. Dois botões de mesmo nome
na mesma tela não acrescentam ação alguma e atrapalham quem navega por leitor de tela —
é a razão de 2026-10-09, e ela continua valendo; o que muda é **onde** o botão único
mora (decisão do fundador de 2026-10-10).

As duas ações SHALL ser apresentadas como um **par de iguais**: lado a lado, de mesma
altura, mesma forma e mesmo peso, distinguidas **por cor e por rótulo**, nunca por
tamanho. A distinção NEVER SHALL se apoiar só na cor — o rótulo de cada uma já a carrega.

O que o herói comunica NEVER SHALL depender da ilustração: some a ilustração — rede
fora, preferência do aparelho —, e a frase e as ações continuam de pé. A ilustração
NEVER SHALL entrar no caminho crítico da tela nem exigir recurso de domínio de terceiro.

A ilustração SHALL ser uma **composição**, e não quatro figuras em qualquer ordem: os dois
estudantes nas extremidades, e ao centro o professor ao lado da criatura que a mão dele
indica. A ordem NEVER SHALL mudar sem que a razão mude junto — o gesto do professor aponta
para o vazio se a criatura sair do lado dele.
(documento 15 §§1, 3.2, 6, 13.6; `RF-03-01`, `RF-03-51`, `RF-03-58`, `RN-03-21`; decisões
do fundador de 2026-10-10)

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

#### Scenario: Quem lê por leitor de tela ouve o elenco na ordem em que ele aparece

- **WHEN** a ilustração é alcançada por leitor de tela
- **THEN** ela é anunciada uma vez, como um grupo só, nomeando as quatro figuras na mesma
  ordem em que aparecem na tela

### Requirement: O botão "Entrar" fica sempre visível e pergunta qual persona está entrando

A App 06 SHALL manter o botão **"Entrar"** visível em toda tela pública, e ao ser acionado ele
SHALL perguntar **quem está entrando**, apresentando as personas que têm aplicação: Guerreiro(a),
responsável, Mestre, Apoiador, gestão e o **aparelho da aula**.

O botão SHALL ser **um só por tela**. Onde a tela tem herói, ele é do herói; onde não tem,
é do cabeçalho. Qualquer que seja o lugar, ele abre a mesma pergunta, com as mesmas
personas e sem escolha pré-marcada. (`RF-03-58`, PRD-03 §5.9; decisão do fundador de
2026-10-10)

#### Scenario: O botão está em toda tela

- **WHEN** o visitante está em qualquer tela pública da vitrine
- **THEN** o botão "Entrar" está visível

#### Scenario: Há um "Entrar" por tela, e não dois

- **WHEN** o visitante percorre as telas públicas da vitrine
- **THEN** cada tela traz exatamente um "Entrar" — no herói, quando a tela tem herói, e no
  cabeçalho, quando não tem

#### Scenario: O botão pergunta antes de encaminhar

- **WHEN** o visitante aciona "Entrar"
- **THEN** a vitrine pergunta qual persona está entrando, sem encaminhar ninguém antes da
  resposta

#### Scenario: A pergunta é a mesma venha o botão de onde vier

- **WHEN** o visitante aciona o "Entrar" do herói e, em outra tela, o do cabeçalho
- **THEN** as duas vezes a vitrine apresenta a mesma pergunta, com as mesmas personas e sem
  escolha pré-marcada
