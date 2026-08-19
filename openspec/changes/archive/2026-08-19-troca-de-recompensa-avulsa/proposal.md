## Why

Oitava fatia do **PRD-07 — Economia de recursos e ledger**. Atende `RF-07-35`, `RF-07-36`,
`RF-07-37`, `RF-07-38` e `RF-07-46`, e as regras `RN-07-24`, `RN-07-25`, `RN-07-27`,
`RN-07-29` e `RN-07-30`. Do PRD-01, fecha a face de débito do `RF-01-56`, com `RN-01-39` e
`RN-01-40`.

A sétima fatia entregou a régua e o catálogo e deixou dito, na própria capacidade, que a troca
viria em seguida: `catalogo-avulso` termina em "a troca em si é capacidade própria" e
`ponto-extra` em "nesta fatia as duas contas só recebem crédito; a operação de débito nasce com
a troca por recompensa avulsa (PRD-07)". Hoje o `PontoExtra` é uma conta que só sobe, e a
separação entre **acumulado** e **saldo disponível** — invariante 23 do documento 99 §6 — não
tem como se manifestar: nada debita o segundo. Esta fatia entrega a troca e, com ela, o único
débito de ponto extra previsto para o Ciclo 01.

## What Changes

- **Troca** com item, Guerreiro(a), **preço em pontos extras cobrado**, encontro, Mestre que
  entregou e data (`RF-07-35`). O preço cobrado é o da **vigência corrente na data da troca**,
  gravado no registro para que a mudança posterior da tabela não reescreva o histórico
  (`RF-07-46`, `RF-07-38`, `RN-07-29`).
- **Uma operação só, na entrega** (`RF-07-36`, `RN-07-27`): grava a `Troca`, debita o **saldo
  disponível** de pontos extras sem tocar o acumulado (`RF-01-56`, `RN-01-39`, `RN-01-40`),
  decrementa o **estoque** do item e emite o **débito no livro-razão** de uma unidade do tipo
  de recurso do item, no ponto de apoio dele. Não há estado intermediário: a troca não reserva
  item entre encontros.
- **Quatro recusas** (`RF-07-37`, `RN-07-30`, invariantes 9 e 23): item inativo ou sem lastro
  no ato, item sem estoque, Guerreiro(a) de comunidade diferente da do item, e saldo disponível
  de pontos extras menor que o preço cobrado.
- **Nenhuma saída da troca traz moedas nem reais** (`RN-07-24`, `RN-07-25`, invariante 23).
- **Quatro decisões novas gravadas no mesmo PR**, antes de virarem comportamento — no
  documento-fonte de cada uma e no documento 09, em "Já decididos":
  1. O **encontro** que a `Troca` registra é a **`Aula`** do PRD-01, e o núcleo **não verifica
     o estado dela nem a presença** do Guerreiro(a) — mesma linha da decisão da sétima fatia,
     que pôs a janela de troca do `RF-04-49` como garantia da App 01 (documento 02 §8.2).
  2. A troca é registrada em **`POST /aulas/{id}/trocas`, com Mestre em sessão**, num ato só, o
     da entrega. A §9 do PRD-07 lista dezessete rotas e nenhuma de troca (PRD-07 §9).
  3. O **débito emitido pela troca não declara aula**, como o crédito e o ajuste já não
     declaram. `Lancamento.aula` guarda um significado só — a reserva daquela aula foi baixada —
     e `GET /prestacao-de-contas/aulas` segue medindo consumo de atividade (documento 04 §1).
  4. A troca **exige que o Guerreiro(a) seja da comunidade do item**, no mesmo filtro por
     comunidade que já vale no cadastro do item e no resto do núcleo (documento 02 §8.2).

## Capabilities

### New Capabilities

- `troca-de-recompensa-avulsa`: a troca de pontos extras por item do catálogo — as recusas, o
  preço cobrado na data, a operação única de entrega e a leitura do histórico.

### Modified Capabilities

- `ponto-extra`: ganha a **operação de débito** do saldo disponível, que a capacidade já
  anunciava e não tinha. O acumulado segue sem decrescer.
- `catalogo-avulso`: o **estoque decresce pela troca**, fora do caminho de alteração de gestão,
  e o item chega a estoque zero sem ser retirado nem desativado por isso.
- `livro-razao`: o débito passa a ter **duas origens** — a baixa da reserva, que declara a aula,
  e a troca, que não declara. O requisito hoje descreve só a primeira.

## Impact

- **Código**: nasce `backend/src/nucleo/trocas/`. `backend/src/nucleo/ponto_extra/` ganha o
  débito; `backend/src/nucleo/catalogo_avulso/` e `backend/src/nucleo/livro_razao/` são lidos e
  escritos pela operação. Migração Alembic para a tabela da troca.
- **API**: `POST /aulas/{id}/trocas` (Mestre) e a leitura do histórico de trocas. Nenhuma rota
  pública nova.
- **Depende de**: `catalogo-avulso`, `ponto-extra`, `livro-razao`, `aula-e-presenca`,
  `catalogo-de-tipos-de-recurso` e `persona-e-credencial` — todos já consolidados.
- **Documentação**: documentos 02 §8.2 e 04 §1 (fontes das decisões 1, 3 e 4), documento 09
  ("Já decididos"), PRD-07 §§8, 9 e 13, e `docs/prds/index.md` pela situação do PRD-07. Nenhum
  arquivo novo em `docs/`, logo a `nav` do `mkdocs.yml` não muda.

## Fora do escopo

Reproduz o que o PRD-07 §3.2 já exclui, mais o recorte desta fatia:

- **Patrimônio permanente** — `RF-07-11`, `RF-07-13`, `RF-07-20`, `RF-07-48`: fatia própria.
- **Desafio extra** — `RF-07-15`, `RF-07-39`, `RF-07-40`, `RF-07-41`: travado enquanto não
  existir a entidade `DesafioExtra`, que nasce em PRD-09 ou PRD-14.
- **Recompensa de marco**: conquistada, nunca trocada (invariante 23). Depende de
  `RecompensaDeMarco`, que nasce no PRD-09.
- **A janela de troca** do `RF-04-49`: garantia da App 01, decidida na sétima fatia.
- **Interface da troca**: App 01 (PRD-04) e App 05 (PRD-05).
- **Preços concretos de cada item acima do piso**: cadastro da gestão, pendente do calendário
  do Ciclo 01 no documento 09.
