# Proposal

Origem: **PRD-03 — Vitrine pública (App 06)**, **fatia 11** do
`openspec/cronograma-de-fatias.md`.

A fatia não fecha recorte de `RF`: é a última parte da correção de contradição com o
documento 15 §6, que as fatias 9 e 10 começaram. Atende ou preserva `RF-03-01`,
`RF-03-45`, `RF-03-51`, `RF-03-58` e `RN-03-21`.

> **A implementação espera os arquivos do elenco.** Eles são insumo do fundador, e o
> manifesto do que entregar — formato, dimensão, pasta e nome — está em
> `comum/marca/README.md` §3. Os artefatos ficam prontos para que, chegando os arquivos, o
> `/opsx:apply` não precise de mais nenhuma decisão.

## Why

A vitrine abre em `Cabecalho` — título, subtítulo e o botão "Entrar" — e cai direto na
navegação de recortes. Não há herói, não há primeiro plano, não há crescendo: as onze
seções entram todas com o mesmo peso, e a primeira coisa que o visitante lê é uma lista.

O documento 15 §6 dá à Arena **ilustração em primeiro plano**, e a fatia 10 entregou tudo
o que se podia entregar sem ilustração — a moldura, o palco, o glifo, o respiro. O que
falta é a ilustração, e ela depende do **elenco de personagens**, que o documento 15 §13
declara não definido e que o documento 09 mantém pendente.

É por isso que a vitrine "não parece o projeto": o documento 15 §2 declara o traço do
Gorillaz a **base** do sistema, e a base não existe como arquivo. A marca do projeto já
entrou pela change `2026-10-02-marca-do-projeto-e-silhueta-de-nivel` — logotipo, símbolo e
submarcas —, mas logotipo não é ilustração: sem o elenco sobra tipografia e cor, que é
exatamente o que está no ar.

## What Changes

- **Herói na abertura**: a primeira tela ganha ilustração em primeiro plano, a frase que
  diz o que o projeto é, e as duas ações que já existem — "Entrar" e "Quero
  participar". Nenhuma ação nova.
- **O elenco entra em `comum/marca/elenco/`**: Susy, Otávio, Rôbróders e prof. Carlos
  Trenell, em pose neutra, um arquivo por personagem, no orçamento do manifesto.
- **O "como funciona" não entra como código.** Decisão do fundador de 2026-09-30: ele
  sai em **texto**, como bloco de "Quem somos", no molde do bloco "Licenças" — o Admin
  publica e a seção exibe (`RF-03-45`). Nada a implementar.
- **Nenhuma ação nova, nenhuma rota nova, nenhuma decisão nova.**

## Capabilities

### New Capabilities

Nenhuma.

### Modified Capabilities

- `aplicacao-da-vitrine`: passa a declarar que a **abertura tem herói** — ilustração em
  primeiro plano, a frase do projeto e as ações que já existem —, e que o que ele
  apresenta nunca é a única via a informação alguma.

## Impact

| Alvo | Efeito |
| --- | --- |
| `comum/marca/elenco/` | pasta nova, com os quatro personagens e a procedência deles |
| `apps/app-06-vitrine/src/pages/index.astro` | recebe o herói |
| Núcleo | **nenhuma rota nova e nenhuma alteração** |
| Documentação | documento 15 §13 perde a linha do universo dos personagens; documento 09 move a pendência correspondente |

Fora do escopo, como o PRD-03 §3.2 já exclui: qualquer tela de login, cadastro ou área
restrita. Fora do escopo por pendência do documento 09: a **foto da comunidade**, que
segue sem existir. Fora do escopo desta fatia: a **marca do projeto**, o **cabeçalho** e o
**favicon**, entregues pela change `2026-10-02-marca-do-projeto-e-silhueta-de-nivel`; e o
**registro da marca no INPI**, que é ato jurídico da pessoa jurídica e não código.
