# A marca do projeto — o que entregar aqui

Esta pasta guarda a **marca** do Comunidade Game: logotipo, símbolo, submarcas e o
elenco de personagens. Ela é **constante da plataforma** — não varia por comunidade — e
por isso vive versionada aqui, e não no núcleo (documento 15 §12).

A marca é **reservada**: fica fora da AGPL e da CC BY-SA, e quem replica a plataforma
troca-a pela sua (documento 03 §1). A reserva mora em `LICENCA.md`, ao lado dos
arquivos, pelo mesmo motivo que a licença das fontes mora ao lado delas.

**A marca do projeto e as submarcas já estão aqui** — produzidas, não encomendadas (§8).
**O elenco ainda não chegou**, e para ele este documento segue sendo o manifesto do que
entregar, escrito antes dos arquivos para que a entrega não precise de ida e volta.

## O que é regra e o que é recomendação

| | |
| --- | --- |
| **Regra** | O que os documentos 03 e 15 já fixam: formato vetorial sempre que couber, cor da paleta do §3, servir pelo próprio domínio, nada de terceiro em tempo de execução |
| **Convenção** | Pasta e nome de arquivo — definidos aqui, no padrão de `comum/fontes/`: minúsculas, hífen, português |
| **Recomendação** | Os orçamentos de peso e as grades de desenho abaixo. Derivados do princípio 4 do documento 15, que exige peso como requisito sem fixar número. Para virarem regra, precisam descer ao documento 15 |
| **Sua decisão** | Proporção, traço, área de proteção, tamanho mínimo e quais personagens são de uso público. Nenhum desses números está nos documentos, e nenhum se inventa aqui |

## 1. Marca do projeto

Todos em `comum/marca/`.

| Arquivo | Formato | Grade de desenho | Peso máximo | Para quê |
| --- | --- | --- | --- | --- |
| `marca-horizontal.svg` | SVG | altura `32`, largura livre | 10 KB | Vitrine, rodapé e documento — **não** o cabeçalho |
| `marca-horizontal-mono.svg` | SVG, `currentColor` | idem | 10 KB | Modo escuro e uso sobre a foto de comunidade |
| `marca-empilhada.svg` | SVG | caixa `160 × 96` | 10 KB | Herói da vitrine e espaço vertical |
| `simbolo.svg` | SVG | `48 × 48` | 3 KB | **Cabeçalho das oito aplicações** e todo espaço curto |
| `simbolo-mono.svg` | SVG, `currentColor` | `48 × 48` | 3 KB | Idem, no escuro e sobre foto |

**Uma versão colorida e uma monocromática**, e não um par claro/escuro: a monocromática
usa `currentColor` e herda a cor do texto, então **um arquivo serve o modo escuro e o
uso sobre foto**. Um par claro/escuro dobraria os arquivos e deixaria o caso da foto sem
resposta.

A monocromática é **em traço**: contorno em `currentColor` e preenchimento nenhum, com o
monograma cheio dentro (decisão do fundador de 2026-10-02). Ela é, portanto, **desenho
próprio** — não se deriva da colorida trocando preenchimento.

**O orçamento da monocromática é igual ao da colorida**, e não menor: as duas carregam as
mesmas curvas, e o que muda entre elas são alguns bytes de atributo de cor.

O **`apple-touch-icon.png`** (`180 × 180`, atalho em iOS, que não aceita SVG) **não se
desenha**: é rasterizado do `simbolo.svg` na implementação. Não entra na encomenda.

**Não há arquivo de favicon.** Sob a forma de escudo com ponta, o favicon e o símbolo
ficaram idênticos — os dois limitados pela mesma grade de 48 —, e a esteira copia o
`simbolo.svg` para as sete `apps/*/public/` com o nome `favicon.svg`, que é o que cada
`index.html` referencia (decisão do fundador de 2026-10-02).

## 2. Submarcas

Em `comum/marca/`. As duas que o documento 09 nomeia.

| Arquivo | Formato | Grade | Peso máximo |
| --- | --- | --- | --- |
| `submarca-robroders.svg` | SVG | altura `32`, largura livre | 5 KB |
| `submarca-robroders-mono.svg` | SVG, `currentColor` | idem | 5 KB |
| `submarca-robo-educa.svg` | SVG | altura `32`, largura livre | 5 KB |
| `submarca-robo-educa-mono.svg` | SVG, `currentColor` | idem | 5 KB |

