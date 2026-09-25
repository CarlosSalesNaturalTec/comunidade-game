# Proposal

**PRD de origem:** PRD-02 §10 e PRD-04 §10, aplicando o documento 15 §6.
**Cronograma:** linha `—` do bloco **Infraestrutura transversal (sem PRD)**.
**Identificadores atendidos:** `RF-04-01`, `RF-05-15`, `RF-05-16`. Nenhum identificador novo: os
três eixos já são norma do documento 15 §6.

**Depende** da change da **carta do personagem** — não há como a carta dominar a tela antes de a
carta existir.

## Dois insumos que o fundador fornece na implementação

A fatia precisa de duas coisas que não estão no repositório e que nenhum artefato do OpenSpec pode
decidir. Em 2026-09-25 o fundador declarou que **fornece as duas no momento da implementação** — não
são, portanto, perguntas pendentes de planejamento, e a change não espera por elas para ser
aprovada. Elas são a entrada das tarefas 2 e 3, que a tarefa 0 mantém como porta.

**1. As imagens de comunidade.** O documento 15 §6 dá à Arena "cor chapada e **imagem de comunidade
ao fundo**". Não há fotografia alguma no repositório. O fundador fornece as imagens e diz de onde
saem — acervo do projeto, foto da própria comunidade registrada na plataforma, ou ilustração no traço
do documento 15 §2 —, e a regra de uso de imagem de território é gravada no documento-fonte junto com
elas. O documento 11 §8.3 prevê "fotos e memórias registradas" como **dado** da Comunidade Virtual,
que é outra coisa: ali a foto é conteúdo exibido, aqui é fundo de interface.

**2. Quais fatos ganham retorno.** O §6 dá à Arena "**retorno de progresso e conquista**" a `300` ms,
sem enumerar os fatos. Os candidatos são conhecidos: missão desbloqueada, badge certificado, nível
que subiu, ponto creditado, produção entregue. É decisão de gamificação — documento 11 —, e quando o
fundador a der, ela é gravada lá antes de virar código.

**A tarefa 1 não depende de nenhuma das duas**: a carta dominando a tela precisa apenas da change da
carta.

## Why

A change do temperamento Arena escreveu a camada de tema e corrigiu a declaração das Apps 01 e 05,
mas deixou de fora os três eixos do documento 15 §6 que exigem conteúdo: ilustração em primeiro
plano com a carta dominando a tela, imagem de comunidade ao fundo e retorno de progresso e
conquista. Sem eles, a Arena é a Operação com outro raio: o temperamento existe para que a
aplicação da criança de 6 anos **não** se pareça com o painel de operação de um adulto, e é isso que
ainda não acontece.

## What Changes

- **A carta domina a tela** nas Apps 01 e 05: onde a Arena apresenta personagem, a carta é o
  elemento maior da tela, com uma decisão por tela — a densidade baixa que o §6 atribui à Arena.
- **Imagem de comunidade ao fundo**, atrás da cor chapada, sem jamais carregar significado sozinha e
  sem baixar o contraste medido do texto que fica sobre ela (§§3.3, 5).
- **Retorno de progresso e conquista** a `300` ms, com `ease-in-out`, nos fatos que o fundador
  declarar na implementação. O retorno **informa dado real** — é o que o princípio 2 exige, e é o que o distingue do
  movimento decorativo que a camada já proíbe. Suprimido por completo quando o aparelho pede menos
  movimento, e nunca a única via ao conteúdo.

### Fora do escopo

- As quatro aplicações do temperamento Operação, que não têm Arena nenhuma.
- Rotação da carta (documento 15 §8.1, "onde houver"): fatia própria, quando houver verso a mostrar.
- Ilustração de personagem — Susy, Otávio, Rôbróders, Trenell —, cujo universo segue **pendente** no
  documento 09 e não se decide aqui.
- A representação visual da Comunidade Virtual do documento 11 §8.3, que é dado da App 06.

## Capabilities

### New Capabilities

Nenhuma.

### Modified Capabilities

- `camada-visual-comum`: passa a declarar como a Arena põe a ilustração em primeiro plano, como a
  imagem de fundo entra sem ferir o contraste e como o retorno de progresso e conquista se distingue
  do movimento decorativo que a camada proíbe (documento 15 §§5, 6).

## Impact

- `comum/react/` e `comum/tokens.css` — o retorno de conquista e o que a imagem de fundo exige.
- `apps/app-01-aula-presencial/src/index.css` e `apps/app-05-guerreiro/src/index.css` — a composição
  da Arena.
- As telas das Apps 01 e 05 que apresentam personagem e progresso.
- `docs/15-identidade-visual.md` §6 e `docs/11-modelo-de-gamificacao.md` — onde as duas decisões do
  fundador são gravadas quando ele as der, com a linha correspondente no documento 09.
- `openspec/cronograma-de-fatias.md` — a situação desta linha.
- Sem alteração no núcleo, em rota ou em contrato de API.
