## Why

Fatia 9 do PRD-14 (`openspec/cronograma-de-fatias.md`, bloco "PRD-14 — Área do Apoiador"),
atendendo `RF-14-77` a `RF-14-81` e `RN-14-42` a `RN-14-44`. É a última fatia do PRD-14.

O núcleo já aceita o item do catálogo avulso ofertado por Apoiador — nasce pendente, só o Admin
homologa, o preço vem da tabela de referência da gestão e o lastro decide a ativação —, mas a
App 08 não tem por onde ofertar, e quem oferta não tem por onde acompanhar o que aconteceu com
o item: a leitura do catálogo que o núcleo oferece hoje ao Apoiador traz só os itens **ativos**
da comunidade dele, de modo que o item pendente, o recusado e o inativo por falta de lastro ou
de preço somem da vista justamente de quem os ofertou.

A pendência de `RF-14-77` anotada no cronograma é de **dado**, não de desenho: a §14 do PRD-14
registra que a tabela de referência e o piso de 20 estão decididos e que os preços por tipo são
cadastro da gestão. Item de tipo sem preço de referência vigente já nasce inativo no núcleo, e a
tela dirá o que falta — o mesmo tratamento das fatias 1 e 5. Decisão do fundador de 2026-09-02.

## What Changes

- **Acompanhamento da oferta** no núcleo: rota nova que devolve ao Apoiador em sessão os itens
  que **ele** ofertou, em qualquer situação — pendente, homologado com motivo de recusa quando
  houver, ativo ou não, estoque restante, preço vigente, o que falta de lastro e de preço — e a
  **quantidade de trocas** de cada item, agregada (`RF-14-80`).
- A resposta dessa rota NEVER identifica quem trocou: só a contagem (`RF-14-81`, `RN-14-44`).
- Área **Catálogo avulso** na App 08, com a oferta do item — nome, tipo de recurso, quantidade e
  o ponto de apoio que a lastreia — **sem campo de preço**, declarando que o preço vem da tabela
  de referência da gestão e que o item só entra no catálogo depois de homologado pelo Admin
  (`RF-14-77` a `RF-14-79`, `RN-14-42`, `RN-14-43`).
- A mesma área lista as ofertas do Apoiador com situação, marca de ativo, estoque restante e
  quantas trocas, sem qualquer identificação de quem trocou (`RF-14-80`, `RF-14-81`).
- Sem entidade nova e sem mudança de regra no núcleo: cadastro, homologação, lastro e preço já
  estão implementados pela fatia 7 do PRD-07.

## Capabilities

### New Capabilities

Nenhuma.

### Modified Capabilities

- `catalogo-avulso`: ganha a leitura das próprias ofertas pelo Apoiador — toda situação, estoque
  restante e a contagem agregada de trocas, sem identificar quem trocou.
- `area-do-apoiador`: ganha os requisitos da área de catálogo avulso — a oferta sem preço, o
  aviso de que só a homologação do Admin põe o item no catálogo e o acompanhamento agregado.

## Impact

- `backend/src/nucleo/catalogo_avulso/regra.py` e `rotas.py`: a listagem das próprias ofertas e a
  contagem de trocas por item.
- `backend/tests/`: os testes da rota nova.
- `apps/app-08-apoiador/src/catalogoAvulso/` (novo): tela, cliente e testes.
- `apps/app-08-apoiador/src/App.tsx`: área nova na navegação.
- Banco, entidades e migrações: nada muda.
- Documentação: a linha da fatia 9 no `openspec/cronograma-de-fatias.md` e a situação do PRD-14
  em `docs/prds/index.md`.