## 3. Elenco de personagens

Em `comum/marca/elenco/`. Os quatro que o documento 15 §13.6 nomeia.

| Arquivo | Formato | Grade | Peso máximo |
| --- | --- | --- | --- |
| `susy.svg` | SVG | caixa `512 × 512` | 40 KB |
| `otavio.svg` | SVG | caixa `512 × 512` | 40 KB |
| `trenell.svg` | SVG | caixa `512 × 512` | 40 KB |
| `robo-educa.svg` | SVG | caixa `512 × 512` | 40 KB |

Não confundir `elenco/robo-educa.*`, que é o **personagem**, com
`submarca-robo-educa.svg` do §2, que é a **palavra**. Os **Rôbróders** não têm arquivo de
elenco: eles seguem só como submarca.

**Pose neutra, um arquivo por personagem.** Expressões, se vierem, seguem o mesmo nome
com sufixo — `susy-alegre.svg`, `otavio-pensativo.svg` — e não substituem a pose neutra.

**Cor, contorno, fundo e keyline** seguem o documento 15 §13.6: cor livre, contorno
`tinta-900` grosso e fechado, preenchimento chapado sem gradiente, fundo transparente, e
o filete em `cal-050` por fora da silhueta. O keyline é **gravado no arquivo**, nunca
aplicado em CSS.

**Por que SVG e não imagem:** o documento 15 §2 descreve o traço como *contorno grosso e
cor chapada*, que é precisamente o que vetoriza bem e escala sem peso. Se algum
personagem só existir em raster, entregue **AVIF** com fallback **WebP**, em `1024` px
de lado maior, até 120 KB cada — e diga qual, para a implementação prever `srcset`.
Saindo em raster, o par é `<nome>.avif` com reserva `<nome>.webp`, e os nomes da tabela
acima valem com a extensão trocada.

**Os quatro saíram pela rota raster**, decisão tomada com os arquivos na mão: cada figura
traz de 47 a 66 mil cores, de sombreado suave, e vetorizar isso não fecharia os 40 KB do
SVG. Os oito arquivos entregues pesam de 34 a 50 KB, contra o teto de 120 KB. Nenhum
personagem saiu em SVG, então o `srcset` tem só o par AVIF/WebP.

## 4. O que precisa vir junto, e não é arquivo

Sem estes dois, a implementação não fecha o documento 15 §13.6:

1. **Quais personagens são de uso público.** A vitrine é pública e indexável.
2. **Procedência**: quem dirigiu, com que ferramenta, quando, e sob qual acordo — a
   titularidade é da pessoa jurídica (documento 03 §1), e isso precisa estar registrado.

A área de proteção e o tamanho mínimo saíram desta lista: foram decididos pela change da
marca e estão no documento 15 §13.4.

## 5. O que não entra aqui

| Isto | Vai para |
| --- | --- |
| A **foto de fundo** da comunidade | Núcleo — varia por comunidade (documento 15 §6.3). Pendente no documento 09 |
| Personagem como **cena de missão** | `conteudo-da-missao`, autorado pelo Mestre na App 09 |
| Ícone de interface | `comum/react/Icone.tsx`, que é código e já tem a grade do §11.1 |
| Avatar do Guerreiro(a) | `comum/avatar/`, que é paramétrico e composto em código (§7) |

## 6. Como entregar, e o que acontece depois

Esta seção existe para que a entrega **não dependa de nenhuma conversa**: quem chegar
aqui com os arquivos na mão, meses depois, encontra o caminho inteiro.

**Onde pôr.** Nesta pasta e em `elenco/`, com os nomes exatos das tabelas acima. Dois
caminhos, e tanto faz qual:

- **Pelo console do GitHub**, num branch — nunca direto na `main`. Branch → `comum/marca/`
  → _Add file · Upload files_. Na `main` os arquivos entrariam sem passar pelo
  `pull_request` da esteira, e sem diff para alguém olhar antes.
- **Entregando os arquivos a quem implementa.** SVG é texto: dá para colar. Quem
  implementa cria os arquivos com os nomes certos e confere antes de gravar.

