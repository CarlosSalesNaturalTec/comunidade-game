# Design

## Context

Ver `proposal.md` — Why. O que o desenho precisa levar em conta:

- As fatias 9 e 10 já mergearam: a casca é Astro, a moldura da Arena está no layout, o
  palco está nas quatro páginas individuais e o glifo de poder está na seção de poderes.
- A **marca do projeto já entrou** pela change
  `2026-10-02-marca-do-projeto-e-silhueta-de-nivel`: `comum/marca/` existe, está declarada
  em `comum/package.json` e o cabeçalho das oito aplicações já a apresenta.
- O que falta da Arena é **a ilustração**, e ela depende do elenco, que não existe como
  arquivo.
- O documento 15 §12 já fixa que a marca mora em `comum/marca/`, versionada, e o
  documento 03 §1 que ela é reservada. `comum/marca/**` já está fora do alcance do Biome e
  a `LICENCA.md` já cobre o elenco nominalmente.

## Goals / Non-Goals

**Goals:**

- Fechar a linha de "não define" do documento 15 §14 sobre o **universo dos personagens**,
  e a pendência correspondente do documento 09.
- Manter o piso: a ilustração não entra no caminho crítico.

**Non-Goals:**

- A marca, o cabeçalho e o favicon — entregues pela change da marca.
- A foto da comunidade — pendência do documento 09, e decisão do fundador.
- O "como funciona" — sai em texto, publicado na App 03; nada a implementar.
- Rota nova, ação nova ou tela nova.

## Decisions

### 1. O elenco é insumo, e o manifesto mora onde ele mora

`comum/marca/README.md` §3 diz o que entregar — formato, grade e orçamento de peso, um
arquivo por personagem em pose neutra —, no molde do `comum/fontes/README.md`. Ele é
escrito **antes** dos arquivos justamente para que a entrega não precise de ida e volta.

O §3 do manifesto já prevê a rota alternativa: personagem que só exista em **raster** entra
como AVIF com reserva em WebP, a `1024` px de lado maior, e a implementação prevê `srcset`.
A escolha entre as duas rotas é empírica e se faz com os arquivos na mão.

A licença fica ao lado, em `comum/marca/LICENCA.md`, que já nomeia os quatro personagens.

### 2. O herói é composição, não componente novo

Ele é a ilustração, a frase e as duas ações que já existem, montados na abertura. Nada
de componente novo em `comum/`: o que a Arena precisa já está lá, e o herói é o arranjo
disso na primeira tela.

A ilustração fica **fora do caminho crítico** — `loading="lazy"` abaixo da dobra, ou
SVG embutido quando couber no orçamento —, e a frase e as ações são texto e botão, que
existem sem ela. É o princípio 3 do documento 15 aplicado ao herói.

### 3. Os testes seguem os três níveis

Nível 1: o herói apresenta a frase e as duas ações, e continua inteiro sem a ilustração.
Nível 2, sobre o `dist/`: o herói sai no documento servido e nenhuma requisição a terceiro
entra com a ilustração. Nível 3: nenhum.

## Risks / Trade-offs

| Risco | Mitigação |
| --- | --- |
| A ilustração pesar e furar o piso de rede | Orçamento declarado no manifesto; fora do caminho crítico; o nível 2 confere o que o documento carrega |
| Os arquivos chegarem fora do manifesto | O manifesto é escrito antes, e a tarefa 1.1 confere formato e nome antes de qualquer código |
| O personagem só existir em raster, e o vetor não fechar o orçamento | O §3 do manifesto já prevê AVIF com reserva em WebP, e a tarefa decide com os arquivos na mão |

## Open Questions

Uma, que fica para o fundador **junto com os arquivos**, e é declaração a registrar, não
decisão técnica:

- **Quais personagens são de uso público**, já que a vitrine é pública e indexável.
