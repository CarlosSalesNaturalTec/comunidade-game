# Design

## Context

Ver `proposal.md` — Why. O que molda o desenho é um fato de arquitetura: **uma só**
`CartaDoPersonagem` e **uma só** `cartaEstaCompleta` servem três superfícies — a Área do
Guerreiro(a), o desfecho da presença na App 01 e a página pública da vitrine —, e a terceira é
pública. O padrão de montagem já existe e não se reabre: `comum/carta` lê, trata cada leitura
isoladamente e entrega o objeto da variante; o componente só apresenta.

O estado atual dos requisitos está em `openspec/specs/camada-visual-comum/spec.md` e
`openspec/specs/area-do-guerreiro/spec.md`. Os deltas desta change estão em `specs/`.

## Goals / Non-Goals

**Goals:**

- Fazer o saldo chegar à carta **sem** que ele possa chegar à superfície pública, por construção e
  não por cuidado de quem escreve a tela.
- Fazer a falta do saldo ser **inofensiva**: não derruba a carta, não vira carta pela metade.
- Pôr as quatro seções em colunas sem que o arranjo depende do número de seções.
- Reusar a estrela que já existe, em vez de desenhar uma segunda.

**Non-Goals:**

- Nenhuma variante nova da carta, nenhum parâmetro de "modo público" no componente.
- Nenhuma ficha (pastilha) das grandezas: ver a decisão 4.
- Nenhuma mudança no núcleo.

## Decisions

### 1. O saldo é campo opcional do tipo, e fica fora da decisão de completude

`CartaDeGuerreiro` recebe um campo para o saldo que aceita ausência, e `guerreiroEstaCompleto`
**não** o consulta. Quem o preenche é `comum/carta`, que só é usado por tela logada; o adaptador da
vitrine (`apps/app-06-vitrine/src/guerreiros/carta.ts`) não tem de onde tirá-lo — a leitura pública
não devolve o dado e o núcleo não ganha campo.

A garantia é dupla e vem de onde já estava: a rota recusa quem não é o próprio Guerreiro(a), e a
projeção pública não tem o campo. A carta não precisa saber em que superfície está.

- Descartado: variante nova (`guerreiro-logado`) — duplicaria a tabela do documento 11 §8.2 e as
  três superfícies passariam a escolher variante.
- Descartado: campo obrigatório com valor neutro — a vitrine passaria a afirmar um saldo que não
  leu, e `cartaEstaCompleta` recusaria a carta pública.

### 2. A estrela cheia sai do trio para peça própria

O traçado em `comum/react/TrioDeEstrelas.tsx` é extraído para uma peça só de estrela, que o trio
passa a compor três vezes e a carta usa uma vez. A exceção ao traço sem preenchimento já está
escrita no requisito do sistema de ícone, para a ficha das grandezas do documento 15 §9 — a estrela
cheia entra por ela, com preenchimento e contorno vindos dos tokens da família ponto.

- Descartado: glifo no `Icone` — ele fixa `fill="none"`, por força do documento 15 §11.1.
- Descartado: duplicar o traçado na carta — dois desenhos da mesma forma divergem na primeira
  correção.

### 3. O arranjo é "duas por linha, e em linha a partir do marco"

No celular, duas colunas de largura igual. A partir de `768` px, **todas** as seções em uma linha —
o que dá quatro na tela logada e três na pública, sem trilha vazia e sem o número de seções estar
escrito no CSS. O alinhamento é pelo topo: coluna curta fica curta.

- Descartado: quatro trilhas fixas a partir do marco — a carta pública, com três seções, ficaria com
  uma trilha vazia.
- Descartado: trilhas que se acomodam pela largura mínima de cada uma — a quebra aconteceria em
  larguras imprevisíveis e o contrato de 2×2 no celular se perderia.

### 4. A carta não leva amarelo

