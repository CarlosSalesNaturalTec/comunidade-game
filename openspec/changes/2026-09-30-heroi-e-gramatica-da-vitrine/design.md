# Design

## Context

Ver `proposal.md` — Why. O que o desenho precisa levar em conta:

- As fatias 9 e 10 já mergearam: a casca é Astro, a moldura da Arena está no layout, o
  palco está nas quatro páginas individuais e o glifo de poder está na seção de poderes.
- O que falta da Arena é **a ilustração**, e ela depende de arquivos que não existem.
- `comum/react/Cabecalho.tsx` é consumido pelas **oito** aplicações. Mexer nele alcança
  todas, e é o que o documento 09 registra como travado pela falta do logotipo.
- As sete aplicações servem hoje o **favicon padrão do Vite** — o mesmo arquivo de
  9,5 KB, com filtros de desfoque, em `apps/*/public/favicon.svg`.
- O documento 15 §12 já fixa que a marca mora em `comum/marca/`, versionada, e o
  documento 03 §1 que ela é reservada.

## Goals / Non-Goals

**Goals:**

- Fechar as três linhas de "não define" do documento 15 §13 e as três pendências
  correspondentes do documento 09.
- Deixar a marca alcançar as oito aplicações de uma vez, pela camada comum.
- Manter o piso: a ilustração não entra no caminho crítico.

**Non-Goals:**

- A foto da comunidade — pendência do documento 09, e decisão do fundador.
- O "como funciona" — sai em texto, publicado na App 03; nada a implementar.
- O registro da marca no INPI — ato jurídico, não código.
- Rota nova, ação nova ou tela nova.

## Decisions

### 1. Os arquivos são insumo, e o manifesto mora onde eles moram

`comum/marca/README.md` diz o que entregar — formato, dimensão, pasta e nome —, no molde
do `comum/fontes/README.md`, que já faz isso para as duas famílias tipográficas. Ele é
escrito **antes** dos arquivos justamente para que a entrega não precise de ida e volta.

A licença fica ao lado, em `comum/marca/LICENCA.md`, como o `OFL-archivo.txt` fica ao
lado das fontes: é o que faz quem clona o repositório descobrir que a marca não está na
AGPL (documento 03 §1).

### 2. Uma versão colorida e uma monocromática, e não um par claro/escuro

A monocromática usa `currentColor`, como o sistema de ícone do documento 15 §11.1: ela
herda a cor do texto que acompanha e, com isso, **um arquivo serve o modo escuro e o uso
sobre foto**. Um par claro/escuro dobraria os arquivos e ainda deixaria o caso da foto
sem resposta.

_Descartado:_ um SVG só, com `@media (prefers-color-scheme)` embutido — não resolve o
uso sobre foto, onde o que decide é a superfície e não o modo.

### 3. A marca entra por `Cabecalho`, e alcança as oito de uma vez

É o componente que as oito aplicações já montam. O nome do projeto **continua em texto**
ao lado dela: a marca nunca é a única via ao nome, que é o princípio 3 do documento 15
aplicado à própria marca.

_Descartado:_ marca por aplicação — oito lugares para manter, e o documento 15 §6 diz
que a marca não muda entre temperamentos.

### 4. O favicon é um arquivo só, copiado para as sete

A fonte é `comum/marca/favicon.svg`, e a esteira o copia para `apps/*/public/` no build.
Manter sete cópias à mão é sete oportunidades de divergir.

_Descartado:_ deixar cada aplicação com o seu — foi assim que o logotipo do Vite ficou em
todas sem ninguém notar.

### 5. O herói é composição, não componente novo

Ele é a ilustração, a frase e as duas ações que já existem, montados na abertura. Nada
de componente novo em `comum/`: o que a Arena precisa já está lá, e o herói é o arranjo
disso na primeira tela.

A ilustração fica **fora do caminho crítico** — `loading="lazy"` abaixo da dobra, ou
SVG embutido quando couber no orçamento —, e a frase e as ações são texto e botão, que
existem sem ela. É o princípio 3 do documento 15 aplicado ao herói.

### 6. Os testes seguem os três níveis

Nível 1: o herói apresenta a frase e as duas ações, e continua inteiro sem a ilustração;
o cabeçalho apresenta o nome em texto mesmo sem a marca. Nível 2, sobre o `dist/`: o
herói sai no documento servido, o favicon é o do projeto e nenhuma requisição a terceiro
entra com nada disso. Nível 3: nenhum.

## Risks / Trade-offs

| Risco | Mitigação |
| --- | --- |
| A ilustração pesar e furar o piso de rede | Orçamento declarado no manifesto; fora do caminho crítico; o nível 2 confere o que o documento carrega |
| A marca sobre foto perder contraste | Versão monocromática sobre superfície opaca, como a moldura já garante |
| Mexer em `Cabecalho` quebrar as outras sete aplicações | Ele é o componente mais testado de `comum/`; a suíte das oito roda na mesma esteira |
| Os arquivos chegarem fora do manifesto | O manifesto é escrito antes, e a tarefa 1.1 confere formato e nome antes de qualquer código |
| Esquecer um dos sete favicons | Arquivo único copiado pela esteira (decisão 4), com o nível 2 conferindo |

## Open Questions

Nenhuma que mude specs, abordagem ou tarefas. Duas ficam para o fundador **junto com os
arquivos**, e são declarações a registrar, não decisões técnicas:

- **Área de proteção e tamanho mínimo** da marca, que o documento 15 §13 cita como parte
  do que falta. Chegam com os arquivos e entram no documento 15.
- **Quais personagens são de uso público**, já que a vitrine é pública e indexável.
