# Proposal

Origem: **PRD-03 — Vitrine pública (App 06)**, **fatia 10** do
`openspec/cronograma-de-fatias.md`.

A fatia não fecha recorte de `RF`: é **correção de contradição com o documento 15**, do
mesmo tipo da transversal `2026-09-25-temperamento-arena-nas-apps-01-e-05`. Os
identificadores que ela atende ou preserva são `RF-03-02`, `RF-03-03`, `RF-03-05`,
`RF-03-15`, `RF-03-51` e `RN-03-22`.

## Why

O documento 15 §6 é literal: *"o temperamento é da aplicação inteira: a App 06 é Arena do
cabeçalho ao rodapé, inclusive no painel do território e nos rankings"*. A tabela do
mesmo §6 define a Arena por **ilustração em primeiro plano, carta dominando a tela e cor
chapada com imagem de comunidade ao fundo**.

A App 06 declara `data-temperamento="arena"`, herda os tokens de raio e de duração e
consome corretamente só as camadas semântica e de tema. E para aí: não usa
`FundoDeComunidade`, que o §6.3 exige e que já existe em `comum/react`; não usa `Icone`;
não usa `PalcoDoPersonagem`, e por isso a carta não domina tela nenhuma. A vitrine tem o
chassi da Arena e nenhuma das qualidades dela — é tipografia e cor sobre fundo caiado.

A capacidade `camada-visual-comum` já obriga a Arena a pôr a ilustração em primeiro
plano, mas a obriga **na camada**: nada exige que a App 06 a use, e é por isso que a
divergência atravessou oito fatias sem acusar.

O piso de rede e de aparelho **não é afrouxado** (documento 15 §1, princípio 4; PRD-03
§10; reafirmado pelo fundador em 2026-09-30). O que a fatia 9 deixou de baixar em JS é o
que paga o peso desta.

## What Changes

- **Fundo de comunidade em toda tela pública**, pelo layout: a cor chapada ganha a
  moldura que o §6.3 define, com os pisos de contraste medidos sobre superfície opaca e
  nada se perdendo quando a imagem não carrega.
- **A carta passa a dominar as quatro páginas individuais** — Guerreiro(a), Mestre,
  Apoiador e comunidade — por `PalcoDoPersonagem`: a apresentação em primeiro plano, uma
  decisão só, e o resto abaixo e menor.
- **O sistema de ícone entra**, onde hoje há ação e estado sem glifo. O ícone nunca
  aparece sozinho, e nenhum estado passa a se comunicar só por ele.
- **Peso de Arena nos cards e nas seções**: o que o §6 chama de densidade baixa, aplicado
  ao que a vitrine já apresenta — sem transformar as seções de leitura em telas de uma
  decisão, que o próprio §6 ressalva ao dizer que painel e ranking também são Arena.
- **Nenhum requisito novo, nenhuma rota nova, nenhuma decisão nova.** `comum/` não muda:
  os cinco componentes já existem.

### A foto da comunidade continua `null`

O `FundoDeComunidade` recebe o endereço da foto, e **a foto não existe na plataforma**:
`ComunidadeVirtual` não tem campo de foto e nenhuma rota a serve. É pendência **já
registrada** no documento 09, e é por isso que as Apps 01 e 05 passam `null` desde
2026-09-25.

Esta fatia faz o mesmo, e é o comportamento que o próprio componente contrata:
*"comunidade que não escolheu foto não ganha fundo nenhum — e a tela é exatamente a
mesma"*. Entrega a moldura; a foto entra sem tocar na vitrine no dia em que a pendência
do documento 09 for decidida.

## Capabilities

### New Capabilities

Nenhuma.

### Modified Capabilities

- `aplicacao-da-vitrine`: passa a declarar que **a vitrine aplica a Arena** — fundo de
  comunidade, carta dominando a página individual e ícone acompanhando ação e estado.
  Hoje a capacidade descreve o que cada tela mostra e, desde a fatia 9, como ela é
  servida, mas nada sobre o temperamento; a obrigação existe só em `camada-visual-comum`,
  dirigida à camada, e foi essa brecha que deixou a App 06 divergir do documento 15 §6
  por oito fatias sem nenhum teste acusar.

## Impact

| Alvo | Efeito |
| --- | --- |
| `apps/app-06-vitrine/src/layouts/Vitrine.astro` | recebe o fundo de comunidade |
| `apps/app-06-vitrine/src/guerreiros/`, `adultos/`, `territorio/` | as quatro páginas ganham palco |
| `apps/app-06-vitrine/src/index.css` | peso de Arena nos cards e nas seções |
| `comum/` | **não muda** — os cinco componentes já existem |
| Núcleo | **nenhuma rota nova e nenhuma alteração** |
| Documentação | nenhuma decisão nova; fecha a linha da fatia 10 no cronograma |

Fora do escopo desta fatia, pelo cronograma: o **herói** e a **marca**, que são da fatia
11 e dependem dos arquivos do fundador. Fora do escopo por pendência do documento 09: a
**foto da comunidade**. Fora do escopo, como o PRD-03 §3.2 já exclui: qualquer tela de
login, cadastro ou área restrita.
