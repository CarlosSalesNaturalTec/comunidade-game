# Design

## Context

Ver `proposal.md` — Why. O que molda o desenho:

- `.cg-caminhos`/`.cg-caminho` existem e funcionam, mas moram em
  `apps/app-01-aula-presencial/src/index.css`. Já são cartão com glifo, alvo de toque acima de
  48 px e rótulo em frase.
- A `AreaDoGuerreiro` já tem os quatro blocos montados e o temporizador de inatividade; só o
  padrão e a navegação mudam.
- `Trilha.tsx` já nasce em `tela = "guia"`, e `GuiaDaTrilha` já atende o `RF-05-08`. **Nada se
  constrói no lado da trilha.**
- `listarMinhasTrilhas` (`GET /v1/eu/trilhas`) já devolve `proxima_missao_titulo` e
  `proxima_missao_posicao`.
- A grade 2×2 que dobra em quatro colunas no marco de `768` px já tem idioma no repositório:
  `.cg-carta__colunas` em `comum/react/estilos.css`.

## Goals / Non-Goals

**Goals:**

- Um componente comum que sirva **as duas** disposições, sem bifurcar em dois componentes.
- App 01 **pixel-equivalente** depois da promoção do CSS.
- Nenhuma chamada nova ao núcleo.

**Non-Goals:**

- Mudar a disposição da tela inicial da App 01 — segue em coluna.
- Mexer no lugar da saída da sessão na App 05 — segue no cabeçalho.
- Narração das telas na App 05 — ela não provê `ProvedorDeNarracao`, e isso não é desta fatia.
- Promover `cg-caminhos__operacao` e `cg-caminhos__grupo`: o `fieldset` "para quem opera o
  aparelho" é só da App 01.

## Decisions

### 1. Uma propriedade `disposicao`, e o lugar do glifo decorre dela

`ListaDeCaminhos` recebe `disposicao: "coluna" | "grade"`. Na coluna o glifo fica **ao lado** do
rótulo; na grade, **acima**. É uma decisão, não duas propriedades: quem escolhe a disposição não
deve poder combinar grade com glifo ao lado, que é justo o arranjo que não cabe em 2×2 no
celular.

- _Descartado:_ duas propriedades independentes — abre arranjo que ninguém quer e que quebra na
  largura de 360 px.
- _Descartado:_ dois componentes — duplicaria o cartão, que é o que esta fatia vem unificar.

### 2. O glifo pode ficar acima do rótulo

O CSS da App 01 afirma "nunca acima", citando o documento 15 §§5 e 11.1. O §11.1 pede o rótulo
**junto** do ícone, não ao lado; e a fatia `2026-10-30-carta-em-colunas-e-saldo-para-trocar` pôs
o símbolo **acima** do rótulo nas colunas da carta, por decisão do fundador. O comentário da App
01 é leitura dela, não regra do documento — e será corrigido na promoção.

### 3. Grade de duas colunas que dobra em quatro no marco de `768` px

Pelo idioma de `.cg-carta__colunas`: `grid-template-columns: repeat(2, minmax(0, 1fr))` e, em
`@media (min-width: 768px)`, `grid-auto-flow: column`. O `--marco-768` é primitiva de
`comum/tokens.css` e não entra em `@media`, que não lê `var()` — a literal `768px` é o que o
repositório já faz.

- _Por que não coluna:_ quatro cartões com frase dão ~24 rem e jogam o Guia abaixo da dobra num
  aparelho de 360×640, que é o que a §10 do PRD-05 proíbe.

### 4. Cartões são navegação com item corrente, não menu de destinos

`caminhoAtual` é opcional. Declarado, o cartão correspondente recebe `aria-current="true"` e um
sinal além da cor — é o que o `NavegacaoDeAreas` já faz. Os cartões **permanecem na tela** com o
bloco aberto, então não existe tela de menu: o `RF-05-08` fica atendido na letra ("abre no bloco
da trilha") e no espírito ("sem procurar em menu").

A App 05 **não** usa o componente `NavegacaoDeAreas`, e por isso o requisito "aplicação com
navegação de áreas NEVER SHALL apresentar a saída da sessão dentro das telas de área" não a
alcança. O Sair segue no `Cabecalho`, onde já está, sempre no mesmo lugar.

### 5. O cartão da Trilha nomeia a próxima missão com o dado que já chega

`AreaDoGuerreiro` passa a chamar `listarMinhasTrilhas` para compor o rótulo do cartão da Trilha.
A trilha de referência é a **primeira** da lista — a mesma que `Trilha.tsx` seleciona por
padrão —, para que cartão e bloco não discordem. Falhando a leitura ou não havendo próxima
missão, o cartão fica só com o rótulo, e nunca espaço vazio. O cartão é **silencioso**: não
acrescenta aviso algum — o aviso de falha, quando houver, é o do próprio bloco da trilha, que já
o tem.

- _Descartado:_ rota nova ou endpoint de resumo — o dado já vem.
- _Descartado:_ içar o estado da trilha para a área — acoplaria os dois e não paga o cartão.

### 6. Três glifos novos, desenhados fora do que está reservado

| Caminho | Glifo | Por que não colide |
| --- | --- | --- |
| Minha carteira | dobra de carteira, **sem moeda dentro** | o círculo é da moeda (§9) |
| Trilha | `trilhas`, que já existe | — |
| Desafios e equipes | bandeira | não é silhueta de família (§8.3) |
| Coleta do território | gota com régua | mede o território, e não repete escudo nem estrela |

Traço de `2` px, grade de `24` px, `currentColor`, sem preenchimento — como todo glifo do
`Icone.tsx`. O escudo é da marca (invariante 24) e a estrela é da grandeza ponto (§9).

### 7. A promoção do CSS é movimentação, não reescrita

As regras saem de `apps/app-01-aula-presencial/src/index.css` e entram em
`comum/react/estilos.css` **com os mesmos valores e os mesmos tokens**. O `--raio-campo` segue
resolvendo pelo temperamento de cada aplicação, que é o comportamento desejado de peça comum:
Arena na App 05, Operação na App 01.

## Risks / Trade-offs

- **A App 01 regride visualmente na promoção** → o cartão dela permanece em `disposicao="coluna"`
  e as regras migram sem alteração de valor; os testes de `inicio.test.tsx` cobrem rótulo, ordem
  e glifo, e passam a cobrir a disposição.
- **Grade 2×2 com frase aperta em 360 px** → o rótulo é frase **curta**; a frase longa da App 01
  ("Onboarding — cadastro do Guerreiro(a) e presença do dia") é da coluna, não da grade. O
  `minmax(0, 1fr)` impede o estouro horizontal.
- **O cartão da Trilha some do ar se a leitura falhar** → o rótulo sozinho é o estado de reserva,
  e o cartão não acrescenta aviso: quem relata a falha é o bloco da trilha, que já relatava.
- **Quem entra sem inscrição não tem próxima missão** → o bloco da trilha já leva à escolha do
  poder (requisito vigente), e o cartão fica só com o rótulo.
- **Duas navegações na tela da Trilha** — os cartões e as abas Guia/Progresso/Retomadas → fica
  como está; reduzir isso é mudança de desenho da trilha, que o fundador não pediu e que esta
  fatia não antecipa.