**O que destrava.** Com o elenco aqui, a fatia 11 do `openspec/cronograma-de-fatias.md`
sai da trava. A change é `2026-09-30-heroi-e-gramatica-da-vitrine`, e a implementação
retoma na **tarefa 1.1** dela, que é conferir cada arquivo contra a tabela do §3. A marca
do projeto já foi entregue pela change `2026-10-02-marca-do-projeto-e-silhueta-de-nivel`.

**O que não trava a entrega.** SVG com metadado de editor, `<style>` interno ou camada
oculta — Figma e Illustrator exportam assim. Quem implementa limpa e diz o que mudou.

## 7. Regras que valem para todo arquivo desta pasta

- **Nenhuma cor fora da paleta** do documento 15 §3 — **exceto o elenco de `elenco/`**,
  que tem licença cromática própria (documento 15 §13.6). A monocromática não declara cor
  nenhuma: usa `currentColor`.
- **Nenhuma referência externa** — sem fonte de terceiro embutida, sem imagem
  referenciada por URL, sem `<script>`. O que a aplicação serve sai do próprio domínio
  (documento 15 §1, princípio 6).
- **SVG otimizado**: sem metadado de editor, sem camada oculta, sem filtro de desfoque.
  O favicon atual, do Vite, é o contraexemplo — 9,5 KB quase todos de `feGaussianBlur`.
- **Texto do logotipo em curvas**, nunca em `<text>`: fonte não instalada no aparelho
  quebraria a marca.

## 8. Procedência do que já está aqui

Os nove arquivos da marca do projeto e das submarcas — tudo o que os §§1 e 2 listam — foram
**produzidos pelo próprio projeto em 2026-10-02**, e não encomendados.

| | |
| --- | --- |
| **Logotipo e submarcas** | **Archivo** convertido em curvas, peso `700`, eixo de largura `62` no logotipo e `87` nas submarcas. A família já é servida pelo projeto e está em `comum/fontes/`, com a licença e a data de cópia ao lado |
| **Símbolo** | Escudo com o monograma `CG`, desenho original do projeto. O **topo em ponta**, por duas curvas côncavas, entrou em 2026-10-02 a partir de um modelo de referência do fundador, medido e não estimado: ponta a 18,1% da altura, proporção `1 : 1,172`. As cinco peças que carregam o escudo descrevem a **mesma silhueta**, diferindo só pela escala, e `comum/marca.test.ts` o confere |
| **Cores** | Escudo em `marca-500`, contorno em `marca-700`, monograma em `tinta-900` — os três da paleta do documento 15 §3 |
| **Licença da fonte** | SIL Open Font License 1.1, em `comum/fontes/OFL-archivo.txt`. Converter glifos em curvas dentro de um logotipo é uso permitido e **não** submete o logotipo à OFL: a cláusula de _Reserved Font Name_ restringe redistribuir a **fonte** modificada, não o desenho que a usa |
| **Titularidade** | Da pessoa jurídica vinculada ao projeto, como manda a `LICENCA.md`. Não há cessão de terceiro a registrar, porque não houve autor externo |

A construção completa — proporção do escudo, altura de maiúscula, contrastes medidos — está
no documento 15, que é a fonte única da identidade visual. Aqui fica só a procedência.

**O elenco** do §3 foi produzido pelo próprio projeto, com assistência de **IA generativa
sob direção do fundador** — cor, traço, olhos, cabelo, enquadramento e pose dirigidos a cada
geração. Não houve autor externo, e por isso não há cessão de terceiro a registrar: a
titularidade é da pessoa jurídica, como manda a `LICENCA.md`. Os arquivos entregues passam
por recorte do fundo, aplicação do keyline e redimensionamento antes de entrar aqui.

Do que chegou para o que está aqui, o que mudou — o §6 manda dizer: as quatro origens
vieram em JPEG sobre fundo magenta chapado, que foi recortado por distância de cor; a
franja de magenta saiu só na faixa de borda, para não alterar cor legítima; a figura foi
recortada, recebeu 3% de margem e desceu para `1024` px de lado maior; e o keyline em
`cal-050` foi aplicado aqui, porque nenhuma origem o trazia. **O contorno veio entre
`#261D29` e `#2E1C20`**, e não no `tinta-900` que o documento 15 §13.6 pede — ficou como
veio, porque separar contorno de cabelo escuro automaticamente estragaria o cabelo, que
em três dos quatro é marrom muito escuro.

> **A definir:** a ferramenta usada e a data da produção do elenco, que completam este
> registro.
