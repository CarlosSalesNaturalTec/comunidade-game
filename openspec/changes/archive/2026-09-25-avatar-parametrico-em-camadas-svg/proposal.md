# Proposal

**PRD de origem:** PRD-04 §6.1 e PRD-05 §6, aplicando o documento 15 §7.
**Cronograma:** linha `—` do bloco **Infraestrutura transversal (sem PRD)**.
**Identificadores atendidos:** `RF-04-07`, `RF-04-34`, `RF-05-23`. Nenhum identificador novo: a
rastreabilidade do `RF-04-07` (PRD-04 §15) já aponta para **15 §7 (avatar)**, e o que falta é
cumprir o que está lá.

## Why

O documento 15 §7 define o avatar do Guerreiro(a) como o **único retrato público** dele e fixa
quatro exigências: paramétrico em camadas SVG montado de catálogo fechado, cada traço com nome
dizível em português simples, composto no próprio aparelho sem rede, e sem marca de gênero no
traço. O §7.1 lista as **nove camadas** e o que varia em cada uma; o §7.2 fixa o **objeto
versionado** que o núcleo guarda; o §7.3 define o **avatar padrão do projeto**.

Nada disso existe. O que existe:

- No onboarding da App 01, um **campo de texto livre** — `caracteristicasDoAvatar` —, gravado com
  `JSON.stringify({ formaDeTratamento, caracteristicasDoAvatar })`. O objeto do §7.2 nunca é
  produzido, e uma criança de 6 anos dita características que ninguém desenha.
- **Nenhum renderizador**, em aplicação alguma. As telas que o documento 11 §8.2 manda exibir por
  avatar e nick — equipes da aula (`RF-04-34`), integrantes de atividade (`RF-05-23`) — não
  desenham avatar nenhum.

O invariante do documento 99 §6 diz que **Guerreiros e Guerreiras aparecem em público só por
avatar e nick**. Sem avatar desenhado, a metade que sobra é o nick — e a proteção que o invariante
descreve como "só avatar e nick" está cumprida por falta, não por desenho.

## What Changes

- `comum/` ganha o **catálogo fechado** das nove camadas do documento 15 §7.1, cada traço com o
  nome dizível em português que o §7 exige, e o **renderizador SVG** que as compõe na ordem da
  tabela.
- O **objeto versionado do §7.2** passa a ser o que a App 01 grava no campo `avatar`. Traço
  desconhecido **cai no padrão da camada** e nunca quebra a renderização, como o §7.2 manda — é o
  que faz os cadastros já existentes, com texto livre no lugar do objeto, renderizarem sem
  migração de dado.
- O **avatar padrão do projeto** (§7.3) ocupa o lugar de qualquer avatar que falte.
- No onboarding da App 01, o campo de texto livre dá lugar à **escolha no catálogo**
  (`RF-04-07`). A forma de tratamento continua campo próprio, como o §7 exige.
- As telas de equipe da App 01 (`RF-04-34`) e de integrantes da App 05 (`RF-05-23`) passam a
  **desenhar** o avatar ao lado do nick.
- **Sem rota nova e sem migração:** o núcleo guarda `avatar` como texto opaco — `Text`, anulável —
  e o objeto do §7.2 cabe ali sem alteração de modelo.

### Fora do escopo

- A **carta do personagem**, o emblema de nível, os badges e o glifo de poder: fatia própria,
  que depende desta.
- Adotar o avatar nas Apps 03, 06, 07 e 08 e no App 04: cada uma tem a sua tabela de exibição no
  documento 11 §8.2, e entra em fatia própria.
- O **avatar do Apoiador**, que é logomarca ou imagem escolhida, com piso de 10 moedas
  (documento 11 §8.2) — outro sistema, outra fatia.
- Crescer o catálogo além das nove camadas do §7.1.

## Capabilities

### New Capabilities

Nenhuma.

### Modified Capabilities

- `camada-visual-comum`: passa a entregar o avatar paramétrico — catálogo fechado, composição no
  aparelho sem rede, objeto versionado e avatar padrão do projeto (documento 15 §7).
- `aplicacao-da-aula-presencial`: o cadastro do onboarding passa a compor o avatar pelo catálogo,
  e as telas de equipe passam a desenhá-lo (`RF-04-07`, `RF-04-34`).

## Impact

- `comum/avatar/` — o catálogo, o renderizador e o avatar padrão.
- `comum/package.json` — a exportação da pasta nova.
- `apps/app-01-aula-presencial/src/onboarding/TelaDeCadastro.tsx` — a escolha no catálogo.
- `apps/app-01-aula-presencial/src/equipes/TelaDeEquipes.tsx` e
  `src/trilhas/EquipeDaTrilha.tsx` — o avatar desenhado.
- `apps/app-05-guerreiro/src/desafios/MinhasEquipes.tsx` e `src/carteira/MinhaCarteira.tsx` — o
  mesmo.
- Os testes das telas alteradas e do `comum`.
- `docs/03-plataforma-e-arquitetura.md` §1.2 — a linha de `comum/avatar/`.
- `docs/09-topicos-em-aberto-e-sugestoes.md` — a pendência da escolha por conversa.
- `openspec/cronograma-de-fatias.md` — a situação desta linha.
- Sem alteração no núcleo, em rota, em contrato de API ou em revisão de banco.
