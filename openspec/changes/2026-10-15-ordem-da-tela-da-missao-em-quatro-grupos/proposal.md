# Proposal

Origem: **PRD-04 — Aula presencial (App 01)**, **fatia 27** do
`openspec/cronograma-de-fatias.md`.

Alcança `RF-04-72`, `RF-04-73`, `RF-05-08` e `RF-05-10` a `RF-05-12`, **sem identificador
novo**: a ordem da tela da missão é apresentação, e nenhum enunciado a fixa. Mesmo molde
das fatias 25 e 26, que moveram caminhos da tela inicial pela mesma razão.

Decisão do fundador de **2026-10-15**.

## Why

A tela da missão empilha hoje, num fluxo só, o que a criança veio fazer e o que é
metadado: logo abaixo do conteúdo vem o **crédito e licença**, depois a **bibliografia**,
e só então o **ato** — a sondagem que abre a trilha ou o desafio de desbloqueio. A
**próxima missão** fica fora, depois da missão inteira, e na App 01 ainda vêm as
atividades do encontro e o acesso ao catálogo de poderes. Nada marca onde uma coisa acaba
e a outra começa, contra a densidade baixa que o documento 15 §6 pede da Arena.

O fundador decidiu agrupar: o conteúdo e o ato primeiro, depois o que se lê em seguida,
depois o encontro, e por último o rodapé. Quatro grupos, três linhas separadoras mudas.

Entra no caminho uma **dívida da fatia 21**: `comum/trilha` foi promovida sem a folha de
estilo, e as regras `cg-trilha__*` moram só em `apps/app-05-guerreiro/src/index.css`. A
App 01 importa apenas o `index.css` dela, que não tem nenhuma delas — o separador nasceria
visível na App 05 e invisível na App 01, que é justamente a aplicação que o pediu.

## What Changes

- A tela da missão passa a ter **quatro grupos**, nas duas aplicações: (1) o conteúdo e o
  **ato** — a sondagem ou o desafio de desbloqueio fica junto do conteúdo, acima da
  primeira linha; (2) `Próxima missão` e `Bibliografia`; (3) `Atividades do encontro`;
  (4) `Escolher outro poder` e `Crédito e licença`.
- A **bibliografia** passa a bloco recolhível de resumo neutro, como o crédito e a próxima
  missão já são, e segue **omitida quando a missão não tem bibliografia**.
- O **crédito e licença** deixa o fluxo de leitura da missão e passa ao **rodapé da tela**,
  recolhido e alcançável como hoje.
- A linha separadora é **muda**: não é anunciada e não carrega rótulo. Grupo que não tem
  conteúdo **não apresenta a sua linha** — não sobra separador sem nada entre ele e o
  próximo.
- `Escolher outro poder` passa a aparecer **somente onde é o único caminho ao catálogo de
  poderes**: na App 01 com **uma** trilha inscrita, onde a lista de trilhas é inalcançável;
  **nunca** na App 05, cuja tela de trocar de trilha sempre alcança o catálogo. Retirá-lo
  sem essa condição contrariaria `RF-04-74`, que não admite teto de inscrições: quem tem
  uma trilha só não chegaria à segunda pelo aparelho do encontro.
- Os quatro grupos valem também na **trilha sem próxima missão**, onde hoje a App 01
  perderia as atividades do encontro. Nesse caminho o **crédito passa a ser apresentado**,
  o que hoje não acontece — a trilha inteira é lida e a autoria dela não aparece, contra o
  invariante 5 do documento 99.

Segue fora do escopo o que o PRD-04 §3.2 já exclui e as fatias anteriores mantiveram: a
**culminância** da trilha, a **entrega individual** da produção — a desta aplicação é por
equipe (`RF-04-45`) — e a distinção entre missão realizada, liberada e bloqueada. Nenhuma
rota nova, nenhuma mudança no núcleo.

## Capabilities

### New Capabilities

Nenhuma.

### Modified Capabilities

- `aplicacao-da-aula-presencial`: o requisito do percurso do Guerreiro(a) e das atividades
  das equipes dele passa a fixar a **ordem em quatro grupos** com separador mudo, a
  bibliografia recolhida, o crédito no rodapé e a condição de `Escolher outro poder`.
- `area-do-guerreiro`: o requisito do conteúdo e da bibliografia da missão passa a fixar a
  mesma ordem — a bibliografia recolhida junto da próxima missão, e o crédito no rodapé em
  vez de logo abaixo do conteúdo.

## Impact

- `comum/trilha`: `GuiaDaTrilha` passa a buscar a trilha pública e a compor os quatro
  grupos; `Missao` perde a bibliografia e o crédito e fica com o conteúdo e o ato; nasce
  `comum/trilha/estilos.css`, importada pelo `indice.ts`.
- `apps/app-05-guerreiro/src/index.css`: devolve as regras `cg-trilha__*` à camada comum.
- `apps/app-01-aula-presencial`: a tela das trilhas passa `Atividades do encontro` como
  slot e decide quando oferecer `Escolher outro poder`.
- `apps/app-05-guerreiro/src/trilha/Trilha.tsx`: não oferece `Escolher outro poder` no
  guia; a tela de trocar de trilha mantém o dela.
- Testes das duas aplicações e de `comum/trilha` que afirmam a presença desses blocos.
- Sem efeito no backend, nas rotas e no MkDocs.
