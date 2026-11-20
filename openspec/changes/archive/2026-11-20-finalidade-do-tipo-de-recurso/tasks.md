# Tasks

## 1. Núcleo — modelo e migração

- [x] 1.1 `recursos/modelo.py`: enum `FinalidadeDoRecurso` e coluna `finalidade` anulável em
      `TipoDeRecurso`, com `CheckConstraint` nula se, e só se, durável (`RF-07-53`, `RN-07-41`).
- [x] 1.2 Migração Alembic: cria a coluna, grava `recompensa` em todo tipo não durável e cria a
      `CheckConstraint`; o `downgrade` remove as duas (`RF-07-53`, decisão de 2026-11-20).

## 2. Núcleo — catálogo de tipos de recurso

- [x] 2.1 `recursos/regra.py`: cadastro exige a finalidade no não durável e a recusa no durável;
      `alterar_tipo_de_recurso` aceita corrigi-la, com a mesma recusa; nova guarda
      `exigir_finalidade(tipo, esperada, campo)` (`RF-07-53`, `RF-07-01`, `RF-07-51`).
- [x] 2.2 `recursos/rotas.py`: `finalidade` na entrada do `POST` e do `PATCH` e na saída do
      `GET /tipos-de-recurso` (`RF-07-01`, `RF-07-51`).

## 3. Núcleo — as quatro escolhas novas

- [x] 3.1 `aulas/regra.py` (`agendar_aula`): recusa tipo que não seja de consumo do encontro
      (`RF-07-53`, `RF-02-31`).
- [x] 3.2 `recompensas_de_marco/regra.py` (`declarar_recompensa_de_marco`),
      `catalogo_avulso/regra.py` (`cadastrar_item`) e `desafios_extras/regra.py`
      (`propor_desafio_extra`): recusam tipo que não seja de recompensa (`RF-07-53`,
      `RF-09-71`, `RF-09-84`, `RN-07-41`).

## 4. Núcleo — testes

- [x] 4.1 `tests/test_tipo_de_recurso_rota.py` e `tests/test_finalidade_do_tipo_de_recurso.py`: cadastro com e
      sem finalidade, durável com finalidade, correção pelo Admin, 403 do Mestre, leitura com a
      finalidade e correção que não alcança o já gravado (`RF-07-53`, `RF-07-01`, `RF-07-51`).
- [x] 4.2 Teste da migração: consumível passa a recompensa e durável segue nulo (`RF-07-53`).
- [x] 4.3 `tests/test_finalidade_do_tipo_de_recurso.py`, ao lado do teste do tipo desativado:
      nas quatro escolhas, a finalidade errada é recusada com 422 e nada é gravado, e a certa é
      aceita (`RF-07-53`, `RF-02-31`, `RF-09-71`, `RF-09-84`). A fábrica de tipo da
      `conftest.py` ganha a finalidade, e os testes de recompensa, item avulso e desafio extra
      passam a criar o tipo como recompensa.

## 5. Aplicações

- [x] 5.1 App 03, `catalogos/TelaDeCatalogos.tsx` e `recursos/api.ts`: finalidade no
      cadastro do não durável, na lista e na alteração do tipo, com testes (`RF-02-107`,
      `RF-02-113`).
- [x] 5.2 App 03, `agenda/FormularioDeAgendamento.tsx`: o seletor de recursos oferece só consumo
      do encontro, com teste (`RF-02-31`).
- [x] 5.3 App 09, `trilhas/DeclaracaoDeRecompensa.tsx` e `recursos/api.ts`: o seletor oferece só
      recompensa, com teste (`RF-09-71`, `RF-09-84`).

## 6. Documentação

- [x] 6.1 Fatia 11 do PRD-07 como implementada em `openspec/cronograma-de-fatias.md`, com o slug;
      no documento 09, a linha "Consumo do encontro e recompensa de marco" recebe a finalidade
      `recompensa` dada aos tipos existentes na migração. Os PRDs já estão na v12/v13/v8 e não
      mudam.
