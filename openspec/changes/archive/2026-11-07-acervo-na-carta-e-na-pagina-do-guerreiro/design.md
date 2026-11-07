# Design

## Context

O acervo público e o portão dele já existem em `leitura-publica-da-vitrine`, e a linha do
portfólio com a produção abrindo, em `aplicacao-da-vitrine`, ambos desde a fatia 12. Esta
fatia só leva os dois à carta e à página do Guerreiro(a). Hoje `_criacoes_na_carta`
(`publico.py`) lê só `CriacaoOriginal`, e o montador do item do acervo vive dentro de
`listar_criacoes_publicas` (`rotas.py`).

## Goals / Non-Goals

**Goals:** um montador só do item do acervo, servindo a listagem e a carta.

**Non-Goals:** paginar o acervo na página — a carta já sai inteira na projeção (spec
`leitura-publica-da-vitrine`, "A composição sai sem consulta por nick").

## Decisions

1. **O montador do item sai de `rotas.py` para `publico.py`.** Uma função recebe as criações e
   as comprovações já filtradas pelos dois portões e devolve os itens, com autoria, trilha e
   desafio hidratados num round-trip por tabela. A listagem continua com o keyset dela e chama
   o montador; `_criacoes_na_carta` chama o mesmo montador e agrupa por Guerreiro(a).
   `CriacaoPublicaSaida` e `FonteDoAcervo` vão junto para `publico.py`, e `rotas.py` reimporta.
   _Descartado:_ uma segunda cópia na carta — é a divergência que o precedente de
   `condicoes_de_criacao_publica` proíbe.
2. **`criacoes` da carta passa a ser `list[CriacaoPublicaSaida]`**, e `CriacaoNaCartaSaida` sai.
   É um superconjunto do formato de hoje (`trilha`, `validada_em`), então nada quebra no
   contrato. _Descartado:_ um campo `acervo` ao lado de `criacoes` — duas listas para a mesma
   coisa.
3. **Agrupar por Guerreiro(a):** a criação em equipe vai para cada integrante da página, como
   hoje; a comprovação vai para o `guerreiro_id` dela. A ordem é decrescente por
   `(data, id)`, a mesma chave da listagem.
4. **App 06: a linha do portfólio sai de `SecaoDoPortfolio` para uma função `linhaDoAcervo`**,
   no mesmo diretório, que a seção e a página usam. A página desenha a lista com a mesma
   marcação de `ListaDeRegistros`, sem paginação, porque os itens já chegaram.
   _Descartado:_ `ListaDeRegistros` na página com uma leitura falsa — esconderia que não há
   leitura nenhuma.
5. **`carta.ts` monta `título — data`.** `CriacaoNaCartaPublica` sai de `leituras.ts`, e
   `GuerreiroPublico.criacoes` passa a `CriacaoPublica[]`.

## Risks / Trade-offs

- [A listagem `/vitrine/guerreiros` faz mais consultas por página] → o montador consulta por
  conjunto, nunca por item; um teste conta as consultas de uma página de cards.
- [A carta de quem tem muitas missões fica longa] → é a decisão do fundador ("em lista");
  nenhum teto se inventa aqui.
