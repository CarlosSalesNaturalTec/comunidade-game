# Design

## Context

Ver `proposal.md` — Travas e Why. A spec alterada é `camada-visual-comum`, que já declara os
temperamentos, a camada de tema da Arena e a proibição de movimento decorativo.

Esta fatia fecha os três eixos do documento 15 §6 que a fatia do temperamento deixou de fora por
falta de conteúdo. Dois deles estão bloqueados; o desenho abaixo é o que vale quando destravarem, e
o que já dá para fazer antes.

## Goals / Non-Goals

**Goals:**

- A carta como elemento maior das telas de personagem da Arena.
- Imagem de fundo que não fere o contraste medido.
- Retorno de progresso e conquista que informa e desaparece sob `reduced-motion`.

**Non-Goals:**

- Aplicações da Operação.
- Rotação da carta.
- Universo dos personagens, pendente no documento 09.
- Representação visual da Comunidade Virtual, que é da App 06.

## Decisions

1. **O retorno entra como requisito de fato, não de tela.** A regra é "não há retorno sem fato" — o
   que o torna compatível com a proibição de movimento decorativo que a camada já declara, em vez de
   abrir exceção nela. É também o que o princípio 2 do documento 15 pede: o visual representa dado
   real. _Descartado:_ modificar o requisito "A camada não impõe movimento" para abrir exceção à
   Arena — não há exceção a abrir, porque retorno de conquista não é decoração.

2. **O fato fica legível sem o movimento, sempre.** O §5 exige conteúdo legível sem depender de
   movimento, e a conquista é conteúdo. Então o retorno é a segunda via, nunca a primeira: a
   conquista aparece em texto, numeral ou forma, e o movimento a acompanha.

3. **A imagem de fundo é responsabilidade de contraste de quem a põe, e a spec a mede.** Fotografia
   ao fundo é a forma mais fácil de furar o piso de `4,5:1` sem ninguém notar — e o documento 15 §3
   diz que o contraste é medido "para o fundo de apoio da própria coluna". Por isso o requisito não
   diz "cuidado com o contraste": diz que os pisos continuam cumpridos **sobre** a imagem, o que é
   verificável. _Descartado:_ imagem como token de cor, que não se mede.

4. **A tarefa 1 pode rodar antes das travas.** A carta dominando a tela depende só da change da
   carta. As tarefas da imagem e do retorno esperam as duas decisões do fundador, e a tarefa 0 as
   bloqueia explicitamente.

5. **O peso da imagem de fundo entra como conferência, não como número.** O princípio 4 do documento
   15 põe o celular modesto como alvo e o peso de arquivo como requisito de projeto, mas não fixa
   número. Quando a imagem existir, o peso dela se confere contra esse princípio; inventar um limite
   aqui seria criar regra.

## Risks / Trade-offs

- **A fatia ficar aberta por tempo indefinido** → é o custo de registrá-la em vez de esquecê-la; as
  duas travas entram no documento 09, que é a pauta do fundador, e a tarefa 1 entrega algo útil
  sozinha.
- **Imagem de fundo virando decoração** → o requisito diz que nada se perde quando ela não carrega,
  com cenário próprio. Se algo se perder, a imagem estava carregando informação, o que o princípio 3
  proíbe.
- **Retorno de conquista virando animação em toda tela** → "não há retorno sem fato" é cenário de
  aceite, não recomendação.
