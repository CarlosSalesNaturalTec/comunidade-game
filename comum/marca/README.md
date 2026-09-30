# A marca do projeto — o que entregar aqui

Esta pasta guarda a **marca** do Comunidade Game: logotipo, símbolo, submarcas e o
elenco de personagens. Ela é **constante da plataforma** — não varia por comunidade — e
por isso vive versionada aqui, e não no núcleo (documento 15 §12).

A marca é **reservada**: fica fora da AGPL e da CC BY-SA, e quem replica a plataforma
troca-a pela sua (documento 03 §1). A reserva mora em `LICENCA.md`, ao lado dos
arquivos, pelo mesmo motivo que a licença das fontes mora ao lado delas.

**Os arquivos ainda não chegaram.** Este documento é o manifesto do que entregar, e foi
escrito antes deles para que a entrega não precise de ida e volta.

## O que é regra e o que é recomendação

| | |
| --- | --- |
| **Regra** | O que os documentos 03 e 15 já fixam: formato vetorial sempre que couber, cor da paleta do §3, servir pelo próprio domínio, nada de terceiro em tempo de execução |
| **Convenção** | Pasta e nome de arquivo — definidos aqui, no padrão de `comum/fontes/`: minúsculas, hífen, português |
| **Recomendação** | Os orçamentos de peso e as grades de desenho abaixo. Derivados do princípio 4 do documento 15, que exige peso como requisito sem fixar número. Para virarem regra, precisam descer ao documento 15 |
| **Sua decisão** | Proporção, traço, área de proteção, tamanho mínimo e quais personagens são de uso público. Nenhum desses números está nos documentos, e nenhum se inventa aqui |

## 1. Marca do projeto

Todos em `comum/marca/`.

| Arquivo | Formato | Grade de desenho | Peso máximo | Para quê |
| --- | --- | --- | --- | --- |
| `marca-horizontal.svg` | SVG | altura `32`, largura livre | 6 KB | Cabeçalho das oito aplicações, modo claro |
| `marca-horizontal-mono.svg` | SVG, `currentColor` | idem | 4 KB | Modo escuro e uso sobre a foto de comunidade |
| `marca-empilhada.svg` | SVG | caixa `160 × 96` | 6 KB | Herói da vitrine e espaço vertical |
| `simbolo.svg` | SVG | `48 × 48` | 3 KB | Espaço curto, onde o nome não cabe |
| `simbolo-mono.svg` | SVG, `currentColor` | `48 × 48` | 2 KB | Idem, no escuro e sobre foto |
| `favicon.svg` | SVG | `48 × 48` | 2 KB | Aba do navegador das sete aplicações |
| `apple-touch-icon.png` | PNG opaco | `180 × 180` | 12 KB | Atalho em iOS, que não aceita SVG |

**Uma versão colorida e uma monocromática**, e não um par claro/escuro: a monocromática
usa `currentColor` e herda a cor do texto, então **um arquivo serve o modo escuro e o
uso sobre foto**. Um par claro/escuro dobraria os arquivos e deixaria o caso da foto sem
resposta.

O `favicon.svg` entra **uma vez** aqui e a esteira o copia para as sete
`apps/*/public/`. Hoje as sete servem o logotipo padrão do Vite — o mesmo arquivo de
9,5 KB, com filtros de desfoque —, e é isso que esta entrega substitui.

## 2. Submarcas

Em `comum/marca/`. As duas que o documento 09 nomeia.

| Arquivo | Formato | Grade | Peso máximo |
| --- | --- | --- | --- |
| `submarca-robroders.svg` | SVG | altura `32`, largura livre | 5 KB |
| `submarca-robroders-mono.svg` | SVG, `currentColor` | idem | 3 KB |
| `submarca-robo-educa.svg` | SVG | altura `32`, largura livre | 5 KB |
| `submarca-robo-educa-mono.svg` | SVG, `currentColor` | idem | 3 KB |

## 3. Elenco de personagens

Em `comum/marca/elenco/`. Os quatro que o documento 09 nomeia.

| Arquivo | Formato | Grade | Peso máximo |
| --- | --- | --- | --- |
| `susy.svg` | SVG | caixa `512 × 512` | 40 KB |
| `otavio.svg` | SVG | caixa `512 × 512` | 40 KB |
| `robroders.svg` | SVG | caixa `512 × 512` | 60 KB |
| `trenell.svg` | SVG | caixa `512 × 512` | 40 KB |

**Pose neutra, um arquivo por personagem.** Expressões, se vierem, seguem o mesmo nome
com sufixo — `susy-alegre.svg`, `otavio-pensativo.svg` — e não substituem a pose neutra.

**Por que SVG e não imagem:** o documento 15 §2 descreve o traço como *contorno grosso e
cor chapada*, que é precisamente o que vetoriza bem e escala sem peso. Se algum
personagem só existir em raster, entregue **AVIF** com fallback **WebP**, em `1024` px
de lado maior, até 120 KB cada — e diga qual, para a implementação prever `srcset`.

## 4. O que precisa vir junto, e não é arquivo

Sem estes quatro, a implementação não fecha o documento 15 §13:

1. **Área de proteção** da marca — em múltiplos de alguma medida dela, do seu jeito.
2. **Tamanho mínimo** de uso, em pixels, para o cabeçalho no celular.
3. **Quais personagens são de uso público.** A vitrine é pública e indexável.
4. **Procedência**: quem desenhou, quando, e sob qual acordo de cessão — a titularidade
   é da pessoa jurídica (documento 03 §1), e isso precisa estar registrado.

## 5. O que não entra aqui

| Isto | Vai para |
| --- | --- |
| A **foto de fundo** da comunidade | Núcleo — varia por comunidade (documento 15 §6.3). Pendente no documento 09 |
| Personagem como **cena de missão** | `conteudo-da-missao`, autorado pelo Mestre na App 09 |
| Ícone de interface | `comum/react/Icone.tsx`, que é código e já tem a grade do §11.1 |
| Avatar do Guerreiro(a) | `comum/avatar/`, que é paramétrico e composto em código (§7) |

## 6. Regras que valem para todo arquivo desta pasta

- **Nenhuma cor fora da paleta** do documento 15 §3. A monocromática não declara cor
  nenhuma: usa `currentColor`.
- **Nenhuma referência externa** — sem fonte de terceiro embutida, sem imagem
  referenciada por URL, sem `<script>`. O que a aplicação serve sai do próprio domínio
  (documento 15 §1, princípio 6).
- **SVG otimizado**: sem metadado de editor, sem camada oculta, sem filtro de desfoque.
  O favicon atual, do Vite, é o contraexemplo — 9,5 KB quase todos de `feGaussianBlur`.
- **Texto do logotipo em curvas**, nunca em `<text>`: fonte não instalada no aparelho
  quebraria a marca.
