## Why

O território é o único bloco da §6.1 do PRD-02 sem nada entregue: a App 03 cria a Comunidade
Virtual desde a primeira fatia e, desde então, a comunidade **nasce vazia e continua vazia** —
não há por onde o Admin cadastrar um local. Sem local cadastrado, o Guerreiro(a) não abre série
de coleta (PRD-08 §12), e a invariante 4 do documento 99 — todo Guerreiro(a) preso a uma
comunidade — não tem onde ser conferida.

O núcleo já entregou tudo o que sustenta esta fatia: a hierarquia de seis níveis
(`local-do-territorio`), a solicitação de novo local e a avaliação dela
(`solicitacao-de-local`), e o vínculo com histórico (`comunidade-virtual`). O que falta é a
gestão — a ponta que o `RF-08-24` chama de "alerta nas suas aplicações" e que hoje só existe na
App 05, do lado de quem pede.

Origem: **PRD-02**, fatia **9** do `openspec/cronograma-de-fatias.md`, §§6.1, 6.2 e 7, com as
rotas de território do **PRD-08** §9.

Requisitos atendidos: `RF-02-15`, `RF-02-16`, `RF-02-17`, `RF-02-21` e `RF-02-22`, sob
`RN-02-06`, `RN-02-21` e `RN-02-22`. Do lado do núcleo, alcança `RF-08-04`, `RF-08-23` e
`RF-08-24` do **PRD-08**, pelas rotas que já existem, e `RF-08-02` na leitura nova do vínculo.

## What Changes

- A **App 03** ganha a área **Território**, com a comunidade escolhida no seletor que as demais
  áreas já usam: a hierarquia dos locais cadastrados, o cadastro de local novo com nível e local
  pai (`RF-02-16`), e a fila das solicitações de novo local, que **alerta enquanto houver
  solicitação em aberto** (`RF-02-21`) e onde o Admin aprova, informando o local pai, ou recusa
  com motivo (`RF-02-22`). As três leituras e as duas escritas são as rotas de `RF-08-04`,
  `RF-08-23` e `RF-08-24`, já no núcleo: **nenhuma regra de território nova**.
- A lista de Guerreiros e Guerreiras da área Personas passa a mostrar a **comunidade vigente e
  a data de início do vínculo**, em leitura (`RF-02-15`). Não há ação de troca: a transferência
  é `RF-08-03`, fora do Ciclo 01, e o `RN-02-06` mantém a tela sem esse caminho.
- A saída de **`GET /v1/guerreiros`** passa a trazer a **comunidade do vínculo vigente e a data
  de início dele**. Hoje nenhuma rota do núcleo expõe o vínculo a quem administra, e sem isso o
  `RF-02-15` não tem o que conferir. Decisão do fundador, 2026-08-27, no precedente da própria
  rota, criada na segunda fatia para servir o `RF-02-01` sem estar na §9: **leitura que serve
  RF já escrito não é regra nova**. Nada é acrescentado à escrita: continua não existindo rota
  que mova o Guerreiro(a) de comunidade (`RF-08-03`, fora do Ciclo 01).
- Nasce **`GET /v1/desafios-de-coleta`**, de Admin, que lista os desafios **publicados** com
  tipo, cadência, vigência, granularidade e a **quantidade de séries ativas** de cada um
  (`RF-02-17`). "Publicado" é o desafio cuja missão pertence a **trilha em situação
  `publicada`** — decisão do fundador, 2026-08-27: o desafio não tem situação própria no
  modelo, e a trilha é a única publicação do domínio. A App 03 apresenta a lista em leitura, no
  Território.
- **Correção de redação do PRD-02**, sem decisão nova: o `RF-02-17` passa a dizer "desafios de
  coleta de trilha publicada", que é o que a resposta acima fixou. Mesmo caminho das três
  correções da fatia 7.
- **Nenhuma entidade nova, nenhuma coluna nova e nenhuma migração.** As duas rotas novas são
  leitura derivada do que já está gravado.

## Capabilities

### New Capabilities

Nenhuma. A fatia é a ponta de gestão de capacidades que já existem.

### Modified Capabilities

- `aplicacao-de-gestao`: a App 03 ganha a área Território — hierarquia e cadastro de locais,
  fila das solicitações de novo local com alerta e desfecho, e a leitura dos desafios
  publicados —, e a lista de Guerreiros e Guerreiras passa a mostrar o vínculo (`RF-02-15`,
  `RF-02-16`, `RF-02-17`, `RF-02-21`, `RF-02-22`, `RN-02-06`).
- `comunidade-virtual`: o núcleo passa a expor ao Admin a leitura do vínculo vigente do
  Guerreiro(a), sem abrir caminho de troca (`RF-02-15`, `RF-08-02`, `RN-02-06`).
- `desafio-de-coleta`: nasce a leitura de Admin dos desafios de trilha publicada, com as séries
  ativas de cada um (`RF-02-17`).

## Impact

- **Backend** — `backend/src/nucleo/personas/` (o vínculo na saída da listagem) e
  `backend/src/nucleo/coletas/` (a listagem de Admin). Nenhuma migração de esquema.
- **Apps** — `apps/app-03-gestao/src/territorio/` (novo) e a lista de Guerreiros e Guerreiras em
  `apps/app-03-gestao/src/personas/`.
- **Reuso, sem recriar** — `POST /v1/locais` e `GET /v1/locais` (`local-do-territorio`),
  `GET /v1/solicitacoes-de-local/abertas` e `POST /v1/solicitacoes-de-local/{id}/avaliacao`
  (`solicitacao-de-local`), o seletor de comunidade e o padrão de tela das áreas Pontos de
  Apoio e Filas, e `VinculoJogador` com o `vinculo_vigente` já mapeado.
- **Documentação no mesmo PR** — `docs/prds/prd-02-frontend-de-gestao.md` (a redação do
  `RF-02-17`, na §6.1) e a linha da fatia 9 em `openspec/cronograma-de-fatias.md`. Sem decisão
  de produto nova e, portanto, sem linha no documento 09; sem arquivo novo em `docs/` e sem
  alteração na `nav` do `mkdocs.yml`. A situação do PRD-02 em `docs/prds/index.md` não muda:
  seguem oito fatias em aberto depois desta.
- **Fora do escopo**, pelo PRD-02 §3.2 — **autoria de desafio de coleta**, que é da App 09: a
  App 03 apenas acompanha o que foi publicado; **transferência de Guerreiro(a) entre
  comunidades**, que existe no modelo e não é operada no Ciclo 01 (`RF-08-03`); e a **cadência
  de coleta**, normatizada no PRD-08. Também fora: o catálogo de **tipos de coleta**
  (`RF-08-05`), que não está no recorte desta fatia.
