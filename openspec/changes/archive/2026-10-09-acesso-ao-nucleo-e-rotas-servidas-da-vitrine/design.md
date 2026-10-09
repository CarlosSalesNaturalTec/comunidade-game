# Design

## Context

Ver `proposal.md` — Why. O que o desenho precisa ter em mãos:

- A App 06 é Astro com saída estática; não tem `main.tsx`, e foi essa a porta por onde
  a configuração de acesso ao núcleo se perdeu. As demais sete aplicações a chamam no
  `main.tsx` delas.
- `src/api/nucleo.ts` é o gargalo único de leitura da vitrine — o docstring dele já
  diz "toda leitura da vitrine passa por aqui". Nenhuma ilha chama `comum/api` direto.
- `comum/api` exige configuração explícita por aplicação e lança sem ela. Isso é
  requisito de `camada-de-acesso-comum` ("Configuração ausente não é suprida por
  padrão embutido"), não defeito: a camada se comportou como manda.
- O Firebase Hosting resolve um pedido nesta ordem: arquivo exato, `cleanUrls`,
  índice de diretório, `rewrites` na ordem declarada. `build.format: "file"` emite
  `pesquisadores.html`; sem `cleanUrls` o endereço `/pesquisadores` não alcança
  arquivo nenhum e cai no `**`.

## Goals / Non-Goals

**Goals:**

- A configuração de acesso ao núcleo alcança o navegador por **um** caminho, e não
  por um por ilha.
- Cada endereço público publicado é servido pelo documento daquela rota.
- Os dois pontos cegos do CI viram teste, no nível que consegue afirmar o que a spec
  exige.

**Non-Goals:**

- Não mexer em `comum/api`: a camada está correta.
- Não trocar `build.format`, não migrar de Astro, não revisar a ordem dos `rewrites`
  nem a lista de `ENDERECOS_INDEXAVEIS` — a fatia 9 as decidiu e elas estão certas.
- Não mudar o comportamento de nenhuma seção: elas já estão escritas e testadas; o
  que falta é alcançarem o núcleo.
- Não subir Firebase de verdade no CI.

## Decisions

### 1. A configuração do cliente mora em `src/api/nucleo.ts`, idempotente

`lerDoNucleo` configura o acesso antes de chamar, uma vez por carregamento do
documento. É o gargalo por onde toda ilha já passa, então nenhuma ilha nova nasce,
nenhum JS extra é servido e não há ilha nova a esquecer na próxima seção.

`src/build/dados.ts` já tem esse idioma (`configurarUmaVez`) com flag própria. A
função passa a morar em `src/api/nucleo.ts` e o `build/dados.ts` a consome: um idioma
só, servindo o build e o navegador, em vez de duas cópias que podem divergir.

| Alternativa | Por que não |
| --- | --- |
| Ilha `client:load` no `Base.astro` | A ordem de hidratação entre ilhas não é contratual no Astro: corrida silenciosa |
| Chamar em cada ilha | Repetitivo, e a próxima seção nasce sem a chamada — é a regressão de novo |
| `comum/api` ler a variável de ambiente sozinho | Contraria a requirement de `camada-de-acesso-comum` e a decisão 6 da fatia 1 |

### 2. `cleanUrls: true` no alvo `vitrine`, preservando `build.format: "file"`

Uma linha, e é ela que falta para a aposta da fatia 9 se fechar. As canônicas já
emitidas são o endereço **sem** `.html`, que passa a ser exatamente o endereço
servido; o Firebase redireciona `/x.html` → `/x` com 301, o que consolida a
identidade de cada rota para o buscador em vez de dividi-la.

Descartado: `build.format: "directory"`. Funciona, mas mexe na canônica do
`Base.astro` (o `pathname` passa a ter barra final), reabre `trailingSlash` e muda o
nome de todo arquivo de `dist/` — risco maior, mesmo resultado.

### 3. `cleanUrls` cria o endereço `/app`, e a casca de pessoa tem de cobri-lo

Consequência da decisão 2 que **não** é detalhe de implementação: com `cleanUrls`, a
casca passa a ser alcançável também em `/app`, endereço que hoje não existe. O
`robots.txt` barra `/app.html` e a regra de cabeçalho casa `/app.html` — nenhum dos
dois alcança `/app`.

A casca de pessoa nunca ser indexada é o invariante 12 do documento 99, e por isso a
cobertura passa a valer para **os dois** endereços: `robots.txt` barra `/app` e
`/app.html`, e a regra de `X-Robots-Tag` casa os dois. A etiqueta no documento da
casca continua onde está — é a defesa que não depende de configuração de hospedagem.

Isso toca `src/descoberta/enderecos.ts`, que é onde a montagem do `robots.txt` mora
justamente para ser testável em unidade (fatia 9, decisão 6).

### 4. O teste de endereço servido modela a precedência, alimentado pelo que existe

Nenhum teste hoje cruza **arquivo emitido × caminho servido**, e é a junta exata por
onde o defeito 2 passou. O teste novo resolve, para cada endereço público, qual
arquivo o serve, aplicando a precedência documentada do Firebase sobre **o
`firebase.json` real e a árvore real de `dist/`** — não sobre fixture.

Alimentar o teste com o que existe é o ponto: assim ele falha quando o `firebase.json`
muda, quando o `build.format` muda e quando uma rota nova nasce sem endereço — os três
jeitos de a regressão voltar.

Descartado: subir `firebase emulators` no CI — exige a CLI e credencial numa esteira
que hoje não precisa de nenhuma das duas, para afirmar o mesmo.

### 5. O teste do defeito 1 é o que **não** configura o acesso

O defeito sobreviveu porque `semRastro.test.tsx` fornece a configuração que a produção
não fornece. O teste novo é um arquivo que **nunca** chama
`configurarAcessoAoNucleo`: dubla só o `fetch`, apresenta uma seção de leitura e
afirma que a chamada saiu com a chave da App 06.

Arquivo separado, e não um caso dentro de um existente: a configuração vive em estado
de módulo, e o registro de módulos do Vitest é por arquivo — num arquivo que já
configura, o teste passaria por engano.

## Risks / Trade-offs

| Risco | Mitigação |
| --- | --- |
| O modelo de precedência do teste 4 divergir do Firebase real | Ficar na precedência documentada, sem esperteza, e alimentá-lo do `firebase.json` e do `dist/` reais; a publicação confirma uma vez em produção |
| `cleanUrls` criar outro endereço duplicado que passe batido | O teste 4 varre os endereços públicos, não uma lista escrita à mão; a decisão 3 é o caso já encontrado |
| A configuração na leitura atrasar a primeira chamada | Atribuição de dois valores em memória, sem E/S; a alternativa com ilha tem corrida, que é pior |
| A regressão ter deixado outro rastro ainda não visto | A verificação em produção depois da publicação cobre as nove seções, as três páginas de pessoa e os dez endereços — não só os dois sintomas relatados |

## Migration Plan

Sem migração de dado e sem mudança de contrato de API. A publicação é a esteira
`app-06-deploy.yml` de sempre, que já dispara por `firebase.json` e por
`apps/app-06-vitrine/**`, e publica `--only hosting:vitrine`.

Reversão: os dois ajustes são de poucas linhas em `src/api/nucleo.ts`,
`src/descoberta/enderecos.ts` e `firebase.json`; reverter o merge devolve o estado
anterior sem resíduo.

Depois do merge em `main`, conferir em produção os dez endereços públicos e as nove
seções de leitura — é a confirmação que o teste 4 não dá por si.
