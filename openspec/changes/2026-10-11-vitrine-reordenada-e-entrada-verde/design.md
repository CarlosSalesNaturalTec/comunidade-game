# Design

## Context

A ordem das seções da abertura mora em `src/pages/index.astro`, como `src/navegacao/recortes.ts`
declara desde a fatia 9: "quais seções cada recorte abre, e em que ordem, mora na página do
recorte". Por isso a reordenação não é decisão de desenho — é edição de uma lista.

O que exige desenho são três coisas: o par de cores do herói (o verde entra numa família que o
documento 15 trata como **estado**, não como ação), o destino do que a seção de poderes
derivava, e a ordem em que as sete camadas são tocadas para que nenhum passo contradiga o de
cima. Motivação e recorte: `proposal.md`. Requisitos: o delta em
`specs/aplicacao-da-vitrine/spec.md`.

## Goals / Non-Goals

**Goals:**

- Fazer o verde do "Entrar" caber no documento 15 **sem família nova e sem degrau inventado**.
- Deixar a remoção das duas seções sem resíduo: nenhum componente, tipo ou leitura órfã na
  vitrine, e nenhuma rota do núcleo tocada.
- Dar ordem às sete camadas, de modo que o código seja a última.

**Non-Goals:**

- Não se decide aqui qual cor cada ação do herói recebe em outras aplicações: a variante é
  deste par, como a decisão de 2026-10-10 já registrou.
- Não se reescreve a seção de Mestres para absorver o que a de poderes mostrava. Os Mestres
  responsáveis **saem**, e a seção de Mestres fica como está.

## Decisions

### 1. O verde reaproveita a família Sucesso, com um token semântico novo e nenhuma primitiva

A família Sucesso do documento 15 §3.2 tem **dois degraus** — 600 e 400 —, porque nasceu como
cor de estado. Um botão cheio precisa de três coisas que ela não tem: o texto sobre o fundo, o
contorno, e a razão de contraste medida.

| Papel | Valor | Natureza |
| --- | --- | --- |
| Fundo | `--cor-sucesso` | já existe |
| Texto | `--cor-sobre-sucesso` — `cal-000` no claro, `tinta-900` no escuro | **token novo**, derivação pura |
| Contorno | `--cor-sucesso` | já existe |

O token novo segue exatamente o padrão que Marca, Ação e Moeda já têm (`--cor-sobre-marca`,
`--cor-sobre-acao`, `--cor-sobre-moeda`), nos dois modos de `comum/tokens.css`. Não é primitiva:
aponta para primitiva que já está lá.

O **contorno reusa o 600** porque a família não tem 700 e inventar o hexadecimal seria criar
número que o documento 15 não fixa. A regra do documento 15 sobre contorno no degrau 700 vale
para **ficha** — "toda ficha leva contorno no degrau 700 da sua família" —, não para botão;
`.cg-botao` exige um `border-color` apenas para reservar a largura do foco. O `index.css`
registra isso em comentário, para a próxima pessoa não ler como esquecimento.

- _Alternativa descartada:_ família nova de cinco degraus no documento 15 — o fundador decidiu
  reaproveitar.
- _Alternativa descartada:_ acrescentar só o degrau 700 à família Sucesso — exigiria hexadecimal
  que nenhum documento fixa.
- _Alternativa descartada:_ virar a família Marca para verde — repintaria logotipo, submarcas e
  o cabeçalho das oito aplicações.

### 2. O token passa a ter dois papéis, e isso vai escrito no documento 15

`--cor-sucesso` tem hoje **um** consumidor, o `.cg-aviso--sucesso` da camada comum. Com esta
change ele significa "deu certo" **e** "entre aqui". Duplicidade de papel que não está escrita é
acidente, e a próxima pessoa que mexer na cor de aviso mexe no "Entrar" sem saber — por isso a
§3.2 ganha a frase, e não só o código.

O invariante de acessibilidade continua de pé sem esforço: o par do herói se distingue **por cor
e por rótulo** (delta do herói), e "Nenhum estado se comunica apenas por cor" é requisito de
`camada-visual-comum` que nada aqui afrouxa.

### 3. `.cg-botao--marca` é renomeada, não repintada

A variante tem **um** consumidor, `EntradaDaAbertura.tsx`, e nasceu em 2026-10-10 para este par.
Repintar de verde uma classe chamada `--marca` deixaria o nome mentindo. Ela vira
`.cg-botao--entrada`: nome do **papel**, não da família — o que também a protege da próxima troca
de cor.

Continua morando em `apps/app-06-vitrine/src/index.css`, e não na camada comum: a variante é
deste par, e as outras sete aplicações não pediram ação verde.

### 4. A remoção da seção de poderes não toca o núcleo

