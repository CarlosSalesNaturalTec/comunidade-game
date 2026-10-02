# Proposal

Origem: a **linha transversal da marca** do `openspec/cronograma-de-fatias.md` — não é fatia
de PRD. Ela serve o cabeçalho das **oito** aplicações e mora em `comum/`, no molde já
praticado por `comum/fontes/`.

A change não fecha recorte de `RF`: executa decisões do fundador de **2026-10-02**, que
descem aos documentos 09 e 15 aqui, e corrige uma contradição interna do documento 15.

## Why

Três coisas estão paradas há tempo, e as três têm a mesma causa — a marca não existe como
arquivo.

**O documento 09 trava duas linhas.** "Logotipo e marca gráfica" e "Submarcas" seguem em
Decisões pendentes, e o documento 15 §13 as declara não definidas. O licenciamento e o lugar
já foram decididos — marca reservada, em `comum/marca/` —, e o manifesto do que entregar está
escrito em `comum/marca/README.md`. Faltava o desenho.

**As sete aplicações publicam marca de terceiro.** Todas servem hoje o favicon padrão do
Vite: o mesmo arquivo de 9,5 KB, quase todo de `feGaussianBlur`. Isso contraria o princípio 4
do documento 15 — peso é requisito — e põe a marca de outro produto num repositório que
reserva a sua (documento 03 §1).

**O cabeçalho não apresenta marca nenhuma**, nas oito.

E há uma quarta, que só aparece quando se decide o desenho: **o escudo já tem dono dentro do
sistema**. O documento 15 §8.3 dá o escudo à família de badge **de nível**, e o §8.4 diz que a
silhueta significa a família. Adotar o escudo como símbolo do projeto sem mexer nisso faria o
logotipo ser lido como badge de nível na mesma tela — forma é canal semântico declarado aqui
(invariante 24).

## What Changes

- **A marca entra em `comum/marca/`**: logotipo horizontal e empilhado, símbolo, favicon e as
  duas submarcas, cada um com a sua monocromática. Dez arquivos.
- **Eles são produzidos, não recebidos.** O logotipo e as submarcas são **Archivo em curvas**,
  família que o repositório já serve sob OFL 1.1 em `comum/fontes/`; o símbolo é desenho
  geométrico. Não há insumo externo a esperar, e a procedência fica resolvida.
- **O cabeçalho das oito passa a apresentar o símbolo**, com o nome do projeto em texto ao
  lado. Nunca a marca horizontal, que repetiria o nome.
- **O favicon das sete deixa de ser o do Vite**, a partir do arquivo único de `comum/marca/`.
- **A silhueta do badge de nível passa de escudo a losango**, liberando o escudo para a marca.
- **As decisões do fundador descem aos documentos**: duas linhas saem do documento 09 e do
  §13 do documento 15, e o corpo do documento 15 passa a declarar a construção da marca, a
  área de proteção e o tamanho mínimo.
- **O elenco não entra.** Susy, Otávio, Rôbróders e Trenell seguem na change
  `2026-09-30-heroi-e-gramatica-da-vitrine`, junto do herói que depende deles. A linha
  "Universo dos personagens" continua pendente no documento 09.
- **Nenhuma rota nova, nenhuma ação nova, nenhuma tela nova.**

## Capabilities

### New Capabilities

Nenhuma.

### Modified Capabilities

- `camada-visual-comum`: passa a declarar que o **cabeçalho apresenta a marca do projeto** nas
  oito aplicações, servida pelo próprio domínio, com versão para os dois modos e para o uso
  sobre foto, e nunca como única via ao nome; e o requisito das **silhuetas de badge** muda —
  a família de nível deixa o escudo, que passa a ser forma da marca, e nenhuma silhueta de
  badge se confunde com ela.

## Impact

| Alvo | Efeito |
| --- | --- |
| `comum/marca/` | dez arquivos novos, mais a procedência no `README.md` |
| `comum/marca/README.md` | corrige o §1: a monocromática é **em traço** e não se deriva da colorida |
| `comum/package.json` | `./marca` em `exports` e em `files` |
| `comum/react/MarcaDoProjeto.tsx` | componente novo: o símbolo e o nome, montado uma vez por aplicação |
| `apps/*/src/main.tsx` e `Vitrine.astro` | os sete pontos de montagem, um por aplicação |
| `comum/react/BadgeDaFamilia.tsx` | a silhueta `de_nivel` passa de escudo a losango |
| `apps/*/public/favicon.svg` | as sete trocam o favicon do Vite pelo do projeto |
| Núcleo | **nenhuma rota nova e nenhuma alteração** |
| `docs/15` | §8.3 muda a silhueta; §13 perde duas linhas; o corpo ganha a construção da marca |
| `docs/09` | duas pendências vão para "Já decididos" |
| `docs/99` | §§1 e 8, se a relação entre documentos mudar |

Fora do escopo: o **elenco de personagens** e o **herói da vitrine**, que seguem na change
`2026-09-30-heroi-e-gramatica-da-vitrine`; a **moldura do avatar em escudo**, decidida pelo
fundador e adiada para change própria; o **`apple-touch-icon.png`**, rasterizado do favicon
aqui e não desenhado; e o **registro da marca no INPI**, que é ato jurídico e não código.
