## Why

Conserto das fatias 2, 6 e 17 do PRD-09 (`openspec/cronograma-de-fatias.md`, linha sem número
no bloco do PRD-09, acrescentada em 2026-09-16). Atende `RF-09-29`, `RF-09-30`, `RF-09-25`,
`RF-09-14` a `RF-09-19`, `RF-09-24`, `RF-05-11` e `RF-05-12`. Relatado pelo fundador em
2026-09-16.

**A culminância declarada não volta ao Mestre autor.** Ele declara, publica, sai da tela e
volta: a trilha diz "Esta trilha ainda não tem a culminância declarada", o painel torna a
apontá-la como pendente enquanto o núcleo publica normalmente, e o botão volta a oferecer
"Declarar culminância" com o formulário **vazio** — redigitar por cima substitui a linha pela
unicidade de `trilha_id` e perde o critério de validação anterior sem aviso. O dado está no
banco: `POST /v1/trilhas/{id}/culminancia` grava, e a leitura pública (`GET /v1/trilhas/{id}`)
já serve a mesma culminância corretamente. Falta só a leitura de volta ao autor —
`GET /v1/trilhas/minhas` não traz o campo. É a quarta ocorrência da mesma classe de defeito,
depois de "Leitura do desafio de desbloqueio pelo Mestre" e "Leitura de conteúdo e
bibliografia pelo Mestre"; esta última chegou a ver a culminância e a deixou de fora de
propósito. `area-do-mestre` já prescreve "apresentar a culminância já declarada e permitir
substituí-la".

**A pré-visualização da missão não mostra o que o Guerreiro(a) verá.** Ela desenha só conteúdo
e bibliografia: nunca lê as **atividades**, embora o Guerreiro(a) as encontre na entrega da
produção; não mostra obrigatoriedade, sondagem nem desafio de desbloqueio; e o crédito sai sem
autor. `RF-09-25` exige a missão "como o Guerreiro(a) a verá".

**Ninguém exibe o arquivo enviado — nem o Guerreiro(a).** Não existe leitura dos bytes do
conteúdo da missão: só a abertura e a confirmação do envio. Por isso a App 05 imprime a
**referência crua** do armazenamento como texto, e a pré-visualização responde "Arquivo
enviado.". `RF-05-11` exige que o Guerreiro(a) percorra "texto, imagens, vídeo, arquivos" —
requisito essencial nunca cumprido.

## What Changes

- `GET /v1/trilhas/minhas` passa a trazer, por trilha, a **culminância declarada** — descrição,
  modalidade e critério de validação —, pela mesma consulta que a leitura pública já faz
  (`RF-09-29`, `RF-09-30`, `RF-09-04`). Trilha sem culminância vem com o campo nulo, distinto
  de ausente.
- O conteúdo da missão passa a **guardar o tipo real do arquivo**, apurado no armazenamento na
  confirmação do envio — hoje ele é consultado e descartado, e sem ele não há como servir os
  bytes com o tipo correto (`RF-09-16`, `RF-09-17`, `RF-09-115`).
- **`GET /v1/conteudos/{id}/arquivo`** passa a servir os bytes do vídeo, da imagem e do arquivo
  de apoio ao **Mestre autor** da trilha e ao **Guerreiro(a) inscrito** nela, e a mais ninguém
  — mesma autorização estrita que a imagem da pergunta do quiz já tem (`RF-05-11`, `RF-09-25`).
- A App 09 **reabre a culminância gravada**: o resumo, o bloco, o painel de pendências e o
  rótulo do botão passam a refletir o banco, não só o que foi declarado na sessão corrente
  (`RF-09-29`, `RF-09-30`, `RF-09-06`, `RF-09-07`).
- A **pré-visualização da missão** passa a apresentar, espelhando a tela do Guerreiro(a):
  título, aviso de missão opcional, conteúdo na ordem com imagem e vídeo **exibidos**, crédito
  e licença, bibliografia, **atividades** e o desafio de desbloqueio (ou a sondagem) em
  leitura (`RF-09-25`).
