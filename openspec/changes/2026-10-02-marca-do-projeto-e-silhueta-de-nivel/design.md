# Design

## Context

Ver `proposal.md` — Why. O que o desenho precisa levar em conta:

- `comum/react/Cabecalho.tsx` é consumido pelas **oito** aplicações; mexer nele alcança todas.
- `comum/react/BadgeDaFamilia.tsx` já desenha as **seis** silhuetas do documento 15 §8.3, em
  grade de `24` px, com o glifo do poder dentro — e a de nível é o escudo.
- As sete aplicações servem hoje o **favicon do Vite**, o mesmo arquivo de 9,5 KB, em
  `apps/*/public/favicon.svg`. Nenhuma esteira o copia: as sete cópias estão versionadas à mão.
- `comum/fontes/` já guarda **Archivo** variável sob OFL 1.1, com procedência e licença ao lado.
- `comum/marca/**` já está fora do alcance do Biome, e a `LICENCA.md` já está escrita — as duas
  vieram da change `2026-09-30-heroi-e-gramatica-da-vitrine`.
- `comum/biometria/provisionamento.ts` já estabelece como um ativo de `comum/` chega ao
  `public/` de uma aplicação: função exportada que copia, chamada por um plugin do Vite na
  configuração de cada app.

## Goals / Non-Goals

**Goals:**

- Produzir a marca **sem encomenda externa**, resolvendo a procedência pelo que o repositório
  já licencia.
- Fazer a marca alcançar as oito aplicações de uma vez, pela camada comum.
- Liberar o escudo antes de a marca o usar — nunca depois.

**Non-Goals:**

- O elenco de personagens e o herói da vitrine — seguem na change do herói.
- A moldura do avatar em escudo — decidida, adiada para change própria.
- Qualquer alteração no núcleo.

## Decisions

### 1. O logotipo é tipográfico, em Archivo convertido em curvas

A família já está em `comum/fontes/`, sob OFL 1.1, com procedência datada. Converter glifos em
curvas dentro de um logotipo é uso permitido e **não** submete o logotipo à OFL — a cláusula de
_Reserved Font Name_ restringe redistribuir a **fonte** modificada, não o desenho que a usa.

Com isso a Família A deixa de ser insumo a esperar, e o §4 do manifesto — "quem desenhou,
quando, sob qual cessão" — se resolve em um parágrafo.

_Descartado:_ encomendar lettering original — custo e espera, para um ganho que a prancha de
decisão não mostrou.

### 2. O cabeçalho apresenta o símbolo, nunca a marca horizontal

A tabela do `comum/marca/README.md` destina `marca-horizontal.svg` ao cabeçalho, e o nome do
projeto também vai ali **em texto**, para não depender da imagem. As duas coisas juntas poriam
o nome duas vezes. Fica o símbolo, que não carrega o nome; a marca horizontal serve vitrine,
rodapé e documento.

_Descartado:_ marca horizontal no cabeçalho, com o nome só na imagem — fere o princípio 3.

### 3. A monocromática é em traço, e por isso é desenho próprio

Decisão do fundador de 2026-10-02, tomada sobre a prancha de comparação. A consequência é de
projeto: o §1 do manifesto afirma que a monocromática "não é desenho novo" e que a
implementação a deriva trocando preenchimento por `currentColor`. Com a versão em traço isso
deixa de valer — sólido e contorno são duas construções. O manifesto é corrigido nesta change.

_Descartado:_ monocromática cheia com o monograma vazado por máscara — lê melhor sobre foto,
mas não foi a escolhida.

### 4. A silhueta de nível vira losango

O escudo passa à marca, e a família de nível precisa de forma própria. O **círculo** seria o
candidato óbvio e está **vetado**: o documento 15 §9 o reserva à moeda — círculo de moeda e
ficha circular —, e o invariante 23 exige que ponto, ponto extra e moeda nunca se confundam na
tela. O losango é distinto das outras cinco a `24` px e comporta o glifo do poder no centro.

A troca entra **no mesmo PR** que o símbolo: entregar a marca antes criaria uma janela em que
marca e badge de nível são ambos escudo.

_Descartado:_ círculo (é da moeda); galhardete (primo do escudo, recria a confusão).

### 5. O favicon se provisiona como os modelos de biometria já se provisionam

Arquivo único em `comum/marca/favicon.svg`, copiado para `apps/*/public/` por função exportada
de `comum/marca/`, chamada por um plugin do Vite na configuração de cada aplicação — o mesmo
caminho de `provisionarModelosDeBiometria`, que já roda em `vite dev` e em `vite build`. A App
06 é Astro e aceita o mesmo plugin pela chave `vite` da configuração dela.

_Descartado:_ manter sete cópias versionadas à mão — foi assim que o favicon do Vite ficou em
todas sem ninguém notar.

### 6. Os parâmetros do desenho moram no documento 15, não aqui

Proporção do escudo, eixos do Archivo, degraus de cor e contrastes medidos são **decisão do
fundador** e descem ao documento 15, que é a fonte única da identidade visual. Os artefatos
desta change os aplicam e não os repetem.

## Risks / Trade-offs

| Risco | Mitigação |
| --- | --- |
| O logotipo furar o orçamento de 6 KB — são 15 glifos em curvas | Precisão de coordenada de 1 a 2 casas decimais, que é onde o orçamento se ganha; a tarefa confere o peso antes de gravar |
| O monograma não se distinguir a `16` px no favicon | O favicon é o símbolo com **afinação óptica própria** — monograma maior, margem mais apertada; confere-se no arquivo, não na prancha |
| Mexer em `Cabecalho` quebrar as outras sete aplicações | É dos componentes mais testados de `comum/`; a suíte das oito roda na mesma esteira |
| O contorno `marca-700` sumir contra o fundo escuro | No escuro quem entra é a monocromática, que herda a cor do texto; a colorida é do modo claro |
| A troca do losango invalidar teste existente de silhueta | O teste da silhueta roda junto, no mesmo PR |

## Open Questions

Duas declarações do fundador, que entram no documento 15 na implementação e **não** mudam
specs, abordagem nem tarefas:

- **Área de proteção** da marca, em múltiplos de alguma medida dela.
- **Tamanho mínimo** de uso. A prancha de decisão já dá a evidência — o símbolo lê a `16` px —,
  mas o número declarado é do fundador.
