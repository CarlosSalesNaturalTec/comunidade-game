# Design

## Context

Ver `proposal.md` — Why. O que molda o desenho é que os três itens caem em **três componentes
de `comum/`** consumidos por mais de uma aplicação, e não na App 01:

```text
comum/react/SequenciaPaginada  ──┬── comum/trilha/DesafioDeDesbloqueio  (quiz + sondagem)
                                 ├── comum/trilha/Missao                (conteúdos)
                                 └── App 01 TelaDaProgramacao           (conteúdos)
comum/react/MidiaDoNucleo      ──┬── comum/trilha/DesafioDeDesbloqueio
                                 ├── comum/trilha/Missao
                                 └── App 09 (duas telas, em lista — não paginadas)
comum/narracao                 ──── montado só pela App 01
```

Três restrições já decididas que o desenho não reabre:

- `SequenciaPaginada` **não sabe o que renderiza** (decisão 2 do desenho dela). Nada que
  dependa do tipo do item pode descer para dentro dele.
- A narração fala o que a tela **declara**, nunca o que o DOM contém (spec
  `narracao-por-sintese-de-fala`), e a App 05 segue sem montar o provedor: lá o roteiro nasce
  inerte.
- `MidiaDoNucleo` busca em bytes porque nenhuma rota sob `/v1` aceita `<img src>` direto
  (`RF-05-11`); a moldura de tamanho fixo é decisão do fundador de 2026-09-17.

## Goals / Non-Goals

**Goals:**

- Uma única correção em `MidiaDoNucleo` que sirva ao quiz **e** ao conteúdo da missão.
- Narração disparada por **identidade do item**, imune a render repetido.
- O paginador ganha encaixe de ações e trava de controles **sem** passar a conhecer o item.

**Non-Goals:**

- **Cache e pré-busca da mídia.** A exploração mostrou que não existe cache: voltar a uma
  pergunta rebaixa a imagem inteira, e as perguntas já chegam todas juntas, o que permitiria
  pré-buscar a seguinte e quase eliminar a espera em vez de apenas sinalizá-la. O fundador
  decidiu a **trava com indicador** (decisão 4); ampliar para cache é recorte novo e fica como
  sugestão para o fundador, fora desta fatia.
- Tempo limite para a trava. A válvula de escape desta fatia é a **falha da busca**, que já
  tem caminho próprio no componente.
- Roteiro de narração para a App 05, que segue sem provedor.
- Qualquer mudança na App 09: as mídias dela não são paginadas, e o defeito de estado não se
  manifesta lá.

## Decisions

### 1. A narração da pergunta mora no desafio, disparada por `ref` na troca de `pergunta.id`

O roteiro é do `DesafioDeDesbloqueio`, que conhece a pergunta; o paginador segue cego.
O disparo compara `pergunta.id` com um `useRef`, no precedente de `TelaDaPartida`.

- _Alternativa: `useNarrarAoEntrar` com a fala montada._ Descartada — o `useEffect` dele
  dispara por identidade do valor, e a frase montada é string nova a cada render: falaria em
  laço. É o laço que o docblock do próprio hook adverte.
- _Alternativa: o paginador narrar o item._ Descartada — ele não sabe o que o item é.

### 2. A fala reúne enunciado e alternativas numa frase, que nunca entra na tela

A camada recebe uma `Fala`, que é texto. A frase é montada a partir do **array de alternativas
da pergunta** e entregue à síntese; **nenhum nó novo** é acrescentado ao documento.

Isso resolve a tensão que a fatia encostava: a spec exigia `aria-hidden` no que a camada fala, e
a implementação nunca escondeu nada. Com a frase vivendo só na chamada à síntese **não há nó a
esconder**, e o enunciado e as alternativas continuam sendo lidos por leitor de tela como a tela
os apresenta. A spec passou a dizer isso em vez de exigir a marcação.

- _Alternativa: narrar as alternativas em falas separadas, uma por item._ Descartada — `falar()`
  cancela a fala em curso, então só a última seria ouvida.

### 3. A posição sai do paginador por remoção, não por propriedade

Saem o parágrafo da posição e a propriedade `nome`, que só existia para montá-lo, mais a regra
`.cg-sequencia__posicao`.

- _Alternativa: `mostrarPosicao?: boolean`._ Descartada — o fundador escolheu o alcance largo
  (quiz, conteúdo da missão e programação) conhecendo o preço; uma propriedade deixaria
  configuração que nenhum chamador usaria.

**Consequência de acessibilidade, registrada de propósito:** o parágrafo removido tinha
`aria-live="polite"` e era, no caminho dos conteúdos, a única coisa que anunciava a troca de
item. No quiz o `<legend>` segue numerando a pergunta; nos conteúdos **nada** passa a numerar. O
piso do documento 15 §5 continua cumprido — todo conteúdo segue legível e alcançável, e os
controles têm rótulo textual próprio —, mas quem percorre por leitor de tela deixa de saber
quantos itens faltam. Decisão do fundador de 2026-10-16, tomada com esse efeito enunciado.

### 4. O botão de enviar entra por encaixe de ações, e a linha de controles passa a existir por ele

