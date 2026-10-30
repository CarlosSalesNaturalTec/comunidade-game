# Proposal

**Origem:** PRD-05 (Área do Guerreiro(a)), alcançando PRD-04 e PRD-03 pelas telas que montam a
mesma carta. **Fatia:** linha sem número no bloco "Infraestrutura transversal (sem PRD)" do
`openspec/cronograma-de-fatias.md`, onde já moram as fatias da carta, do avatar paramétrico e da
camada visual comum. **Identificadores atendidos:** `RF-05-82`, `RF-05-50`, `RF-05-51`,
`RF-04-67`, e `RF-03-06` com `RF-01-21` como não regressão. **Sem identificador novo**, pelo
precedente das fatias `2026-09-25-temperamento-arena-nas-apps-01-e-05` e
`2026-10-30-sankofa-no-escudo-e-contorno-mais-grosso`: decisão visual do fundador aplica os
documentos 11 §8.2 e 15 §§8.1, 9 e 11.1, e não cria requisito de produto.

## Why

A carta do personagem é o que a criança vem ver de si, e hoje ela se lê como ficha, não como
carta de jogo: tudo encostado à esquerda, as três listas em fluxo vertical único e nenhum
símbolo guiando a leitura. Decisão do fundador de 2026-10-30, elicitada em seis pontos.

Duas coisas estavam erradas antes do pedido, e esta fatia as conserta:

- O documento 11 §8.2 manda a carta do Apoiador ter o avatar **centralizado**, e o CSS nunca
  centralizou nada — `.cg-carta__avatar` tem largura de metade sem margem automática, nas quatro
  variantes.
- O `--cor-ponto-contorno` não tem valor no tema escuro, e o trio de estrelas da recompensa de
  marco perde a borda ali. Lacuna preexistente, registrada na fatia 10 do PRD-05.

E uma coisa faltava: o saldo que dá para trocar por recompensa avulsa só aparece na carteira, em
bloco de apoio abaixo da carta. Quem abre a Área para ver a própria carta não vê quanto tem para
trocar (`RF-05-82`).

## What Changes

- **Centralização** de avatar, identificação e frase de desempenho, nas **quatro** variantes da
  carta. Mestre, Apoiador e Comunidade Virtual recebem **só** isto.
- A frase de desempenho **continua frase** e ganha ao lado a **estrela cheia** da grandeza ponto
  regular do documento 15 §9. O traçado é extraído do `TrioDeEstrelas` para reuso, não duplicado;
  a estrela cheia **não** entra no `Icone`, que é `fill="none"` por força da §11.1 — e a §9 já é
  exceção declarada ali, para a ficha das grandezas.
- Na variante **Guerreiro(a)**, Poderes, Badges, Criações originais e a quarta seção viram
  **colunas**, com o **símbolo acima do rótulo** e o rótulo acima do conteúdo. **2×2** no celular
  e **4 em linha** a partir do marco de `768` px (documento 15 §4). O grid se ajusta ao número de
  seções presentes: na vitrine pública, onde a quarta não existe, são três.
- **Dois glifos novos** no `Icone`, na grade de `24` px da §11.1: **medalha** (retângulo
  arredondado com duas caudas de fita) para Badges e **pincel** para Criações originais.
  Reaproveitar silhueta de família de badge como cabeçalho de coluna está vedado — a silhueta diz
  a **família** (§8.3), e um losango ali afirmaria "badge de nível". Escudo e círculo também estão
  fora: são a marca (invariante 24) e a moeda (§9). Poderes usa o glifo `poder`, que já existe.
- **Quarta seção da carta do Guerreiro(a): o saldo de pontos extras que dá para trocar.** Só o
  `saldo_disponivel`, nunca o acumulado, com rótulo que diz ser o saldo — a §9 proíbe as duas
  contas aparecerem sem rótulo que as separe. Glifo: **estrela vazada**, que nasce pronta no
  `Icone`, em `currentColor`.
- **A quarta seção nunca aparece em superfície pública.** O campo entra opcional no tipo da
  variante e **fora** de `cartaEstaCompleta`, e a assimetria entre tela logada e superfície
  pública passa a ser regra escrita, não efeito de implementação.
- `--cor-ponto-contorno` ganha valor no tema escuro.

Sem rota nova e sem migração: `GET /v1/eu/pontos-extras` já existe e já recusa qualquer papel que
não seja o próprio Guerreiro(a) em sessão.

### Fora do escopo

- **A ficha (pastilha) das grandezas do documento 15 §9.** A carta não leva amarelo: medido,
  `ponto-500` como contorno de `2` px sobre `cal-000` dá `1,82:1`, e é por isso que a §3.3 mede
  `tinta-900` **sobre** `ponto-500`, nunca o inverso. A ficha segue onde a §9 a põe, na tela de
  troca.
- **O bloco de apoio da carteira da App 05.** Mantido com as duas contas e o aviso que explica a
  diferença. O saldo passa a aparecer duas vezes na mesma tela, com rótulos distintos — decisão
  expressa do fundador depois de a duplicação ser levantada.
- **O núcleo.** Nenhuma projeção pública ganha campo, nenhuma rota nasce, nenhuma tabela muda.
- O que o PRD-05 §3.2 já exclui do Ciclo 01 — acervo do Guerreiro(a), canal de sugestões e apoio
  escolar por assistente de voz — segue excluído.

## Capabilities

### New Capabilities

Nenhuma. A carta, os glifos e as fichas já são comportamento de `camada-visual-comum`.

### Modified Capabilities

- `camada-visual-comum`: a carta ganha alinhamento centralizado e, na variante Guerreiro(a), o
  grid de colunas com símbolo acima do rótulo; a frase de desempenho passa a levar a estrela cheia
  da grandeza; nasce a quarta seção da variante Guerreiro(a), opcional, fora da decisão de carta
  completa e **nunca** apresentada em superfície pública; o sistema de ícone ganha os glifos de
  medalha, pincel e estrela vazada.
- `area-do-guerreiro`: a carta do próprio Guerreiro(a) passa a mostrar também o saldo disponível
  de pontos extras, sem que a carteira deixe de mostrar as duas contas (`RF-05-82`).

## Impact

| Alcance | O que muda |
| --- | --- |
| `comum/react` | `CartaDoPersonagem.tsx`, `Icone.tsx`, `TrioDeEstrelas.tsx`, `estilos.css`, `indice.ts` e `carta.test.tsx` — cerca de 700 linhas apoiadas na estrutura atual |
| `comum/tokens.css` | `--cor-ponto-contorno` no bloco do tema escuro |
| `comum/carta` | `api.ts` lê `GET /v1/eu/pontos-extras`; `CartaDoGuerreiro.tsx` monta a quarta seção |
| App 05 | A carta da carteira passa a trazer a quarta seção; o bloco de apoio não muda |
| App 01 | O desfecho da presença herda a quarta seção, porque monta a mesma carta (`RF-04-67`) |
| App 06 | A carta pública recebe a centralização e o grid de três colunas, e **nunca** a quarta |
| Documentação | Documento 11 §8.2, documento 15 §§8.1, 9, 3.3 e 11.1, documento 09 §1, PRD-05 §9 e a linha desta fatia no cronograma |
| Esteiras | Biome e Vitest em `comum/` e nas Apps 01, 05 e 06; markdownlint, Prettier, Lychee e MkDocs porque toca `docs/` |

A ordem de execução importa: **os documentos-fonte primeiro**, depois o código. Decisão nova
nasce no documento normativo, nunca no artefato do OpenSpec — e o PR é um só, pelo precedente da
fatia 24 do PRD-04.