`GET /v1/vitrine/poderes` fica. Removê-la arrastaria o contrato OpenAPI, o corpus do assistente
do Desenvolvedor e o PRD-03 §9, sem ganho: a vitrine existe para ser construída por cima, e a
Área do Apoiador Desenvolvedor é a porta disso.

Na vitrine saem três coisas, juntas: `src/poderes/SecaoDePoderes.tsx`, a função `listarPoderes`
de `src/api/leituras.ts` e o tipo `PoderPublico`, se nada mais o usar. Leitura sem consumidor na
vitrine é código morto, e o Biome não a flagra por ser `export`.

### 5. A chave PIX fica num lugar só, e o requisito da porta passa a dizer isso

Com "Como apoiar" fora da tela, a porta do convite é o **único** lugar público onde a chave PIX
aparece. O requisito da porta deixa de descrevê-la como "a mesma que 'Como apoiar' publica" —
frase que ficaria apontando para tela inexistente — e passa a apontar a seção do conteúdo
institucional que a guarda. O `NEVER SHALL deixar de oferecê-la quando o núcleo a devolve` é
consequência direta de ser o único lugar: antes havia redundância, agora não há.

### 6. A ordem das sete camadas

Nenhum passo pode contradizer o de cima enquanto a árvore estiver no meio do caminho:

```
1. documento 03 §8           ← regra de negócio: seções, "Como apoiar", rótulo da chamada
2. documento 15 §§3.2, 3.3   ← identidade visual: a família Sucesso e as razões medidas
3. documentos 02, 08, 12, 14 ← as menções ao rótulo, uma frase cada (fonte única)
4. documento 09 §1           ← as seis decisões, de "pendentes" para "já decididos"
5. PRD-03 e PRD-02           ← os requisitos que as decisões mudam
6. delta de spec             ← o contrato de comportamento
7. código e testes           ← execução
```

As medições do passo 2 são feitas **antes** de o número entrar no documento: `cal-000` sobre
`sucesso-600` no claro, `sucesso-400` com `tinta-900` no escuro. Nenhum valor é escrito de
memória nem estimado.

## Risks / Trade-offs

- **O token de sucesso ganha dois papéis** → a frase no documento 15 §3.2 e o comentário no
  `index.css`. Quem for mexer na cor de aviso encontra o aviso.
- **O par do herói perde a cor da família Marca** → conferido no navegador, e o receio era
  maior que o fato: o laranja segue dominando a abertura **pela ilustração do elenco**, onde o
  Robô Educa é laranja, além do símbolo do cabeçalho. O que muda é só a cor do botão, e a
  abertura não esfriou. Consequência aceita, não defeito.
- **"Quero apoiar" estreita a leitura da porta**, que atrás dela mantém as sete modalidades do
  documento 14 §10, a pretensão de ensinar incluída → risco real e aceito pelo fundador. O garfo
  não muda, e quem quer ensinar continua encaminhado; se a conversão de Mestre cair, é dado para
  uma decisão futura, não para esta change.
- **O caminho `/quero-participar` passa a divergir do rótulo** → aceito: o endereço é público e
  compartilhável, está no `sitemap.xml`, e trocá-lo quebraria link de fora sem ganho. Um cenário
  do delta trava isso.
- **O par de contraste do escuro pode não passar** o piso de 4,5:1 → a medição acontece antes da
  edição do documento 15. Se não passar, a change para e a cor volta ao fundador; não se inventa
  degrau para salvar o desenho.
- **"Como apoiar" fica gravável sem tela**, o que pode parecer defeito a quem lê o Admin → o
  cenário do delta registra que a publicação segue aceita de propósito, e o PRD-02 §16 diz o
  mesmo.
- **A chave PIX deixa o documento servido** — achado da implementação, não previsto neste
  desenho. "Como apoiar" era renderizada **no build** (`secaoInstitucionalDoBuild`), e por isso
  a chave saía dentro do `index.html`; a porta é ilha `client:load`, e busca a leitura
  institucional no aparelho. Com a seção fora, a chave **não sai em documento nenhum**: quem
  visita sem JS, e quem indexa, não a alcança mais. O `RF-03-46` continua cumprido — a porta a
  exibe —, e o `saidaDoBuild.test.ts` passou a afirmar o que o build realmente emite, em vez de
  afirmar a chave onde ela não está. **Fica para decisão do fundador** se a porta deve
  pré-renderizar a chave no build, como "Como apoiar" fazia; não se resolve aqui, porque muda o
  que o PRD-03 §10 exige do institucional servido.

## Migration Plan

Não há migração de dado: nenhuma entidade, rota ou contrato muda. A seção `como-apoiar` segue
no núcleo com o texto que já tem, e o que estava semeado continua lá.

O recuo é reverter o PR: nada no núcleo foi tocado, e o conteúdo institucional não foi alterado.
