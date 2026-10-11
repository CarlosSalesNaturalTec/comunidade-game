# Design

## Context

Ver `proposal.md` — Why. O que o desenho precisa saber do estado atual:

- A App 06 é **Astro com ilhas**: cada seção de leitura é uma ilha `client:visible`, e **prop de
  função não atravessa a fronteira** — por isso `irPara` tem valor padrão (`navegacao/navegar.ts`).
- `useLeitura(ler, chave)` refaz a leitura **pela chave**, não pela função, e **não guarda nada
  no aparelho** (`RN-03-22`).
- O núcleo pagina por **cursor keyset só-pra-frente**: `PaginaDeResultado` traz `itens` e
  `proximo_cursor`, e `contrato_de_listagem` já aceita `cursor` e `tamanho` (padrão 25, teto
  100). **Não há cursor anterior nem total.**
- A listagem de adultos usa keyset `(Persona.criada_em, Persona.id)`; a identificação pública é
  `COALESCE(nick.valor, persona.nome)`, com `Nick` em **tabela própria** e junção por página.
- `paginar_comunidades_publicas` já faz keyset alfabético por `(nome, id)` — é o precedente
  deste desenho.
- Os componentes de `comum/react` que a fatia encosta: `Tabela` (é da Operação, não serve aqui),
  `SequenciaPaginada` (documento 15 §6.4, quatro consumidores fora da vitrine) e
  `CartaDoPersonagem` (continua montando as quatro páginas individuais).

## Goals / Non-Goals

**Goals:**

- Uma única forma de lista para as seis seções, sem duplicar marcação por seção.
- Ordem alfabética estável e paginável no núcleo, sem trocar o contrato de cursor.
- A troca de página sem requisição além da que a página exige, e sem gravar nada.

**Non-Goals:**

- Mexer em `comum/react`. Nenhum outro app lista personagem desta forma.
- Trocar cursor por deslocamento, nem introduzir contagem total.
- Tocar `/vitrine/rankings` e `/v1/comunidades`, que já ordenam como o `RF-03-83` pede.

## Decisions

### 1. A linha é `<ol>`/`<ul>`, nunca `<table>`

A tabela é da Operação (documento 15 §6), e o requisito da Arena a proíbe nominalmente. A linha
sai como item de lista, com a célula que identifica o registro sendo o **elemento acionável** —
nunca a linha inteira, que não recebe foco nem é anunciada.

_Descartado:_ reusar `comum/react/Tabela` — é `<table>` com cabeçalho de coluna e coluna
`recolhida` amarrada ao marco de 768 px, que é a densidade progressiva que o §6 nega à Arena.

### 2. O componente de lista mora na App 06, não em `comum/`

Só a App 06 lista personagem em linha. Entra como componente da própria App, genérico por
`props` sobre o tipo do item, no mesmo desenho de `SecaoDeAdultos.tsx` — que ele substitui.

_Descartado:_ pôr em `comum/react` — precedente da change de 2026-10-11, em que o par de ações
ficou na App 06 justamente por não ter segundo consumidor.

### 3. O acionável é `<a href>`, não `<button>`

Hoje o card usa `<button>` com `window.location.assign`. Com endereço próprio por rota (fatia
9), `<a href>` dá ao visitante abrir em nova aba, copiar o endereço e navegar pelo teclado — e o
`noindex` das páginas de pessoa continua **no destino**, que é onde o requisito o exige.

_Descartado:_ manter `<button>` — custaria afordância sem ganho de privacidade, porque a
exclusão de indexação é declarada pela página alvo, não pela ausência de link.

### 4. "Voltar" é pilha de cursores em memória na ilha

A ilha guarda a sequência de cursores já visitados em `useState`; avançar empilha
`proximo_cursor`, voltar faz `pop`. A chave de `useLeitura` passa a carregar a página
(`"vitrine/mestres#2"`), que é o que refaz a leitura.

