## Context

Ver `proposal.md` — Why. Quatro pontos já usam o mesmo padrão de leitura de mídia por bytes
(design — decisão 6 de `2026-09-16-leitura-da-culminancia-e-pre-visualizacao-fiel-da-missao`):
buscar com o token de sessão, montar `URL.createObjectURL`, exibir, revogar no unmount, tratar
erro sem travar a tela. Nenhum tem regra de tamanho, e o `design.md` daquela fatia já havia
adiado — por decisão do fundador — a extração de um componente comum para quando uma fatia
própria justificasse. Esta é essa fatia.

## Goals / Non-Goals

**Goals:**

- Dar moldura de tamanho fixo, igual, às quatro telas que hoje exibem mídia sem regra.
- Fazer a pré-visualização da sondagem/desbloqueio (App 09) mostrar a imagem da pergunta, que
  hoje falta.
- Extrair o padrão repetido para `comum/react`, resolvendo a divergência que a fatia anterior
  havia aceito como risco.

**Non-Goals:**

- Miniatura clicável, lightbox ou qualquer ampliação — decisão do fundador de 2026-09-17.
- Streaming por faixa de bytes do vídeo grande — fora desta fatia.
- Unificar o texto de erro/carregando entre as quatro telas além do que a extração naturalmente
  traz — cada persona mantém o tom que já usa quando for relevante.

## Decisions

### 1. Dois tokens novos em `comum/tokens.css`, ao lado da escala de espaço

`--largura-de-miniatura: 320px` e `--altura-de-miniatura: 240px`. Não reaproveito
`--espaco-*` (a escala vai só até 64px, para espaçamento, não para dimensão de mídia) nem
`--marco-*` (são larguras de viewport, não de componente). Dois tokens de tamanho de mídia são
categoria nova na camada semântica, análoga a `--largura-de-leitura`.

_Descartado:_ `max-width`/`max-height` sem altura fixa — a imagem alta continuaria a variar de
tamanho conforme a proporção, que é o problema original.

### 2. `object-fit: contain`, nunca `cover`

`cover` preenche a moldura cortando o excesso. Numa imagem de pergunta de quiz, o corte pode
esconder justamente o detalhe que a pergunta pede para observar — inaceitável. `contain` deixa
a imagem ou o vídeo inteiro visível, com friso (`--cor-campo-desabilitado` de fundo, borda 1px
`--cor-separador`, `--raio-campo`) quando a proporção não preenche a caixa.

### 3. `MidiaDoNucleo` nasce em `comum/react`, ao lado de `Aviso`/`Botao`/`MarcaDeGravacao`

Assinatura: recebe a função que busca os bytes (`(token: string) => Promise<Blob>`) — já
existem quatro dessas em `api.ts`/`trilha.ts` — o `tipo` (`"imagem" | "video"`), o `token` da
sessão, o `alt`/`rotulo` e o texto a mostrar quando a mídia não abre. Internamente resolve
buscar, montar e revogar a URL de objeto, aplicar a moldura da decisão 1–2, e mostrar
carregando/erro. As quatro chamadas hoje diretas passam a chamá-lo:

- App 09 `PreVisualizacaoDaMissao.tsx` — troca `ConteudoPreVisualizado` (conteúdo) e ganha a
  chamada nova para a imagem da pergunta, que hoje não existe ali.
- App 09 `DesafioDeDesbloqueio.tsx` — troca `ImagemDaPergunta`.
- App 05 `Missao.tsx` — troca `ConteudoDaMissao`.
- App 05 `DesafioDeDesbloqueio.tsx` — troca `ImagemDaPergunta`.

O texto e o link do conteúdo tipo `texto`/`link_externo` **não** passam por `MidiaDoNucleo` —
não são bytes buscados do núcleo, continuam como já estão em cada tela.

_Descartado:_ manter as quatro cópias e só acrescentar CSS em cada uma — repetiria a moldura em
quatro lugares e a pré-visualização da sondagem continuaria sem a imagem da pergunta até
alguém lembrar de replicar ali também; foi exatamente esse esquecimento que abriu esta fatia.

### 4. A pré-visualização ganha a imagem da pergunta pela mesma leitura que a edição já faz

`PreVisualizacaoDaMissao.tsx` já recebe `missao.perguntas_do_desbloqueio` com
`imagem_referencia` — só não a exibia. Passa a chamar `MidiaDoNucleo` com `lerImagemDaPergunta`,
a mesma função que `DesafioDeDesbloqueio.tsx` (App 09) já usa. Nenhuma rota nem contrato muda.

## Risks / Trade-offs

- **Moldura fixa em conteúdo muito vertical ou muito horizontal** → `contain` garante que nada
  é cortado; o friso nas bordas é o preço aceito por não cortar.
- **`MidiaDoNucleo` genérico demais para um caso futuro (ex.: arquivo de apoio, que é link, não
  mídia embutida)** → escopo desta fatia é só `imagem`/`video`; o arquivo de apoio continua
  como link direto em cada tela, sem passar pelo componente.
