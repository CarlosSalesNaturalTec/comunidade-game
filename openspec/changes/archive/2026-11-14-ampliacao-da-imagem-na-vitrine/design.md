# Design

## Context

A ampliação já existe na camada comum: `MidiaDoNucleo` (`comum/react`) ganhou a propriedade
`ampliavel` em `2026-11-11-ampliacao-da-imagem-em-tela-cheia`, que embrulha a imagem num
`<button>` e a abre no `Dialogo` com `telaCheia` e `fecharAoTocarFora`, reaproveitando a URL de
objeto já montada. O contrato está nos specs `area-do-guerreiro` e `area-do-mestre`. Na App 06,
`portfolio/ProducaoDoAcervo.tsx` monta o `MidiaDoNucleo` com `semSessao` e sem `ampliavel`;
`linhaDoAcervo.tsx` o usa na seção do portfólio e na página do Guerreiro(a). A vitrine já carrega
`comum/react/estilos.css` pelo índice da camada comum, e `src/testes/configuracao.ts` já tem o
polyfill de `showModal`.

## Goals / Non-Goals

**Goals:**

- A imagem do acervo amplia como nas Apps 01, 05 e 09, com a mesma implementação.

**Non-Goals:**

- Pinça, arrastar ou zoom em degraus (decisão do fundador de 2026-11-11, que esta estende).
- Ampliar vídeo ou áudio; ampliar as figuras do herói da abertura, que são marca, e não
  produção do acervo.
- Trocar a cópia do polyfill da App 06 pelo módulo de `comum` — fora desta fatia.

## Decisions

1. **Ligar `ampliavel` em `ProducaoDoAcervo`, e só lá.** É o único ponto da App 06 que exibe
   imagem buscada do núcleo; as três fontes e os dois lugares da linha passam por ele. O
   componente já ignora `ampliavel` para vídeo e áudio. _Descartado:_ ligar por padrão no
   `MidiaDoNucleo` — tiraria das Apps o pedido explícito que a fatia 33 do PRD-04 escolheu.
2. **O rótulo e o título do diálogo seguem o `alt` atual** ("Produção de <título>"); nenhum
   texto novo.
3. **"Fechar a produção" e o "Fechar" do diálogo convivem.** O primeiro recolhe a linha; o
   segundo só fecha a ampliação. O diálogo modal cobre a página, então os dois nunca ficam
   acionáveis ao mesmo tempo.

## Risks / Trade-offs

- [Recolher a linha com a imagem ampliada] → impossível pela página: o `<dialog>` modal torna
  o resto inerte. O desmonte do `MidiaDoNucleo` revoga a URL e leva o diálogo junto.
