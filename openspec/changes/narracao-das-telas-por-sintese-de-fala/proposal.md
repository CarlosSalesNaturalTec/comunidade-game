# Proposal

## Why

Parte do público do Ciclo 01 tem 6 anos e ainda não lê com fluência; parte não enxerga; parte
lê com esforço. Hoje nenhuma das aplicações diz nada em voz alta, e a criança que não decifra a
tela depende de um adulto ler por ela — no encontro, com um aparelho por equipe, isso é o
Mestre repetindo a mesma frase em cinco mesas.

Fatia 23 do PRD-04, decisão do fundador de 2026-09-26 (documento 15 §5.1, documento 03 §1.12,
documento 09 §1). Responde em parte a pendência de acessibilidade do documento 09 §2.

Esta change entrega a **camada e a App 01**. As demais aplicações entram depois: nelas o que
falta é roteiro de tela, não desenho novo.

## What Changes

- Nasce `comum/narracao`, camada de **síntese de fala** em pt-BR pelo navegador, disponível às
  oito aplicações. É irmã de `comum/fala` e vai no sentido contrário: aquela transcreve o que a
  criança diz, esta lê a tela em voz alta.
- A camada é a **fronteira do dado**: dos dados do Guerreiro(a), **só o nick** pode ser falado;
  **nunca o nome**, nem qualquer outro campo. A voz é de rede, e é o tipo que impede o resto de
  atravessar.
- Cada tela **declara o que fala** — nunca se extrai do DOM. `Cabecalho` e `Aviso` de
  `comum/react` passam a declarar a narração deles, o que cobre a maior parte das telas sem
  roteiro avulso.
- **Fala sozinha** o texto curto ao entrar na tela; o **texto longo** — conteúdo de missão —
  espera o toque de um botão de alto-falante.
- A App 01 ganha, na **tela inicial**, o botão que liga e desliga, **ligado por padrão**, com o
  estado guardado **no aparelho**. A **primeira interação** traz um botão de iniciar, porque o
  navegador não deixa falar antes de um gesto.
- No **Quiz ao Vivo**, o **enunciado** da pergunta no ar é falado — só ele, não as
  alternativas.
- O texto que a narração fala é marcado `aria-hidden`: ela **não substitui** leitor de tela e
  não concorre com ele.
- Sem rede, cai para voz local do aparelho se houver; não havendo, fica **em silêncio**, sem
  mensagem de erro.

Não é **BREAKING**: nenhuma tela perde comportamento, e o piso de acessibilidade do documento
15 §5 continua cumprido com a narração desligada.

Fora de escopo, declarado: as **outras sete aplicações**, que recebem a camada depois; e
qualquer preferência de narração **guardada no núcleo** — o estado é do aparelho, e vinculá-lo
à pessoa exigiria rota e entidade que nenhum requisito pede.

## Capabilities

### New Capabilities

- `narracao-por-sintese-de-fala`: a camada que lê em voz alta o texto que cada tela declara,
  com o liga e desliga, a fronteira do dado que pode ser falado e o limite perante o leitor de
  tela.

### Modified Capabilities

- `aplicacao-da-aula-presencial`: a tela inicial ganha o botão de liga e desliga e o de
  iniciar; o Quiz ao Vivo fala o enunciado da pergunta no ar; o conteúdo de missão em texto
  ganha o botão de alto-falante.

## Impact

| Onde | O que muda |
| ---- | ---------- |
| `comum/narracao/` | pasta nova: a camada, o provedor React e o catálogo de roteiro |
| `comum/react/Cabecalho.tsx` | declara a narração do título da tela |
| `comum/react/Aviso.tsx` | declara a narração do aviso |
| `comum/trilha/Missao.tsx` | botão de alto-falante no conteúdo em texto |
| `apps/app-01-aula-presencial/src/inicio/TelaInicial.tsx` | o botão de liga e desliga |
| `apps/app-01-aula-presencial/src/App.tsx` | o provedor, ao lado do de sessão |
| `apps/app-01-aula-presencial/src/sessao-de-trabalho/AparelhoDaAula.tsx` | o botão de iniciar |
| `apps/app-01-aula-presencial/src/quiz/TelaDaPartida.tsx` | o enunciado da pergunta no ar |

`comum/narracao` fica **dentro** de `comum/`, que já tem esteira de CI — nenhuma pasta de topo
nova, logo nenhuma esteira nova. Sem rota, sem entidade e sem mudança no núcleo: o navegador
sintetiza, e o Backend API não participa.

`comum/trilha/Missao.tsx` é compartilhada com a App 05, que passa a ter o botão de
alto-falante no conteúdo; sem o provedor montado, a camada fica inerte e a tela não muda.
