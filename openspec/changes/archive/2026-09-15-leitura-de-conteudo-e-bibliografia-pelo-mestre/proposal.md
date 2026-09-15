## Why

Conserto da fatia 6 do PRD-09 (`openspec/cronograma-de-fatias.md`, linha sem número no bloco
do PRD-09, acrescentada em 2026-09-15). Atende `RF-09-14`, `RF-09-15`, `RF-09-21`, `RF-09-22`,
`RF-09-23`, `RF-09-25` e `RN-09-16`.

**`GET /v1/trilhas/minhas` não devolve o conteúdo nem a bibliografia da missão.** Relatado pelo
fundador: o Mestre anexa imagem (ou texto, vídeo, arquivo, link) como conteúdo de uma missão,
vê a marca de gravação, sai da missão e volta — a lista aparece vazia, como se nada tivesse
sido gravado. O mesmo acontece com a bibliografia. O dado está no banco: `POST
/v1/missoes/{id}/conteudos` e a sessão de envio confirmam normalmente, e a leitura pública
(`GET /v1/trilhas/{id}`) já serve o mesmo conteúdo corretamente. O que falta é só a leitura de
volta ao autor.

A App 09 hoje só mostra o que foi declarado **na própria sessão**, por *merge* local em
memória a cada gravação (`onSalvo`/`onSalva` em `ListaDeMissoes.tsx`) — o mesmo formato vazio
some assim que a árvore é reconstruída do zero por uma nova leitura. `area-do-mestre` já
prescreve "a aplicação SHALL apresentar o conteúdo já escrito" e "SHALL apresentar as entradas
[de bibliografia] já declaradas": a leitura que sustentaria isso entre sessões nunca foi
escrita — mesma origem do defeito que a linha sem número "Leitura do desafio de desbloqueio
pelo Mestre" já consertou para o desafio de desbloqueio, na mesma rota.

## What Changes

- A leitura das trilhas próprias do Mestre (`GET /v1/trilhas/minhas`) passa a trazer, em cada
  missão, o **conteúdo** declarado — texto, imagem, link externo, vídeo e arquivo de apoio, na
  ordem e com a autoria e a fonte já gravadas — e a **bibliografia** declarada — título,
  capítulo e o exemplar apontado, quando houver (`RF-09-14`, `RF-09-15`, `RF-09-21`). É a
  mesma consulta que a leitura pública já usa (`consultar_conteudos_da_missao`), só que também
  para trilha em rascunho ou despublicada, que a rota pública nunca serve.
- A App 09 passa a **reabrir** o conteúdo e a bibliografia já gravados: a lista de conteúdo, o
  bloco de bibliografia e a pré-visualização da missão deixam de depender do que foi declarado
  na sessão corrente para mostrar o que existe (`RF-09-25`).
- O comentário em `api.ts` que descreve a ausência de `conteudos` em `GET /trilhas/minhas`
  como intencional, comparando-a à de `culminancia`, sai: a comparação não vale — `culminancia`
  não tem coluna nenhuma em `TrilhaSaida`, enquanto `conteudos` já existe em `MissaoSaida` e já
  é populado em outra rota.

Fora do escopo:

- `POST /v1/missoes/{id}/conteudos`, o upload retomável e a trava de conteúdo de terceiro sem
  fonte — nada disso está quebrado.
- A leitura pública (`GET /v1/trilhas/{id}`) — já correta.
- A disponibilidade do exemplar e o crédito ao Apoiador na bibliografia (`RF-09-22`,
  `RF-09-23`) continuam derivados na leitura, nunca gravados; esta change só estende **onde**
  a bibliografia passa a ser lida, não como ela é calculada.

## Capabilities

### New Capabilities

Nenhuma. A change conserta o alcance de capacidades que já existem.

### Modified Capabilities

- `trilha-e-missao`: a leitura das trilhas próprias do Mestre passa a trazer o conteúdo e a
  bibliografia de cada missão — hoje a leitura devolve a missão sem nenhum dos dois, mesmo
  quando gravados.
- `area-do-mestre`: as telas de conteúdo, bibliografia e pré-visualização da missão passam a
  reabrir o que já foi declarado em sessão anterior, em vez de nascerem vazias.

## Impact

- `backend/src/nucleo/trilhas/rotas.py` — `listar_minhas_trilhas_rota` passa a chamar
  `_saida_da_missao` com `conteudos=` e `bibliografia=`, como `obter_trilha_publica_rota` já
  faz; a forma da bibliografia ao autor é decidida em design.md.
- `apps/app-09-mestre/src/trilhas/api.ts` — o comentário que descreve a ausência de
  `conteudos` como intencional sai.
- Testes: `backend/tests/test_trilha_rota.py` e
  `apps/app-09-mestre/src/trilhas/trilhas.test.tsx`.
- Documentação: `openspec/cronograma-de-fatias.md` (a linha desta change, já `em andamento`,
  vira `implementado` ao arquivar).