Os símbolos das colunas, inclusive a estrela vazada do ponto extra, herdam a cor do texto, como todo
glifo. Medido contra a superfície da carta: `ponto-500` como contorno de `2` px sobre `cal-000` dá
**1,82:1** — é por isso que o documento 15 §3.3 mede `tinta-900` **sobre** `ponto-500`, e nunca o
inverso. A cor da família ponto aparece onde a §9 a põe: no preenchimento da ficha, na tela de
troca, que esta fatia não alcança.

O que separa as duas grandezas na carta é, então, **forma e rótulo** — estrela cheia contra vazada,
"pontos regulares" contra "pontos extras" —, que é o que o documento 15 §5 exige de qualquer modo.

- Descartado: contorno em `ponto-700` (`6,72:1`, legível) para o glifo — tornaria o símbolo da
  coluna a única peça do sistema de ícone com cor própria, contra a §11.1.

### 5. O contorno da família ponto no tema escuro vale `ponto-400`

Medido sobre `tinta-800`: `ponto-700` dá **2,34:1**, abaixo do piso de `3:1` que o documento 15
§3.3 fixa para contorno; `ponto-400` dá **10,58:1**. As duas razões entram na tabela da §3.3.

- Descartado: `ponto-500` (`8,64:1`) — é o valor do **preenchimento** no escuro, e contorno igual ao
  preenchimento apaga o limite que a §9 pede de toda ficha.

### 6. Os dois glifos novos: medalha e pincel

**Medalha** para Badges — retângulo arredondado com duas caudas de fita — e **pincel** para Criações
originais. Desenhados na grade de `24` px com traço de `2` px, em `currentColor`, como os demais.

As formas óbvias estavam vedadas: losango e folha com canto dobrado são silhuetas de **família**
(documento 15 §8.3), e no cabeçalho de coluna afirmariam família errada; o escudo é a marca
(invariante 24) e o círculo é a moeda (§9). Poderes usa o glifo `poder` genérico, que já existe.

- Descartado para Badges: fita sozinha — lida como laço de presente, sem dizer prêmio.
- Descartado para Criações originais: moldura com traço dentro — lida como imagem, e criação
  original também é mapa, música e protótipo.

### 7. O saldo entra na leitura que já existe, e falha sozinho

`CartaDoGuerreiro` já lê em paralelo e trata cada falha isoladamente, deixando o campo ausente. O
saldo entra nesse mesmo conjunto — e, por causa da decisão 1, a falha dele não tem consequência
nenhuma além de a seção não aparecer. Recusa de sessão continua tratada como recusa de sessão, nunca
como dado faltante.

## Risks / Trade-offs

| Risco | Mitigação |
| --- | --- |
| `carta.test.tsx` tem cerca de 700 linhas apoiadas no fluxo vertical atual, e asserções que dependem da ordem dos nós quebram em bloco | As asserções passam a se apoiar em rótulo e papel acessível, não em posição; o que quebrar por ordem é corrigido assim, não remendado |
| A carta **pública** muda de forma junto, para três colunas | É consequência declarada da decisão de o grid ser da variante Guerreiro(a), e não efeito colateral: a carta pública é dessa variante |
| Mudar `--cor-ponto-contorno` alcança o **trio de estrelas** de outra tela | É o conserto pretendido — hoje a borda do trio desaparece no escuro. Declarado na `proposal.md` |
| O saldo passa a aparecer **duas vezes** na carteira da App 05 | Decisão expressa do fundador depois de a duplicação ser levantada. Os rótulos são distintos: "para trocar" na carta, "saldo disponível" na carteira |
| A carta ganha uma quinta leitura, e a montagem fica mais lenta | Entra no `Promise.all` que já existe, não em leitura em série |

## Migration Plan

Nenhuma migração: sem rota nova, sem tabela nova, sem campo novo em projeção pública. A ordem de
execução é a da hierarquia de autoridade — **documentos-fonte primeiro**, depois tokens e glifos,
depois a carta, depois as telas, e os testes junto de cada bloco de código. Reversão é reverter o
_merge commit_: nenhum dado fica em estado novo.

## Open Questions

Nenhuma. Os seis pontos foram elicitados com o fundador em 2026-10-30, e as três razões de contraste
usadas aqui foram medidas, não estimadas.
