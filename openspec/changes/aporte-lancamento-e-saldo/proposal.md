## Why

**PRD de origem:** PRD-07 — Economia de recursos e livro-razão. Segunda fatia dele e vigésima
oitava da esteira, na ordem do documento 99 §9.

**Requisitos atendidos:** `RF-07-04` e `RN-07-36` (registro do aporte, com o ponto de apoio em
que entra), `RF-07-05` e `RN-07-03` (conversão em moedas pela tabela vigente **na data do
aporte**), `RF-07-06` e `RF-07-21` (aporte por absorção, que nasce ressarcível), `RN-07-35` (a
absorção credita no ato, sem homologação), `RN-07-16` (quem homologa não é o provedor),
`RF-07-07` (saldo por tipo **e ponto de apoio**), `RF-07-19` e `RN-07-15` (lançamento imutável,
corrigido por ajuste), `RF-07-32` (aporte com período apurado anterior à entrada do livro-razão
no ar), `RF-07-03` (tipo cadastrado no ato do aporte, que a fatia 1 deixou pela metade),
`RF-07-30` e `RN-07-21` (homologação do aporte declarado no pré-cadastro, que converte em moedas
e credita), `RN-07-02` (todo custo atribuído a um provedor), `RN-07-04` (duas casas exatas) e
`RN-07-22` (comprovante em PDF, JPG ou PNG, sem confirmação automática de PIX). Do PRD-01
valem, por herança do roteador e com capacidade própria, `RF-01-02`, `RF-01-03`, `RF-01-16` e
`RF-01-27` — esta change não os redeclara.

Esta é a fatia que **destrava todo o resto do PRD-07**. Reserva na aula, necessidade publicada,
Poder Sustentador, ressarcimento, patrimônio, catálogo avulso e desafio extra penduram, sem
exceção, no lançamento e no saldo que nascem aqui. A fatia 1 entregou o vocabulário — onde o
recurso fica e quanto cada tipo vale; esta entrega o **movimento**.

### O que foi decidido antes desta change

Duas lacunas entre o requisito e o modelo de dados foram ao fundador e voltaram decididas, pelo
fluxo de sempre — documento-fonte, documento 09, PRD:

1. **O aporte declara em que ponto de apoio entra**, e o lançamento de crédito herda esse ponto.
   O saldo é por tipo **e** ponto de apoio e é sempre derivado dos lançamentos, mas nem `Aporte`
   nem `Lancamento` declaravam lugar: o débito achava o ponto pela aula e o crédito não achava
   nenhum, o que deixava o saldo inderivável. Vale para **todas as naturezas**, inclusive
   serviço e financeiro. Nasce a `RN-07-36`.
2. **A absorção credita no ato, sem homologação**, e o campo do Admin homologador nasce vazio. A
   `RN-07-16` vale para as formas que passam por homologação — o registro da gestão e o do
   pré-cadastro. Nasce a `RN-07-35`.

## What Changes

- Nasce o **lançamento**, unidade do livro-razão: natureza (crédito, débito ou ajuste), tipo de
  recurso, ponto de apoio, quantidade, moedas, autor e data. É **somente inserção** — nenhuma
  via o altera nem o remove (`RF-07-19`, `RN-07-15`).
- Nasce o **saldo por tipo de recurso e ponto de apoio**, **derivado** dos lançamentos e nunca
  editável: recontar os lançamentos devolve o mesmo número (`RF-07-07`, PRD-07 §10).
- Nasce o **aporte** registrado por Admin, com provedor, tipo, quantidade, **ponto de apoio de
  entrada**, comprovante e data. Homologado, gera o lançamento de crédito (`RF-07-04`).
- O aporte é convertido em moedas pela **vigência da tabela na data do aporte**, não na data do
  registro — mudar o valor de referência hoje NÃO altera aporte já registrado (`RF-07-05`).
- **Quem homologa não pode ser o provedor**: o Admin que registra um aporte em nome de si mesmo
  é recusado com **403** (`RN-07-16`).
- Nasce o **aporte por absorção** de Mestre ou Admin, que **credita no ato, sem homologação** e
  nasce marcado como **ressarcível**, com situação de ressarcimento **em aberto** (`RF-07-06`,
  `RF-07-21`, `RN-07-35`).
- O aporte aceita **período apurado** anterior à entrada do livro-razão no ar, com comprovante
  anexado — é o que permite lançar retroativamente o custo já incorrido (`RF-07-32`).
- O **comprovante** é aceito em PDF, JPG ou PNG e guardado pela porta de armazenamento já
  existente; nenhuma rota pública o serve (`RN-07-22`, PRD-07 §11).
- O **tipo de recurso passa a declarar se exige comprovante** — atributo que o PRD-07 §8 já
  previa e que a fatia 1 não implementou, porque não havia comprovante algum a exigir.
- **`RF-07-03` fecha aqui**: o Admin cadastra tipo e valor de referência **no ato do registro do
  aporte**, sem interromper o fluxo. A fatia 1 entregou a condição — o cadastro avulso e barato
  —, e esta entrega a composição.
- Erro em lançamento se corrige por **lançamento de ajuste**, que referencia o original e guarda
  motivo e autor; tentar editar um lançamento é recusado com **405** (`RF-07-19`, PRD-07 §9).
- O aporte guarda a **origem do registro** — gestão ou pré-cadastro — e, quando vem do
  pré-cadastro, a **solicitação de origem** que o declarou. Registrá-lo é o ato de
  **homologação** que converte em moedas e credita o que a solicitação só havia declarado
  (`RF-07-30`, `RN-07-21`).
