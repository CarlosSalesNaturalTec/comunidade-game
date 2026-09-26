# Proposal

**Origem:** PRD-01 (`RF-01-76`, novo), PRD-05 (fatia "Carta e ranking pela sessão, sem série
de coleta"), PRD-02 (fatia 22) e PRD-04 (`RF-04-67`). As duas linhas estão no
`openspec/cronograma-de-fatias.md`. Uma change só, por decisão do fundador de 2026-09-26.

**Recorte:** `RF-01-76` (novo), `RF-05-50` a `RF-05-53`, `RF-05-84`, `RF-04-67`, `RF-02-06`,
`RN-05-16`, `RN-05-21`.

## Why

Dois defeitos de campo, relatados pelo fundador em 2026-09-26.

**A carta do Guerreiro(a) não aparece para quem não abriu série de coleta.** A carta exige
nick e desempenho (documento 11 §8.2), e os dois só existem na `minha_posicao` do ranking
logado, que pede a comunidade na URL. A comunidade é adivinhada de
`GET /v1/series-de-coleta/minhas`, uma leitura de **coleta de território** que nasce vazia
para quem nunca abriu série. Sem ela a carta recusa a montagem e a tela cai no aviso de carta
incompleta — no desfecho da presença da App 01 e na Área do Guerreiro(a). O ranking da turma
da App 05 quebra pela mesma causa, e hoje pede em tela que o Guerreiro(a) abra uma série de
coleta para ver o ranking. Nenhum requisito pede esse acoplamento: ele é resíduo do único
caminho que existia quando a carta foi montada, e está registrado como pendência no
documento 09 §1 (`GET /v1/eu` não devolve nick nem avatar).

**O cadastro de responsável da App 03 é impossível.** A tela manda `POST /v1/responsaveis`
sem corpo, e o núcleo exige o nome desde a change
`2026-08-24-responsavel-consentimento-e-captura-da-imagem` — o nome que sustenta a base legal
do consentimento. Toda tentativa responde 422. As Apps 09 e 01 já mandam o nome; a App 03
ficou para trás e nenhum teste exercia o contrato.

## What Changes

**Identidade do Guerreiro(a) na sessão (`RF-01-76`, novo)**

- `GET /v1/eu` passa a devolver **nick e avatar** do Guerreiro(a) em sessão. Só dele: os
  demais papéis seguem recebendo o que já recebiam.

**Ranking logado pela sessão (`RF-05-52`, `RF-05-53`, `RF-05-84`)**

- O ranking logado da turma passa a **derivar a comunidade do vínculo vigente** de quem
  pergunta, em vez de recebê-la na URL. A rota já busca e confere esse vínculo hoje, e só o
  usa para recusar comunidade alheia: a comunidade na URL é conferência de um dado que o
  núcleo já tem.
- **BREAKING** — `GET /v1/rankings/{comunidade}` dá lugar a `GET /v1/eu/ranking`, com os
  mesmos filtros (trilha **ou** poder, nunca os dois) e a mesma paginação. A rota antiga fica
  sem consumidor e é aposentada; ponto submetido ao fundador na revisão desta proposta.

**Carta e ranking deixam de depender da coleta (`RF-05-50`, `RF-05-51`, `RF-04-67`)**

- A montagem da carta em `comum/carta` passa a tirar nick e avatar de `GET /v1/eu` e o
  desempenho de `GET /v1/eu/ranking`, e **não lê mais** `GET /v1/series-de-coleta/minhas`.
- O ranking da turma da App 05 deixa de adivinhar a comunidade e some com o texto que manda
  abrir série de coleta.
- No desfecho da presença da App 01, a frase de presença registrada deixa de aparecer duas
  vezes na mesma tela, e o aviso de carta incompleta deixa de usar o tom "Em andamento:", que
  anuncia como em curso uma montagem que já terminou.

**Nome do responsável na gestão (`RF-02-06`)**

- O formulário de Responsáveis da App 03 ganha o campo **nome** e passa a enviá-lo, como as
  Apps 09 e 01 já fazem. Correção de defeito: nenhum requisito novo, nenhuma rota nova.

Fora do escopo, pelo que os PRDs já excluem: afrouxar a regra de carta completa — o documento
11 §8.2 exige o desempenho na variante Guerreiro(a), e o fundador descartou esse caminho;
servir a comunidade do Guerreiro(a) em `GET /v1/eu`, que deixaria de ter consumidor com o
ranking derivando-a sozinho; e a lista de responsáveis cadastrados na App 03, que nenhum
requisito desta fatia pede.

## Capabilities

### New Capabilities

Nenhuma.

### Modified Capabilities

- `persona-e-credencial`: a sessão passa a devolver ao Guerreiro(a) o **próprio** nick e
  avatar, a única leitura logada que hoje não os entrega a ele (`RF-01-76`).
- `pontos-niveis-e-badges`: o ranking logado da turma deriva a comunidade do vínculo vigente
  em vez de recebê-la na URL (`RF-05-52`, `RF-05-53`, `RF-05-84`, `RN-05-16`, `RN-05-21`).
- `area-do-guerreiro`: a carta e o ranking da App 05 param de depender de série de coleta
  aberta (`RF-05-50` a `RF-05-53`, `RF-05-84`).
- `aplicacao-da-aula-presencial`: o desfecho da presença apresenta a carta sem depender da
  coleta, sem repetir a frase de presença e sem anunciar como em curso o que já terminou
  (`RF-04-67`).
- `aplicacao-de-gestao`: o cadastro de responsável declara o **nome** (`RF-02-06`).

## Impact

| Onde | O que muda |
| ---- | ---------- |
| `backend/src/nucleo/sessoes/rotas.py` | `EuSaida` e `GET /v1/eu` ganham nick e avatar do Guerreiro(a) |
| `backend/src/nucleo/pontuacao/rotas.py` | `GET /v1/eu/ranking` no lugar de `GET /v1/rankings/{comunidade}` |
| `comum/carta/api.ts`, `comum/carta/CartaDoGuerreiro.tsx` | montagem por `/v1/eu` e `/v1/eu/ranking`; sai a leitura de séries |
| `apps/app-05-guerreiro/src/api/carteira.ts`, `carteira/RankingDaTurma.tsx` | rota nova; sai a adivinhação da comunidade |
| `apps/app-01-aula-presencial/src/entrada/TelaDeEntradaDoGuerreiro.tsx` | frase repetida e tom do aviso |
| `apps/app-03-gestao/src/personas/api.ts`, `personas/FormularioDeResponsavel.tsx` | campo e envio do nome |
| `docs/09`, `docs/prds/prd-01-backend-api.md`, `docs/prds/prd-05-area-do-guerreiro.md` | decisão movida para "Já decididos"; `RF-01-76`; rota na §9 dos dois PRDs |

Sem entidade nova, sem migração e sem mudança no ranking público da vitrine, que deriva de
outra regra e não é tocado.
