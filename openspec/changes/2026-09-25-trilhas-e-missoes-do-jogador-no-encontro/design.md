# Design

## Context

Ver `proposal.md` — Why e Trava. A spec alterada é `aplicacao-da-aula-presencial`, em dois
requisitos existentes — a entrada do Guerreiro(a) e a tela inicial — e num requisito novo para o
percurso.

O que a App 05 já tem, e que esta fatia reusa: `Trilha`, `GuiaDaTrilha`, `Missao`, `Sondagem`,
`DesafioDeDesbloqueio` e `EscolhaDoPoder`, em `apps/app-05-guerreiro/src/trilha/`, sobre o cliente
`src/api/trilha.ts`. A `GuiaDaTrilha` já abre na missão atual e mostra a seguinte trancada, que é
exatamente o recorte desta fatia, e a `EscolhaDoPoder` já lista o catálogo e inscreve.

## Goals / Non-Goals

**Goals:**

- A presença registrada leva ao percurso, e a tela inicial também.
- O percurso é o da App 05, sem reimplementação.
- As atividades da aula aparecem pelas equipes do Guerreiro(a).

**Non-Goals:**

- Entrega individual da produção no encontro — o único ato individual da trilha que não entra.
- Lista inteira do percurso e distinção de missão realizada.
- Progresso, retomadas e culminância.
- Rota nova no núcleo.

## Decisions

1. **Os seis componentes promovidos vão para `comum/trilha/`, e a App 05 passa a consumi-los de
   lá.**
   Os `package.json` de `apps/*` declaram uma dependência de projeto só, `comum`; App 01 importar de
   `apps/app-05-guerreiro` não é possível sem inventar dependência entre aplicações, o que o
   documento 03 §1.2 não prevê. Promover é o que resta, e é o que o precedente de `MidiaDoNucleo`
   já fez quando duas aplicações precisaram do mesmo padrão.
   _Descartado:_ duplicar as telas na App 01 — duas cópias do percurso divergiriam na primeira
   correção. _Descartado:_ `comum/react/`, que é o contrato visual e de acessibilidade: tela de
   domínio ali apagaria a distinção.

2. **O cliente de API vai junto, na fatia que as telas usam.** As telas promovidas leem
   `listarMinhasTrilhas`, `obterMissaoNoPercurso`, `obterTrilhaPublica`, `lerArquivoDoConteudo` e
   `lerImagemDaPergunta`. Deixá-las recebendo os dados por prop empurraria a leitura para as duas
   aplicações e faria cada uma montar o mesmo encadeamento de chamadas.
   _Descartado:_ componentes sem cliente, alimentados por prop.

3. **A escrita entra como capacidade opcional dos componentes promovidos, e cada aplicação liga a
   sua.** `Missao` hoje monta `EntregaDaProducao` e `DesafioDeDesbloqueio`, que escrevem. A App 01
   liga o **desbloqueio** — que carrega a sondagem — e a **inscrição**, e **não** liga a entrega
   individual; a App 05 liga os três. O opcional deixa de ser "ligado na 05, desligado na 01" e passa
   a ser por ato, que é o que a decisão do fundador exige. _Descartado:_ dois componentes distintos,
   um de leitura e um de escrita — divergiriam no conteúdo, que é a parte grande e igual nos dois.
   _Descartado:_ um único interruptor de escrita — juntaria desbloqueio e entrega individual, que
   agora seguem caminhos diferentes.

4. **As atividades vêm de `GET /v1/eu/equipes`, não de `GET /v1/equipes/{id}/missao`.** A primeira
   devolve, por equipe, o `aula_id` e as atividades já montadas; a segunda exige saber a equipe
   antes. E a App 01 **não tem como saber** qual equipe da aula é a do Guerreiro(a): a lista da aula
   traz integrantes com avatar, nick e papel, sem identificador de persona, por exigência do
   `RN-04-14`. Deduzir pelo nick seria adivinhar o que uma rota já responde.
   _Corrige_ o que o cronograma previa, como o `config.yaml` manda fazer na própria change.

5. **O caminho novo entra como quinto caminho da entrada, com título próprio.** A fatia 18 deu à
   entrada a prop `caminho` e a de 2026-09-24 o mapa de títulos; o caminho das trilhas entra nos dois
   e na guarda de presença. Não entrar no mapa reproduziria o defeito de rótulo que aquela correção
   fechou.

6. **Nenhuma trilha inscrita leva ao catálogo de poderes, não a um aviso.** É o mesmo desfecho
   que a `Trilha` da App 05 já dá — sem inscrição, ela abre a `EscolhaDoPoder` —, e promovê-la
   traz esse comportamento junto. Feita a inscrição, o percurso abre na sondagem no mesmo
   atendimento, porque a inscrição devolve a trilha e a próxima missão dela vem do núcleo.
   _Descartado:_ avisar que inscrever-se acontece na App 05, que era o recorte antes da decisão do
   fundador de 2026-09-25 e deixaria sem porta quem não tem aparelho em casa.

7. **O delta da tela inicial já traz o parágrafo do glifo.** Esta change e a do temperamento Arena
   alteram o mesmo requisito, e um bloco `MODIFIED` substitui o requisito inteiro. Por isso a change
   da Arena **entra antes**: se esta entrasse primeiro, a spec afirmaria o glifo antes de os glifos
   existirem.

## Risks / Trade-offs

- **Aparelho compartilhado escrevendo no percurso de quem não está mais nele** → o desbloqueio grava
  sob a sessão do Guerreiro(a), que morre a cada atendimento (`RF-04-28`), e a `GuardaDePresenca`
  barra quem não tem presença. A janela é a do próprio atendimento, como já é na entrega por equipe.
- **Inscrição repetida criando duplicata** → a porta do núcleo devolve a inscrição existente sem
  erro (`RN-05-43`), e o cenário "A inscrição não se desfaz e não tem teto" o afirma. O aparelho do
  encontro é compartilhado e o toque repetido é esperado.
- **Promover tela de domínio para `comum/` alargar o que `comum/` é** → a pasta nasce separada de
  `comum/react`, e o documento 03 §1.2 recebe a linha que a descreve.
- **A App 05 regredir na promoção** → a fatia não muda comportamento dela; os testes dela ficam onde
  estão e passam a cobrir o componente promovido, e é isso que prova que a promoção não mudou nada.
- **Duas leituras por trilha no aparelho do encontro** → a `GuiaDaTrilha` já faz duas chamadas, uma
  para a missão atual e uma para a seguinte, e o encontro tem rede instável. É o comportamento que a
  App 05 já tem; nada nesta fatia o piora, e a indisponibilidade sem rede está no requisito.
