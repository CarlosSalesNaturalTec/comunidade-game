# Proposal

Origem: **PRD-04 — Aula presencial (App 01)**, fatia **25** do
`openspec/cronograma-de-fatias.md`. Identificadores alcançados: **`RF-04-71`** (encerramento da
sessão de trabalho na tela inicial) e **`RF-04-49`** (abertura e fechamento do momento de
troca). Nenhum identificador novo: a narração das telas não tem `RF`/`RN` no PRD-04 — entrou
pela fatia 23 direto do documento 15 §5.1 e do documento 03 §1.12 —, e a posição de um controle
na tela não é fixada por nenhum dos dois enunciados alcançados. A autoridade da parte da
narração é o **documento 15 §5.1**, que esta change altera; a decisão é do fundador, de
2026-10-14.

## Why

A tela inicial da App 01 acumulou três controles fora do menu que ela existe para apresentar, e
dois deles são de som. O "Iniciar a narração das telas" se sobrepõe a **qualquer** tela enquanto
a narração está ligada e não armada; o "Ligar/Desligar a narração das telas" mora na tela
inicial com uma frase de estado de duas linhas. São dois botões para o que a pessoa entende como
uma coisa só — som ligado ou desligado —, e o segundo é uma frase comprida justamente para quem
a narração serve: quem ainda não lê com fluência.

O par só existe porque a narração nasce ligada: o navegador não fala sem gesto da pessoa, então
alguém precisa armar o que já está ligado. Nascendo **desligada**, o clique que liga é o gesto, e
o segundo botão perde a razão de existir.

Ao mesmo tempo, "Encerrar a sessão de trabalho" ocupa o canto do cabeçalho — onde o polegar de
quem segura o aparelho encosta — e "Abrir o momento de troca" ficou num bloco solto abaixo do
menu, nenhum dos dois no padrão dos caminhos que a tela apresenta.

## What Changes

**Um controle de som só, de glifo, no canto do cabeçalho**

- O "Ligar/Desligar a narração das telas" e a frase `cg-narracao__estado` dão lugar a um
  **toggle só de glifo** no canto do cabeçalho da tela inicial. O estado é dito pela **forma** —
  alto-falante quando ligado, alto-falante cortado quando desligado — e por `aria-pressed`,
  nunca pela cor; o rótulo vai em `aria-label`.
- **BREAKING** A narração passa a **nascer desligada**, e a escolha **deixa de persistir** no
  `localStorage` do aparelho: vale entre atendimentos no mesmo carregamento e morre na recarga
  da aba. `CHAVE_DA_NARRACAO_NO_APARELHO` sai da interface pública de `comum/narracao`.
- **BREAKING** O estado `armada`, o `armarNarracao` e o controle de **iniciar** deixam de
  existir. O clique que liga é o gesto que o navegador exige, e sem arranque ligado nem
  persistência não há mais o estado "ligada e muda" que o controle de iniciar cobria.
- **BREAKING** A **fala sob toque** sai do liga e desliga: o controle de ouvir o conteúdo de
  missão em texto passa a depender apenas de o navegador oferecer síntese de fala. Com o
  arranque desligado, mantê-lo atrás do toggle tiraria a leitura do texto longo do app por
  padrão — de quem menos lê.
- A camada comum ganha um **botão de alternância só de ícone**, com rótulo acessível
  obrigatório: `Botao` sempre exigiu `children` textual.

**Encerrar e abrir a troca descem para o fim do menu**

- "Encerrar a sessão de trabalho" sai do canto do cabeçalho e "Abrir/Fechar o momento de troca"
  sai do bloco abaixo da lista. Os dois viram cartões no **mesmo padrão dos caminhos**, no fim
  do menu, sob o separador **"Para quem opera o aparelho"**, com **encerrar por último**.
- Quatro glifos novos: alto-falante, alto-falante cortado, **porta com flecha** (encerrar) e o
  da chave da troca — que não pode ser o glifo `troca` do caminho, porque com o momento aberto
  os dois cartões ficam encostados e têm funções opostas.

Nada muda em rota, entidade ou contrato do núcleo: a narração é do navegador, e as duas ações
que mudam de lugar continuam exigindo o que já exigiam — o PIN de quem abriu o aparelho e a
sessão de trabalho de um Mestre.

## Capabilities

### New Capabilities

