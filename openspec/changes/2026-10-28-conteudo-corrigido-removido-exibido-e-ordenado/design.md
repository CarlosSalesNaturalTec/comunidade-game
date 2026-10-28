# Design

## Context

Ver `proposal.md` — *Why*. O que o desenho precisa ter em conta:

- `conteudos/rotas.py` tem hoje quatro rotas: criar, abrir envio, confirmar envio e ler os
  bytes. A guarda de autoria é uma só — `conferir_autoria_estrita_da_trilha` —, e as recusas de
  coerência por tipo vivem em `criar_conteudo`.
- `ConteudoDaMissao` não é apontado por nenhuma outra tabela, e `criar_conteudo` é chamado
  apenas pela rota de criação: `duplicar_trilha` não copia conteúdo. Apagar a linha é seguro.
- `ComAutoria` dá a toda linha o `registrado_em` com `server_default=func.now()` — é por ele
  que a migração sabe a sequência de criação, já que o `id` é `uuid4` e não guarda ordem.
- `_referencia_do_arquivo(conteudo)` deriva do id do conteúdo: reabrir a sessão de envio
  sobrescreveria os mesmos bytes.
- `PortaDeArmazenamento.remover` já existe e está implementado nos dois adaptadores, disco e
  nuvem.
- `BlocoRecolhivel` monta os filhos mesmo fechado — só os esconde com `hidden` —, e
  `MidiaDoNucleo` busca os bytes no `useEffect` de montagem.

## Goals / Non-Goals

**Goals:**

- Corrigir, remover, exibir e ordenar o conteúdo sem reabrir nenhuma decisão de conteúdo e
  upload já tomada no documento 03 §11.
- Deixar a ordem verdadeira no banco, inclusive no que já está gravado.
- Não fazer a abertura da tela da trilha buscar byte algum.

**Non-Goals:**

- Tornar `BlocoRecolhivel` preguiçoso: é componente de `comum/`, alcança as oito aplicações e
  merece fatia própria. Esta fatia não depende disso.
- Fazer a rota de leitura dos bytes servir em fluxo. Ela carrega o corpo inteiro em memória
  hoje; é defeito pré-existente, não desta fatia.
- Lixeira, histórico de versões ou valor original do conteúdo corrigido. O molde do artefato
  comprobatório — que guarda o original — existe porque lá o valor foi declarado por um
  **Admin**; aqui autor e editor são a mesma pessoa.

## Decisions

**1. Três portas, no molde que o projeto já usa.** `PATCH /v1/conteudos/{id}` corrige;
`DELETE /v1/conteudos/{id}` remove, com **204**, como `DELETE
/perguntas-do-desbloqueio/{id}`; `POST /v1/conteudos/{id}/ordem` move, com `direcao` em
`cima` ou `baixo`, no molde dos substantivos de ação que `/trilhas/{id}/publicacao` e
`/missoes/{id}/retomada` já firmaram. _Descartado:_ `PUT` do conteúdo inteiro, como a pergunta
do quiz — devolveria tipo e arquivo ao corpo, que `RN-09-45` veda.

**2. A ordem sai do contrato de criação — BREAKING.** `CriarConteudoEntrada.ordem` deixa de
existir e o núcleo atribui `max(ordem) + 1` dentro da missão. Com `extra="forbid"`, mandar o
campo passa a responder **422**; o único cliente que o manda é a App 09, que vem no mesmo PR.
É o que faz `RF-09-126` verdadeiro: enquanto o cliente declarar o número, ele declara 1.
Declarar a ordem passa a ser **mover**, não digitar. _Descartado:_ manter o campo e ignorá-lo —
deixa no contrato um campo que não faz nada.

**3. Mover troca a ordem com o vizinho, e a unicidade fica na regra.** Sem
`UniqueConstraint(missao_id, ordem)`: o modelo já declara que a coerência do conteúdo é
conferida na regra e não no banco, e a restrição obrigaria valor temporário no meio da troca.
A regra é o único escritor da coluna. _Descartado:_ ordem esparsa de 10 em 10 — o número que o
Mestre vê deixaria de corresponder à posição, e ele não vê número nenhum neste desenho.

