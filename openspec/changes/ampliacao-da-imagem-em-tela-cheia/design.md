# Design

## Context

A moldura fixa e o componente que a entrega, `MidiaDoNucleo` em `comum/react`, nasceram em
`2026-09-17-moldura-fixa-de-midia-na-missao`; o contrato está nos specs `area-do-guerreiro` e
`area-do-mestre`. O componente busca os bytes, monta a URL de objeto e a revoga ao desmontar. A
App 06 também o usa e fica de fora (proposal — Impact). `comum/react/Dialogo` já embrulha o
`<dialog>` nativo aberto por `showModal`, que prende o foco e fecha por `Esc`, com o botão
"Fechar" e a volta do foco a quem abriu.

A tela da programação da App 01 (`TelaDaProgramacao.tsx`) não usa o componente: põe
`conteudo.referencia` direto em `<img src>`/`<video src>`, o que não abre — a rota exige a chave
da aplicação em cabeçalho. O percurso do Guerreiro(a) na App 01 já usa `comum/trilha`, com
`MidiaDoNucleo`.

## Goals / Non-Goals

**Goals:**

- Uma única implementação da ampliação, dentro de `MidiaDoNucleo`, ligada por quem monta.
- A programação da App 01 no mesmo padrão de busca e moldura das outras telas.

**Non-Goals:**

- Pinça, arrastar ou zoom em degraus dentro da imagem ampliada (decisão do fundador).
- Ampliação de vídeo e de áudio; ampliação na App 06.
- Guardar a mídia para leitura sem rede (ver Risks).

## Decisions

1. **Ampliação opcional no `MidiaDoNucleo`, desligada por padrão.** Nova propriedade
   `ampliavel`; só vale com `tipo="imagem"`. As Apps 01, 05 e 09 a ligam em cada ponto de uso; a
   App 06 não muda uma linha. _Descartado:_ ligada por padrão com opção de desligar — mexeria na
   vitrine, que a decisão não alcança.
2. **O controle é um `<button>` em volta da imagem, com rótulo "Ampliar imagem: <alt>".** É o
   que dá teclado, foco visível e anúncio de controle por construção (documento 15 §5); a moldura
   de 320 × 240 já passa do alvo mínimo de toque. _Descartado:_ `onClick` no `<img>` — sem
   teclado nem papel acessível.
3. **A ampliação abre no `Dialogo` da camada comum, com variante de tela cheia.** `Dialogo`
   ganha duas propriedades opcionais: `telaCheia` (largura e altura até a janela, imagem em
   `contain` limitada a `100dvw` × o que sobra abaixo do cabeçalho) e `fecharAoTocarFora`
   (clique no próprio `<dialog>`, fora do corpo, fecha). O título do diálogo é o `alt` da imagem.
   Os diálogos existentes não passam nenhuma das duas e ficam como estão. _Descartado:_ um
   segundo componente de sobreposição — duplicaria foco, `Esc` e devolução do foco.
4. **A imagem ampliada reaproveita a URL de objeto já montada.** Nada é buscado de novo; a URL
   continua revogada na desmontagem do `MidiaDoNucleo`, que contém o diálogo.
5. **Na programação da App 01, imagem e vídeo passam por `MidiaDoNucleo` com
   `lerArquivoDoConteudo` de `comum/trilha/api`**, a mesma leitura que o percurso do
   Guerreiro(a) já faz no aparelho, e com a mesma trava de avançar enquanto carrega, cedendo na
   falha (padrão de `comum/trilha/Missao.tsx`). Arquivo de apoio e link não mudam.

## Risks / Trade-offs

- [Sem rede, a imagem de um conteúdo já visto não volta ao reabrir o item: a URL de objeto
  morre na desmontagem] → É o comportamento que as Apps 05 e 09 já têm, e não piora a
  programação de hoje, cuja imagem não abre nem com rede. Guardar bytes para leitura sem rede é
  escopo próprio, e vai ao fundador se for pedido.
- [`fecharAoTocarFora` fecharia o diálogo num clique dentro da imagem, se o alvo fosse
  confundido] → Fecha só quando o alvo do clique é o próprio `<dialog>` (o fundo), nunca a
  imagem nem o cabeçalho; o teste de `Dialogo` cobre os dois casos.
