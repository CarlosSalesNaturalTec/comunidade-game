## Context

Ver `proposal.md` — Why. Três das quatro superfícies desta fatia **já estão implementadas e
testadas no núcleo** desde o PRD-08 e o PRD-01: `POST /v1/desafios-de-coleta`
(`openspec/specs/desafio-de-coleta`), a avaliação e a listagem das solicitações de local em
aberto com o recorte do Mestre (`openspec/specs/solicitacao-de-local`) e `POST /v1/sugestoes`
(`openspec/specs/fila-de-avaliacao`). A fatia é, sobretudo, **frontend**.

O que falta no núcleo são **três leituras**, e nenhuma delas é regra nova: sem elas os
requisitos do PRD-09 não têm como ser cumpridos pela tela. O que este documento decide é onde
cada leitura mora e como o alerta de `RF-09-54` é montado contra o filtro de comunidade
obrigatório do núcleo.

## Goals / Non-Goals

**Goals:**

- Abrir na App 09 as portas do desafio de coleta, do território e da proposta, sobre as rotas de
  escrita que já existem.
- Acrescentar as três leituras que faltam, sem entidade nova e **sem migração**.

**Non-Goals:**

- Mudar qualquer regra de coleta, de local ou da fila única — todas são do PRD-08 e do PRD-01.
- Tocar `locais/`: a avaliação e a listagem já atendem ao Mestre.
- Rota de leitura de desafio para a App 03 ou para a App 05: as duas já existem e não mudam.

## Decisions

1. **O desafio de coleta é lido aninhado em `GET /v1/trilhas/minhas`, não por rota nova.**
   A missão dessa saída já aninha atividades e etiquetas ODS; o desafio é dado da mesma
   estrutura, e é ele que decide se a trilha publica. Uma rota `GET /v1/missoes/{id}/desafios`
   custaria uma chamada por missão na tela da trilha.
   _Descartada:_ rota própria por missão — N+1 na tela que mais importa.

2. **`GET /v1/tipos-de-coleta` é rota nova, paginada, aberta a Mestre e Admin.**
   O catálogo hoje só tem escrita. A leitura devolve todos os tipos com a marca `ativo`, e não
   só os ativos: a App 03 precisará dos dois quando ganhar a tela do catálogo, e a App 09
   filtra os ativos na tela.
   _Descartada:_ devolver só os ativos — fecharia a porta da gestão antes de ela existir.

3. **`GET /v1/sugestoes/minhas` é rota nova, do autor em sessão.**
   Segue o padrão `/minhas` já consolidado no núcleo — `/trilhas/minhas`, `/perguntas/minhas`,
   `/solicitacoes-de-local/minhas`, `/necessidades/minhas`. Ela **não** devolve o `parecer`, que
   é campo da avaliação interna; devolve o `motivo_do_retorno`, que o PRD-01 define como o que
   volta a quem propôs.
   _Descartada:_ relaxar o `GET /v1/sugestoes` de Admin para filtrar pelo autor — misturaria
   dois recortes e dois conjuntos de campos na mesma rota.

4. **O alerta de `RF-09-54` varre as comunidades.** `GET /v1/solicitacoes-de-local/abertas`
   exige o filtro de comunidade (`RF-01-18`), e a trilha do Mestre é bem comum, sem comunidade
   (`RN-01-42`): não há uma comunidade a filtrar. A App 09 lê a lista pública de comunidades
   (`GET /v1/comunidades`, já usada pela vitrine) e consulta as em aberto de cada uma, somando o
   total. O núcleo já recorta pelas trilhas do Mestre, então o que sobra é dele.
   _Descartada:_ dispensar o filtro de comunidade para o Mestre — contraria `RF-01-18`, que é
   requisito do PRD-01, e seria decisão de produto, não de desenho.

5. **A área de território da App 09 não tem seletor de comunidade.** Diferente da App 03, que é
   a tela da gestão de um território, aqui o Mestre olha as trilhas dele, que atravessam
   comunidades. A lista sai agrupada por comunidade, das mesmas consultas que alimentam o
   alerta.

6. **O formulário do desafio não oferece etiqueta ODS.** `RN-09-36` a torna herdada e o núcleo
   recusa desafio que a declare; a tela não repete a trava, só não oferece o campo.

## Risks / Trade-offs

- **A varredura do alerta é N+1 em comunidades** → o Ciclo 01 roda com uma comunidade (Case
  Guerreira Zeferina) e o piso de crescimento é a dezena; as consultas são paralelas e a
  primeira página basta para saber se há alguma. Se o número crescer a ponto de pesar, a saída é
  uma contagem no núcleo, e isso é fatia futura, não desta.
- **Aninhar o desafio em `/trilhas/minhas` engorda uma resposta que já é grande** → a saída
  cresce por uma consulta a mais por trilha, e a alternativa custaria uma chamada por missão. Se
  a resposta virar problema, quem pagina é a lista de trilhas, não o desafio.
- **A leitura de `/tipos-de-coleta` expõe a faixa esperada ao Mestre** → é justamente o que ele
  precisa saber para escolher o tipo, e a faixa não é dado de criança nem de território: é
  cadastro do catálogo.

## Migration Plan

Não há migração: nenhuma entidade e nenhuma coluna nascem. As três tabelas envolvidas —
`tipo_de_coleta`, `desafio_de_coleta` e `sugestao_ou_proposta` — já existem, e as três leituras
são consultas sobre elas. _Rollback:_ remover as duas rotas novas e o aninhamento; nada fica
gravado que dependa deles.
