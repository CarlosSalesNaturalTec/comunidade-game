## Context

O núcleo já tem a capacidade `catalogo-avulso` inteira: cadastro por Mestre ou Apoiador,
homologação do Admin, lastro por tipo e ponto de apoio, preço lido da tabela de referência e
decremento do estoque na troca. Esta fatia não mexe em nenhuma dessas regras — acrescenta uma
leitura e as telas da App 08. Motivação: `proposal.md` — Why. Requisitos: os deltas em `specs/`.

O débito de ponto extra e o lançamento no livro-razão acontecem na **troca**, já implementada
pela capacidade `troca-de-recompensa-avulsa`; ofertar item não é operação com custo e nada
lança.

## Goals / Non-Goals

**Goals:**

- Dar a quem oferta a visão do item em toda situação, que a leitura por comunidade não dá.
- Manter a contagem de trocas agregada, sem abrir caminho para identificar quem trocou.

**Non-Goals:**

- Tela de homologação do item na App 03 — é da gestão, fora deste recorte.
- Edição, reposição de estoque ou retirada do item pelo Apoiador: o núcleo já as restringe a
  Admin e Mestre vinculado, e o PRD-14 não as pede.

## Decisions

1. **Rota nova `GET /v1/eu/catalogo-avulso`, restrita ao Apoiador**, no mesmo molde de
   `GET /v1/eu/desafios-extras`: filtra pelo **autor** do cadastro, não por comunidade, e traz
   toda situação. A §9 do PRD-14 não lista rota para `RF-14-77` a `RF-14-81`; o prefixo `/eu` é
   o padrão já consolidado da App 08 para "o que é meu".
   _Descartado:_ um filtro `minhas=true` em `GET /v1/catalogo-avulso` — misturaria numa rota só
   a leitura do catálogo (por comunidade, só ativos) com a leitura da autoria (toda situação).
2. **A quantidade de trocas é contada na leitura**, agrupada por item, não guardada em coluna.
   _Descartado:_ contador desnormalizado no item — dado redundante, que a troca já teria de
   manter junto com o decremento do estoque.
3. **Saída própria da rota**, que reaproveita a saída do item e acrescenta só
   `quantidade_de_trocas`. A saída do catálogo permanece como está, para não alargar o payload
   de quem lê o catálogo para trocar.
4. **A tela de oferta declara tipo de recurso e ponto de apoio por identificador**, como a tela
   de proposta de desafio extra já faz.
   _Descartado:_ seletores lendo `GET /v1/tipos-de-recurso` e `GET /v1/pontos-de-apoio` — as duas
   são restritas à gestão, e abri-las ao Apoiador é regra nova, que o PRD-14 não pede.
5. **Duas áreas na navegação** — "Ofertar item" e "Minhas ofertas" —, o mesmo par da proposta e
   do acompanhamento do desafio extra, em `apps/app-08-apoiador/src/catalogoAvulso/`.

## Risks / Trade-offs

- [Sem preço de referência cadastrado para o tipo, o item ofertado nunca ativa] → o núcleo já o
  grava inativo com a marca de preço ausente, e a tela mostra o que falta; é a pendência de dado
  da §14 do PRD-14, não de desenho.
- [O núcleo não amarra a oferta do Apoiador à comunidade do vínculo dele, como faz com o Mestre]
  → comportamento vigente da capacidade, que o PRD-14 não contradiz; "Minhas ofertas" é por
  autoria e mostra o item de qualquer forma.
- [Contar trocas a cada leitura custa uma consulta agregada] → a lista é do próprio Apoiador, de
  poucas dezenas de itens no Ciclo 01; o custo não justifica desnormalizar.