- Rotas: `POST /aportes` (Admin), `POST /aportes/absorcao` (Mestre ou Admin) e
  `POST /lancamentos/{id}/ajuste` (Admin) — todas sob chave de aplicação (PRD-07 §9).

### Fora do escopo

O PRD-07 §3.2 já exclui empréstimo de bancada, reposição solidária, entrega de dados a
pesquisadores, o painel de efetividade do Apoiador, a interface de gestão e a contabilidade
fiscal. Nada disso volta aqui.

O que é **adiado por recorte**, não excluído — cada item é fatia própria:

| Fica para                                 | Porque                                                            |
| ----------------------------------------- | ----------------------------------------------------------------- |
| `RF-07-08`, `RF-07-09` e a `Reserva`      | fatia própria, já destravada pelas decisões do ciclo de vida da aula |
| `RF-07-27`, `RF-07-28` e `RF-07-31`       | necessidade publicada, que só existe depois da reserva            |
| `RF-07-10`, `RF-07-17`, `RF-07-26`        | Poder Sustentador, que é leitura derivada do que nasce aqui       |
| `RF-07-16` e `RF-07-18`                   | prestação de contas pública e o que falta às aulas agendadas      |
| `RF-07-22` a `RF-07-25`                   | ressarcimento; a marca `ressarcível` já nasce nesta fatia         |
| `RF-07-11`, `RF-07-13`, `RF-07-20`, `-48` | patrimônio, ficha de vida e conferência de inventário             |
| `RF-07-33` a `RF-07-46`                   | catálogo avulso e preço em pontos extras                          |
| `RF-07-39` a `RF-07-41` e `RF-07-15`      | desafio extra com lastro, que reserva como a aula reserva         |

**`RF-07-29` já está entregue e não é refeito.** Ele pede que o aporte declarado no
pré-cadastro entre **pendente, com comprovante e sem creditar nada** — e é exatamente o que a
capacidade `fila-de-avaliacao` já faz: `POST /solicitacoes-de-participacao` guarda o aporte
declarado e o comprovante, e nenhum caminho dali credita moeda ou cria cadastro. O que faltava
era o outro lado, o `RF-07-30`, e é ele que entra aqui: o Admin registra o aporte pela rota da
gestão, apontando a **solicitação de origem**, e é esse ato que converte em moedas e credita.
O atributo "solicitação de origem" do PRD-07 §8 é justamente essa ponte.

**Nenhuma rota de leitura entra.** O saldo é estado interno consumido pela reserva; o PRD-07 §9
não declara rota que o devolva, e as consultas que existem lá — prestação de contas, meus
aportes, ressarcíveis — são das fatias adiadas acima.

### O ciclo de vida da aula, decidido depois desta proposta

A `Aula` do núcleo não tinha ciclo de vida, o que deixava o `RF-07-09` sem sujeito. As quatro
decisões vieram do fundador e já estão gravadas nos documentos 04 §1 e 05 §4, no documento 09 e
nos PRDs 01, 02 e 07: a baixa é o **lançamento da atividade realizada**, e a rota
`POST /aulas/{id}/baixa` sai do PRD-07 §9; o cancelamento é de **Admin ou de Mestre da
comunidade** da aula, com motivo, conferido contra o vínculo de comunidade e sem campo novo no
núcleo; e a reserva de aula que passou sem desfecho **não expira sozinha**. Nada disso alcança
esta fatia, que não toca em aula alguma — é a fatia seguinte que executa.

## Capabilities

### New Capabilities

- `livro-razao`: o lançamento imutável — crédito, débito e ajuste — e o saldo por tipo de
  recurso e ponto de apoio, derivado dos lançamentos e nunca editável.
- `aporte`: o registro do que entra, valorado em moedas pela tabela vigente na data, com as
  formas financeira, material, serviço e absorção, o comprovante anexado e a marca de
  ressarcível.

### Modified Capabilities

- `catalogo-de-tipos-de-recurso`: o tipo de recurso passa a declarar se **exige comprovante** —
  atributo previsto no PRD-07 §8 e sem efeito até agora, porque nenhum comprovante existia.

## Impact

- `backend/src/nucleo/livro_razao/`: pasta nova — `modelo.py` do `Lancamento` e do saldo
  derivado, `regra.py` do ajuste e `rotas.py` de `POST /lancamentos/{id}/ajuste`.
- `backend/src/nucleo/aportes/`: pasta nova — `modelo.py`, `regra.py` e `rotas.py` do registro,
  da absorção e da conversão em moedas.
- `backend/src/nucleo/recursos/modelo.py` e `regra.py`: o campo `exige_comprovante` e o cadastro
  de tipo no ato do aporte.
- `backend/src/nucleo/fila/`: nenhuma mudança — o aporte apenas **referencia** a solicitação de
  participação que já existe.
- `backend/src/nucleo/principal.py`: registro dos dois roteadores novos.
- `backend/alembic/versions/`: migration com as tabelas novas e o campo em `tipo_de_recurso`.
- `backend/tests/`: conversão pela vigência da data do aporte e imunidade do aporte já
  registrado à mudança de valor; aporte do próprio Admin recusado com 403; absorção que credita
  sem homologação e nasce ressarcível em aberto; saldo que separa ponto de apoio de ponto de
  apoio; recontagem dos lançamentos que devolve o mesmo saldo; edição e remoção de lançamento
  recusadas dentro e fora do ORM; ajuste que referencia o original e exige motivo; comprovante
  fora de PDF/JPG/PNG recusado; tipo cadastrado no ato do aporte; período apurado retroativo
  aceito; aporte que aponta a solicitação de participação de origem e credita só aí; escrita sem
  chave recusada com 401.