`SequenciaPaginada` recebe `acoes?: ReactNode`, renderizado dentro de
`cg-sequencia__controles`. A guarda `itens.length > 1` passa a valer **só para os controles de
navegação**: havendo `acoes`, a linha é renderizada mesmo com um item só.

Sem isso o quiz de **uma** pergunta perderia o botão de enviar — a linha inteira não renderiza
hoje. É a armadilha mais fácil de entregar quebrada, e o teste dela é obrigatório.

- _Alternativa: o desafio abandonar o paginador e montar a navegação._ Descartada — duplicaria
  navegação já resolvida e faria o quiz divergir do conteúdo da missão.

### 5. O envio condicionado substitui o estado `faltando`, que é removido inteiro

`todasRespondidas` é **derivado** de `perguntas` e `escolhas` no render — não é estado novo. Com
o envio impedido antes do toque, somem `faltando`, o aviso de falta, o salto até a primeira
pendente e a classe `cg-trilha__pergunta--falta`.

A condição vale **só** para `desafio.tipo === "quiz"`: o desafio por declaração não tem pergunta
e seu botão segue sempre disponível.

**O preço, registrado:** o aviso removido era narrado de graça pelo `Aviso`, então a plataforma
hoje **fala** o que falta e passará a não dizer nada — um botão indisponível não se explica.
Isto **reverte** a decisão 4 do desenho da fatia que criou o comportamento, cujo argumento era
que "com uma pergunta por vez, contar quantas faltam manda procurar". O fundador escolheu a
opção A entre três apresentadas, com esse efeito enunciado, e recusou a variante que mantinha
uma linha explicativa ao lado do botão.

### 6. `MidiaDoNucleo` guarda o `id` junto do endereço, e a divergência é o estado de carga

O estado passa a ser um par — o `id` que foi buscado e o endereço resultante. Quando o `id` da
propriedade **difere** do guardado, o componente está carregando: a moldura diz "Carregando…" e
nem a mídia nem o erro do item anterior aparecem.

- _Alternativa: `useEffect` que reinicia o estado na troca de `id`._ Descartada — reiniciar em
  efeito rende um quadro com a mídia antiga sob o item novo, que é exatamente o defeito.
- _Alternativa: `key={pergunta.id}` no chamador._ Descartada — corrigiria só o quiz e deixaria o
  conteúdo da missão com o mesmo defeito, além de pôr em quem monta a correção de um estado que
  é do componente.

`naoAbriu` entra no mesmo par, o que resolve de graça o erro que grudava de um item no seguinte.

### 7. A trava de navegação é informada pelo componente e aplicada pelo chamador

`MidiaDoNucleo` recebe `aoMudarCarregamento?: (carregando: boolean) => void` e o chamador guarda
o estado, passando-o ao paginador como `controlesTravados`. O paginador desabilita avançar e
voltar; as `acoes` **não** são travadas por ele, porque o envio tem condição própria.

Duas quedas obrigatórias, senão a trava tranca:

1. **Falha da busca** reporta `carregando: false` — é a válvula de escape que a spec exige.
2. **Desmontagem** reporta `carregando: false` na limpeza. Sem isso, ir de uma pergunta com
   imagem para uma **sem** imagem desmonta o componente com a trava armada e prende a navegação
   para sempre.

- _Alternativa: o paginador detectar a carga por conta própria._ Descartada — ele não sabe o que
  renderiza.

## Risks / Trade-offs

| Risco | Mitigação |
| --- | --- |
| A trava prende a navegação quando a mídia nunca resolve | Falha e desmontagem reportam fim de carga (decisão 7); ambas com teste próprio |
| Quem percorre conteúdos por leitor de tela perde a noção de quantos faltam | Efeito aceito pelo fundador (decisão 3); controles seguem rotulados e todo conteúdo alcançável |
| O botão indisponível não explica o que falta, para quem tem 6 anos | Efeito aceito pelo fundador (decisão 5); registrado aqui para reabrir com dado de uso, não por suposição |
| Quiz de uma pergunta perder o botão de enviar | Decisão 4 muda a guarda da linha de controles; teste obrigatório do caso de um item |
| A fala repetir a mesma pergunta a cada render | Disparo por `ref` na troca de `id` (decisão 1), com teste que reapresenta o mesmo item |
| `nome` removido quebrar chamador não previsto | Três chamadores de produção, todos neste PR; o TypeScript acusa qualquer outro na esteira |
| Mudança em `comum/` alcançar a App 05 sem recorte próprio | O comportamento é o mesmo para as duas aplicações e a spec que o governa é `area-do-guerreiro`; a App 05 fica só sem a voz |

## Migration Plan

Nenhuma migração de dado: as três mudanças são de apresentação e de estado de componente, e
nenhuma rota, entidade ou contrato de API é tocado. A reversão é o `revert` do PR.

A ordem de implementação segue a dependência entre os componentes — primeiro `comum/react`
(paginador e moldura), depois `comum/trilha` (desafio e missão), depois os chamadores da App 01
—, porque o encaixe de ações e a trava precisam existir antes de quem os usa.