_Descartado:_ `?direcao=anterior` no núcleo (keyset invertido) e `?pagina=N` com total — o
primeiro muda contrato público para um ganho que a pilha já dá; o segundo trocaria cursor por
deslocamento em **toda** listagem do núcleo, contra `convencoes-da-api`. Consequência aceita
pelo fundador: não há "página 3 de 12" nem endereço direto para a página N.

### 5. O keyset alfabético ordena pela identificação exibida, com `COALESCE`

`_paginar_adultos_publicos` passa a `LEFT JOIN` em `Nick` e a ordenar por
`(COALESCE(nick.valor, persona.nome), persona.id)`, com o cursor levando `{valor, id}`. Serve
Mestres e Apoiadores — **as duas listas são alfabéticas, então o helper não se bifurca**.

A ordenação precisa dobrar acento, senão "Ávila" cai fora do lugar. O desenho usa **collation
ICU `pt-BR`** na expressão de ordenação, declarada na consulta, e não um `lower()` simples.

_Descartado:_ ordenar na aplicação depois de ler a página — quebra o keyset, que precisa da
mesma ordem no banco; e materializar a identificação numa coluna de `Persona` — seria campo
novo, decisão que nenhum documento tomou.

### 6. A paginação de 10 vem de `tamanho=10` na chamada, não de um padrão novo

`configuracao.paginacao_tamanho_padrao` fica em 25: ele serve às outras sete aplicações. A
vitrine pede `tamanho=10`, que o contrato já aceita e está dentro do teto de 100.

### 7. A seção de Guerreiros perde a listagem, e `listarGuerreiros` sai do cliente

`GET /v1/vitrine/guerreiros` fica no núcleo, sem mudança — precedente de `/vitrine/poderes`.
Sai `listarGuerreiros()` de `api/leituras.ts`, e `SecaoDeGuerreiros.tsx` fica só com
`BuscaPorNick` mais a frase de que a vitrine não lista quem está cadastrado. `GuerreiroPublico`
e `cartaDoGuerreiro` **ficam**: a página individual os usa.

## Risks / Trade-offs

- **O keyset alfabético muda a ordem de uma listagem pública já consumida por terceiros** →
  a ordem nunca foi contratada como estável nesta capacidade, e a spec já dizia "alfabética";
  a change **fecha** a divergência em vez de criar uma. Nenhum cursor sobrevive à troca, e
  cursor inválido já responde 422 com mensagem.
- **Collation ICU pode não estar disponível no Postgres de teste** → se não estiver, a
  alternativa é normalizar na expressão de ordenação; a tarefa de núcleo começa por um teste
  com acento, que acusa o caso antes de o resto ser escrito.
- **Seis seções de 10 linhas na abertura somam 60 linhas** → cada seção é ilha
  `client:visible`, então a leitura só sai quando a seção entra em tela; o peso não muda porque
  a página pedida encolheu de todos os registros para dez.
- **A pilha de cursores se perde ao recarregar** → é o que o `RN-03-22` exige; o visitante volta
  à primeira página, e nenhum requisito promete retomar a posição.
- **Dois requisitos do delta saem com descrição acima de 500 caracteres**, e `openspec validate`
  avisa → eles **substituem** requisitos de igual extensão, preservando o conteúdo; dividi-los
  reestruturaria requisito que o fundador não pediu para reestruturar, e a instrução do OpenSpec
  reserva essa divisão a uma change feita para isso. `validate` normal passa, e o CI não roda
  `--strict`.

## Migration Plan

Não há migração de dados: nenhuma tabela, coluna ou rota muda. O keyset novo é de consulta, e o
cursor é opaco e de vida curta — um cursor emitido antes da troca responde 422, que o cliente já
trata relendo a primeira página.

A documentação já foi entregue (commit `c0e6e05`). Ao arquivar, a linha do cronograma passa de
`em andamento` a `implementado`.
