# Design

## Context

Ver `proposal.md` — Why. O que o desenho precisa levar em conta do código de hoje:

- A App 06 tem 88 arquivos, 26 deles de teste. A casca — `index.html`, `App.tsx`,
  `main.tsx`, `src/navegacao/*`, `vite.config.ts` — é o que sai; os cerca de sessenta
  componentes ficam.
- Só sete arquivos tocam API de navegador fora dos testes, e seis deles são
  legitimamente de cliente (navegação, diálogo, chat do Desenvolvedor, rotação de
  cards). O sétimo, `institucional/SecoesInstitucionais.tsx`, usa
  `window.location.hash` apenas para rolar até a âncora.
- `src/api/leituras.ts` são funções que devolvem `Promise` sobre `comum/api`. Não
  dependem de navegador: rodam em Node, no build.
- `comum/tokens.css` e `comum/fontes.css` são CSS puro, e `comum/react` é React. A
  camada comum **não muda**.

## Goals / Non-Goals

**Goals:**

- Cumprir a fronteira de entrega das specs deste delta com a fronteira **declarada em
  arquivo**, não em condicional de código: a rota diz o que ela é.
- Reusar os componentes existentes como ilhas, sem reescrevê-los.
- Deixar a App 06 mais leve do que entrou, para a fatia 10 ter orçamento.

**Non-Goals:**

- Mudar qualquer endereço público, contrato de rota do núcleo ou comportamento de tela.
- Tocar em `comum/`, no núcleo ou nas outras sete aplicações.
- Trazer biblioteca de roteamento, de UI ou de gráfico.

## Decisions

### 1. Astro com `output: 'static'` e `@astrojs/react`

O documento 03 §1, princípio 13, já decidiu Astro, e o mesmo princípio exige **saída
estática servida pelo Firebase Hosting, sem runtime de servidor**. `@astrojs/react`
renderiza os componentes existentes; os que precisam de interação recebem diretiva de
cliente.

_Descartado:_ manter Vite e acrescentar passo de pré-renderização — mais cola para
chegar onde o Astro já chega, e contra o documento 03.

### 2. A fronteira vive no mapa de rotas

| Rota | Entrega | No `sitemap.xml` |
| --- | --- | --- |
| `/` | estático; ilhas para cards rotativos e ranking | sim |
| `/o-que-coletamos` | estático inteiro | sim |
| `/quero-participar` | estático; ilha para necessidades em aberto | sim |
| `/comunidades/[id]` | casca estática por `getStaticPaths`; painel em ilha | sim |
| `/participar`, `/solicitar-dados` | casca estática; formulário em ilha | não |
| `/desenvolvedor`, `/apresentar-url` | casca estática; assistente em ilha | não |
| `/guerreiros/[nick]`, `/mestres/[id]`, `/apoiadores/[id]` | ilha inteira, `noindex` | não |

A ilha recebe `client:load` quando é a razão da tela (formulário, assistente, página de
pessoa) e `client:visible` quando é seção abaixo da dobra (cards, ranking,
necessidades) — é o que devolve orçamento de rede sem afrouxar nada.

### 3. As páginas de pessoa saem por uma casca `noindex`, não por rota estática

Saída estática não tem rota dinâmica sem caminhos, e gerar caminho por pessoa é
exatamente o que a spec proíbe. Então: um único `src/pages/app.html.astro` — casca com
`<meta name="robots" content="noindex">` que lê o caminho no aparelho e monta a página
de pessoa —, e o `firebase.json` reescreve `/guerreiros/**`, `/mestres/**` e
`/apoiadores/**` para ela, com `X-Robots-Tag: noindex` nos mesmos caminhos.

O cabeçalho vai junto da etiqueta porque agente que não executa script lê o cabeçalho e
não leria a etiqueta. O `robots.txt` também barra `/app.html`, para a própria casca não
ser indexada.

O `rewrite` `**`, hoje a rota de tudo, passa a apontar para essa mesma casca e a valer
só para o que não tem arquivo: o Firebase Hosting serve arquivo real antes de aplicar
`rewrite`. É o que atende comunidade criada depois da última publicação — ela abre pela
casca e ganha arquivo próprio na publicação seguinte.

_Descartado:_ reescrever `**` para `/index.html`, como hoje — serviria o conteúdo da
abertura no endereço de uma pessoa.

### 4. O que é buscado no build, e o que acontece se o núcleo não responder

No build: o conteúdo institucional e a lista de comunidades, com as leituras de
`src/api/leituras.ts` rodando em Node. Em ilha, na visita: tudo o que a spec exige
fresco.

**Núcleo fora do ar no build derruba o build.** Publicar a vitrine com o institucional
vazio é pior do que não publicar: a spec exige que o documento servido traga o conteúdo
publicado, e uma página indexada vazia é pior do que uma não indexada. O deploy já
depende de rede para publicar no Firebase.

_Descartado:_ publicar casca vazia e buscar no cliente — indexaria página sem conteúdo,
que é o defeito que esta fatia existe para corrigir.

### 5. O `sitemap.xml` é escrito à mão, num endpoint

`src/pages/sitemap.xml.ts` monta o XML a partir da mesma lista de comunidades do build.
A regra que importa — excluir pessoa e formulário, incluir comunidade — é lógica própria
de qualquer jeito, e uma dependência a mais para gerar vinte linhas de XML não se paga.

