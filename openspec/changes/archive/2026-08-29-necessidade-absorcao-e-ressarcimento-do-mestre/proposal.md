## Why

Origem: **PRD-09 — Área do Mestre**, fatia **9** do `openspec/cronograma-de-fatias.md`.
Recorte: `RF-09-56` a `RF-09-60`, `RN-09-12`, `RN-09-13`, `RN-09-23`.

O núcleo já sabe fazer tudo o que a jornada 5.8 do PRD-09 descreve: `GET /necessidades/minhas`
serve ao Mestre a falta das aulas da comunidade dele, `POST /aportes/absorcao` credita no ato e
nasce ressarcível, e `GET /meus-aportes/ressarciveis` devolve a situação do que ele absorveu.
**Nenhuma dessas três rotas tem porta na App 09.** A necessidade que `RN-09-12` manda publicar
só é vista hoje pela vitrine e pela App 03: o Mestre, que é quem propõe a atividade e quem a
jornada põe para cobrir a falta, não a enxerga — e a atividade sem lastro não acontece.

É a última superfície da Área do Mestre que depende só de tela: as rotas estão testadas desde
o PRD-07 e a fatia não abre entidade nem migração.

## What Changes

- A App 09 ganha a área de **recursos**: as **necessidades das aulas da comunidade do Mestre**,
  com o tipo, a quantidade que falta, o valor **em moedas**, o ponto de apoio e o horário da
  aula (`RF-09-56`, `RN-09-12`). A lista vem derivada do núcleo — a App não soma nem recalcula
  a falta.
- Da própria necessidade, o Mestre **assume a absorção em um ato de confirmação**, declarando a
  aula que atende (`RF-09-57`). O aporte nasce em nome dele, marcado como **ressarcível**, e a
  aula é confirmada quando o saldo fecha, sem intervenção de Admin (`RF-09-58`, `RN-09-13`).
- A App 09 ganha o **acompanhamento do ressarcimento**: as absorções do próprio Mestre com tipo,
  quantidade, ponto de apoio, moedas, data e a situação de cada uma — em aberto, ressarcido ou
  não se aplica (`RF-09-59`). É **somente leitura**: não há como exigir, apressar ou reordenar
  o ressarcimento.
- A tela declara, onde o Mestre acompanha o que absorveu, que a plataforma **não guarda dado
  bancário** e que a chave PIX vai **por e-mail ao Admin**, único retorno por e-mail do Ciclo 01
  (`RF-09-60`, `RN-09-23`). Nenhum campo da App 09 coleta ou exibe chave, banco ou conta; o
  comprovante da transferência é anexado pelo Admin, na App 03.
- O núcleo passa a servir o **catálogo de tipos de recurso em leitura ao Mestre**: hoje
  `GET /tipos-de-recurso` é restrito ao Admin, e sem ele a necessidade sai só com identificador
  e a absorção não sabe se o tipo exige valor de origem em reais ou comprovante.

Fora do escopo, como o PRD-09 §3.2 e a §6.8 já excluem: o **empréstimo do acervo permanente**
(`RF-09-61`), que é Ciclo 02; o **registro do ressarcimento** e o anexo do comprovante da
transferência, que são ato de Admin na App 03; e a **homologação de aporte**, que a absorção
dispensa por definição.

## Capabilities

### New Capabilities

Nenhuma. As três capacidades tocadas nasceram no PRD-07 e já estão consolidadas em
`openspec/specs/`; esta change abre as portas do Mestre para elas.

### Modified Capabilities

- `area-do-mestre`: a App 09 ganha a área de recursos — a leitura das necessidades das aulas da
  comunidade dele, a absorção declarando a aula que atende, o acompanhamento da situação do
  ressarcimento e o aviso de que a plataforma não guarda dado bancário (`RF-09-56` a
  `RF-09-60`, `RN-09-12`, `RN-09-13`, `RN-09-23`).
- `catalogo-de-tipos-de-recurso`: a leitura do catálogo, hoje privativa do Admin, passa a
  alcançar o **Mestre** — sem ela `RF-09-56` sai sem nome de tipo e `RF-09-57` não sabe quando
  exigir o valor de origem. A escrita não muda.

## Impact

- **Núcleo (`backend/`)**: apenas `recursos/regra.py` e o docstring da rota — a leitura do
  catálogo passa a aceitar Mestre além de Admin. **Nenhuma migração**: não nasce entidade nem
  coluna. `necessidades/`, `aportes/` e `ressarcimentos/` **não são tocados**: as três rotas do
  recorte já estão implementadas e testadas desde o PRD-07.
- **App 09 (`apps/app-09-mestre/`)**: módulo novo `recursos/`, com a lista de necessidades, o
  ato de absorção e o acompanhamento do ressarcimento. A navegação de áreas ganha uma entrada.
- **Documentação**: a linha da fatia 9 no `openspec/cronograma-de-fatias.md`. Nenhuma decisão
  nova de produto, logo nada muda nos documentos 01–15, no 99 nem no `mkdocs.yml`.
