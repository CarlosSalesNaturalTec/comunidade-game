# Design

## Context

Ver `proposal.md` — Why. O que molda a abordagem:

- `comum/fala` **já existe** e é o **reconhecimento** — microfone para texto —, importado por
  quatro telas das Apps 01 e 05. Ele se declara "o único módulo que toca a API de fala do
  navegador — a fronteira que garante que o áudio nunca sai do aparelho". A síntese é o
  caminho inverso e precisa da própria fronteira, com o próprio nome.
- `speechSynthesis.speak()` é bloqueado sem gesto prévio da pessoa em navegador móvel, e
  `getVoices()` volta vazio até o evento `voiceschanged` no Chrome.
- As vozes pt-BR de Chrome e Android costumam ser **de rede** (`voice.localService === false`):
  o texto sai do aparelho.
- No App 01 os títulos de tela são literais ou vêm de mapas constantes — nenhum é montado com
  dado de Guerreiro(a). Os **subtítulos** têm interpolação (saldo, sujeito da medição).
- `TelaDaPartida` sonda a partida a cada 2 s e recebe a mesma pergunta em cada leitura.

## Goals / Non-Goals

**Goals:**

- Uma fronteira que o **tipo** defende: entregar o nome à narração não deve compilar.
- Cobrir a maior parte das telas sem escrever roteiro tela a tela.
- A camada inerte por omissão: aplicação sem provedor montado não muda de comportamento.

**Non-Goals:**

- Escolher voz, velocidade ou tom pela pessoa. Nenhum requisito pede, e cada controle a mais é
  uma decisão a mais na tela da Arena.
- Fila de falas. Uma tela fala uma coisa; a seguinte cancela a anterior.
- Roteiro das outras sete aplicações.

## Decisions

### 1. `comum/narracao`, não `comum/fala`

Nome próprio, porque `comum/fala` já é o reconhecimento e é importado por quatro telas.
Renomear o par para `comum/fala/reconhecimento` e `comum/fala/sintese` seria mais simétrico,
mas mexeria em quatro importações de duas aplicações para ganhar simetria de pasta — custo sem
requisito. Fica para quando alguma delas for tocada por outro motivo.

### 2. A fronteira é um tipo, não um comentário

A camada NÃO expõe `falar(texto: string)`. Expõe uma fala declarada:

```ts
type Fala = { texto: string; nick?: string };
```

O `texto` é a frase declarada pela tela e pode conter o marcador `{nick}`; a substituição
acontece **dentro** da camada. Não há campo para nome, nascimento, comunidade ou vínculo —
entregá-los não tem por onde.

Descartado o `falar(string)` cru: uma interpolação no ponto de chamada põe o nome na rede sem
que nada reclame, e foi assim que o 422 da dimensão do descritor sobreviveu um mês. A regra
precisa estar onde o compilador a lê.

Limite honesto, declarado aqui para a leitura seguinte não supor garantia que não existe: o
tipo impede o **campo**, não uma interpolação que alguém escreva dentro de `texto`. O que
fecha esse resto é o roteiro viver num **catálogo de constantes** (decisão 4), revisável num
arquivo só.

### 3. Provedor React, ao lado do de sessão

`ProvedorDeNarracao` envolve a aplicação em `App.tsx`, como `ProvedorDeSessao` já faz, e
entrega um gancho às telas. Estado do provedor: ligado ou não (em `localStorage`), armado ou
não (o gesto), e a voz escolhida. Sem provedor montado, o gancho não fala — é o que mantém a
App 05 inalterada enquanto ela não receber o roteiro dela.

### 4. O roteiro é catálogo de constantes, e o cabeçalho já o dispensa

`Cabecalho` e `Aviso` narram a propriedade que **já recebem**. Isso cobre a maior parte das
telas sem edição. Ler uma prop declarada por quem montou a tela não é extrair do DOM: o
documento 15 §5.1 veda ler o que o navegador renderizou, e é o contrário disto.

O **subtítulo fica de fora** do que se narra por padrão: é onde mora a interpolação, e narrar
saldo e sujeito não é o que a decisão pediu. Tela que quiser mais declara `narracao`.

Frase que não sai de uma prop existente vive num catálogo de constantes da aplicação, com
`{nick}` como único buraco.

### 5. A voz se escolhe uma vez, depois de `voiceschanged`

A camada espera o evento, prefere voz `pt-BR`, e entre as candidatas prefere a **local** —
não por privacidade do texto da plataforma, que a decisão já liberou, mas porque ela funciona
sem rede. Não havendo pt-BR alguma, a camada **cala**: voz em outro idioma lendo português
não é acessibilidade, é ruído.

### 6. O armar é um estado, não um truque

O botão de iniciar chama `speak()` com um enunciado vazio dentro do próprio gesto — é isso que
libera o motor — e marca o provedor como armado. Descartado tentar falar e detectar a falha:
o navegador não a reporta de forma confiável, e a tela ficaria sem saber se falou.

### 7. O quiz fala por `id` de pergunta, não por leitura

`TelaDaPartida` já guarda `perguntaIdConhecidaRef` para saber quando a pergunta trocou. A fala
entra **nesse mesmo ponto**, não num efeito sobre o objeto da pergunta: a sondagem devolve
objeto novo a cada 2 s e um efeito por identidade falaria trinta vezes por minuto.

### 8. `aria-hidden` no que existe para a voz

O texto que só existe para ser falado — quando houver — sai marcado. O que já está escrito na
tela e é narrado **não** é escondido do leitor de tela: escondê-lo tiraria da tela o que o
leitor precisa. O que se evita é o texto **duplicado** para a narração.

## Risks / Trade-offs

- **Voz de rede leva o texto da plataforma a um terceiro** → decisão do fundador de
  2026-09-26, com a trava do nick. A nota pública e o documento 03 §12 já a declaram.
- **Sala com cinco aparelhos narrando** → é o que a distinção curto/longo mitiga. Se o
  encontro mostrar que até o título em cinco mesas incomoda, o ajuste é o padrão por
  aplicação, e ele cabe numa prop do provedor.
- **`localStorage` indisponível** — aba privativa, dado de site bloqueado — → leitura e escrita
  em `try/catch`, e a falha cai no padrão ligado. Nada quebra.
- **Aparelho modesto sem voz pt-BR** → a camada cala, por decisão 5. Vale conferir no primeiro
  encontro quais vozes os aparelhos reais oferecem; é o tipo de coisa que só o campo diz.
- **Teste sem `speechSynthesis`** → o jsdom não o tem. O padrão já existe em
  `comum/fala/fala.test.ts`, que instala um construtor falso com `vi.stubGlobal`; a camada
  nova segue o mesmo caminho.

## Open Questions

Nenhuma.