- A App 05 passa a **exibir** imagem e vídeo do conteúdo, em vez de imprimir a referência do
  armazenamento como texto (`RF-05-11`).

Fora do escopo:

- A gravação da culminância, o upload retomável e a trava de conteúdo de terceiro sem fonte —
  nada disso está quebrado.
- A leitura pública `GET /v1/trilhas/{id}` — já correta na culminância e no conteúdo.
- Extrair para `comum/` um componente único de leitura da missão, partilhado entre a App 05 e a
  pré-visualização: decisão do fundador de 2026-09-16 é espelhar agora e deixar o componente
  comum para fatia própria.
- O teto, a lista de formatos e a medição de consumo de nuvem (`RF-09-18`, `RF-09-20`,
  `RF-09-115`) seguem como estão.

## Capabilities

### New Capabilities

Nenhuma. A change conserta o alcance de capacidades que já existem.

### Modified Capabilities

- `trilha-e-missao`: a leitura das trilhas próprias do Mestre passa a trazer a culminância
  declarada de cada uma — hoje a devolve sem ela, mesmo quando gravada.
- `culminancia`: a culminância declarada passa a ter leitura de volta ao Mestre autor; hoje só
  a leitura pública a serve, e só de trilha publicada.
- `conteudo-da-missao`: o tipo real do arquivo passa a ser gravado na confirmação do envio, e o
  núcleo passa a servir os bytes a quem pode ver a missão — hoje não há leitura alguma deles.
- `area-do-mestre`: a culminância passa a reabrir entre sessões, e a pré-visualização da missão
  passa a apresentar atividades, obrigatoriedade, desafio de desbloqueio, crédito e os arquivos
  exibidos.
- `area-do-guerreiro`: a imagem e o vídeo do conteúdo passam a ser exibidos, em vez de a
  referência do armazenamento aparecer como texto.

## Impact

- **Backend** (`backend/src/nucleo/`): `trilhas/rotas.py` (`TrilhaDoMestreSaida` e
  `listar_minhas_trilhas_rota`), `conteudos/modelo.py`, `conteudos/regra.py`
  (`confirmar_envio` e a regra nova de leitura) e `conteudos/rotas.py` (a rota nova).
- **Migração Alembic**: revisão nova para a coluna do tipo do arquivo em `conteudo_da_missao`.
  Sem ela, a coluna existe no modelo e não no banco — o defeito que
  `2026-09-10-migracao-das-tabelas-de-recompensa-de-marco` já consertou uma vez.
- **App 09** (`apps/app-09-mestre/src/trilhas/`): `api.ts`, `TelaDaTrilha.tsx`,
  `ListaDeMissoes.tsx` e `PreVisualizacaoDaMissao.tsx`.
- **App 05** (`apps/app-05-guerreiro/src/`): `api/trilha.ts` e `trilha/Missao.tsx`.
- **Contrato de API**: uma rota nova sob `/v1`; nenhuma rota existente muda de forma. O campo
  novo em `GET /v1/trilhas/minhas` é aditivo e não quebra consumidor.
- **Documentação**: PRD-09 §9 (a rota nova na tabela de contrato), PRD-05 se a §9 dele listar a
  leitura do conteúdo, `docs/09-topicos-em-aberto-e-sugestoes.md` §1 (o crédito da
  pré-visualização pelo nick, decisão do fundador de 2026-09-16), a linha sem número no bloco
  do PRD-09 de `openspec/cronograma-de-fatias.md` e o documento 99 se alguma relação entre
  documentos mudar.
- **Esteiras**: backend (Ruff e pytest), `apps/app-09-mestre` e `apps/app-05-guerreiro` (Biome
  e Vitest) e documentação (markdownlint, Prettier, Lychee e MkDocs), porque a change toca
  `docs/`.
