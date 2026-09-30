# Design

## Context

Ver `proposal.md` — Why. O que o desenho precisa levar em conta:

- A fatia 9 já mergeou. A casca é Astro: `src/pages/` com rotas de arquivo,
  `src/layouts/Base.astro` e `Vitrine.astro`, e os componentes da App 06 como ilhas.
- Os cinco componentes desta fatia **já existem** em `comum/react` e são consumidos
  pelas Apps 01 e 05 desde 2026-09-25: `FundoDeComunidade`, `PalcoDoPersonagem`,
  `Icone`, `CartaDoPersonagem` e `RetornoDeConquista`.
- A capacidade `camada-visual-comum` já exige a Arena — ilustração em primeiro plano,
  carta dominando, imagem ao fundo, retorno de progresso —, mas dirigida à camada.
- `ComunidadeVirtual` não tem campo de foto, e nenhuma rota a serve. Pendência já
  registrada no documento 09.

## Goals / Non-Goals

**Goals:**

- Fechar a divergência entre a App 06 e o documento 15 §6, usando o que já existe.
- Deixar a moldura pronta para a foto entrar sem tocar na vitrine de novo.
- Gastar o orçamento que a fatia 9 liberou, sem afrouxar o piso.

**Non-Goals:**

- Herói e marca — fatia 11, travada nos arquivos do fundador.
- Trazer a foto da comunidade ao núcleo — pendência do documento 09, e decisão dele.
- Tocar em `comum/`, no núcleo ou nas outras sete aplicações.
- Trazer biblioteca de ilustração, de animação ou de ícone.

## Decisions

### 1. O fundo de comunidade entra pelo layout, não por tela

`Vitrine.astro` envolve o conteúdo em `FundoDeComunidade`, e com isso toda rota o recebe
de uma vez — inclusive as que ainda nem existem. É o que o §6 quer dizer com "do
cabeçalho ao rodapé": temperamento é da aplicação, não de região de tela.

O componente é **renderizado no build**, sem diretiva de cliente: ele não tem estado e
não busca nada. Não custa JS.

_Descartado:_ envolver tela a tela — a próxima rota nasceria sem a moldura, e nada
acusaria.

### 2. `imagem={null}`, como nas Apps 01 e 05

A foto não existe na plataforma. O componente contrata o caso: sem imagem, só a cor
chapada, e a tela é exatamente a mesma. Passar `null` é o comportamento correto hoje, e
é o que as outras duas aplicações da Arena já fazem.

_Descartado:_ pôr uma imagem do projeto como padrão — o §6.3 diz que **não há acervo de
fundo próprio do projeto**, e a foto é da comunidade ou não é nada.

### 3. O palco vale nas quatro páginas individuais, e não nas seções

`PalcoDoPersonagem` contrata **uma decisão por tela**, e a página individual cabe nisso:
a decisão é "Quero participar", e voltar é saída, no cabeçalho.

As seções de leitura — cards, ranking, portfólio, painel do território — **não** entram
no palco. O documento 15 §6 as declara Arena ao dizer "inclusive no painel do território
e nos rankings", e ao mesmo tempo dá à Arena a densidade de uma decisão por tela: as
duas frases só se conciliam se a densidade baixa governar a tela **que apresenta
personagem**, e o peso da Arena — carta grande, cor chapada, ilustração — governar o
resto. Forçar o palco numa tela de onze seções produziria onze telas ou uma tela mutilada,
e nenhuma das duas é o que o §6 pede.

_Descartado:_ quebrar o recorte em uma seção por tela — mudaria o `RF-03-02` e o
`RF-03-25`, que são requisito, não estilo.

### 4. O ícone entra onde há ação e estado, e o rótulo fica

O `Icone` acompanha; nunca substitui. Onde a vitrine hoje tem botão só com texto, o
glifo entra ao lado; onde tem estado, o glifo acompanha o numeral ou o rótulo que já
existe. Nenhum alvo de toque encolhe, e nenhum estado passa a depender do glifo — é o
princípio 3 do documento 15, que a camada comum já cumpre por construção.

### 5. O peso da Arena é CSS sobre os tokens, sem valor novo

Carta maior, cor chapada com mais presença, espaçamento da escala do §4. Tudo pela
camada semântica e a de tema, nunca pela primitiva (documento 15 §12). O tema da Arena
já fixa raio de `12` px e duração de `300` ms — a fatia consome, não redeclara.

O piso de rede continua: nenhuma imagem nova entra no caminho crítico, o movimento
respeita `prefers-reduced-motion` — que `comum/tokens.css` já zera —, e nada é buscado de
terceiro.

### 6. Os testes seguem os três níveis da fatia 9

Nível 1, no jsdom, sobre `TelaDaVitrine.tsx`: a página individual apresenta a carta e uma
decisão; o ícone não aparece sem rótulo. Nível 2, sobre o `dist/`: a moldura sai em toda
rota, e nenhuma requisição a terceiro entra com ela. A composição de teste precisa ganhar
a moldura junto com o layout, ou o nível 2 acusa a divergência — que é exatamente o que
ele existe para fazer.

## Risks / Trade-offs

| Risco | Mitigação |
| --- | --- |
| A moldura reduzir contraste do texto sobre ela | O componente já garante superfície opaca; o nível 1 confere o estado de foco |
| `TelaDaVitrine.tsx` desviar do layout ao ganhar a moldura | O nível 2 confere a moldura rota a rota sobre o `dist/` |
| O palco apertar a página individual, que tem portfólio e desempenho | Eles vão para `apoio`, abaixo e menor, que é o campo que o componente tem para isso |
| Peso extra na tela, contra o piso de rede | Nenhuma imagem nova; o que entra é CSS e SVG do próprio domínio |
| A foto nunca chegar, e a moldura ficar sem uso | Ela não fica: a cor chapada é o caso contratado, e a tela é a mesma |