**4. A migração renumera por `registrado_em`, com desempate por `id`.** Uma revisão do Alembic
reescreve `ordem` de todo conteúdo já gravado, por missão, na sequência de criação. O desempate
pelo `id` deixa o resultado determinístico quando duas linhas nascem no mesmo instante.
_Descartado:_ renumerar por `id` apenas — `uuid4` não guarda ordem alguma.

**5. `abrir_envio` passa a recusar conteúdo que já tem `referencia`.** Sem essa guarda
`RN-09-45` não se sustenta: a referência deriva do id, e um segundo envio sobrescreveria os
bytes do primeiro — trocando o arquivo pela porta dos fundos. A recusa é de validação, com o
motivo dizendo que o caminho é remover e cadastrar outro conteúdo.

**6. Na remoção, os bytes saem antes da linha.** `remover_conteudo` chama
`armazenamento.remover` e só então apaga a linha. Falhando o armazenamento, nada é apagado e a
falha sobe como erro de camada, não como recusa do domínio — invariante 25 do documento 99.
Referência que o armazenamento já não tem conta como removida: o fim pretendido é não haver
bytes. **Nenhum lançamento no livro-razão**, na remoção como no envio: `RF-09-20` e `RN-09-07`
mantêm o armazenamento fora da medição por ato.

**7. O renderizador do conteúdo sai para módulo próprio.** `ConteudoPreVisualizado`, hoje local
a `PreVisualizacaoDaMissao.tsx`, vira módulo e é usado pelas duas superfícies. O comentário que
recusa partilhar componente fala da App 09 **com a App 05**, que podem divergir; dentro da
App 09 as duas telas são o mesmo Mestre vendo o mesmo conteúdo e precisam concordar. A
pré-visualização segue exibindo tudo de imediato, porque é uma missão por ato deliberado; o
bloco de cadastro envolve o renderizador num estado por item, e nenhum `MidiaDoNucleo` monta
antes do comando do Mestre.

**8. O rascunho do texto desce ao conteúdo.** `chaveDoRascunho` passa a levar o id do conteúdo
em correção; a criação continua com a chave da missão. Sem isso, editar um conteúdo e começar
outro na mesma missão sobrescreveria um texto com o outro.

## Risks / Trade-offs

- **A trilha publicada muda sob os pés de quem está no meio dela** → decisão do fundador de
  2026-10-27, na mesma gramática que `desbloqueio-da-missao` já aplica à redeclaração do
  desafio: nada que Guerreiros e Guerreiras gravaram é apagado ou alterado.
- **Bytes removidos não voltam** → a remoção é ato explícito do Mestre autor sobre conteúdo da
  própria trilha, e o Ciclo 01 não tem lixeira. A alternativa — deixar o arquivo órfão — seria
  invisível para sempre, porque o projeto deliberadamente não mede armazenamento.
- **A migração toca toda a tabela** → é uma passada só, por missão, e o estado de partida
  (todos em `ordem = 1`) não tem informação a perder; a sequência de criação é a melhor
  aproximação disponível da ordem que o Mestre pretendia.
- **Exibir arquivo grande ainda passa pelo núcleo** → sob demanda e um por vez, o custo fica no
  patamar que a pré-visualização já pratica. O que esta fatia impede é o pior caso novo: todas
  as missões da etapa buscando arquivo ao abrir a tela.
- **`PATCH` parcial e campo omitido** → omitir campo deixa o valor como está; apagar valor é
  mandá-lo vazio, e aí valem as recusas de coerência do tipo. Sem isso, corrigir a fonte
  apagaria o corpo.

## Migration Plan

1. Revisão do Alembic que renumera `conteudo_da_missao.ordem` por missão, por
   `registrado_em` e `id`. Sem coluna nova, sem restrição nova.
2. Núcleo e App 09 sobem no mesmo PR, porque a decisão 2 é quebra de contrato: a App 09 para
   de mandar `ordem` e o núcleo para de aceitá-lo.
3. Reversão: a revisão não tem volta útil — desfazê-la devolveria todos os conteúdos a
   `ordem = 1`, que é o defeito. `downgrade` fica vazio, com o motivo no comentário.