Nenhuma.

### Modified Capabilities

- `narracao-por-sintese-de-fala`: o requisito do liga e desliga é reescrito — nasce
  **desligada**, o controle é de **glifo** com rótulo acessível, a escolha vale entre
  atendimentos mas não sobrevive à recarga, e o **gesto de armar deixa de ser um controle
  próprio**: o clique que liga é o gesto. O controle de ouvir o texto longo deixa de depender
  do liga e desliga.
- `aplicacao-da-aula-presencial`: o requisito do controle na tela inicial passa a descrever o
  toggle de glifo no cabeçalho, sem persistência entre recargas; o requisito "A App 01 arma a
  narração na primeira interação" é **removido**; o requisito do controle de ouvir o conteúdo
  em texto perde a condição "com a narração ligada"; e os requisitos do menu, do encerramento
  e do momento de troca passam a dizer onde os dois controles ficam.
- `camada-visual-comum`: a camada passa a entregar o **botão de alternância só de ícone**, com
  rótulo acessível obrigatório e estado dito por forma e por `aria-pressed`, dentro do que o
  requisito do ícone já exige ("rótulo textual visível **ou acessível**").

## Impact

**Documentação (mesmo PR)**

- `docs/15-identidade-visual.md` §5.1, a tabela: as linhas "Liga e desliga", "Primeiro áudio",
  "Onde mora o estado" e "Fala sob toque". A §5 fica como está — "rótulo textual visível **ou
  acessível**" já cobre o glifo, e dois glifos distintos cobrem "Nenhum significado por cor
  sozinha".
- `docs/09-topicos-em-aberto-e-sugestoes.md` §1: a decisão de 2026-10-14 entra em "Já
  decididos".
- `openspec/cronograma-de-fatias.md`: a fatia 25 do PRD-04, já acrescentada.
- `docs/prds/index.md`, `docs/99-mapa-de-referencias.md` e a `nav` do `mkdocs.yml`: intocados —
  nenhum arquivo novo em `docs/`, a situação do PRD-04 não muda e nenhuma relação entre
  documentos muda.
- O PRD-04 não é alterado: nenhum `RF`/`RN` dele muda de enunciado.

**Código** — alcance App 01 e `comum/`; só a App 01 monta `ProvedorDeNarracao`.

- `comum/narracao/ProvedorDeNarracao.tsx` e `comum/narracao/indice.ts`
- `comum/react/Icone.tsx` (quatro glifos na união `NomeDeGlifo`), o botão de ícone novo e
  `comum/react/estilos.css`
- `comum/react/Cabecalho.tsx`, para acolher o toggle no canto sem espalhá-lo às outras ~20
  telas que o montam
- `comum/trilha/Missao.tsx`, a guarda do controle de ouvir
- `apps/app-01-aula-presencial/src/inicio/TelaInicial.tsx`,
  `apps/app-01-aula-presencial/src/sessao-de-trabalho/AparelhoDaAula.tsx` e
  `apps/app-01-aula-presencial/src/index.css`

**Testes a ajustar** — citam os rótulos pelo nome acessível ou a chave do `localStorage`:
`inicio.test.tsx`, `troca.test.tsx`, `fila.test.tsx`, `sessao-de-trabalho.test.tsx`,
`precarga.test.tsx` e `quiz.test.tsx` na App 01; `comum/narracao/ProvedorDeNarracao.test.tsx`
(os casos de nascer ligada se invertem), `comum/react/narracao.test.tsx`,
`comum/react/Icone.test.tsx` (lista os glifos à mão) e `comum/trilha/trilha.test.tsx`.

**Esteiras**: Biome e Vitest em `apps/*` e `comum/`; markdownlint, Prettier, Lychee e MkDocs em
`docs/`. Nenhuma pasta de código nova, nenhuma esteira nova.

## Fora do escopo

O que o PRD-04 §3.2 já exclui, e além disso:

- A App 05 e as outras seis aplicações: nenhuma monta `ProvedorDeNarracao`, e `useNarracao`
  continua devolvendo a camada inerte nelas.
- Espalhar o toggle de som às demais telas da App 01: o documento 15 §5.1 o quer na tela
  inicial, que é a que aparece entre atendimentos.
- Rever o glifo dos caminhos que já existem, o avatar, a carta ou qualquer outra peça da
  camada visual.
