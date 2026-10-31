# Proposal

PRD de origem: **PRD-05 — Área do Guerreiro(a) (App 05)**, fatia **11** do
`openspec/cronograma-de-fatias.md`.

Identificadores atendidos: `RF-05-08` e `RF-05-17`. **Sem identificador novo** — é decisão
visual do fundador de 2026-10-31, pelo precedente de
`2026-09-25-temperamento-arena-nas-apps-01-e-05` e de
`2026-10-30-carta-em-colunas-e-saldo-para-trocar`.

## Why

A Área do Guerreiro(a) abre em `definirBloco("coleta")`, e a navegação dos quatro blocos é a
classe `cg-area-do-guerreiro__blocos` — **sem uma linha de CSS**, com `Botao` empilhados crus.
As duas coisas contrariam o `RF-05-08` e as §§5.2, 10 e 12 do PRD-05: quem entra cai na coleta
do território e tem de ir ao menu para chegar à missão, justo o que a §10 proíbe ao exigir a
tela inicial "sem exigir navegação por menu". É deriva **preexistente**, não regressão desta
fatia, e é aqui que ela se acerta.

O lado da trilha não precisa de nada novo: o `Trilha.tsx` já nasce em `tela = "guia"` e o
`GuiaDaTrilha` já diz o que fazer e o que a missão desbloqueia. Falta o padrão deixar de ser a
coleta — e os quatro caminhos ganharem a forma de cartão que a criança reconhece antes de ler
a frase inteira, como já acontece na tela inicial da App 01.

## What Changes

- O bloco padrão da Área do Guerreiro(a) passa de **coleta** para **trilha**, pondo em efeito
  o `RF-05-08` sem construir tela alguma.
- Os quatro caminhos passam a **cartão estilizado com frase**, em **grade 2×2 no celular e 4 em
  linha a partir do marco de 768 px**, com o **glifo acima do rótulo**. Quatro cartões com
  frase em coluna dariam ~24 rem e jogariam o Guia abaixo da dobra num aparelho de 360×640 —
  a mesma doença que a §10 quis curar.
- A **ordem** dos caminhos fica fixada em spec, e não é o acaso de quando cada fatia
  acrescentou o bloco: **minha carteira, Trilha, desafios e equipes, coleta do território**.
- O bloco corrente é marcado por `aria-current`. Os cartões são **navegação com item
  corrente**, não menu de destinos — e por isso a tela inicial não é o menu que o `RF-05-08`
  proíbe.
- O cartão da Trilha **nomeia a próxima missão**, sem rota nova: `GET /v1/eu/trilhas` já
  devolve `proxima_missao_titulo` e `proxima_missao_posicao`.
- `.cg-caminhos` e `.cg-caminho` **sobem** de `apps/app-01-aula-presencial/src/index.css` para
  a camada comum, como componente **`ListaDeCaminhos`** com `caminhoAtual` opcional, e a App 01
  passa a consumi-lo. `cg-caminhos__operacao` e `cg-caminhos__grupo` **ficam** na App 01: o
  `fieldset` "para quem opera o aparelho" é só dela.
- **Três glifos novos** no `Icone` — carteira, desafios e coleta; `trilhas` já existe.
- A App 01 fica **visualmente igual**: o componente serve as duas disposições, e a dela segue
  em coluna com o glifo ao lado. Do lado dela isto é refatoração, não mudança de
  comportamento.

## Capabilities

### New Capabilities

Nenhuma. A lista de caminhos é peça da camada visual comum, que já existe e já possui as
exigências de ícone, de alvo de toque e de marcação da área corrente; abrir capacidade nova
partiria ao meio um limite coeso.

### Modified Capabilities

- `camada-visual-comum`: requisito **novo** para a **lista de caminhos em cartão** — a
  disposição em coluna e em grade, o glifo acima do rótulo na grade, o alvo de toque, o rótulo
  em frase e a marcação do caminho corrente sem depender de cor. O requisito do ícone recebe os
  três glifos novos, com a mesma reserva que o da coluna da carta já declara: nenhum deles é
  silhueta de família de badge, escudo da marca, círculo da moeda nem estrela da grandeza
  ponto.
- `area-do-guerreiro`: o requisito "A App 05 abre na próxima missão do Guerreiro(a)" passa a
  dizer que a aplicação **abre no bloco da trilha**, e não apenas que o bloco da trilha abre na
  próxima missão quando alcançado. Requisito **novo** para a ordem dos quatro caminhos, a forma
  de cartão e a próxima missão nomeada no cartão da Trilha.

## Impact

| Alcance | O que muda |
| --- | --- |
| `comum/react` | `ListaDeCaminhos` (novo), `estilos.css` (recebe `.cg-caminhos`/`.cg-caminho`), `Icone.tsx` (três glifos), `indice.ts` (exporta o componente) |
| `apps/app-05-guerreiro` | `AreaDoGuerreiro.tsx` (tela inicial, ordem, padrão trilha, próxima missão no cartão), `index.css` (perde `cg-area-do-guerreiro__blocos`, que nunca teve CSS) |
| `apps/app-01-aula-presencial` | `TelaInicial.tsx` passa a consumir o componente; `index.css` perde `.cg-caminhos`/`.cg-caminho` e mantém `__operacao` e `__grupo` |
| Núcleo | **não muda** — nenhuma rota, nenhum modelo, nenhuma migração |
| Documentação | `openspec/cronograma-de-fatias.md` (situação e slug da fatia 11) e `docs/prds/index.md` apenas se a situação do PRD-05 mudar |

Pendências da §14 do PRD-05 — o catálogo de recompensa por marco e os preços do catálogo
avulso — **não tocam** este recorte.

### Fora do escopo

O que a §3.2 do PRD-05 já exclui, e que esta fatia não reabre: autoria de trilha, conteúdo e
desafio (App 09); lançamento de atividade, presença e mérito; Quiz ao Vivo; cadastro do próprio
Guerreiro(a) e captura da imagem (App 01); formação de equipe (App 01); execução da troca por
recompensa avulsa (App 01); acervo do Guerreiro(a), canal de sugestões e apoio escolar por
assistente de voz, todos a partir do Ciclo 02.

Acrescente-se, por serem decisões que o fundador não tomou e que esta fatia **não** antecipa: a
disposição da tela inicial da App 01, que segue em coluna; o lugar da saída da sessão na App 05,
que segue no cabeçalho como hoje; e a narração das telas, que a App 05 não provê.
