## Why

Conserto da fatia sem número do PRD-09 (`openspec/cronograma-de-fatias.md`, "Moldura fixa de
mídia na missão", acrescentada em 2026-09-17). Atende `RF-09-25`, `RF-05-11`, `RF-05-12` e
`RF-09-119`. Relatado pelo fundador em 2026-09-17, elicitado em `/opsx:explore`.

**A pré-visualização da missão (App 09) não mostra a imagem da pergunta do quiz.** A seção de
sondagem/desafio de desbloqueio lê `pergunta.enunciado` e `pergunta.alternativas`, mas nunca
`pergunta.imagem_referencia` — mesmo a tela real do Guerreiro(a)
(`app-05/trilha/DesafioDeDesbloqueio.tsx`) já exibindo essa imagem. `RF-09-25` exige a missão
"como o Guerreiro(a) a verá"; hoje a pré-visualização mostra menos.

**Toda mídia servida em bytes pelo núcleo aparece sem moldura de tamanho.** Quatro pontos usam
o mesmo padrão — buscar os bytes com o token de sessão, montar `URL.createObjectURL` e exibir
em `<img>`/`<video>` — e nenhum tem `object-fit`, `max-width` fixo nem qualquer regra
equivalente em CSS: `comum/tokens.css` não tem token de tamanho de mídia. Uma imagem grande
enviada pelo Mestre estoura o layout tanto na pré-visualização quanto na tela real do
Guerreiro(a).

## What Changes

- `comum/tokens.css` ganha dois tokens novos — `--largura-de-miniatura` (320px) e
  `--altura-de-miniatura` (240px) — para a moldura fixa de mídia.
- Nasce `MidiaDoNucleo` em `comum/react`: componente único que busca os bytes de uma mídia do
  núcleo pelo token de sessão, monta e revoga a URL de objeto, aplica a moldura fixa
  (`object-fit: contain`, nunca `cover`) e trata carregando/erro — para imagem e para vídeo.
  Substitui as quatro implementações hoje quase idênticas.
- **App 09** (`apps/app-09-mestre/src/trilhas/`):
  - `PreVisualizacaoDaMissao.tsx` passa a exibir a imagem da pergunta do desafio de
    desbloqueio/sondagem, e o conteúdo da missão passa a usar `MidiaDoNucleo`.
  - `DesafioDeDesbloqueio.tsx` (edição) passa a usar `MidiaDoNucleo` para a imagem anexada à
    pergunta.
- **App 05** (`apps/app-05-guerreiro/src/trilha/`):
  - `Missao.tsx` passa a usar `MidiaDoNucleo` para o conteúdo da missão.
  - `DesafioDeDesbloqueio.tsx` passa a usar `MidiaDoNucleo` para a imagem da pergunta.

Fora do escopo:

- Miniatura clicável ou qualquer componente de ampliação — decisão do fundador de 2026-09-17.
- Faixa de bytes / streaming do vídeo grande — permanece servido inteiro, como hoje.
- Autorização das rotas `GET /v1/conteudos/{id}/arquivo` e da imagem da pergunta — já corretas,
  nenhuma muda.
- Unificar o crédito por nick (App 09) e por nome (App 05) — divergência já registrada e
  aceita noutra fatia.

## Capabilities

### New Capabilities

Nenhuma.

### Modified Capabilities

- `area-do-mestre`: a pré-visualização da missão passa a exibir a imagem da pergunta do
  desafio de desbloqueio/sondagem, e toda mídia exibida pela App 09 (conteúdo e imagem da
  pergunta, na pré-visualização e na edição) passa a ter moldura de tamanho fixo.
- `area-do-guerreiro`: toda mídia exibida pela App 05 (conteúdo da missão e imagem da pergunta
  do desbloqueio) passa a ter a mesma moldura de tamanho fixo.

## Impact

- **`comum/tokens.css`**: dois tokens novos, sem remover nem alterar nenhum existente.
- **`comum/react/`**: componente novo `MidiaDoNucleo`, exportado ao lado de `Aviso`, `Botao`
  etc.; teste novo.
- **App 09** (`apps/app-09-mestre/src/trilhas/`): `PreVisualizacaoDaMissao.tsx` e
  `DesafioDeDesbloqueio.tsx` passam a chamar `MidiaDoNucleo` em vez de reimplementar a busca de
  bytes.
- **App 05** (`apps/app-05-guerreiro/src/trilha/`): `Missao.tsx` e `DesafioDeDesbloqueio.tsx`,
  mesma troca.
- **Backend, contrato de API e migração**: nenhuma mudança — é fatia puramente de
  apresentação, sobre dados que o núcleo já serve.
- **Documentação**: nota dos dois tokens novos em `docs/15-identidade-visual.md` §12; a
  situação da linha desta fatia em `openspec/cronograma-de-fatias.md` passa de "proposto" para
  "implementado" ao fechar.
- **Esteiras**: `apps/app-09-mestre` e `apps/app-05-guerreiro` (Biome e Vitest), e
  documentação (markdownlint, Prettier, Lychee e MkDocs), porque a change toca `docs/15`.
