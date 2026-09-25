# Design

## Context

Ver `proposal.md` — Why. As specs alteradas são `camada-visual-comum`, que ganha os quatro
componentes, e `area-do-guerreiro`, no progresso e na carta do próprio Guerreiro(a).

O documento 15 §§8.1 a 8.4 fixa os valores e o documento 11 §8.2 diz o que cada variante exibe. Esta
fatia decide **qual variante entra primeiro**, **onde ela aparece** e **o que fazer com as duas
famílias de badge que o documento declara e o núcleo não tem**.

## Goals / Non-Goals

**Goals:**

- Carta, emblema de nível, seis silhuetas de badge e glifo de poder em `comum/react`.
- A variante Guerreiro(a) aparecendo na Área do Guerreiro(a), com dado completo.
- Nível contável e badge por silhueta no progresso.

**Non-Goals:**

- As variantes Mestre, Apoiador e Comunidade Virtual.
- Carta nas Apps 01, 03, 06, 07 e 08.
- Rotação da carta e retorno de conquista.
- Página individual de cada card.

## Decisions

1. **A variante Guerreiro(a) entra primeiro, e entra onde o dado está completo.** A Área do
   Guerreiro(a) já consome tudo o que o documento 11 §8.2 exige da variante: avatar, nick, badges e
   poderes com níveis por `GET /v1/eu/progresso` e `GET /v1/eu/trilhas`, criações originais pelo
   portfólio. _Descartado:_ entregar as quatro variantes de uma vez — três delas dependem de rotas
   de outras aplicações e de tabelas de exibição distintas.

2. **A tela das equipes da App 01 não recebe carta.** A rota devolve integrante por avatar, nick e
   papel; a carta exigiria badges, poderes e desempenho, que ela não traz. O fundador já decidiu o
   caso análogo na linha "Apresentação da lista de comunidades da App 03" do documento 09: lista
   densa, não carta, porque **carta pela metade contraria o documento 11**. A regra sobe para a spec,
   como requisito da camada, em vez de ficar decidida caso a caso.
   _Corrige_ o recorte previsto no cronograma, que dizia aplicar nas telas de equipe.

3. **As seis silhuetas são entregues; quatro têm dado.** O `TipoDeBadge` do núcleo tem quatro
   valores — nível, valores e causas, autoria, protagonismo. O documento 15 §8.3 declara **seis**
   famílias: faltam **conquista** e **território**. O território já é previsto no núcleo como fatia
   futura, pelo comentário do próprio modelo. Desenhar as seis agora custa o mesmo e evita que a
   fatia do território tenha de voltar aqui. _Pendência no documento 09_ para as duas famílias sem
   tipo no núcleo.

4. **O emblema acompanha o numeral, não o substitui.** O documento 15 §8.2 pede o nível contável, e
   o §5 proíbe significado só por forma como proíbe só por cor. As marcas contáveis entram ao lado
   do numeral que já existe. _Descartado:_ trocar o numeral pelas marcas.

5. **O glifo de poder vem do sistema de ícone da fatia do temperamento Arena.** Grade de `24` px,
   traço de `2` px, `currentColor` — os mesmos valores, o mesmo componente. Um glifo por poder do
   catálogo mais o genérico do §8.4, que é o que deixa o catálogo crescer pela gestão sem tocar em
   código.

6. **O raio da carta vem do temperamento, não da carta.** O `--raio-carta` ganhou consumidor: é
   aqui. Na Operação vale `4` px e na Arena `12`, como o §8.1 fixa, e a carta só lê o token.

## Risks / Trade-offs

- **Carta pela metade escapando numa tela futura** → virou requisito da camada, com cenário próprio,
  em vez de decisão de quem monta a tela.
- **Silhueta sem dado parecer funcionalidade morta** → as duas famílias sem tipo no núcleo entram no
  documento 09 e a `proposal` diz quais são; o genérico do glifo garante que nada quebre.
- **Emblema de nível 5 confundido com moldura decorativa** → a moldura fechada é a marca de Mestre
  Aprendiz e leva rótulo, como o §5 exige de todo significado.
