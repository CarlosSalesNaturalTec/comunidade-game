# Design

## Context

A geometria das 59 formas do avatar são literais JSX dentro de `comum/avatar/Avatar.tsx`, montados
em memória a cada renderização. Nada é arquivo, e o que o núcleo guarda referencia só ids — o
contrato é o catálogo e as nove camadas, não o desenho. Ver `proposal.md` — Why.

Três limites moldam a solução, e nenhum deles se negocia aqui:

| Limite | De onde vem |
| --- | --- |
| Nove `<g data-camada>`, filhos diretos do `<svg>`, nessa ordem, para todo traço de toda camada | documento 15 §7.1, conferido em `avatar.test.tsx` |
| Nenhuma referência de rede no SVG, conferida por `not.toMatch(/https?:\|url\(/)` sobre o `outerHTML` | documento 15 §7 princípio 6 |
| `class`, `viewBox` e `width` iguais entre o avatar padrão do projeto e qualquer outro | documento 15 §7.3 |

A asserção do meio proíbe, do jeito que está escrita, **também a referência interna** —
`fill="url(#id)"`, `clip-path="url(#id)"`. Gradiente, máscara e `clipPath` ficam portanto fora, e o
desenho continua em preenchimento chapado.

## Goals / Non-Goals

**Goals:**

- Dez silhuetas de cabelo distinguíveis a 48 px, que é o tamanho em que o avatar aparece ao lado do
  nick.
- Toda escolha do catálogo visível no desenho, inclusive a cor do cabelo sob `raspado`.
- Acrescentar penteado sem escrever `path` à mão.

**Non-Goals:**

- Mudar a grade de `64`. Ela comporta o desenho novo; aumentá-la multiplicaria o diff sem ganho.
- Sobrancelha, que o catálogo não tem e que criaria dependência entre as camadas de olhos e de cor
  do cabelo.
- A moldura circular do avatar.

## Decisions

**A distinção vai para onde é visível, não para dentro do rosto.** O rosto é pintado depois do
cabelo, e as massas atuais cabem quase inteiras atrás dele: de `liso`, `trancas`, `dreads` e
`crespo-curto` aparecem 2 a 4 unidades de borda, e de `raspado`, nada. Os três lugares visíveis são
a silhueta fora do rosto, o comprimento fora do torso e a frente da testa. _Alternativa descartada:_
encolher o rosto para revelar mais cabelo — mexeria em todos os quatro formatos e em todas as
camadas por causa de uma.

**A peça da frente mora no grupo `rosto`, com `fill` próprio.** Com a ordem das nove camadas
travada, nenhum cabelo pode cair à frente da testa: a camada 3 vem antes da 5. Um `<g>` interno com
a cor do cabelo, depois da silhueta, resolve sem tocar a ordem nem criar camada. _Alternativa
descartada:_ décima camada — contraria o documento 15 §7.1 e migraria o objeto versionado.

**As orelhas passam da camada 2 para o grupo `rosto`.** Ficam no mesmo tom de pele e deixam de ser
cobertas pelo cabelo. A camada 2 continua existindo, com o pescoço. _Alternativa descartada:_
desenhar as orelhas por cima na camada 9 — misturaria pele com acessório.

**Lista declarativa de primitivas, não `path` escrito à mão.** Cada textura declara três listas —
massa, comprimento e frente —, e seis helpers (`elipse`, `circulo`, `caminho`, `bolhas`, `mecha`,
`contas`, `onda`, `traco`) as desenham. É o que faz `bolhas` servir ao black power, ao crespo curto
e ao cacheado com parâmetros diferentes, e o que torna o próximo penteado uma linha de dados.
_Alternativa descartada:_ dez `path` novos à mão — mesma dívida de hoje, só mais bem desenhada.

**O contorno da roupa é `var(--cor-superficie)`, não um token novo.** É o fio que as peças já usam
nos detalhes — o V da camisa, o capuz do moletom —, então acompanha o tema e não inventa cor. Só a
coincidência de cor entre fundo e roupa é problema, e ela tem quatro casos, não um.
_Alternativa descartada:_ recusar a combinação — o fundador decidiu que escolher as duas iguais
continua permitido.

**O realce do rosto é `rgba(255,255,255,0.22)`, não uma cor nova no catálogo.** Funciona sobre os
oito tons de pele sem acrescentar campo ao `TracoDoCatalogo`. _Alternativa descartada:_ um
`corDeRealce` por tom de pele — mais fiel, mas muda o catálogo, que esta fatia não toca.

**A composição de partida fica na tela, não no catálogo.** `escreverAvatar({ fundo: "acao-100" })`
na `TelaDeCadastro`. O `padrao` da camada continua `marca-100`, porque ele tem outra função: é onde
cai o traço desconhecido (documento 15 §7.2). _Alternativa descartada:_ trocar o `padrao` da camada
de fundo — mudaria junto o avatar padrão do projeto, que o documento 15 §7.3 fixa em cores da marca.

## Risks / Trade-offs

- **O avatar padrão do projeto continua com fundo e roupa da mesma cor** → o contorno da roupa
  devolve a silhueta a ele; recompor o padrão exigiria mudar o documento 15 §7.3 e o teste que o
  fixa, e fica fora desta fatia.
- **A peça da frente não está prevista no documento 15 §7.1**, que descreve a camada 5 como "Rosto,
  formato" → uma frase entra no §7.1 no mesmo PR, pelo precedente da fatia 24.
- **`bolhas`, `contas` e `onda` emitem dezenas de elementos por avatar** → são formas simples, sem
  filtro nem gradiente, e o avatar continua sem buscar nada; o custo é marcação, não rede.
- **Os quatro formatos de rosto têm silhuetas diferentes**, e uma peça da frente só serve aos
  quatro → ela é desenhada para transbordar levemente a silhueta, o que em cabelo é correto; os
  quatro formatos entram na verificação.

## Migration Plan

Não se aplica: nada é gravado a partir da geometria, e o objeto do documento 15 §7.2 não muda.
Avatares existentes passam a desenhar diferente na próxima carga, sem escrita no núcleo.