_Descartado:_ `@astrojs/sitemap` — configurá-lo para excluir por padrão daria o mesmo
trabalho, com dependência.

### 6. O `.astro` fica fino, e a carga de dados vai para `.ts` ao lado

O Biome 2.5.9 analisa `.astro`, mas **só o frontmatter**: variável definida ali e usada
só no template é reportada como não usada. Conferido: é aviso, e `biome check` sai com
código 0 — não quebra a esteira, mas polui.

Manter o `.astro` compondo e a carga de dados num `.ts` importado resolve o ruído e é o
desenho melhor de todo modo: a lógica volta a ser testável em unidade.

### 7. Os testes se dividem em três níveis

**Corrigida durante a implementação, em 2026-09-30.** A versão anterior desta decisão
dizia que os 26 arquivos de teste seguiriam valendo, porque as ilhas continuam React.
Era verificável e estava errada: **19 deles renderizam `<App />`** — são os 118 casos da
App 06 — e **19 casos afirmam navegação entre rotas** comparando `location.pathname`
depois de um clique. Essa transição era de cliente e passou a ser carga de documento,
que o jsdom não executa. Decisão do fundador de 2026-09-30, pela opção híbrida.

**Nível 1 — ilha, no jsdom.** Os 118 casos seguem, e passam a montar
`src/testes/TelaDaVitrine.tsx`: a composição de tela equivalente à das páginas de
`src/pages/`, com navegação de cliente. Ela existe **só para teste** e é declarada como
tal. O que cada caso afirma continua sendo comportamento de componente que a produção
tem; o que a composição de teste substitui é a carga de documento, que o jsdom não faz.

**Nível 2 — a saída do build.** É o que guarda o nível 1 contra desvio: se uma página de
`src/pages/` deixar de trazer uma seção, o nível 1 não percebe e este percebe. Confere
os cenários das specs sobre o `dist/` de um build real, contra um núcleo de mentira:
conteúdo no documento institucional, títulos e seções por rota, casca da comunidade sem
o painel, ausência de perfil no documento da pessoa, `noindex` presente só onde deve,
`sitemap.xml` e `robots.txt`.

**Nível 3 — unidade.** As funções puras de `src/descoberta/enderecos.ts` — montagem do
`sitemap.xml` e do `robots.txt` — têm teste próprio, sem build.

### 8. `astro check` no lugar de `tsc -b`

O `frontend-ci.yml` roda `npm run build --workspaces --if-present`, e é o que faz erro de
tipo barrar o PR. O `build` da App 06 passa a ser `astro check && astro build`, com
`@astrojs/check`. As outras seis aplicações não mudam.

### 9. Navegação vira link real

`useNavegacao` sai. Entre rotas estáticas a navegação é `<a href>`, o que dá histórico
de navegador de verdade e prévia de compartilhamento. Dentro da casca de pessoa, a
navegação de cliente permanece.

O `voltar` do `RF-03-44` — recusar o convite devolve à navegação, e quem chegou por
endereço direto sai para a raiz — hoje depende de uma contagem em memória porque não há
histórico real. Com link real, `history.length` deixa de ser adivinhação; o
comportamento declarado não muda.

## Risks / Trade-offs

| Risco | Mitigação |
| --- | --- |
| Núcleo fora do ar trava a publicação (decisão 4) | É a troca aceita; publicar vazio é pior. O deploy já depende de rede |
| Comunidade criada depois da última publicação não tem arquivo | Abre pela casca da decisão 3 e entra no `sitemap.xml` na publicação seguinte |
| Institucional editado na App 03 só aparece na publicação seguinte | É o preço de indexar. O institucional muda em dias, não em minutos |
| `@astrojs/react` renderizando componente que supõe navegador | Só sete arquivos tocam API de navegador, e seis já são de cliente. O sétimo tem a rolagem de âncora isolada em ilha |
| Aviso de variável não usada do Biome em `.astro` | Decisão 6: frontmatter fino. Conferido que não quebra a esteira |
| A composição de teste do nível 1 desviar das páginas de `src/pages/` | O nível 2 confere títulos e seções por rota sobre o `dist/` de um build real |
| Publicação com `noindex` faltando numa página de pessoa | Etiqueta **e** cabeçalho, em caminhos declarados no `firebase.json`, com teste sobre o `dist/` |

## Migration Plan

1. Astro e integrações entram na App 06, convivendo com a casca atual.
2. Rotas estáticas por arquivo; componentes viram ilhas, um grupo por vez, com os testes
   de componente verdes a cada passo.
3. Casca `noindex`, `robots.txt` e `sitemap.xml`.
4. `firebase.json`: `rewrite` específicos, `**` como fallback, cabeçalhos.
5. Esteiras: `app-06-deploy.yml` e `frontend-ci.yml`.
6. Casca antiga removida — `index.html`, `App.tsx`, `main.tsx`, `src/navegacao/`,
   `vite.config.ts`.

Rollback: a fatia é um PR só, com merge commit. Reverter o merge devolve a App 06
inteira ao estado de hoje; nada fora de `apps/app-06-vitrine/`, `firebase.json` e dois
workflows é tocado, e o núcleo não muda.
